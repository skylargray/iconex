//============================================================================
// 74S287 - 256 x 4 bipolar TTL fuse PROM (TRI-STATE outputs) (74S287 family)
//----------------------------------------------------------------------------
// PART:       1024-bit field-programmable ROM organized as 256 words x 4 bits.
//             Factory-shipped with all outputs LOW (logic 0). A HIGH (logic 1)
//             may be programmed at any location by blowing the Ti-W fuse link.
//             TWO active-LOW output-enable inputs (/G1, /G2); when either is
//             HIGH, all four outputs go to HI-Z. BEHAVIORAL model.
// VARIATIONS: 74S287 / DM74S287 (National/TI) is functionally and pin-
//             compatible with the 82S129 (Signetics), 27S21 (AMD), 6301-1 (MMI),
//             24S10, HM7611, 93427. All are 256x4 tri-state bipolar PROMs.
//             (74S387 is the open-collector variant of the same pinout.)
//             Lexicon P/N: (verify against 224X parts list).
// IN 224XL:   Verify against U-IC map.
//
// PINOUT (DIP-16):
//    1  A6       16  VCC
//    2  A5       15  A7
//    3  A4       14  /G2
//    4  A3       13  /G1
//    5  A0       12  Q0
//    6  A1       11  Q1
//    7  A2       10  Q2
//    8  GND       9  Q3
//
// FUNCTION:
//   /G1 = LOW AND /G2 = LOW: Q0..Q3 = stored data at address A7..A0.
//   /G1 = HIGH OR  /G2 = HIGH: Q0..Q3 = HI-Z (3-state off).
//   Address bits: A0 (pin 5) is LSB; A7 (pin 15) is MSB.
//   Outputs Q0 (pin 12) .. Q3 (pin 9): Q0 = LSB of word.
//============================================================================
// SRC: MAME wiki PROM cross-reference ASCII pinout (74S287 = 82S129 = 27S21 =
//      same DIP-16 map); confirmed against NSC DM74S287 connection diagram
//      signal names (A0-A7, G1, G2, Q0-Q3, 16-pin, VCC=16, GND=8).
//      Confirm against schematic 060-01318.
