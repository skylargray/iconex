//============================================================================
// 74LS03 - quad 2-input NAND gate, OPEN-COLLECTOR outputs  (74x03 family)
//----------------------------------------------------------------------------
// PART:       Four 2-input NAND gates with open-collector outputs (require an
//             external pull-up; outputs may be wired-AND together). Same pin
//             layout as the '00, but '00 has totem-pole outputs.
// VARIATIONS: 7403 / 74LS03 / 74S03 share function AND pinout (all open-coll).
//             Lexicon P/N: 330-00694 (74LS03).
// IN 224XL:   DMEM (7.5): U52.
//             T&C (7.6): U55.
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
//   Outputs are open-collector: drive LOW or float (HIGH only via pull-up).
//============================================================================
// SRC: U.Toronto CSC258 pinout sheet ('03 shares '00 pin layout); standard.
//      Confirm against schematic 060-01318.
