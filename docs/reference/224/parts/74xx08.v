//============================================================================
// 74x08 - quad 2-input AND gate                            (74x08 family)
//----------------------------------------------------------------------------
// PART:       Four independent 2-input AND gates.  Yn = An & Bn.
// VARIATIONS: 7408 / 74LS08 / 74S08 / 74F08 share function AND pinout.
//             Lexicon P/Ns: 330-00696 (74LS08), 330-01256 (74S08).
// IN 224XL:   74LS08 (330-00696): T&C U32, U34.
//             74S08  (330-01256): DMEM U45 ; T&C U35.
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
//   1Y=1A&1B  2Y=2A&2B  3Y=3A&3B  4Y=4A&4B
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet; standard '08 (all families).
//      Confirm against schematic 060-01318.
