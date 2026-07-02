# Lexicon Model 224X — Service Manual

**Digital Reverb/Effects Processor**

© Copyright 1984, Lexicon. All rights reserved.

---

## Preface

This service manual for the Lexicon 224X Digital Reverberator has eight sections.

- **Section 1, Introduction** — contains a general description of the 224X and lists the specifications.
- **Section 2, Service/Warranty** — gives instructions for periodic maintenance and describes how to return units for service and order parts. In addition, it contains the limited warranty.
- **Section 3, Theory of Operation** — includes a system overview and describes how each module in the 224X works and how the modules interact with one another.
- **Section 4, Performance Tests and Calibration** — lists the equipment required for performance tests and calibration, and describes how to conduct these procedures.
- **Section 5, Troubleshooting** — contains troubleshooting procedures, including a discussion of the power supplies and the diagnostic programs.
- **Section 6, Schematics and Assembly Drawings** — contains all 224X schematic and assembly drawings.
- **Section 7, Parts List** — lists the part number, quantity, description, and reference for all parts.
- **Section 8, Engineering Changes** — describes modifications to the 224X and provides instructions on how to make the modifications.

---

## Table of Contents

- **1 Introduction**
  - 1.1 Description
  - 1.2 Specifications
- **2 Service/Warranty**
  - 2.1 Periodic Maintenance
  - 2.2 Returning Units for Service
  - 2.3 Module Exchange Program
  - 2.4 Ordering Parts
  - 2.5 Limited Warranty
- **3 Theory of Operation**
  - 3.1 System Overview
  - 3.2 Control Head and Transition Module
  - 3.3 Single-Board Computer (SBC) Module
  - 3.4 Nonvolatile Storage (NVS) Module
  - 3.5 Timing and Control (T&C) Module
  - 3.6 Data Memory (DMEM) Module
  - 3.7 Arithmetic Unit (ARU) Module
  - 3.8 Floating Point Converter (FPC) Module
  - 3.9 Audio Input (AIN) Module
  - 3.10 Audio Output (AOUT) Module
  - 3.11 Power Supplies
- **4 Performance Tests and Calibration**
  - 4.1 Test Equipment Required
  - 4.2 System Tests
  - 4.3 Power Supplies
  - 4.4 Analog Tests
  - 4.5 Calibration
- **5 Troubleshooting**
  - 5.1 Overall Approach
  - 5.2 Power Supplies
  - 5.3 Power-up Diagnostics
  - 5.4 Maximum Delay (0.5-sec) Program
  - 5.5 Zero Delay Program
  - 5.6 Self-Test Mode
  - 5.7 Signature Analysis
- **6 Schematics and Assembly Drawings**

---

# 1 Introduction

## 1.1 Description

This service manual contains specifications, service and warranty information, theory of operation, performance tests and calibration procedures, a troubleshooting guide, schematics and assembly drawings, a parts list, and engineering changes for the 224X Reverberation/Effects Processor. This manual can be used as a reference for standard servicing procedures.

> **IMPORTANT:** As a result of improvements and updates to the 224X, the unit being serviced may differ slightly from the descriptions and specifications in this manual. Service operations must be performed in the order described by a competent service technician only. If you have doubts about performing a procedure, please contact your Lexicon dealer or Lexicon for assistance. Lexicon is not responsible for damage resulting from incorrectly followed service procedures. Lexicon has taken considerable care in determining the accuracy of the information in this manual; however, it is not responsible for consequential damage resulting from the implementation of the procedures described.

> **WARNING:** Hazardous voltages exist inside this unit when the power cord is connected; use extreme caution when servicing or adjusting. Service must be performed by qualified service personnel. Always place the unit on an isolation transformer before servicing.

### Precautions

Many of the internal components of this unit are extremely sensitive to static electricity. To ensure that static charges are dissipated safely, do not hand a component or board directly to another person — place the device on a nonconductive surface and then have it picked up. The following practices minimize possible damage to ICs that can result from electrostatic discharge:

1. Minimize handling of integrated circuits (ICs).
2. Keep parts in original containers until ready for use.
3. Discharge personal static before handling devices.
4. Handle each IC by its body.
5. Use antistatic containers for handling and transport.
6. Do not slide devices over a surface.
7. Avoid plastic, vinyl, or styrofoam in the work area.
8. When removing plug-in boards, handle only by nonconductive surfaces and **never** touch open-edge connectors except at a static-free work station. Placing shorting strips on edge connectors usually provides complete protection to installed ICs.
9. Handle ICs only at a static-free work station.
10. Use only grounded-tip soldering irons.

**Always disconnect the power cord before servicing internal components.**

## 1.2 Specifications

| Parameter | Specification |
|---|---|
| Program Capacity | Varies depending on software version. |
| Storage Capacity | 36 registers (nonvolatile). |
| Reverberation Time | Adjustable in two bands from approximately 0.6 to 70 seconds (program-dependent). |
| Mainframe Controls | Power on switch with LED; system reset; Left and Right input level adjustments; A, B, C, and D output level adjustments. |
| Frequency Response | 20 Hz to 15 kHz, ±1.5 dB; 20 Hz to 12 kHz, ±0.5 dB. |
| Dynamic Range* — Reverberant mode | 84 dB typical, 81 dB minimum at Reference Level, 20 Hz to 20 kHz for all reverb times from 0 to 10 seconds. |
| Dynamic Range* — Nonreverberant mode | 90 dB typical, 86 dB minimum, 20 Hz to 20 kHz noise bandwidth. |
| Total Harmonic Distortion (THD) and Noise* | 0.04% typical, 0.07% maximum at Reference Level for all reverberation times between 0 and 35 seconds. |
| Interchannel Crosstalk | −55 dB at 1 kHz. |
| Inputs | Two, balanced and transformer-isolated; impedance: 20 kilohm; maximum level adjustable: +8 to 18 dBm. |
| Outputs | Four, balanced and transformer-isolated; impedance: 90 ohm; maximum level adjustable: +8 to +18 dBm; power-on muting. |
| Control Head Cable | 15 ft standard; optional 25-ft and 50-ft cables available. |
| Power | Nominal: 100, 120, 220, 240 Vac (−10%, +5%) switch-selectable; 50 to 60 Hz; 150 W. |
| RFI Shielding | AC power connector, audio connectors, and console cable are RFI-shielded. Complies with FCC limits for Class A computing device. |
| Protection | Mains and secondaries fused; voltage crowbar and/or current limiting, thermal protection. |

### Connectors

| Location | Connectors |
|---|---|
| Mainframe | Power: standard IEC 3 pin; Audio: XLR-3; Control Head: DB-25; Optional Automation Interface: DB-25. |
| Control Head | Mainframe Cable: DB-25. |

### Physical and Environmental

| Parameter | Specification |
|---|---|
| Serviceability | Field-serviceable, each major assembly removable. |
| Diagnostic Programs | Control and display via remote controller. |
| Cooling | Convection-cooled power supply, forced-air cooling of logic boards. |
| Environment | Operating: 0 to 35 °C (32 to 95 °F); Storage: −30 to 75 °C (−22 to 167 °F); Relative humidity: 95% maximum (without condensation). |
| Size — Mainframe | Standard 19-in. rack mount: 19"w × 7"h × 15"d (483 × 178 × 381 mm). |
| Size — Control Head | 5.4"w × 8.8"h × 3"d (137.2 × 223.5 × 76.2 mm). |
| Weight — Mainframe | 34 lb (15.5 kg); 48 lb (22 kg) shipping. |
| Weight — Control Head | 2.5 lb (1.2 kg); 6 lb (2.7 kg) shipping. |
| Automation Interface | Optional RS-232C serial interface. |

*Specifications subject to change without notice.*

> \* The Reference Level is set using the zero delay-line diagnostic test program with input level adjustment set just below the level at which the +12 dB LED lights with a 1-kHz tone at the input and with output sensitivity set to produce +12 dBm with a 600-ohm load. For reverberant mode, measurements are made using the Concert Hall program with the Mode Enhancement toggle off; for nonreverberant mode, measurements are made using the zero delay-line diagnostic test program.

---

# 2 Service/Warranty

## 2.1 Periodic Maintenance

Under normal conditions, the 224X requires minimal maintenance. At six-month intervals, clean or replace the air filters on the right side and front panel of the mainframe. Filter elements can be cleaned using a mild detergent and warm water, and new filters can be obtained from Lexicon (front-panel filter: Lexicon no. 720-03386; side-panel filter: Lexicon no. 720-01261).

Use a soft lint-free cloth lightly dampened with a mild detergent and warm water to clean the exterior surfaces of the 224X. During servicing, use a vacuum or blower to clean dust out of the interior of the 224X.

## 2.2 Returning Units for Service

If the 224X must be returned to Lexicon or a designated facility for service, Lexicon assumes no responsibility for the unit in shipment from customer to factory, whether in or out of warranty. All shipments must be well packed (using the original packing materials, if possible), properly insured, and consigned to a reliable agent, such as UPS or Federal Air Express. If original packing materials are not available, please procure a new packing kit from Lexicon.

**Before returning a unit, always consult with Lexicon to determine the extent of the problem and to decide on a shipping procedure.**

When returning a unit for service, include the following information:

- Name
- Company name
- Address
- City, State, ZIP
- Telephone number (include area code)
- Serial number of unit
- Description of problem
- Desired return date
- Preferred method of return shipment

Please include a note describing conversations with Lexicon personnel, and give the name and telephone number of the person directly responsible for maintaining the equipment. Do NOT include accessories, such as power cords, manuals, or remote switches.

## 2.3 Module Exchange Program

If a defective module is clearly identified, Lexicon can usually provide a repair/exchange module within 24 hours in advance of receipt of the defective module. If a fast turnaround is required, Lexicon can ship a module by Federal Air Express or other expedited air service, resulting in 24-hour delivery if the customer is near a major airport. For this service, the customer is expected to pay shipping charges.

> **IMPORTANT:** When shipping a module for repair or exchange, always call Lexicon before packaging it for shipment; Lexicon ships modules in reusable static protective bags with appropriate packing materials — use these materials or procure new materials from Lexicon. Lexicon is not liable for damage resulting from unauthorized shipping procedures.

## 2.4 Ordering Parts

Replacement parts can be ordered from:

```
Lexicon, Inc.
60 Turner Street
Waltham, MA 02154 USA
(617) 891-6790
Telex 923 468
Attn: Customer Service
```

## 2.5 Limited Warranty

Lexicon warrants each 224X to be free from defects in material and workmanship under normal use and service for one year. This warranty begins on the date of delivery to the purchaser or his authorized agent or carrier. During the warranty period, Lexicon will repair, or at its option replace, at no charge, components that prove to be defective, provided that the equipment is returned, shipping prepaid, to Lexicon's factory or designated service facility.

The warranty is null and void under the following conditions:

1. Abuse, neglect, alteration, or repair by unauthorized personnel.
2. Damage caused by improper use or operation from an incorrect power source.
3. Damage caused by accident, act of God, war, or civil insurrection.

Lexicon is not responsible for loss or damage, direct or consequential, resulting from machine failure or the inability of the product to perform. Lexicon is not responsible for damage or loss during shipment to or from its factory or designated service facility.

Lexicon reserves the right to make changes or improvements in the design or construction of the machine without obligation to make such changes or improvements in the purchaser's machine.

No equipment may be returned under this warranty without prior authorization from Lexicon. Shipments must be packed in authorized Lexicon packing material, fully insured, and prepaid.

This warranty is in lieu of all other warranties, expressed or implied, and of any other liabilities on Lexicon's part; in addition, Lexicon does not assume or authorize anyone to make any warranty or assume any liability not strictly in accordance with the above.

---

# 3 Theory of Operation

## 3.1 System Overview

As shown in Fig. 3.1, the 224X is divided into 11 major functional modules:

1. Control Head
2. Transition
3. Single-Board Computer (SBC)
4. Nonvolatile Storage (NVS)
5. Timing and Control (T&C)
6. Data Memory (DMEM)
7. Arithmetic Unit (ARU)
8. Floating Point Converter (FPC)
9. Audio Input (AIN)
10. Audio Output (AOUT)
11. Power Supplies (PS1, PS2, and PS3)

Except for the control head, Transition module, and power supplies, all modules plug into an 8-slot card cage and are interconnected via a motherboard. The card cage and the power supply are contained in a mainframe. The control head is connected to the mainframe by a 25-conductor cable. The Timing and Control (T&C), Data Memory (DMEM), and Arithmetic Unit (ARU) modules comprise a dedicated, 293-ns-cycle, microprogrammed digital signal processor (DSP).

During normal operation, signal flow begins with the two audio input channels. The Audio Input (AIN) module filters, samples, and digitizes analog audio signals into 14-bit floating point representations (12-bit mantissa, 2-bit exponent). These floating point representations are then converted into 16-bit fixed-point two's complement numbers by the Floating Point Converter (FPC) module. The DSP processes this information and generates up to four independent channels of output data. This processed data is passed back to the FPC module, which reconverts it into floating point form. To generate the audio output, the Audio Output (AOUT) module reconstitutes four analog signals from the digital data stream.

The Single Board Computer (SBC) module is a controller that interfaces the control head to the DSP. The microprocessor (an 8080) on the SBC module scans the switches and pots on the control head and drives the control head displays. It processes the information received from the control head and changes the program running in the DSP. In addition, the SBC module performs various housekeeping tasks, such as power-up diagnostics and storing and retrieving nonvolatile user setups from the Nonvolatile Storage (NVS) module.

> **Figure 3.1.** Detailed Block Diagram — 224X. *(See original manual for the full block diagram.)*

## 3.2 Control Head and Transition Module

The control head contains the switches and slide pots that allow a user to modify the control parameters of the reverberation and effects programs and control program access. In addition, the control head displays program and input signal level information.

The control head consists of two board assemblies connected by a 27-pin flexible cable. The display and pushbutton board has three diodes, eight current-limiting resistors, switches, and LED displays. The second board contains all the remaining electronics, including the slidepots, and a 25-pin I/O connector. The I/O connector has 14 signal wires and two power wires. The rest of the 25 lines are used for digital and chassis ground returns. Ground returns are inserted between signal lines to prevent signal interference. The 14 signal wires connecting the control head to the mainframe consist of three groups of signals from three I/O ports on the SBC module: eight lines from port A form a bidirectional data bus; four lines from port B form a 4-bit address; two lines from port C serve as control signals. Table 3.1 lists the cable and connector wiring runs and tie points between the control head and the SBC module.

### Table 3.1. Control Head to Mainframe Wiring

| 25-pin Connector (Control Head to Mainframe) | 50-pin Connector (Transition to SBC Module) | Function Name |
|---|---|---|
| 1 | 2 | GND |
| 2 | 1 | PB3 |
| 3 | 3 | PB2 |
| 4 | 5 | PB1 |
| 5 | 7 | PB0 |
| 6 | 4, 6, 8 | GND |
| 7 | * | GND (Chassis) |
| 8 | 20 | GND |
| 9 | 21, 29 | PC1 |
| 10 | 30 | GND |
| 11 | 25 | PC0 |
| 12 | 26 | GND |
| 13 | 33 | PA7 |
| 14 | 35 | PA6 |
| 15 | 37 | PA5 |
| 16 | 39 | PA4 |
| 17 | 47 | PA3 |
| 18 | 45 | PA2 |
| 19 | 41 | PA1 |
| 20 | 43 | PA0 |
| 21 | 34, 36, 38, 40, 42, 44, 46, 48 | GND |
| 22 | ** | AC1 |
| 23 | ** | AC1 |
| 24 | ** | AC2 |
| 25 | ** | AC2 |

> \* Connected to chassis, not to SBC module.
> \*\* Connected to 10-Vac secondary, not to SBC module.

The control head interfaces with the SBC module through a 25-pin cable, with a transition at the mainframe to a 50-pin cable: this cable, in turn, connects to the J1 edge connector on the SBC module. The transition from 25 to 50 conductors is made through the Transition module, which is also used as an input point for the AC power to the control head, or 10-Vac power supply generated from a separate secondary of the power transformer. The 10-Vac power supply is fused to protect against cable shorts or similar faulty conditions.

**Power Supply.** The power supply for the control head consists of a full-wave bridge with filter and a 5-V 7805 regulator. The unregulated dc supply directly powers the LED displays.

Rectification at the control head allows power transmission to the control head without IR voltage drop in the ground returns, because a voltage drop in the ground returns would degrade noise margins and increase noise spikes in the logic signals.

**Display Section.** The display section is based on a scanned display concept in which all digits share a common segment drive. All digits use a common anode, and current flows through digit segments only if the cathode for that digit is grounded. The display and data transfer sections of the control head use as few interconnection wires as possible. The segment data comes out on port A; the 4-bit address selecting the digit comes out on port B; the control signals come out on port C.

The display cycle is controlled by software. At the end of a cycle, the eight lines of port A are used to send pot or switch data back to the SBC module. Addresses for the switches and pots are the same as for the respective digit just used during a display cycle. Table 3.2 lists the various display and read-back device addresses. The command sequences used are as follows:

```
ACTION
  Load Digit, Port B
  Load Segments, Port A
  Set PC2/ (ACK/)
  Set PC0 (STCONV)
  Clear PC0
  .
  Delay Approximately 500 us
  .
  Clear PC2/
  Set PC1/ (Read Enable)
  .
  Delay 12 us
  Read Data
  Clear PC1/
  .
  Select Next Digit
  Repeat Sequence
```

### Table 3.2. Control Head Displays, Pots, and Pushbuttons

Port B 4-bit addresses select digits 0–8. For each address, Port A bits (PA0–PA7) carry write (segment/LED) and read (data) functions.

| Port B Addr | 0 (0000) | 1 (0001) | 2 (0010) | 3 (0011) | 4 (0100) | 5 (0101) | 6 (0110) | 7 (0111) | 8 (1000) |
|---|---|---|---|---|---|---|---|---|---|
| Function | Digit 0 / Bass-Pot | Digit 1 / Mid | Digit 2 / Crossover | LEDs / Treble Decay | LEDs / Depth | LEDs / Pre-Delay | LEDs / Pushbutton | LEDs / Pushbutton | — / Pushbutton |
| PA0 | SEG a / LSB | SEG a / LSB | SEG a / LSB | PROG 1 / LSB | IMED / LSB | SEC / LSB | L 0dB / PROG 1 | R 0dB / IMED | — / BASS |
| PA1 | SEG b | SEG b | SEG b | PROG 2 | SET | MS | L 6dB / PROG 2 | R 6dB / SET | — / MID |
| PA2 | SEG c | SEG c | SEG c | PROG 3 | CALL | Hz | L 12dB / PROG 3 | R 12dB / CALL | — / CROSSOVER |
| PA3 | SEG d | SEG d | SEG d | PROG 4 | SHIFT | kHz | L 18dB / PROG 4 | R 18dB / SHIFT | — / TREBLE |
| PA4 | SEG e | SEG e | SEG e | PROG 5 | REG A | OVFL | L 24dB / PROG 5 | R 24dB / REG A | — / DEPTH |
| PA5 | SEG f | SEG f | SEG f | PROG 6 | REG B | — | BASS-POT / PROG 6 | TREBLE DECAY / REG B | — / PRE-DELAY |
| PA6 | SEG g | SEG g | SEG g | PROG 7 | REG C | — | MID POT / PROG 7 | DEPTH / REG C | — / — |
| PA7 | DP / MSB | DP / MSB | DP / MSB | PROG 8 / MSB | REG D / MSB | — / MSB | CROSSOVER / PROG 8 | PRE-DELAY / REG D | — / — |

A 74LS42 4-to-10 line decoder, controlling 75376 high-current drivers, selects digits. The LEDs are arranged into eight digits: 0, 1, and 2 correspond to the three 7-segment displays, and 3 to 9 are groupings of the various discrete LEDs on the panel. Refer to the schematics for details. 75327 driver arrays, current-limited with 150-ohm resistors, provide segment drive. The RDENB/ signal disables segment drive when pot or switch data is to be transmitted over the eight data lines.

Each time a display cycle is begun, a one-shot U2 fires to start the 75326 drivers for a period of several microseconds. If the SBC module becomes hung up in an unresolved operation, the one-shot times out, turning off all displays to prevent sustained high current (50 mA) from being drawn to any LED. The LEDs can run at high currents for only brief periods.

**Slidepot Digitization.** The control head uses an ADC-0817, which is a complete A/D subsystem capable of scanning up to 16 inputs and converting each input amplitude to an 8-bit binary code representation. A clock source, a start conversion pulse, and addresses are the only inputs. The ADC-0817 is used in a ratiometric configuration — that is, the pot terminals and chip +REF (pin 19) are tied to 5 V, and the low terminals and ground (0 V) are tied to −REF (pin 23). The pots represent the complete range from −REF to +REF as a linear function of the position of the slidepots. The ADC translates this to 0000 0000 – 1111 1111 codes.

The start conversion pulse (STCONV) is filtered for noise rejection and routed to the start-convert and address-latch inputs of the ADC. The ADC synchronizes this command to its free-running input clock and begins a conversion cycle. Within 64 clock cycles, or 128 us, assuming a 500-kHz clock, the ADC-0817 completes the conversion and outputs the result at tristate outputs. An internal analog multiplexer selects the desired pot.

The clock to the ADC-0817 A/D converter is generated by a CMOS/RC free-running square-wave oscillator running at a nominal 500 kHz ±150 kHz (±30%). The actual conversion time ranges from 70 to 130 us. When RDENB/ is LOW and the digit address is 0 through 5, data from the ADC-0817 outputs is gated onto the PA0–7 data bus. A tristate LS244 is used for this function.

**Switch Data.** The switches are all normally open pushbuttons arranged in three banks corresponding to digits 6 to 8. Germanium diodes 1N283 are used to isolate each bank or column of switches if more than one pushbutton is pressed at the same time.

The banks are wired into rows assigned to data lines PA0–7. Pull-up resistors ensure proper threshold for the tristate buffers. A complete bank or column of switches can be read when RDENB/ is LOW and the bank's digit line is selected. Any pushbutton pressed corresponds to data out onto the bus as a TTL logic "0". Refer to the schematics or Table 3.2 for details of pushbutton and pot assignments.

## 3.3 Single-Board Computer (SBC) Module

The SBC module is a National Semiconductor BLC-11 (or equivalent) using an 8080 microprocessor. It also includes 1K bytes of RAM at hexadecimal addresses 3C00 to 3FFF and supports four 5-V 2716 ROMs to provide a total of 8K bytes of ROM at hexadecimal addresses 0 to 1FFF.

The SBC module controls all functions of the control head, such as reading switches and slide pots, as well as data display. Its ROMs also contain the reverberation and effects software, which controls the DSP. The multibus provides the pathway for interaction between the SBC and the DSP. The software can be updated and expanded simply by replacing ROMs. The SBC module has three parallel ports and one serial port. The serial port is normally not used, but it has been configured as an RS-232 data set at 4800 baud (settable from 110 to 9600 baud).

Parallel port A is a bidirectional port and is used in mode 2. Parallel port B is used in mode 0 and provides four output bits used as an address to the control head. Parallel port C provides both control bits for port A and the control head.

## 3.4 Nonvolatile Storage (NVS) Module

The NVS module (sometimes referred to as the memory expansion module) provides nonvolatile memory consisting of (1) battery-backed-up RAM for the 36 user storage registers that hold customized reverberation and effects program variations, and (2) ROM storage expansion for the reverberation and effects software. The NVS module is contained on a single multibus-compatible board that plugs into the OPTION slot on the 224X card cage.

A NiCad battery backup powers the RAM of the NVS module to preserve the memory contents after power has been shut off. The RAM consists of four 1K × 4-bit RAMs (U5, U6, U12, U13) for a total of 2K bytes. It resides in memory address from hexadecimal 2000 to 27FF. The battery backup can protect the memory contents for as long as three months without recharging. All control head settings and register stores can be saved. The batteries are maintained at full charge by a trickle charger that operates when the 224X is turned on. The charger consists of a 78L05 that regulates the +12-V supply down to +5 V plus a diode drop. This voltage powers the battery supply Vbb via CR1 when power is on. The battery is charged via R16, a 270-ohm resistor. The batteries are fully charged after power has been on for 20 hours. An on-board detection circuit monitors the ac mains power and places the memory in protected store mode when a power outage is detected.

The 10-Vac power supply is conditioned to a TTL-compatible level to trigger the one-shot U21. Under normal power-up, the one-shots are continuously triggered, thus disabling the power-fail signal PFAIL. When a power failure occurs, the one-shot is not triggered and PFAIL will be activated. When PFAIL is activated, the write signals to the nonvolatile RAMs are disabled, preventing any accidental erasure to the contents. Part of the power fail circuitry is powered from the battery voltage Vbb to prevent any unpredictable behavior at power fail.

The ROM section of the NVS module has sockets for eight 2732-type 4K × 8 ROMs for storage of reverberation and effects software. The ROM resides in memory address from hexadecimal 8000 to FFFE. Memory location FFFF is mapped to a 4-position dip switch. (Thus the last byte in the last ROM cannot be read by the microprocessor.)

The dip switch may be preset to one of 16 code combinations, corresponding to 15 registers. The software reads the switch setting upon power-up to determine which register, if any, has been selected. By changing the switch settings, the 224X can power up with a predetermined program setup.

## 3.5 Timing and Control (T&C) Module

The T&C module contains the clock and state generation circuitry, 512 bytes of microprogram memory, an interface between the SBC module and the microprogram memory, and microinstruction decode and control signal generation logic.

The clock generation circuitry on the T&C module is synchronized to the SBC module by a phase lock loop. 02/ is the clock signal generated by the SBC module, running at 2.048 MHz. An MC4044, U27, forms the phase comparator and the low pass filter. The voltage controlled oscillator is formed by an LC tank oscillator, with a varactor, CR1, for voltage control. A divide-by-15 counter, U41, is embedded in the phase lock loop, making it a frequency multiplier of 15. Thus the master clock, MC, runs at 30.72 MHz. Since the LC tank oscillator output is divided by 2 by a J-K flip-flop, U26, to become MC, the oscillator actually runs at 61.44 MHz. This clock can be observed at TP2 (OSC). MC is driven from a Schottky nand gate, U40, with an active pull-up, Q3.

The state generation circuitry consists of a divide-by-9 counter, U56, and an 8-bit shift register U39. Thus the system clock period is at 3.41 MHz, i.e., 293 ns, which is divided into nine time slots, MS0–MS8. These nine time slots are grouped into three, AS0, AS1, and AS2 by U38, U25, and U23. Refer to Fig. 3.2 for the basic timing of the T&C module.

The control signal generation is achieved through a writable control store (WCS), formed by four 128 × 8 static RAMs (U2, U15, U29, U43). The WCS is cycled by an eight bit program counter (U1, U14). A 100-step control program is allowed, giving a sampling rate of 34.13 kHz. Thus the counter is normally reset at count 99 by a RESET signal that is generated by the WCS itself. The WCS program is loaded from the SBC module. Thus the address from the counter is multiplexed with the address from the SBC module. The bidirectional data bus to the WCS is buffered by bidirectional drivers, U3, U16, U30, U44, to the SBC module.

> **Figure 3.2.** T&C Module Timing. Microinstruction cycle = 292.97 ns, divided into MS0–MS8 (32.55 ns each), grouped into AS0, AS1, AS2. Notes: ARU operates on a clock that can lag MC by < 19 ns. AS1 is shorter than either AS0 or AS2 to avoid MS4 clearing AS0 prematurely.

The least significant 16 bits of the WCS word are normally used as an address for the data memory. The remaining 16 bits contain the multiplier coefficient, the register file addresses, and miscellaneous control signals. They are clocked by a 32-bit microinstruction register, U4, U5, U17, U18, U31, U45. The upper 16 bits of the microinstruction register are formed by 74S163 counters for the synchronous clear functions that they provide. The upper 16 bits of the microinstruction register are cleared whenever the cycle is used by the SBC module in accessing the WCS, since the data on the microinstruction bus, MI0–MI31, may not be valid. The microinstruction word is set up such that all zeros correspond to a no-operation. The lower 16 bits of the microinstruction word can be "don't cares," since they represent only an address.

The remaining control signal generation circuitry consists of decoders (U47, U48, U49, U32, U34), which generate the control signals that are encoded in the instruction word; register U19, U20, which further pipelines and synchronizes the required control signals; and flip-flops U24, U22, U21, U20, which generate more complicated control signals from the basic timings MS0–MS8. The multiplier coefficient from the microinstruction word, C0/ to C5/, is serialized into an even and an odd stream, M0/ and M1/, by shift registers U10 and U11 for the serial multiplier in the ARU module.

The access to the WCS from the SBC module is decoded by U50 and synchronized by U52 and U53. Since the multibus is an asynchronous bus, an acknowledge signal to the SBC module, XACK/, is generated by U54. The WCS can be accessed from the SBC module in two modes. First, the DSP can be halted by stopping the program counter (U1, U14) by asserting HALT/. In this mode, the SBC module can read from and write to the WCS anytime. The WCS is mapped into hexadecimal address locations 4000 – 41FF of the SBC module address space. The decoder U46 decodes the least significant two bits of the address from the SBC module to select one out of the four 128 × 8 bit static RAMs and the corresponding bidirectional drivers. Alternatively, the SBC module can also access the WCS while the DSP is running, allowing it to change program characteristics on the fly. In this mode, a protect bit in the microinstruction determines when the SBC module can access the WCS. The program must be organized such that the microinstruction, which is displaced during an SBC access, is a no-operation. Normally, the SBC module only writes into the WCS in this mode, which only takes up one microinstruction time. Reading from the WCS in this mode can take up to three microinstruction times. In this mode, a flip-flop, half of U53, is used to attempt to synchronize pairs of SBC module accesses in the same sample time: an allowed access slot not utilized will disable the next access slot.

Finally, there is some diagnostic hardware included in the T&C module. Three groups of eight timing control signals can be read by the SBC module via tristate bus drivers, U6, or registers U7 and U8. The DSP is halted when these diagnostic ports are being read. In the registers U7 and U8, the signals being read are dynamic and thus need to be sampled by appropriate clocks. Note that the digital overload signal SAT is also read through one of these diagnostic ports, U8. This allows the SBC module to detect when digital overflow has occurred in the ARU module. The SAT signal is first clocked through a flip-flop. Then it triggers a one-shot since the SAT signal can be transient. When the overflow is continuous, the one-shot is not triggered. Thus the SAT signal is OR-ed with the output of the one-shot, which is then read by the SBC module. U9 forms a shift register to perform a serial-to-parallel conversion of the four serial bit streams S0, S1, M0/, M1/ to be observed. Exclusive or gates U12 minimize the hardware needed to observe the bit streams. ARUCK fires one-shot U13, the output of which drives an LED on the edge of the board. This gives a preliminary indication of whether the clock is running. Another test point TP1 is available for test synchronization purposes.

## 3.6 Data Memory (DMEM) Module

The DMEM module contains the data memory, control signal and address generation circuitry, the XREG (DMEM transfer register), diagnostic ports, and the 8080 port-decoding circuitry. The DMEM communicates with the rest of the system over the digitized audio bus (DAB).

The address to the data memory coming from the microinstruction is in the form of an offset relative to a current position in memory. This current position is held by a 16-bit current position counter (U51 and U65) and is normally incremented once every sampling interval. The absolute address of a memory reference is computed by subtracting the offset from the current position. A 2's complement subtraction is performed by adding the complemented 16-bit word, OFST/, to the output of the current position counter and tying the carry input of the adder (U49, U50, U63, and U64) high. A multiplexer (U18 and U36) is used to multiplex the resulting address onto the eight address lines of the 64k dynamic RAMs. The circuitry is set up such that either one bank of 64k dynamic RAMs or two banks of 16k dynamic RAMs can be used. The address and control lines of all the RAMs are tied together. Because the RAM outputs are capable of fanning out to ten low-power Schottky TTL loads, they are tied directly to the DAB without buffering.

The timing and control signals for the DMEM modules are generated by a delay-line circuit (U59) based on signals supplied by the T&C module MEMAC, DABSTB, and MEMR. Refer to Figure 3.3 for the data memory timing.

In addition to the data memory circuitry, the DMEM module also contains some decoders (U55, U56, U57) which are used to generate the strobes used in the I/O access of the ports used in various modules in the DSP from the SBC module. The open collector-gate U52 is used to return an acknowledge, XACK/, to the SBC module after an I/O access. The NAND gates U53 and U54 are used to implement the single cycle/halt/run control modes of the DSP.

The module can single cycle, halt, or let continue run the DSP through accessing these latches via the I/O ports.

Some diagnostic circuitry is also included on the DMEM module. The tristate bus drivers U48 and U62 are used to enable the SBC module to read the OFST/ lines when they are static. U42 forms the bus test register, which enables the SBC module to sample and read its own data bus DATA/ on the DMEM module. U38, U39, U40, and U41 form the X register, which enables the SBC module to read from and write to the DAB. U38 and U40 are used to send data from the DAB to the SBC module and U39 and U41 are used to send data from the SBC module to the DAB.

> **Figure 3.3.** DMEM Timing. Notes: CAS/ falls only when MEMAC is high, indicating memory operation. Critical timing path for DIN is XFER CK to result register of ARU.

## 3.7 Arithmetic Unit (ARU) Module

The ARU consists of a 4 × 16-bit register file, a 16 × 6-bit 2's complement multiplier with saturation logic, a 20-bit accumulator, and a 16-bit result register. The 4 × 16-bit register file acts as a temporary store for the multiplicands taken from the DAB. The source of the multiplicand can thus be from the FPC module, DMEM module, the SBC module via the X registers on the DMEM module or even from the result register. The multiplier performs a 16 × 6-bit multiply and accumulate every system clock time (i.e., 293 ns). The 6-bit multiplier coefficient and the control signals to the multiplier are generated from the T&C module. The result register acts as a buffer between the outputs of the multiplier and the DAB, allowing the multiplier to perform the next multiplication without having to wait for its previous result to be read by the other parties on the DAB. In a similar manner, other parts on the ARU are pipelined to maximize the operating speed of the essentially serial multiplier through the register file, the partial product register, and the accumulator.

The 4 × 16-bit register file (U29, U30, U31, U32) has independent write addresses (WA0, WA1) and read addresses (RA0, RA1), which are controlled by the microinstruction. In this way, data on the DAB can be written into the register file at one address while data at another address can be read by the multiplier. Note that the write signal to the register, DAB WSTB/, is active every system clock time (293 ns) although the data on the DAB is not always relevant. Address 3 in the register file is used as a pass-through location in these instances.

The multiplier is implemented by a modified shift and add serial multiply technique. Instead of the normal shift and add, two shifts and adds are performed at the same time such that the multiply is twice as fast. A system cycle time (293 ns) is divided into three ARU states: AS0, AS1, and AS2. During each of these states, a double shift and add is performed. This gives a 6-bit multiply in a system cycle time. The double shift is performed by a "dual rank" shift register (one which shifts by two bits at a time) (U3, U4, U15, U16, U17, and U18). The double shift is performed by interleaving the bits to two sets of the shift register: U4, U18, and U15 form one shift register that receives the even-numbered bits, and U3, U17, and U16 form another register that receives the odd-numbered bits. In the first ARU state, AS0, the contents of the register file are simply loaded into the shift register. The output of the shift register is split into two groups: one is the direct output and the other the output shifted right by one bit. Depending on the 6-bit multiplier coefficient from the microinstruction, which is serialized into bit streams M0/ and M1/ in the T&C module, these two are blanked or added to the other (by the nand gates U14, U26, U27, U28, U40, U41, U50, U51, U52, and U53). The result is loaded into the partial product register (U10, U11, U12). Note that the adder forming the partial products is used as a negative logic adder because the nand gates provide an inversion, and the carry input of the adder is tied high. This inversion is taken into account by the following stage of exclusive or gates.

The partial product register acts as a pipeline register for the second stage of addition. As the double shift and add circuit previously described proceeds to perform another double shift and add in the second ARU state, AS1, the partial product is added to the accumulator. The outputs of the partial product register are passed through a set of exclusive or gates (U5, U6, U7, U8, and U9) controlled by the sign bit of the multiply CSIGN/. Depending on the logic state of CSIGN/, the data can be negated by inverting the data and tying high the carry input of the adder that follows. U19, U20, U21, U22, and U23 form the adder that adds the partial product to the accumulator.

Overflow in the ARU has to be handled properly. In this system, saturation arithmetic is performed. In the event of a positive or negative overflow, the most positive number or the most negative number is forced in place of the overflow number. This is implemented by the most significant two bits in the 20-bit data path within the multiplier. It should be noted that, in forming the 20-bit word to the multiplier from the 16-bit data from the register file, the most significant bit of the 16-bit word is the two most significant bits in the 20-bit word and the least significant three bits of the 20-bit word are tied to zero. Thus, the most significant two bits of the 20-bit word should always be the same unless an overflow has occurred. This condition is detected by exclusive or gate U42. This would force the multiplexors (U33, U34, U35, U36, and U37) to select either the most positive or the most negative numbers, depending on the MSB of the overflow number. The accumulator is formed by 4-bit counters 74LS163s (U45, U46, U47, U48, and U49). The counting function is not used, however; only the synchronous load and clear functions are used.

Because of pipelining, the final result of the multiply and accumulate does not become available until the very end of AS0 of the next system cycle. If a transfer to the result register command is present in the microinstruction, the result register is loaded at this time by XFER CK. If the zero accumulator command is given, the accumulator is also cleared at this instant. Refer to Fig. 3.4 for the ARU module timing.

> **Figure 3.4.** ARU Module Timing. Notes: Microinstruction 1 has ZERO/ and XFER/ bits asserted. Only actions resulting from microinstruction 1 are shown.

## 3.8 Floating Point Converter (FPC) Module

The FPC module serves as an interface between the DSP and the two analog modules: AIN and AOUT. For the DSP, the analog I/O looks simply like another device that can be read from and written into via the DAB. For the analog modules, the FPC module is the source of the timing strobes and clocks that direct the A/D and D/A conversion processes. In addition, the FPC module is responsible for making the floating point/fixed-point translation required for communication between the two analog modules and the DAB.

The FPC module has four major functions:

1. Timing and control generation
2. Input floating-to-fixed-point conversion
3. Output fixed-to-floating-point conversion
4. Headroom level indication.

**Timing and Control Generation Circuitry.** Besides supplying its own timing and control signals, the FPC module generates the timing and control signals for the analog modules. It generates these signals based on several signals from the T&C module: FPC CK, which occurs every system clock time (293 ns), provides the basic clock; RESET/, which occurs every sample time (29.3 ns), synchronizes the timing cycles; RD AD/ and WR DA/, which control the reading from and writing to the floating-to-fixed-point circuitry. The timing and control signals are generated by an 8-bit input cycle counter (U7 and U8), which drives a 256- × 4-bit ROM (U6). Some of the outputs of the ROM are deglitched by a register (U18), and some are directly used as timing and control signals. Because 100 system clock times occur in each sample time, only the first 100 locations of the ROM are used.

Two multiplexors (U4 and U42) implement a self-test mode in which the FPC CK signal is replaced by 02/, the SBC system clock (488 ns) and the RESET/, RD AD/, WR DA/, and the output channel select signals SDAA, SDAB, SDAC, SDAD, are substituted by signals decoded from the counter by nand gates (U5).

The select signal to the multiplexors, FPC DBUG, is tied low in the T&C, ARU, and DMEM modules. Thus, when these modules are removed, the FPC DBUG signal floats high and the self-test mode is automatically activated. In the self-test mode, the only external signal needed is the 02/ clock. The input from the left channel is immediately transmitted to the output channels A and B via the FPC module. Similarly, the right channel is transmitted to channels C and D. In this way, the FPC, the AIN, and the AOUT modules can be checked independently of the DSP. However, in using the 02/ signal from the SBC module, the sampling frequency changes from 34.13 kHz to 20.48 kHz. To obtain the correct sampling rate, the SBC module must be removed also and a 3.413-MHz TTL-compatible input clock must be supplied to pin A28 of the backplane connector using a signal generator.

**Input Floating-to-Fixed Point Conversion Circuitry.** At the beginning of a sample cycle (starting with state 0 of the input cycle counter), the successive approximation register (SAR) on the AIN module is instructed to start an input conversion by bringing STCONV/ signal high and sending thirteen clock pulses on the CNVCK signal. Just after the twelfth clock pulse, the SAR contains valid input data. The LOAD signal to the shift registers (U27, U28, U38, and U39) is then brought high, loading the input data into the shift registers. STCONV/ is brought low again and the thirteenth clock pulse on the CNVCK resets the SAR, readying it for the next conversion.

Shift register U27, U28, U38, and U39 and counter U16 perform the floating-point-to-fixed-point conversion. Note that the LOAD signal is asserted for two clock pulses. The first clock pulse loads the input gain counter, U16, with the input gain bits IGA1 and IGA0. Because a one is also loaded into bit 2 of the input gain counter (U16 pin 12), which is connected to the S1 input of the shift register, both S1 and S0 of the shift register are high for the second clock pulse, causing it to load the 12 bits from the SAR. When LOAD returns low, the input gain counter counts up, and the shift register shifts left until QC QB QA = 000. Gain bits of 00 result in four shifts; 01 results in three shifts; 10 in two shifts; and 11 in one shift. By the fourth clock pulse following the falling edge of LOAD, the Channel 2 conversion is complete. Tristate drivers U25 and U26 enable this data onto the DAB when the DSP asserts the RD AD/ line. Meanwhile, CH1L (a signal derived from CH1 on the AIN module) goes high, causing an input channel switch. A similar conversion for Channel 1 takes place during the second half of the input conversion cycle. Refer to Fig. 3.5 for the floating-to-fixed-point conversion and A/D conversion cycle timing.

**Output Fixed-to-Floating-Point Conversion Circuitry.** The 4-bit register, U40, and the 16-bit register, U36, U37, comprise a double buffer that stores the output channel select code, SDAA–SDAD, and the 16-bit fixed point output value from the DSP, respectively. When the DSP signals an output to the D/A by asserting WR DA/, the double buffer is loaded and NEW DAT/ (U3 pin 6) is asserted, indicating that the double buffer is full. At the next clock pulse, BUSY from the strobe counter, U1, U2, is inspected. If BUSY is high, indicating that a D/A conversion is currently taking place, nothing happens. If BUSY is low, the 16-bit data stored in the double buffer is loaded into shift register U23, U24, U34, U35; the 4-bit select code stored in the double buffer is loaded into register U41; and the flag NEW DAT/, is deasserted, indicating that the double buffer is ready for the next output value. NOR gate U14 pin 1 ensures that this flag is not deasserted if the DSP reloads the double buffer, just as the old information in the double buffer is loaded into the shift registers.

When the shift register is loaded, strobe counter, U1, U2, and output gain counter U43 are loaded, initiating an output cycle. Refer to Fig. 3.6. The output gain counter counts up from zero and the shift register shifts left until NOR gate U14 pin 4 detects one of two conditions: (1) The sign bit is about to be shifted out of the shift register (that is, the two MSBs disagree). When STOP/ goes low, the fixed-to-floating-point conversion is complete. (2) The counter has incremented three times.

The two LSBs of the output gain counter are transmitted to the gain switch amplifier (GSA) on the AOUT module as output gain bits OGA1, OGA0. Meanwhile, the strobe counter has been counting up from its initially loaded value of hexadecimal 2A. After allowing enough time for the fixed-to-floating-point conversion to complete and then enough time for the GSA and D/A converter on the AOUT module to settle, flip-flop U3 pulses the multiplexor enable U42 pin 15, thereby strobing the appropriate output line OUT A–OUT D.

**Headroom Level Circuitry.** The headroom level information is sent to the FPC module from the AIN module, where rectifiers and comparators generate a 5-bit code representing the instantaneous levels of the analog inputs. Because this information is multiplexed between the two input channels, the FPC module demultiplexes it by clocking two headroom registers, U31, U32 and U21, U20, on opposite edges of the channel select signal, CH1. Peak detection occurs by clearing a register bit any time the corresponding headroom bit is asserted. What remains in the register, then, is the complement of the largest headroom word that has occurred since the register was initialized. The SBC module reads a headroom register by strobing either HR1/ or HR2 low, enabling the tristate drivers U19 or U30 onto the SBC module data bus. The rising edge of the strobes trigger a one-shot, which initializes the corresponding headroom register.

> **Figure 3.5.** Floating-to-Fixed-Point Conversion and A/D Cycle Timing. Notes: In the absence of a RESET pulse, all the signals remain the same beyond count 99. Note that the CH1L signal is generated on the AIN module, not on the FPC module.

> **Figure 3.6.** Fixed-to-Floating-Point Conversion and D/A Cycle Timing.

## 3.9 Audio Input (AIN) Module

The AIN module gain conditions, filters, and digitizes two input channels of audio signals in a floating point format. The major subsections of the module are:

1. Input gain conditioning and filtering
2. Sample-and-hold and multiplexer circuits
3. Gain ranger
4. Analog-to-digital converter (ADC)

**Input Gain Conditioning and Filtering.** Inputs are transformer-coupled and then gain-conditioned by a buffer stage with an adjustment range of 15 dB. The nominal level at the output of buffer stage U1 is +13 dBm (5-V peak) at 1 kHz. This amplitude corresponds to the onset of clipping in the ADC. Diode clamps prevent overloading the input stage of U1.

The input filters are 7-pole active elliptical (or Cauer) networks synthesized from "FDNR" networks. The nominal cut-off frequency for the input filters is 15 kHz to prevent aliasing distortion at a sampling rate of 34.13 kHz. The next stage is a shelving preemphasis network with 50-us and 12.5-us time constants. The last filter stage provides aperture correction to compensate for the slight amount of high-frequency loss introduced by the sampling process.

**Sample-and-Hold and Multiplexer Circuits.** The input sample-and-hold (S&H) circuits are designed so that when one channel is tracking, the other channel is in hold mode. Control signal CH1L places U20 in hold mode when HIGH, simultaneously placing U21 in tracking mode. Analog switch U22 is controlled by HLCH1L, an inverted and level-shifted version of CH1L. This switch is configured so that the "held" channel is commutated to the gain switch amplifier (GSA) stage.

**Gain Ranger.** Both filtered channels are sent to precision full-wave rectifier circuits that give a positive output equal to the peak amplitude of their inputs. The rectified output of the tracked channel is routed by analog switch U14 to an amplitude quantizer made up of five comparators biased at 5.0 V, 2.24 V, 1.12 V, 0.56 V, and 0.280 V, respectively. These thresholds are arranged so that 5 V corresponds to the onset of clipping in the ADC, and each of the lower thresholds is 6 dB apart and allows determination of the optimum gain to be used for the GSA. Table 3.3 shows how the proper gain is selected for signals of various amplitudes.

### Table 3.3. Comparator Outputs Showing Selected Gains for Various Signals

| Signal | U15-13 (5.0 V) | U15-1 (2.2 V) | U15-2 (1.12 V) | U16-1 (560 mV) | U16-2 (280 mV) | GAIN A (dB) | IGA1 | IGA0 |
|---|---|---|---|---|---|---|---|---|
| >5.0 V | 0 | 0 | 0 | 0 | 0 | 0 | 0* | 0* |
| 2.24–5.0 V | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.12–2.24 V | 1 | 1 | 0 | 0 | 0 | 6 | 0 | 1 |
| 560 mV–1.12 V | 1 | 1 | 1 | 0 | 0 | 12 | 1 | 0 |
| 280 mV–560 mV | 1 | 1 | 1 | 1 | 0 | 18 | 1 | 1 |
| <280 mV | 1 | 1 | 1 | 1 | 1 | 18 | 1 | 1 |

> \* Comparator outputs are decoded and latched to provide gain-control signals IGA0 and IGA1.

The 5-V and the 280-mV comparator outputs are needed for headroom display only, while all of the additional comparators provide gain-change information as well as headroom display. A gain of 6 dB is added whenever a signal falls below 45% of the clipping level. A signal level falling to 45% of the clipping level would then be increased by a factor of two to about 90% of clipping level to take full advantage of the ADC's usable dynamic range. The technique of gain ranging used here is commonly referred to as "instantaneous floating point conversion" — that is, an appropriate gain is selected just before converting each sample. The gain thus follows the envelope of the converted signal.

Excellent signal reconstruction can be achieved if the ADC is properly offset to deliver a zero code for 0-V input. Good gain matching is provided by using a precision resistor network to set the gain of U23. The resistor feedback ratio is selected by analog switch U24. Because U24 conducts negligible current, errors resulting from switch resistance are also negligible. U24 also provides a decode function for gain bits HLG0 and HLG1. Voltage offset in this stage is not important, provided that it is proportional to gain. Maximum offset due to accumulated errors should never exceed 80 mV at this output stage.

**Analog-To-Digital Converter.** The analog-to-digital converter (ADC) is a 12-bit successive-approximation type. A 12-bit current output digital-to-analog converter (DAC) is sequenced by a successive approximation register (SAR) chip, U26. This device receives its start command (STCONV) and conversion clock (CNVCLK) from the FPC module. An LM211 comparator is used to compare the DAC's output with the input signal. The output of this comparator is used as the input to the SAR.

## 3.10 Audio Output (AOUT) Module

The AOUT module provides four output channels serviced from a single timeshared DAC and gain switch amplifier. The AOUT module has four major subsections:

1. Digital-to-analog converter (DAC)
2. Gain ranger
3. Demultiplexor and sample-and-hold circuits
4. Filtering and output gain conditioning

**Digital-to-Analog Converter.** The DAC, U2, is updated by 12-bit word DA0 to DA11. The DAC responds with an analog output in the range of −5 to +5 V.

**Gain Ranger.** Gain control is set by two bits, OGA1 and OGA0, which control analog switch U3. U3 selects one of four taps from precision divider network RD2. Gain selection is either 1, 1/2, 1/4, or 1/8 ±0.05%. U4 operates as a high input impedance follower to prevent loading of the attenuator network.

**Demultiplexor and Sample-and-Hold Circuits.** The corresponding channel-selection signal OUT A, B, C or D goes high approximately 1.76 us after DAC and gain data become valid. This delay allows time for the DAC and GSA to stabilize before placing the selected output sample-and-hold in the sample mode. The OUT (sample) command is valid for approximately 4.08 us. During this time, U6 switches the output gain-conditioned DAC voltage to capacitor C13, 16, 17, or 20. U7 and U8 provide high impedance buffering to prevent discharge of the sample capacitors during the hold period.

The +7- and −7-V CMOS switch bias is provided by zener diode regulators, CR5 and CR6. Power-on muting is provided by transistor Q9, which is held off for several seconds after power is applied. R159 charges a 22-uF capacitor from −7 to +7 V. Saturation of Q9 places a ground signal on pin 6 of U3, enabling U3 to pass signal.

**Filtering and Output Gain Conditioning.** Output deemphasis is provided by stages U13 and U21. Filtering is provided by 7-pole elliptical (Cauer) filters. Adjustments to compensate component sensitivity are provided for each section. These settings should never need adjustment if related components are not changed.

The output stage consists of a level adjustment potentiometer and an opamp stage with a complementary output transistor buffer for each channel. Overall, negative feedback is provided around the stage to maintain fixed gain and provide low distortion. A loading network is also provided to maintain high-frequency stability. Each output stage drives an output transformer on the audio transformer board at the rear of the chassis with the audio I/O connectors. The output transformer provides a voltage gain of about 2.5.

## 3.11 Power Supplies

The three 224X power supplies produce six regulated dc voltages and one unregulated ac voltage.

**+5-V and −5-V Power Supplies.** The +5-V and −5-V power supplies are derived from a single secondary winding fused in both legs by a pair of 15-amp slow-blow fuses. The +5-V power supply consists of a uA723 regulator, a current boost transistor, and a pair of high-current pass transistors. The regulator is a current foldback design that limits short-circuit currents to less than 3 A.

Over-voltage protection is provided by a crowbar circuit. The +5-V power supply is designed to provide a continuous 10 A. Both voltage and current limits are adjustable.

The −5-V power supply is a 7905 monolithic regulator fused at 2.5 A. This power supply is both current-limited and thermally protected. It is designed to provide 250 mA.

**+12-V and −12-V Power Supplies.** The +12-V and −12-V power supplies are derived from a single secondary fused in both legs by a pair of 3-A slow-blow fuses. The +12-V power supply consists of a LM317K monolithic voltage regulator controlled by a pair of 1% resistors. This power supply is both thermal- and current-protected, and provides 1.25 A. The −12-V power supply is derived from a 7912 monolithic voltage regulator that is both thermal- and current-protected, and provides 150 mA.

The +12-V power supply is interlocked with the −5-V power supply so that +12 V is not available until after −5 V is available. Should any problems occur with the +12-V power supply, check to be sure that the −5-V power supply is available.

**+15-V and −15-V Power Supplies.** The +15-V and −15-V power supplies use a tracking design that allows the −15-V power supply to track the +15-V power supply. Both are derived from a single secondary fused in both legs by a pair of 2-A slow-blow fuses. The +15-V power supply is an LM317 monolithic voltage regulator incorporating an adjustable resistor network. The −15-V power supply is a 7912 controlled by an LM301 opamp that senses the difference between the +15-V and −15-V outputs and forces the −15-V output to track the +15-V output. A balance control is provided to trim the −15-V output. The ±15-V power supplies are not ground-referenced to the ±5-V or ±12-V power supplies unless the analog boards are installed in the 224X chassis. All voltage measurements must be referenced to the correct ground. The +15-V power supplies provide 750 mA and are current and thermal protected.

**Mains Circuit.** The mains circuit for the 224X uses a dual primary transformer with 120-V and 100-V taps (a pair of DPDT switches select the operating voltage: 100, 120, 220, 240 V). This supply is switched on both sides of the line. A primary fuse is provided on the chassis ahead of the RFI filter unit. Fan power is maintained at 120 V by placing the fan across one of the 120-V primaries.

---

# 4 Performance Tests and Calibration

Performance tests are used to check the operation of the unit. Always execute the performance tests before proceeding to calibration.

## 4.1 Test Equipment Required

The following equipment is needed for performance tests and calibrations:

1. Variable ac voltage source with isolation transformer, voltmeter, and ammeter
2. Digital voltmeter (DVM)
3. Dual trace oscilloscope with >60-MHz bandwidth
4. Audio band low distortion sine wave generator with a 20-dBm maximum output
5. Harmonic distortion analyzer with level meter
6. Noise meter
7. High-quality music source
8. Lexicon-compatible footswitch and footpedal
9. Headphone amplifier and headphones
10. Cables and dip clips
11. Extender card (Lexicon no. 750-01850)
12. 1.15-ohm, 30-W resistor

See Figs. 4.2 and 4.3 at the end of this section for interior views of the 224X mainframe.

## 4.2 System Tests

**Diagnostics, nonvolatile storage, and listening tests.** When the 224X is turned on or reset, it runs a series of diagnostic programs.

1. Make sure that the unit passes all power-up diagnostics. Repeat the diagnostics several times.
2. Store a control-head setting in a register, then leave the unit off for a while (>1 min). Turn on the unit and make sure that the setting is restored. Check to see that the contents of the register are unchanged by calling the register.
3. Using various signals from signal generators and music sources, listen carefully to all programs and variations. Make sure that there are no excess or unusual noises, birdies, or intermittents.
4. Make sure that moving or gently shaking the control head or mainframe does not affect its output.

**Visual Inspection.** Inspect the 224X and control head for obvious signs of physical damage. If possible, compare it with a unit operating properly. Remove the front panel of the unit and make the following checks:

1. The protective shield should be in place for the power switch and wiring.
2. The fuse ratings should be as follows:

   | Fuse | Rating |
   |---|---|
   | Primary 100/120 V | 3 AG 3 A slow blow |
   | Primary 220/240 V | 3 AG 1.5 A slow blow |
   | F1, F2 (±15 Vac) | 2 A slow blow |
   | F3, F4 (+12 Vac) | 3 A slow blow |
   | F5 (+10 Vac) | 2 A slow blow |
   | F6, F7 (±5 Vac) | 15 A slow blow |
   | F8 (−5 Vdc) | 2.5 A slow blow |

   *(Fuse numbers are schematic fuse numbers.)*

3. The ac voltage changeover switches should be set correctly (see Sec. 1 of Owner's Manual).
4. All jacks, pots, and switches should operate smoothly.
5. XLR connectors should be secure.
6. There should be no loose screws.
7. All ribbon cables and connectors should be secure.
8. All ICs should be securely in their sockets.
9. There should be no parts missing.

## 4.3 Power Supplies (PS1, PS2, and PS3)

The nominal and operating line voltages for the 224X are as follows:

| Nominal (Vac) | Operating (Vac) |
|---|---|
| 100 | 90–105 |
| 120 | 108–126 |
| 220 | 198–231 |
| 240 | 216–252 |

Measure all power supplies. Compare voltages to Table 4.1. All power supplies must provide the correct voltage; if they do not, repair and/or calibration is required.

### Table 4.1. Test Point Locations for Power Supplies

| # | Supply (Vdc) | Limits (Vdc) | Location Description | Adjustment Location |
|---|---|---|---|---|
| 1 | +5 | 4.85 to 5.15 | SBC module; U16, pin 16: left front-most IC; left front IC pin; verify left LED lit on NVS module | R7 on PS3 |
| 2 | −5 | −4.75 to 5.25 | SBC module; J72 at the rear and right of U16** | * |
| 3 | +12 | 11.4 to 12.6 | SBC module; R8 front lead; 2.7-Kohm, 1/4-W resistor, left of U15; verify center LED lit on NVS module | * |
| 4 | −12 | −11.4 to 12.6 | SBC module; R4 front lead; 270-ohm, 1/2-W resistor, right of U15 | * |
| 5 | +15 | 14.75 to 15.25 | AIN module; +15 = test point, ground to test point | R6 on PS2 |
| 6 | −15 | −14.75 to 15.25 | AIN module; −15 = test point, ground to test point | R5 on PS2 |
| 7 | +7 | 6.3 to 7.7 | AIN module; +7 = test point, ground to test point | * |
| 8 | −7 | −6.3 to 7.7 | AIN module; −7 = test point, ground to test point | * |
| 9 | +7 | 6.3 to 7.7 | AOUT module; +7 = test point, ground to test point | * |
| 10 | −7 | −6.3 to 7.7 | AOUT module; −7 = test point, ground to test point | * |
| 11 | 10 Vac | 8 to 14 Vac | Power molex connector on Transition module | * |

> \* No adjustment.
> \*\* To access this test point, turn off the 224X and loosen the SBC module from its backplane connector, connect a test lead to the J72 test point, and then reinsert the SBC module into the backplane.

## 4.4 Analog Tests

Apply a 1-kHz, +12-dBm sine wave from the oscillator to both input channels. (This signal is used for standard input tests.) Run the zero-delay test program.

### 4.4.1 Input sensitivity

Adjust the signal generator output for +8 dBm. Advance input gain adjust pots R1 and R2 until the onset of clipping is reached (the gain pots should be close to their full clockwise rotation). Next, set the signal generator for +18 dBm and rotate the input gain pots counterclockwise (CCW) to just below the clipping level. This should be close to full CCW rotation. Design tolerances allow most machines to operate within a +7- to +22-dBm input range, even though the device is rated at +8 to +18 dBm. Adjust R1 and R2 so that the "0 dB" LED headroom indicator just goes off when the signal generator output is set at +12 dBm.

### 4.4.2 Output sensitivity

Check each channel for audio output. Make sure that each output can deliver +8- to +18-dBm output into a 600-ohm load by varying the output gain potentiometers; then set each output gain for an output level of +12 dBm.

### 4.4.3 Frequency response

Check frequency response for each output channel and compare with the frequency response curves in Fig. 4.1. Make sure that the frequency response is within system specification: ±1.5 dB from 20 Hz to 15 kHz; ±0.5 dB from 20 Hz to 12 kHz.

> **Figure 4.1.** Typical Overall System Frequency Response.

### 4.4.4 Total harmonic distortion (THD) and noise

THD and noise measured at 1 kHz and 10 kHz should be as follows:

| Signal Level (dBm) | Frequency (kHz) | THD and Noise (%) |
|---|---|---|
| +12 | 1 | <0.04 |
| 0 | 10 | <0.50 |

### 4.4.5 Noise floor/signal-to-noise ratio

With 600-ohm loads connected to both inputs and outputs, the noise level at each output should be within the following limits:

| | Wide Band (20 Hz to 20 kHz) | A-Weighted |
|---|---|---|
| Noise floor | <−68 dBm | <−80 dBm |
| Ratio relative to +12 dBm | >80 dB | >92 dB |

### 4.4.6 Channel separation

On the left channel input, remove the signal source and connect a 600-ohm load. Apply the standard input test signal to the right channel input. Residual signal measured in output channels A and D should be 60 dB or more below +12 dBm (−48 dBm or below).

Next, remove the input signal to the right channel input and connect a 600-ohm load. Apply the standard input test signal to the left channel input. Residual signal measured in output channels B and C should be −48 dBm or below.

## 4.5 Calibration

Before proceeding with calibration procedures, the performance tests (Secs. 4.1 to 4.4) should be carried out to determine whether adjustments are necessary.

### 4.5.1 +5-V current foldback adjustment

1. Turn off the 224X and remove the NVS module from its slot (labeled OPT.).
2. Clip a 1.15-ohm 30-W resistor onto pins 1 and 3, and attach a DVM's minus lead to pin 1 and its positive lead to pin 3. Insert the extender board into the OPT. slot.
3. Turn on the unit. Adjust R11 on power supply module 3 until the meter reads approximately 3.00 V (2.8 to 3.2 V).
4. Remove the extender board and replace the NVS module.

> **Caution:** The 1.15-ohm resistor must handle at least 30 W; it may become hot during use.

### 4.5.2 Phase-lock loop calibration

1. Connect channel 1 of the oscilloscope to U27 pin 3 and synchronize on channel 1.
2. Connect channel 2 of the oscilloscope to U27 pin 8 (clip on the end of R10, 1 K resistor).
3. Adjust the variable capacitor C12 for a loop control voltage, U27 pin 8, of about 3.8 V.

### 4.5.3 Input offset calibration

Power down and carefully remove U23. Connect a jumper from pin 6 of the U23 socket (hook onto CR21 cathode) to a quiet ground (for example, low side of C73). Power up and connect one channel of the oscilloscope to U19 pin 1 (CH1L) and the other channel to U26 pin 21 (MSB of A/D word). Synchronize on CH1L (positive going) and set the oscilloscope to 5 us/DIV and 2 V/DIV on each channel. Offset (R90) should now be adjusted so that the MSB (most-significant bit) dithers between 1 and 0 with equal intensity when viewed on the oscilloscope.

Power down, remove jumper, and replace U23. This procedure ensures that the analog-to-digital converter (ADC) responds with code 1000 0000 0000 or 0111 1111 1111 for a true 0-V input. This will ensure good gain step matching during output conversion.

### 4.5.4 Output offset calibration

Set up mainframe with the AOUT module on an extender card. Apply a 1-kHz, +12-dBm sine wave from the oscillator to both input channels. Run the zero-delay test program. Adjust the input level potentiometers (R1 and R2) on the AIN module so that the overload indicator in the headroom display is just turned off. Measure the level of the output of Channel A. Adjust the Channel A output level potentiometer (R119) so that the output level is +12 dBm. Measure the distortion of the Channel A output. Adjust R4 for minimum distortion.

### 4.5.5 Output filter calibration

Each of the four output filters has three null adjustments to compensate for component sensitivity. The nulling procedure is done by removing the signals to the audio inputs and then injecting signals at various frequencies at certain points. The following procedure outlined for channel A should be executed on all four channels.

1. Apply a 22.153-kHz signal with peak amplitude of 0.5 V to the high side of R43 and adjust R19 for a null at node R20/R21.
2. Apply a 19.200-kHz signal with peak amplitude of 0.5 V to node R20/R21 and adjust R25 for a null at node R26/R27.
3. Apply a 35.850-kHz signal with peak amplitude of 0.5 V to node R26/R27 and adjust R31 for a null at node R32/R33.
4. If nulls can't be achieved, carefully examine all component values of the stage in question.

Repeat for channels B, C, and D. Refer to schematics for corresponding test points.

> **Figure 4.2.** 224X Mainframe Interior — Front View. Labeled items: Protective Shield, Board Retainer, I/O Cable, Power Switch, Reset Switch, Voltage Changeover Switch, ARUCK Error Indicator. Modules (top to bottom): NVS, SBC, DMEM, T&C, ARU, FPC, AIN, AOUT.

> **Figure 4.3.** 224X Mainframe Interior — Top View. Labeled items: Fuses for 5-Vdc Supplies (15A slow blow), Fuse for ac Power to Control Head (2A slow blow), Fuses for 12-Vdc Supplies (3A slow blow), Fuses for 15-Vdc Supplies (2A slow blow), Power Switch, Reset Switch, Voltage Changeover Switch.

---

# 5 Troubleshooting

## 5.1 Overall Approach

A thorough visual inspection of the 224X and control head is good general troubleshooting practice. Check for any obvious component failures, such as burnt or overheated parts or damaged PC board traces. There should be no loose ICs, connectors, or cables. Observe whether the malfunction is intermittent, heat related, or shock related.

Figure 5.1 shows a flow chart for troubleshooting problems in the Model 224X. As can be seen, the power-up software diagnostics are an important tool in the troubleshooting process. One of the first things to do is to see whether the unit can run the power-up diagnostics. If these diagnostics do not run, the problem probably is in the power supply module, the SBC module, or the remote control head. (Note that the power-up diagnostics will run with only these three modules in the unit.) First look at the power supplies, then check the cable to the control head. If the problem is with the control head or the connecting cable, and the mainframe is functional, the unit will eventually run one of the reverberation/effects programs (after running the power-up diagnostics), with the remote control head disconnected.

If the unit can run the power-up diagnostics, the diagnostic error codes it produces often supply some information about the nature of the malfunction. Note that the power-up diagnostics test only the digital signal processor (DSP) circuitry, that is, the NVS, SBC, DMEM, T&C, and ARU modules. Although the power-up diagnostics are thorough, they do not test these modules completely. Also, with noise-related or intermittent problems, the power-up diagnostics may not catch an error. Thus, if the unit passes power-up diagnostics, but the reverberation/effects programs sound bad, the DSP may have problems that are not diagnosed by the power-up diagnostics, or the analog conversion system, that is, the FPC, AIN, and AOUT modules, may have problems.

Furthermore, it is possible for the reverberation/effects programs to sound OK and the unit to fail power-up diagnostics. Possibly, the diagnostic hardware or a low-order bit may be malfunctioning. In any case, these kinds of problems should be pursued.

The analog conversion system can be tested on its own through a self-test procedure. Self-test is accomplished by removing the DSP, NVS, DMEM, T&C, and ARU modules. The SBC module is retained to generate a clock signal. If the unit works in the self-test mode, the problem is likely to lie with the DSP.

The 224X has several other diagnostic programs available to help when troubleshooting problems. These programs are called by pushing one of the eight program pushbuttons at the beginning of the power-up diagnostics. The diagnostic programs are listed in Table 5.1.

The first diagnostic programs to run are a maximum delay (0.5-sec) program (diagnostic program 8) and a zero delay program (diagnostic program 7). These delay programs are similar, except that the maximum delay program uses the DMEM module and the zero delay program does not. Thus, if the unit works in the zero delay program, but not in the maximum delay program, the problem is probably in the DMEM module. These two programs also help in exercising the digital-to-analog interface that is not tested in the self-test mode and in diagnosing where a problem is in the analog conversion system. (Note that the self-test mode does not run at the correct sampling rate when the SBC module is used to generate the clock signal.)

> **Figure 5.1.** Troubleshooting Approach. *(Flow chart — see original manual.)*

### Table 5.1. Diagnostic Programs

| Program* | Description |
|---|---|
| 1 RESTART | Restarts self-testing power-up diagnostics and returns to normal operation |
| 2 QUICK EXIT | Exits directly to normal operation |
| 3 ARU SIGNAT | Generates signature analysis signals; for use by service personnel to test the ARU module |
| 4 ARU TEST | Runs a quick test of the ARU module and returns to menu |
| 5 NVS STROBE | Generates analysis signals; to test the NVS module |
| 6 FPC SIGNAT | Generates signature analysis signals; to test the FPC module |
| 7 ZERO DELAY | Loads a 0-second delay-line program for setting input and output levels; Left input passes to outputs A and D, and Right input passes to outputs B and C |
| 8 MAX DELAY | Loads a 0.5-second delay-line program for setting input and output levels; Left input passes to outputs A and D, and Right input passes to outputs B and C |

> \* Programs 3, 4, 5, 6, and 7 are not implemented in V8.0 software.

The ARU test (diagnostic 4) exercises the ARU module more thoroughly than the power-up diagnostics and can be tried when the unit passes power-up diagnostics but the ARU is still suspected to be bad. The NVS strobe program (diagnostic 5) continuously sends signals to the NVS module so that they can be checked with an oscilloscope. In addition, two signature programs (diagnostics 3 and 6) can be used with signature analyzers for troubleshooting some of the modules. The signature programs are also useful in troubleshooting with oscilloscopes, because they provide simplified and more observable signals to the various modules.

## 5.2 Power Supplies

If the 224X does not power up, first check the ac line cord for a good connection and the service outlet for power. Next check the power fuse at the rear of the mainframe. If the fuse is blown, replace with an exact replacement fuse: 3AG 3A slow blow for 100/120 Vac operation, 3AG 1.5A slow blow for 220/240 Vac operation.

The 224X mainframe has a 10-Vac unregulated power supply (ac-fused), three pairs of ac-fused regulated power supplies, and one dc-fused regulated power supply. A blown internal fuse generally indicates a problem in the related power supply circuitry, which should be thoroughly checked out.

Table 5.2 lists the power supply fuses. Replacement fuses should always have the correct rating to ensure protection from circuit damage or fire. Table 5.3 shows the location of each of the power supplies.

### Table 5.2. Power Supplies and Fuses

| Schematic Fuse No. | Fuse Board Designation | Power Supply Fusing | Fuse Rating |
|---|---|---|---|
| F1, F2 | ±15 V | +15 Vac Secondary | 2 A slow blow |
| F3, F4 | +12 V | +12 Vac Secondary | 3 A slow blow |
| F5 | Viso | +10 Vac Secondary | 2 A slow blow |
| F6, F7 | ±5 V | ±5 Vac Secondary | 15 A slow blow |
| F8 | −5 Vdc | −5 Vdc | 2.5 A slow blow |

### Table 5.3. Location of Power Supplies

| Power Supply | Output Supply Voltage/Current Rating | Rectified/Filtered | Regulated |
|---|---|---|---|
| +15 V | +15 Vdc/750 mA | PS2 | PS2 |
| −15 V | −15 Vdc/750 mA | PS2 | PS2 |
| +12 V | +12 Vdc/1.25 A | PS3 | PS2 |
| −12 V | −12 Vdc/150 mA | PS3 | PS3 |
| +10 Viso | +5 Vdc/500 mA | Control Head | Control Head |
| +5 V | +5 Vdc/10 A | PS1 | PS3 |
| −5 V | −5 Vdc/250 mA | PS1 | PS3 |

The first test of any faulty operation is to make sure all power supplies are working properly.

## 5.3 Power-up Diagnostics

The 224X diagnostic programs test many components of the digital hardware. Although a diagnostic routine may not point out the exact component that has failed, a faulty module or section can usually be isolated. Diagnostic error messages are easier to understand if you are familiar with the overall operation of the 224X and the hexadecimal numbering system.

Table 5.4 shows number conversion between decimal, hexadecimal, and binary numbering systems. Figure 5.2 shows how errors and correct data are displayed on the control head.

### Table 5.4. Number System Conversion

| Decimal | Hex | Binary |
|---|---|---|
| 0 | 0 | 0000 |
| 1 | 1 | 0001 |
| 2 | 2 | 0010 |
| 3 | 3 | 0011 |
| 4 | 4 | 0100 |
| 5 | 5 | 0101 |
| 6 | 6 | 0110 |
| 7 | 7 | 0111 |
| 8 | 8 | 1000 |
| 9 | 9 | 1001 |
| 10 | A | 1010 |
| 11 | B | 1011 |
| 12 | C | 1100 |
| 13 | D | 1101 |
| 14 | E | 1110 |
| 15 | F | 1111 |
| 16 | 10 | 0001 0000 |
| … | … | … |
| 255 | FF | 1111 1111 |

> **Figure 5.2.** Control Head Error Display. The error code appears in the 7-segment displays. Correct data is shown on one LED row (LSB to MSB) and data in error on another.

The 224X diagnostic programs are run whenever the machine is turned on or reset. They can also be run by holding the SHIFT key while pushing CALL and PROGRAM 1 (SHIFT/CALL/PGM 1). The diagnostics make a single pass through all testable features of the machine. If the 224X passes all tests, normal operation begins. If an error is detected, an error message is displayed.

The diagnostic sequence varies for the nonvolatile storage (NVS) module, depending on how the diagnostics are started. When the diagnostics are started by powering up or resetting the 224X, a checksum test is performed on all ROMs on the NVS module, but the nonvolatile RAM is not tested because data can be lost if the power becomes unstable during testing. When the key sequence CALL/SHIFT/PGM 1 is used to start the diagnostics, testing of the nonvolatile RAM on the NVS module is included in the diagnostic program sequence. When the NVS module's nonvolatile RAM is tested, the contents are loaded into the RAM on the SBC module and reloaded to the NVS module when the test is finished. This procedure ensures that registers are not lost as a result of testing.

> **Caution:** Do not reset or power down the unit while the NVS diagnostic is in progress; otherwise contents of the NVS registers may be lost.

During a diagnostic test, or when an error is displayed, all controls and pushbuttons on the control head, except the PROGRAM pushbuttons, are inactive. Briefly pushing PGM 1 allows the unit to go to the next diagnostic test after an error display. Pushing PGM 2 bypasses all further diagnostics and starts normal system operation. Pushing PGM 7 calls a zero delay test program and pushing PGM 8 calls a maximum delay test program.

The diagnostic programs compare the actual data in one part of the machine to the data that should be there if the machine were working perfectly. The diagnostic programs display the expected data pattern (the good data) using the LEDs on the PROGRAM pushbuttons. If different from the expected data pattern, the pattern of the actual data resident in the machine is displayed using the mode/register pushbutton LEDs. Usually an error is displayed when the two data patterns do not agree. The patterns displayed by these LEDs are essential in determining the cause of error. If errors appear, the error message numbers and the lighting patterns of the LEDs should be noted in the order of occurrence when diagnosing or referring a problem to Lexicon service technicians. Table 5.5 is a summary of the 224X error codes, Sec. 5.3.1 describes in detail how to run the programs during troubleshooting, and Sec. 5.3.2 gives in-depth descriptions of the error codes.

### Table 5.5. Summary of 224X Error Codes

| Error Type* | Cause of Error |
|---|---|
| E0X | SBC ROM checksum |
| E1X | SBC RAM |
| E2X, E3X, E4X | T&C (may also be DMEM) |
| E5X – E8X | ARU (may also be T&C or DMEM) |
| E91, E92, E95, E96 | DMEM |
| H0X, H2X | NVS ROM checksum |
| H1X | NVS RAM |
| H2F, H10 | NVS card missing |

> \* Where X is from 0 to 9 or from A to F.

### 5.3.1 Running the diagnostics

The 224X diagnostic programs are run in a particular order. In general, if the diagnostics indicate an error, the source of the first error should be found before much time is spent on any others. The checksum and microprocessor tests come first. Errors here may not disrupt the reverberation or effects programs and are easy to interpret. The remaining diagnostics work by loading the T&C module with a simple program and testing the effects of the program on the machine. The microprocessor must communicate with the T&C module to perform these tests. Failure to communicate usually results in an E23 error, which means that either the timing is incorrect between the T&C module and the microprocessor or a memory chip on the T&C module is faulty. The T&C module has a single LED diagnostic indicator labeled ARUCK ERROR. If this LED lights, the timing signal ARUCK (ARU Clock) is missing, indicating a failure within the clock circuitry on the T&C module. Because the entire machine depends on the T&C module, any problem on this module generally gives errors in other diagnostic tests, even if other sections are not faulty.

Some parts of the tests cannot be easily separated. All tests of the DMEM module require that the ARU module work at least minimally. Most of the microprocessor communication and test circuits for both the T&C and ARU modules are on the DMEM module. A failure here may cause the T&C test to take a long time to complete and may also cause an unusual flashing pattern of the LEDs on the control head. In addition, a short circuit or defective IC on the ARU or FPC modules can cause an error that appears to be on the T&C module. It is sometimes useful to unplug the ARU and FPC modules to see if the error still occurs. The FPC module is not testable by the microprocessor, and the machine should pass all diagnostics with the FPC module unplugged.

If the machine does not appear to work at all, the cable to the control head should be checked first. If no diagnostic errors occur, the machine will eventually run the sonic ambience programs with the control head unplugged. If so, the control head or the cable is faulty. However, it is more likely that a transformer plug in the power supply has come loose, or that a power supply fuse has opened. See Sec. 5.2 for the power supply test points. Failure of the machine to respond with either diagnostics or reverb programs when the power supplies are good probably means that the SBC module is faulty.

### 5.3.2 Descriptions of error codes

**E00 through E0F: SBC ROM checksum test.** Each ROM in the SBC module is checked by adding all data bytes; if the data is correct, the sum is 0. If an error is detected, one of the error messages E00 through E0F is displayed, depending on which ROM is faulty. The least-significant hexadecimal digit of the error code represents an encoded nibble (4-bit quantity) binary value. Within that binary value, the bit positions corresponding to a logic 1 identify which chip numbers are faulty. ROM 1 (U23) is indicated by a binary equivalent of 1, ROMs 2 and 3 are both indicated by a binary equivalent of 6, etc., for example:

| Error Message | Binary Representation | Faulty ROM* |
|---|---|---|
| E01 | 0001 | 1 |
| E02 | 0010 | 2 |
| E06 | 0110 | 2 and 3 |
| E0F | 1111 | 1, 2, 3, and 4 |
| E0A | 1010 | 2 and 4 |

> \* ROM 1 = U23, 2 = U25, 3 = U24, and 4 = U26.

Note that a checksum error does not always result in a noticeable machine malfunction.

**E10 through E13: SBC module RAM test.** The RAM on the SBC module is tested using a semirandom pattern, altering all contents. Errors are indicated by display of one of the error messages E10 to E13, depending on the address of the incorrect byte; for example, E10 corresponds to hexadecimal addresses 3C00 to 3CFF and E11 corresponds to addresses 3D00 to 3DFF. The correct pattern is displayed on the Program LEDs, and any incorrect pattern is displayed on the mode/register LEDs. The bit positions corresponding to the elements of the patterns that do not match isolate the location of the error. The error messages and bit patterns are defined as follows:

| Error Message | RAM Addresses |
|---|---|
| E10 | 3C00–3CFF |
| E11 | 3D00–3DFF |
| E12 | 3E00–3EFF |
| E13 | 3F00–3FFF |

Bit positions: PROGRAM LEDs show correct data; Mode LEDs show incorrect data. Bits 0 to 3 are in U36 of the SBC module and bits 4 to 7 are in U37. (LSB = least significant bit; MSB = most significant bit.)

The test is accomplished in two passes. First, the memory is loaded with the contents of ROM 1, starting from location zero. This data is complemented twice in two separate passes. The data in RAM is then compared with the original data in ROM. (Data is read from the top down.) The test will stop as soon as any error has been detected. This RAM test is sensitive to addressing errors and data errors.

**Control Head Display Test.** The panel test outputs data to the control head to light all LEDs (except the 7-segment displays, which display the revision number of the resident software). The test is bypassed if PROGRAM 1 is pushed. The control head display should blank out after the panel test for about 10 to 15 seconds, while the unit is performing diagnostics. Failure of the DMEM and T&C modules to return a ready signal to the SBC module causes the writable control store (WCS) memory test to require more than a minute to complete. If the 224X is not initialized after several minutes, the protect circuitry on the T&C module may be locking the 8080 on the SBC in a hold state. This condition means that the HALT decoding circuitry on the DMEM module or the protect gating on the T&C module is faulty.

**E20 through E23: Writable Control Store (WCS) memory test.** The WCS (U3, U18, U33, U48, and associated circuits on the T&C module) are tested in the same way as the RAM on the SBC module is tested. The error codes, E20 to E23, are as follows:

| Error Message | Hexadecimal Address | Component |
|---|---|---|
| E20 | 4000, 4004 … 41FC | U49 & associated circuits |
| E21 | 4001, 4005 … 41FD | U33 & associated circuits |
| E22 | 4002, 4006 … 41FE | U18 & associated circuits |
| E23 | 4003, 4007 … 41FF | U3 & associated circuits |

Correct data is displayed on the program LEDs, and faulty data is displayed on the mode/register LEDs. Error message E23 could mean that the entire program memory is faulty. If so, or if a problem on the DMEM module prevents data from being properly loaded into the program memory, the memory test will take a long time to complete. Such a delay indicates faults in the SBC bus-decoding checks in the DMEM module or on the T&C module. Two of the memory chips can be swapped to see if different error messages are displayed. Other problems, such as open or shorted address lines, or defective address or data buffers, can also cause a faulty program memory. The diagnostics detect such problems, but require additional steps to isolate them.

**E32: 8080 bus test register test.** If an error is found when checking the contents of the 8080 bus test register, the 8080 microprocessor in the SBC module cannot communicate with the DSP (consisting of the T&C, ARU, and DMEM modules). If an actual system error occurs, as opposed to a fault in the diagnostic test, it will seriously affect proper operation of further diagnostics as well as the reverberation and effects programs. Short circuits on the T&C or DMEM modules may be the cause. Check to see if the error occurs with the T&C module unplugged. If so, the DMEM module, the Backplane, or the SBC module is faulty. If the reverberation or effects programs seem to be running properly, the bus test register itself (U34 on the DMEM module) is faulty, and the error can be ignored, because it will not interfere with the proper operation of the reverberation and effects programs in the machine.

**E40 & E41: Halt and single-step mode tests.** Both the halt and single-step mode tests display an error if the return data matches, indicating the halt state cannot be initiated. Because the first program step is continually repeated in the halt state and many tests load known data into the first program step and look for that data at the output of the T&C module, it is necessary to be able to initiate the halt state for subsequent diagnostics to be valid. The halt test works by loading an instruction in the second executable address of the WCS memory. This instruction transfers data from the input of the XREG to the output, and a value loaded into the XREG is checked against the value output. If a halt condition has occurred within the 224X, the values will be different. If no halt has occurred, the values will be identical.

**E43: XREG read/write test.** The ability of the DSP to read correctly from and write correctly to the transfer register (XREG) on the DMEM module is tested. The WCS memory is first loaded with a NOP and then with an instruction to read the XREG and write to it. If the DSP cannot execute these functions, it means either a faulty XREG itself, or incorrect decoding of the bus control bits of the T&C module. It is important that these errors be corrected before further diagnostics are run, because incorrect XREG contents may invalidate results in all subsequent tests. This error may indicate short circuits or faulty chips at any location along the DAB (digital audio bus). The ARU and FPC modules may be unplugged to be sure they do not contribute to this error. If the same error code is still given, the problem is probably with the transfer registers themselves (U38, U39, U40, and U41 on the DMEM module).

**E51 to E7F: ARU register test.** All four ARU registers are tested. The registers are composed of four 16-bit memory chips, with each chip organized into four rows of nibbles (4-bit quantities). The first row of chips 1, 2, 3, and 4 constitute the 16 bits of register 1, with chips 1 and 2 containing the higher-order byte of the register and chips 3 and 4 containing the lower-order byte. The second row of the four chips constitutes register 2, the third row register 3, and the fourth row register 4.

Error messages E51 to E5F indicate one or both of the chips comprising the lower-order byte of a register is faulty, E61 to E6F indicate a faulty chip or chips in the higher-order byte of a register, and E71 to E7F indicate chips in both bytes are faulty. The registers are identified by the least-significant hexadecimal digit of the error code. This represents an encoded nibble value. The positions of the bits in a logic 1 state in the binary representation of the nibble value indicate which registers are faulty. For example, the 5 in error code E51 represents a lower-order byte of a register and the 1 corresponds to a binary representation of 0001, indicating an error in register 1. The 9 in E59 corresponds to a binary code of 1001, indicating an error in registers 1 and 4; the 3 in E53 corresponds to 0011, indicating an error in registers 1 and 2; and the 4 in E54 corresponds to 0100, indicating an error in register 3, etc. The following chart shows an example. Incorrect bits within a register are displayed by the mode/register pushbutton LEDs.

#### ARU register decoding

| Error Message | Address Bytes | Binary Code of LSD | Register Number |
|---|---|---|---|
| E67 | high | 0111 | 1, 2, and 3 |
| E52 | low | 0010 | 2 |
| E69 | high | 1001 | 1 and 4 |
| E75 | high and low | 0101 | 1 and 3 |
| E7B | high and low | 1011 | 1, 2, and 4 |

To understand the significance of these diagnostics, examine the following conditions:

1. **The multiplier is OK, but the registers are faulty.**
   - a. If both high and low bytes are faulty, register addressing is probably invalid. This condition could result in an error in some registers and not in others.
   - b. If a register file chip is faulty, only one byte is affected, and only part of that byte. This may affect all addresses or just one. The data on the LEDs must be checked to determine which chip is actually faulty.
2. **The registers are OK, but the multiplier is faulty.** All file addresses are incorrect, and this may propagate errors to areas that are not faulty, so that just replacing the faulty chip does not correct the errors.

**E80 to E8F: Multiplier test.** The multiplier test is divided into four parts, each of which displays separate error codes. E81 to E83 indicate an error when the multiply coefficient is ±21/32. E81 indicates a low-order byte error, E82 a high-order byte error, and E83 indicates both bytes are incorrect. E85 to E87 indicate an error when multiplying by ±42/32. E89 to E8B indicate an error in the coefficient ±63/64. Four multiplications are made with each coefficient. The incorrect and correct data are displayed on the pushbutton LEDs in the same way as previous tests. If both the high-order and low-order bytes are incorrect, the data in the low-order byte is displayed. The last two coefficients should set the saturation monostable multivibrator. If not, error code E80 is displayed.

Note that E89 to E8B will test the intermediate address. Therefore, if E89 to E8B is displayed, check U13, U24 to U25, and U38 and U39.

**E91, E92, E95, and E96: data memory test.** This test makes two passes with complementary data. For this test to be valid, the multiplier must be operating correctly. Error message E91 indicates a low-order byte error and E92 indicates a high-order byte error. If both bytes are incorrect, E91 is displayed, which may mean that the entire memory is faulty, or it may mean that the multiplier or T&C module is faulty. The memory test is sensitive to both data errors and addressing errors, and should detect most problems. If either E91 or E92 are the only errors displayed and only a single LED indicates incorrect data, the problem is most likely to be a faulty memory chip, which is identified by the pushbutton LED. The defective memory chip can be swapped with the lowest-order memory chip (U1). This increases the noise level of the machine by 6 dB, but allows immediate operation if needed. For units with two banks of 16K dynamic RAMs, E91 and E92 refer to bank 1 (U20 to U35), and E95 and E96 refer to bank 2 (U1 to U16).

**EA0 to EB3: Additional Multiplier Test.** This test is performed when diagnostic program 4 (not available in V8.0) is called. Even error codes indicate a problem with the low byte and the odd error codes indicate a problem with the high byte. The error codes are grouped in fours; in any group, the first two groups use even test data and the second two use odd test data. EA0 to EA3 test a multiply by 1. EA4 to EA7 test a multiply by 1/2. EA8 to EAB test a multiply by −1. EAC to EAF test a multiply by 1/4. EB0 to EB3 test a multiply by 5/4.

If EA0 to EA3 all appear, the coefficients into the 74LS00 (U14, U26 to U28, U40 and U41, and U50 to U53) should be checked. If the high byte is bad with the bad data reading hexadecimal 80 or 7F, check the saturation logic (U42) or the MSB's of the data path through the ARU. If EA0 to EA3 appear, but EA4 to EA7 do not, check the 74LS00's or the intermediate adder (U13, U24, U25, U38, and U39). If EA0 to EA7 appear but EA8 to EAB do not, check the 74S86's (U5 to U9). EAC to EAF test the shift registers (U3, U4, and U15 to U18) and coefficients. EB0 to EB3 test the second adders (U19 to U23).

## 5.4 Maximum Delay (0.5-sec) Program

The 224X's maximum delay diagnostic program is stereo and can be used as an abbreviated machine test (or for setting output levels). This program can be called during normal operation by the key sequence CALL/SHIFT/PGM 2, or by pressing PGM 8 at the beginning of the power-up diagnostics. The nonadjustable delay provided by this program is approximately half a second. In this program, the left input is passed to outputs A and D; and the right input is passed to outputs B and C.

## 5.5 Zero Delay Program

The zero delay program is similar to the maximum delay program except that the DMEM module is not used and the delay is zero; that is, the analog inputs are immediately transmitted to the analog outputs. (The digitized signals still pass through the ARU module, however.) This program is called by pushing PGM 7 at the beginning of the power-up diagnostics. In this program, the left input is passed to outputs A and D; and the right input is passed to outputs B and C. The zero delay program is recommended for troubleshooting the analog circuitry and also for setting input and output levels.

## 5.6 Self-Test Mode

If operating difficulties arise, it is possible to determine proper operation of the AIN, AOUT, and FPC modules by performing a self-test. This test usually isolates problems in the analog conversion subsystem. To perform the self-test, loosen the DMEM, T&C, ARU, and NVS modules. When these modules are removed from the motherboard, a control signal (FPC DBUG) to the FPC module goes HIGH, initiating self-test mode. Do not remove the DMEM, T&C, ARU, and NVS modules when you loosen them; just free them from their edge connectors. If there is no response of any kind in self-test mode, check the power supplies and connections, as well as the clock on the SBC module. Then perform a stage-by-stage investigation from the AIN to the AOUT module to determine where the problem is.

The self-test allows the 224X analog and digitizing subsystems to operate without any intervention from the DSP. This mode digitizes analog information from the left input, and outputs the information to outputs A and B; the right channel input is passed to outputs C and D. Note that the signal routing is different than that in both the maximum delay and zero delay programs. This can sometimes help in determining which channel is bad in a malfunctioning AIN or AOUT module. For example, if the output B is bad in self-test but good in the zero delay program, then the left input channel is bad. If output B is bad in both self-test and zero delay program, then probably the B output channel is bad.

The digital sampling rate in the self-test is only 20 kHz. Therefore, when using the self-test, do NOT use input signals above 10 kHz. The self-test mode samples at only 20 kHz; therefore, it is meant for a preliminary check of the operation of the FPC, AIN, and AOUT modules. If measurements and calibrations are necessary, the zero delay program should be used. The self-test mode can also be exercised at the proper sampling rate of 34.13 kHz by removing the SBC module also and injecting a 3.413-MHz TTL level compatible clock from an external signal generator to pin A28 at the backplane connector for the SBC module. The self-test mode exercises about 95% of the circuitry in the AIN and AOUT modules and about 85% of the circuitry in the FPC module.

## 5.7 Signature Analysis

Because the digital signals on the digital modules in the 224X can be quite complex, signature analysis tables have been provided as a useful aid in tracing problems to a malfunctioning node.

Signature analysis is a technique used to troubleshoot electronic logic circuits. A signature analyzer (Hewlett Packard 5004A or equivalent) is connected to the unit being tested and the test program of the unit being tested is started. Long, complex data stream patterns are compressed into a unique 4-segment "signature" that the analyzer will display for each point in the unit being tested as the analyzer probe is moved from point to point. The analyzer requires several signals from the unit under test: the clock signal synchronizes the analyzer and the unit under test; the start and stop signals define the bounds between which the data signal is examined by the analyzer. After the stop signal, the analyzer displays the signature of the data it received. If the signature displayed does not match the corresponding signature given in the table, the circuitry connected to the node is malfunctioning.

The correct signatures for the various modules in the 224X are summarized in the signature tables that follow. The conditions for taking the signatures are listed with each module and setup. Figure 5.3 shows what some of the waveforms should look like.

> **Figure 5.3.** Converter Waveforms. These waveforms are observed with the unit in zero delay program. Input signal level is +12 dBm to the left input channel; input level potentiometer is set so that the level indicator is just beneath overload. Reference points: U21 pin 5, AIN board (AGR, output of input S/H), 1 kHz; U22 pin 4, AIN board (output of channel MUX), 1 kHz; U4 pin 6, AOUT board (output of output gain range amplifier), 1 kHz; U8 pin 1, AOUT board (output of output S/H), 1 kHz; U23 pin 6, AIN board (output of input gain range amplifier), 100 Hz; U12 pin 7, AIN board (output of gain range rectifier), 1 kHz; U2 pin 18, AOUT board (output of DAC), 100 Hz.

### Signature Tables

The original manual includes extensive node-by-node signature tables for the T&C, ARU, DMEM, and FPC modules (Version 8.2.1), giving the expected 4-character signature at each IC pin. These are reproduced in the appendix below. General setup conditions for each module:

**T&C — Version 8.2.1**
- SETUP: in Diagnostic Program 3 (ARU Signatures). Refer to Schematic #060-02475.
- NOTE: Blue control head should display E0A.
- START = RESET, U19 pin 9
- STOP = RESET, U19 pin 9
- CLOCK = DAB RSTB/, U20 pin 6
- +5V = FP54; GROUND = 0000

**ARU — Version 8.2.1 — no feedback**
- SETUP: Diagnostic Program 3 (ARU Signatures). Refer to Schematic #060-01318.
- NOTE: Blue control head should display E0A.
- START = RESET/, extender card pin 16
- STOP = XFERCK, U43 pin 11
- CLOCK = ARUCK, U10 pin 11
- +5V = 29F3; GROUND = 0000

**ARU — Version 8.2.1 (feedback configuration)**
- SETUP: Diagnostic Program 3 (ARU Signatures). Refer to Schematic #060-01318.
- NOTE: Blue control head should display E0A.
- START = RESET/, extender card pin 16
- STOP = RESET/, extender card pin 16
- CLOCK = ARUCK, U10 pin 11
- +5V = 3696; GROUND = 0000

**DMEM — Version 8.2.1**
- SETUP: Diagnostic Program 3 (ARU Signatures). Lift U65 pin 13 and jumper to U65 pin 1. Refer to Schematic #060-02512.
- NOTE: Blue control head should display E0A.
- START = MSB of CPC, U65 pin 8
- STOP = MSB of CPC, U65 pin 8
- CLOCK = RESET/, U58A pin 1
- +5V = 826P; GROUND = 0000

**FPC — Version 8.2.1**
- SETUP: Diagnostic Program 6 (FPC Signatures). Lift pin 11 of SAR IC (U26) on AIN module and jumper to +5V. Refer to Schematic #060-01320.
- NOTE: Blue control head should display E0F.
- START = RESET, U4 pin 2
- STOP = RESET, U4 pin 2
- CLOCK = FPCCLK, U4 pin 5
- +5V = 96F6; GROUND = 0000

### Signature Value Tables (Version 8.2.1)

In each block, columns are: `Pin  Signature`. The two pin columns reflect the DIP layout of the IC (e.g. pins 1–8 on the left, the opposite-side pins on the right). A dash (`-`) indicates a pin for which no signature is listed in the original manual.

#### T&C Module — Version 8.2.1

```
U1   1  -      16  FP54        U2   1  0000   24  FP54
     2  -      15  -                2  07P6   23  45FF
     3  -      14  3U9F             3  FP4C   22  F344
     4  -      13  0000             4  03UA   21  95CP
     5  -      12  0000             5  3U9U   20  A36H
     6  -      11  -                6  F5AA   19  3U9F
     7  FP54   10  40A5             7  A0A8   18  0000
     8  0000    9  FP54             8  53PH   17  0000
                                    9  028H   16  FP54
                                   10  -      15  0000
                                   11  0000   14  0000
                                   12  0000   13  -

U3   1  07P6   20  FP54        U4   1  FP54   16  FP54
     2  FP4C   19  -                2  -      15  -
     3  03UA   18  -                3  07P6   14  03U3
     4  3U9U   17  -                4  FP4C   13  6725
     5  F5AA   16  -                5  03UA   12  01UH
     6  A0A8   15  -                6  3U9U   11  1UFU
     7  53PH   14  -                7  0000   10  0000
     8  028H   13  -                8  0000    9  0000
     9  FP54   12  -
    10  00U0   11  FP54

U5   1  FP54   16  FP54        U10  1  FP54   16  FP54
     2  -      15  -                2  -      15  -
     3  F5AA   14  P2H5             3  -      14  -
     4  A0A8   13  H054             4  1UFU   13  8146
     5  53PH   12  29U6             5  H054   12  -
     6  028H   11  8146             6  8146   11  F1C3
     7  0000   10  0000             7  8146   10  -
     8  0000    9  0000             8  0000    9  -

U11  1  FP54   16  FP54        U14  1  -      16  FP54
     2  -      15  -                2  -      15  -
     3  -      14  -                3  -      14  45FF
     4  01UH   13  29U6             4  -      13  F344
     5  P2H5   12  -                5  -      12  95CP
     6  2PU6   11  FPAA             6  -      11  A36H
     7  29U6   10  -                7  FP54   10  FP54
     8  0000    9  -                8  0000    9  FP54

U15  1  0000   24  FP54        U16  1  C5A9   20  FP54
     2  C5A9   23  45FF             2  909P   19  -
     3  909P   22  F344             3  0000   18  -
     4  0000   21  95CP             4  0000   17  -
     5  0000   20  A36H             5  8C99   16  -
     6  8C99   19  3U9F             6  0H10   15  -
     7  0H10   18  0000             7  0000   14  -
     8  0000   17  0000             8  7302   13  -
     9  7302   16  FP54             9  FP54   12  -
    10  -      15  0000            10  0000   11  FP54
    11  0000   14  0000
    12  0000   13  -

U17  1  FP54   16  FP54        U18  1  FP54   16  FP54
     2  -      15  -                2  -      15  -
     3  C5A9   14  U3AA             3  8C99   14  PFC2
     4  909P   13  484U             4  0H10   13  2UU6
     5  0000   12  0000             5  0000   12  0000
     6  0000   11  0000             6  7302   11  3981
     7  0000   10  0000             7  0000   10  0000
     8  0000    9  0000             8  0000    9  0000

U19  1  -      20  FP54        U20  1  -      16  FP54
     2  0000   19  FP54             2  -      15  -
     3  0000   18  FP54             3  -      14  FP54
     4  PFC2   17  6725             4  -      13  -
     5  PFC2   16  6725             5  -      12  -
     6  2UU6   15  03U3             6  -      11  -
     7  2UU6   14  03U3             7  -      10  FP54
     8  FP54   13  3981             8  0000    9  9FF0
     9  672A   12  3981
    10  0000   11  -

U28  1  FP54   16  FP54        U29  1  0000   24  FP54
     2  -      15  0000             2  4496   23  45FF
     3  3U9F   14  -                3  P265   22  F344
     4  3U9F   13  -                4  2P14   21  95CP
     5  -      12  -                5  F71H   20  A36H
     6  0000   11  -                6  C10H   19  3U9F
     7  0000   10  0000             7  A80H   18  0000
     8  0000    9  0000             8  CA09   17  0000
                                    9  909P   16  FP54
                                   10  -      15  0000
                                   11  0000   14  0000
                                   12  0000   13  -

U30  1  4496   20  FP54        U31  1  0000   20  FP54
     2  P265   19  -                2  7132   19  A24C
     3  2P14   18  -                3  P265   18  4496
     4  F71H   17  -                4  F71H   17  2P14
     5  C10H   16  -                5  638P   16  970A
     6  A80H   15  -                6  H406   15  71U8
     7  CA09   14  -                7  A80H   14  C10H
     8  909P   13  -                8  909P   13  CA09
     9  FP54   12  -                9  484U   12  HH04
    10  0000   11  FP54            10  0000   11  -

U32  1  A24C   14  FP54        U33  1  -      14  FP54
     2  A24C   13  7132             2  -      13  -
     3  A24C   12  7132             3  484U   12  -
     4  970A   11  7132             4  861C   11  -
     5  970A   10  638P             5  -      10  -
     6  970A    9  638P             6  -       9  -
     7  0000    8  638P             7  0000    8  -

U34  1  861C   14  FP54        U42  1  FP54   16  FP54
     2  830C   13  3981             2  -      15  0000
     3  0000   12  -                3  45FF   14  -
     4  861C   11  -                4  45FF   13  A36H
     5  HH05   10  U7H5             5  -      12  A36H
     6  0001    9  -                6  F344   11  -
     7  0000    8  -                7  F344   10  95CP
                                    8  0000    9  95CP

U43  1  0000   24  FP54        U44  1  0616   20  FP54
     2  0616   23  45FF             2  7P28   19  -
     3  7P28   22  F344             3  F237   18  -
     4  F237   21  95CP             4  CA0C   17  -
     5  CA0C   20  A36H             5  0616   16  -
     6  0616   19  3U9F             6  7P28   15  -
     7  7P28   18  0000             7  F184   14  -
     8  F184   17  0000             8  1C45   13  -
     9  1C45   16  FP54             9  FP54   12  -
    10  -      15  0000            10  0000   11  FP54
    11  0000   14  0000
    12  0000   13  -

U45  1  0000   20  FP54        U46  1  FP54   16  FP54
     2  3U14   19  830C             2  FP54   15  -
     3  7P28   18  0616             3  -      14  FP54
     4  CA0C   17  F237             4  FP54   13  -
     5  HH05   16  611C             5  FP54   12  FP54
     6  3U14   15  830C             6  FP54   11  FP54
     7  7P28   14  0616             7  FP54   10  FP54
     8  1C45   13  F184             8  0000    9  FP54
     9  8HA2   12  F9CF
    10  0000   11  -

U47  1  0000   16  FP54        U48  1  U3AA   14  FP54
     2  U3AA   15  -                2  -      13  -
     3  484U   14  71U8             3  -      12  6725
     4  -      13  H406             4  861C   11  -
     5  484U   12  -                5  -      10  -
     6  U3AA   11  -                6  -       9  -
     7  CCP5   10  -                7  0000    8  -
     8  0000    9  -

U49  1  -      14  FP54
     2  861C   13  F9CF
     3  3U14   12  -
     4  861C   11  861C
     5  -      10  FP54
     6  -       9  8HA2
     7  0000    8  55C6
```

#### ARU Module — Version 8.2.1 — no feedback

```
U2   1  -      14  29F3        U3   1  29F3   16  29F3
     2  -      13  C356             2  F494   15  C77H
     3  -      12  9A95             3  0000   14  0C0P
     4  -      11  C356             4  0000   13  -
     5  9A95   10  9A95             5  -      12  -
     6  C356    9  C8P7             6  -      11  0000
     7  0000    8  9124             7  -      10  8FC4
                                    8  0000    9  29F3

U4   1  29F3   16  29F3        U5   1  3H61   14  29F3
     2  U69F   15  8575             2  9A95   13  9A95
     3  46PU   14  8653             3  A7U4   12  P600
     4  0000   13  -                4  9A4H   11  7F95
     5  -      12  -                5  9A95   10  9A95
     6  -      11  0000             6  00H8    9  5779
     7  -      10  8FC4             7  0000    8  FHPF
     8  0000    9  29F3

U6   1  91A4   14  29F3        U7   1  697U   14  29F3
     2  9A95   13  9A95             2  9A95   13  9A95
     3  0C31   12  CU83             3  U3PA   12  PHC1
     4  HF27   11  2516             4  7U69   11  7724
     5  9A95   10  9A95             5  9A95   10  9A95
     6  46C2    9  0AU0             6  P5UF    9  5FF8
     7  0000    8  9065             7  0000    8  F65H

U8   1  9A15   14  29F3        U9   1  A175   14  29F3
     2  9A95   13  9A95             2  9A95   13  9A95
     3  0080   12  4070             3  3CP0   12  2272
     4  H39H   11  HAP5             4  6750   11  C8P7
     5  9A95   10  9A95             5  9A95   10  9A95
     6  4908    9  8441             6  UHF5    9  2272
     7  0000    8  1PH4             7  0000    8  C8P7

U10  1  0000   20  29F3        U11  1  0000   20  29F3
     2  2272   19  9A15             2  PHC1   19  91A4
     3  3PA1   18  4P6P             3  A127   18  590F
     4  3PA1   17  HH7P             4  F3H4   17  F20A
     5  2272   16  H39H             5  5FF8   16  HF27
     6  6750   15  8441             6  7U69   15  0AU0
     7  C4P4   14  72F6             7  8497   14  6UA4
     8  38AU   13  UAA5             8  A8CC   13  0543
     9  A175   12  4070             9  697U   12  CU83
    10  0000   11  0000            10  0000   11  0000

U12  1  29F3   16  29F3        U13  1  4PHU   16  29F3
     2  P600   15  3H61             2  4CU5   15  8595
     3  -      14  -                3  2FP9   14  78P0
     4  C645   13  0087             4  0087   13  H4C6
     5  H4C6   12  4PHU             5  0097   12  A6FH
     6  -      11  -                6  29H3   11  3F61
     7  5779   10  9A4H             7  29F3   10  C645
     8  0000    9  0000             8  0000    9  2FP9

U14  1  8575   14  29F3        U15  1  29F3   16  29F3
     2  90U2   13  90U2             2  4FF4   15  4FF4
     3  78P0   12  C77H             3  3312   14  0U19
     4  F494   11  2FP9             4  8244   13  57U8
     5  90U2   10  90U2             5  PH68   12  6U15
     6  A6FH    9  8653             6  C156   11  0000
     7  0000    8  0097             7  -      10  8FC4
                                    8  0000    9  29F3

U16  1  29F3   16  29F3        U17  1  29F3   16  29F3
     2  4FF4   15  4FF4             2  UF7F   15  UCC9
     3  3312   14  35FC             3  3312   14  3PF5
     4  5F3P   13  75F4             4  5F3P   13  A574
     5  AC87   12  UF7F             5  9895   12  F494
     6  U7C9   11  0000             6  F4AC   11  0000
     7  -      10  8FC4             7  -      10  8FC4
     8  0000    9  29F3             8  0000    9  29F3

U18  1  29F3   16  29F3        U19  1  6A6H   16  29F3
     2  6U15   15  F9C1             2  00H8   15  FHPF
     3  75UH   14  0FFH             3  H9P3   14  U0U6
     4  1AH1   13  977F             4  1PU7   13  8P4F
     5  HP7A   12  U69F             5  0A55   12  HUPH
     6  8244   11  0000             6  A7U4   11  7F95
     7  -      10  8FC4             7  C356   10  7A3U
     8  0000    9  29F3             8  0000    9  3P92

U20  1  2161   16  29F3        U21  1  HCUP   16  29F3
     2  46C2   15  9065             2  P5UF   15  F65H
     3  5941   14  CA1P             3  5938   14  44PA
     4  7819   13  P813             4  94F5   13  CA12
     5  4HCA   12  6HA3             5  A547   12  9152
     6  0C31   11  2516             6  U3PA   11  7724
     7  3P92   10  8AHH             7  F268   10  HPH3
     8  0000    9  F268             8  0000    9  38A5

U22  1  6P49   16  29F3        U23  1  F2A5   16  29F3
     2  4908   15  1PH4             2  UHF5   15  C8P7
     3  1UP4   14  7H7H             3  07F5   14  H491
     4  313U   13  5C0F             4  97CF   13  54H3
     5  091A   12  85A6             5  94U9   12  H491
     6  0080   11  HAP5             6  3CP0   11  C8P7
     7  38A5   10  67P6             7  38A5   10  54H3
     8  0000    9  38A5             8  0000    9  -

U24  1  C4P4   16  29F3        U25  1  8497   16  29F3
     2  0CHA   15  819U             2  3P83   15  2HF9
     3  9PP9   14  9PP9             3  9CF3   14  FUFA
     4  38AU   13  3PA1             4  A8CC   13  F3H4
     5  9321   12  9PP9             5  4380   12  11P7
     6  8767   11  819U             6  8777   11  943H
     7  2FP9   10  3PA1             7  6F4F   10  A127
     8  0000    9  -                8  0000    9  24UH

U26  1  F9C1   14  29F3        U27  1  0FFH   14  29F3
     2  90U2   13  90U2             2  4471   13  4471
     3  FUFA   12  UCC9             3  3P83   12  F9C1
     4  0FFH   11  9CF3             4  UCC9   11  943H
     5  90U2   10  90U2             5  4471   10  4471
     6  4380    9  UF7F             6  2HF9    9  3PF5
     7  0000    8  11P7             7  0000    8  8777

U28  1  8575   14  29F3        U29  1  -      16  29F3
     2  4471   13  4471             2  -      15  -
     3  3F61   12  0C0P             3  -      14  29F3
     4  8653   11  29H3             4  U7C9   13  29F3
     5  4471   10  4471             5  AC87   12  29F3
     6  4CU5    9  C77H             6  PH68   11  0000
     7  0000    8  8595             7  5F3P   10  3312
                                    8  0000    9  8244

U30  1  -      16  29F3        U31  1  -      16  29F3
     2  -      15  -                2  -      15  -
     3  -      14  29F3             3  -      14  29F3
     4  U7C9   13  29F3             4  U7C9   13  29F3
     5  AC87   12  29F3             5  AC87   12  29F3
     6  75UH   11  0000             6  HP7A   11  0000
     7  U7C9   10  AC87             7  5F3P   10  3312
     8  0000    9  C156             8  0000    9  1AH1

U32  1  -      16  29F3        U33  1  0000   16  29F3
     2  -      15  -                2  1PU7   15  0000
     3  -      14  29F3             3  9124   14  7A3U
     4  U7C9   13  29F3             4  1PU7   13  9124
     5  AC87   12  29F3             5  6A6H   12  7A3U
     6  46PU   11  0000             6  9124   11  8P4F
     7  F4AC   10  9895             7  6A6H   10  9124
     8  0000    9  8244             8  0000    9  8P4F

U34  1  0000   16  29F3        U35  1  0000   16  29F3
     2  7819   15  0000             2  94F5   15  0000
     3  9124   14  8AHH             3  9124   14  HPH3
     4  7819   13  9124             4  94F5   13  9124
     5  2161   12  8AHH             5  HCUP   12  HPH3
     6  9124   11  P813             6  9124   11  CA12
     7  2161   10  9124             7  HCUP   10  9124
     8  0000    9  P813             8  0000    9  CA12

U36  1  0000   16  29F3        U37  1  0000   16  29F3
     2  313U   15  0000             2  97CF   15  0000
     3  9124   14  67P6             3  9124   14  54H3
     4  313U   13  9124             4  97CF   13  C8P7
     5  6P49   12  67P6             5  F2A5   12  54H3
     6  9124   11  5C0F             6  9124   11  54H3
     7  6P49   10  9124             7  F2A5   10  C8P7
     8  0000    9  5C0F             8  0000    9  54H3

U38  1  HH7P   16  29F3        U39  1  F20A   16  29F3
     2  968C   15  2H9U             2  3PH5   15  F772
     3  2A87   14  3P2C             3  95C9   14  F1CU
     4  4P6P   13  72F6             4  590F   13  6UA4
     5  45PP   12  1789             5  U2F4   12  1789
     6  2U7H   11  8160             6  8721   11  7P86
     7  24UH   10  UAA5             7  2FP9   10  0543
     8  0000    9  2FP9             8  0000    9  6F4F

U40  1  U69F   14  29F3        U41  1  977F   14  29F3
     2  4471   13  4471             2  90U2   13  90U2
     3  3PH5   12  A574             3  F1C0   12  A574
     4  977F   11  F772             4  3PF5   11  95C9
     5  4471   10  4471             5  90U2   10  90U2
     6  7P86    9  F494             6  1789    9  U69F
     7  0000    8  8721             7  0000    8  U2F4

U42  1  54H3   14  29F3        U43  1  2839   20  29F3
     2  54H3   13  -                2  -      19  -
     3  0000   12  -                3  97CF   18  6P49
     4  -      11  -                4  67P6   17  5C0F
     5  -      10  29F3             5  -      16  -
     6  -       9  29F3             6  -      15  -
     7  0000    8  0000             7  54H3   14  HPH3
                                    8  F2A5   13  313U
                                    9  -      12  -
                                   10  0000   11  -

U44  1  2839   20  29F3        U45  1  3108   16  29F3
     2  -      19  -                2  0000   15  -
     3  94F5   18  2161             3  7A3U   14  HUPH
     4  8AHH   17  P813             4  8P4F   13  U0U6
     5  -      16  -                5  6A6H   12  H9P3
     6  -      15  -                6  1PU7   11  0A55
     7  CA12   14  7A3U             7  0000   10  0000
     8  HCUP   13  7819             8  0000    9  0000
     9  -      12  -
    10  0000   11  -

U46  1  3108   16  29F3        U47  1  3108   16  29F3
     2  0000   15  -                2  0000   15  -
     3  8AHH   14  6HA3             3  HPH3   14  9152
     4  P813   13  CA1P             4  CA12   13  44PA
     5  2161   12  5941             5  HCUP   12  5938
     6  7819   11  4HCA             6  94F5   11  A547
     7  0000   10  0000             7  0000   10  0000
     8  0000    9  0000             8  0000    9  0000

U48  1  3108   16  29F3        U49  1  3108   16  29F3
     2  0000   15  -                2  0000   15  -
     3  67P6   14  85A6             3  54H3   14  H491
     4  5C0F   13  7H7H             4  54H3   13  H491
     5  6P49   12  1UP4             5  F2A5   12  07F5
     6  313U   11  091A             6  97CF   11  94U9
     7  0000   10  0000             7  0000   10  0000
     8  0000    9  0000             8  0000    9  0000

U50  1  UF7F   14  29F3        U51  1  6U15   14  29F3
     2  4471   13  4471             2  90U2   13  90U2
     3  2U7H   12  57U8             3  45PP   12  33FC
     4  6U15   11  8160             4  75F4   11  1789
     5  4471   10  4471             5  90U2   10  90U2
     6  968C    9  75F4             6  2A87    9  57U8
     7  0000    8  2H9U             7  0000    8  3P2C

U52  1  0U19   14  29F3        U53  1  0U19   14  29F3
     2  4471   13  4471             2  90U2   13  90U2
     3  0CHA   12  35FC             3  9321   12  4FF4
     4  4FF4   11  8767             4  4FF4   11  9PP9
     5  4471   10  4471             5  90U2   10  90U2
     6  819U    9  4FF4             6  9PP9    9  4FF4
     7  0000    8  819U             7  0000    8  9PP9

U54  1  HP7A   14  29F3
     2  U7C9   13  C931
     3  0000   12  90U2
     4  29F3   11  6HC2
     5  8244   10  4471
     6  AC87    9  0000
     7  0000    8  29F3
```

#### ARU Module — Version 8.2.1 (feedback configuration)

```
U2   1  -      14  3696        U3   1  3696   16  3696
     2  -      13  U804             2  9C33   15  8P47
     3  -      12  FP92             3  0000   14  U8A9
     4  -      11  U804             4  0000   13  -
     5  FP92   10  FP92             5  -      12  -
     6  U804    9  3P2U             6  -      11  0000
     7  0000    8  08C9             7  -      10  4573
                                    8  0000    9  3696

U4   1  3696   16  3696        U5   1  85U0   14  3696
     2  343H   15  2149             2  FP92   13  FP92
     3  50U5   14  5465             3  4C62   12  HFUF
     4  0000   13  -                4  H10A   11  126P
     5  -      12  -                5  FP92   10  FP92
     6  -      11  0000             6  1U98    9  0HP6
     7  -      10  4573             7  0000    8  F374
     8  0000    9  3696

U6   1  H827   14  3696        U7   1  4808   14  3696
     2  FP92   13  FP92             2  FP92   13  FP92
     3  16C5   12  5C3U             3  869A   12  3A87
     4  876U   11  95AH             4  UP8C   11  U415
     5  FP92   10  FP92             5  FP92   10  FP92
     6  49UH    9  162P             6  3019    9  FCFH
     7  0000    8  H8CF             7  0000    8  055U

U8   1  361P   14  3696        U9   1  C7C3   14  3696
     2  FP92   13  FP92             2  FP92   13  FP92
     3  U88F   12  H021             3  7921   12  U0CH
     4  A1P2   11  1PC3             4  6U12   11  3P2U
     5  FP92   10  FP92             5  FP92   10  FP92
     6  6U70    9  3077             6  A180    9  U0CH
     7  0000    8  UPP5             7  0000    8  3P2U

U10  1  0000   20  3696        U11  1  0000   20  3696
     2  U0CH   19  361P             2  3A87   19  H827
     3  CAF1   18  3786             3  2PC5   18  PCU4
     4  CAF1   17  187U             4  FF20   17  5565
     5  U0CH   16  A1P2             5  FCFH   16  876U
     6  6U12   15  3077             6  UP8C   15  162P
     7  859P   14  3C55             7  A6AF   14  77P6
     8  34HF   13  UCU9             8  FCAC   13  PHF4
     9  C7C3   12  H021             9  4808   12  5C3U
    10  0000   11  0000            10  0000   11  0000

U12  1  3696   16  3696        U13  1  U9AP   16  3696
     2  HFUF   15  85U0             2  U903   15  6FF1
     3  -      14  -                3  1P6H   14  3276
     4  P243   13  505C             4  505C   13  4077
     5  4077   12  U9AP             5  33UP   12  3P50
     6  -      11  -                6  5533   11  F27P
     7  0HP6   10  H10A             7  3696   10  P243
     8  0000    9  0000             8  0000    9  1P6H

U14  1  2149   14  3696        U15  1  3696   16  3696
     2  86CP   13  86CP             2  0UAH   15  0UAH
     3  3276   12  8P47             3  3PC5   14  5140
     4  9C33   11  1P6H             4  UH8F   13  HU4H
     5  86CP   10  86CP             5  9CPU   12  2C67
     6  3P50    9  5465             6  F339   11  0000
     7  0000    8  33UP             7  -      10  4573
                                    8  0000    9  3696

U16  1  3696   16  3696        U17  1  3696   16  3696
     2  0UAH   15  0UAH             2  UC7F   15  81PA
     3  3PC5   14  APH6             3  3PC5   14  567U
     4  58H6   13  2344             4  58H6   13  9FFP
     5  FC1A   12  UC7F             5  U5AU   12  9C33
     6  93FF   11  0000             6  AH79   11  0000
     7  -      10  4573             7  -      10  4573
     8  0000    9  3696             8  0000    9  3696

U18  1  3696   16  3696        U19  1  2A65   16  3696
     2  2C67   15  2PP4             2  1U98   15  F374
     3  6P40   14  U971             3  60CU   14  09U9
     4  0823   13  33F0             4  P885   13  9AH7
     5  A55A   12  343H             5  5CP3   12  34P3
     6  UH8F   11  0000             6  4C62   11  126P
     7  -      10  4573             7  U804   10  F5F1
     8  0000    9  3696             8  0000    9  F7P1

U20  1  U9U2   16  3696        U21  1  PHPF   16  3696
     2  49UH   15  H8CF             2  3019   15  055U
     3  4815   14  6A06             3  0H92   14  8U4F
     4  9136   13  P978             4  PC08   13  P9P4
     5  4062   12  011F             5  2999   12  CA59
     6  16C5   11  95AH             6  869A   11  U415
     7  F7P1   10  U058             7  440C   10  12U0
     8  0000    9  440C             8  0000    9  5F4F

U22  1  411A   16  3696        U23  1  6665   16  3696
     2  6U70   15  UPP5             2  A180   15  3P2U
     3  4U40   14  2U18             3  4FF8   14  P1UC
     4  CHH8   13  C5PH             4  0HH7   13  77AH
     5  1918   12  1126             5  8PH4   12  P1UC
     6  U88F   11  1PC3             6  7921   11  3P2U
     7  5F4F   10  5064             7  UA22   10  77A3
     8  0000    9  UA22             8  0000    9  -

U24  1  859P   16  3696        U25  1  A6AF   16  3696
     2  6P1P   15  5141             2  4H81   15  0C16
     3  P500   14  P500             3  FHUC   14  P1P0
     4  34HF   13  CAF1             4  FCAC   13  FF20
     5  PU81   12  P500             5  C6PH   12  AH67
     6  809C   11  5141             6  P33P   11  A5A9
     7  5CF6   10  CAF1             7  9P78   10  2PC5
     8  0000    9  -                8  0000    9  267C

U26  1  2PP4   14  3696        U27  1  U971   14  3696
     2  86CP   13  86CP             2  0205   13  0205
     3  P1P0   12  81PA             3  4H81   12  2PP4
     4  U971   11  FHUC             4  81PA   11  A5A9
     5  86CP   10  86CP             5  0205   10  0205
     6  C6PH    9  UC7F             6  0C16    9  567U
     7  0000    8  AH67             7  0000    8  P33P

U28  1  2149   14  3696        U33  1  000P   16  3696
     2  0205   13  0205             2  P885   15  0000
     3  F27P   12  U8A9             3  08C9   14  F5F1
     4  5465   11  5533             4  P885   13  08C9
     5  0205   10  0205             5  2A65   12  F5F1
     6  U903    9  8P47             6  08C9   11  9AH7
     7  0000    8  6FF1             7  2A6H   10  08C9
                                    8  0000    9  9AHU

U34  1  000P   16  3696        U35  1  000P   16  3696
     2  9136   15  0000             2  PC08   15  0000
     3  08C9   14  U058             3  08C9   14  12U0
     4  9136   13  08C9             4  PC02   13  08C9
     5  U9U2   12  U05P             5  PHPF   12  12UF
     6  08C9   11  P978             6  08C9   11  P9P4
     7  U9U0   10  08C9             7  PHPA   10  08C9
     8  0000    9  P978             8  0000    9  P9PA

U36  1  000P   16  3696        U37  1  000P   16  3696
     2  CHH8   15  0000             2  0HH7   15  0000
     3  08C9   14  5064             3  08C9   14  77A3
     4  CHHP   13  08C9             4  0HHH   13  3P2U
     5  411A   12  5062             5  6665   12  77A3
     6  08C9   11  C5PH             6  08C9   11  77AH
     7  4110   10  08C9             7  666C   10  3P2U
     8  0000    9  C5P9             8  0000    9  77A3

U38  1  187U   16  3696        U39  1  5565   16  3696
     2  9740   15  1A74             2  496H   15  47U5
     3  29UF   14  82P8             3  F27F   14  PP67
     4  3786   13  3C55             4  PCU4   13  77P6
     5  8476   12  C2A0             5  124C   12  9AU6
     6  958C   11  H721             6  P7H2   11  P94A
     7  267C   10  UCU9             7  1P6H   10  PHF4
     8  0000    9  5CF6             8  0000    9  9P78

U40  1  343H   14  3696        U41  1  33F0   14  3696
     2  0205   13  0205             2  86CP   13  86CP
     3  496H   12  9FFP             3  PP67   12  9FFP
     4  33F0   11  47U5             4  567U   11  F27F
     5  0205   10  0205             5  86CP   10  86CP
     6  P94A    9  9C33             6  9AU6    9  343H
     7  0000    8  P7H2             7  0000    8  124C

U42  1  77A3   14  3696        U43  1  25C5   20  3696
     2  77AH   13  -                2  -      19  -
     3  000P   12  -                3  0HHH   18  4110
     4  -      11  -                4  5062   17  C5P9
     5  -      10  3696             5  -      16  -
     6  -       9  3696             6  -      15  -
     7  -       8  0000             7  77A3   14  12UF
                                    8  666C   13  CHHP
                                    9  -      12  -
                                   10  0000   11  -

U44  1  25C5   20  3696        U45  1  8658   16  3696
     2  -      19  -                2  0000   15  -
     3  PC02   18  U9U0             3  F5F1   14  34P3
     4  U05P   17  P978             4  9AHU   13  09U9
     5  -      16  -                5  2A6H   12  60CU
     6  -      15  -                6  P885   11  5CP3
     7  P9PA   14  F5F1             7  0000   10  0000
     8  PHPA   13  9136             8  0000    9  0000
     9  -      12  -
    10  0000   11  -

U46  1  8658   16  3696        U47  1  8658   16  3696
     2  0000   15  -                2  0000   15  -
     3  U05P   14  011F             3  12UF   14  CA59
     4  P978   13  6A06             4  P9PA   13  8U4F
     5  U9U0   12  4815             5  PHPA   12  0H92
     6  9136   11  4062             6  PC02   11  2999
     7  0000   10  0000             7  0000   10  0000
     8  0000    9  0000             8  0000    9  0000

U48  1  8658   16  3696        U49  1  8658   16  3696
     2  0000   15  -                2  0000   15  -
     3  5062   14  1126             3  77A3   14  P1UC
     4  C5P9   13  2U18             4  77A3   13  P1UC
     5  4110   12  4U40             5  666C   12  4FF8
     6  CHHP   11  1918             6  0HHH   11  8PH4
     7  0000   10  0000             7  0000   10  0000
     8  0000    9  0000             8  0000    9  0000

U50  1  UC7F   14  3696        U51  1  2C67   14  3696
     2  0205   13  0205             2  86CP   13  86CP
     3  958C   12  HU4H             3  8476   12  APH6
     4  2C67   11  H721             4  2344   11  C2A0
     5  0205   10  0205             5  86CP   10  86CP
     6  9740    9  2344             6  29UF    9  HU4H
     7  0000    8  1A74             7  0000    8  82P8

U52  1  5140   14  3696        U53  1  5140   14  3696
     2  0205   13  0205             2  86CP   13  86CP
     3  6P1P   12  APH6             3  PU81   12  0UAH
     4  0UAH   11  809C             4  0UAH   11  P500
     5  0205   10  0205             5  86CP   10  86CP
     6  5141    9  0UAH             6  P500    9  0UAH
     7  0000    8  5141             7  0000    8  P500

U54  1  A55A   14  3696
     2  93FF   13  C028
     3  0000   12  86CP
     4  3696   11  3493
     5  UH8F   10  0205
     6  FC1A    9  0000
     7  0000    8  3696
```

#### DMEM Module — Version 8.2.1

ICs U1–U16 and U20–U35 share a common signature pattern (shown together below), followed by individually listed ICs.

```
U1–U16,       1  -      16  0000   U17  1  -      16  -
U20–U35       2  -      15  -            2  0AU1   15  0AU1
(common)      3  -      14  -            3  A6F7   14  A6F7
              4  -      13  0AU1         4  UH56   13  UH56
              5  UH56   12  A6F7         5  FU8U   12  FU8U
              6  P279   11  FU8U         6  P279   11  P279
              7  861U   10  44U7         7  44U7   10  44U7
              8  -       9  -            8  861U    9  861U

U18  1  0000   16  826P        U36  1  0000   16  826P
     2  FU8U   15  0000             2  UH56   15  0000
     3  1F7P   14  8HU0             3  UF4C   14  A6F7
     4  FU8U   13  9237             4  UH56   13  6266
     5  44U7   12  -                5  861U   12  A6F7
     6  6633   11  -                6  5439   11  P279
     7  44U7   10  74P1             7  861U   10  440H
     8  0000    9  0AU1             8  0000    9  P279

U48  1  826P   20  826P        U49  1  5439   16  826P
     2  826P   19  826P             2  0000   15  0000
     3  -      18  -                3  2A1F   14  A206
     4  0000   17  0000             4  UF4C   13  440H
     5  -      16  -                5  7P25   12  C133
     6  0000   15  0000             6  0000   11  0000
     7  -      14  -                7  826P   10  6266
     8  0000   13  0000             8  0000    9  9241
     9  -      12  -
    10  0000   11  0000

U50  1  6633   16  826P        U51  1  -      14  826P
     2  0000   15  826P             2  0000   13  C133
     3  3319   14  7C47             3  7P25   12  0000
     4  1F7P   13  74P1             4  2A1F   11  8P3U
     5  8P3U   12  C25F             5  A206   10  3319
     6  0000   11  0000             6  C133    9  7C47
     7  9241   10  9237             7  0000    8  C25F
     8  0000    9  A077

U62  1  826P   20  826P        U63  1  861U   16  826P
     2  0000   19  826P             2  0000   15  0000
     3  -      18  -                3  19H6   14  HP66
     4  0000   17  826P             4  UH56   13  P279
     5  -      16  -                5  5H21   12  U81P
     6  0000   15  0000             6  0000   11  0000
     7  -      14  -                7  A077   10  A6F7
     8  0000   13  0000             8  0000    9  10F0
     9  -      12  -
    10  0000   11  0000

U64  1  44U7   16  826P        U65  1  C25F   14  826P
     2  0000   15  0000             2  0000   13  C25F
     3  19H6   14  HP66             3  5H21   12  0000
     4  FU8U   13  0AU1             4  0000   11  5H21
     5  5H21   12  U81P             5  HP66   10  19H6
     6  826P   11  0000             6  U81P    9  HP66
     7  10F0   10  8HU0             7  0000    8  U81P
     8  0000    9  FPHA
```

#### FPC Module — Version 8.2.1

```
U1   1  96F6   16  96F6        U2   1  96F6   16  96F6
     2  0000   15  -                2  0000   15  80F0
     3  0000   14  1686             3  0000   14  -
     4  96F6   13  388A             4  96F6   13  H48C
     5  0000   12  AP4F             5  0000   12  -
     6  0000   11  -                6  96F6   11  -
     7  80F0   10  80F0             7  96F6   10  388A
     8  0000    9  C869             8  0000    9  C869

U3   1  96F6   16  96F6        U4   1  0000   16  96F6
     2  -      15  96F6             2  4C63   15  0000
     3  5151   14  AP4F             3  96F6   14  5151
     4  0000   13  UC7P             4  4C63   13  H30A
     5  96F6   12  0000             5  0000   12  5151
     6  -      11  96F6             6  -      11  96F6
     7  -      10  5F99             7  0000   10  H30A
     8  0000    9  -                8  0000    9  96F6

U5   1  AU07   14  96F6        U6   1  AU07   16  96F6
     2  P11U   13  1H0P             2  P11U   15  0000
     3  -      12  96F6             3  1H0P   14  0000
     4  1C7C   11  -                4  1358   13  0000
     5  CHC5   10  -                5  1C7C   12  38UP
     6  96F6    9  2712             6  CHC5   11  7FU6
     7  0000    8  H30A             7  26HC   10  72A7
                                    8  0000    9  6HU5

U7   1  4C63   16  96F6        U8   1  4C63   16  96F6
     2  0000   15  0000             2  0000   15  2712
     3  -      14  1H0P             3  -      14  1C7C
     4  -      13  P11U             4  -      13  CHC5
     5  -      12  AU07             5  -      12  26HC
     6  -      11  0000             6  -      11  1358
     7  96F6   10  2712             7  96F6   10  96F6
     8  -       9  96F6             8  -       9  -

U12  1  0000   14  96F6        U13  1  -      14  96F6
     2  -      13  1686             2  -      13  -
     3  96F6   12  H48C             3  -      12  -
     4  -      11  UC7P             4  -      11  -
     5  -      10  87H6             5  -      10  1A65
     6  -       9  C869             6  -       9  4325
     7  0000    8  3UCU             7  0000    8  5940

U14  1  -      14  96F6        U15  1  0000   14  96F6
     2  -      13  2PAU             2  -      13  -
     3  C869   12  -                3  5151   12  -
     4  1110   11  388A             4  -      11  1110
     5  HP96   10  -                5  -      10  87H6
     6  5940    9  -                6  -       9  2PAU
     7  0000    8  -                7  0000    8  C869

U16  1  96F6   16  96F6        U17  1  AU07   14  96F6
     2  0000   15  -                2  -      13  P11U
     3  96F6   14  -                3  -      12  77H9
     4  96F6   13  -                4  -      11  -
     5  96F6   12  36UA             5  -      10  -
     6  -      11  -                6  -       9  6HU5
     7  36UA   10  36UA             7  0000    8  UC33
     8  0000    9  UC33

U18  1  96F6   16  96F6        U23  1  96F6   16  96F6
     2  -      15  3953             2  -      15  1A65
     3  6C8P   14  -                3  428H   14  4325
     4  41HA   13  72A7             4  9U57   13  2U46
     5  38UP   12  7FU6             5  P3A1   12  6211
     6  -      11  A8CH             6  A12F   11  0000
     7  41HA   10  3P7C             7  010H   10  3UCU
     8  0000    9  0000             8  0000    9  2PAU

U24  1  96F6   16  96F6        U25  1  96F6   20  96F6
     2  -      15  010H             2  96F6   19  96F6
     3  HHHA   14  52A5             3  -      18  -
     4  PA30   13  2513             4  96F6   17  96F6
     5  P3A1   12  76CC             5  -      16  -
     6  H44C   11  0000             6  96F6   15  96F6
     7  010H   10  3UCU             7  -      14  -
     8  0000    9  2PAU             8  36UA   13  96F6
                                    9  -      12  -
                                   10  0000   11  96F6

U26  1  96F6   20  96F6        U27  1  96F6   16  96F6
     2  7C6U   19  96F6             2  -      15  HC53
     3  -      18  -                3  AH63   14  0000
     4  96F6   17  0000             4  AH63   13  0000
     5  -      16  -                5  AH63   12  0000
     6  96F6   15  0000             6  AH63   11  0000
     7  -      14  -                7  7C6U   10  36UA
     8  96F6   13  0000             8  0000    9  6HU5
     9  -      12  -
    10  0000   11  HC53

U28  1  96F6   16  96F6        U34  1  96F6   16  96F6
     2  -      15  7C6U             2  -      15  010H
     3  AH63   14  96F6             3  HHHA   14  52A5
     4  CA1F   13  96F6             4  PA30   13  2513
     5  735H   12  96F6             5  P3A1   12  76CC
     6  0A75   11  0000             6  H44C   11  0000
     7  96F6   10  36UA             7  010H   10  3UCU
     8  0000    9  6HU5             8  0000    9  2PAU

U35  1  96F6   16  96F6        U36  1  5151   20  96F6
     2  -      15  010H             2  HHHA   19  H44C
     3  HHHA   14  -                3  -      18  -
     4  PA30   13  -                4  -      17  -
     5  P3A1   12  -                5  PA30   16  P3A1
     6  H44C   11  0000             6  P3A1   15  PA30
     7  -      10  3UCU             7  -      14  -
     8  0000    9  2PAU             8  -      13  -
                                    9  H44C   12  HHHA
                                   10  0000   11  0000

U37  1  5151   20  96F6        U38  1  96F6   16  96F6
     2  428H   19  H44C             2  -      15  96F6
     3  -      18  -                3  2550   14  96F6
     4  -      17  -                4  P0C4   13  96F6
     5  9U57   16  P3A1             5  H808   12  96F6
     6  P3A1   15  PA30             6  9U1U   11  0000
     7  -      14  -                7  96F6   10  36UA
     8  -      13  -                8  0000    9  6HU5
     9  A12F   12  HHHA
    10  0000   11  0000

U39  1  96F6   16  96F6        U40  1  96F6   16  96F6
     2  -      15  96F6             2  0000   15  -
     3  57UH   14  96F6             3  CCC4   14  HHHA
     4  2PP1   13  96F6             4  HHHA   13  A12F
     5  81F2   12  36UA             5  3PAP   12  9U57
     6  9426   11  0000             6  9U57   11  7567
     7  0000   10  36UA             7  0000   10  0000
     8  0000    9  6HU5             8  0000    9  5151

U41  1  96F6   16  96F6        U42  1  0000   16  96F6
     2  0000   15  -                2  779C   15  5F99
     3  HHHA   14  779C             3  P11U   14  F543
     4  A12F   13  49P0             4  C3U7   13  77H9
     5  9U57   12  6HUP             5  49P0   12  43PH
     6  7567   11  F543             6  P11U   11  6HUP
     7  0000   10  0000             7  3833   10  77H9
     8  0000    9  C869             8  0000    9  0276

U43  1  96F6   16  96F6
     2  0000   15  HP96
     3  0000   14  584H
     4  0000   13  9P3F
     5  96F6   12  -
     6  96F6   11  -
     7  1110   10  96F6
     8  0000    9  C869
```

---

# 6 Schematics and Assembly Drawings

The following schematics and assembly drawings are contained in the original manual in the order listed:

| Title | Lexicon Drawing No. |
|---|---|
| Single Board Computer Schematic | — |
| Single Board Computer Assembly | — |
| Arithmetic Unit Board Schematic | 060-01318 |
| Arithmetic Unit Board Assembly | 030-02735 |
| Floating Point Converter Board Schematic | 060-01320 |
| Floating Point Converter Board Assembly | 030-01420 |
| Analog Input Board Schematic | 060-01321 |
| Analog Input Board Assembly | 030-02733 |
| Analog Output Board Schematic | 060-01322 |
| Analog Output Board Assembly | 030-02734 |
| Power Supplies Schematic | 060-01324 |
| Power Supply #1 Assembly | 030-01423 |
| Power Supply #2 Assembly | 030-01424 |
| Power Supply #3 Assembly | 030-01425 |
| Motherboard Schematic | 060-01360 |
| Motherboard Assembly | 030-01428 |
| Memory Expansion Board Schematic | 060-02273 |
| Memory Expansion Board Assembly | 080-02281 |
| Timing and Control Board Schematic | 060-02475 |
| Timing and Control Board Assembly | 030-02481 |
| Data Memory Board Schematic | 060-02512 |
| Data Memory Board Assembly | 030-02516 |
| Data Memory Board Block Diagram | — |
| Fuse Board Schematic (see Power Supply Schematic) | — |
| Fuse Board Assembly | 030-02647 |
| Output Transformer Board Schematic | 060-01359 |
| Output Transformer Board Assembly | 030-02769 |
| Transition Board Assembly | 030-01426 |
| Remote Control Head (Panel) Schematic (Logic and Display) | 060-01323 |
| Remote Control Head Assembly | 080-01757 |
| Power Supply Module Assembly | 080-01611 |
| Power Transformer Assembly | 080-01650 |
| Chassis-1 Assembly | 080-01662 |
| Chassis-2 Assembly | 080-01676 |
| Chassis-3 Assembly | 080-01845 |
| LARC Schematic | 060-03534 |
| LARC Display Board Assembly | 080-03397 |
| LARC Electronics Board Assembly | 080-03403 |
| LARC Panel Board Assembly | 080-03409 |
| LARC Transition Board Schematic | 060-03576 |
| LARC Transition Board Assembly | 080-03447 |

---

*Converted to Markdown from the Lexicon Model 224X Service Manual (© 1984 Lexicon, Inc.). This conversion covers the full text, all tabular content, and the complete per-pin signature-analysis value tables for the T&C, ARU (both configurations), DMEM, and FPC modules. Block diagrams, circuit schematics, and oscilloscope/photographic figures remain in the original PDF and are noted with descriptive callouts where they occur. Signature values were transcribed from a scanned source; verify any critical value against the original PDF.*
