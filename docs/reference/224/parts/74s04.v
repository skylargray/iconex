//============================================================================
// 74S04 - hex inverter                                     (74x04 family)
//----------------------------------------------------------------------------
// PART:       Six independent inverters.  Yn = ~An.
// VARIATIONS: 7404 / 74LS04 / 74S04 / 74F04 share function AND pinout.
//             Lexicon P/Ns: 330-01272 (74S04), 330-00695 (74LS04).
// IN 224XL:   74S04  (330-01272): ARU U2,U54 ; DMEM U58 ; T&C U37.
//             74LS04 (330-00695): T&C U33.
//
// PINOUT (DIP-14):
//    1  1A       14  VCC
//    2  1Y       13  6A
//    3  2A       12  6Y
//    4  2Y       11  5A
//    5  3A       10  5Y
//    6  3Y        9  4A
//    7  GND       8  4Y
//
// FUNCTION:
//   1Y=~1A  2Y=~2A  3Y=~3A  4Y=~4A  5Y=~5A  6Y=~6A
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet (74LS04, identical pinout all families).
//      Confirm against schematic 060-01318.
