//============================================================================
// 74LS20 - dual 4-input NAND gate                          (74x20 family)
//----------------------------------------------------------------------------
// PART:       Two independent 4-input NAND gates.  Yn = ~(An & Bn & Cn & Dn).
//             Pins 3 and 11 are no-connect.
// VARIATIONS: 7420 / 74LS20 / 74S20 / 74F20 share function AND pinout.
//             Lexicon P/N: 330-00699 (74LS20).
// IN 224XL:   DMEM (7.5): U54.
//
// PINOUT (DIP-14):
//    1  1A       14  VCC
//    2  1B       13  2D
//    3  NC       12  2C
//    4  1C       11  NC
//    5  1D       10  2B
//    6  1Y        9  2A
//    7  GND       8  2Y
//
// FUNCTION:
//   1Y = ~(1A & 1B & 1C & 1D)   [inputs 1,2,4,5  -> out 6]
//   2Y = ~(2A & 2B & 2C & 2D)   [inputs 9,10,12,13-> out 8]
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet; standard '20 (all families).
//      Confirm against schematic 060-01318.
