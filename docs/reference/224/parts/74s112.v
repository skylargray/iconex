//============================================================================
// 74S112 - dual JK flip-flop, negative-edge, preset+clear  (74x112 family)
//----------------------------------------------------------------------------
// PART:       Two NEGATIVE-edge-triggered JK flip-flops, each with independent
//             clock and active-LOW asynchronous preset (/PRE) and clear (/CLR).
//             16-pin package.
// VARIATIONS: 74112 / 74LS112 / 74S112 / 74F112 share function AND pinout.
//             Lexicon P/N: 330-01279 (74S112).
// IN 224XL:   T&C (7.6): U20, U21, U22, U26.
//
// PINOUT (DIP-16):
//    1  1CLK     16  VCC
//    2  1K       15  1/CLR
//    3  1J       14  2/CLR
//    4  1/PRE    13  2CLK
//    5  1Q       12  2K
//    6  1/Q      11  2J
//    7  2/Q      10  2/PRE
//    8  GND       9  2Q
//
// FUNCTION (per flip-flop, on FALLING edge of CLK):
//   /PRE = LOW -> Q = 1 (async).   /CLR = LOW -> Q = 0 (async).
//   J K = 0 0 -> HOLD       J K = 0 1 -> Q <= 0 (reset)
//   J K = 1 0 -> Q <= 1     J K = 1 1 -> TOGGLE (Q <= ~Q)
//============================================================================
// SRC: KiCad 74xx.lib pin map (74LS112, same pinout); '112 negative-edge.
//      Confirm against schematic 060-01318.
