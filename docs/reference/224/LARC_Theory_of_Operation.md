# LARC Theory of Operation

*From the Lexicon Model 224XL Service Manual Addendum*

Information in this section is presented in the following order:

- 1.1 Power Supply
- 1.2 CPU
- 1.3 Reset Logic
- 1.4 Address Decoding Logic
- 1.5 ADC Logic
- 1.6 UART Logic
- 1.7 RS-422 Logic
- 1.8 Litronix Display Logic
- 1.9 Tape Interface Logic
- 1.10 Buffered Bus and Sink Logic

## 1.1 Power Supply

The power supply for the LARC is a 5V switching regulator. The central item in this regulator is an MC34060 or TL494 pulse width modulation (PWM) control chip. The 34060 produces an output control whose duty cycle multiplied by the input voltage is equal to 5V. This control is then applied to a pass transistor (Q1) located between the input voltage and an output filter. The output filter is a low-pass filter with a single pole at a frequency sufficiently low to attenuate the switching frequency and harmonic components in the switched square wave.

The input section is relatively simple. The LARC may be powered from one of two sources; from the mainframe through J1, or from an alternate power source through J2. Note that whenever a plug is inserted into J2, an integral switch disconnects the mainframe power source. C30, and FB3-4 form a simple RF filter for the mainframe power source; C23 and R13 provide a bypass for RF and static between the cable shield and LARC ground; and C31-33 and FB5-8 form a two stage RF filter for the alternate power source. The CR7 bridge rectifier is provided so that either AC or DC power may be used (the mainframe power is rectified). C35-37 form a composite filter capacitor operating over a large frequency range with low ESR. F1 was chosen through extensive testing to be a 1 amp fast fuse. Note, however, that one fault condition can occur that can not be protected by this (or any other) fuse: while the LARC is being powered by the mainframe, the fuse will not blow if a short occurs in the LARC circuitry after the regulator, because the mainframe can not provide enough power to blow the fuse. This fault condition will not damage the regulator or the mainframe.

The 34060 accepts a Vcc input (pin 12) from which the chip is powered and a 5V reference (Vref, pin 14) is produced. This Vcc may be from 7 to 40 Vdc, and need not be carefully regulated. The dead time input (DT, pin 4) is used to "soft-start" the regulator; when DT is near Vref the regulator is effectively shut down, and when DT is near ground the regulator is allowed to function normally. Thus as C39 is charged from Vref through R19 and R20, the output of the power supply ramps up from 0V to the normal 5V output. The 34060 generates the switching frequency internally using the external timing components RT (pin 6 connected to R21) and CT (pin 5 connected to C40). The switching frequency is 1.1/(RT*CT), which figures out to approximately 50 kHz in the LARC. The output transistor of the 34060 is controlled by the product of comparators whose inputs are an internal ramp waveform at the switching frequency, the dead time input, and the sum of two other comparators whose inputs are pins 1 and 2, and 16 and 15. The first comparator is used to compare the regulator output voltage with the reference voltage. The second comparator (which is normally used for current limiting) is not used, and its inputs are tied off. The COMP input (pin 3) is used for compensation of the comparators. The output transistor is used common-emitter fashion to control the pass transistor.

The output section of the regulator consists of the pass transistor (a P-channel MOSFET) and output filter (a single pole LC low-pass filter). The pass transistor is turned on when its gate is pulled to ground by the output transistor of the 34060. R22 is used to quickly discharge the pass transistor's stray gate capacitance when the 34060 output transistor turns off. The output of the pass transistor is a 50 kHz square wave which swings from ground to the input voltage and whose average voltage is 5V. The output filter (which consists of CR8, FB9 and 10, L1, and composite capacitor C41 and C42) has its pole at 83 Hz and is used to block the 50 kHz (and higher harmonic) components of the square wave, yielding only the DC component at the output (the desired 5 VDC).

## 1.2 CPU

The central processing unit of the LARC is an 8749, containing the CPU, clock oscillator, RAM, UV erasable ROM, and three 8-bit I/O ports on a single chip.

The XTAL1 and XTAL2 (pins 2 and 3) are connected to a 4.608 MHz crystal, yielding a processor throughput of 307,200 instruction cycles/second. The ALE output (pin 11) is a 20% duty cycle square wave at the same frequency as instruction cycles (307.2 kHz), and is present whenever the 8749 has power. This is the first place to verify that the processor's clock is correctly functioning.

The three I/O ports are used as follows: The BUS port (pins 12-19) is used as a bidirectional data bus. It is used in two modes; in the tristate mode to transfer 8-bit data to the Litronix DL-1414 intelligent displays from the ADC0809 A/D converter, and both to and from the CDP1854 UART; and in the latched mode (through the NE594 buffer/driver) to scan the switches and headroom LEDs. Bits 0-6 of Port 2 are outputs used as the address bus bits A0-A6, and bit 7 is used as the FSK tape output. Bits 0-3 of Port 1 are used as inputs from the switch array (B0-B3), and bits 4-7 are used as outputs controlling which section/row is lit in the headroom LED array (S0-S3).

There are also several control pins on the 8749: the SS input (pin 5), which must be unconnected for correct operation; the EA input (pin 7), which must be grounded for correct operation; the INT/ input (pin 6), which the UART pulls low to signal the processor when a character is available; the T0 input (pin 1), which the processor can read to determine if there was a framing error on the last character received (this feature is not currently used by the software); the T1 input (pin 39), which the processor reads during FSK tape input; the PROG/ output (pin 25), which is normally used with a 8243 I/O port expander, but is used in the LARC to clock the address of the slider to convert into the ADC0809; and the RD, WR and PSEN (pins 8, 9, and 10) outputs, which are normally used for external memory access, but are not used in the LARC.

## 1.3 Reset Logic

Both the 8749 and the CDP1854 need to be reset after power up. A simple RC (R7 and C9) circuit is used as an input to a differential driver (U3, the uA9638) to produce the required RES and RES/ signals, which are asserted for approximately 1/4 second after power is applied. The CR5 Schottky diode is used to quickly discharge C9 when power is removed (or when power is momentarily lost). To manually reset the LARC, momentarily ground pin 3 of U3.

## 1.4 Address Decoding Logic

In order to be able to access the devices that share the data bus (the ADC0809, CDP1854, and 12 DL-1414s), an address decoder is used. Address bits A2-A5 are decoded into 16 low-active chip select lines using a CD4515 4-to-16 line decoder. Address bit A6 is used as the decoder enable so that any race conditions (which may cause glitches in the decoder outputs) are eliminated.

When addressing devices, the software in the 8749 goes through several steps to assure that the addressing is done without any glitches. When addressing devices for output (such as the CDP1854 and DL-1414s), the 8749 first places the output data on the BUS port, presents the address of the desired device on A0-A5, then pulls A6 low to address the device, and lastly pulls A6 high again to disable the device. When addressing devices for input (such as the CDP1854 and ADC0809), the 8749 first tristates the BUS port, presents the address of the desired device on A0-A5, pulls A6 low to address the device, then reads the desired input data from the BUS port, and lastly pulls A6 high again to disable the device.

A simple device address map is presented here:

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

Where: XX are don't-cares, and CC is the code for the character within a DL-1414 display chip: 00 is the right-most character, 01 is the second from the right, 10 is the second from the left, and 11 is the left-most character.

## 1.5 ADC Logic

The first item of interest concerning the ADC0809 is its power source; in order to guarantee that any switching supply noise will not affect the converter, a filter is used between the 5V supply and the ADC0809's Vcc input. The filter is an RC filter consisting of R12 and the composite capacitor C16 and C17. Since the ADC0809 is CMOS (and consequently low power), the voltage drop across R17 is minimal. Note also that all the analog inputs are decoupled for further noise immunity.

Parts of the addressing logic for the ADC0809 are slightly more complicated than the other chips on the data bus. The ADC0809's internal analog multiplexer address (the address of the slider to convert) is transferred to the ADC0809 using the 8749's PROG/ output, which is normally used with 8243 Port 2 expander chips. When the processor wishes to change the address of the slider to convert, it uses a command which places a flurry of (mostly useless) information on A0-A3. During this command, the address of the slider to convert is placed on A0-A3 400 ns before the rising edge of PROG/, and is held for 90 ns after the rising edge.

After the processor sets up the address of the next slider to convert, the processor will read the results of the last conversion and start the next conversion simultaneously by addressing the ADC0809 for input as described in section 4. Note that the ADC0809's end of conversion (EOC) output is not used since the processor's software never accesses the ADC0809 more often than the 250 microsecond conversion time.

The last item of interest concerning the ADC0809 is the circuitry associated with analog inputs IN6 and IN7, which is used to measure the 5V power supply's actual voltage. The circuit connected to IN6 is a resistor/zener diode constant voltage source (R10 and CR6). The digital code resulting from the conversion of this signal will change as the supply voltage to the ADC0809 changes, because the ratio of the supply voltage to the constant voltage will change. The circuit connected to IN7 is simply a resistive voltage divider (R9 and R11) with an adjustable output voltage. Since the voltage source to this divider is the same as the ADC0809 supply voltage, the resulting digital code from the conversion of this signal will be always a constant. If the adjustable voltage source is adjusted so that it is the same as the constant voltage source when the 5V power supply is at 5.00V, then the actual voltage of the 5V power supply is calculated using a linearization of the system equations governing these circuits.

## 1.6 UART Logic

The UART data is read and written using the addressing scheme in section 4. The UART clock inputs (RCLK and TCLK pins 17 and 40), which are 16 times the 9600 baud data rate, are derived by dividing the 307.2 kHz ALE clock by two using 1/2 of the CD4013 flip-flop. The UART is strapped to provide and recognize 8-bit characters with no parity and 2 stop bits. The UART data available (DA, pin 19) output, which signals that the UART has received a complete character, is inverted before being used to interrupt the processor.

## 1.7 RS-422 Logic

The serial data to and from the UART is converted to RS-422 compatible signals by the uA9637 (U2) differential receiver and the uA9638 (U3) differential driver. The LC filter comprised of C27, FB1 and FB2 is used to rate limit the signal rise and fall times (and thereby reduce RF noise), and the R14 termination resistor is used to eliminate signal reflections.

## 1.8 Litronix Display Logic

The Litronix DL-1414 displays act very much like a memory device that happens to display its memory's contents. Once a character has been written to the DL-1414, it will be displayed without any need for refresh from the processor. When the addressing scheme from section 4 is used to output data to the DL-1414, the data on the BUS port is the character to display (in ASCII), the A0 and A1 lines correspond to the character to display within a given display chip, and the A2-A5 lines correspond to the address of the display chip. Remember that these lines are decoded by the CD4515 into low-going enable lines, which are connected to the WR/ (pin 3) lines of the DL-1414s and used to clock the data into the displays. Remember that the characters within a chip are numbered from character 00 on the right to character 11 on the left.

## 1.9 Tape Interface Logic

As much as possible of the tape interface has been done in the software of the processor; the hardware portion of the tape interface is mostly buffers and filters the signals. The processor recognizes and generates 4800 Hz (logic 1) and 2400 Hz (logic 0) FSK data at a 600 baud rate.

The tape output circuitry is rather simple. Since the uA9637 (U2) buffer has a differential input, the R29/R30 voltage divider is used to set the transition threshold. The output is protected with clamp diodes CR3 and CR4, then AC coupled, current limited, and low-pass filtered with C6, R6, and C2.

C1 is used for RF bypass; R1, CR1, CR2, C3, and C4 provide current and voltage limiting and a low-pass filter. R2, R3, and R4 set the input biasing and transition threshold of the LM311 (U1). R5 provides positive feedback for hysteresis, and R31 is used as a pull up for CMOS output compatibility. Note that if nothing is connected to the input, or the input is a low frequency or DC, then the comparator output will oscillate at random frequencies between 2400 and 4800 Hz. This output of the comparator is divided by two using 1/2 of the CD4013 (U10) flip-flop in order to make the tape data have close to a 50% duty cycle.

## 1.10 Buffered Bus and Sink Logic

The NE594 driver circuit buffers the BUS port and provides current drive capability for the headroom LEDs. No headroom LEDs, however, will light unless the appropriate current sink (the 75492, U4) is activated also. Therefore when the processor is using the data bus to communicate with the DL-1414s, ADC0809, or the CDP1854, it keeps the sinks deactivated so that the LEDs do not light up spuriously. Upon reset of the 8749, all the bits on Port 1 and Port 2 are set to logic 1; therefore Port 1 bits 4-7 are inverted before the 75492 so the LEDs do not light up during power up. R5-R12 on the Panel board are provided for LED current limiting.

The Panel board switches are also scanned from the NE594 buffered BUS output. CR1-CR8 of the Panel board are provided so that "sneak paths" will not cause the LEDs to light if multiple buttons are pushed. R1-R4 of the Panel board provide a pulldown to ground, which is the default condition when buttons are not pushed.

Unlike many other Lexicon products, the LARC processor software does not scan its LEDs and switches simultaneously. The software first will scan the LEDs, lighting eight at a time: the data for each group is placed on the BUS port, then the appropriate bit on Port 1 is set low for several hundred microseconds, then it is set high again. After all the LEDs have been scanned, then the processor will scan all the switches, scanning four at a time: the appropriate bit on each group on the BUS port is set high, then the processor reads the B0-B3 bits from Port 1 to determine the states of the buttons in the selected column. Note that the processor scans only the switches during the Diagnostic Menu Mode; the LEDs are not scanned.

---

# 2 Troubleshooting Notes

### Touching a slider puts unit in diagnostic mode

Some LARCs were shipped with a Signetics 4515 (U11) that has proved to be unreliable. Almost any other brand of 4515 will work correctly.

### A pop is audible when changing programs or using Mute switch

The pop is caused by U7 and U8 (LF353 dual opamps) on the AOUT board. Select new U7 and U8 for low bias current.

### Unpredictable operation with LARC

There is a four-position switch on the NVS board. All switches should be in the OPEN position, but a few units were shipped with switches in the CLOSED position.

### LARC doesn't work with 1000 feet or more cable between it and mainframe

Some LARC transition boards were shipped with a 10 kilohm resistor at R4. This should be a 1 kilohm resistor. Note that this will only cause a problem with extremely long cable runs (1000 feet or more).

### Miscellaneous notes

1. Do not exchange boards between 224, 224X, and 224XL units.
2. Do not exchange Power Supply modules with new modules.
3. Known software version 8.2 bugs:
   - No B output on the Dark Hall program.
   - A and C outputs on Rich Split mute when Mid Decay control is set to infinite (--).
   - Variation 5 of Dark Hall can cause reverb runaway.

### Diagnostics

Starting with software version 8.2, the ROM checksum diagnostics have been improved. All the serial communications code is in the first SBC ROM, as is the checksum diagnostics program. Thus if the first SBC ROM is functioning, errors on the other ROMs will be reported.

Each ROM has been given a checksum which is identical to its ROM number. Thus SBC ROM 1 has a checksum of 1, as does NVS ROM 1.

If a checksum error is detected, the data is displayed as follows:

- `E01` is an error in SBC ROM 1.
- `E02` is an error in SBC ROM 2 (the ROM in the third socket)
- `E03` is an error in SBC ROM 3
- `H01` is an error in NVS ROM 1
- `H02` is an error in NVS ROM 2

...and so forth.

If there is more than one error, the errors are displayed sequentially by pressing button 1 after each error is displayed.

If a checksum error occurs, the bottom display on the LARC contains some useful information. "C=" gives the actual checksum read from the ROM, and "B=" gives the expected checksum. "Address" gives the last address tested, plus one. Thus if SBC ROM 3 is inadvertently installed in the socket for SBC ROM 2, the error E02, C=03, B=02, Address 1000 will be displayed. This is conclusive evidence that the two higher SBC ROMs are reversed.

If C is equal to 0, FF, or some random 2-digit number, the indicated ROM has probably been damaged, and should be replaced.
