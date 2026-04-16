High-Speed UART Echo Controller (12 MBaud)
This repository contains a high-performance UART (Universal Asynchronous Receiver-Transmitter) implementation optimized for extreme baud rates, reaching up to 12 MBaud. The design features an optimized FIFO buffering system and custom clock management to ensure zero-loss data transmission.

Project Overview
Standard UART communication typically operates at rates like 115200. This project pushes the boundaries of asynchronous serial communication by achieving a stable 12 MBaud rate. A key challenge was managing the data flow between the high-speed serial interface and the internal processing logic, which was resolved through architectural optimizations.

Key Features:
Extreme Throughput: Achieves a reliable 12 MBaud data rate.

Bottleneck Mitigation: Integrated an optimized FIFO (First-In-First-Out) buffer system. To prevent data overflow during high-speed bursts, the FIFO width and depth were strategically increased, ensuring a seamless data stream.

Custom Clock Management: The system operates on a precise 96 MHz clock frequency, specifically tailored to provide the ideal sampling resolution for 12 MBaud (exactly 8 samples per bit).

Hardware-Level Echo: Low-latency data loopback (Echo) implemented directly in FPGA logic.

Technical Specifications
FPGA Architecture: Xilinx Artix-7 (XC7A35T-1CSG324C)

Baud Rate: 12,000,000 bits per second (12 MBaud)

System Clock: 96 MHz (Internal PLL/MMCM generated)

Buffering: High-bandwidth FIFO with optimized bit-width for bottleneck prevention.

Protocol: 8-N-1 (8 Data bits, No parity, 1 Stop bit)

Development Tool: Vivado Design Suite

Architectural Solution: Overcoming Throughput Bottlenecks
During initial testing at 12 MBaud, standard buffer sizes caused data congestion. To solve this, the FIFO architecture was redesigned:

Increased Width/Depth: The buffer parameters were expanded to handle larger data bursts without dropping packets.

Clock Synchronization: By shifting the system frequency to 96 MHz, we achieved a perfect integer division for the 12 MBaud rate, significantly reducing sampling errors.
