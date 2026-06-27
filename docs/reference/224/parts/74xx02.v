//============================================================================
// 74x02 - quad 2-input NOR gate                            (74x02 family)
//----------------------------------------------------------------------------
// PART:       Four independent 2-input NOR gates.  Yn = ~(An | Bn).
//             NOTE: the '02 pinout puts the OUTPUT first (1Y on pin 1), unlike
//             the '00/'08 where the output is pin 3.
// VARIATIONS: 7402 / 74LS02 / 74S02 / 74F02 share function AND pinout.
//             Lexicon P/N: (TBD - owner).
// IN 224XL:   DMEM (7.5): U60 (74S02).
//
// PINOUT (DIP-14):
//    1  1Y       14  VCC
//    2  1A       13  4Y
//    3  1B       12  4B
//    4  2Y       11  4A
//    5  2A       10  3Y
//    6  2B        9  3B
//    7  GND       8  3A
//
// FUNCTION:
//   1Y=~(1A|1B) [2,3->1]   2Y=~(2A|2B) [5,6->4]
//   3Y=~(3A|3B) [8,9->10]  4Y=~(4A|4B) [11,12->13]
//============================================================================
// SRC: pinout DATASHEET-VERIFIED from TI (datasheets/7402_TI.pdf), 2026-06-26.
//      Confirm against schematic 060-02512 (DMEM U60).
