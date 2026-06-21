# Lexicon 480L Service Manual — Chapter 4: Circuit Description

This chapter is a guide to the organization and function of the various circuit blocks within the 480L. It is provided as an aid to qualified service personnel and is not intended to serve as a primer in digital and analog circuitry.

> **Note:** Throughout this chapter, three different methods are used to indicate hexadecimal numbers:
>
> - `474FH`
> - `10h`
> - `$C0015`
>
> All of these indicate a hexadecimal number.

---

## 4.1 Organization

The circuit descriptions are presented in the following order:

- **4.2** HSP (High Speed Processor) board
- **4.3** Host Processor – Rev. 1
- **4.4** Host Processor – Rev. 2 and up
- **4.5** Motherboard
- **4.6** Power Supply
- **4.7** LARC
- **4.8** SME board (Optional)

---

## 4.2 High Speed Processor Board

### 4.2.1 Overview

The HSP board is a digital signal multiprocessor system composed of two identical self-contained signal processing subsystems. Each subsystem has five functional sections:

1. Slave Processor
2. Writable Control Store
3. Microcode Pipeline
4. Digital Signal Processor
5. Digital Audio I/O

The Slave Processor receives programs from the host processor board, which writes them into the slave's memory using Direct Memory Access (DMA). After a program is written the slave is released and executes the program in its memory.

The slave first writes the microprogram for the Digital Signal Processor (DSP) into the Writable Control Store (WCS). Thereafter the slave dynamically updates the microcode store with new values of offsets and coefficients. The slave accesses the WCS during one of the four phases of the high speed processor. During the three remaining phases, microcode is read from the WCS and passed into the microcode pipeline. The pipeline aligns the microcode bits in order to drive the DSP. The microword is composed of 48 bits which provide offset, coefficient, and control information.

The DSP is composed of the arithmetic unit, the memory management unit and the audio memory. All audio information is passed into or out of the DSP via the Digital Audio I/O section. The I/O section allows each of the audio processors to access the shared audio bus. Each of the processors can write to or read from other signal processors on the bus, write to or read from the D/A or A/D, or write to or read from the transfer registers. Each of the five sections is discussed separately in the following text.

### 4.2.2 Slave Processor

The Slave Processor is a 4 MHz version of the Z80. It receives all operating system code via a DMA link to the Host Processor board. U1 and U2 provide address buffering, U3 provides data buffering and one half of U41 provides control buffering for Slave processor #1. Similarly U16 and U17 provide address buffering, U18 provides data buffering and the other half of U41 provides control buffering for Slave processor #2. The scenario for the downloading of code (both operating or music programs) is as follows.

The Master issues a `DMAREQ/` to the appropriate slave. The slave, upon relinquishing control of the bus, issues a `BUSACK/` which signals the host that the bus is free and also enables the tristate buffers onto the slave's environment, enabling the Master to write to the Slave RAM. Once the Master has finished the desired download, the Slave is released and continues either at the point where it left off, or the Slave can be reset to start from a known point. In order to smoothly initiate the slaves upon power up, a quad latch is provided (U30). This latch is cleared upon power on, placing all slaves into the reset condition. The Master can now individually load each of the slaves with the appropriate code by first releasing the reset and immediately requesting the bus. Once a particular slave has received its code, the Master can again place it into the reset condition and continue loading the other slave memories. After all slaves have been loaded, the Master can release all the slaves simultaneously. U30 also provides the Master with the ability to interrupt each of the slaves individually.

The sole purpose of the Slave processor is to provide dynamic updating of the microcode program running the DSP. In order to synchronize the Slave with the running microprogram a WAIT state generator has been provided. When the Slave writes to a particular address (see memory map) `WAITEN` on U20 strobes high, providing a clocking edge to U43. This places the Slave into a wait state. The WAIT state is removed when `PCCLR/` goes low, signalling the beginning of the next sample period.

One of the more elegant features of the Slave interaction with the WCS is that the Slave essentially steals one of the phases of the DSP in order to write to or read from the WCS. The WCS appears as a dual ported memory in which one fourth of the time is devoted to the Slave and three fourths of the time is taken by the DSP. More will be said about this feature in the section on the WCS. Memory decoding is provided by U6 on Slave #1 and by U33 on Slave #2. See the memory map in Table 4.1.

**Table 4.1. Memory Map.**

| Strobe | Address | Function |
|---|---|---|
| RAM0/ | 0000H–1FFFH | ENABLE 8k×8 STATIC RAM |
| DABRD/ | 2000H–3FFFH | READ DAB TO SLAVE |
| BANKA/ | 4000H–47FFH | WCS BANKA |
| PGSEL/ | 4000H | SELECT CURRENT HSP PAGE |
| IOEN/ | 4001H | ENABLE I/O LATCHES & BUFFERS & CPCC/, CURRENT POSITION COUNTER CLEAR |
| SLAVEINT/ | 4002H | SLAVE INTERRUPT STROBE TO HOST |
| WAITEN | 4003H | ENABLE SYNCHRONIZING WAIT STATE |
| | 4800H–5FFFH | NOT USED |
| BANKB/ | 6000H–67FFH | WCS BANKB |
| | 6800H–7FFFH | NOT USED |
| | 8000H–FFFFH | NOT USED |

### 4.2.3 Clock Generation

The 480L uses a four phase clock to drive the HSP and micro pipeline, provide addressing to the WCS, and to allow the slaves access to the WCS during one of these phases. The four phases `MPH<A/:D/>` are generated using D-flip flop U102 and ROM U103. The outputs of U103 are latched in U104 to provide minimum clock skew between MC and each phase. ZCLK is also derived from ROM U103 and latched by U104. The ZCLK is one fourth the MC frequency and, because it is latched along with the phase clocks, it is in phase with the DSP.

### 4.2.4 Writable Control Store

The WCS is composed of two banks, A & B. Each bank consists of two pages in one 2k × 8 static RAM. The WCS appears as a dual port memory to the Slave and DSP. The dual porting of the RAM is accomplished as follows:

As explained above in the clock generation section, the 480L is a four phase machine and the Slave's clock is synchronized with the start of phase A/. Because of this synchronization, the WCS appears as a dual port memory. When the Slave wants to write to the WCS, it simply writes as though the memory were its own. During phase A/, address muxes U10, U11 and U12 — or muxes U37, U38 and U39 — are enabled, allowing the Slave address bus access to the WCS. During a write, the enable pins on U23 (bank A) or U25 (bank B) are pulled low, allowing data to be passed to the WCS. Decoding of the `WR/` and `BANK1/` is provided by U8 and U21. During a memory read, everything above applies but data is now latched by U22 or U24. The data must be latched to provide correct data read timing to the Slave. The output enable and clock signals are provided by decoding `RD/` and `BANK1/` with U8 or U21.

During phases B/, C/, and D/, the DSP is allowed access to the WCS. All muxes mentioned above are selected for the program counter. `PC<0:6>` is enabled onto the WCS address bus. The DSP always reads the WCS and therefore `WR/` on U21 and U8 is always high during these three phases. `PCCLR/` provides synchronization of the reset of the program counter to the beginning of the sample cycle. The program counter will normally count to 79 decimal and then be reset. U9 and U36 are the counters used to provide the PC which are clocked at the end of phase D/. A feature provided with the WCS is the ability of the Slave to choose which half of bank A and B that the microcode is being read from to run the DSP. Slave data bit zero is used to select the bank page in conjunction with `PGSEL/` and `OP/`. U7 or U34 provide the latching of the page select. A memory map of the WCS is provided in Table 4.2.

**Table 4.2. WCS Memory Map.**

| Bank | Address | Byte | Page |
|---|---|---|---|
| A | 4000H–40FFH | STROBE DECODE | 1 |
| A | 4100H–41FFH | NOT USED | 1 |
| A | 4180H–41DFH | 4 | 1 |
| A | 41E0H–427FH | NOT USED | 1 |
| A | 4280H–42DFH | 2 | 1 |
| A | 4300H–434FH | 0 | 1 |
| A | 4350H–457FH | NOT USED | 1 |
| A | 4580H–45DFH | 4 | 2 |
| A | 46E0H–467FH | NOT USED | 2 |
| A | 4680H–46DFH | 2 | 2 |
| A | 4700H–474FH | 0 | 2 |
| A | 4750H–47FFH | NOT USED | 2 |
| B | 6000H–617FH | NOT USED | 1 |
| B | 6180H–61DFH | 5 | 1 |
| B | 61E0H–627FH | NOT USED | 1 |
| B | 6280H–62DFH | 3 | 1 |
| B | 6300H–634FH | 1 | 1 |
| B | 6350H–657FH | NOT USED | 1 |
| B | 6580H–65DFH | 5 | 2 |
| B | 65E0H–667FH | NOT USED | 2 |
| B | 6680H–66DFH | 3 | 2 |
| B | 6700H–674FH | 1 | 2 |
| B | 6750H–67FFH | NOT USED | 2 |

> **Editorial note (not in original manual):** The Bank A row `4100H–41FFH NOT USED` overlaps the byte-4 window `4180H–41DFH` immediately below it. This is reproduced exactly as printed in the manual. The overlap is a cosmetic anomaly in Lexicon's table, not a transcription error, and it cannot be resolved from the schematic (no hardware defines these boundaries). See **Appendix A.2**.

Because the WCS is read and write accessible to the Slave processor, the unused blocks of memory can be used by the Slave for storage or scratch pad memory.

### 4.2.4 Microcode Description

The microcode for the 480L is a 48 bit microword. The composition of the microword is shown in Table 4.3. All even numbered bytes reside in bank A of the WCS while all odd bytes reside in bank B.

**Table 4.3. 48 bit Microword.**

| Byte | MS (7) | 6 | 5 | 4 | 3 | 2 | 1 | LS (0) |
|---|---|---|---|---|---|---|---|---|
| 0 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| 1 | 15 | 14 | 13 | 12 | 11 | 10 | 09 | 08 |
| 2 | C7/ | C6/ | C5/ | C4/ | C3/ | C2/ | C1/ | C0/ |
| 3 | SIGN | ENACC/ | RA11 | RA01 | SHORT/ | CLKEN/ | RA10 | RA00 |
| 4 | IORD/ | IOWR/ | SLVWRT/ | WADB4 | WADB3 | WADB2 | WADB1 | WADB0 |
| 5 | MWR | MCEN/ | OP/ | XCLK/ | DP/ | ACC/ | WA1 | WA0 |

The first two bytes (0 and 1) are used to specify the offsets to the MMU. These offset bytes are latched directly into the MMU at the end of micro phase B. Byte 2 is used to specify the coefficients for the multiply in the ARU. Eight bits are used to specify a value from 0 to 255. The coefficients can be loaded in one read cycle from the WCS, facilitating rapid ramp up and ramp down of coefficients. Hardware is provided in the pipeline to align the micro bits of the coefficients and the associated control bits needed to drive the ARU through the series of multiplies. These control bits are contained in byte 3 of the microword. They are:

- **RA10, RA00** — Read address for the register file in the ARU used in a single precision multiply, and all cycles of n-precision (double precision) multiply except the last cycle.
- **CLKEN/** — Enables clocking of U79 and U80 thru U116. The clock is always enabled on a single precision multiply and enabled on all cycles of n-precision multiplies except the last cycle. It also selects the register to be used during the current multiply cycle. A 0 enables U79, which is used during all single precision multiplies and all cycles of n-precision multiplies except for the last cycle. A 1 enables U80, which is used for the last cycle of the n-precision multiplies.
- **SHORT/** — Signals the timing ROM that the result of the current n-precision multiply will be used as the source to the n-precision multiply which is to follow.
- **RA01, RA11** — Register file address for the last cycle of an n-precision multiply.
- **ENACC/** — During the last cycle of an n-precision multiply this bit determines whether to accumulate or not.
- **SIGN** — Determines the sign of the coefficient during the last cycle of an n-precision multiply.

Byte 4 contains the five WET address bits used by each HSP to address all I/O ports in the system. A total of 32 addresses for I/O are provided. The I/O map is provided in Table 4.4.

**Table 4.4. I/O Map.**

| Hex Address | I/O Function |
|---|---|
| 10h | READ WET CH0 |
| 11h | READ WET CH1 |
| 12h | READ WET CH2 |
| 13h | READ WET CH3 |
| 14h | READ WET CH4 |
| 15h | READ WET CH5 |
| 16h | NOT USED |
| 17h | NOT USED |
| 18h | D/A PRIMARY LEFT |
| 19h | D/A PRIMARY RIGHT |
| 1Ah | D/A SECONDARY LEFT |
| 1Bh | D/A SECONDARY RIGHT |
| 1Ch | A/D IN LEFT |
| 1Dh | A/D IN RIGHT |
| 1Eh | WRITE XREG |
| 1Fh | READ XREG |

The two most significant bits of byte 4, `IORD/` and `IOWR/`, indicate a read or write operation during an I/O operation. A detailed description of the I/O operations is given below. The last byte of microcode (byte 5) contains the remaining control bits for the DSP. These bits are:

- **WA1, WA0** — Register file write address.
- **ACC/** — Determines the source of the multiply or the source of the accumulate. `ACC/ = 0` specifies the source as the register file; `ACC/ = 1` specifies the accumulator.
- **DP/** — Indicates a double precision multiply or an n-precision multiply. `DP/ = 0` indicates either the first cycle of a double precision, or any cycle of an n-precision multiply other than the last cycle where `DP/ = 1`.
- **XCLK/** — Transfers the accumulated result in the ARU accumulator to the transfer register in the ARU.
- **OP/** — Indicates an I/O instruction, enabling the HSP address buffer page selection onto the WET address bus and WET control bus.
- **MCEN/** — Memory control enable. Used to enable audio memory read and writes in conjunction with MWR. A 0 allows audio read or writes.
- **MWR** — Purpose depends on the level of `MCEN/`. Table 4.5 shows the different possibilities.

**Table 4.5. MCEN Operations.**

| MWR | MCEN/ | Operation |
|---|---|---|
| 0 | 0 | Audio memory read, disable output of ARU transfer register |
| 0 | 1 | used on I/O reads |
| 1 | 0 | Audio memory write, enable output of ARU transfer register onto DAB |
| 1 | 1 | used for I/O writes and to pass the ARU transfer register to the ARU register files |

### 4.2.5 Microcode Pipeline

The microcode pipeline aligns the microcode for driving the digital signal processor through the phases of operation. The offset information is latched directly into the MMU and therefore requires no additional phase alignment. The remaining thirty-two bits of microcode must be extensively realigned. Latches U70, U71, U83 and U84 (or U99, U100, U118 and U119) represent the beginning of the pipe. Coefficient information and several control bits are latched out of the WCS during phase C. This information is passed on to U79 and U80 and then to U78, or to U114 and U115 and then to U113. I/O information is latched in U71 or U100 and then relatched in U106 or U107. These I/O bits are global control and address bits for the WET busses. U109 is provided to handle the control bits in a local sense. These locally used bits provide each of the DSPs with the ability to pass information to the WET latches from the DAB, or read information from the WET bus to the DAB. Finally, miscellaneous control bits are latched in U84 or U119 and passed on for phase alignment in latches U82 and U63 (or latches U117 and U92).

### 4.2.6 Digital Signal Processor

The 480L digital signal processor is composed of two major functional blocks: the digitized audio management and memory section, and the arithmetic section. Each of these sections is explained separately below.

### 4.2.7 Audio Management and Memory

This section can be subdivided into three functional subsections: the Memory Management Unit (MMU), memory timing, and the Digitized Audio Memory (DAM). The MMU (U69 or U98) provides addressing of the DAM by subtracting offsets (micro bits 0–15) from an internal position pointer. The offsets are clocked into buffers directly from the WCS. They are then subtracted from the current pointer to memory to generate the row and column addresses for the DAM. The current position pointer is incremented once a sample cycle by the falling edge of WC (word clock). The signal SEL is used to multiplex out the addresses necessary for correct memory access. Delay line U40 and inverter U51 provide correct timing for the `RAS/`, `CAS/` and SEL strobes. U50 or U51, D-flip-flop U28 and AND gate U15 provide decoding of the delayed signals. The DAM is composed of five 64k × 4 dynamic RAMs for a total of 64K 20-bit audio words. Eighteen bits provide the audio word and two bits are used for further expansion.

### 4.2.8 Arithmetic Section

The arithmetic section is made up of the timing and control subsection and the ARU. The timing and control subsection is composed of ROMs U77 and U62 with latches U76 and U61 and ARU U60 — or ROMs U112 and U91 with latches U111 and U90 and ARU U89. Coefficient bits `C<0:4>`, state bits `ST<0:2>`, and several control bits make up the address bits for the ROMs. The data is latched on every master clock (MC) for control of the ARU. The ARU performs an eighteen by four bit multiply and accumulate every instruction cycle. Data is read into or gated out of the ARU buffers onto the DAB once an instruction cycle.

### 4.2.9 Digital Audio I/O

The 480L has two 18-bit audio busses. The first bus is the WET bus, which is a global bus used by all HSPs plugged into the backplane. It provides access from one HSP to another, access to an HSP by the Host processor, and access by any HSP to or from the audio input or output channels. The second audio bus is the DAB bus, which is local to each HSP and not directly accessible to any other HSP or Host. For the purpose of the discussions below, the latches from the DAB to the WET data bus are U73, U75 and U58 (or U86, U88, and U59). The buffers from the WET data bus to the DAB are U72, U74, and U57 (or U85, U87, and U56).

### 4.2.10 HSP X to HSP Y

Let's assume that HSP x wants to pass one digitized audio word to HSP y for further processing. HSP x first strobes data off the x DAB into its WET bus output latches. This is done by HSP x by either reading from audio memory the desired word while setting `IOWR/` to a 0 and leaving `OP/` inactive (1), or performing a write with `MCEN/` inactive, `OP/` inactive and `IOWR/` a 0. Once this has been done, `IOWR/` is set back to a 1.

When HSP y needs the audio word from HSP x, it has to perform an I/O operation. `OP/` is now set active by HSP y, which enables HSP x's address onto the WET ADDRESS bus and sets `IORD/` low on the WET CONTROL bus. This causes HSP x's WET output latch to be enabled onto the WET DATA bus. This data is subsequently gated onto HSP y's DAB. `IOWR/` used by HSP x is only a local usage; without `OP/` enabled, the WET CONTROL bus is not affected.

### 4.2.11 HSP X to Audio Output

Let's assume that HSP x wants to write to one of the four output channels. HSP x first strobes the audio word into the WET output latches, using the same method as above. On the instruction where the audio word is to be written to the audio output, HSP x sets `OP/` active, enabling all WET busses, sets `IOWR/` low, and places the WET address of the output port on the WET ADDRESS bus. The DAB output latch is gated to the WET DATA bus and the `IOWR/` signal on the WET CONTROL bus clocks the audio word into the addressed audio output register.

### 4.2.12 Audio Input to HSP X

HSP x audio data is read from the audio inputs by enabling the audio input buffer onto the WET DATA bus and simultaneously gating the WET DATA bus to the DAB. The following method is used by HSP x: HSP x performs an I/O read by setting `OP/` active. `IORD/` is set low, gating the WET data to DAB x. At the same time HSP x places the audio input address on the WET ADDRESS bus, enabling the desired input channel onto the WET DATA bus. The data passes to HSP x and the transfer is complete.

### 4.2.13 HSP X to XREG or XREG to HSP X

A method has been provided to allow the Host processor to pass audio data to and from any HSP. This feature is enabled only during test and is not meant to be a real time exchange of audio information. A register called XREG is used for the passing of the audio data from/to the DAB to/from the Host data bus. The method used to pass data to the Host from the HSP is the same as passing data to audio output, except that the WET address of the XREG is placed on the WET ADDRESS bus. To read data is the same as reading the audio input except, again, the WET address is for the XREG.

---

## 4.3 Host Processor (Rev. 1)

The 480L Host Processor is a 68008-based microprocessor system that interprets external control events and services the needs of the Slave/High Speed Processor subsystems. External control events include multiple LARCs, MIDI, and (in the future) Computer Automation communications. The Slaves rely on the Host Processor for program download and control via interrupts, reset, and DMA read/write to Slave memory. Additionally, the Host provides system clock generation, digital audio I/O, Serial-to-Parallel and Parallel-to-Serial conversion, and support of the audio parallel bus.

The Host Processor hardware kernel is shown on sheet 1 of the schematics. An 8 MHz clock is generated by the 16 MHz crystal oscillator module U18 and counter U16. U16 also generates MIDICLK (500 kHz) and ERRCLK (62.5 kHz). MIDICLK is used by the DUARTs for either timing or MIDI baud-rate communication. ERRCLK is used by U14 to flag bus time-out errors on the processor bus.

Bus operations are most easily explained by walking through a typical bus transaction. The 68008 places an address on A19–A0, a code indicating access type on FC2–FC0, and then strobes valid address by bringing `AS/` low. For any function code other than 111 (or access type Interrupt Acknowledge), the output of U12 is driven low, enabling U23 and U24. U23 decodes which area of memory is being accessed. If the memory access is to ROM or RAM, then U24 will select the appropriate IC. In the case of a ROM access, U23 will drive `ROMRAMSEL` (U9-8) high. `ROMRAMSEL` is delayed for two 8 MHz cycles by U28. This delayed edge propagates through U27, U29, and U25, finally bringing the `DTACK/` input to the 68008 low. `DTACK/` low completes the asynchronous bus handshake; the 68008 brings `DS/` and `AS/` high. `AS/` high drives AS low, clearing U28 and releasing DTACK. The 68008 responds by commencing the next bus transaction.

DTACK generation may be simply summarized. The memory map in U23 reflects the maximum configuration of the system: four 1-Megabit ROMs and two 32k × 8 nonvolatile RAMs. The map in device U24, which does the ROM and RAM Chip Selects, will change as device sizes are changed. The intent here is to do DTACK generation for any possible system with a single U23, and change U24 for specific configurations. DTACKs are generated by U28 for the cases ROM, RAM, RAMCART, and Strobes. In the case of DUART access, the DUARTs generate DTACKs. DTACK is generated by the Slave DMA circuit for the case of Slave channel access. There are two remaining cases of DTACK generation. The DUARTs will generate their ordinary `DUARTxDTACK/` in the case of an Interrupt Acknowledge cycle after a DUART interrupt. Device U23 will generate a ROMRAMSEL DTACK in the case of a level 7 or level 2 Interrupt Acknowledge. This is accomplished via signal `IACKSTB/`, generated by U25.

Bus Errors are closely connected to the asynchronous bus handshake. If, through program error, the 68008 presents an address outside the limits of the maximum system, U23 will fail to decode. No device will respond with DTACK, and the µP will hang in the middle of its handshake, waiting for the `DTACK/` falling edge. After four cycles of ERRCLK, or 64 µsec, U14 will drive the `BERR/` input to the 68008 low, forcing a Bus Error Cycle. The 68008 responds by beginning a Bus Error exception process, fetching a specific vector and commencing execution at that location. Information about the errant bus cycle is preserved in a stack frame to permit analysis of the fault. Bus errors may also be generated during slave access. If a slave fails to respond to the Host's request for bus access, after 64 µsec a bus error cycle will be initiated.

The operating system distinguishes between several classes of bus error:

- Bus error during power-up diagnostic check of NVRAM, RAMCART, etc., indicating faulty DTACK hardware.
- Bus error during power-up diagnostic check of DUARTs, indicating faulty DUART hardware.
- Bus error at run-time due to access of nonexistent memory, indicating either hardware fault or program logic fault.
- Bus error during initial access of a Slave, indicating no slave in place.
- Bus error during subsequent access of a Slave, indicating a lunched slave.

There are four types of reset in the system: power-up reset to the 68008 and Slave processors; hard reset of the 68008 due to power failure; 68008 generated reset; and 68008 generated reset to the Slaves, `SR/`.

Devices R15, C35, and CR10 generate `POPI/` on power-up. `POPI/` forces U52 to drive HRESET, driving the 68008's `HALT/` and `RESET/` pins low simultaneously. This reset condition lasts for about 100 msec. Upon release of `POPI/`, the 68008 will fetch two vectors needed for initialization: the Supervisor Stack Pointer and the Initial Program Counter. Fetching these two vectors requires eight byte read operations. During this time a mechanism operates to ensure that these fetches occur from the first eight locations of ROM0. HRESET high loads zeros into shift register U30, driving `MAP/` low. `MAP/` stays low for the next eight `AS/` falling edges, thus forcing selection of ROM0 through gate U25. After the eighth fetch, `MAP/` goes high and the 68008 begins execution at the location specified by the Initial Program Counter. This mechanism allows one important system advantage. During hard reset the system accesses ROM for its initialization. At all other times, base or zero page is located in NVRAM, allowing soft write of the exception processing vectors.

The `RESET/` line of the 68008 is bidirectional/open collector. Execution of a RESET instruction will drive `RESET/` low, resetting the DUARTs and Slave interrupt flop, but leaving the Slave processor's unaffected. The 68008 may read location `$C0007`, strobing `SOFTR/`, which will drive `SR/` (System Reset) low, resetting all Slaves. `SR/` is also driven active by `POPI/` (Power-On Prime), so that the slaves are reset at power-on. There is a separate mechanism for resetting Slaves individually, which is discussed below.

The 68008 supports three levels of external interrupt. `PF/` (Power Fail) drives interrupt level 7, the highest level. DUARTs U7 and U6 drive level 5, the second-highest level. `SLAVEINT/` (Slave Interrupt) drives interrupt level 2, the lowest level. Priority encoder U19 places the current highest level on `IPL2/0`, `IPL1/`, holding lower priority interrupts pending.

Host interrupt processing is most easily explained by walking through each of the possible interrupt cycles: Slave, Power Fail, and DUART.

A Slave Z80 requests service by driving `SLAVEINT/` low. `SLAVEINT/` is buffered by U22. The buffered signal, `SLAVINTB/`, clears U8, making `IR2/` active. If neither `IR5/` nor `PF/` is active, `IR2/` will be encoded by U19 and presented to the 68008. The 68008 will respond within an instruction cycle if interrupt level 2 is enabled.

The interrupt level is output on the address bus, function code FC2–FC0 is set to 111, and `AS/` is set active. U26, the IACK decoder, is enabled by FC2–FC0 high, and outputs `IACK2/` active. `IACK2/` clocks U8, removing the `IR2/`. `IACK2/` enables U67, sending 66 decimal on D7–D0. `IACKSTB/` is active, forcing U23 to set ROMRAMSEL, initiating a `DTACK/` handshake. The 68008 completes the bus cycle, fetches user vector 66 from its base page memory (NVRAM), and commences interrupt exception processing.

The Motherboard will set `PF/` active upon detecting low unregulated DC on the 5V power supply. `PF/` is encoded by U19 and presented to the 68008 as interrupt level 7. Level 7 is the highest priority, and not maskable by the µP. The train of events is similar to the case of `SLAVEINT/`: an interrupt acknowledge cycle is decoded by U26; `IACK7/` enables U67; vector 67 is thus returned to the µP; `IACKSTB/` is input to U23 and U23 sets ROMRAMSEL active, completing the DTACK handshake. The 68008 commences interrupt exception processing. The tasks to be performed by the power fail interrupt are discussed in greater detail later.

DUART interrupts employ a different hardware path. The 68681s, U6 and U7, each have `IRQ/` and `IACK/` signal lines. `IRQ/`, output from the DUART, signals that an interrupt condition has occurred. `IACK/` is an input to the DUART that signals a 68008 IACK bus cycle. Due to the limited number of interrupt levels available, both DUARTs share interrupt level 5, in round-robin fashion. Let us presume that DUART1, U7, has just completed transmission of a character and is set up to issue an interrupt on TX Ready. U7 drives `IRDUART1/` active. If there is no request pending from DUART2, then U10 will be clocked low by the next falling edge of 8MCLK. `IR5/` is driven active by U25, encoded by U19, and presented to the 68008. The 68008 responds with an IACK cycle. `IACK5/` is generated by U26. U12 steers `IACK5/` to `IACKDUART1/`. U7 responds by placing the contents of its Interrupt Vector Register on the data bus D7–D0. U7 completes the DTACK handshake via the `DUART1 DTACK/` signal. If DUART2 (U6) were to issue an `IRDUART2/` during DUART1's IACK cycle, or while DUART1's IRQ was being held pending (by 68008 mask), then DUART2's interrupt request would be held pending, with the `IRQ5/` issued only after DUART1's IRQ had been removed. Note that each half of U10 is clocked on opposite phases of 8MCLK, precluding races in the round-robin circuit.

The principal system features of DUART interrupts are:

- DUART interrupts may be programmed to occur on TX, RX, and Timer/Counter events as described in the 68681 manual.
- DUART1 and DUART2 interrupts are serviced in round-robin fashion, both arriving at IR level 5, second in priority only to Power Fail.
- Each DUART issues a user vector number, programmed by register, which points to an entry in the user vector table in NVRAM. Thus, each DUART may have its own interrupt service routine or routines. The µP must poll the DUART requesting service to determine which event triggered the interrupt.
- The DUART round-robin circuit arbitrates the hardware interrupt requests. Since the 68008's interrupt mask is set within software, the service routines may set the interrupt mask to allow interruption of one DUART's service routine by the other's requests.

Host communication to the Slaves is done via DMA (Direct Memory Access) on one of six 16k byte channels, one channel dedicated per slave. See the address map for definition of the boundaries of the slave channels. PAL U23 sets `SLAVEAS/` active when a read or write operation is to one of the slaves. Buffers U32, U21, and U22 are enabled by `SLAVEAS/`, and present address bus A19–A0 to the slaves as PAB19–PAB0.

The Slave DMA interface operates in either byte mode or block mode. In byte mode, `BLOCK/`, originating at DUART1, is set inactive. A19–A14 appear at hex D-latch U48. The falling edge of `SLAVEAS/` latches this high order address into U48. U33 decodes the address as being in one of the six channels and sets one of its outputs. This output is buffered by U37 and appears as one of `DMAREQ5/` to `DMAREQ0/`. The Slave Z80 receives the DMAREQ as a Bus Request. After completion of its current instruction cycle, the Z80 relinquishes its bus and returns Bus Grant, which appears as a low on the open-collector wired-or signal `DMAACK/`. During this time, the 68008 has been held with DTACK incomplete. `DMAACK/` low satisfies gate U54, and permits U17 to generate `DMADTACK/`. On the next processor access outside of the slave channels, AS will be high indicating valid address. This is delayed one 8MCLK edge by U17 and appears at U15 as ASDELAY. `SLAVEAS/` is high (since we are outside the slave channels), `BLOCK/` is high, and U15 clears U48. This removes the DMAREQ from `DMAREQ5/` – `DMAREQ0/`. The slave last accessed is released, and processing continues. Note that byte mode is a misnomer in that multi-byte operations are supported. Any byte or multi-byte write, read, or read/modify/write access to a slave will run as an automatic event under byte mode. This is possible since the slave bus is not relinquished until the 68008 accesses its own memory outside the slave channel space.

The slave channel block mode permits the host µP to read or write the memory space of a particular slave without relinquishing control of the slave busses between accesses. First, the Host µP sets `BLOCK/` active (Output Bit 4 of DUART1). The Host then accesses the first byte in Slave memory space. Operation for this first access is identical to that of byte mode, except that U15 does not clear U48. U48 remains latched, the Slave remains in Bus Grant, and `DMAACK/` remains low. Subsequent accesses to the Slave are made with U17 generating `DMADTACK/` after the falling edge of `SLAVEAS/`. To terminate block mode for a particular slave, the host µP sets `BLOCK/` inactive. On the next memory access outside of slave channel space, U15 will clear U48, releasing the slave.

There is one final mechanism for controlling slaves. The host µP may write to a register on the Slave/HSP PCA, setting `RESET/` and `INT/` for each slave processor. There is one write-only register per Slave/HSP PCA, controlling two Slave processors, as shown in Table 4.6.

**Table 4.6. Slave Control.**

| D3 | D2 | D1 | D0 | Function |
|---|---|---|---|---|
| 1 | 1 | 1 | 0 | INT/ Lo-order Slave |
| 1 | 1 | 0 | — | RESET/ Lo-order Slave |
| 1 | 0 | — | — | INT/ Hi-order Slave |
| 0 | — | — | — | RESET/ Hi-order Slave |

These registers are mapped into the Host memory as shown in Table 4.7.

**Table 4.7. Register Mapping.**

| Address | Strobe | Function |
|---|---|---|
| $C0015 | SP0WR/ | Write address for Slave 0, 1 |
| $C0016 | SP1WR/ | Write address for Slave 2, 3 |
| $C0017 | SP2WR/ | Write address for Slave 4, 5 |

In order to reset Slave 0, the Host µP writes byte `$0D` to `$C0015`. During this write, decoder U92 drives `SP0WR/` low. `SLAVEBUSEN/` is also low, enabling buffer U36. Buffer U36 drives host D7–D0 onto PDB7–PDB0 on the backplane. `$0D` is presented to the Slave register and latched on the rising edge of `SP0WR/`.

> **Editorial note (not in original manual):** The byte `$0D` is hardware-verified correct (see **Appendix A.1**). The slave control register is U30, a 74HCT175 quad D flip-flop on sheet 10 of drawing 060-04391, clocked by buffered `SP0WR/`. `$0D` = `0000 1101` asserts only `RESET1/` (bit 1 → lo-order slave reset) while leaving both interrupts and the hi-order reset de-asserted.

When the unit is powered on, Slave registers will be cleared by `SR/`, holding all Slaves reset. If the Host wishes to stop all Slaves as a result of some cataclysm, it may assert `SR/` by reading address `$C0007`. To initiate a program on a Slave after power-up, the Host must do the following:

1. Reset the Slave by writing to its slave register.
2. Disable interrupts and task switching. Assert `BLOCK/`.
3. Release the Slave from reset by writing to its slave register. (This is necessary because a Slave in reset will not respond to Bus Requests from the Slave DMA interface.)
4. Immediately read or write to that slave channel. The slave now has its operations suspended and is held in Bus Grant.
5. Download a minimal program to slave location zero.
6. Reset the Slave by writing to its slave register.
7. Deassert `BLOCK/`. Reenable interrupts and task switching.
8. Release the Slave from reset.

Slaves may be interrupted by asserting `INT/` on the appropriate Slave register, as described in the Slave/HSP section.

The Host communicates over four external serial channels provided by two 68681 DUARTs (Dual Asynchronous Receiver/Transmitter). DUART1, U7, is memory mapped with its internal registers appearing at locations `$60000` through `$6000F`. DUART2, U6, appears at locations `$64000` through `$6400F`. DUART registers are summarized in Table 4.8.

The DUARTs provide four serial channels, programmable for any of 20 baud rates from 50 baud to 38.4k baud, including the MIDI baud rate of 31.25k baud. U7 pins X1/CLK and X2 drive crystal Y1, 3.6864 MHz. U6 X1/CLK is driven at the same clock rate by HCT04 U9. Access to the DUARTs is mediated by R/W, `DUARTxCS/`, and `DUARTxDTACK/`, with A3–A0 being internally decoded to select one of the 16 internal registers. DUART interrupt function is as described above.

DUART1 Channel A is dedicated to MIDI input and output. MIDICLK provides a 500 kHz (16 × 31.25k baud) clock to input pins IP4 and IP3 for this purpose. Additionally, MIDICLK is connected to IP2 to be used as a clock source for the 16-bit internal counter/timer. IP5, IP1, and IP0 on U7 are used for additional system status inputs. Buffers for the MIDI channel are located on the Motherboard. U7 Channel B is buffered by RS422 buffers U2 and U4 and provides LARC1 serial. FB3 and FB4 (Ferrite Bead) serve to limit slew rate on the L1SD/ and L1SD outputs. R2 provides serial termination on the Receive Data differential inputs and R66 improves noise immunity. Output pins OP7 through OP0 provide control over various system functions.

DUART2 Channel A is dedicated to Computer Automation functions, buffered by RS422 buffers U1 and U3, and may run at any of the 20 baud rates including MIDI rate. DUART2 Channel B is dedicated to the second LARC. LARC2 inputs and outputs are buffered and terminated similarly to those of LARC1. All serial receive channels are quadruple-buffered internally. All serial transmit channels are double-buffered internally. On DUART2, IP2 provides a WC0 (Work Clock Out) input. IP1 and IP0 monitor W2 and W1 jumpers for setting test or diagnostic modes, etc. Output pins OP7 through OP0 provide control over various system functions. DUART1 and 2 parallel input and output functions are summarized in Table 4.9.

**Table 4.8. DUART Register Summaries.**

| DUART1 Add | DUART2 Add | Register/Function Read | Register/Function Write |
|---|---|---|---|
| $6000F | $6400F | Stop Counter Command | Bit Reset Command |
| $6000E | $6400E | Start Counter Command | Bit Set Command |
| $6000D | $6400D | Input Port (Unlatched) | Output Port Config. |
| $6000C | $6400C | Interrupt Vector Reg. | Int. Vector Reg. |
| $6000B | $6400B | Receiver Buffer B | Trans. Buffer B |
| $6000A | $6400A | Do Not Access | Command Reg. B |
| $60009 | $64009 | Status Register B | Clock Sel. Reg. B |
| $60008 | $64008 | Mode Register B | Mode Register B |
| $60007 | $64007 | Counter Mode: LSB | Counter/Time Lower |
| $60006 | $64006 | Counter Mode: MSB | Counter/Time Upper |
| $60005 | $64005 | Interrupt Status Reg. | Interrupt Mask Reg. |
| $60004 | $64004 | Input Port Change Reg. | Auxilliary Control |
| $60003 | $64003 | Receiver Buffer A | Trans. Buffer A |

**Table 4.9. DUART 1 and 2 I/O Port Functions.**

| Input | Signal | Notes |
|---|---|---|
| IP5 | PLOCK | Hi level indicates Phase Lock Loop is locked |
| IP1 | WCPRES | Hi level indicates external 1610 clock is present |
| IP0 | OVLDB | Lo level indicates a digital overload has occurred in one of the ARUs (latching) |

Devices U40, U41, U42, and U43 are ROM sockets designed for either 27256 or 27512 EPROMs. PAL U24 decodes the chip select signals `ROM0M/`, `ROM1/`, `ROM2/`, and `ROM3/`. A different U24 will be programmed for different selections of memory size. Table 4.10 summarizes jumper positions and pin functions for the different EPROM sizes.

**Table 4.10. Jumper Positions and Pin Functions.**

| EPROM/ROM Type | Jumper Position | Pin Function |
|---|---|---|
| 27256 | W11,13,17,20 to +5V; W10,14,15,18 to ROMx/ | Pin 1 – Vpp; Pin 22 – OE/ |
| 27512 | W11,13,17,20 to A15; W10,14,15,18 to ROMx/ | Pin 1 – A15; Pin 22 – EO/ |

The remaining core functions of the Host processor are shown on sheets 2 and 4 of the schematics. Connector J1 is the interface to the nonvolatile RAM Cartridge. The RAM cartridge is mapped by PAL U23 to `$70000` through `$77FFF` and may contain as much as 32k × 8 nonvolatile store, depending upon the cartridge chosen. Buffers U20 and U31 present processor address bus A19–A0 to the J1 connector. These buffers are enabled by `RAMCASEL/`, generated by PAL U23. `RAMCASEL/` also serves to drive `CARTENABLE/` and `OUTENABLE/`. U44 drives `WRENABLE/` (cartridge write enable) low when the cartridge is selected and µP R/W is low. U35 buffers the cartridge data bus and µP data bus D7–D0.

Device U38 is either a 4364C (8k × 8) or 43256C (32k × 8) nonvolatile RAM. U39 is a 43256 (32k × 8). Jumper W9 is connected to a pull-up for the 4364, or to A13 for a 43256. Backup power for the RAMs, and U49, is provided by two batteries, BT1 and BT2. When +5V is present, diode CR8 supplies current to bring BATVCC to approximately 4.5V. When +5V falls to 0V, CR7 and CR9 conduct, supplying approximately 2.6V to BATVCC, supplying standby voltage to the CMOS RAMs. BT1 and BT2 each have a capacity of 150 mAH. At typical leakage currents in the circuit, this provides battery backup for greater than 80,000 hours. The diode isolation between BT1 and BT2 prevents a defective battery from destroying NVRAM contents. Either BT1 or BT2 may be changed (with an isolated soldering iron) without disrupting RAM contents. U49, the RAM protect flop, is also a CMOS device powered by BATVCC. In response to a `PF/` interrupt, or other command to go into a standby state, the Host µP will complete housekeeping tasks dictated by software and then pulse DISRAM high. U49 will be reset with RAMBUFEN low. U50, which buffers the RAM select signals `HIRAMSEL/` and `LORAMSEL/`, will be disabled, preventing RAM access. On power-up, the Motherboard will keep `PF/` active for greater than 120 msec. This time is required for Host µP reset. When the processor comes out of reset, its first task will be to enable NVRAM by pulsing ENRAMSTB. RAMBUFEN will then go high and NVRAM access is permitted. U50, the isolating gate, is an LS-family device to prevent excessive leakage while in power-down. Note that on power-up, U54 forces `MUTE/` to the Motherboard. Before enabling RAM, the µP will wish to set FORCEMUTE high, forcing `MUTE/` active while slaves are brought to life.

The remaining functions of the Host are system clock generation and digital audio interface, both of which are peripheral to the Host µP itself, but essential to system operation. There are three principal clocks in the system: `WCB/`, `BCB/`, and MCB — buffered Word Clock Bar, buffered Bit Clock Bar, and buffered Master Clock, respectively. Internal to the Host these are generated as BC, BC/, MC, and WC/. The 8 MHz processor clock is also supplied to the system as 8MCLKB.

With the exception of 8MCLKB, the system clocks are derived from MC. MC (Master Clock) is provided by either the Phase Lock Loop or one of two internal crystal oscillators. Regardless of MC source, the generation of BC, BC/ and WC/ is identical. The timing diagram on the following page illustrates the relationship between MC, BC, BC/, 64CLK5 and WC/. MC is driven by the 1Y output of the multiplexer U105. MC clocks U107, a 74F161 configured as a divide-by-five counter. The rising edge of BC/ is coincident with the rising edge of MC. BC/ remains high for three MC periods, then goes low for two periods. BC is the inverse of BC/, as generated by the 74F04 U106. BC rising edges clock U108 and U109, which together constitute a divide-by-64 counter. The six bits of this divide-by-64 counter (64CLK5 – 64CLK0) drive the state ROM U68. U68 is used to control serialization and 1610 transfers. 64CLK5 is a square-wave clock at the sample frequency. The rising edge of 64CLK5 clocks U95, setting it. WC/ is driven low, and remains low for two MC periods until BC goes low, clearing U95. U107, U108, and U109 constitute a divide-by-320 counter. Thus, at an MC frequency of 15.36 MHz, a sample frequency of 48 kHz is generated. At an MC of 14.112 MHz, the sample frequency is 44.1 kHz.

When operating with external bits in (1610 interface) the bits-in source supplies a sample frequency square-wave clock. This clock appears, in buffered form, as signal WCI at U100. It is necessary to generate all system clocks in phase-lock with this signal. When MCSEL0,1 are set to 11, U105 routes the output of U106-6 to MC. U106-5 is driven by Q3, a level converter, which is in turn driven by the ECL oscillator U110. By virtue of the varactor diode VRC1 on its tank circuit, U110 is a VCO, or Voltage-Controlled Oscillator. The MC4044 amplifier, in conjunction with the transistor Q2 and associated discretes, serve as a LPF, or Low-Pass Filter. The LPF is driven by the phase detector section of U96. The phase detector compares input signals WCI (the external reference) and WC/ (the output of the divide-by-320 chain). The phase-detector, LPF, VCO, and divider chain constitute a fixed divide ratio frequency synthesizer with MC as the output and WCI as the input.

The VCO is switched between a high and low range by a second varactor, VRC2. The signal VSEL is high when MCSEL1,0 = 10. VSEL thus biases VRC2 with approximately +4.6 V, setting its capacitance to a low value of approx. 24 pf. This is appropriate for a WCI input frequency of 48 kHz. When MCSEL1,0 is set to 11, VSEL is set to 0V, and VRC2 is biased at a voltage less than 5V determined by the value of R51, which is Selected At Test. This lower bias voltage results in a higher varactor capacitance, so that the VCO will run at 44.1 kHz. The bits-in interface (1610) is specified at 44.1 kHz; however, the interface will run at 48 kHz, a non-standard 1610 frequency. When running on external word clock, the internal crystal oscillators, U93 and U94, are not powered on. Transistor Q1 is in cut-off. This is to prevent beating between the internal oscillators and the Phase Lock Loop VCO.

In addition to the 48 kHz and 44.1 kHz external clock modes described above, the clock generation circuit will also run 44.1 kHz and 48 kHz internal. When MCSEL1,0 = 00 or 01, Q2 is saturated and either 15.36 MHz or 14.112 MHz is selected as MC by U105. MCSEL1,0 = 00 selects 15.36 MHz; 01 selects 14.112 MHz. Note that the U107, U108, U109 counter chain functions identically whether internal or external clocks are chosen. When running from either of the internal oscillators, the PLL VCO is unconnected. The PLL is thus open loop, and runs to either its highest or lowest frequency, depending upon: internal states in the MC4044; whether external WCI is present; and frequency chosen.

The 1610 interface requires an output word clock, WCO. The Host will fulfill this requirement by either passing on the received 1610 word clock in, WCI, or by passing on an internally derived clock 64CLK5. The received 1610 clock, WCI, is buffered by U100, a Schmitt trigger inverter. U100 pin 8 drives CR11, connected to R30 and C63. When WCI is present, U100 pin 3 will be pulled low and WCPRES will go high. WCPRES is available to the 68008 µP as an input at the DUARTs. If the µP sets `WCOFF/` active, then 64CLK5 will be selected through U99 and will appear as WCO. If `WCOFF/` is inactive, WCI will be selected as WCO. If WCI is not present, WCPRES inactive guarantees that 64CLK5 is selected as WCO.

Four functional blocks on the Host PCA manipulate digital audio data. Input data from the 1610 interface or the A/D converters is converted from serial to parallel by the serial input registers. High-speed processor output is converted from parallel to serial and transmitted by the serial output registers. The digital peak detect circuit monitors either A/D inputs or D/A outputs. The transfer registers permit interchange of audio data between the Host µP and the high speed processors.

Timing and control EPROM U68 provides control signals for serial input and output. U68 is addressed by 64CLK5-0, generating 64 states per sample period. Data slew is eliminated by clocking register U81 with BC. Thus, the serial timing and control signals appear in phase lock with the sample frequency, at bit clock rate.

Digital audio input will come from either 1610 format bits-in, or from 480L internal format from the motherboard A/D converters. The 1610 format is 16 bits; internal format is 18 bits. Schematic page six shows the input registers. SELIN, supplied by DUART1, selects the input mode. With SELIN high, GBCLKIN is selected at U102 and clocks the SCLK input of the input registers. GBCLKIN (Gated bit clock in) appears at rising edges of BC and is gated by the signal BGATEIN from the timing ROM. Serial input data from the motherboard (ADDB) is selected by U102 to appear at U60 serial input. U88's serial output, PASSOUT, is passed through to the second set of registers, U59, U73, and U87. Serial data from the A/Ds is presented by the motherboard at ADDB in two bursts of 18 bits, left channel first, followed by right channel. The HCT595 serial registers are fully buffered. The outputs at A,B,C,D,E,F,G,H are the contents of an output register; shift register operations proceed without disturbing the contents of the output register. The first BGATEIN pulse lasts for 24 BC clocks and clocks the 18 left channel bits so that the MSB appears at position H of U88 and the LSB appears at position G of U60. The second BGATEIN pulse also lasts for 24 BC clocks. The left channel data appears at PASSOUT and is clocked through the U102 multiplexer into U59, U73, and U87. Meanwhile, the right channel data appears at ADDB and is clocked into U60, U74, and U88. WC/ pulses low on the last BC period of the sample. This pulse transfers the parallelized data from the shift registers into the output registers of the HCT595s.

A small digression to explain WET bus operation is now in order. The WET Bus serves to transfer parallel audio data from input and output to the high speed processors and intermediate values between the high speed processors. The WET Bus consists of twenty-four data lines (`WETDB<23:0>`), five address lines (`WETADB<4:0>`), and two control lines (`IORD/` and `IOWR/`). The Host is a passive partner in WET Bus transactions in that only HSPs drive the address and control lines. For example, to read the A/D left channel input, an HSP places `11100` b on the WETADB and simultaneously pulses `IORD/` low. This address is decoded by U98 (schematic sheet 7) as `ADINL/`. `ADINL/` enables the input register U59, U73, and U87 onto the WETDB. The addresses and functions of Host peripherals on the WET bus are shown in Table 4.14.

**Table 4.14. Host Peripheral Addresses and Functions.**

| Address | Strobe Signal | Function |
|---|---|---|
| 11000 (38) | DAPRIML/ | Left Primary D/A |
| 11001 (39) | DAPRIMR/ | Right Primary D/A |
| 11010 (3A) | DASECL/ | Left Secondary D/A |
| 11011 (3B) | DASECR/ | Right Secondary D/A |
| 11100 (3C) | ADINL/ | Left A/D input |
| 11101 (3D) | ADINR/ | Right A/D input |
| 11110 (3E) | WRXREG/ | Write wet data to transfer register |
| 11111 (3F) | RDXREG/ | Read transfer register to wet bus |

A/D left and right input from the previous sample period are available for transfer to the wet bus during the entire current sample. As described below, the D/A data must be presented to Host output registers within two time slots.

1610 input operation is similar to A/D input. SELIN is set low. The input registers are clocked by 1610CLK. 1610 input data appears on SADILB (Serial Audio Data Input Left Buffered) and SADIRB. 1610CLK, generated by the timing ROM, clocks the 16 bits of 1610 data in and then clocks 8 additional cycles to bring the data to the top bits of the input registers. WC/ clocks the parallelized data into the HCT595 output registers. As with internal A/D inputs, the audio data from the previous sample cycle is available to the HSPs throughout the entire sample period. The Host microprocessor's only task in this operation is to set the input mode via SELIN.

Output of audio data to the D/As and 1610 interface is slightly more complicated. There are four D/A output channels. These four channels are supported by two sets of registers: U57, U71, U85; and U58, U72, U86 (sheet 7). The four D/A outputs are time-multiplexed into the two register sets. 1610 bits-out is supported by two separate sets of registers: U55, U69, U83; and U56, U70, U84. The HSPs write primary output data during the latter half of the sample period. WET bus writes to `DAPRIML/` and `DAPRIMR/` are latched into the input registers of all four sets of HCT597s. Note that 1610 output data is the same as the data presented to the Primary D/A channels. On the last BC period of the sample period, `NLDAD/` and 1610XFOUT pulse low, transferring the HCT597 input register data to the serial output registers. 1610OUTCLK begins clocking 1610 data out at the beginning of the next sample cycle. 1610 data is clocked at 32 times the sample frequency and appears on the bus at SADOL and SADOR. Simultaneously, the primary D/A channels are being clocked out by GBCLKOUT. GBCLKOUT is produced by delaying BC by one MC cycle and gating it with BGATEOUT, a ROM output. A total of 18 BCs are used, clocking the full output word to the primary D/As. During this time (the first half of the sample period), the HSPs may write the `DASECL/` and `DASECR/` data to the input registers. A second pulse of `NLDAD/` transfers the secondary data to the serial output registers of the HCT597s. This data is shifted out to the motherboard (appearing on DADL and DADR) during the latter half of the sample cycle. This is accomplished by a second pulse of BGATEOUT producing a second set of 18 GBCLKOUT clocks.

The Host µP uses its transfer registers as a source and sink of digital audio data to and from the WET bus. As with the A/D and D/A registers, the HSPs supply addresses and control signals governing the WET bus transactions. Decoders U91 and U92 generate address derived strobes as shown in Table 4.15.

**Table 4.15. Address-derived strobes.**

| Write Address | Strobe | Function |
|---|---|---|
| $C0017 | SP2WR/ | Write to Slave Pair 2 control reg. |
| $C0016 | SP1WR/ | Write to Slave Pair 1 control reg. |
| $C0015 | SP0WR/ | Write to Slave Pair 0 control reg. |
| $C0014 | (not used) | |
| $C0012 | XFEROUTHI/ | Writes high byte to transfer out |
| $C0011 | XFOUTMID/ | Writes middle byte to transfer out |
| $C0010 | XFOUTLO/ | Writes low byte to transfer out |

| Read Address | Strobe | Function |
|---|---|---|
| $C0007 | SOFTR/ | Soft reset (generates SR/) |
| $C0006 | (not used) | |
| $C0005 | (not used) | |
| $C0004 | RDPEAKR/ | Read peak detect right channel |
| $C0003 | RDPEAKL/ | Read peak detect left channel |
| $C0002 | XFERINHI/ | Read xfer reg. high byte |
| $C0001 | XFERINMID/ | Read xfer reg. middle byte |
| $C0000 | XFERINLO/ | Read xfer reg. low byte |

The Host µP writes a value to the 24 bit transfer out register by writing the low, middle, and high bytes to `$C0010`, `$C0011`, and `$C0012`. Host µP `D<7:0>` is latched into U62, U76, and U90. To read the contents of the transfer out register, the HSP must read wet address `$3F`. Wet address `$3F` generates `RDXREG/`, enabling U62, U76, and U90 onto the bus. To write a digital audio word to the transfer in register, the HSP must write to wet address `$3E`. Wet address `$3E` generates `WRXREG/`, latching wet bus data into U61, U75, and U89. The Host µP may read this word by reading `$C0002`, `$C0001`, and `$C0000`, generating `XFERINHI/`, `XFERINMID/` and `XFERINLO/`. The uses for the transfer registers are many and include: download of wave tables to the HSPs; diagnostic testing of the HSPs; monitoring of intermediate HSP calculations; and even upload of samples to the Host for FFT or other analysis.

Sheet 9 of the schematics shows the digital peak detect circuitry. The digital peak circuitry detects and holds the values of peaks in the digital audio data with eight bit resolution. Byte-wide latch U63 holds the old peak value. When bit 23 of the WET bus is low, indicating a positive value (WET bus is 2's complement), comparators U77 and U78 compare the old peak value, latched in U63, with the current WET bus value, the high-order byte of which is presented on bits WETDB22 through WETDB15. If the WET bus value is greater than the stored value, then U63 is clocked, latching the present value in as the new peak. Comparator output is gated by the output of mux U103, indicating a WET bus I/O operation, and by ZRCLK, to allow propagation time. Latch U63 and U64 are clocked simultaneously. By reading location `$C0003`, the Host µP reads the 8 MSBs of the previous peak and simultaneously clears U63, enabling it to start a new cycle of peak detection. The time between µP reads of the peak detector sets the periodicity of the peak detect. The signal PEAKSEL determines which of the WET bus I/O operations is monitored by the detector. With PEAKSEL low, U44 gates `ADINL/` and `ADINR/` to the detectors. With PEAKSEL high, the D/A primary left and right channels are monitored. The right section of the peak detect circuit functions identically to the left.

---

## 4.4 Host Processor Board (Rev. 2 and up)

> **Note:** The Rev. 2 and up Host Processor boards are revisions of the original Rev. 1 board, incorporating all ECOs. The Rev. 2 and up boards also use multi-layer technology for improved signal quality.

The Host Processor is a 68008-based microprocessor system that interprets external control events and services the needs of the slave/High Speed Processor subsystems. External control events include multiple LARCs, MIDI, and (in the future) Computer Automation communications. The slaves rely on the Host Processor for program download and control via interrupts, reset, and DMA read/write to slave memory. The Host also provides system clock generation, digital audio I/O, Serial-to-Parallel and Parallel-to-Serial conversion, and support of the audio parallel bus.

The Host Processor hardware kernel is shown on sheet 1 of the schematics. An 8 MHz clock is generated by the 16 MHz crystal oscillator module U14 and counter U13. U13 also generates MIDICLK (500 kHz) and ERRCLK (62.5 kHz). MIDICLK is used by the DUARTs for either timing or MIDI baud-rate communication. ERRCLK is used by U12 to flag bus time-out errors on the processor bus.

Bus operations are best explained by walking through a typical bus transaction. The 68008 places an address on A19–A0, a code indicating access type on FC2–FC0, and then strobes valid address by bringing `AS/` low. For any function code other than 111 (or access type Interrupt Acknowledge), the output of U27 is driven low, enabling U23 and U24. U23 decodes which area of memory is being accessed. If the memory access is to ROM or RAM, U24 selects the appropriate IC. In the case of a ROM access, U23 drives MEMSEL high. MEMSEL is delayed for two 8 MHz cycles by U10. This delayed edge propagates through U27 and U21, finally bringing the `DTACK/` input to the 68008 low. `DTACK/` low completes the asynchronous bus handshake; the 68008 brings `DS/` and `AS/` high. `AS/` high drives AS low, clearing U10 and releasing DTACK. The 68008 responds by commencing the next bus transaction.

The memory map in U23 reflects the maximum configuration possible: four 1-Mbit ROMs and two 32k × 8 nonvolatile RAMs. The map in device U24, which performs the ROM and RAM Chip Selects, will change as device sizes are changed. The intent is to provide DTACK generation for any possible system with a single U23, and change U24 for specific configurations. DTACKs are generated by U10 for the cases ROM, RAM, RAMCART, and Strobes. In the case of DUART access, the DUARTs generate DTACKs. DTACK is generated by the slave DMA circuit for the case of slave channel access. There are two remaining cases of DTACK generation. The DUARTs generate their ordinary `DUARTxDTACK/` in the case of an Interrupt Acknowledge cycle after a DUART interrupt. Device U23 generates a MEMSEL DTACK in the case of a level 7 or level 2 Interrupt Acknowledge. This is accomplished via signal `IACKSTB/`, generated by U21.

Bus Errors are closely connected to the asynchronous bus handshake. If, through program error, the 68008 presents an address outside the limits of the maximum system, U23 will fail to decode. No device will respond with DTACK, and the µP will hang in the middle of its handshake, waiting for the `DTACK/` falling edge. After four cycles of ERRCLK (64 µsec), U12 drives the `BERR/` input to the 68008 low, forcing a Bus Error Cycle. The 68008 responds by beginning a Bus Error exception process, fetching a specific vector and commencing execution at that location. Information about the errant bus cycle is preserved in a stack frame to permit analysis of the fault. Bus errors may also be generated during slave access. If a slave fails to respond to the Host's request for bus access, a bus error cycle is initiated after 64 µsec.

The operating system distinguishes between several classes of bus error:

- Bus error during power-up diagnostic check of NVRAM, RAMCART, etc., indicating faulty DTACK hardware.
- Bus error during power-up diagnostic check of DUARTs, indicating faulty DUART hardware.
- Bus error at run-time due to access of non-existent memory, indicating either a hardware or program logic fault.
- Bus error during initial access of a slave, indicating no slave in place.
- Bus error during subsequent access of a slave, indicating a defective slave.

There are four types of resets in the system: power-up reset to the 68008 and slave processors; hard reset of the 68008 due to power failure; 68008 generated reset; and 68008 generated reset to the slaves, `SR/`.

Devices R21, C24, and CR6 generate `POPI/` (Power-On Prime) on power-up. `POPI/` forces U36 to drive HRESET, driving the 68008's `HALT/` and `RESET/` pins low simultaneously. This reset condition lasts for about 100 msec. Upon release of `POPI/`, the 68008 fetches two vectors needed for initialization: the Supervisor Stack Pointer and the Initial Program Counter. Fetching these vectors requires eight byte read operations. During this time a mechanism operates to ensure that these fetches occur from the first eight locations of ROM0. HRESET high loads zeros into shift register U28, driving `MAP/` low. `MAP/` stays low for the next eight `AS/` falling edges, forcing selection of ROM0 through U24. After the eighth fetch, `MAP/` goes high and the 68008 begins execution at the location specified by the Initial Program Counter. During hard reset the system accesses ROM for its initialization. At all other times, base or zero page is located in NVRAM, allowing soft write of the exception processing vectors.

The `RESET/` line of the 68008 is bidirectional/open collector. Execution of a RESET instruction drives `RESET/` low, resetting the DUARTs and slave interrupt flop, but leaving the slave processor's unaffected. The 68008 may read location `$C0007`, strobing `SOFTR/`, which drives `SR/` (System Reset) low, resetting all slaves. `SR/` is also driven active by `POPI/` (Power-On Prime), so that the slaves are reset at power-on. A separate mechanism for resetting slaves individually is discussed below.

The 68008 supports three levels of external interrupt. `PF/` (Power Fail) drives interrupt level 7, the highest level. DUARTs U7 and U6 drive level 5, the second-highest level. `SLAVEINT/` (slave Interrupt) drives interrupt level 2, the lowest level. Priority encoder U17 places the current highest level on `IPL2/0`, `IPL1/`, holding lower priority interrupts pending.

Host interrupt processing is best explained by walking through each of the possible interrupt cycles: slave, Power Fail, and DUART.

A slave Z80 requests service by driving `SLAVEINT/` low. `SLAVEINT/` is buffered by U20. The buffered signal, `SLAVINTB/`, clears U8, making `IR2/` active. If neither `IR5/` nor `PF/` is active, `IR2/` is encoded by U17 and presented to the 68008. The 68008 responds within an instruction cycle if interrupt level 2 is enabled.

The interrupt level is output on the address bus, function code FC2–FC0 is set to 111, and `AS/` is set active. U22, the IACK decoder, is enabled by FC2–FC0 high, and outputs `IACK2/` active. `IACK2/` clocks U8, removing the `IR2/`. `IACK2/` enables U26, sending 66 decimal on D7–D0. `IACKSTB/` is active, forcing U23 to set MEMSEL, initiating a `DTACK/` handshake. The 68008 completes the bus cycle, fetches user vector 66 from its base page memory (NVRAM), and commences interrupt exception processing.

The Motherboard sets `PF/` active upon detecting low unregulated DC on the 5V power supply. `PF/` is encoded by U17 and presented to the 68008 as interrupt level 7. Level 7 is the highest priority, and not maskable by the µP. The train of events is similar to the case of `SLAVEINT/`: an interrupt acknowledge cycle is decoded by U22; `IACK7/` enables U26; vector 67 is thus returned to the µP; `IACKSTB/` is input to U23 and U23 sets MEMSEL active, completing the DTACK handshake. The 68008 then commences interrupt exception processing.

DUART interrupts employ a different hardware path. The 68681s, U6 and U7, each have `IRQ/` and `IACK/` signal lines. `IRQ/`, output from the DUART, signals that an interrupt condition has occurred. `IACK/` is an input to the DUART that signals a 68008 IACK bus cycle. Due to the limited number of interrupt levels available, both DUARTs share interrupt level 5, in round-robin fashion. Let us presume that DUART1 (U7) has just completed transmission of a character and is set up to issue an interrupt on TX Ready. U7 drives `IRDUART1/` active. `IR5/` is driven active by U21, encoded by U17, and presented to the 68008. The 68008 responds with an IACK cycle. `IACK5/` is generated by U22. U7 responds by placing the contents of its Interrupt Vector Register on the data bus D7–D0. U7 completes the DTACK handshake via the `DUART1 DTACK/` signal. If DUART2 (U6) were to issue an `IRDUART2/` during DUART1's IACK cycle, or while DUART1's IRQ was being held pending (by 68008 mask), DUART2's interrupt request would be held pending, with the `IRQ5/` issued only after DUART1's IRQ had been removed.

The principal system features of DUART interrupts are:

- DUART interrupts may be programmed to occur on TX, RX, and Timer/Counter events as described in the 68681 manual.
- DUART1 and DUART2 interrupts are serviced in round-robin fashion, both arriving at IR level 5, second in priority only to Power Fail.
- Each DUART issues a user vector number, programmed by register, which points to an entry in the user vector table in NVRAM. Thus, each DUART may have its own interrupt service routine or routines. The µP must poll the DUART requesting service to determine which event triggered the interrupt.
- The DUART round-robin circuit arbitrates the hardware interrupt requests. However, since the 68008's interrupt mask is set with software, the service routines may set the interrupt mask to allow interruption of one DUART's service routine by the other's requests.

Host communication to the slaves is via DMA on one of six 16k byte channels, one channel dedicated per slave. See the address map for definition of the boundaries of the slave channels. PAL U23 sets `SLAVEAS/` active when a read or write operation is to one of the slaves. Buffers U30, U19, and U20 are enabled by `SLAVEAS/`, and present address bus A19–A0 to the slaves as PAB19–PAB0.

The slave DMA interface operates in either byte mode or block mode. In byte mode, `BLOCK/`, originating at DUART1, is set inactive. A16–A14 appear at hex D-latch U44. The falling edge of `SLAVEAS/` latches this high order address into U44. U31 decodes the address as being in one of the six channels and sets one of its outputs. This output is buffered by U32 and appears as one of `DMAREQ5/` to `DMAREQ0/`.

The slave Z80 receives the DMAREQ as a Bus Request. After completion of its current instruction cycle, the Z80 relinquishes its bus and returns Bus Grant, which appears as a low on the open collector wired-or signal `DMAACK/`. During this time, the 68008 is held with DTACK incomplete. `DMAACK/` low satisfies gate U51, and permits U16 to generate `DMADTACK/`.

On the next processor access outside of the slave channels, AS will be high indicating valid address. This is delayed one 8MCLK edge by U16 and appears at U50 as ASDELAY. `SLAVEAS/` is high (since we are outside the slave channels), `BLOCK/` is high, and U50 clears U44. This removes the DMAREQ from `DMAREQ5/` – `DMAREQ0/`. The slave last accessed is released, and processing continues.

Note that "byte mode" is a misnomer in that multi-byte operations are supported. Any byte or multi-byte write, read, or read/modify/write access to a slave will run as an automatic event under byte mode. This is possible since the slave bus is not relinquished until the 68008 accesses its own memory outside the slave channel space.

The slave channel block mode permits the host µP to read or write the memory space of a particular slave without relinquishing control of the slave busses between accesses. First, the Host µP sets `BLOCK/` active (Output Bit 4 of DUART1). The Host then accesses the first byte in slave memory space. Operation for this first access is identical to that of byte mode, except that U50 does not clear U44. U44 remains latched, the slave remains in Bus Grant, and `DMAACK/` remains low. Subsequent accesses to the slave are made with U16 generating `DMADTACK/` after the falling edge of `SLAVEAS/`. To terminate block mode for a particular slave, the host µP sets `BLOCK/` inactive. On the next memory access outside of slave channel space, U50 clears U44, releasing the slave.

There is one final mechanism for controlling slaves. The host µP may write to a register on the slave/HSP PCA (Processor Control Adder), setting `RESET/` and `INT/` for each slave processor. There is one write-only register per slave/HSP PCA, controlling two slave processors, as shown in Table 4.16.

**Table 4.16. Write-Only Registers.**

| D3 | D2 | D1 | D0 | Function |
|---|---|---|---|---|
| 1 | 1 | 1 | 0 | INT/ Lo-order Slave |
| 1 | 1 | 0 | — | RESET/ Lo-order Slave |
| 1 | 0 | — | — | INT/ Hi-order Slave |
| 0 | — | — | — | RESET/ Hi-order Slave |

These registers are mapped into the Host memory as shown in Table 4.17.

**Table 4.17. Slave Write Addresses.**

| Address | Strobe | Function |
|---|---|---|
| $C0015 | SP0WR/ | Write address for Slave 0, 1 |
| $C0016 | SP1WR/ | Write address for Slave 2, 3 |
| $C0017 | SP2WR/ | Write address for Slave 4, 5 |

In order to reset slave 0, the Host µP writes byte `$0D` to `$C0015`. During this write, decoder U88 drives `SP0WR/` low. `SLAVEBUSEN/` is low, enabling buffer U33. Buffer U33 drives host D7–D0 onto PDB7–PDB0 (Processor Data Bus) on the backplane. `$0D` is presented to the slave register and latched on the rising edge of `SP0WR/`.

> **Editorial note (not in original manual):** The OCR source for this Rev-2 passage rendered the reset byte as `$00`; it has been normalized to `$0D` here and hardware-verified (see **Appendix A.1**). Whether the printed Rev-2 manual actually shows `$00` (a manual typo) or this is purely an OCR artifact is unconfirmed and would be settled by reading a clean copy of the page. Either way, `$0D` is the electrically correct value; `$00` would reset *and* interrupt *both* slaves simultaneously.

When the unit is powered on, slave registers are cleared by `SR/`, holding all slaves reset. If the Host wishes to stop all slaves as a result of some cataclysm, it asserts `SR/` by reading address `$C0007`. To initiate a program on a slave after power-up, the Host must:

1. Reset the slave by writing to its slave register.
2. Disable interrupts and task switching and assert `BLOCK/`.
3. Release the slave from reset by writing to its slave register. (This is necessary because a slave in reset doesn't respond to Bus Requests from the slave DMA interface.)
4. Immediately read or write to that slave channel. The slave now has its operations suspended and is held in Bus Grant.
5. Download a minimal program to slave location zero.
6. Reset the slave by writing to its slave register.
7. Deassert `BLOCK/`. Reenable interrupts and task switching.
8. Release the slave from reset.

Slaves may be interrupted by asserting `INT/` on the appropriate slave register, as described in Section 4.1.

The Host communicates over four external serial channels provided by two 68681 DUARTs. DUART1, U7, is memory mapped with its internal registers appearing at locations `$60000` through `$6000F`. DUART2, U6, appears at locations `$64000` through `$6400F`. DUART registers are summarized in Table 4.18 (identical layout to Table 4.8).

The DUARTs provide four serial channels, programmable for any of 20 baud rates from 50 baud to 38.4k baud, including the MIDI baud rate of 31.25k baud. U7 pins X1/CLK and X2 drive crystal Y1, 3.6864 MHz. U6 X1/CLK is driven at the same clock rate by HCT04 U9. Access to the DUARTs is mediated by R/W, `DUARTxCS/`, and `DUARTxDTACK/`, with A3–A0 being internally decoded to select one of the 16 internal registers. The DUART interrupt function is as described above.

DUART1 Channel A is dedicated to MIDI input and output. MIDICLK provides a 500 kHz (16 × 31.25k baud) clock to input pins IP4 and IP3 for this purpose. Additionally, MIDICLK is connected to IP2 to be used as a clock source for the 16-bit internal counter/timer. IP5, IP1, and IP0 on U7 are used for additional system status inputs. Buffers for the MIDI channel are located on the Motherboard. U7 Channel B is buffered by U2 and U4 and provides LARC1 serial. FB3 and FB4 (Ferrite Bead) serve to limit slew rate on the L1SD/ and L1SD outputs. R5 provides serial termination on the Receive Data differential inputs and R4 improves noise immunity. Output pins OP7 through OP0 provide control over various system functions.

DUART2 Channel A is dedicated to Computer Automation functions, buffered by U1 and U3, and may run at any of the 20 baud rates including MIDI rate. DUART2 Channel B is dedicated to the second LARC. LARC2 inputs and outputs are buffered and terminated similarly to those of LARC1. All serial receive channels are quadruple-buffered internally. All serial transmit channels are double-buffered internally. On DUART2, IP2 provides a WC0 (Work Clock Out) input. IP1 monitors W1 jumper for setting test or diagnostic modes, etc. Output pins OP7 through OP0 provide control over various system functions. DUART1 and 2 parallel input and output functions are summarized in Table 4.18.

Devices U40, U41, U42, and U43 are ROM sockets designed for 27512 EPROMs. PAL U24 decodes the chip select signals `ROM0/`, `ROM1/`, `ROM2/`, and `ROM3/`.

The remaining core functions of the Host processor are shown on sheets 2 and 4 of the schematics. Connector J3 is the interface to the nonvolatile RAM Cartridge. The RAM cartridge is mapped by PAL U23 to `$70000` through `$77FFF` and may contain as much as 32k × 8 nonvolatile store, depending upon the cartridge in use. Buffers U15 and U18 present processor address bus A14–A0 to the J3 connector. These buffers are enabled by `RAMCASEL/`, generated by PAL U23. `RAMCASEL/` also serves to drive `CARTENABLE/` and `OUTENABLE/`. U25 drives `WRENABLE/` (cartridge write enable) low when the cartridge is selected and µP R/W is low. U29 buffers the cartridge data bus and µP data bus D7–D0.

Backup power for the RAMs and U46 is provided by two batteries, BT1 and BT2. When +5V is present, diode CR8 supplies current to bring BATVCC to approximately 4.5V. When +5V falls to 0V, CR7 and CR9 conduct, supplying approximately 2.6V to BATVCC, supplying standby voltage to the CMOS RAMs. BT1 and BT2 each have a capacity of 150 mAH. At typical leakage currents in the circuit, this provides battery backup for greater than 80,000 hours. The diode isolation between BT1 and BT2 prevents a defective battery from destroying NVRAM contents. Either BT1 or BT2 may be changed (with an isolated soldering iron) without disrupting RAM contents. U46, the RAM protect flop, is also a CMOS device powered by BATVCC. In response to a `PF/` interrupt, or other command to go into a standby state, the Host µP will complete housekeeping tasks dictated by software and then pulse DISRAM high. U46 will be reset with RAMBUFEN low. U47, which buffers the RAM select signals `HIRAMSEL/` and `LORAMSEL/`, will be disabled, preventing RAM access. On power-up, the Motherboard will keep `PF/` active for greater than 120 msec. This time is required for Host µP reset. When the processor comes out of reset, its first task will be to enable NVRAM by pulsing ENRAMSTB. RAMBUFEN will then go high and NVRAM access is permitted. U47, the isolating gate, is an LS-family device to prevent excessive leakage while in power-down. Note that on power-up, U51 forces `MUTE/` to the Motherboard. Before enabling RAM, the µP will wish to set FORCEMUTE high, forcing `MUTE/` active while slaves are brought to life.

The remaining functions of the Host are system clock generation and digital audio interface. There are three principal clocks in the system: `WCB/`, `BCB/`, and MCB — buffered Word Clock Bar, buffered Bit Clock Bar, and buffered Master Clock, respectively. Internal to the Host these are generated as BC, BC/, MC, and WC/. The 8 MHz processor clock is also supplied to the system as 8MCLKB.

With the exception of 8MCLKB, the system clocks are derived from MC. MC (Master Clock) is provided by either the Phase Lock Loop or one of two internal crystal oscillators. Regardless of MC source, the generation of BC, BC/ and WC/ is identical. MC is driven by the 1Y output of the multiplexer U102. MC clocks U104, a 74F161 configured as a divide-by-five counter. The rising edge of BC/ is coincident with the rising edge of MC. BC/ remains high for three MC periods, then goes low for two periods. BC is the inverse of BC/, as generated by the 74F04 U103. BC rising edges clock U105 and U106, which together constitute a divide-by-64 counter. The six bits of this divide-by-64 counter (64CLK5 – 64CLK0) drive the state ROM U65. U65 is used to control serialization and 1610 transfers. 64CLK5 is a square-wave clock at the sample frequency. The rising edge of 64CLK5 clocks U91, setting it. WC/ is driven low, and remains low for two MC periods until BC goes low, clearing U91. U104, U105, and U106 constitute a divide-by-320 counter. Thus, at an MC frequency of 15.36 MHz, a sample frequency of 48 kHz is generated. At an MC of 14.112 MHz, the sample frequency is 44.1 kHz.

When operating with external bits in (1610 interface), the bits-in source supplies a sample frequency square-wave clock. This clock appears, in buffered form, as signal WCI at U97. It is necessary to generate all system clocks in phase-lock with this signal. When MCSEL0,1 are set to 11, U102 routes the output of U103-6 to MC. U103-5 is driven by Q3, a level converter, which is in turn driven by the ECL oscillator U107. By virtue of the varactor diode VRC1 on its tank circuit, U107 is a VCO, or Voltage-Controlled Oscillator. The MC4044 amplifier, in conjunction with the transistor Q2 and associated discretes, serve as a LPF, or Low-Pass Filter. The LPF is driven by the phase detector section of U92. The phase detector compares input signals WCI/ (the external reference) and WC/ (the output of the divide-by-320 chain). The phase-detector, LPF, VCO, and divider chain constitute a fixed divide ratio frequency synthesizer with MC as the output and WCI as the input.

The VCO is switched between a high and low range by a second varactor, VRC2. The signal VSEL is high when MCSEL1,0 = 10. VSEL thus biases VRC2 with approximately +4.6 V, setting its capacitance to a low value of approx. 24 pf. This is appropriate for a WCI input frequency of 48 kHz. When MCSEL1,0 is set to 11, VSEL is set to 0V, and VRC2 is biased at a voltage less than 5V. This lower bias voltage results in a higher varactor capacitance, so that the VCO will run at 44.1 kHz. The bits-in interface (1610) is specified at 44.1 kHz; however, the interface will run at 48 kHz, a non-standard 1610 frequency. When running on external word clock, the internal crystal oscillators, U89 and U90, are not powered on. Transistor Q1 is in cut-off. This is to prevent beating between the internal oscillators and the Phase Lock Loop VCO.

In addition to the 48 kHz and 44.1 kHz external clock modes described above, the clock generation circuit will also run 44.1 kHz and 48 kHz internal. When MCSEL1,0 = 00 or 01, Q2 is saturated and either 15.36 MHz or 14.112 MHz is selected at MC by U102. MCSEL1,0 = 00 selects 15.36 MHz; 01 selects 14.112 MHz. Note that the U104, U105, U106 counter chain functions identically whether internal or external clocks are chosen. When running from either of the internal oscillators, the PLL VCO is unconnected. The PLL is thus open loop, and runs to either its highest or lowest frequency, depending upon: internal states in the MC4044; whether external WCI is present; and frequency chosen.

The 1610 interface requires an output word clock, WCO. The Host will fulfill this requirement by either passing on the received 1610 word clock in, WCI, or by passing on an internally derived clock 64CLK5. The received 1610 clock, WCI, is buffered by U97, a Schmitt trigger inverter. U97 pin 8 drives CR18, connected to R52 and C75. When WCI is present, U97 pin 3 will be pulled low and WCPRES will go high. WCPRES is available to the 68008 µP as an input at the DUARTs. If the µP sets `WCOFF/` active, then 64CLK5 will be selected through U96 and will appear as WCO. If `WCOFF/` is inactive, WCI will be selected as WCO. If WCI is not present, WCPRES inactive guarantees that 64CLK5 is selected as WCO.

Four functional blocks on the Host PCA manipulate digital audio data. Input data from the 1610 interface or the A/D converters is converted from serial to parallel by the serial input registers. High-speed processor output is converted from parallel to serial and transmitted by the serial output registers. The digital peak detect circuit monitors either A/D inputs or D/A outputs. The transfer registers permit interchange of audio data between the Host µP and the high speed processors.

Timing and control EPROM U65 provides control signals for serial input and output. U65 is addressed by 64CLK5-0, generating 64 states per sample period. Data slew is eliminated by clocking register U78 with BC. The serial timing and control signals appear in phase lock with the sample frequency at bit clock rate.

Digital audio input comes from either 1610 format bits-in or 480L internal format from the motherboard A/D converters. The 1610 format is 16 bits; internal format is 18 bits. Schematic page six shows the input registers. SELIN, supplied by DUART1, selects the input mode. With SELIN high, GBCLKIN is selected at U99 and clocks the SCLK input of the input registers. GBCLKIN (Gated bit clock in) appears at rising edges of BC and is gated by the signal BGATEIN from the timing ROM. Serial input data from the motherboard (ADDB) is selected by U99 to appear at U57 serial input. U84's serial output (PASSOUT) is passed through to the second set of registers — U56, U70, and U83. Serial data from the A/Ds is presented by the motherboard at ADDB in two bursts of 18 bits, left channel first, followed by right channel. The HCT595 serial registers are fully buffered. The outputs at A,B,C,D,E,F,G,H are the contents of an output register; shift register operations proceed without disturbing the contents of the output register. The first BGATEIN pulse lasts for 24 BC clocks and clocks the 18 left channel bits so that the MSB appears at position H of U84 and the LSB appears at position G of U57. The second BGATEIN pulse also lasts for 24 BC clocks. The left channel data appears at PASSOUT and is clocked through the U99 multiplexer into U56, U70, and U83. Meanwhile, the right channel data appears at ADDB and is clocked into U57, U71, and U84. WC/ pulses low on the last BC period of the sample. This pulse transfers the parallelized data from the shift registers into the output registers of the HCT595s.

A small digression to explain WET bus operation is now in order. The WET Bus transfers parallel audio data from input and output to the high speed processors and intermediate values between the high speed processors. It consists of 24 data lines (`WETDB<23:0>`), five address lines (`WETADB<4:0>`), and two control lines (`IORD/` and `IOWR/`). The Host is a passive partner in WET Bus transactions; only HSPs drive the address and control lines. For example, to read the A/D left channel input, an HSP places `11100` b on the WETADB and simultaneously pulses `IORD/` low. This address is decoded by U95 (Schematic Sheet 7) as `ADINL/`. `ADINL/` enables the input register U56, U70, and U83 onto the WETDB. The addresses and function of Host peripherals on the WET bus are shown in Table 4.22 (same address/strobe assignments as Table 4.14).

A/D left and right input from the previous sample period are available for transfer to the wet bus during the entire current sample. As described below, the D/A data must be presented to Host output registers within two time slots.

1610 input operation is similar to A/D input. SELIN is set low. The input registers are clocked by 1610CLK. 1610 input data appears on SADILB and SADIRB. 1610CLK, generated by the timing ROM, clocks the 16 bits of 1610 data in and then clocks 8 additional cycles to bring the data to the top bits of the input registers. WC/ clocks the parallelized data into the HCT595 output registers. As with internal A/D inputs, the audio data from the previous sample cycle is available to the HSPs throughout the entire sample period. The Host microprocessor's only task in this operation is to set the input mode via SELIN.

Output of audio data to the D/As and 1610 interface is slightly more complicated. There are four D/A output channels. These four channels are supported by two sets of registers: U54, U68, U81; and U55, U69, U82 (sheet 7). The four D/A outputs are time-multiplexed into the two register sets. 1610 bits-out is supported by two separate sets of registers: U52, U66, U79; and U53, U67, U80. The HSPs write primary output data during the latter half of the sample period. WET bus writes to `DAPRIML/` and `DAPRIMR/` are latched into the input registers of all four sets of HCT597s. Note that 1610 output data is the same as the data presented to the Primary D/A channels. On the last BC period of the sample period, `NLDAD/` and 1610XFOUT pulse low, transferring the HCT597 input register data to the serial output registers. 1610OUTCLK begins clocking 1610 data out at the beginning of the next sample cycle. 1610 data is clocked at 32 times the sample frequency and appears on the bus at SADOL and SADOR. Simultaneously, the primary D/A channels are being clocked out by GBCLKOUT. GBCLKOUT is produced by delaying BC by one MC cycle and gating it with BGATEOUT, a ROM output. A total of 18 BCs are used, clocking the full output word to the primary D/As. During this time (the first half of the sample period), the HSPs may write the `DASECL/` and `DASECR/` data to the input registers. A second pulse of `NLDAD/` transfers the secondary data to the serial output registers of the HCT597s. This data is shifted out to the motherboard (appearing on DADL and DADR) during the latter half of the sample cycle. This is accomplished by a second pulse of BGATEOUT producing a second set of 18 GBCLKOUT clocks.

The Host µP uses its transfer registers as a source and sink of digital audio data to and from the WET bus. As with the A/D and D/A registers, the HSPs supply addresses and control signals governing the WET bus transactions. Decoders U87 and U88 generate address derived strobes as shown in Table 4.23 (same assignments as Table 4.15).

The Host µP writes a value to the 24 bit transfer out register by writing the low, middle, and high bytes to `$C0010`, `$C0011`, and `$C0012`. Host µP `D<7:0>` is latched into U59, U73, and U86. To read the contents of the transfer out register, the HSP must read wet address `$3F`. Wet address `$3F` generates `RDXREG/`, enabling U59, U73, and U86 onto the bus. To write a digital audio word to the transfer in register, the HSP must write to wet address `$3E`. Wet address `$3E` generates `WRXREG/`, latching wet bus data into U58, U72, and U85. The Host µP may read this word by reading `$C0002`, `$C0001`, and `$C0000`, generating `XFERINHI/`, `XFERINMID/` and `XFERINLO/`. The WC0 input to DUART2 may be used to monitor WC by the Host, synchronizing Host execution with the sample period. However, an exchange of flags between the Host and Slave is more appropriate for mediating most transfer register exchanges. The uses for the transfer registers are manifold and include: download of wave tables to the HSPs; diagnostic testing of the HSPs; monitoring of intermediate HSP calculations; and even upload of samples to the Host for FFT or other analysis.

Sheet 9 of the schematics shows the digital peak detect circuitry. The digital peak circuitry detects and holds the values of peaks in the digital audio data with eight bit resolution. Byte-wide latches U61 and U62 hold the old peak values. When bit 23 of the WET bus is low, indicating a positive value (WET bus is 2's complement), comparators U74 and U75 compare the old peak value with the current WET bus value latched in U61 or U62, the high-order byte of which is presented on bits WETDB22 through WETDB15. If the WET bus value is greater than the stored value, then U61 or U62 is clocked, latching the present value in as the new peak. Comparator output feeds PAL U77. Latch U63 or U64 are then clocked simultaneously. By reading location `$C0003`, the Host µP reads the 8 MSBs of the previous peak and simultaneously clears U63 or U64, enabling it to start a new cycle of peak detection. The time between µP reads of the peak detector sets the periodicity of the peak detect. The signal PEAKSEL determines which of the WET bus I/O operations is monitored by the detector. With PEAKSEL low, U77 gates `ADINL/` and `ADINR/` to the detectors. With PEAKSEL high, the D/A primary left and right channels are monitored.

### DUART Output/Input Signal Tables (Rev. 1 = Tables 4.11–4.13; Rev. 2 = Tables 4.19–4.21)

**DUART1 Outputs and Signals.**

| Output | Signal | Notes |
|---|---|---|
| OP7 | DISRAM | Hi level disables non-volatile RAM |
| OP6 | MCSEL1 | (Master Clock source select, MSB) |
| OP5 | MCSEL0 | Selects Master Clock source: 00 = 15.36 MHz internal, 01 = 14.112 MHz internal, 10 = 15.36 MHz external, 11 = 14.112 MHz external |
| OP4 | BLOCK/ | Lo level enables block slave DMA mode |
| OP3 | PEAKSEL | Selects source monitored by peak detect circuit: 0 = Monitor A/D, 1 = Monitor D/A |
| OP1 | SELIN | Selects input to Serial-to-Parallel input registers: 0 = Input serial from 1610, 1 = Input serial from A/Ds |
| OP0 | WCOFF/ | Forces selection of internal clock for 1610 word clock |

> **Note:** The signal `OVLD/` is an open-collector wired-or output of the slave/HSPs. A pulse indicates that an overflow has occurred within the ARU. Pulses on `OVLD/` clock U8, setting OVLDB active. OVLDB is available as an input to DUART1. U8 is cleared by a low-going pulse on `CLROVLD/`. Clearing U8 sets OVLDB inactive.

**DUART2 Inputs and Signals.**

| Input | Signal | Notes |
|---|---|---|
| IP5 | PF/ | Input for monitoring power fail |
| IP2 | WC0 | Word Clock Out is available as a source of interrupts to synchronize Host operations to the sample period |
| IP1 | W1 | Input jumper |
| IP0 | BLOW/ | |

**DUART2 Outputs and Signals.**

| Output | Signal | Notes |
|---|---|---|
| OP7 | | Hi level signal illuminates CR3, the most significant LED |
| OP6 | | Hi level illuminates CR4 |
| OP5 | | Hi level illuminates CR1 |
| OP4 | | Hi level illuminates CR2, the least significant LED |
| OP3 | | Not used |
| OP2 | | Not used |
| OP1 | CLROVLD/ | Low-going pulse clears overload flop |

---

## 4.5 Motherboard

The 480L Motherboard consists of the following sections:

- MIDI interface
- ±15 V and +5 V linear supplies
- Two channels of audio input and A-to-D conversion
- Two D-to-A converters
- Four channels of audio output
- Timing and control section

In this description, left channel ICs are shown unbracketed and right channel are shown bracketed.

### 4.5.1 Audio Input Stages

Signals enter in either balanced or unbalanced mode thru a 3 pin XLR to a balanced differential input stage with active common-mode impedance boosting, U62 (U54). The gain of this stage is −10 dB, allowing +28 dBm signals to be directly connected to the machine without overloading the input.

The signal is routed to the input level pot and then to a gain stage, U63 (U55), resulting in +18 to −5 dB of gain before going to a hybrid 9-pole elliptical low-pass (20 kHz) filter, LPF6 (LPF5). This is followed by a 2-pole high-pass filter with a cutoff frequency of around 10 Hz. The 20 kHz LPF has a gain of −6 dB, and the high pass filter has a gain of 11 dB in their passbands.

The next stage is a track/hold amplifier which is comprised of a charge pump, U64 (U56); a DMOS switch IC, U65 (U57); a composite amplifier (consisting of a matched FET pair, Q12 (Q10), followed by a low noise bipolar op amp, U66 (U58)); and a FET-input low-offset op amp, U67, configured as an integrator, which nulls DC offsets in the circuit.

The sampled waveform from the track/hold stage then branches to two circuits. First, it is fed to a window comparator circuit U69 & U70 (U60 & U61), which will trigger if the absolute value of the level of the sample is greater than 1/4 (−12 dB) of the maximum A-to-D converter level (+10 V peak). This is done by comparing the sampled waveform to +2.5V generated by U68 (U59), derived from the reference voltage of the DAC in the A-to-D converter. The other circuit which is fed by the track/hold is a gain-ranging circuit U52 & U53 (U50 & U51), which will provide unity gain or gain of 4 (+12 dB), depending on the output of the window comparator circuit. The window comparator drives a precision one-shot, U27, which will immediately switch the gain-range circuit to unity gain if the signal exceeds +2.5V (1/4 of full scale), but will not switch back to +12 dB gain unless the signal remains below +2.5V for the full time-out period (about 75 ms) of the one-shot. This prevents "noise pumping" when the signal is constantly crossing the gain range threshold, and it means that the gain-range circuit need not maintain 18 or even 16 bit accuracy since gain changes occur relatively intermittently.

### 4.5.2 A-to-D Conversion

The output of the gain range circuit is fed to a 16-bit DAC, U47 (U45), in conjunction with a precision comparator U46 (U44), and a 16-bit SAR and latch LSI, U35 (U34), the CMU, performs a successive approximation conversion on the input signal.

At the appropriate time in the cycle, each channel's data is enabled from the CMU and loaded into a 16-bit parallel-to-serial shift register. The data is then shifted out to a high speed opto-coupler, U12, which then transmits the data to the backplane, where it is sent to the Host Processor board for conversion back to parallel format and subsequent processing.

### 4.5.3 D-to-A Conversion

Serial data is received from the Host Processor board via backplane connector P1, is opto-coupled by U3, and routed to two banks (left & right) of latching serial-to-parallel shift registers U22, 23, & 24 (U18, 19, & 21). Both channels are received simultaneously, each containing 18 bits of data per output channel. The main channels are received, latched, and outputted in the first half of the word clock cycle, followed by the auxiliary channels in the second half cycle. The latched data for each channel is immediately presented to that channel's DAC. There are two output DACs, one for the left (U31) and one for the right channels (U29). Each DAC converts both main and auxiliary channel data. The DACs are current output devices which are each followed by an op amp configured as a current-to-voltage converter, U32 (U30). The voltage thus obtained is sampled by the appropriate front or rear channel deglitch circuit. The deglitch circuits use the Blesser technique of charging a cap on the op amp's output, and then in the hold mode, switching the grounded end of the cap to the virtual ground inverting input node of the op amp. This is done to reduce acquisition time and to decrease hold mode noise bandwidth. These circuits are comprised of a quad DMOS switch IC (U36, 38, 40, 42), a low noise, high output current op amp (U37, 39, 41, 43) and associated components.

The deglitch circuits are followed by 2-pole aperture correction filters, U49 (U48), with a mid-band gain of −7.5 dB. These correct for the sinx/x loss inherent in the reconstruction process.

This signal is then routed to the 9-pole anti-imaging low pass filter LPF3 & 4 (LPF1 & 2), the same as used for input anti-alias filtering, with a loss of 6 dB in the passband. This is then passed through a passive single pole high pass filter and to the output level pots, which control the gain of the hybrid balanced output amplifiers OPA2 & 4 (OPA1 & 3).

The gain of this stage is 0 dB to +21 dB. This signal is routed to the 3 pin male output XLRs. Output muting is accomplished by clamping the inputs to the output amplifiers via low on-resistance FETs Q6–9. Muting occurs when either `MUTE/` from the Host Processor goes low, or if a power fail (`PF/`) is detected. These signals are opto-coupled by U8 and then level shifted (BMUTE) in order to drive the FETs.

### 4.5.4 Timing and Control

The 480L was designed to produce minimal noise. To that end, the motherboard operates on totally separate power supplies from the digital portion of the system, so that noise generated by the digital processing is isolated from the "audio world". The interface between these two separate systems is handled by opto-couplers, which allow clocks and data to be transmitted without the drawback of electrically connecting the two ground systems.

To minimize the number of opto-couplers required, digital audio data is transmitted and received in serial format, and only two clock and synchronization signals are received: `BCB/` (a 3.072 MHz clock, when operating a 48 kHz sample rate), and `WCB/`, a synchronization pulse which occurs once per sample period. The remainder of the timing signals used for A/D and D/A conversion are generated in a CMOS ROM, U6. `WCB/` is opto-coupled and inverted to become CLR which synchronizes the 8-bit counter, U5, to the rest of the unit. This counter is clocked by `BCLK/`, generated from `BCB/`. The ROM data is latched by U14 at the same time the counter is clocked. This means that the timing signals outputted by U14 are one BCLK period behind the ROM state, something to keep in mind when examining the timing diagram. The signal `SYNC/`, generated by the counter, is opto-coupled, inverted and run to the backplane via P1, where it is sent to the power supply board in order to synchronize the switcher to the sample frequency. This minimizes the generation of "beat frequencies" due to the combination of unrelated clock frequencies.

### 4.5.5 Conversion Chronology

When SAMP goes high, the track/hold circuit will begin tracking the filtered and gain conditioned input signal. This sample period is around 3.9 µs long, at which time the circuit goes into hold mode. During this sample period, `STAB/` is low, which enables the window comparator's output to be fed to the one-shot. If the signal is within the window (+2.5V), this signal will remain high, and the one-shot will not be triggered. If the signal is outside the window, this signal will go low, which will trigger a 75 ms long pulse from the one-shot. This pulse will immediately clear the D flop at the one-shot's output and cause the gain range signals to switch to unity gain setting (unless a sample within the past 75 ms had already cleared the flop). When 75 ms elapses without retriggering the one-shot, the clear pulse goes away, and on the next rising edge of `STAB/`, the D flop clocks, thereby returning to gain of 4 mode. 1.3 µs is then allowed for the gain-range amp and comparator to settle before the CMU chip containing the SAR latches the first (most significant) bit. The successive approximation then continues for the remaining 15 bits, as controlled by CCLK. Notice that the SAR is cleared and the MSB set for the next conversion immediately following the LSB being converted. This is to allow as much time as possible for the DAC's MSB to settle.

Meanwhile, the status of the gain range bits is clocked into another D flop, the output of which, GRL, is fed to the timing ROM. The just-converted 16 bit word for the left channel is enabled onto the ADC bus by `INL/`, and loaded into the parallel-to-serial shift registers, U26 and U28, by `LD/`. If GRL is low, indicating the signal is greater than +2.5V, CLKINH is disabled by the timing ROM and the 16 bit word is shifted out on each successive rising edge of BCLK. This is followed by 16 shifts of 0. Thus the 18 bit word transmitted is the 16 MSBs generated by the ADC followed by two 0s.

If GRL is high, indicating the ADC data has been gained up by a factor of 4 (input signals less than +2.5V), CLKINH is enabled, which inhibits the clocking of the shift register for two BCLK cycles, and then goes away. The 18 bit word then transmitted consists of the MSB repeated 3 times followed by the 15 remaining bits.

In the second half of the cycle, the right channel data is enabled onto the ADC bus by `INR/`, and clocked into the shift registers by `LD/`. Meanwhile, the right channel gain bit, GRR, will have determined whether or not the timing ROM should activate CLKINH, and the data will be shifted out as described above.

Simultaneous to the shifting out of the left channel A/D data, the left and right main output data is being shifted into the serial-to-parallel shift registers, MSB first, and clocked by `BCLK/`. After the 18th bit is clocked in, OCLK causes this data to be latched and enabled to the two output DACs U31 and U29.

About 2.5 µs is allowed for the DAC and I-to-V op amp to settle, after which the front channel deglitch circuit will acquire the signal. The acquisition period is approximately 7.5 µs, after which the deglitch circuit goes into the hold mode until new front channel data gets converted on the next cycle.

Simultaneous to the shifting out of the right channel A/D data, the left and right auxiliary output data is being shifted into the serial-to-parallel shift registers as above. Once again OCLK latches this data, it gets converted and the rear channel deglitch circuit will acquire and then hold the signal as the entire process gets repeated in the next cycle.

---

## 4.6 Power Supply

The 5 Volt Power Supply Board uses a switching regulator and is configured as a buck (DC-to-DC stepdown) regulator.

The transformer secondary is rectified by CR1 and filtered by C3 and C4. This results in a DC voltage of between 24 and 32 volts, depending on loading and line voltage. This voltage is chopped by a MOSFET switch, Q1, and the resultant squarewave is filtered by inductor L1 and capacitors C13 and C14.

Remote sensing of the output voltage is used in order to compensate for the IR losses in the wiring harness going to the backplane. With this scheme, the regulator IC U1 regulates the voltage at the backplane, and not at the actual outputs of the supply board. The regulator IC has a 5.00 volt reference output which is divided by R9 and R10 and sent to the non-inverting input of the transconductance error amplifier, pin 1 of U1. The +5 Volts on the backplane is divided by R7 and R8 and sent to the inverting input of the error amp, pin 2 of U1. C8 and R6 provide pole-zero compensation for the error amp. The output of the error amp is compared to a ramping waveform generated by the oscillator section of U1. The SYNC signal, via Q2, synchronizes this internal oscillator to the sample rate of the machine. R11 controls discharge time of the oscillator, while C9 and R3 are the components which control the free-run (non-synchronized) frequency and ramp rate. The output of this comparator goes through some gating functions to prevent double pulsing and then drives the gate of P-channel MOSFET, Q1. R13 and R14 set the proper gate voltage when pin 14, an open-collector output of U1, goes low, thereby turning Q1 on. CR3, a 16 volt Zener, prevents excessive source-gate voltage under high line conditions. CR4, a high current Schottky diode, clamps the drain of Q1 to about −0.5V when Q1 is turned off.

In short, a feedback loop is created which seeks to maintain the backplane voltage equal to the reference voltage by modulating the on-time (or pulse width) of the MOSFET. The greater the load or the lower the input voltage, the greater the duty cycle at which the MOSFET is operated, and vice-versa.

### 4.6.1 Power-Up/Down

The regulator IC has an undervoltage lockout circuit which protects the IC itself and the MOSFET it controls from inadequate supply voltage. If the input voltage is too low (below approximately 7V), the circuit disables the output drivers (pin 14) and holds the `RST/` pin low (pin 5). This prevents spurious output pulses while the control circuitry is stabilizing, and holds the soft start timing capacitor (C7) in a discharged state.

The soft-start circuit protects the rectifier diodes (CR1) and MOSFET (Q1) from high current surges during power supply turn-on. When the undervoltage lockout circuit releases `RST/`, an internal current source begins charging C7. As the voltage on this capacitor ramps up to +5 V, the duty cycle of the MOSFET linearly increases to whatever value the voltage regulation loop requires for an error null. Ramp time is about 100 msec.

### 4.6.2 Current Limit/Foldback

Current limiting is accomplished by sensing the voltage drop across a .02 ohm resistor in series with the +5V output line. With the configuration of R4, R5 and R18, a foldback effect is produced whereby the output voltage of the supply will drop as more current is demanded of it, beyond the current limit threshold. The current sense amplifier (pins 6 & 7) has a threshold of 100 mV. If this threshold is exceeded, the SHTDN pin (pin 8) goes low. This pin is tied to the `RST/` pin (which is bidirectional) which will cause the soft-start capacitor, C7, to be discharged and the output drive (pin 14) to be disabled, thereby shutting off the supply. Since no more current is being supplied, the current sense amp allows `SHTDN/` to return high (and thereby `RST/`) and C7 will begin charging. This allows the duty cycle of the MOSFET to ramp up as in the power-up sequence. If the output of the supply is a dead short (or close to it), this current limit sequence repeats itself until the short is removed. This is known as a "hiccup mode." The supply will keep trying to power up, but is immediately shut down due to excessive current draw.

### 4.6.3 Overvoltage Protection

The 5 volt supply is protected against overvoltage either by shorting to a higher potential supply or by failure of the regulator circuitry. There are two circuit configurations provided. When the MPC2005 becomes available, CR5, R19, and C16 will be eliminated. The MPC2005 is a monolithic overvoltage protector with built-in reference, comparator, and clamping SCR. It clamps the 5 volt supply to ground, thereby blowing fuse F1 if the supply voltage exceeds 6.2 volts. Until availability of this part, it is replaced by a 2N6400 SCR which, in conjunction with the three components previously mentioned, provides the same protection. As the voltage of the supply rises, CR5 will begin to conduct at 5.6 volts. If the supply voltage increases further, the voltage at the gate (pin 3) of the SCR rises due to the current flowing through R19. Once the voltage across R19 reaches approximately 0.7 volts, the SCR goes into conduction, shunting the supply to ground.

---

## 4.7 LARC

### 4.7.1 Power Supply

The power supply for the LARC is a 5V switching regulator. The central item in this regulator is an MC34060 or TL494 pulse width modulation (PWM) control chip. The 34060 produces an output control whose duty cycle multiplied by the input voltage is equal to 5V. This control is then applied to a pass transistor (Q1) located between the input voltage and an output filter. The output filter is a low-pass filter with a single pole at a frequency sufficiently low to attenuate the switching frequency and harmonic components in the switched square wave.

The input section is relatively simple. The LARC may be powered from one of two sources: from the mainframe through J1, or from an alternate power source through J2. Note that whenever a plug is inserted into J2, an integral switch disconnects the mainframe power source. C30 and FB3-4 form a simple RF filter for the mainframe power source; C23 and R13 provide a bypass for RF and static between the cable shield and LARC ground; and C31-33 and FB5-8 form a two stage RF filter for the alternate power source. The CR7 bridge rectifier is provided so that either AC or DC power may be used (the mainframe power is rectified). C35-37 form a composite filter capacitor operating over a large frequency range with low ESR. F1 was chosen through extensive testing to be a 1 amp fast fuse. Note, however, that one fault condition can occur that can not be protected by this (or any other) fuse: while the LARC is being powered by the mainframe, the fuse will not blow if a short occurs in the LARC circuitry after the regulator, because the mainframe can not provide enough power to blow the fuse. This fault condition will not damage the regulator or the mainframe.

The 34060 accepts a Vcc input (pin 12) from which the chip is powered and a 5 V reference (Vref, pin 14) is produced. This Vcc may be from 7 to 40 Vdc, and need not be carefully regulated. The dead time input (DT, pin 4) is used to "soft-start" the regulator; when DT is near Vref the regulator is effectively shut down, and when DT is near ground the regulator is allowed to function normally. Thus as C39 is charged from Vref through R19 and R20, the output of the power supply ramps up from 0 V to the normal 5 V output. The 34060 generates the switching frequency internally using the external timing components RT (pin 6 connected to R21) and CT (pin 5 connected to C40). The switching frequency is 1.1/(RT·CT), which figures out to approximately 50 kHz in the LARC. The output transistor of the 34060 is controlled by the product of comparators whose inputs are an internal ramp waveform at the switching frequency, the dead time input, and the sum of two other comparators whose inputs are pins 1 and 2, and 16 and 15. The first comparator is used to compare the regulator output voltage with the reference voltage. The second comparator (which is normally used for current limiting) is not used, and its inputs are tied off. The COMP input (pin 3) is used for compensation of the comparators. The output transistor is used common-emitter fashion to control the pass transistor.

The output section of the regulator consists of the pass transistor (a P-channel MOSFET) and output filter (a single pole LC low-pass filter). The pass transistor is turned on when its gate is pulled to ground by the output transistor of the 34060. R22 is used to quickly discharge the pass transistor's stray gate capacitance when the 34060 output transistor turns off. The output of the pass transistor is a 50 kHz square wave which swings from ground to the input voltage and whose average voltage is 5 V. The output filter (which consists of CR8, FB 9 and 10, L1, and composite capacitor C41 and C42) has its pole at 83 Hz and is used to block the 50 kHz (and higher harmonic) components of the square wave, yielding only the DC component at the output (the desired 5 VDC).

### 4.7.2 CPU

The central processing unit of the LARC is an 8749, containing the CPU, clock oscillator, RAM, UV-erasable ROM, and three 8-bit I/O ports on a single chip. The XTAL1 and XTAL2 (pins 2 and 3) are connected to a 4.608 MHz crystal, yielding a processor throughput of 307,200 instruction cycles/second. The ALE output (pin 11) is a 20% duty cycle square wave at the same frequency as instruction cycles (307.2 kHz), and is present whenever the 8749 has power. This is the first place to verify that the processor's clock is correctly functioning.

The three I/O ports are used as follows: The BUS port (pins 12-19) is used as a bidirectional data bus. It is used in two modes: in the tristate mode to transfer 8-bit data to the Litronix DL-1414 intelligent displays from the ADC0809 A/D converter, and both to and from the CDP1854 UART; and in the latched mode (through the NE594 buffer/driver) to scan the switches and headroom LEDs. Bits 0-6 of Port 2 are outputs used as the address bus bits A0-A6, and bit 7 is used as the FSK tape output. Bits 0-3 of Port 1 are used as inputs from the switch array (B0-B3), and bits 4-7 are used as outputs controlling which section/row is lit in the headroom LED array (S0-S3).

There are also several control pins on the 8749: the SS input (pin 5), which must be unconnected for correct operation; the EA input (pin 7), which must be grounded for correct operation; the `INT/` input (pin 6), which the UART pulls low to signal the processor when a character is available; the T0 input (pin 1), which the processor can read to determine if there was a framing error on the last character received (this feature is not currently used by the software); the T1 input (pin 39), which the processor reads during FSK tape input; the `PROG/` output (pin 25), which is normally used with an 8243 I/O port expander, but is used in the LARC to clock the address of the slider to convert into the ADC0809; and the RD, WR and PSEN (pins 8, 9, and 10) outputs, which are normally used for external memory access, but are not used in the LARC.

### 4.7.3 Reset Logic

Both the 8749 and the CDP1854 need to be reset after power up. A simple RC (R7 and C9) circuit is used as an input to a differential driver (U3, the µA9638) to produce the required RES and RES/ signals, which are asserted for approximately 1/4 second after power is applied. The CR5 Schottky diode is used to quickly discharge C9 when power is removed (or when power is momentarily lost). To manually reset the LARC, momentarily ground pin 3 of U3.

### 4.7.4 Address Decoding Logic

In order to be able to access the devices that share the data bus (the ADC0809, CDP1854, and 12 DL-1414s), an address decoder is used. Address bits A2-A5 are decoded into 16 low-active chip select lines using a CD4515 4-to-16 line decoder. Address bit A6 is used as the decoder enable so that any race conditions (which may cause glitches in the decoder outputs) are eliminated.

When addressing devices, the software in the 8749 goes through several steps to assure that the addressing is done without any glitches. When addressing devices for output (such as the CDP1854 and DL-1414s), the 8749 first places the output data on the BUS port, presents the address of the desired device on A0-A5, then pulls A6 low to address the device, and lastly pulls A6 high again to disable the device. When addressing devices for input (such as the CDP1854 and ADC0809), the 8749 first tristates the BUS port, presents the address of the desired device on A0-A5, pulls A6 low to address the device, then reads the desired input data from the BUS port, and lastly pulls A6 high again to disable the device.

A simple device address map is shown in Table 4.24.

**Table 4.24. Device Address Map.**

| Device | A5 | A4 | A3 | A2 | A1 | A0 |
|---|---|---|---|---|---|---|
| DL-1414, U1, Display Bd | 0 | 0 | 0 | 0 | C | C |
| DL-1414, U2, Display Bd | 0 | 0 | 0 | 1 | C | C |
| DL-1414, U3, Display Bd | 0 | 0 | 1 | 0 | C | C |
| DL-1414, U4, Display Bd | 0 | 0 | 1 | 1 | C | C |
| DL-1414, U5, Display Bd | 0 | 1 | 0 | 0 | C | C |
| DL-1414, U6, Display Bd | 0 | 1 | 0 | 1 | C | C |
| DL-1414, U1, Panel Bd | 0 | 1 | 1 | 0 | C | C |
| DL-1414, U2, Panel Bd | 0 | 1 | 1 | 1 | C | C |
| DL-1414, U3, Panel Bd | 1 | 0 | 0 | 0 | C | C |
| DL-1414, U4, Panel Bd | 1 | 0 | 0 | 1 | C | C |
| DL-1414, U5, Panel Bd | 1 | 0 | 1 | 0 | C | C |
| DL-1414, U6, Panel Bd | 1 | 0 | 1 | 1 | C | C |
| CDP1854 character output | 1 | 1 | 0 | 0 | X | X |
| CDP1854 character input | 1 | 1 | 0 | 1 | X | X |
| ADC0809 input | 1 | 1 | 1 | 0 | X | X |

Where: XX are don't cares, and CC is the code for the character within a DL-1414 display chip: 00 is the right-most character, 01 is the second from the right, 10 is the second from the left, and 11 is the left-most character.

### 4.7.5 ADC Logic

The first item of interest concerning the ADC0809 is its power source; in order to guarantee that any switching supply noise will not affect the converter, a filter is used between the 5 V supply and the ADC0809's Vcc input. The filter is an RC filter consisting of R12 and the composite capacitor C16 and C17. Since the ADC0809 is CMOS (and consequently low power), the voltage drop across R17 is minimal. Note also that all the analog inputs are decoupled for further noise immunity.

Parts of the addressing logic for the ADC0809 are slightly more complicated than the other chips on the data bus. The ADC0809's internal analog multiplexer address (the address of the slider to convert) is transferred to the ADC0809 using the 8749's `PROG/` output, which is normally used with 8243 Port 2 expander chips. When the processor wishes to change the address of the slider to convert, it uses a command which places a flurry of (mostly useless) information on A0-A3. During this command, the address of the slider to convert is placed on A0-A3 400 ns before the rising edge of `PROG/`, and is held for 90 ns after the rising edge.

After the processor sets up the address of the next slider to convert, the processor will read the results of the last conversion and start the next conversion simultaneously by addressing the ADC0809 for input as described in section 4. Note that the ADC0809's end of conversion (EOC) output is not used since the processor's software never accesses the ADC0809 more often than the 250 microsecond conversion time.

The last item of interest concerning the ADC0809 is the circuitry associated with analog inputs IN6 and IN7, which is used to measure the 5 V power supply's actual voltage. The circuit connected to IN6 is a resistor/zener diode constant voltage source (R10 and CR6). The digital code resulting from the conversion of this signal will change as the supply voltage to the ADC0809 changes, because the ratio of the supply voltage to the constant voltage will change. The circuit connected to IN7 is simply a resistive voltage divider (R9 and R11) with an adjustable output voltage. Since the voltage source to this divider is the same as the ADC0809 supply voltage, the resulting digital code from the conversion of this signal will be always a constant. If the adjustable voltage source is adjusted so that it is the same as the constant voltage source when the 5 V power supply is at 5.00 V, then the actual voltage of the 5 V power supply is calculated using a linearization of the system equations governing these circuits.

### 4.7.6 UART Logic

The UART data is read and written using the addressing scheme in section 4. The UART clock inputs (RCLK and TCLK pins 17 and 40), which are 16 times the 9600 baud data rate, are derived by dividing the 307.2 kHz ALE clock by two using 1/2 of the CD4013 flip-flop. The UART is strapped to provide and recognize 8-bit characters with no parity and 2 stop bits. The UART data available (DA, pin 19) output, which signals that the UART has received a complete character, is inverted before being used to interrupt the processor.

### 4.7.7 RS-422 Logic

The serial data to and from the UART is converted to RS-422 compatible signals by the µA9637 (U2) differential receiver and the µA9638 (U3) differential driver. The LC filter comprised of C27, FB1 and FB2 is used to rate limit the signal rise and fall times (and thereby reduce RF noise), and the R14 termination resistor is used to eliminate signal reflections.

### 4.7.8 Litronix Display Logic

The Litronix DL-1414 displays act very much like a memory device that happens to display its memory's contents. Once a character has been written to the DL-1414, it will be displayed without any need for refresh from the processor. When the addressing scheme from section 4 is used to output data to the DL-1414, the data on the BUS port is the character to display (in ASCII), the A0 and A1 lines correspond to the character to display within a given display chip, and the A2-A5 lines correspond to the address of the display chip. Remember that these lines are decoded by the CD4515 into low-going enable lines, which are connected to the `WR/` (pin 3) lines of the DL-1414s and used to clock the data into the displays. Remember that the characters within a chip are numbered from character 00 on the right to character 11 on the left.

### 4.7.9 Tape Interface Logic

Unused with 480L.

### 4.7.10 Buffered Bus and Sink Logic

The NE594 driver circuit buffers the BUS port and provides current drive capability for the headroom LEDs. No headroom LEDs, however, will light unless the appropriate current sink (the 75492, U4) is activated also. Therefore, when the processor is using the data bus to communicate with the DL-1414s, ADC0809, or the CDP1854, it keeps the sinks deactivated so that the LEDs do not light up spuriously. Upon reset of the 8749, all the bits on Port 1 and Port 2 are set to logic 1; therefore Port 1 bits 4-7 are inverted before the 75492 so the LEDs do not light up during power up. R5-R12 on the Panel board are provided for LED current limiting.

The Panel board switches are also scanned from the NE594 buffered BUS output. CR1-CR8 of the Panel board are provided so that "sneak paths" will not cause the LEDs to light if multiple buttons are pushed. R1-R4 of the Panel board provide a pulldown to ground, which is the default condition when buttons are not pushed.

Unlike many other Lexicon products, the LARC processor software does not scan its LEDs and switches simultaneously. The software first will scan the LEDs, lighting eight at a time: the data for each group is placed on the BUS port, then the appropriate bit on Port 1 is set low for several hundred microseconds, then it is set high again. After all the LEDs have been scanned, then the processor will scan all the switches, scanning four at a time: the appropriate bit for each group on the BUS port is set high, then the processor reads the B0-B3 bits from Port 1 to determine the states of the buttons in the selected column. Note that the processor scans only the switches during the Diagnostic Menu Mode; the LEDs are not scanned.

---

## 4.8 SME Board (Optional — requires V.2.0 or higher software)

The Sample Memory Expander (SME) is an optional processor board for the Lexicon M480L. The purpose of the board is to provide current and future users with the ability to increase the amount of audio storage currently provided with the standard M480L. The SME provides over twenty-one seconds of digitized audio storage in mono, or greater than ten seconds stereo storage at 48 kHz. All samples are stored as 18 bit words. The SME is conceptually divided into several logical blocks (See SME Block Diagram, Chapter 8.) The individual blocks are:

1. Slave Processor and Associated Circuitry
2. Writable Control Store
3. Micro Pipeline
4. Memory Management Unit
5. Digitized Audio Memory (1 megaword audio storage)
6. Disk Interfaces and DMA
7. Wet Bus Interface

The system works much like the HSP boards currently used in the 480L. The Z80 is controlled by the Host processor and is responsible for supplying and updating the microcode in the WCS. The WCS provides information to the DSP to drive the hardware to perform a specific function. The micro pipeline redistributes the microbits to provide correct phasing of control and data. Microcode also provides offset pointers fed to the MMU for audio addressing. The audio store is physically divided into four 256k word blocks of eighteen bits per word. An optional disk interface is provided and will, in the future, allow storage and retrieval capability all under DMA control. Audio is accessible to the rest of the system over the WET bus via the WET bus interface.

### 4.8.1 Slave Processor and Associated Circuitry

The Slave processor used on the SME board is an eight (8) MHz Z80 (U66). The processor is provided with a 32k × 8 static RAM for data and program storage. Programs and data are downloaded to the board from the Host processor via the DMA port composed of the address buffers (U25 and U65), the control buffer (U101) and the data buffer (U87). The Host releases the Slave from reset by removing the low level on the reset pin through quad latch U103. Once the reset has been removed the Host requests the Slave bus by asserting `DMAREQA/`. The Slave responds by asserting `BUSACK/`, thus enabling the DMA buffers to control the Slave environment. Note that on the very first access to the Slave environment it is assumed that the Host processor will read one byte or word. This will provide the Host with an identifier code set by jumpers W10-W17. The code on powerup is enabled onto the Slave data bus through U113 and flip-flop U165. Once the DMA request is removed, U113 is disabled by clocking U165. Upon completing this sequence the Host may now carry on in the normal mode.

Memory decoding is performed by PAL U102. This PAL also provides `WAIT/` to the processor for synchronization, and bus requests are also arbitrated between the disk DMA U155 and Host DMA requests. I/O decoding is performed by U104, U107, and U27. A map of both the memory decoding and the I/O decoding is provided below. `IORD/` and `IOWR/` signals for the DMA U155 and SCSI controller U115 are created by U121, U134, U123 and U124.

**SME Memory Decode**

| Strobe | Address | Function |
|---|---|---|
| RAM0/ | 0000H–7FFFH | ENABLE 32k×8 STATIC RAM |
| BANKA/ | 8000H–87FFH | WCS BANKA |
| BANKB/ | 9000H–97FFH | WCS BANKB |

**WCS Addressing**

| Bank | Address | Byte | Page |
|---|---|---|---|
| A | 8000H–817FH | NOT USED | 1 |
| A | 8180H–81DFH | 4 | 1 |
| A | 81E0H–827FH | NOT USED | 1 |
| A | 8280H–82DFH | 2 | 1 |
| A | 8300H–834FH | 0 | 1 |
| A | 8350H–857FH | NOT USED | 1 |
| A | 8580H–85DFH | 4 | 2 |
| A | 86E0H–867FH | NOT USED | 2 |
| A | 8680H–86DFH | 2 | 2 |
| A | 8700H–874FH | 0 | 2 |
| A | 8750H–87FFH | NOT USED | 2 |
| B | 9000H–917FH | NOT USED | 1 |
| B | 9180H–91DFH | 5 | 1 |
| B | 91E0H–927FH | NOT USED | 1 |
| B | 9280H–92DFH | 3 | 1 |
| B | 9300H–934FH | 1 | 1 |
| B | 9350H–957FH | NOT USED | 1 |
| B | 9580H–95DFH | 5 | 2 |
| B | 95E0H–967FH | NOT USED | 2 |
| B | 9680H–96DFH | 3 | 2 |
| B | 9700H–974FH | 1 | 2 |
| B | 9750H–97FFH | NOT USED | 2 |

**SME Slave I/O Map** — listing of the I/O ports for the SME Z80.

| Address (Hex) | Function |
|---|---|
| 0xh | DISK SELECT |
| 00h–0Fh | This section of I/O addresses varies in function based on the interface type used, SCSI or Floppy |
| 1xh | DMA SELECT |
| 10h | INIT PORT R/W |
| 11h | CHANNEL REGISTER PORT R/W |
| 12h | COUNT REGISTER PORT R/W |
| 13h | NOT USED |
| 14h | LSB OF MEMORY START ADDRESS, R/W |
| 15h | MID BYTE OF MEMORY START ADDRESS, R/W |
| 16h | MSB OF MEMORY START ADDRESS, R/W |
| 17h | NOT USED |
| 18h | DEVICE CONTROL REGISTER, R/W |
| 19h | DEVICE CONTROL REGISTER, R/W |
| 1Ah | MODE CONTROL REGISTER, R/W |
| 1Bh | STATUS REGISTER, R ONLY |
| 1Ch | NOT USED |
| 1Dh | NOT USED |
| 1Eh | REQUEST REGISTER, R/W |
| 1Fh | MASK REGISTER, R/W |
| 2xh | DAB REGISTER |
| 20h | LSB DAB WRITE REGISTER, W ONLY |
| 21h | MID BYTE DAB WRITE REGISTER, W ONLY |
| 22h | MSB DAB WRITE REGISTER, W ONLY |
| 23h | LSB DAB READ REGISTER, R ONLY |
| 24h | MID BYTE DAB READ REGISTER, R ONLY |
| 25h | MSB DAB READ REGISTER, R ONLY |
| 26h | CLEAR CURRENT POSITION COUNTER, R/W |
| 27h | WAIT ENABLE, R/W |
| 3xh | WORD CLOCK COUNT REGISTER AND CURRENT POSITION COUNT |
| 30h | WORD CLOCK COUNTER LSB, W ONLY |
| 31h | WORD CLOCK COUNTER MID BYTE, W ONLY |
| 32h | WORD CLOCK COUNTER MSB, W ONLY |
| 33h | WORD CLOCK COUNTER REGISTER LOAD, R/W |
| 34h | CURRENT POSITION COUNTER STORE, W ONLY |
| 35h | CURRENT POSITION COUNTER LSB, R ONLY |
| 36h | CURRENT POSITION COUNTER MID, R ONLY |
| 37h | CURRENT POSITION COUNTER MSB, R ONLY |
| 4xh | SLAVE INTERRUPT, R/W |
| 5xh | WCS PAGE SELECT (DATA BIT 0 DETERMINES PAGE) |
| 6xh | WRITE STATUS REGISTER |
| 7xh | READ STATUS REGISTER |

**Write Status Register (6xh) bit layout:**

| bit 7 | bit 6 | bit 5 | bit 4 | bit 3 | bit 2 | bit 1 | bit 0 |
|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | IOEN | CLEAR DISK INT | CLEAR DMA INT | CLEAR WC INT | CLEAR HST INT |

**Read Status Register (7xh) bit layout:**

| bit 7 | bit 6 | bit 5 | bit 4 | bit 3 | bit 2 | bit 1 | bit 0 |
|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | IOEN | DISK INT | DMA INT | WC INT | HST INT |

#### DAB Register

These registers are bidirectional latches (U100, U96, U90) that are used for transferring audio data to and from the audio store. The write registers (addresses 20h-22h) are used by the Slave to send data to the audio store. The microprogram is responsible for reading this information onto the DAB by asserting `SLVRD/`. The microprogram is also responsible for writing audio data into this register by asserting `SLVWRT/` for the Slave to read (addresses 23h-25h).

Clear current position counter (`CPCC/`) is used to clear the current position counter output register. The current position counter is composed of U127-U129 and U139-U140.

Wait enable is used in the same manner as the HSP board.

#### Word Clock Counter and Current Position Counter Value Register

The SME board has a Word Clock Counter (U1, U2 and U3). A register is provided to allow the count to be loaded to the counters without affecting the count. Once the count has been loaded to these buffers, the Slave strobes `CLOAD/` (addr 34h), loading the counters. The register is preloadable from addresses 30h-32h. When the counters carry out from the MSB, an interrupt is generated.

A set of registers has been provided for the Slave to read the CPC at any time (Read addresses 35h-37h). The Slave must first arm these registers by strobing `CPSTOR/`. Note that the Slave should now wait one sample cycle to insure that a current position clock occurs. The next current position clock will clock the current position −1 into registers U93-U95. The Slave can now read this value at any time without it being corrupted. The only way for the Slave to get a new value is to arm the clocking mechanism again.

#### Slave Interrupt

Writing to address 4xh generates a Slave interrupt to the host.

#### Page Select

The strobe is used to select the active page of the WCS. Writing with the data reset 1's bit set to 0 sets the page to zero. If this bit is set to 1, the page is set to one.

#### Write Status Register

This register (U91) is used to clear interrupts. Four sources are provided on the MXP, each of which is maskable. On power up all interrupts are disabled. By writing 1's to the proper bits, each of the interrupts can be enabled. Once an interrupt has been enabled an interrupt will be sent to the Z80. The interrupt is cleared by writing a 0 and then activating it by writing a 1.

#### Read Status Register

This buffer (U106) enables the Slave to determine which device has interrupted if the interrupts have been enabled. Otherwise the Slave can poll for interrupts.

### 4.8.2 Writable Control Store

The Writable Control Store (WCS) on the SME board is very similar to that of the current HSP boards. Clocking is generated by PAL U125. These clocks are used to determine the access to the WCS RAM U149 and U173 and also generate `PCCLR/` which starts the program counter (U161, U171) at zero. Access to the WCS RAMs for the Z80 occurs during phase A/ of the four-phase clock. For writing and reading to Bank A, buffer (U160), latch U159 and OR gates U146 are used. For access to Bank B, buffer (U170), latch U169 and OR gates U132 are used. Micro accesses are performed during phases B/, C/ and D/. For more detail on the WCS see the HSP circuit description.

#### Microcode Description

The microcode for the M480L is a 48 bit microword. The composition of the microword is shown below. Note that all even numbered bytes reside in bank A of the WCS, while all odd bytes reside in bank B.

| Byte | MS (7) | 6 | 5 | 4 | 3 | 2 | 1 | LS (0) |
|---|---|---|---|---|---|---|---|---|
| 0 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| 1 | MWR/ | MCEN/ | PROT/ | SLVWR/ | SLVRD/ | ADDREN/ | OREGWR/ | CPCLK |
| 2 | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 |
| 3 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 |
| 4 | IORD/ | IOWR/ | WOE/ | WADB4 | WADB3 | WADB2 | WADB1 | WADB0 |
| 5 | — | — | — | — | — | — | — | — |

The bytes 0, 2, and 3 are used to specify the offsets to the MMU. Byte 0 is latched during phase B/ and bytes 2 and 3 are latched during phase C/. Offset bytes are latched into the MMU augend registers which are summed with the output of the current position counter, which provides the addends for the calculation of the row-col addresses. These offsets are provided in the microcode as the 2's complement of the offset. Byte 1 is used to specify the source or destination of all audio transfers except for the WET bus transfers. Each bit is described below.

- **CPCLK** — Current Position Clock: used to clock the current position counter. The rising edge of this signal is the clocking edge to the counter; the falling edge clocks the value of the counter into the output registers.
- **OREGWR/** — Output Register Write: clocks audio data from a source into the WET bus output registers. Sources may be the Slave audio registers, audio memory, or the WET bus.
- **ADDREN/** — Address Enable: used to enable the micro controlled portion of the SME to access the audio store. During normal operation the DMA address circuitry is enabled for addressing the audio store.
- **SLVRD/** — Slave Read: used to enable data onto the DAB from the slave's audio data registers.
- **SLVWR/** — Slave Write: used to clock audio data from the DAB into the slave's audio registers.
- **PROT/** — Protect: used in conjunction with any audio access from the microcoded section of the machine. Its purpose is to prevent access to the DAM by the DMA section. The bit will be automatically set by the micro-assembler when appropriate. It must be pipelined one instruction ahead of the micro-instruction which requires access to the DAB.
- **MCEN/** — Memory Control Enable: indicates a microcoded memory operation is occurring.
- **MWR/** — Memory Write: used to indicate either a read or write to the audio store. It is used in conjunction with MCEN.

Byte 4 contains the five WET address bits used by each HSP to address all I/O ports in the system. A total of 32 addresses for I/O are provided. The I/O map is provided below.

| Hex Address | I/O Function |
|---|---|
| 10h | READ WET CH0 |
| 11h | READ WET CH1 |
| 12h | READ WET CH2 |
| 13h | READ WET CH3 |
| 14h | READ WET CH4 |
| 15h | READ WET CH5 |
| 16h | NOT USED |
| 17h | NOT USED |
| 18h | D/A PRIMARY LEFT |
| 19h | D/A PRIMARY RIGHT |
| 1Ah | D/A SECONDARY LEFT |
| 1Bh | D/A SECONDARY RIGHT |
| 1Ch | A/D IN LEFT |
| 1Dh | A/D IN RIGHT |
| 1Eh | WRITE XREG |
| 1Fh | READ XREG |

Bit 5, `WOE/`, enables all WET transactions. It is used to enable the WET output registers onto the bus or for reading from the WET bus onto the DAB. The two most significant bits of byte 4, `IORD/` and `IOWR/`, indicate a read or write operation during a WET I/O operation. For phantom reads the `IORD/` bit is set low without setting `WOE/` low. The last byte of microcode (byte 5) is not used.

### 4.8.3 Micro-Pipeline

The micro-pipeline is responsible for aligning microcode for driving the SME board through the proper phases of operation. Offset information is clocked directly from the WCS into the registers U152-U154. Control information is clocked into register U174 and is realigned by U165 and U137. These bits provide source and destination information for movement of data on the Memory Data bus (MD). Register U150 receives WET bus control and address bits from the WCS. These bits are reclocked by U158 and are used when a WET bus operation occurs.

### 4.8.4 Memory Management Unit

The memory management unit is responsible for providing offset pointer information to the Digitized Audio Memory (DAM). Offsets from the WCS are clocked into U152-U154. This information is subtracted from the current position pointer contained in counters U109-U111. The current position counter is clocked by setting `CPCLK/` active in the microcode. The counter can also be cleared by setting `CPCC/` low in the Slave status register. The result of the computation generated by adders U127-U129, U139 and U140 is used to generate nine bits each of row and column information for DAM addressing. Two bits for bank selection are also generated to select the 256k word bank currently used. Multiplexers generate the row and column information by manipulating the SEL line.

### 4.8.5 Digitized Audio Memory

The Digitized Audio Memory (DAM) is composed of four banks of 256k words. A word is composed of eighteen bits. These four banks are:

| Bank | Devices |
|---|---|
| Bank 1 | U68-U85 |
| Bank 2 | U47-U64 |
| Bank 3 | U28-U45 |
| Bank 4 | U7-U24 |

The memory has been designed to have DMA accesses performed by DMA controller U155, or to perform normal micro accesses from the DSP. The selection of the provider of row-column addresses is determined by the `ADDEN/` bit in the microcode. The default case has the DMA controller providing the addresses. The drivers responsible for providing addresses to the memories are U67 and half of U105 for micro accesses, and U88 and the other half of U105 for DMA accesses. Bank selection is decoded using OFSA bits 0, 1 for micro accesses and address bits A1 and A2 for DMA addressing. For RAS, CAS generation, PAL U178 is used. Half of U4 and half of U5 generate the selected bank RAS and CAS signals. By selecting only one bank at a time the power requirements of the system are greatly reduced. Termination resistors U6, U46 and U86, along with series resistors R1 and R8-R15, provide signal conditioning of the row addresses. DMA accesses are byte wide accesses. The bank is selected as above but the byte high or low is selected by decoding address bit A0 of the DMA. The decoding is performed by U121, U147 and half of U4 and U5.

> **Note:** Data transfers via the DMA port result in only 16 bit words being stored. The low two bits of the audio are discarded.

### 4.8.5 Disk Interfaces and DMA

> (Not supported as of v. 2.0 software release)

The SME board has been provided with two possible disk interfaces. Only one interface can be populated on the board at a time. The two interfaces provided are:

1. Floppy disk interface
2. SCSI interface

The Floppy interface is composed of floppy disk controller U156, driver U157, open collector drivers U167 and inverters U179. This interface can potentially be connected to 8 inch, 5.25 inch and 3.5 inch floppy drives. Floppy interfaces require a 34-pin header located at the front edge of the board.

The SCSI interface is the industry standard 5380 SCSI controller along with termination resistors U116-U118. The standard connector used by this interface is a 50-pin header.

The DMA operates in the following manner for disk requests. The DMA controller is programmed by the Slave processor to perform Memory–I/O transfers, byte wide. For example, assume a request for service comes from the floppy controller (or SCSI). The controller issues a `DRQ/` to the DMA controller. The DMA controller issues a request to the Slave for access to the Slave's bus by asserting `HLDREQ/`. If the Slave accepts the request it relinquishes its bus and asserts `BUSACK/`. This event then causes PAL U102 to issue `DMAOK/` to the RAS/CAS PAL U178. If the `PROT/` bit of the microcode is not active then this PAL issues `HLDACK/` to the DMA controller to start the memory access. The DMA controller asserts `IOWR/` or `IORD/` to the disk controller and simultaneously generates the memory address to be accessed in the DAM. Buffers U97 and U99 are used to write information to the DAM, and latches U89 and U98. Addresses for row and column are provided by multiplexers U122, U151 and U175. Once a byte has been transferred the process begins all over.

### 4.8.6 Wet Bus Interface

The WET bus interfaces exactly as the HSP board, except for the fact that the SME board has only one read address (RDWET0-RDWET5). Register U158 drives the addresses and control bits out to the WET bus when `WOE/` is asserted. U168 provides decoding for interprocessor data exchange. Registers U119, U131, and U144 provide audio input to the SME from the WET bus, and U120, U135 and U143 provide output audio to the WET bus. Data is read from a WET bus address and clocked into the input registers for reading onto the DAB on a subsequent cycle. Data is written from the DAB to the output registers and is read or driven out to another WET address in a subsequent cycle.

---

## Appendix A — Editorial Notes & Hardware Verification

> *This appendix is **not** part of the original Lexicon service manual. It documents transcription decisions and hardware verification performed during reverse-engineering, cross-referenced against schematic drawing **060-04391** ("Schematic, HSP, M480L Slave Processors," 10 sheets, Rev. 5). On that drawing: **sheet 1** carries the two slave Z80 CPUs (U4, U31) and their SRAM (U5, U32); **sheet 10** carries the connectors, bypass caps, the strobe buffer (U29), and the slave control register (U30).*

### A.1 Slave reset byte `$0D` — VERIFIED against hardware

**Manual claim (§4.3 / §4.4):** to reset Slave 0, the host writes `$0D` to `$C0015`, which strobes `SP0WR/` and latches the byte into the slave control register on the Slave/HSP PCA. Table 4.6 defines the register's active-low bit functions.

**OCR/transcription note:** the Rev-2 source rendered the byte as `$00`; it was normalized to `$0D` in this document. The origin of the `$00` (manual typo vs. OCR artifact) is unconfirmed — resolvable only by reading a clean copy of the Rev-2 page. The hardware trace below establishes `$0D` as correct regardless of which it is.

**Signal trace (drawing 060-04391, sheet 10):**

- `SP0WR/` → strobe buffer **U29 (74HCT244)**: input 1A1 (pin 2) → output 1Y1 (pin 18). A '244 is a non-latching buffer; it only cleans up / fans out the strobe.
- Buffered `SP0WR/` → **clock (pin 9)** of register **U30**.
- **U30 = 74HCT175**, a *quad* D flip-flop. The 4-bit width matches the fact that only four control bits exist (Table 4.6) — there is no 8-bit register here.
- **Clear:** U30 pin 1 (`CLR/`) ← `SR/`. Asserting `SR/` forces all Q outputs low; because the outputs are active-low, this holds every slave in reset — consistent with the manual's "powered on, Slaves cleared by `SR/`."

**Bit map (74HCT175 is non-inverting; Q follows D):**

| Written data bit | D input (pin) | Q output (pin) | Signal | Function |
|---|---|---|---|---|
| 0 | D1 (4) | Q1 (2) | `INT1/`   | INT/ lo-order slave |
| **1** | **D2 (5)** | **Q2 (7)** | **`RESET1/`** | **RESET/ lo-order slave** |
| 2 | D3 (12) | Q3 (10) | `INT2/`   | INT/ hi-order slave |
| 3 | D4 (13) | Q4 (15) | `RESET2/` | RESET/ hi-order slave |

This is an exact match to **Table 4.6**.

**Decode of `$0D = 0000 1101`:**

```
bit 3 = 1 → RESET2/ high  (hi-order slave NOT reset)
bit 2 = 1 → INT2/  high  (hi-order slave NOT interrupted)
bit 1 = 0 → RESET1/ LOW   (lo-order slave RESET)        ✓
bit 0 = 1 → INT1/  high  (lo-order slave NOT interrupted)
```

`$0D` resets the lo-order slave and disturbs nothing else. `$00` would pull all four bits low, asserting `RESET1/`, `INT1/`, `RESET2/`, `INT2/` at once — resetting *and* interrupting *both* slaves, which is not "reset Slave 0." **Conclusion: `$0D` confirmed; `$00` rejected.**

> **Note on the upper nibble:** only D1–D4 (data bits 0–3) are wired; bits 4–7 of the written byte go nowhere and are don't-care. `$0D`, `$4D`, and `$FD` behave identically. The manual writes the high nibble as `0` by convention.

### A.2 Table 4.2 (WCS Memory Map) — `4100H–41FFH` overlap: cosmetic, not hardware-verifiable

**Anomaly:** the Bank A row `4100H–41FFH NOT USED` overlaps the byte-4 window `4180H–41DFH` directly below it.

**Status:** `41FF` is what the manual prints (confirmed against the source — **not** an OCR error). The transcription reproduces it verbatim.

**Why the schematic cannot settle it:** there is no address-decode hardware that defines these byte-window boundaries.

- The bank read/write enables are produced by simple **OR gates — U8 and U21 are 74F32** (quad 2-input OR), *not* decoders. The manual's word "decoding" is loose; these chips only OR `WR/`/`RD/` with the bank-select to gate the SRAM's write/read enable. They contain no address comparison and no boundary.
- The byte-window addresses arise instead from (a) the **Slave firmware's chosen write addresses**, and (b) the **micro-sequencer driving the upper address bits (A7–A10) during DSP reads**, with A0–A6 = the program counter. Neither is a comparator with a readable threshold. The `417F`-vs-`41FF` digit is encoded nowhere in the silicon.

**Bank B parallel (for reference):** Bank B is structurally identical and clean — `6000H–617FH NOT USED` ends exactly where byte 5 (`6180H–61DFH`) begins, with no overlap. By that symmetry the Bank A row "ought" to read `4100H–417FH`, but this is *inference from symmetry*, not a documented or hardware-confirmed value.

**Functional reality:** the DSP program counter counts 0–79 (`0x00`–`0x4F`), so byte 4 is only ever accessed at `4180H–41CFH` (80 locations). The declared `41DF` rounds up by 16; the `41FF` NOT-USED bound is a loose enclosing description with no effect on where microcode is stored.

**Recommendation:** treat `4180H–41DFH` (or `4180H–41CFH` actually-accessed) as authoritative for byte 4, and the byte windows generally — which are internally self-consistent and mirrored across pages and banks — as reliable. Regard the `4100H–41FFH NOT USED` entry as a cosmetic overlap. Definitive confirmation of the gap boundary would require the Slave microcode/firmware write addresses, not the schematic.

### A.3 OCR normalization conventions applied throughout this transcription

To aid readers cross-referencing the original scan, the following consistent normalizations were applied to obvious OCR corruption, with **no invention of technical content**:

- `zao` / `ZS0` → `Z80`; `OMA` → `DMA`; `161 0` → `1610`
- `DI A` / `D/ A` → `D/A`; `AID` / `ND` / `A to D` → `A/D`
- letter `O` → digit `0` and letter `l` → digit `1` inside hex/numeric tokens (e.g. `$OD` → `$0D`)
- garbled chip designators repaired from context (e.g. `Ufl` → U11, `USO` → U50, `U1 o` → U10)

Two source values were left exactly as printed and flagged rather than "corrected": the `$0D`/`$00` reset-byte discrepancy (Appendix A.1) and the `4100H–41FFH` Table 4.2 overlap (Appendix A.2).
