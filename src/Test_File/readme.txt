Test Zamanı : 20260330_135358
Port        : COM6

=================================================================
  [1] Baseline           size=10MB  chunk=256B  pattern=random  timeout=60s
=================================================================
[*] 10 MB test verisi oluşturuluyor (desen: random)...
[*] Veri hazır: 10,485,760 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 256 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 10,485,760 byte  ->  received_data.bin / sent_data.bin
[00:09]  Gönderilen:   10,485,760  Alınan:   10,420,320  100.0%  Anlık: 1.10 MB/s  Ort: 1.11 MB/s  [63 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 10.00 MB
Geçen Süre           : 9.27 s
Ort. Hız             : 1.079 MB/s
Gönderilen Byte      : 10,485,760
Alınan Byte          : 10,485,760
Kayıp Byte           : 0
Karşılaştırılan      : 10,485,760
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [2] Büyük chunk        size=10MB  chunk=8192B  pattern=random  timeout=60s
=================================================================
[*] 10 MB test verisi oluşturuluyor (desen: random)...
[*] Veri hazır: 10,485,760 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 8192 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 10,485,760 byte  ->  received_data.bin / sent_data.bin
[00:09]  Gönderilen:   10,485,760  Alınan:   10,424,400  100.0%  Anlık: 1.09 MB/s  Ort: 1.11 MB/s  [59 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 10.00 MB
Geçen Süre           : 9.27 s
Ort. Hız             : 1.079 MB/s
Gönderilen Byte      : 10,485,760
Alınan Byte          : 10,485,760
Kayıp Byte           : 0
Karşılaştırılan      : 10,485,760
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [3] Küçük chunk        size=10MB  chunk=8B  pattern=random  timeout=90s
=================================================================
[*] 10 MB test verisi oluşturuluyor (desen: random)...
[*] Veri hazır: 10,485,760 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 8 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 10,485,760 byte  ->  received_data.bin / sent_data.bin
[00:57]  Gönderilen:   10,446,200  Alınan:   10,444,800   99.6%  Anlık: 0.18 MB/s  Ort: 0.17 MB/s  [1 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 10.00 MB
Geçen Süre           : 57.83 s
Ort. Hız             : 0.173 MB/s
Gönderilen Byte      : 10,485,760
Alınan Byte          : 10,485,760
Kayıp Byte           : 0
Karşılaştırılan      : 10,485,760
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [4] 1 byte chunk       size=1MB  chunk=1B  pattern=random  timeout=120s
=================================================================
[*] 1 MB test verisi oluşturuluyor (desen: random)...
[*] Veri hazır: 1,048,576 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 1 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 1,048,576 byte  ->  received_data.bin / sent_data.bin
[00:48]  Gönderilen:    1,043,836  Alınan:    1,043,713   99.5%  Anlık: 0.02 MB/s  Ort: 0.02 MB/s  [0 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 1.00 MB
Geçen Süre           : 48.57 s
Ort. Hız             : 0.021 MB/s
Gönderilen Byte      : 1,048,576
Alınan Byte          : 1,048,576
Kayıp Byte           : 0
Karşılaştırılan      : 1,048,576
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [5] Büyük veri         size=100MB  chunk=256B  pattern=random  timeout=180s
=================================================================
[*] 100 MB test verisi oluşturuluyor (desen: random)...
[*] Veri hazır: 104,857,600 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 256 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 104,857,600 byte  ->  received_data.bin / sent_data.bin
[01:30]  Gönderilen:  104,857,600  Alınan:  104,823,360  100.0%  Anlık: 0.98 MB/s  Ort: 1.10 MB/s  [33 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 100.00 MB
Geçen Süre           : 90.89 s
Ort. Hız             : 1.100 MB/s
Gönderilen Byte      : 104,857,600
Alınan Byte          : 104,857,600
Kayıp Byte           : 0
Karşılaştırılan      : 104,857,600
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [6] Dev chunk          size=50MB  chunk=65536B  pattern=random  timeout=120s
=================================================================
[*] 50 MB test verisi oluşturuluyor (desen: random)...
[*] Veri hazır: 52,428,800 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 65536 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 52,428,800 byte  ->  received_data.bin / sent_data.bin
[01:00]  Gönderilen:   52,428,800  Alınan:   52,426,948  100.0%  Anlık: 0.00 MB/s  Ort: 0.83 MB/s  [1 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 50.00 MB
Geçen Süre           : 60.61 s
Ort. Hız             : 0.825 MB/s
Gönderilen Byte      : 52,428,800
Alınan Byte          : 52,426,948
Kayıp Byte           : 1,852
Karşılaştırılan      : 52,426,948
Pozisyonel Uyumsuz   : 50,403,001  [!] Kayıp nedeniyle güvenilmez
Bit Hata Oranı       : N/A (byte kaybı var)
Sonuç                : BASARISIZ
==================================================
[!] BYTE KAYBI VAR: USB/UART FIFO taşması.
Öneri: --chunk-size 512 ile tekrar dene.
Veya FPGA'da RTS/CTS akış kontrolünü etkinleştir.

=================================================================
  [7] Sıfır verisi       size=10MB  chunk=256B  pattern=zeros  timeout=60s
=================================================================
[*] 10 MB test verisi oluşturuluyor (desen: zeros)...
[*] Veri hazır: 10,485,760 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 256 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 10,485,760 byte  ->  received_data.bin / sent_data.bin
[00:09]  Gönderilen:   10,485,760  Alınan:   10,424,400  100.0%  Anlık: 1.10 MB/s  Ort: 1.11 MB/s  [59 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 10.00 MB
Geçen Süre           : 9.27 s
Ort. Hız             : 1.078 MB/s
Gönderilen Byte      : 10,485,760
Alınan Byte          : 10,485,760
Kayıp Byte           : 0
Karşılaştırılan      : 10,485,760
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [8] Artan byte         size=10MB  chunk=256B  pattern=increment  timeout=60s
=================================================================
[*] 10 MB test verisi oluşturuluyor (desen: increment)...
[*] Veri hazır: 10,485,760 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 256 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 10,485,760 byte  ->  received_data.bin / sent_data.bin
[00:09]  Gönderilen:   10,485,760  Alınan:   10,424,400  100.0%  Anlık: 1.09 MB/s  Ort: 1.11 MB/s  [59 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 10.00 MB
Geçen Süre           : 9.27 s
Ort. Hız             : 1.079 MB/s
Gönderilen Byte      : 10,485,760
Alınan Byte          : 10,485,760
Kayıp Byte           : 0
Karşılaştırılan      : 10,485,760
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=================================================================
  [9] Çarpışma deseni    size=10MB  chunk=256B  pattern=alternating  timeout=60s
=================================================================
[*] 10 MB test verisi oluşturuluyor (desen: alternating)...
[*] Veri hazır: 10,485,760 byte
[*] COM6 portu 12,000,000 baud hızında açılıyor...
[*] Chunk boyutu: 256 byte  |  Max ilerleme: 64 KB
[*] Test başlıyor: 10,485,760 byte  ->  received_data.bin / sent_data.bin
[00:09]  Gönderilen:   10,485,760  Alınan:   10,420,320  100.0%  Anlık: 1.10 MB/s  Ort: 1.11 MB/s  [63 KB önde]
[*] Veri bütünlüğü doğrulanıyor...
==================================================
UART Veri Bütünlüğü Test Raporu
==================================================
Port                 : COM6 @ 12,000,000 baud
Veri Boyutu          : 10.00 MB
Geçen Süre           : 9.27 s
Ort. Hız             : 1.079 MB/s
Gönderilen Byte      : 10,485,760
Alınan Byte          : 10,485,760
Kayıp Byte           : 0
Karşılaştırılan      : 10,485,760
Bit Hatası           : 0
Bit Hata Oranı       : 0.000000e+00
Sonuç                : BASARILI
==================================================

=====================================================================================
   #  Senaryo             Sonuç        Süre(s)   Hız(MB/s)   KayıpByte   BitHata
=====================================================================================
   1  Baseline            BASARILI        9.27       1.079           0         0
   2  Büyük chunk         BASARILI        9.27       1.079           0         0
   3  Küçük chunk         BASARILI       57.83       0.173           0         0
   4  1 byte chunk        BASARILI       48.57       0.021           0         0
   5  Büyük veri          BASARILI       90.89       1.100           0         0
   6  Dev chunk           BASARISIZ      60.61       0.825        1852         ?
   7  Sıfır verisi        BASARILI        9.27       1.078           0         0
   8  Artan byte          BASARILI        9.27       1.079           0         0
   9  Çarpışma deseni     BASARILI        9.27       1.079           0         0
=====================================================================================

  Sonuç: 8/9 BASARILI


