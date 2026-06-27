//============================================================================
// 74LS174 - hex D flip-flop, common clock + clear          (74x174 family)
//----------------------------------------------------------------------------
// PART:       Six positive-edge D flip-flops with a common clock and common
//             asynchronous active-LOW clear. True (Q) outputs only.
// VARIATIONS: 74174 / 74LS174 / 74S174 / 74F174 share function AND pinout.
//             Lexicon P/N: 330-00713 (74LS174).
// IN 224XL:   T&C (7.6): U9.
//
// PINOUT (DIP-16):
//    1  /CLR      16  VCC
//    2  Q0        15  Q5
//    3  D0        14  D5
//    4  D1        13  D4
//    5  Q1        12  Q4
//    6  D2        11  D3
//    7  Q2        10  Q3
//    8  GND        9  CLK
//
// FUNCTION:
//   /CLR = LOW -> all Qn = 0 (asynchronous, overrides clock).
//   Rising edge of CLK: Qn <= Dn  (n = 0..5).
//============================================================================
// SRC: KiCad 74xx.lib pin map + U.Toronto CSC258 sheet (identical).
//      Confirm against schematic 060-01318.
