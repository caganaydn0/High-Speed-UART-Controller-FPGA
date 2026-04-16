





"""
UART Echo Test Koşucusu
Tüm senaryoları sırayla çalıştırır, sonuçları özetler ve log'a kaydeder.

Kullanım:
    python test_runner.py
    python test_runner.py --port COM6
    python test_runner.py --port COM6 --skip 4 5
"""

import subprocess
import sys
import re
import os
import glob
import threading
import argparse
import datetime
import io
import contextlib
from typing import IO, Any

# ─── Senaryolar ──────────────────────────────────────────────────────────────
#  timeout: senaryo bu süre (saniye) içinde bitmezse TIMEOUT olarak raporlanır
SCENARIOS = [
    {"id": 1, "name": "Baseline",        "size": 10,  "chunk": 256,   "pattern": "random",      "timeout": 60},
    {"id": 2, "name": "Büyük chunk",     "size": 10,  "chunk": 8192,  "pattern": "random",      "timeout": 60},
    {"id": 3, "name": "Küçük chunk",     "size": 10,  "chunk": 8,     "pattern": "random",      "timeout": 90},
    {"id": 4, "name": "1 byte chunk",    "size": 1,   "chunk": 1,     "pattern": "random",      "timeout": 120},
    {"id": 5, "name": "Büyük veri",      "size": 100, "chunk": 256,   "pattern": "random",      "timeout": 180},
    {"id": 6, "name": "Dev chunk",       "size": 50,  "chunk": 65536, "pattern": "random",      "timeout": 120},
    {"id": 7, "name": "Sıfır verisi",    "size": 10,  "chunk": 256,   "pattern": "zeros",       "timeout": 60},
    {"id": 8, "name": "Artan byte",      "size": 10,  "chunk": 256,   "pattern": "increment",   "timeout": 60},
    {"id": 9, "name": "Çarpışma deseni", "size": 10,  "chunk": 256,   "pattern": "alternating", "timeout": 60},
]
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT      = os.path.join(PROJECT_DIR, "UART_ECHO.py")


def cleanup_previous_results() -> None:
    """Önceki test çalıştırmalarının dosyalarını temizler."""
    removed = []
    for fname in ["received_data.bin", "sent_data.bin"]:
        p = os.path.join(PROJECT_DIR, fname)
        if os.path.exists(p):
            os.remove(p)
            removed.append(fname)
    for p in glob.glob(os.path.join(PROJECT_DIR, "test_results_*.log")):
        os.remove(p)
        removed.append(os.path.basename(p))
    if removed:
        print(f"[*] Temizlendi: {', '.join(removed)}", flush=True)


def _stream_output(proc: "subprocess.Popen[bytes]", log_fh: IO[str]) -> str:
    """
    Binary passthrough: subprocess çıktısını doğrudan sys.stdout.buffer'a yazar.
    Bu sayede \\r terminalde native olarak işlenir (satır üstüne yazar, akma olmaz).
    Log dosyasına temiz (\\r soyulmuş) satırlar yazar.
    """
    raw_data = bytearray()
    assert proc.stdout is not None

    while True:
        chunk = proc.stdout.read(64)
        if not chunk:
            break
        raw_data.extend(chunk)
        sys.stdout.buffer.write(chunk)   # ham bayt → terminal \r'yi kendisi işler
        sys.stdout.buffer.flush()

    text = raw_data.decode("utf-8", errors="replace")

    # Log: \r ve \n'e göre böl → her progress güncellemesi ayrı eleman olur
    # Sadece son progress satırını tut (log'da akma olmaz)
    seen_progress: dict[str, str] = {}
    log_lines: list[str] = []
    for raw_line in re.split(r'[\r\n]+', text):   # hem \r hem \n ayracı
        clean = raw_line.strip()
        if not clean:
            continue
        if re.match(r'\[\d{2}:\d{2}\]', clean):
            seen_progress["progress"] = clean   # sadece son halini tut
        else:
            if "progress" in seen_progress:
                log_lines.append(seen_progress.pop("progress"))
            log_lines.append(clean)
    if "progress" in seen_progress:
        log_lines.append(seen_progress["progress"])

    for line in log_lines:
        log_fh.write(line + "\n")
    log_fh.flush()

    return text


def parse_results(text: str) -> dict[str, Any]:
    def _float(pattern: str) -> float | None:
        m = re.search(pattern, text)
        return float(m.group(1)) if m else None

    def _int(pattern: str) -> int | None:
        m = re.search(pattern, text)
        return int(m.group(1).replace(",", "").replace(".", "")) if m else None

    result_match = re.search(r"Sonuç\s*:\s*(BASARILI|BASARISIZ)", text)
    return {
        "result":     result_match.group(1) if result_match else "BILINMIYOR",
        "elapsed_s":  _float(r"Geçen Süre\s*:\s*([\d.]+)\s*s"),
        "speed_mbs":  _float(r"Ort\. Hız\s*:\s*([\d.]+)\s*MB/s"),
        "sent_bytes": _int(  r"Gönderilen Byte\s*:\s*([\d,\.]+)"),
        "recv_bytes": _int(  r"Alınan Byte\s*:\s*([\d,\.]+)"),
        "lost_bytes": _int(  r"Kayıp Byte\s*:\s*([\d,\.]+)"),
        "bit_errors": _int(  r"Bit Hatası\s*:\s*([\d,\.]+)"),
    }


def run_scenario(scenario: dict[str, Any], port: str, log_fh: IO[str]) -> dict[str, Any]:
    cmd = [
        sys.executable, SCRIPT,
        "--port",       port,
        "--size",       str(scenario["size"]),
        "--chunk-size", str(scenario["chunk"]),
        "--pattern",    scenario["pattern"],
    ]
    timeout: int = scenario.get("timeout", 300)  # type: ignore[assignment]

    header = (
        f"\n{'='*65}\n"
        f"  [{scenario['id']}] {scenario['name']:<18} "
        f"size={scenario['size']}MB  chunk={scenario['chunk']}B  "
        f"pattern={scenario['pattern']}  timeout={timeout}s\n"
        f"{'='*65}"
    )
    print(header, flush=True)
    log_fh.write(header + "\n")
    log_fh.flush()

    proc = subprocess.Popen(
        cmd,
        env={**os.environ, "PYTHONUTF8": "1"},  # UTF-8 çıktı zorla → regex Türkçe bulabilsin
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,              # unbuffered binary — veri anında gelsin
    )

    # Timeout: süre aşılırsa süreci öldür
    killed = threading.Event()

    def _kill() -> None:
        killed.set()
        try:
            proc.kill()
        except OSError:
            pass

    timer = threading.Timer(timeout, _kill)
    timer.start()
    try:
        full_output = _stream_output(proc, log_fh)
        proc.wait()
    finally:
        timer.cancel()

    if killed.is_set():
        timeout_msg = (f"\n  [!] TIMEOUT — senaryo {timeout}s içinde tamamlanamadı, durduruldu.")
        print(timeout_msg, flush=True)
        log_fh.write(timeout_msg + "\n")
        log_fh.flush()
        metrics: dict[str, Any] = {
            "result":       "TIMEOUT",
            "elapsed_s":    float(timeout),
            "speed_mbs":    None,
            "sent_bytes":   None,
            "recv_bytes":   None,
            "lost_bytes":   None,
            "bit_errors":   None,
        }
    else:
        metrics = parse_results(full_output)

    metrics["scenario_id"]   = scenario["id"]
    metrics["scenario_name"] = scenario["name"]
    metrics["returncode"]    = proc.returncode
    return metrics


def print_summary_table(results: list[dict[str, Any]]) -> None:
    print("\n" + "=" * 85)
    print(f"  {'#':>2}  {'Senaryo':<18}  {'Sonuç':<10}  "
          f"{'Süre(s)':>8}  {'Hız(MB/s)':>10}  "
          f"{'KayıpByte':>10}  {'BitHata':>8}")
    print("=" * 85)
    for r in results:
        lost  = str(r["lost_bytes"])       if r["lost_bytes"]  is not None else "?"
        berrs = str(r["bit_errors"])       if r["bit_errors"]  is not None else "?"
        speed = f"{r['speed_mbs']:.3f}"   if r["speed_mbs"]   is not None else "?"
        elaps = f"{r['elapsed_s']:.2f}"   if r["elapsed_s"]   is not None else "?"
        print(
            f"  {r['scenario_id']:>2}  {r['scenario_name']:<18}  "
            f"{r['result']:<10}  {elaps:>8}  {speed:>10}  "
            f"{lost:>10}  {berrs:>8}"
        )
    print("=" * 85)
    passed  = sum(1 for r in results if r["result"] == "BASARILI")
    timeout = sum(1 for r in results if r["result"] == "TIMEOUT")
    print(f"\n  Sonuç: {passed}/{len(results)} BASARILI"
          + (f"  |  {timeout} TIMEOUT" if timeout else "") + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UART_ECHO.py tüm senaryoları çalıştır ve özetle"
    )
    parser.add_argument("--port",  default="COM6",
                        help="Seri port (varsayılan: COM6)")
    parser.add_argument("--skip",  nargs="*", type=int, default=[],
                        metavar="N",
                        help="Atlanacak senaryo numaraları (örn: --skip 4 5)")
    args = parser.parse_args()

    # Önceki test dosyalarını temizle
    cleanup_previous_results()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path  = os.path.join(PROJECT_DIR, f"test_results_{timestamp}.log")

    print(f"[*] Log dosyası: {log_path}")
    print(f"[*] Port: {args.port}")
    if args.skip:
        print(f"[*] Atlanan senaryolar: {args.skip}")

    all_results: list[dict[str, Any]] = []
    with open(log_path, "w", encoding="utf-8") as log_fh:
        log_fh.write(f"Test Zamanı : {timestamp}\n")
        log_fh.write(f"Port        : {args.port}\n")
        if args.skip:
            log_fh.write(f"Atlananlar  : {args.skip}\n")

        for scenario in SCENARIOS:
            if scenario["id"] in args.skip:
                msg = f"\n[ATLANDI] Senaryo {scenario['id']} — {scenario['name']}"
                print(msg, flush=True)
                log_fh.write(msg + "\n")
                continue
            metrics = run_scenario(scenario, args.port, log_fh)
            all_results.append(metrics)

    print_summary_table(all_results)

    # Özet tabloyu log'a da yaz
    with open(log_path, "a", encoding="utf-8") as log_fh:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_summary_table(all_results)
        log_fh.write(buf.getvalue())

    print(f"[*] Tam log: {log_path}")


if __name__ == "__main__":
    main()
