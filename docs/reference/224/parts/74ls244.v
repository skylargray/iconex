//============================================================================
// 74LS244 - octal buffer / line driver, 3-state, non-inverting (74x244)
//----------------------------------------------------------------------------
// PART:       Eight non-inverting 3-state buffers in two 4-bit groups, each
//             group with its own active-LOW output enable (/1G, /2G). 20-pin.
//             Typical use: bus driver. (The '240 is the inverting version.)
// VARIATIONS: 74244 / 74LS244 / 74S244 / 74F244 share function AND pinout.
//             Lexicon P/N: 330-01290 (74LS244).
// IN 224XL:   DMEM (7.5): U61, U62.
//             T&C (7.6): U6.
//
// PINOUT (DIP-20):
//    1  /1G      20  VCC      /1G = group-1 output enable, LOW (pin 1)
//    2  1A1      19  /2G      /2G = group-2 output enable, LOW (pin 19)
//    3  2Y4      18  1Y1
//    4  1A2      17  2A4
//    5  2Y3      16  1Y2
//    6  1A3      15  2A3
//    7  2Y2      14  1Y3
//    8  1A4      13  2A2
//    9  2Y1      12  1Y4
//   10  GND      11  2A1
//
// FUNCTION:
//   Group 1 (/1G): 1Yn = 1An when /1G = LOW, else high-impedance (Z).
//   Group 2 (/2G): 2Yn = 2An when /2G = LOW, else high-impedance (Z).
//   Non-inverting.
//============================================================================
// SRC: KiCad 74xx.lib pin map; standard '244 (non-inverting).
//      Confirm against schematic 060-01318.
