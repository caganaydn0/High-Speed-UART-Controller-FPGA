"""
Sent ve Received binary dosyalarını byte-byte karşılaştırır.
Fark varsa pozisyon, gönderilen ve alınan değerleri gösterir.
"""

SENT_FILE = "sent_data.bin"
RECV_FILE = "received_data.bin"
CHUNK     = 1024 * 1024  # 1 MB bloklar halinde oku

def compare():
    with open(SENT_FILE, "rb") as f_sent, open(RECV_FILE, "rb") as f_recv:
        sent_size = f_sent.seek(0, 2)
        recv_size = f_recv.seek(0, 2)
        f_sent.seek(0)
        f_recv.seek(0)

        print(f"Sent dosya boyutu   : {sent_size:,} byte")
        print(f"Recv dosya boyutu   : {recv_size:,} byte")

        if sent_size != recv_size:
            print(f"BOYUT FARKI         : {abs(sent_size - recv_size):,} byte")

        compare_len = min(sent_size, recv_size)
        error_count = 0
        max_display = 20  # ilk 20 hatayı detaylı göster
        offset = 0

        while offset < compare_len:
            s_block = f_sent.read(CHUNK)
            r_block = f_recv.read(CHUNK)
            block_len = min(len(s_block), len(r_block))

            for i in range(block_len):
                if s_block[i] != r_block[i]:
                    error_count += 1
                    if error_count <= max_display:
                        pos = offset + i
                        print(
                            f"  HATA #{error_count:>4}  |  Pozisyon: {pos:>12,}  |  "
                            f"Sent: 0x{s_block[i]:02X}  |  Recv: 0x{r_block[i]:02X}"
                        )
                    elif error_count == max_display + 1:
                        print(f"  ... (daha fazla hata var, sayma devam ediyor)")

            offset += block_len

        # Sonuç
        print()
        print("=" * 55)
        if error_count == 0 and sent_size == recv_size:
            print("  HATA YOK — ILETIM BASARILI")
        else:
            print(f"  TOPLAM FARKLI BYTE : {error_count:,}")
            bit_errors = 0
            # tekrar oku ve bit bazında say
            f_sent.seek(0)
            f_recv.seek(0)
            offset = 0
            while offset < compare_len:
                s_block = f_sent.read(CHUNK)
                r_block = f_recv.read(CHUNK)
                block_len = min(len(s_block), len(r_block))
                for i in range(block_len):
                    if s_block[i] != r_block[i]:
                        bit_errors += bin(s_block[i] ^ r_block[i]).count('1')
                offset += block_len
            print(f"  TOPLAM BIT HATASI  : {bit_errors:,}")
            print(f"  BIT HATA ORANI     : {bit_errors / (compare_len * 8):.6e}")
            print("  ILETIM BASARISIZ")
        print("=" * 55)


if __name__ == "__main__":
    compare()
