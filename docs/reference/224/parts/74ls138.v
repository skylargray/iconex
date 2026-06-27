//============================================================================
// 74LS138 - 3-to-8 line decoder / demultiplexer           (74x138 family)
//----------------------------------------------------------------------------
// PART:       Decodes 3 address inputs (A,B,C) to one of eight active-LOW
//             outputs (Y0..Y7). Three enable inputs: G1 (active HIGH),
//             /G2A and /G2B (active LOW); all must be asserted to enable.
// VARIATIONS: 74138 / 74LS138 / 74S138 / 74F138 share function AND pinout.
//             Lexicon P/N: 330-01282 (74LS138).
// IN 224XL:   DMEM (7.5): U55, U56, U57.
//
// PINOUT (DIP-16):
//    1  A        16  VCC
//    2  B        15  /Y0
//    3  C        14  /Y1
//    4  /G2A     13  /Y2
//    5  /G2B     12  /Y3
//    6  G1       11  /Y4
//    7  /Y7      10  /Y5
//    8  GND       9  /Y6
//
// FUNCTION:
//   Enabled only when G1 = HIGH AND /G2A = LOW AND /G2B = LOW.
//   When enabled, the output selected by CBA (C=MSB) goes LOW; the other
//   seven stay HIGH. When disabled, all outputs HIGH.
//============================================================================
// SRC: KiCad 74xx.lib pin map; standard '138 (all families).
//      Confirm against schematic 060-01318.
