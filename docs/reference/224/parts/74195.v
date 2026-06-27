//============================================================================
// 74195 - 4-bit parallel-access shift register            (74x195 family)
//----------------------------------------------------------------------------
// PART:       4-bit shift register, shift-right only, with synchronous
//             parallel load and asynchronous clear. Serial input is a J,/K
//             pair into Q0 (acts as D, T, set or reset depending on J,/K).
//             Positive-edge clocked. Both Q3 and /Q3 brought out.
// VARIATIONS: 74195 / 74LS195 / 74S195 share function AND pinout.
//             Lexicon P/N: 330-01289 (listed "74195").
// IN 224XL:   T&C (7.6): U10, U11.
//
// PINOUT (DIP-16):
//    1  /CLR      16  VCC
//    2  J         15  Q0
//    3  /K        14  Q1
//    4  P0        13  Q2
//    5  P1        12  Q3
//    6  P2        11  /Q3
//    7  P3        10  CLK
//    8  GND        9  SH//LD
//
// FUNCTION (rising edge of CLK, unless /CLR asserted):
//   /CLR = LOW          -> Q0..Q3 = 0 (asynchronous).
//   SH//LD = LOW        -> LOAD: (Q0..Q3) <= (P0..P3).
//   SH//LD = HIGH       -> SHIFT RIGHT: (Q1,Q2,Q3) <= (Q0,Q1,Q2);
//                          Q0 <= per J,/K:  J /K = 0 0 -> 0 ; 0 1 -> hold Q0;
//                          1 0 -> toggle /Q0 ; 1 1 -> 1.  (J=/K -> acts as D=J)
//============================================================================
// SRC: KiCad 74xx.lib pin map; function per CalStateLA digital-lab IC specs.
//      Confirm against schematic 060-01318.
