//============================================================================
// 74F157 - quad 2-line-to-1-line multiplexer, non-inverting  (74x157 family)
//----------------------------------------------------------------------------
// PART:       Four 2:1 muxes with a common select and common enable. Selects
//             between two 4-bit words (A / B) -> Y. Non-inverting output
//             (the '158 is the inverting-output equivalent). Combinational.
// VARIATIONS: 74157 / 74LS157 / 74S157 / 74F157 share function AND pinout.
//             Lexicon P/N: 330-03340 (74F157).
//             (74S157, P/N 330-02504 on DMEM, is the same device - own file.)
// IN 224XL:   ARU board (7.7): U33, U34, U35, U36, U37.
//             T&C board (7.6): U28, U42.
//
// PINOUT (DIP-16):
//    1  SEL      16  VCC      SEL = A/B select          (pin 1)
//    2  1A       15  /G       /G  = output enable, LOW  (pin 15)
//    3  1B       14  4A
//    4  1Y       13  4B
//    5  2A       12  4Y
//    6  2B       11  3A
//    7  2Y       10  3B
//    8  GND       9  3Y
//
// FUNCTION:
//   /G = HIGH -> all outputs 1Y..4Y forced LOW (SEL ignored).
//   /G = LOW:  SEL = LOW  -> Yn = An   (A word selected)
//              SEL = HIGH -> Yn = Bn   (B word selected)
//============================================================================
// SRC: KiCad 74xx.lib pin map; function per CalStateLA digital-lab IC specs.
//      Confirm against schematic 060-01318.
