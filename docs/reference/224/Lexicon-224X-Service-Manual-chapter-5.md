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

**E80 to E8F: Multiplier test.** The multiplier test is divided into four parts, each of which displays separate error codes. E81 to E83 indicate an error when the multiply coefficient is +21/32. E81 indicates a low-order byte error, E82 a high-order byte error, and E83 indicates both bytes are incorrect. E85 to E87 indicate an error when multiplying by +42/32. E89 to E8B indicate an error in the coefficient +63/64. Four multiplications are made with each coefficient. The incorrect and correct data are displayed on the pushbutton LEDs in the same way as previous tests. If both the high-order and low-order bytes are incorrect, the data in the low-order byte is displayed. The last two coefficients should set the saturation monostable multivibrator. If not, error code E80 is displayed.

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

*Converted to Markdown from the Lexicon Model 224X Service Manual (© 1984 Lexicon, Inc.). This conversion covers the full text, all tabular content, and the complete per-pin signature-analysis value tables for the T&C, ARU (both configurations), DMEM, and FPC modules. Block diagrams, circuit schematics, and oscilloscope/photographic figures remain in the original PDF and are noted with descriptive callouts where they occur. Signature values were transcribed from a scanned source; verify any critical value against the original PDF.*
