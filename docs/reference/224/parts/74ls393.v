//============================================================================
// 74LS393 - dual 4-bit binary ripple counter               (74x393 family)
//----------------------------------------------------------------------------
// PART:       Two independent 4-bit binary (mod-16) ripple counters, each with
//             its own clock (CP) and active-HIGH master reset (MR). Counts on
//             the FALLING edge of CP.
// VARIATIONS: 74393 / 74LS393 / 74S393 / 74F393 share function AND pinout.
//             Lexicon P/N: 330-01295 (74LS393).
// IN 224XL:   DMEM (7.5): U51, U65.
//
// PINOUT (DIP-14):
//    1  1CP      14  VCC
//    2  1MR      13  2CP
//    3  1Q0      12  2MR
//    4  1Q1      11  2Q0
//    5  1Q2      10  2Q1
//    6  1Q3       9  2Q2
//    7  GND       8  2Q3
//
// FUNCTION (per counter; Q0 = LSB):
//   MR = HIGH -> Q0..Q3 = 0 (asynchronous).
//   MR = LOW  -> each FALLING edge of CP increments the 4-bit count
//                (ripple: Q1 toggles off Q0, Q2 off Q1, Q3 off Q2).
//============================================================================
// SRC: KiCad 74xx.lib pin map; standard '393 (ripple, MR active-HIGH).
//      Confirm against schematic 060-01318.
