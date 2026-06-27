//============================================================================
// 74LS00 - quad 2-input NAND gate                          (74x00 family)
//----------------------------------------------------------------------------
// PART:       Four independent 2-input NAND gates.  Yn = ~(An & Bn).
// VARIATIONS: 7400 / 74LS00 / 74S00 / 74F00 share function AND pinout.
//             Lexicon P/Ns: 330-00692 (74LS00), 330-01270 (74S00).
// IN 224XL:   74LS00 (330-00692): ARU U14,U26,U27,U28,U40,U41,U50,U51,U52,U53
//                                  ; DMEM U53.
//             74S00  (330-01270): DMEM U44 ; T&C U40,U48,U51.
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
//   1Y=~(1A&1B)  2Y=~(2A&2B)  3Y=~(3A&3B)  4Y=~(4A&4B)
//   Output LOW only when both inputs of a gate are HIGH.
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet; standard '00 (all families).
//      Confirm against schematic 060-01318.
