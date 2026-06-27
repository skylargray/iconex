//============================================================================
// 74x86 - quad 2-input exclusive-OR (XOR) gate            (74x86 family)
//----------------------------------------------------------------------------
// PART:       Four independent 2-input XOR gates.  Yn = An XOR Bn.
//             Combinational; output HIGH when the two inputs differ.
// VARIATIONS: 7486 / 74LS86 / 74S86 / 74F86 share function AND pinout.
//             Lexicon P/Ns: 330-01277 (74S86), 330-01313 (74LS86).
// IN 224XL:   ARU board (7.7): 74S86 at U5,U6,U7,U9,U42 ;  74LS86 at U8.
//             T&C board (7.6): 74LS86 at U12.
//
// PINOUT (DIP-14):
//    1  1A       14  VCC
//    2  1B       13  4B
//    3  1Y       12  4A
//    4  2A       11  4Y
//    5  2B       10  3B
//    6  2Y        9  3A
//    7  GND       8  3Y
//
// FUNCTION:
//   Gate 1: 1Y = 1A ^ 1B        Gate 3: 3Y = 3A ^ 3B
//   Gate 2: 2Y = 2A ^ 2B        Gate 4: 4Y = 4A ^ 4B
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet; standard '86 pinout (all families).
//      Confirm against schematic 060-01318.
