//============================================================================
// 74S175 - quad D flip-flop, common clock + async clear    (74x175 family)
//----------------------------------------------------------------------------
// PART:       Four positive-edge D flip-flops with a common clock and common
//             asynchronous active-LOW clear. Both Q and /Q are brought out.
// VARIATIONS: 74175 / 74LS175 / 74S175 / 74F175 share function AND pinout.
//             Lexicon P/Ns: 330-02505 (74S175), 330-00714 (74LS175).
// IN 224XL:   74S175  (330-02505): ARU U12.
//             74LS175 (330-00714): T&C U23, U52.
//
// PINOUT (DIP-16):
//    1  /CLR     16  VCC
//    2  Q0       15  Q3
//    3  /Q0      14  /Q3
//    4  D0       13  D3
//    5  D1       12  D2
//    6  /Q1      11  /Q2
//    7  Q1       10  Q2
//    8  GND       9  CLK
//
// FUNCTION:
//   /CLR = LOW -> all Qn = 0 (asynchronous, overrides clock).
//   Rising edge of CLK: Qn <= Dn ; /Qn <= ~Dn.
//============================================================================
// SRC: KiCad 74xx.lib pin map + U.Toronto CSC258 sheet (74LS175, identical).
//      Confirm against schematic 060-01318.
