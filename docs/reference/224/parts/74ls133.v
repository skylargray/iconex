//============================================================================
// 74LS133 - 13-input NAND gate                             (74x133 family)
//----------------------------------------------------------------------------
// PART:       Single 13-input NAND gate.  Y = ~(A&B&C&D&E&F&G&H&I&J&K&L&M).
//             Output LOW only when all 13 inputs are HIGH.
// VARIATIONS: 74133 / 74LS133 / 74S133 / 74F133 / 74HC133 share fn AND pinout.
//             Lexicon P/N: 330-01281 (74LS133).
// IN 224XL:   T&C (7.6): U50.
//
// PINOUT (DIP-16):
//    1  A         16  VCC
//    2  B         15  M
//    3  C         14  L
//    4  D         13  K
//    5  E         12  J
//    6  F         11  I
//    7  G         10  H
//    8  GND        9  Y (output)
//
// FUNCTION:
//   Y = ~(A & B & C & D & E & F & G & H & I & J & K & L & M)
//   Inputs A-G on pins 1-7; inputs H-M on pins 10-15; output Y on pin 9.
//============================================================================
// SRC: KiCad 74xx.lib (pin 8/16 = GND/VCC) + build-electronic-circuits +
//      Motorola SN54/74LS133 (output = pin 9). Confirm against 060-01318.
