//============================================================================
// 74LS155 - dual 2-to-4 decoder/demux, common select       (74x155 family)
//----------------------------------------------------------------------------
// PART:       Two 2-to-4 decoders with COMMON select inputs A (LSB) and B.
//             Each half has a strobe (/G) and a data input (C). Active-LOW
//             outputs. The two halves' data polarity differs so that tying
//             1C+2C as a 3rd address bit yields a 3-to-8 decoder.
// VARIATIONS: 74155 / 74LS155 / 74S155 share function AND pinout.
//             Lexicon P/N: 330-01284 (74LS155).
// IN 224XL:   T&C (7.6): U46.
//
// PINOUT (DIP-16):
//    1  1C       16  VCC
//    2  /1G      15  2C
//    3  B        14  /2G
//    4  1/Y3     13  A
//    5  1/Y2     12  2/Y3
//    6  1/Y1     11  2/Y2
//    7  1/Y0     10  2/Y1
//    8  GND       9  2/Y0
//
// FUNCTION (select = B,A with A = LSB; outputs active LOW):
//   Decoder 1: /1G = LOW AND 1C = HIGH -> selected 1Yn = LOW; else all HIGH.
//   Decoder 2: /2G = LOW AND 2C = LOW  -> selected 2Yn = LOW; else all HIGH.
//   3-to-8 use: tie 1C=2C = MSB address; combine 1Y/2Y as Y0..Y7.
//============================================================================
// SRC: KiCad 74xx.lib pin map; function per CalStateLA digital-lab IC specs.
//      Confirm against schematic 060-01318.
