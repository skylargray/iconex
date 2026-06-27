//============================================================================
// 74x74 - dual D flip-flop, async preset+clear            (74x74 family)
//----------------------------------------------------------------------------
// PART:       Two positive-edge D flip-flops, each with independent clock and
//             independent active-LOW asynchronous preset (/PRE) and clear
//             (/CLR).
// VARIATIONS: 7474 / 74LS74 / 74S74 / 74F74 share function AND pinout.
//             Lexicon P/Ns: 330-00703 (74LS74), 330-01276 (74S74).
// IN 224XL:   74LS74 (330-00703): T&C U24, U53, U54.
//             74S74  (330-01276): DMEM U46 ; T&C U25.
//
// PINOUT (DIP-14):
//    1  1/CLR    14  VCC
//    2  1D       13  2/CLR
//    3  1CLK     12  2D
//    4  1/PRE    11  2CLK
//    5  1Q       10  2/PRE
//    6  1/Q       9  2Q
//    7  GND       8  2/Q
//
// FUNCTION (per flip-flop):
//   /PRE = LOW -> Q = 1 (async, overrides clock).
//   /CLR = LOW -> Q = 0 (async, overrides clock).
//   /PRE=/CLR=HIGH: rising edge of CLK -> Q <= D ; /Q <= ~D.
//============================================================================
// SRC: KiCad 74xx.lib pin map + U.Toronto CSC258 sheet (identical all fam).
//      Confirm against schematic 060-01318.
