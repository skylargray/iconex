//============================================================================
// 74LS670 - 4-by-4 register file, 3-state outputs        (74x670 family)
//----------------------------------------------------------------------------
// PART:       4 words x 4 bits register file. Independent read and write
//             address+enable allow reading one word while writing another,
//             simultaneously. Storage is latch-based (level), not edge.
//             Outputs are 3-state (bus-expandable).
// VARIATIONS: 74670 / 74LS670 / 74S670 share this function AND pinout.
//             *** The 74170 is the same logic but OPEN-COLLECTOR and a
//             DIFFERENT pinout - NOT interchangeable. ***
//             Lexicon P/N: 330-01296 (74LS670).
// IN 224XL:   ARU board (7.7): U29, U30, U31, U32.
//
// PINOUT (DIP-16):  *** pins 10/11 CORRECTED 2026-06-26 from datasheet (see SRC) ***
//    1  D2       16  VCC
//    2  D3       15  D1
//    3  D4       14  WA    (write address A)
//    4  RB       13  WB    (write address B)
//    5  RA       12  /GW   (write enable, active LOW)   [datasheet: EW]
//    6  Q4       11  /GR   (read enable,  active LOW)   [datasheet: ER]
//    7  Q3       10  Q1
//    8  GND       9  Q2
//
// FUNCTION:
//   WRITE: D1..D4 -> word selected by (WB,WA) while /GW = LOW (level-latched).
//          /GW = HIGH inhibits writing; stored data held.
//   READ:  word selected by (RB,RA) -> Q1..Q4 while /GR = LOW.
//          /GR = HIGH -> Q1..Q4 high-impedance (Z).
//   Read/write addresses are independent (simultaneous R/W ok).
//   Read is non-destructive. Bit mapping: Dn stored -> Qn.
//============================================================================
// SRC: pinout DATASHEET-VERIFIED from TI SDLS193 (datasheets/74670_TI.pdf), 2026-06-26.
//      CORRECTION: the prior map had pin10 and pin11 swapped (had pin10=/GR, pin11=Q1).
//      Datasheet is unambiguous: pin10=Q1, pin11=/GR (read enable). The 74670 is a
//      JEDEC-standard pinout (TI/Motorola/Fairchild identical). Confirm in-circuit
//      usage against schematic 060-01318 (ARU U29-U32).
