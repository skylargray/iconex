//============================================================================
// 74LS109 - dual JK flip-flop, positive-edge, preset+clear  (74x109 family)
//----------------------------------------------------------------------------
// PART:       Two POSITIVE-edge-triggered JK flip-flops, each with independent
//             clock and active-LOW asynchronous preset (/S) and clear (/R).
//             Distinctive input polarity: J is active-HIGH, /K is active-LOW
//             (i.e. assert K by pulling /K LOW). 16-pin package.
// VARIATIONS: 74109 / 74LS109 / 74S109 / 74F109 share function AND pinout.
//             Lexicon P/N: (verify against 224X parts list - not in current
//             lib74xx scope but included here for completeness).
// IN 224XL:   Verify against U-IC map.
//
// PINOUT (DIP-16):
//    1  1/R      16  VCC
//    2  1J       15  2/R
//    3  1/K      14  2J
//    4  1CLK     13  2/K
//    5  1/S      12  2CLK
//    6  1Q       11  2/S
//    7  1/Q      10  2Q
//    8  GND       9  2/Q
//
// FUNCTION (per flip-flop, on RISING edge of CLK):
//   /S = LOW -> Q = 1 (async preset).   /R = LOW -> Q = 0 (async clear).
//   /S = /R = LOW -> Q = 1, /Q = 1 (both asserted, undefined / disallowed).
//   J  /K = 0  1 -> HOLD (no change)     J  /K = 1  1 -> Q <= 1 (set)
//   J  /K = 0  0 -> Q <= 0 (reset)       J  /K = 1  0 -> TOGGLE (Q <= ~Q)
//   Note: /K=HIGH means K de-asserted; /K=LOW means K asserted.
//   This is the positive-edge complement of the 74S112 (negative-edge JK).
//============================================================================
// SRC: KiCad 74xx.lib pin map (74LS109, verified pin-by-pin). Function per
//      standard 74109 JK truth table (positive-edge, J active-H, /K active-L).
//      Confirm against schematic 060-01318.
