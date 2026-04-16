"""
Yüksek Hızlı UART Veri Bütünlüğü Testi
FPGA: Arty A7 @ 96 MHz, UART Echo @ 12 Mbps

Kullanım:
    python UART_ECHO.py --port COM6 --size 100
    python UART_ECHO.py --port COM6 --size 10 --chunk-size 512
"""

import os
import time
import threading
import argparse
import serial

# ─── Defaults ────────────────────────────────────────────────────────────────
DEFAULT_PORT     = "COM6"
BAUDRATE         = 12_000_000
DEFAULT_CHUNK    = 256          # 256 byte per write (--chunk-size ile değiştirilebilir)
BUFFER_SIZE      = 1024 * 1024   # 1 MB OS serial buffer
FPGA_FIFO_DEPTH  = 65536         # FPGA RX FIFO derinliği (byte) — kullanıcı tarafından ayarlandı
MAX_AHEAD        = FPGA_FIFO_DEPTH  # Writer bu kadar byte ileride olabilir (FIFO taşmasını önler)
RECV_READ_SIZE   = 65536         # 64 KB per blocking read
TIMEOUT_S        = 5             # serial read timeout (saniye)
OUTPUT_FILE      = "received_data.bin"
SENT_FILE        = "sent_data.bin"
# ─────────────────────────────────────────────────────────────────────────────


def build_test_data(size_mb: int, pattern: str = "random") -> bytes:
    total = size_mb * 1024 * 1024
    print(f"[*] {size_mb} MB test verisi oluşturuluyor (desen: {pattern})...", flush=True)
    if pattern == "random":
        data = os.urandom(total)
    elif pattern == "zeros":
        data = bytes(total)
    elif pattern == "ones":
        data = bytes([0xFF] * total)
    elif pattern == "alternating":
        tile = bytes([0xAA, 0x55])
        data = (tile * ((total // 2) + 1))[:total]
    elif pattern == "increment":
        tile = bytes(range(256))
        data = (tile * ((total // 256) + 1))[:total]
    else:
        raise ValueError(f"Bilinmeyen desen: {pattern!r}. "
                         "Geçerli: random, zeros, ones, alternating, increment")
    print(f"[*] Veri hazır: {len(data):,} byte", flush=True)
    return data


def writer_thread(ser: serial.Serial,
                  data: bytes,
                  sent_counter: list,
                  recv_counter: list,
                  write_done_event: threading.Event,
                  chunk_size: int,
                  sent_file):
    """
    Veriyi chunk'lar halinde gönderir.
    Backpressure: reader'dan MAX_AHEAD byte'dan fazla ilerleyemez.
    """
    total = len(data)
    offset = 0
    try:
        while offset < total:
            # Gerçek backpressure: gönderilen - alınan farkı MAX_AHEAD'i geçmesin
            while (sent_counter[0] - recv_counter[0]) > MAX_AHEAD:
                time.sleep(0)

            end = min(offset + chunk_size, total)
            chunk = data[offset:end]
            ser.write(chunk)
            sent_file.write(chunk)
            offset = end
            sent_counter[0] = offset
    finally:
        write_done_event.set()


def reader_thread(ser: serial.Serial,
                  total_expected: int,
                  recv_buffer: bytearray,
                  recv_counter: list,
                  write_done_event: threading.Event,
                  out_file):
    """
    Bloklu ser.read() ile gelen veriyi okur — polling yok, sleep yok.
    İlk byte gelince bekleyenlerin tamamını agresif şekilde drainler.
    """
    drain_retries = 3  # Writer bittikten sonra kaç timeout daha bekle
    while len(recv_buffer) < total_expected:
        # 1 byte bloklu bekle (veri gelene kadar veya timeout)
        first = ser.read(1)
        if first:
            # Veri geldi — bekleyen her şeyi hemen oku
            waiting = ser.in_waiting
            if waiting > 0:
                rest = ser.read(waiting)
                chunk = first + rest
            else:
                chunk = first
            recv_buffer.extend(chunk)
            out_file.write(chunk)
            recv_counter[0] = len(recv_buffer)
            drain_retries = 3  # Veri geldi, retry sayacını sıfırla
        else:
            # Timeout: veri gelmedi
            if write_done_event.is_set():
                drain_retries -= 1
                if drain_retries <= 0:
                    break   # Birden fazla timeout — artık veri gelmeyecek


def verify(sent: bytes, received: bytearray):
    """
    Kayıp byte ve pozisyonel bit hatalarını ayrı ayrı döndürür.

    DİKKAT: Kayıp byte varsa (lost > 0), positional_errors hizalama kayması
    nedeniyle şişirilmiştir — gerçek bit hata sayısı DEĞİLDİR.
    """
    lost_bytes    = len(sent) - len(received)
    compare_len   = min(len(sent), len(received))
    pos_errors    = sum(
        1 for a, b in zip(sent[:compare_len], received[:compare_len]) if a != b
    )
    return lost_bytes, pos_errors, compare_len


def print_report(port, baudrate, data_size_mb, elapsed,
                 sent_bytes, recv_bytes, lost_bytes, pos_errors, compare_len):
    total_bits  = compare_len * 8
    ber         = pos_errors / total_bits if (total_bits > 0 and lost_bytes == 0) else float('nan')
    speed_mbs   = (sent_bytes / 1024 / 1024) / elapsed if elapsed > 0 else 0.0
    result      = "BASARILI" if lost_bytes == 0 and pos_errors == 0 else "BASARISIZ"

    print()
    print("=" * 50)
    print("  UART Veri Bütünlüğü Test Raporu")
    print("=" * 50)
    print(f"  Port                 : {port} @ {baudrate:,} baud")
    print(f"  Veri Boyutu          : {data_size_mb:.2f} MB")
    print(f"  Geçen Süre           : {elapsed:.2f} s")
    print(f"  Ort. Hız             : {speed_mbs:.3f} MB/s")
    print(f"  Gönderilen Byte      : {sent_bytes:,}")
    print(f"  Alınan Byte          : {recv_bytes:,}")
    print(f"  Kayıp Byte           : {lost_bytes:,}")
    print(f"  Karşılaştırılan      : {compare_len:,}")

    if lost_bytes > 0:
        print(f"  Pozisyonel Uyumsuz   : {pos_errors:,}  [!] Kayıp nedeniyle güvenilmez")
        print(f"  Bit Hata Oranı       : N/A (byte kaybı var)")
    else:
        print(f"  Bit Hatası           : {pos_errors:,}")
        ber_str = f"{ber:.6e}" if pos_errors > 0 else "0.000000e+00"
        print(f"  Bit Hata Oranı       : {ber_str}")

    print(f"  Sonuç                : {result}")
    print("=" * 50)

    if lost_bytes > 0:
        print()
        print("  [!] BYTE KAYBI VAR: USB/UART FIFO taşması.")
        print("      Öneri: --chunk-size 512 ile tekrar dene.")
        print("      Veya FPGA'da RTS/CTS akış kontrolünü etkinleştir.")


def main():
    parser = argparse.ArgumentParser(
        description="Yüksek hızlı UART veri bütünlüğü testi (FPGA Echo projesi)"
    )
    parser.add_argument("--port",       default=DEFAULT_PORT,
                        help=f"Seri port (varsayılan: {DEFAULT_PORT})")
    parser.add_argument("--size",       type=int, default=40,  
                        help="Test verisi boyutu MB cinsinden (varsayılan: 100)")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK, dest="chunk_size",
                        help=f"Gönderim chunk boyutu byte cinsinden (varsayılan: {DEFAULT_CHUNK})")
    parser.add_argument("--pattern",    default="random",
                        choices=["random", "zeros", "ones", "alternating", "increment"],
                        help="Test verisi deseni (varsayılan: random)")
    args = parser.parse_args()

    test_data   = build_test_data(args.size, args.pattern)
    total_bytes = len(test_data)

    print(f"[*] {args.port} portu {BAUDRATE:,} baud hızında açılıyor...", flush=True)
    try:
        ser = serial.Serial(
            port=args.port,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT_S,
            write_timeout=TIMEOUT_S,
        )
        ser.set_buffer_size(rx_size=BUFFER_SIZE, tx_size=BUFFER_SIZE)
    except serial.SerialException as e:
        print(f"[!] Port açılamadı: {e}")
        return

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    recv_buffer  = bytearray()
    sent_counter = [0]
    recv_counter = [0]
    write_done   = threading.Event()

    print(f"[*] Chunk boyutu: {args.chunk_size} byte  |  Max ilerleme: {MAX_AHEAD // 1024} KB", flush=True)
    print(f"[*] Test başlıyor: {total_bytes:,} byte  ->  {OUTPUT_FILE} / {SENT_FILE}", flush=True)

    start_time = time.perf_counter()

    with open(OUTPUT_FILE, "wb") as out_file, open(SENT_FILE, "wb") as sent_file:
        t_writer = threading.Thread(
            target=writer_thread,
            args=(ser, test_data, sent_counter, recv_counter, write_done, args.chunk_size, sent_file),
            daemon=True,
        )
        t_reader = threading.Thread(
            target=reader_thread,
            args=(ser, total_bytes, recv_buffer, recv_counter, write_done, out_file),
            daemon=True,
        )

        t_writer.start()
        t_reader.start()

        # İlerleme göstergesi (4 Hz)
        prev_sent = 0
        prev_time = start_time
        while t_writer.is_alive() or t_reader.is_alive():
            now     = time.perf_counter()
            sent    = sent_counter[0]
            recv    = recv_counter[0]
            pct     = (sent / total_bytes) * 100 if total_bytes > 0 else 0
            elapsed = now - start_time
            avg_spd = (sent / 1024 / 1024) / elapsed if elapsed > 0 else 0
            dt      = now - prev_time
            inst_spd = ((sent - prev_sent) / 1024 / 1024) / dt if dt > 0 else 0
            ahead   = (sent - recv) // 1024
            prev_sent = sent
            prev_time = now
            mins, secs = divmod(int(elapsed), 60)
            print(
                f"\r  [{mins:02d}:{secs:02d}]  Gönderilen: {sent:>12,}  Alınan: {recv:>12,}  "
                f"{pct:5.1f}%  Anlık: {inst_spd:.2f} MB/s  Ort: {avg_spd:.2f} MB/s  [{ahead} KB önde]",
                end="", flush=True
            )
            time.sleep(0.25)

        t_writer.join()
        t_reader.join()

    elapsed_total = time.perf_counter() - start_time
    print()

    ser.close()

    print("[*] Veri bütünlüğü doğrulanıyor...", flush=True)
    lost, pos_errors, compared = verify(test_data, recv_buffer)

    print_report(
        port=args.port,
        baudrate=BAUDRATE,
        data_size_mb=args.size,
        elapsed=elapsed_total,
        sent_bytes=len(test_data),
        recv_bytes=len(recv_buffer),
        lost_bytes=lost,
        pos_errors=pos_errors,
        compare_len=compared,
    )


if __name__ == "__main__":
    main()
