//============================================================================
// 74LS139 - dual 2-to-4 line decoder / demultiplexer       (74x139 family)
//----------------------------------------------------------------------------
// PART:       Two independent 2-to-4 decoders, each with its own active-LOW
//             enable (/E) and active-LOW outputs (Y0..Y3).
// VARIATIONS: 74139 / 74LS139 / 74S139 / 74F139 share function AND pinout.
//             Lexicon P/N: 330-01283 (74LS139).
// IN 224XL:   T&C (7.6): U47.
//
// PINOUT (DIP-16):
//    1  1E\      16  VCC
//    2  1A0      15  2E\
//    3  1A1      14  2A0
//    4  1Y0      13  2A1
//    5  1Y1      12  2Y0
//    6  1Y2      11  2Y1
//    7  1Y3      10  2Y2
//    8  GND       9  2Y3
//
// FUNCTION (per decoder):
//   /E = HIGH -> all outputs HIGH.
//   /E = LOW  -> output selected by (A1,A0) goes LOW; others HIGH. (A0 = LSB)
//============================================================================
// SRC: KiCad 74xx.lib pin map; standard '139 (all families).
//      Confirm against schematic 060-01318.
