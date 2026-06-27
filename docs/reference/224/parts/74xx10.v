//============================================================================
// 74x10 - triple 3-input NAND gate                         (74x10 family)
//----------------------------------------------------------------------------
// PART:       Three independent 3-input NAND gates.  Yn = ~(An & Bn & Cn).
//             Same pin layout as the '11 (AND) and '27 (NOR).
// VARIATIONS: 7410 / 74LS10 / 74S10 / 74F10 share function AND pinout.
//             Lexicon P/Ns: 330-00697 (74LS10), 330-01273 (74S10).
// IN 224XL:   74LS10 (330-00697): T&C U49.
//             74S10  (330-01273): DMEM U43 ; T&C U36.
//
// PINOUT (DIP-14):
//    1  1A       14  VCC
//    2  1B       13  1C
//    3  2A       12  1Y
//    4  2B       11  3C
//    5  2C       10  3B
//    6  2Y        9  3A
//    7  GND       8  3Y
//
// FUNCTION:
//   1Y = ~(1A & 1B & 1C)   [inputs 1,2,13 -> out 12]
//   2Y = ~(2A & 2B & 2C)   [inputs 3,4,5  -> out 6 ]
//   3Y = ~(3A & 3B & 3C)   [inputs 9,10,11-> out 8 ]
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet; standard '10 (all families).
//      Confirm against schematic 060-01318.
