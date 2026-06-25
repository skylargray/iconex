# Lexicon Model 224X Service Manual — Chapter 7: Parts Lists

Each table lists parts for one assembly, with columns: **Category**, **Part No.**, **Qty**, **Description**, and **Reference**. Descriptions and reference designators are kept verbatim from the manual (uppercase, comma-delimited fields). Blank reference cells reflect entries with no designator in the original. A quantity of `1` has been supplied where the source dropped the digit; the single explicit `0` (RPL board, 510-01505) is preserved.

> **Scope.** This is the *Model 224X* service-manual parts list. It covers the base 224X chassis **plus** the RCH remote, the LARC remote, and the LARC ROM/RAM retrofit — i.e. the kit set that upgrades a 224X to **224XL** configuration (the LARC shipping kit ships the 224XL owner's manual, P/N 070-03695). "LURCH" in many LARC board/part names is Lexicon's internal codename for the LARC, not an OCR error, and is kept verbatim. See the **OCR & conversion notes** at the end for systematic corrections and residual flags.

## Contents

| § | Assembly |
|---|---|
| 7.1 | Single Board Computer (SBC) Board |
| 7.2 | Floating Point Converter (FPC) Board |
| 7.3 | Analog Input (AIN) Board |
| 7.4 | Analog Output (AOUT) Board |
| 7.5 | Data Memory (DMEM) Board |
| 7.6 | Timing and Control (T&C) Board |
| 7.7 | Arithmetic Unit (ARU) Board |
| 7.8 | Memory Expansion Board |
| 7.9 | Output Transformer Board |
| 7.10 | Power Supply #1 |
| 7.11 | Power Supply #2 |
| 7.12 | Power Supply #3 |
| 7.13 | Power Supply Hardware |
| 7.14 | Transition Board |
| 7.15 | Chassis Hardware |
| 7.16 | Fuse Board |
| 7.17 | Motherboard |
| 7.18 | Shipping Kit |
| 7.19 | 115V Fuse Option |
| 7.20 | 230V Fuse Option |
| 7.21 | RS232 Option |
| 7.22 | V8.1 Retrofit |
| 7.23 | RCH RPL Board |
| 7.24 | RCH RPD Board |
| 7.25 | RCH Hardware |
| 7.26 | LARC Transition Board |
| 7.27 | LARC Hardware Kit |
| 7.28 | LARC ROM/RAM Kit |
| 7.29 | LARC Shipping Kit |
| 7.30 | LARC Display Board |
| 7.31 | LARC Electronics Board |
| 7.32 | LARC Panel Board |
| 7.33 | LARC Finishing Kit |
| 7.34 | 25' Cable Option |
| 7.35 | 50' Cable Option |

---

## 7.1 Single Board Computer (SBC) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Digital/CMOS IC | 330-00673 | 2 | IC,DIGITAL,7437 | U3,6 |
| Memory IC | 350-01304 | 2 | IC,EPROM,2716 | U23,25 |
| Cable Conn | 495-01626 | 1 | CONN,XITION,RIBBON/DIP,14MC | U4 |
| Purch Sub-Assy | 750-01310 | 1 | COMPUTER BOARD,LEVEL BLC 80/11 | |

## 7.2 Floating Point Converter (FPC) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00529 | 1 | RES,CF,5%,1/4W,1K OHM | R3 |
| Ceramic Cap | 245-00598 | 26 | CAP,CER,.01uF,16V,80/20% | C6-12,15-19,22-31,34-37 |
| Tantalum Cap | 241-00652 | 8 | CAP,TANT,4.7uF,25V,RAD | C5,13,14,20,21,32,33,38 |
| Digital/CMOS IC | 330-00692 | 1 | IC,DIGITAL,74LS00 | U12 |
| Digital/CMOS IC | 330-00712 | 8 | IC,DIGITAL,74LS374 | U1,2,7,8,16,40,41,43 |
| Digital/CMOS IC | 330-01288 | 8 | IC,DIGITAL,74LS244 | U23,24,27,28,34,35,38,39 |
| Digital/CMOS IC | 330-01314 | 6 | IC,DIGITAL,74LS245 | U3,20,21,31-33 |
| Digital/CMOS IC | 330-01315 | 1 | IC,DIGITAL,74S287 | U6 |
| PC Hdwr | 610-01594 | 2 | EXTRACTOR,CARD,SCANBE#S-203 | |
| PC Boards | 710-01434 | 1 | PC BD,FPC,M224 | |

## 7.3 Analog Input (AIN) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Potentiometers | 200-00335 | 1 | POT,RTY,PC,50K-U,1/4X3/4 | R1 |
| Trim Resistors | 201-00159 | 1 | RES,TRM,ST,PC,100K,SA,CER | R97 |
| Carbon Flm Res | 202-00509 | 1 | RES,CF,5%,1/4W,47 OHM | R3 |
| Carbon Flm Res | 202-00529 | 1 | RES,CF,5%,1/4W,1K OHM | R2 |
| Metal Flm Res | 203-00464 | 19 | RES,MF,1%,1/8W,3.01K OHM | R16,17,22,23,28,29,33,43,44,R49,50,55,56,R60,72,92,93,100,102 |
| Metal Flm Res | 203-01145 | 1 | RES,MF,1%,1/8W,1.24M OHM | R12 |
| Metal Flm Res | 203-01489 | 1 | RES,MF,1%,1/8W,499 OHM | R9 |
| Metal Flm Res | 203-01664 | 1 | RES,MF,1%,1/8W,133K OHM | R10 |
| Metal Flm Res | 203-02656 | 1 | RES,MF,1%,1/8W,182K OHM | R11 |
| Electrolyt Cap | 240-00609 | 1 | CAP,ELEC,10uF,16V,RAD | C21 |
| Tantalum Cap | 241-00652 | 1 | CAP,TANT,4.7uF,25V,RAD | C47 |
| Pcrb/PP Cap | 244-01151 | 18 | CAP,PP,.001uF,100V,5%,RAD | C3,6,9,12,15,18,21,29,32,35,C38,41,44,47,C71,73,94,95 |
| Ceramic Cap | 245-00600 | 33 | CAP,CER,.02uF,35V,80/20% | C1,2,7,8,13,14,19,20,22,23,C27,28,33,34,C39,40,45,46,48,49,53,54,56,57,59,60,64,65,72,74,75,78,82 |
| Ceramic Cap | 245-02105 | 12 | CAP,CER,.0033uF,100V,10% | C4,5,10,11,16,17,30,31,36,C37,42,43 |
| Linear IC | 340-01183 | 1 | IC,LINEAR,LF 356 | U7 |
| Linear IC | 340-01566 | 1 | IC,LINEAR,LF353,DUAL OP AMP | U8 |
| Converter IC | 355-01362 | 1 | DAC-80-1 | U9 |
| Bulk Wire | 670-01768 | 10 | WIRE,JMP,22AWG,0.5",TEF,WHT | R19,25,31,39,46,52,58,R66,69,70 |
| PC Boards | 710-01435 | 1 | PC BD,AIN,M224 | |

## 7.4 Analog Output (AOUT) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Trim Resistors | 201-00433 | 12 | RES,TRM,ST,PC,5K,SA,CC | R19,25,31,51,57,63,69,75,R81,101,107,R113 |
| Trim Resistors | 201-01677 | 1 | RES,TRM,RTY,PC,50K-U,SA | R1 |
| Carbon Flm Res | 202-00531 | 8 | RES,CF,5%,1/4W,1.5K OHM | R123,124,133,134,143,144,R153,154 |
| Carbon Flm Res | 202-00542 | 8 | RES,CF,5%,1/4W,4.7K OHM | R43,44,93,94,121,131,R141,151 |
| Carbon Flm Res | 202-01157 | 8 | RES,CF,5%,1/4W,3.65K OHM | R126,127,136,137,146,147,R156,157 |
| Metal Flm Res | 203-00471 | 24 | RES,MF,1%,1/8W,10.0K OHM | R22,23,28,29,34,35,54,55,R60,61,66,R67,72,73,78,79,84,85,104,105,R110,111,116,117 |
| Tantalum Cap | 241-00652 | 13 | CAP,TANT,4.7uF,25V,RAD | C2,3,6,21,22,113,114,118,C119,123,124,C128,129 |
| Tantalum Cap | 241-00654 | 9 | CAP,TANT,10uF,25V,RAD | C111,112,116,117,121,122,C126,127,135 |
| Pcrb/PP Cap | 244-01151 | 28 | CAP,PP,.001uF,100V,5%,RAD | C25,28,31,34,37,40,43,44,C51,54,57,60,C63,66,69,72,75,78,81,84,C87,88,95,98,101,104,107,110 |
| Pcrb/PP Cap | 244-02486 | 4 | CAP,PP,510pF,160V,2.5%,AX | C13,16,17,20 |
| Ceramic Cap | 245-00600 | 45 | CAP,CER,.02uF,35V,80/20% | C1,4,5,7-12,14,15,18,19,23,24,C29,30,35,C36,41,42,45,46,49,50,55,C56,61,62,67,68,73,74,79,C80,85,86,89,90,93,94,99,C100,105,106 |
| Ceramic Cap | 245-01164 | 24 | CAP,CER,470pF,100V,10% | C26,27,32,33,38,39,52,53,58,C59,64,65,C70,71,76,77,82,83,96,97,C102,103,108,109 |
| Diodes | 300-01029 | 14 | DIODE,1N914 AND 4148 | CR1-4,CR7-16 |
| Digital/CMOS IC | 330-01457 | 1 | IC,DIGITAL,4054(RCA),CMOS | U5 |
| SS SW IC | 346-00769 | 1 | IC,SS SWITCH,4051 | U7 |
| SS SW IC | 346-01366 | 1 | IC,SS SWITCH,4016 | U6 |
| Converter IC | 355-00774 | 1 | DAC,80-CBI-V | U2 |
| Bulk Wire | 670-01768 | 14 | WIRE,JMP,22AWG,0.5",TEF,WHT | R7,8,10,11,14,15,38,39,40,R41,88,89,R90,91 |
| PC Boards | 710-01436 | 1 | PC BD,AOUT,M224 | |

## 7.5 Data Memory (DMEM) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Ceramic Cap | 245-00598 | 20 | CAP,CER,.01uF,16V,80/20% | C17,39,59-68,71-78 |
| Ceramic Cap | 245-01651 | 43 | CAP,CER,.1uF,50V,80/20% | C1-16,18,19,40,41,43-58,C69,70,79,80,C81,83,87 |
| Digital/CMOS IC | 330-03341 | 2 | IC,DIGITAL,74F283 | U49,50 |
| Memory IC | 350-03439 | 16 | IC,DRAM,4164,64KX1,150NS | U20-35 |
| Modules | 380-02509 | 1 | MOD,DLY,LINE,5 TAPS,30/150 NS | U59 |
| PC Boards | 710-02511 | 1 | PC BD,DATA MEM&IO,M224X | |

## 7.6 Timing and Control (T&C) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Ceramic Cap | 245-00598 | 41 | CAP,CER,.01uF,16V,80/20% | C2-8,10,14,15,21-30,35-44,47,C50-59 |
| Ceramic Cap | 245-01651 | 9 | CAP,CER,.1uF,50V,80/20% | C1,16,20,33,34,48,49,60,63 |
| Digital/CMOS IC | 330-01289 | 2 | IC,DIGITAL,74195 | U10,11 |
| Digital/CMOS IC | 330-01302 | 4 | IC,DIGITAL,AM8304 N | U3,16,30,44 |
| Memory IC | 350-02626 | 4 | IC,RAM,MCM68B10 | U2,15,29,43 |
| Dsply/Ind/LED | 430-00904 | 1 | LED,HP #5082-4850 | LED1 |
| PC Boards | 710-01441 | 1 | PC BD,T&C,M224 | |

## 7.7 Arithmetic Unit (ARU) Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Ceramic Cap | 245-00598 | 30 | CAP,CER,.01uF,16V,80/20% | C4-11,14-23,26-32,36-40 |
| Tantalum Cap | 241-00652 | 8 | CAP,TANT,4.7uF,25V,RAD | C3,12,13,24,25,34,35,41 |
| Digital/CMOS IC | 330-00692 | 10 | IC,DIGITAL,74LS00 | U14,26-28,40,41,50-53 |
| Electronic Hdwr | 600-01565 | 4 | BUSS BAR,1C,1.4X4,TIN | |
| PC Hdwr | 610-01594 | 2 | EXTRACTOR,CARD,SCANBE#S-203 | |
| PC Boards | 710-01432 | 1 | PC BD,ARU,M224 | |

## 7.8 Memory Expansion Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00533 | 9 | RES,CF,5%,1/4W,2K OHM | R4-7,9,13,17,18,REF |
| Ceramic Cap | 245-00598 | 6 | CAP,CER,.01uF,16V,80/20% | C6-9,27,33 |
| Ceramic Cap | 245-00600 | 25 | CAP,CER,.02uF,35V,80/20% | C1-5,10-20,22,24,29-32,35-37 |
| Digital/CMOS IC | 330-00674 | 1 | IC,DIGITAL,7438 | U25 |
| Digital/CMOS IC | 330-00766 | 1 | IC,DIGITAL,4011,CMOS | U14 |
| Memory IC | 350-03439 | 16 | IC,DRAM,4164,64KX1,150NS | U1-16 |
| Cable Conn | 490-02356 | 6 | CONN,JUMPER,.1X025,2FCG | J1-4 |
| PC Mnt Conn | 510-02671 | 8 | CONN,POST,100X025,HDR,3MC,GOLD | J1-4 |
| Bulk Wire | 670-02037 | 5 | WIRE,28AWG,KYNAR,GRN | JUMPER 41-42, CUT (1) 4 1/2" PIECE |
| PC Boards | 710-02663 | 1 | PC BD,MEM EXP,M224X | |

## 7.9 Output Transformer Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Inductors | 270-00779 | 12 | FERRITE,BEAD | FB1-12 |
| Transformers | 470-00261 | 4 | XFORMER,OUTPUT,M224 | T1-4 |
| PC Mnt Conn | 510-02806 | 2 | CONN,XLR,3FC,PC | J23,24 (PIN ASSY) SHELLS ARE TO BE RETAINED FOR CHASSIS ASSY |
| PC Mnt Conn | 510-02807 | 4 | CONN,XLR,3MC,PC | J25-28 (PIN ASSY) SHELLS ARE TO BE RETAINED FOR CHASSIS ASSY |
| Thrd-Form Scrw | 641-02827 | 12 | SCRW,TAP,F,4-40X1/4,PNH,PH,ZN | J23-28 |
| PC Boards | 710-02808 | 1 | PC BD,OUTPUT XFORMER,M224 | |

## 7.10 Power Supply #1

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00518 | 1 | RES,CF,5%,1/4W,220 OHM | R1 |
| Electrolyt Cap | 240-00619 | 1 | CAP,ELEC,1000uF,25V,AX | C2 |
| Electrolyt Cap | 240-01329 | 1 | CAP,ELEC,45,000uF,15V | C1 |
| Ceramic Cap | 245-00596 | 2 | CAP,CER,.005uF,1.6KV,Z5U | C3,4 |
| Diodes | 300-01032 | 2 | DIODE,1N5404 | CR1,2 |
| Diodes | 300-01466 | 1 | DIODE,BRIDGE,VARO#R711 | U1 |
| Dsply/Ind/LED | 430-00904 | 1 | LED,HP #5082-4850 | CR3 |
| Slide Switch | 451-02230 | 2 | SW,SL,2P2T,V-CHNG,PC,4A | SW2,3 |
| Psh But Switch | 453-01467 | 1 | SW,PBPP,2P2T,WINK,BLU,SDR | SW1 |
| Psh But Switch | 453-01468 | 1 | SW,PBM,1P2T,C&K,PCRA | SW4 |
| Cable Conn | 490-01479 | 1 | CONN,POST,156X045,INS-DSP,3FCG | |
| PC Mnt Conn | 510-01469 | 1 | CONN,PIN&SOC,MATE&LOCK,PC,10MC | J9 |
| PC Mnt Conn | 510-02742 | 1 | CONN,PIN&SOC,MATE&LOCK,3FC,PC | J48 |
| Strain Rel | 530-02489 | 2 | TIE,CABLE,NYL,.1"X4" | |
| Lugs | 620-01616 | 6 | LUG,SPADE,1/4",AMP#41729 OR EQ | |
| Insul/Spacrs | 630-00957 | 4 | SPCR,#4CLX1/16,3/16RD,NYL | |
| Insul/Spacrs | 630-01852 | 1 | INSUL,SEMI,SIL RUB,TO-3 | |
| Spcr,Non-Insul | 635-01453 | 5 | SPCR,SWAGE,6-32X1/2,1/4RD,BR/N | |
| Machine Screws | 640-01706 | 2 | SCRW,4-40X3/8,PNH,PH,ZN | |
| Machine Screws | 640-01716 | 4 | SCRW,6-32X3/8,PNH,PH,ZN | |
| Machine Screws | 640-01720 | 1 | SCRW,6-32X3/4,PNH,PH,ZN | CAP BRKT |
| Machine Screws | 640-01841 | 2 | SCRW,2-56X1/4,PNH,PH,ZN | |
| Nuts | 643-01728 | 1 | NUT,6-32,KEP,ZN | CAP BRKT |
| Nuts | 643-01730 | 2 | NUT,6-32,KEP,SMALL,ZN | |
| Nuts | 643-01732 | 2 | NUT,4-40,KEP,ZN | |
| Nuts | 643-01855 | 2 | NUT,2-56,HEX,SMALL,ZN | |
| Washers | 644-01854 | 2 | WSHR,LOCK,SPLIT,#2 | |
| Pre-Cut Wire | 675-02839 | 1 | WIRE,16G,RED,10",ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02840 | 1 | WIRE,16G,BLK,10",ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02842 | 1 | WIRE,16G,YEL,10",ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02864 | 1 | WIRE,18G,BLK,18",ST&T1/4XO | |
| Pre-Cut Wire | 675-02886 | 2 | WIRE,14G,RED,7.5,ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02887 | 1 | WIRE,14G,R/Y,7.5,ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02891 | 1 | WIRE,18G,GRN,18",ST&T1/4XO | |
| Cables/Cords | 680-01527 | 1 | CORD,FAN,PLUG,M92081-24 | J18 |
| Brackets | 701-00299 | 2 | BRACKET,KEYSTONE #617 | |
| Brackets | 701-01330 | 1 | BRACKET,CAP | |
| Panels | 702-00843 | 6 | COVER,BOOT,TS 253224 | |
| Heat Sinks | 704-01451 | 1 | HEAT SINK,TO-3,IERC#UP-TO-3-CB | |
| PC Boards | 710-01437 | 1 | PC BD,PS-1,M224 | |

## 7.11 Power Supply #2

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Trim Resistors | 201-00425 | 1 | RES,TRM,ST,PCRA,500 OHM,SA,CER | R6 |
| Trim Resistors | 201-01461 | 1 | RES,TRM,ST,PCRA,1K,SA,CER | R5 |
| Carbon Flm Res | 202-00542 | 1 | RES,CF,5%,1/4W,4.7K OHM | R9 |
| Metal Flm Res | 203-00461 | 1 | RES,MF,1%,1/8W,2.43K OHM | R7 |
| Metal Flm Res | 203-00471 | 2 | RES,MF,1%,1/8W,10.0K OHM | R3,4 |
| Metal Flm Res | 203-01459 | 2 | RES,MF,1%,1/8W,243 OHM | R2,8 |
| Metal Flm Res | 203-01460 | 1 | RES,MF,1%,1/8W,2.05K OHM | R1 |
| Electrolyt Cap | 240-00609 | 1 | CAP,ELEC,10uF,16V,RAD | C7 |
| Electrolyt Cap | 240-00623 | 1 | CAP,ELEC,5500uF,25V,COP | C2 |
| Electrolyt Cap | 240-01262 | 2 | CAP,ELEC,330uF,25V,RAD | C11,12 |
| Electrolyt Cap | 240-01446 | 2 | CAP,ELEC,3300uF,35V,RAD | C6,10 |
| Tantalum Cap | 241-00652 | 3 | CAP,TANT,4.7uF,25V,RAD | C1,8,9 |
| Mica Cap | 242-00631 | 1 | CAP,MICA,33pF,DM-15,330J | C3 |
| Ceramic Cap | 245-00600 | 2 | CAP,CER,.02uF,35V,80/20% | C4,5 |
| Diodes | 300-01030 | 12 | DIODE,1N4004 AND 4005 | CR1-12 |
| Transistors | 310-01007 | 1 | TRANSISTOR,2N3904 | Q1 |
| Linear IC | 340-00722 | 1 | IC,LINEAR,LM301 | U4 |
| Cable Conn | 490-02712 | 1 | CONN,POST,156X045,INS-DSP,5FCG | J17 |
| PC Mnt Conn | 510-01464 | 2 | CONN,POST,156X045,PCRA,6FCG | J12A,B |
| Sockets | 520-00941 | 1 | IC SCKT,8 PIN,PC,LO-PRO | U4 |
| Pre-Cut Wire | 675-02855 | 2 | WIRE,18G,BRN,12",ST&T1/4XO | |
| Pre-Cut Wire | 675-02857 | 1 | WIRE,18G,GRY,12",ST&T1/4XO | |
| Pre-Cut Wire | 675-02860 | 1 | WIRE,18G,BLU,12",ST&T1/4XO | |
| PC Boards | 710-01438 | 1 | PC BD,PS-2,M224 | |

## 7.12 Power Supply #3

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Trim Resistors | 201-01619 | 2 | RES,TRM,ST,PC,500 OHM,SA,CER | R7,11 |
| Carbon Flm Res | 202-00495 | 1 | RES,CF,5%,1/2W,1.2 OHM | R5 |
| Carbon Flm Res | 202-00514 | 2 | RES,CF,5%,1/4W,100 OHM | R9,10 |
| Carbon Flm Res | 202-00524 | 1 | RES,CF,5%,1/4W,470 OHM | R13 |
| Carbon Flm Res | 202-00527 | 1 | RES,CF,5%,1/4W,750 OHM | R6 |
| Carbon Flm Res | 202-00531 | 1 | RES,CF,5%,1/4W,1.5K OHM | R12 |
| Carbon Flm Res | 202-00535 | 1 | RES,CF,5%,1/4W,2.4K OHM | R8 |
| Carbon Flm Res | 202-00555 | 1 | RES,CF,5%,1/4W,20K OHM | R14 |
| Wirewound Res | 204-01523 | 2 | RES,WW,5%,10W,0.1 OHM | R1,2 |
| Carbon Comp Res | 206-01524 | 2 | RES,CC,5%,2W,27 OHM | R3,4 |
| Electrolyt Cap | 240-00620 | 2 | CAP,ELEC,1000uF,35V,RAD | C6,8 |
| Tantalum Cap | 241-00652 | 5 | CAP,TANT,4.7uF,25V,RAD | C2,3,7,9,10 |
| Ceramic Cap | 245-00592 | 1 | CAP,CER,510pF,500V,10% | C4 |
| Ceramic Cap | 245-00605 | 2 | CAP,CER,.1uF,16V,80/20% | C1,5 |
| Diodes | 300-01027 | 1 | DIODE,1N754 | CR2 |
| Diodes | 300-01030 | 8 | DIODE,1N4004 AND 4005 | CR1,3,5,7,8,9,10,11 |
| Diodes | 300-01032 | 2 | DIODE,1N5404 | CR4,6 |
| Diodes | 300-01526 | 1 | DIODE,1N750,ZENER,4.7V | CR12 |
| Transistors | 310-01007 | 1 | TRANSISTOR,2N3904 | Q4 |
| Linear IC | 340-00730 | 1 | IC,LINEAR,UA 723 | U1 |
| Linear IC | 340-01525 | 1 | IC,LINEAR,7905,-5V REG | U2 |
| Cable Conn | 490-00823 | 2 | CONN,POST,156X045,INS-DSP,6FCG | J15,16 |
| PC Mnt Conn | 510-01464 | 1 | CONN,POST,156X045,PCRA,6FCG | J14 |
| PC Mnt Conn | 510-01480 | 2 | CONN,POST,156X045,HDR,3MCG,LOK | J11,13 |
| PC Mnt Conn | 510-01481 | 2 | CONN,POST,156X045,HDR,6MCG,LOK | J12A,B |
| Sockets | 520-00831 | 3 | CONN,XISTOR,TO-220/202 | Q3,5,U3 |
| Sockets | 520-00947 | 2 | XISTOR SCKT,TO3,SOLDER | Q1,2 |
| Term/Pins | 525-00988 | 3 | QDC,.250X.032,MALE,RA | SCRW MTG |
| Spcr,Non-Insul | 635-01454 | 2 | SPCR,SWAGE,6-32X5/8,1/4RD,BR/N | |
| Machine Screws | 640-01706 | 1 | SCRW,4-40X3/8,PNH,PH,ZN | |
| Nuts | 643-01732 | 1 | NUT,4-40,KEP,ZN | |
| Threadls Fastnr | 650-00989 | 3 | EYELET,1/8CLX1/8L,BRASS/SDR | |
| Bulk Wire | 670-02722 | 2 | WIRE,JMP,22AWG,.75",TEF,WHT | |
| Pre-Cut Wire | 675-02862 | 1 | WIRE,18G,BLK,10",ST&T1/4XO | |
| Pre-Cut Wire | 675-02863 | 2 | WIRE,18G,BLK,14",ST&T1/4XO | |
| Pre-Cut Wire | 675-02865 | 1 | WIRE,18G,RED,3.5",ST&T1/4X1/4 | |
| Pre-Cut Wire | 675-02866 | 1 | WIRE,18G,RED,5.5",ST&T1/4X1/4 | |
| Pre-Cut Wire | 675-02868 | 2 | WIRE,18G,RED,14",ST&T1/4XO | |
| Pre-Cut Wire | 675-02869 | 1 | WIRE,18G,ORN,3.5",ST&T1/4X1/4 | |
| Pre-Cut Wire | 675-02870 | 1 | WIRE,18G,ORN,5.5",ST&T1/4X1/4 | |
| Pre-Cut Wire | 675-02872 | 1 | WIRE,18G,ORN,10",ST&T1/4XO | |
| Pre-Cut Wire | 675-02873 | 1 | WIRE,18G,PRP,3.5",ST&T1/4X1/4 | |
| Pre-Cut Wire | 675-02874 | 1 | WIRE,18G,PRP,5.5",ST&T1/4X1/4 | |
| Pre-Cut Wire | 675-02877 | 1 | WIRE,18G,PRP,14",ST&T1/4XO | |
| Pre-Cut Wire | 675-02880 | 1 | WIRE,18G,YEL,14",ST&T1/4XO | |
| PC Boards | 710-01439 | 1 | PC BD,PS-3,M224 | |

## 7.13 Power Supply Hardware

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Transistors | 310-01017 | 1 | TRANSISTOR,TIP31 A | Q3 (PS BD #3) |
| Transistors | 310-01522 | 2 | TRANSISTOR,2N5885 | Q1,2 (PS BD #3) |
| SCR | 320-01014 | 1 | TRANSISTOR,C122F1,SCR | Q5 (PS BD #3) |
| Linear IC | 340-01462 | 2 | IC,LINEAR,LM317,TO-3 | U1,2 (PS BD #2) |
| Linear IC | 340-01463 | 2 | IC,LINEAR,7912 | U3 (PS BD #2), U3 (PS BD #3) |
| Insul/Spacrs | 630-00952 | 4 | INSUL,SEMI,BUSHING,TO-220 | |
| Insul/Spacrs | 630-00958 | 9 | SPCR,#6CLX1/8,3/16RD,NYL | |
| Insul/Spacrs | 630-01852 | 4 | INSUL,SEMI,SIL RUB,TO-3 | |
| Insul/Spacrs | 630-01853 | 4 | INSUL,SEMI,SIL RUB,TO-220 | |
| Machine Screws | 640-01700 | 1 | SCRW,4-40X1/2,PNH,PH,SS | U3 (PS BD #2) |
| Machine Screws | 640-01705 | 3 | SCRW,4-40X5/16,PNH,PH,ZN | Q3,5,U3 |
| Machine Screws | 640-01708 | 4 | SCRW,6-32X3/16,PNH,PH,ZN | BRACKET MTG |
| Machine Screws | 640-01719 | 9 | SCRW,6-32X1/2,PNH,PH,ZN | U1-2,CAP,BRACKET MTG |
| Machine Screws | 640-01720 | 5 | SCRW,6-32X3/4,PNH,PH,ZN | Q1,2 MTG |
| Nuts | 643-01730 | 9 | NUT,6-32,KEP,SMALL,ZN | U1-2,CAP,BRACKET,MTG |
| Nuts | 643-01732 | 1 | NUT,4-40,KEP,ZN | U3 (PS BD #2) |
| Washers | 644-01736 | 3 | WSHR,FL,#4CLX.218ODX.032THK | Q3,5,U3 |
| Washers | 644-01737 | 3 | WSHR,LOCK,SPLIT,#4 | |
| Washers | 644-01740 | 8 | WSHR,LOCK,SPLIT,#6 | |
| Brackets | 701-00299 | 2 | BRACKET,KEYSTONE #617 | |
| Brackets | 701-01541 | 1 | BRACKET,ELECTROLYTIC SUPPORT | |
| Brackets | 701-01555 | 1 | BRACKET,CAP CLAMP | |
| Heat Sinks | 704-01266 | 1 | HEAT SINK,POWER SUPPLY,M224 | |

## 7.14 Transition Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| PC Mnt Conn | 510-01480 | 1 | CONN,POST,156X045,HDR,3MCG,LOK | |
| PC Mnt Conn | 510-01510 | 1 | CONN,D-SUB,25FC,MB,PC | |
| Bulk Wire | 670-02722 | 1 | WIRE,JMP,22AWG,.75",TEF,WHT | |
| Cables/Cords | 680-01557 | 1 | CABLE,XITION,50 COND | |
| PC Boards | 710-01440 | 1 | PC BD,XITION BD,M224 | |

## 7.15 Chassis Hardware

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Fans/Motrs/Rely | 410-01529 | 1 | FAN,TUBE,AX,4-1/8X1-1/2,50CFM | FAN ASSY |
| Transformers | 470-01475 | 1 | XFORMER,POWER,M224 | XFORMER |
| Cable Conn | 490-00396 | 1 | CONN,AC AND RFI FILTER | |
| Cable Conn | 490-00812 | 1 | CONN,PIN&SOC,.062,HSG,1F,MB | PWR FAIL SENSE |
| Cable Conn | 490-01477 | 1 | CONN,PIN&SOC,MATE&LOCK,HSG,10F | XFORMER |
| Cable Conn | 490-02471 | 2 | CONN,PIN&SOC,M&L,CRIMP PIN,14 | |
| Cable Conn | 490-02741 | 1 | CONN,PIN&SOC,MATE&LOCK,HSG,3M | AC POWER |
| PC Mnt Conn | 510-02806 | 2 | CONN,XLR,3FC,PC | (SOCKET ASSY REMOVED) (ITEM RETAINED FROM 023-02767 — DO NOT DRAW FROM STOCK) |
| PC Mnt Conn | 510-02807 | 4 | CONN,XLR,3MC,PC | (PIN ASSY REMOVED) (ITEM RETAINED FROM 023-02767 — DO NOT DRAW FROM STOCK) |
| Term/Pins | 525-00808 | 1 | CONN,PIN&SOC,062,CRIMP SCKT,24 | PWR FAIL SENSE |
| Term/Pins | 525-01478 | 6 | CONN,PIN&SOC,M&L,CRIMP SCKT | XFORMER |
| Conn Hdwr | 527-00138 | 2 | CONN,D-SUB,JACKSOCKET | XITION BD MTG |
| Strain Rel | 530-01520 | 2 | CLIP,RIBBON,CABLE | |
| Strain Rel | 530-02489 | 10 | TIE,CABLE,NYL,.1"X4" | XFORMER WIRING, PS1,2; 3 MOD WIRING |
| Strain Rel | 530-02738 | 1 | CLIP,WIRE HRNS,.50"DIA,ADH BAK | |
| Grommets | 540-00886 | 1 | PLUG,HOLE,5/8" | |
| Feet | 541-00780 | 4 | BUMPER,FEET,3-M #SJ5023 | |
| Electronic Hdwr | 600-00859 | 8 | PANEL SCRW,CAPTIVE,6-32 | MOUNTED ON FRONT PANEL |
| Electronic Hdwr | 600-00872 | 1 | FUSE HOLDER,3AG,PANEL,RA | |
| Lugs | 620-01999 | 1 | LUG,SOLDER,LCKNG,#6,.020THK | GRNDING LUG |
| Insul/Spacrs | 630-01591 | 1 | INSUL,LOGIC BOARD,M224 | |
| Spcr,Non-Insul | 635-01655 | 1 | SPCR,6-32X7/16,1/4HEX,AL | XLR MTG |
| Machine Screws | 640-01704 | 12 | SCRW,4-40X5/16,FH,PH,ZN | PROTECTIVE COVER,AC POWER CONN |
| Machine Screws | 640-01706 | 4 | SCRW,4-40X3/8,PNH,PH,ZN | XFORMER BD MTG,PROT COVER |
| Machine Screws | 640-01710 | 2 | SCRW,6-32X1/4,PNH,PH,ZN | PS1,3 MTG,TOP COVER |
| Machine Screws | 640-01711 | 13 | SCRW,6-32X1/4,FH,PH,ZN | GRND LUG,EXTRUSION MTG |
| Machine Screws | 640-01716 | 24 | SCRW,6-32X3/8,PNH,PH,ZN | RACK EAR MTG |
| Machine Screws | 640-01720 | 5 | SCRW,6-32X3/4,PNH,PH,ZN | LINE FILT MTG,FAN ASSY |
| Machine Screws | 640-01723 | 4 | SCRW,10-32X3/8,FH,100DEG,PH,ZN | PWR XFORMER |
| Machine Screws | 640-02404 | 4 | SCRW,6-32X13/16,PNH,PH,ZN | XFORMER |
| Machine Screws | 640-03713 | 3 | SCRW,6-32X1/4,PNH,PH,SEMS,ZN | TOP COVER MTG |
| Thrd-Form Scrw | 641-01717 | 20 | SCRW,TAP,F,6-32X1/4,HWH,SLOT | MOTHERBD MTG,FAN PL MTG |
| Nuts | 643-01727 | 4 | NUT,10-32,KEP,ZN | |
| Nuts | 643-01728 | 4 | NUT,6-32,KEP,ZN | FAN ASSY |
| Nuts | 643-01729 | 1 | NUT,6-32,HEX,SMALL,ZN | GRND LUG |
| Nuts | 643-01732 | 2 | NUT,4-40,KEP,ZN | OLD XITION BD MTG |
| Nuts | 643-03538 | 4 | NUT,6-32,SPEED,SLF RETAIN,.093 | XFORMER |
| Washers | 644-01735 | 2 | WSHR,FL,#6CLX3/8ODX1/32THK | PROTECTIVE COVER |
| Washers | 644-01736 | 2 | WSHR,FL,#4CLX.218ODX.032THK | AC CONN MTG |
| Washers | 644-01739 | 17 | WSHR,INT STAR,#6 | EAR, PROT COVER,GRND LUG |
| Washers | 644-01740 | 28 | WSHR,LOCK,SPLIT,#6 | PROTECTIVE COVER |
| Washers | 644-01747 | 2 | WSHR,INT STAR,#4 | |
| Threadls Fastnr | 650-02586 | 1 | FASTNR,NYLATCH,HN5G-52-1 | PCB RETAINER |
| Threadls Fastnr | 650-02587 | 1 | FASTNR,NYLATCH,HN5P-52-4-1 | PCB RETAINER |
| Pre-Cut Wire | 675-02845 | 1 | WIRE,18G,WHT,17",ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02846 | 1 | WIRE,18G,BLK,3",ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02850 | 1 | WIRE,18G,BLK,17",ST1/4XST&T1/4 | |
| Pre-Cut Wire | 675-02852 | 1 | WIRE,16G,GRN,4",ST1/4XST&T1/4 | AC CONN |
| Pre-Cut Wire | 675-03565 | 1 | WIRE,24G,BLU,11.5,ST1/4XST&T1/4 | PWR FAIL SENSE |
| Sleeving | 690-02060 | 1 | SLEEVING,SHRINK,3/16" | AC CONN,1/2" LENGTHS |
| Chassis/Mech | 700-01265 | 1 | MTG PLATE,FAN,CHASSIS,M224 | FAN ASSY |
| Chassis/Mech | 700-01269 | 1 | COVER,TOP,CHASSIS,M224 | |
| Chassis/Mech | 700-01308 | 1 | MAINFRAME,ASSY,3-SHEETS,M224 | |
| Brackets | 701-02440 | 2 | BRACKET,MTG,RACK,M1200 | |
| Panels | 702-01311 | 1 | PROTECTIVE COVER,M224 | |
| Panels | 702-01551 | 1 | COVER,HOLE,DB-25 | |
| Panels | 702-02750 | 1 | STRAP,RETAINER,PC | PCB RETAINER |
| Panels | 702-02758 | 1 | PANEL,FRONT,M224X | |
| Plastics | 720-00436 | 1 | TAPE,FOAM,1/2X1/16X7-1/2 | |
| Plastics | 720-01261 | 1 | AIR FILTER,CHASSIS,M224 | |
| Plastics | 720-01879 | 2 | TAPE,FOAM,1/2X1/8X7-1/2 | |
| Plastics | 720-03272 | 6 | TAPE,FOAM,SGL-STK,1/8THX3/4W | PCB RETAINER |
| Plastics | 720-03386 | 1 | AIR FILTER,FRONT PANEL,M224X | FP |
| Plastics | 720-03389 | 13 | VELCRO ARROWHEAD,PRESSURE SENS | FP, CUT INTO (2) 6.5" PIECES |
| Label/Nameplts | 740-02729 | 1 | LABEL,FCC COMPLIANCE | TOP COVER |
| Label/Nameplts | 740-02773 | 1 | LABEL,CLA APPROVAL | |

## 7.16 Fuse Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00526 | 1 | RES,CF,5%,1/4W,680 OHM | R1 |
| Fuses | 440-00867 | 3 | FUSE,3AG,SLO-BLO,2AMP | |
| Fuses | 440-00869 | 1 | FUSE,3AG,SLO-BLO,2.5AMP | |
| Fuses | 440-01624 | 2 | FUSE,3AG,SLO-BLO,3AMP,250V | |
| Fuses | 440-02664 | 2 | FUSE,3AG,SLO-BLO,15AMP,32V | |
| Cable Conn | 490-01479 | 3 | CONN,POST,156X045,INS-DSP,3FCG | |
| PC Mnt Conn | 510-02743 | 3 | QDC,.250X.032,PC-MALE | J49,50,51 |
| Term/Pins | 525-00802 | 1 | CONN,PIN&SOC,062,PIN,SWAGE | J47 |
| Strain Rel | 530-02489 | 6 | TIE,CABLE,NYL,.1"X4" | FUSE BD WIRING |
| Electronic Hdwr | 600-00871 | 14 | FUSE CLIP,1/4",PC | |
| Electronic Hdwr | 600-03171 | 1 | FUSE BLOCK,3AG,1/4"QDC | |
| Lugs | 620-01616 | 2 | LUG,SPADE,1/4",AMP#41729 OR EQ | |
| Spcr,Non-Insul | 635-02361 | 4 | SPCR,SWAGE,#6CLX1/2,1/4RD,BR/N | |
| Machine Screws | 640-01706 | 1 | SCRW,4-40X3/8,PNH,PH,ZN | |
| Nuts | 643-01732 | 1 | NUT,4-40,KEP,ZN | |
| Washers | 644-01737 | 1 | WSHR,LOCK,SPLIT,#4 | |
| Pre-Cut Wire | 675-02859 | 2 | WIRE,18G,BLU,9",ST&T1/4XO | |
| Pre-Cut Wire | 675-02879 | 2 | WIRE,18G,YEL,9",ST&T1/4XO | |
| Pre-Cut Wire | 675-02888 | 1 | WIRE,18G,BLU/WHT,9",ST&T1/4XO | |
| Pre-Cut Wire | 675-02889 | 1 | WIRE,18G,YEL/BLK,9",ST&T1/4XO | |
| Pre-Cut Wire | 675-02890 | 2 | WIRE,18G,GRN,9",ST&T1/4XO | |
| Pre-Cut Wire | 675-03271 | 1 | WIRE,16G,YEL,11",ST1/4X1/4 | |
| Panels | 702-00843 | 2 | COVER,BOOT,TS 253224 | |
| PC Boards | 710-02642 | 1 | PC BD,FUSE PC BD,M224 CHASSIS | |

## 7.17 Motherboard

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00518 | 2 | RES,CF,5%,1/4W,220 OHM | |
| Carbon Flm Res | 202-00521 | 2 | RES,CF,5%,1/4W,330 OHM | |
| Carbon Flm Res | 202-00525 | 2 | RES,CF,5%,1/4W,510 OHM | |
| Network Res | 205-01590 | 5 | RES,NET,SIP,2%,2.2KX9 | |
| PC Edge Conn | 500-01516 | 8 | CONN,EDGE,30/60 C,.100,PC | J1A-8A |
| PC Edge Conn | 500-01517 | 8 | CONN,EDGE,43/86 C,.156,PC | J1-8 |
| PC Mnt Conn | 510-00827 | 2 | CONN,POST,156X045,HDR,6MCG,POL | J15,16 |
| PC Mnt Conn | 510-00828 | 1 | CONN,POST,156X045,HDR,6MCG | J14 |
| PC Mnt Conn | 510-01480 | 1 | CONN,POST,156X045,HDR,3MCG,LOK | |
| PC Mnt Conn | 510-01481 | 1 | CONN,POST,156X045,HDR,6MCG,LOK | J17 |
| PC Mnt Conn | 510-02898 | 1 | CONN,POST,100X025,HDR,16MC,GLD | |
| PC Hdwr | 610-01654 | 6 | KEY POLARIZATION,PC EDGE CONN | |
| Thrd-Form Scrw | 641-01717 | 1 | SCRW,TAP,F,6-32X1/4,HWH,SLOT | BRKT MTG |
| Nuts | 643-01730 | 1 | NUT,6-32,KEP,SMALL,ZN | |
| Brackets | 701-00299 | 1 | BRACKET,KEYSTONE #617 | |
| PC Boards | 710-01442 | 1 | PC BD,MOTHERBD,M224 | |

## 7.18 Shipping Kit

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Cust Literature | 070-02709 | 1 | MANUAL,OWNER'S,M224X | |
| Cust Literature | 070-02813 | 1 | CARD,WARRANTY,LEXICON | |
| Cables/Cords | 680-00841 | 1 | CORD,POWER,PHILLIP #13E37-1 | |
| Shipping Mat | 730-00201 | 1 | BOX,OUT,15-1/2X12-1/8X8,REM HD | |
| Shipping Mat | 730-01658 | 2 | INSERT,PACKING,M224 | |
| Shipping Mat | 730-01828 | 1 | BOX,OUT,24X23-3/8X12-3/4,M224 | |
| Shipping Mat | 730-01829 | 1 | BOX,IN,17-5/8X19X8,M224 | |
| Shipping Mat | 730-01830 | 1 | INSRT,CDBD,FR,19X8X1-1/2,M224 | |
| Shipping Mat | 730-01831 | 1 | INSRT,CDBD,RR,53-5/8X8,M224 | |
| Shipping Mat | 730-01832 | 8 | CORNER PAD,HORN,TORO | |
| Shipping Mat | 730-01833 | 2 | INSRT,CDBD,END,13-1/4X8,M224 | |
| Shipping Mat | 730-01834 | 1 | INSRT,CDBD,TOP,27-1/4X17,M224 | |
| Shipping Mat | 730-03727 | 1 | BAG,CLEAR,9X14X.004 | REMOTE CONTROL PKG |

## 7.19 115V Fuse Option

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Fuses | 440-01624 | 1 | FUSE,3AG,SLO-BLO,3AMP,250V | PICK AND ADD TO CHASSIS CAGE KIT #023-03021 (M224XL), #023-03706 (M224X) OR #023-03028 (M224) |

## 7.20 230V Fuse Option

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Fuses | 440-01876 | 1 | FUSE,5X20MM,SLO-BLO,1.6AMP | |
| Electronic Hdwr | 600-01878 | 1 | FUSE,ADAPTOR,5X20MM TO 3AG | |

## 7.21 RS232 Option

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Conn Hdwr | 527-00138 | 2 | CONN,D-SUB,JACKSOCKET | WITH ACCOMPANYING HARDWARE [(1) #4 SPLIT LOCK WASHER AND (1) #4 NUT] |
| Cables/Cords | 680-01519 | 1 | CABLE,D-25F to 26C EDGE,30" | |

## 7.22 V8.1 Retrofit

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Cust Literature | 070-03261 | 1 | INSTR,SOFT-UP RETRO,V8.1,M224X | THIS INCLUDES UPDATED SECTIONS OF OWNER'S MANUAL |

## 7.23 RCH RPL Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Potentiometers | 200-01445 | 6 | POT,SLD,PC,10K-U,25MM X 45MM | R5-10 |
| Carbon Flm Res | 202-00522 | 2 | RES,CF,5%,1/4W,360 OHM | R3,4 |
| Carbon Flm Res | 202-00529 | 1 | RES,CF,5%,1/4W,1K OHM | R1 |
| Carbon Flm Res | 202-00543 | 2 | RES,CF,5%,1/4W,5.1K OHM | R11,12 |
| Carbon Flm Res | 202-00561 | 1 | RES,CF,5%,1/4W,36K OHM | R2 |
| Network Res | 205-00330 | 3 | RES,NET,SIP,2%,3.3KX9 | RP1-3 |
| Electrolyt Cap | 240-00619 | 1 | CAP,ELEC,1000uF,25V,AX | C11 |
| Tantalum Cap | 241-00651 | 1 | CAP,TANT,.22uF,35V,RAD | C4 |
| Tantalum Cap | 241-00652 | 1 | CAP,TANT,4.7uF,25V,RAD | C3 |
| Mica Cap | 242-00634 | 1 | CAP,MICA,100pF,DM-15,101J | C9 |
| Ceramic Cap | 245-00588 | 1 | CAP,CER,100pF,1000V,10% | C1 |
| Ceramic Cap | 245-00598 | 12 | CAP,CER,.01uF,16V,80/20% | 6 SLIDE POT BYPASSES,C2,5-8,12 |
| Diodes | 300-01030 | 4 | DIODE,1N4004 AND 4005 | CR1-4 |
| Digital/CMOS IC | 330-00697 | 1 | IC,DIGITAL,74LS10 | U7 |
| Digital/CMOS IC | 330-00768 | 1 | IC,DIGITAL,4049,CMOS | U12 |
| Digital/CMOS IC | 330-01290 | 2 | IC,DIGITAL,74LS244 | U8,11 |
| Digital/CMOS IC | 330-01297 | 1 | IC,DIGITAL,74LS42 | U6 |
| Digital/CMOS IC | 330-01316 | 1 | IC,DIGITAL,74LS123 | U2 |
| Digital/CMOS IC | 330-01592 | 1 | IC,DIGITAL,74LS132 | U1 |
| Linear IC | 340-00742 | 1 | IC,LINEAR,7805 (LM 340 T-5) | U3 |
| Interface IC | 345-01305 | 2 | IC,INTER,SN75327 N | U9,10 |
| Interface IC | 345-01306 | 2 | IC,INTER,SN75326 N | U4,5 |
| Converter IC | 355-01280 | 1 | ADC-0817 | U13 |
| PC Mnt Conn | 510-01504 | 1 | CONN,D-SUB,25FC,MB,PCRA | J2 |
| PC Mnt Conn | 510-01505 | 0 | CONN,D-SUB,25FC,MB,PCRA,2ND | |
| Sockets | 520-00942 | 2 | IC SCKT,14 PIN,PC,LO-PRO | U1,7 |
| Sockets | 520-00943 | 7 | IC SCKT,16 PIN,PC,LO-PRO | U2,4-6,9,10,12 |
| Sockets | 520-00946 | 1 | IC SCKT,40 PIN,PC,LO-PRO | U13 |
| Sockets | 520-01361 | 2 | IC SCKT,20 PIN,PC,LO-PRO | U8,11 |
| Machine Screws | 640-01706 | 2 | SCRW,4-40X3/8,PNH,PH,ZN | J2 |
| Machine Screws | 640-01714 | 1 | SCRW,6-32X3/8,PNH,PH,SS | U3 |
| Machine Screws | 640-02746 | 6 | SCRW,2-M3X.5MMX.175L,PNH,PH,ZN | R5-10 GND |
| Nuts | 643-01730 | 1 | NUT,6-32,KEP,SMALL,ZN | U3 |
| Nuts | 643-01732 | 2 | NUT,4-40,KEP,ZN | J2 |
| Heat Sinks | 704-01503 | 1 | HEAT SINK,PA1-1CB | |
| PC Boards | 710-01443 | 1 | PC BD,REM PAN LOG,M224 | |

## 7.24 RCH RPD Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00501 | 8 | RES,CF,5%,1/2W,150 OHM | R1-8 |
| Diodes | 300-01023 | 3 | DIODE,1N283 | CR16-18 |
| Dsply/Ind/LED | 430-01212 | 15 | LED,HP #5082-4480 | CR1-15 |
| Dsply/Ind/LED | 430-01507 | 3 | LED,DSPLY,5082-7613 | D0-2 |
| Psh But Switch | 453-01508 | 16 | SW,PBM,1P2T,DIGITST,ILLUM,.5W | S1-16 |
| Psh But Switch | 453-01509 | 6 | SW,PBM,1P2T,DIGITST,ILLUM,.69W | S17-22 |
| Bulk Wire | 670-01506 | 1 | CABLE,FLEX-JUMP,27 COND,1X0.1 | J1 |
| PC Boards | 710-01444 | 1 | PC BD,REM PAN DSPLY,M224 | |

## 7.25 RCH Hardware

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Conn Hdwr | 527-00138 | 2 | CONN,D-SUB,JACKSOCKET | |
| Grommets | 540-01502 | 1 | GUARD,DUST,M224 | |
| Feet | 541-00781 | 4 | BUMPER,FEET,3-M #SJ5025 | |
| Knobs/Caps | 550-01499 | 6 | BUTTON,TANG,BLK | |
| PC Hdwr | 610-01241 | 2 | GUIDE,CIRCUIT BD | |
| Spcr,Non-Insul | 635-01500 | 4 | SPCR,#6CLX3/8,1/4RD,AL | |
| Spcr,Non-Insul | 635-01501 | 4 | SPCR,6-32X5/8,1/4HEX,AL | |
| Machine Screws | 640-01709 | 4 | SCRW,6-32X3/16,PNH,PH,BLK | |
| Machine Screws | 640-03713 | 4 | SCRW,6-32X1/4,PNH,PH,SEMS,ZN | |
| Nuts | 643-01732 | 2 | NUT,4-40,KEP,ZN | |
| Chassis/Mech | 700-01449 | 1 | COVER,BOT,REM CNTRL,M224/224X | |
| Chassis/Mech | 700-02696 | 1 | COVER,TOP,REM CNTRL BOX,M224X | |
| Lens/Plate/Panl | 703-01498 | 1 | LENS,DISPLAY,M224 | |

## 7.26 LARC Transition Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00529 | 1 | RES,CF,5%,1/4W,1K OHM | R4 |
| Carbon Flm Res | 202-00549 | 3 | RES,CF,5%,1/4W,10K OHM | R1-3 |
| Electrolyt Cap | 240-00622 | 1 | CAP,ELEC,4700uF,16V,AX | C9 |
| Ceramic Cap | 245-00590 | 2 | CAP,CER,150pF,500V,10% | C4,5 |
| Ceramic Cap | 245-00594 | 1 | CAP,CER,.001uF,500V,10%,Z5F | C7 |
| Ceramic Cap | 245-00598 | 2 | CAP,CER,.01uF,16V,80/20% | C3,6 |
| Ceramic Cap | 245-01651 | 3 | CAP,CER,.1uF,50V,80/20% | C1,2,8 |
| Inductors | 270-00779 | 2 | FERRITE,BEAD | FB1,2 |
| Diodes | 300-01032 | 4 | DIODE,1N5404 | CR1-4 |
| Digital/CMOS IC | 330-00692 | 1 | IC,DIGITAL,74LS00 | U3 |
| Interface IC | 345-01584 | 1 | IC,INTER,DS1488N | U1 |
| Interface IC | 345-01585 | 1 | IC,INTER,DS1489AN | U2 |
| Interface IC | 345-03207 | 1 | IC,INTER,uA9638,LINE DRVR | U5 |
| Interface IC | 345-03208 | 1 | IC,INTER,uA9637A,LINE RCVR | U4 |
| Cable Conn | 490-02356 | 5 | CONN,JUMPER,.1X025,2FCG | W1-5 |
| PC Mnt Conn | 510-01480 | 1 | CONN,POST,156X045,HDR,3MCG,LOK | J3 |
| PC Mnt Conn | 510-01481 | 1 | CONN,POST,156X045,HDR,6MCG,LOK | J1 |
| PC Mnt Conn | 510-02671 | 5 | CONN,POST,100X025,HDR,3MC,GOLD | W1-5 |
| PC Mnt Conn | 510-03551 | 1 | CONN,D-SUB,9FC,MB,PC | J5 |
| Sockets | 520-00941 | 2 | IC SCKT,8 PIN,PC,LO-PRO | U4,5 |
| Sockets | 520-00942 | 3 | IC SCKT,14 PIN,PC,LO-PRO | U1-3 |
| Spcr,Non-Insul | 635-03528 | 2 | SPCR,SWAGE,4-40X3/8,1/4RD,BR/N | J5 |
| Spcr,Non-Insul | 635-03529 | 1 | SPCR,SWAGE,6-32X7/16,1/4RD,BR | |
| Cables/Cords | 680-03490 | 1 | CABLE,XITION/EDGE,26 COND,30" | J2 |
| PC Boards | 710-03442 | 1 | PC BD,XITION BD,M224X | |

## 7.27 LARC Hardware Kit

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Cable Conn | 490-02416 | 4 | SPLICE,INS-DSP,2 WIRE | NEW XITION BD |
| Cable Conn | 490-02712 | 1 | CONN,POST,156X045,INS-DSP,6FCG | |
| Conn Hdwr | 527-00138 | 2 | CONN,D-SUB,JACKSOCKET | NEW XITION BD MTG |
| Strain Rel | 530-02489 | 3 | TIE,CABLE,NYL,.1"X4" | NEW XITION BD MTG |
| Machine Screws | 640-01705 | 2 | SCRW,4-40X5/16,PNH,PH,ZN | ADAPTOR PLATE MTG |
| Machine Screws | 640-01710 | 1 | SCRW,6-32X1/4,PNH,PH,ZN | NEW XITION BD MTG |
| Machine Screws | 640-02404 | 4 | SCRW,6-32X13/16,PNH,PH,ZN | FUSE BD TO XFORMER |
| Nuts | 643-01732 | 2 | NUT,4-40,KEP,ZN | ADAPTOR PLATE MTG |
| Nuts | 643-03538 | 4 | NUT,6-32,SPEED,SLF RETAIN,.093 | FUSE BD TO XFORMER |
| Washers | 644-01740 | 1 | WSHR,LOCK,SPLIT,#6 | NEW XITION BD MTG |
| Pre-Cut Wire | 675-02863 | 1 | WIRE,18G,BLK,14",ST&T1/4XO | |
| Pre-Cut Wire | 675-02868 | 1 | WIRE,18G,RED,14",ST&T1/4XO | |
| Pre-Cut Wire | 675-02877 | 1 | WIRE,18G,PRP,14",ST&T1/4XO | |
| Pre-Cut Wire | 675-03651 | 1 | WIRE,18G,ORN,12" | |
| Panels | 702-03537 | 1 | PLATE,ADAPTOR,DB-25 TO DE-9 | |
| Plastics | 720-00436 | 1 | TAPE,FOAM,1/2X1/16X7-1/2 | |
| Plastics | 720-01879 | 2 | TAPE,FOAM,1/2X1/8X7-1/2 | |

## 7.28 LARC ROM/RAM Kit

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Digital/CMOS IC | 330-02504 | 2 | IC,DIGITAL,74S157 | U18,36 |
| Memory IC | 350-01304 | 3 | IC,EPROM,2716 | U23,24,25 |
| Memory IC | 350-02427 | 7 | IC,EPROM,4KX8,350NS,2732 | U1-4,9-11 |
| Memory IC | 350-03439 | 16 | IC,DRAM,4164,64KX1,150NS | U20-35 |
| Microproc IC | 365-01583 | 1 | IC,uPROC,8251 A | U22 |
| Bulk Wire | 670-01974 | 5 | WIRE,JMP,22AWG,0.1",NON-INSUL | J1-5 |
| Plastics | 720-03002 | 2 | FOAM,CONDUCTIVE,1/4" SHEET | CUT TO 5" x 3-1/2" |
| Shipping Mat | 730-01835 | 2 | BAG,CONDUCTIVE,4.25X8X.004 | |

## 7.29 LARC Shipping Kit

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Cust Literature | 070-02813 | 1 | CARD,WARRANTY,LEXICON | |
| Cust Literature | 070-03695 | 1 | MANUAL,OWNER'S,224XL | |
| Cust Literature | 070-03739 | 1 | INSTR,RETROFIT,LARC,M224X | |
| Cust Literature | 070-03759 | 1 | INSTR,PANEL MOUNT,LARC | |
| Fuses | 440-01624 | 1 | FUSE,3AG,SLO-BLO,3AMP,250V | PUT IN POLY BAG #730-02824 |
| Fuses | 440-01876 | 1 | FUSE,5X20MM,SLO-BLO,1.6AMP | PUT IN POLY BAG #730-02824 |
| Insul/Spacrs | 630-00953 | 2 | WSHR,FL,#6CLX3/8ODX1/16,FBR | PUT IN POLY BAG #730-02824 |
| Spcr,Non-Insul | 635-03720 | 2 | SPCR,6-32X1/2,1/4HEX,BR/N | PUT IN POLY BAG #730-02824 |
| Cables/Cords | 680-03525 | 1 | CABLE,50',LURCH | |
| Cables/Cords | 680-03690 | 1 | CABLE,CASSETTE INTERFACE | |
| Shipping Mat | 730-02824 | 1 | BAG,CLEAR,3X5X.002 | STAPLE TO PANEL MOUNT INSTR |
| Shipping Mat | 730-03085 | 1 | BOX,OUT,23X18.5X7.75 | |
| Shipping Mat | 730-03724 | 1 | BOX,5-1/2X3-7/8X2 | |
| Shipping Mat | 730-03727 | 1 | BAG,CLEAR,9X14X.004 | REMOTE CONTROL PKG |
| Label/Nameplts | 740-00000 | 1 | LABEL/NMPL | LABEL,RETURN SHIPPING |
| Tools | 780-01925 | 1 | TOOL,IC EXTRACTOR | |

## 7.30 LARC Display Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Ceramic Cap | 245-01651 | 4 | CAP,CER,.1uF,50V,80/20% | C1-4 |
| Dsply/Ind/LED | 430-03413 | 6 | LED,DSPLY,4-CHAR,DL-1414 | U1-4 |
| Dsply/Ind/LED | 430-04985 | 8 | LED,DSPLY,STICK,4 RED | CR1-32 |
| Sockets | 520-02718 | 4 | SOCKET STRIP,MACH,.100X020 | CR1-32, 4 LENGTHS OF 1.6" EA |
| Bulk Wire | 670-03530 | 1 | CABLE,FLEX-JUMP,29C,1.5X0.1 | P3 |
| PC Boards | 710-03393 | 1 | PC BD,DISPLAY BD,LURCH | |

## 7.31 LARC Electronics Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Potentiometers | 200-01445 | 6 | POT,SLD,PC,10K-U,25MM X 45MM | R23-28 |
| Trim Resistors | 201-00439 | 1 | RES,TRM,ST,PC,25K,SA,CER | R9 |
| Carbon Flm Res | 202-00502 | 1 | RES,CF,10%,1/2W,270 OHM | R22 |
| Carbon Flm Res | 202-00514 | 2 | RES,CF,5%,1/4W,100 OHM | R12,13 |
| Carbon Flm Res | 202-00523 | 1 | RES,CF,5%,1/4W,390 OHM | R20 |
| Carbon Flm Res | 202-00524 | 2 | RES,CF,5%,1/4W,470 OHM | R10,30 |
| Carbon Flm Res | 202-00529 | 3 | RES,CF,5%,1/4W,1K OHM | R6,14,29 |
| Carbon Flm Res | 202-00534 | 1 | RES,CF,5%,1/4W,2.2K OHM | R3 |
| Carbon Flm Res | 202-00538 | 3 | RES,CF,5%,1/4W,3.3K OHM | R1,4,31 |
| Carbon Flm Res | 202-00542 | 3 | RES,CF,5%,1/4W,4.7K OHM | R15,18,19 |
| Carbon Flm Res | 202-00549 | 2 | RES,CF,5%,1/4W,10K OHM | R8,11 |
| Carbon Flm Res | 202-00556 | 1 | RES,CF,5%,1/4W,22K OHM | R21 |
| Carbon Flm Res | 202-00563 | 2 | RES,CF,5%,1/4W,47K OHM | R7,17 |
| Carbon Flm Res | 202-00564 | 1 | RES,CF,5%,1/4W,51K OHM | R2 |
| Carbon Flm Res | 202-00571 | 1 | RES,CF,5%,1/4W,110K OHM | R5 |
| Carbon Flm Res | 202-00580 | 1 | RES,CF,5%,1/4W,1M OHM | R16 |
| Network Res | 205-03531 | 4 | RES,NET,SIP,2%,10KX5 | RP1-4 |
| Electrolyt Cap | 240-00609 | 3 | CAP,ELEC,10uF,16V,RAD | C9,17,39 |
| Electrolyt Cap | 240-00616 | 1 | CAP,ELEC,470uF,16V,AX | C41 |
| Electrolyt Cap | 240-00619 | 1 | CAP,ELEC,1000uF,25V,AX | C36 |
| Electrolyt Cap | 240-02048 | 1 | CAP,ELEC,47uF,25V,AX | C37 |
| Tantalum Cap | 241-00652 | 1 | CAP,TANT,4.7uF,25V,RAD | C26 |
| Ceramic Cap | 245-00585 | 2 | CAP,CER,18pF,100V,10% | C24,25 |
| Ceramic Cap | 245-00590 | 1 | CAP,CER,150pF,500V,10% | C1 |
| Ceramic Cap | 245-00594 | 5 | CAP,CER,.001uF,500V,10%,Z5F | C18,23,27,29,40 |
| Ceramic Cap | 245-00598 | 15 | CAP,CER,.01uF,16V,80/20% | C2,4,10-16,19-22,34,38 |
| Ceramic Cap | 245-01651 | 12 | CAP,CER,.1uF,50V,80/20% | C3,5-8,28,30-32,33,35,42 |
| Inductors | 270-00779 | 10 | FERRITE,BEAD | FB1-9,FB10 |
| Inductors | 270-03497 | 1 | INDUCTOR,300uH,1A,SWITCHING | L1 |
| Diodes | 300-01024 | 1 | DIODE,1N746 | CR6 |
| Diodes | 300-01029 | 4 | DIODE,1N914 AND 4148 | CR1-4 |
| Diodes | 300-02401 | 1 | DIODE,BAR 35,SCHOTTKY,LOW VF | CR5 |
| Diodes | 300-03498 | 1 | DIODE,SCHOTTKEY,POWER,3A | CR8 |
| Diodes | 300-03546 | 1 | DIODE,BRIDGE,2A,200V | CR7 |
| Transistors | 310-03438 | 1 | TRANSISTOR,IRFD9120,FET | Q1 |
| Digital/CMOS IC | 330-00767 | 1 | IC,DIGITAL,4013,CMOS | U10 |
| Digital/CMOS IC | 330-00768 | 1 | IC,DIGITAL,4049,CMOS | U6 |
| Digital/CMOS IC | 330-03496 | 1 | IC,DIGITAL,CD4515,CMOS | U11 |
| Linear IC | 340-00725 | 1 | IC,LINEAR,LM311 | U1 |
| Linear IC | 340-03499 | 1 | IC,LINEAR,MC34060 OR TL494 | U12 |
| Interface IC | 345-00751 | 1 | IC,INTER,75492,LED DRVR | U4 |
| Interface IC | 345-02913 | 1 | IC,INTER,NE594,DSP DRVR,8-SEG | U7 |
| Interface IC | 345-03207 | 1 | IC,INTER,uA9638,LINE DRVR | U3 |
| Interface IC | 345-03208 | 1 | IC,INTER,uA9637A,LINE RCVR | U2 |
| Converter IC | 355-02903 | 1 | IC,CONVERTER,ADC 0809 | U5 |
| Microproc IC | 365-03524 | 1 | IC,uPROC,8749,EPROM | U9 (PICK AND DELIVER TO TEST) |
| Microproc IC | 365-03526 | 1 | IC,uPROC,CDP1854 or IM6402 | U8 |
| Crystals | 390-02210 | 1 | CRYSTAL,4.608 MHz | Y1 |
| Fuses | 440-02466 | 1 | FUSE,1AG,FAST,1AMP,32V | F1 |
| Cable Conn | 490-00998 | 1 | CONN,DIN,5FC,180DEG | J0 |
| PC Mnt Conn | 510-03088 | 1 | CONN,POST,100X025,HDR,10MCG | W1 (BREAK INTO 2 LENGTHS OF 5 EA) |
| PC Mnt Conn | 510-03484 | 1 | CONN,DC POWER,PC,SMK S-G9314 | J2 |
| PC Mnt Conn | 510-03549 | 1 | CONN,D-SUB,9MC,FB,PCRA | J1 |
| Sockets | 520-00941 | 3 | IC SCKT,8 PIN,PC,LO-PRO | U1-3 |
| Sockets | 520-00942 | 2 | IC SCKT,14 PIN,PC,LO-PRO | U4,10 |
| Sockets | 520-00943 | 2 | IC SCKT,16 PIN,PC,LO-PRO | U6,12 |
| Sockets | 520-00945 | 1 | IC SCKT,24 PIN,PC,LO-PRO | U11 |
| Sockets | 520-00946 | 2 | IC SCKT,40 PIN,PC,LO-PRO | U8,9 |
| Sockets | 520-01458 | 1 | IC SCKT,28 PIN,PC,LO-PRO | U5 |
| Sockets | 520-02177 | 1 | IC SCKT,18 PIN,PC,LO-PRO | U7 |
| Electronic Hdwr | 600-00871 | 2 | FUSE CLIP,1/4",PC | F1 |
| Insul/Spacrs | 630-00953 | 2 | WSHR,FL,#6CLX3/8ODX1/16,FBR | COMPONENT SIDE ELECTRONICS BD TO ENCLOSURE, ATTACHED WITH PLIOBOND |
| Insul/Spacrs | 630-03544 | 2 | WSHR,FL,#6CLX3/8ODX.032,FBR | SUB-PNL TO CIRCUIT SIDE ELECT BD MTG, ATTACHED WITH PLIOBOND |
| Machine Screws | 640-01701 | 2 | SCRW,4-40X1/4,PNH,PH,ZN | DE-9 TO ELECT PCB MTG |
| Nuts | 643-01732 | 2 | NUT,4-40,KEP,ZN | DE-9 TO ELECT PCB MTG |
| Pre-Cut Wire | 675-02884 | 3 | WIRE,24G,WHT,1.5",ST&T1/4X1/4 | P1 TO J0 |
| Pre-Cut Wire | 675-03722 | 1 | WIRE,24G,WHT,2",ST&T1/4X1/4 | P1-1 TO J0-4 |
| PC Boards | 710-03398 | 1 | PC BD,ELECT BD,LURCH | |

## 7.32 LARC Panel Board

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Carbon Flm Res | 202-00509 | 8 | RES,CF,5%,1/4W,47 OHM | R5-12 |
| Carbon Flm Res | 202-00529 | 4 | RES,CF,5%,1/4W,1K OHM | R1-4 |
| Electrolyt Cap | 240-00609 | 1 | CAP,ELEC,10uF,16V,RAD | C1 |
| Ceramic Cap | 245-01651 | 4 | CAP,CER,.1uF,50V,80/20% | C2-5 |
| Diodes | 300-01023 | 8 | DIODE,1N283 | CR1-8 |
| Dsply/Ind/LED | 430-03413 | 6 | LED,DSPLY,4-CHAR,DL-1414 | U1-6 |
| Psh But Switch | 453-03440 | 26 | SW,PBM,1P1T,TANG,PC | SW1-16,18-22,26-30 |
| Sockets | 520-02718 | 4 | SOCKET STRIP,MACH,.100X020 | U1-6, NEED 12 LENGTHS OF .6" EACH |
| Knobs/Caps | 550-03390 | 6 | BUTTON,.57X.47,WHT | SW1-6 |
| Spcr,Non-Insul | 635-03542 | 2 | SPCR,SWAGE,#6CLX.594,1/4RD,BR | PNL BD TO ELECT BD MTG |
| Bulk Wire | 670-02837 | 1 | CABLE,FLEX-JUMP,19C,1.5X0.1 | P2 |
| Bulk Wire | 670-03530 | 1 | CABLE,FLEX-JUMP,29C,1.5X0.1 | P3 |
| PC Boards | 710-03404 | 1 | PC BD,PANEL BD,LURCH | |

## 7.33 LARC Finishing Kit

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Conn Hdwr | 527-00138 | 2 | CONN,D-SUB,JACKSOCKET | DE-9 TO CHASSIS BRKT MTG |
| Grommets | 540-03532 | 1 | GUARD,DUST,LURCH | |
| Knobs/Caps | 550-03388 | 6 | KNOB,SLIDE POT,WHITE | |
| Knobs/Caps | 550-03415 | 1 | BUTTON,.57X.47,"PROG" LEG,BLU | |
| Knobs/Caps | 550-03416 | 1 | BUTTON,.57X.47,"REG" LEG,BLU | |
| Knobs/Caps | 550-03417 | 1 | BUTTON,.57X.47,"0" LEG,WHT | |
| Knobs/Caps | 550-03418 | 1 | BUTTON,.57X.47,"1" LEG,WHT | |
| Knobs/Caps | 550-03419 | 1 | BUTTON,.57X.47,"2" LEG,WHT | |
| Knobs/Caps | 550-03420 | 1 | BUTTON,.57X.47,"3" LEG,WHT | |
| Knobs/Caps | 550-03421 | 1 | BUTTON,.57X.47,"4" LEG,WHT | |
| Knobs/Caps | 550-03422 | 1 | BUTTON,.57X.47,"5" LEG,WHT | |
| Knobs/Caps | 550-03423 | 1 | BUTTON,.57X.47,"6" LEG,WHT | |
| Knobs/Caps | 550-03424 | 1 | BUTTON,.57X.47,"7" LEG,WHT | |
| Knobs/Caps | 550-03425 | 1 | BUTTON,.57X.47,"8" LEG,WHT | |
| Knobs/Caps | 550-03426 | 1 | BUTTON,.57X.47,"9" LEG,WHT | |
| Knobs/Caps | 550-03427 | 1 | BUTTON,.57X.47,"VAR" LEG,WHT | |
| Knobs/Caps | 550-03428 | 1 | BUTTON,.57X.47,"BANK" LEG,WHT | |
| Knobs/Caps | 550-03429 | 1 | BUTTON,.57X.47,"STO" LEG,WHT | |
| Knobs/Caps | 550-03430 | 1 | BUTTON,.57X.47,"PARAM" LEG,WHT | |
| Knobs/Caps | 550-03431 | 1 | BUTTON,.57X.47,"MUTE" LEG,WHT | |
| Knobs/Caps | 550-03432 | 1 | BUTTON,.57X.47,"TAPE" LEG,WHT | |
| Knobs/Caps | 550-03433 | 1 | BUTTON,.57X.47,"2nd F" LEG,WHT | |
| Knobs/Caps | 550-03434 | 1 | BUTTON,.57X.47,"PAGE" LEG,WHT | |
| PC Hdwr | 610-02269 | 2 | HARDWARE,PC,RICHCO #MB-3-156 | DISPLAY BD TO PANEL BD |
| Spcr,Non-Insul | 635-01655 | 2 | SPCR,6-32X7/16,1/4HEX,AL | ELECT BD TO CASE MTG |
| Spcr,Non-Insul | 635-03541 | 2 | SPCR,#6CLX.355,1/4RD,BR/N | SUB-PNL TO PNL BD MTG |
| Machine Screws | 640-02378 | 4 | SCRW,6-32X7/16,TH,PH,BLK | PCB TO CASE MTG |
| Machine Screws | 640-02746 | 6 | SCRW,2-M3X.5MMX.175L,PNH,PH,ZN | R23-28 MTG (NOTE: DO NOT USE METRIC SCREWS PROVIDED WITH THE SLIDERS) |
| Machine Screws | 640-02812 | 2 | SCRW,4-40X3/8,PNH,PH,BLK | DIN TO CHASSIS BRKT MTG |
| Machine Screws | 640-03713 | 2 | SCRW,6-32X1/4,PNH,PH,SEMS,ZN | CONN BRKT TO PNL BD MTG |
| Thrd-Form Scrw | 641-03543 | 2 | SCRW,TAP,F,4-40X1/4,PNH,PH,ZN | DSPLY BD MTG |
| Nuts | 643-01733 | 2 | NUT,4-40,HEX,SMALL,ZN | DIN TO CHASSIS BRKT MTG |
| Washers | 644-01736 | 2 | WSHR,FL,#4CLX.218ODX.032THK | DSPLY BD MTG |
| Washers | 644-01737 | 2 | WSHR,LOCK,SPLIT,#4 | DIN TO CHASSIS BRKT MTG |
| Washers | 644-01747 | 6 | WSHR,INT STAR,#4 | |
| Washers | 644-02379 | 4 | WSHR,FL,#6CLX3/8ODX.049THK,BLK | PCB TO CASE MTG |
| Washers | 644-02716 | 2 | WSHR,FL,#4CLX.312ODX.03THK | DIN TO CHASSIS BRKT MTG |
| Chassis/Mech | 700-03391 | 1 | ENCLOSURE,BOTTOM,LURCH | |
| Chassis/Mech | 700-03392 | 1 | ENCLOSURE,TOP,LURCH | |
| Chassis/Mech | 700-03448 | 1 | CHASSIS,BRACKET,LURCH | |
| Panels | 702-03374 | 1 | PANEL,SUB,LURCH | |
| Panels | 702-03375 | 1 | PANEL,OVERLAY,LURCH | |
| Panels | 702-03545 | 1 | PROTECTIVE COVER,LURCH | |
| Lens/Plate/Panl | 703-00994 | 1 | TRIMPLATE,ALUM,FOIL,GP | CHASSIS BOTTOM |
| Lens/Plate/Panl | 703-03410 | 1 | LENS,DISPLAY,LURCH | |
| Plastics | 720-03548 | 2 | TAPE,FOAM,1/16X1/2X3.4 | BUMPER FEET |
| Plastics | 720-03673 | 1 | GASKET,DBL-STK,LURCH | LENS MTG |
| Label/Nameplts | 740-03676 | 1 | LABEL,LARC,PRODUCT ID & FCC | |

## 7.34 25' Cable Option

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Cables/Cords | 680-02045 | 1 | CABLE,CNTRL HD,SHLD,25FT,RND | PICK AND ADD TO FIN KIT #024-03700 (M224X) OR #022-03061 (M224) |

## 7.35 50' Cable Option

| Category | Part No. | Qty | Description | Reference |
|---|---|---|---|---|
| Cables/Cords | 680-02055 | 1 | CABLE,CNTRL HD,SHLD,50FT,RND | PICK AND ADD TO FIN KIT #022-03700 (M224X) OR #022-03061 (M224) |

---

## OCR & conversion notes

Source: *Lexicon Model 224X Service Manual*, Chapter 7 (Parts List), pp. 7-1 to 7-56. The PDF carries a machine-OCR text layer plus the rendered page images; where the two disagreed, the rendered image was treated as authoritative. Lexicon's own descriptions are inconsistent (e.g. spacing around `#`, `uf`/`uF`), so the items below are the deliberate, systematic decisions made during transcription, followed by per-section residual flags that still warrant a look at the high-res source.

### Systematic normalizations (applied silently throughout)

- **Inch marks.** OCR `11` rendered as `"` (e.g. `0.511` → `0.5"`, `.1"X411` → `.1"X4"`).
- **Outer-diameter token.** Washer specs `…3/80D…` / `…2180D…` normalized to `…3/8OD…` / `…218OD…` (letter **O** for *outer diameter*), matching the 480L parts-list house style.
- **`uf` → `uF`** in all capacitor descriptions.
- **Digit/letter confusions** corrected where unambiguous: `i%`/`1 O%` → `1%`/`10%`; `1/SW` → `1/8W`; `lK`/`lOK`/`lOOK` → `1K`/`10K`/`100K`; `lOpF`/`lOOpF`/`lOOOV` → `10pF`/`100pF`/`1000V`; `O.` → `0.`; `OWNER1S` → `OWNER'S`.
- **Quoted legends** on LARC buttons: OCR `11BANK11` → `"BANK"`, etc.
- **`DIOOE` → `DIODE`; `COMBO`/`MB«>RY` heading garble → `DATA MEMORY (DMEM)`.**
- **Card extractor:** all instances normalized to `EXTRACTOR,CARD,SCANBE#S-203` (p. 7-16 OCR'd the `#` as `U`).
- **Dropped quantities:** a blank Qty in the OCR has been set to **1** (every row in this manual carries Qty ≥ 1; the only genuine `0` is RPL board 510-01505, preserved).
- **`LURCH`** is kept verbatim wherever it appears (Lexicon codename for the LARC). The analogous 480L parts list prints `LARC` for several of the same parts (e.g. `CABLE,50'`), but the 224X source uses `LURCH`.

### Per-section residual flags

- **7.3 / 7.4 (AIN / AOUT converters).** 355-01362 reads `DAC-80-1` or `DAC-80-I`; the Burr-Brown DAC80 family uses letter suffixes (cf. AOUT 355-00774 `DAC,80-CBI-V`), so the intended value is likely `…-I` (current output). Left as the literal OCR (`DAC-80-1`) — verify against high-res.
- **7.8 (Memory Expansion).** 670-02037 reference `JUMPER 41-42, CUT (1) 4 1/2" PIECE` — the `41-42` token is OCR-uncertain (the rest of the note is clear).
- **7.11 (Power Supply #2).** The OCR text layer was badly garbled here; values were taken from the clean page render. Corrections: `201-01451`→**201-01461** (1K trim), `203-00451`→**203-00461** (2.43K), `203-01450`→**203-01460** (2.05K), `240-01445`→**240-01446** (3300µF), `240-00509`→**240-00609** (10µF), `242-00531`→**242-00631** (33pF), `510-01454`→**510-01464**. Trim-resistor refs resolve to **R6** (500 Ω, 201-00425) and **R5** (1K, 201-01461) — the OCR's duplicate "R5/R5" is wrong; 3300µF caps are **C6,10**.
- **7.13 (Power Supply Hardware).** 340-01463 services two boards; reference kept as `U3 (PS BD #2), U3 (PS BD #3)`.
- **7.15 (Chassis Hardware).** The reference column on this page is loosely spaced; the part→reference alignment was reconstructed by sequential 1:1 correspondence anchored from both ends of the list (30 parts ↔ 24 references, 6 left blank) and is internally self-consistent, but the column registration is the single most worthwhile thing to spot-check against the source. The blue 24G wire (675-03565) → **PWR FAIL SENSE**; spacer 635-01655 → **XLR MTG**.
- **7.30 (LARC Display Board).** This page carries **handwritten markup**. Row 2 of the displays printed `430-03414` (struck through) with a handwritten replacement that is hard to read; transcribed here as **430-04985 / Qty 8 / `LED,DSPLY,STICK,4 RED` / CR1-32** to match the identical part on the 480L LARC display board. (One pen reading looked like `…04685`; the `6`/`9` digit is the ambiguity — verify against the high-res scan.) The 4-char display row (430-03413, Qty 6) is reference **U1-4** as printed — note the same part is **U1-6** on the panel board (7.32), and Qty 6 vs. a 4-designator range is an original-source quirk, not OCR (the 480L lists it identically).
- **7.31 (LARC Electronics Board).** 330-00767 (U10) carries a handwritten "switch" scribble in the source; the printed part is transcribed as-is.
- **7.30 / 7.32 (sockets).** `SOCKET STRIP,MACH,.100X020` is kept as the 224X prints it; the 480L variant of 520-02718 reads `…,20C,.100X020` (the `20C` contact count is not in the 224X source).
- **7.34 / 7.35 (Cable Options).** The finishing-kit P/N prefixes differ between the two pages as printed: 7.34 cites `#024-03700 (M224X)`, 7.35 cites `#022-03700 (M224X)`. Both are transcribed verbatim; the `024`/`022` discrepancy is in the source.
