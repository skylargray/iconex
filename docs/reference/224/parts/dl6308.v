//============================================================================
// DL6308 - 5-tap digital delay line  (Bel Fuse 0447-0150-02)
//----------------------------------------------------------------------------
// PART:       TTL active 5-tap digital delay line, 14-pin DIP. One input pulse
//             reappears at 5 tap outputs, each delayed 30 ns more than the last:
//             TAP1=30ns, TAP2=60ns, TAP3=90ns, TAP4=120ns, TAP5=150ns.
//             +5V supply; TTL-compatible outputs (~10 LS loads per tap).
// VARIATIONS: Bel Fuse 0447-0150-02 (this delay = 150 ns total, 30 ns/tap).
//             The 0447 / A447 series spans other total delays
//             (e.g. 0447-0050-02 = 50 ns total / 10 ns per tap).
//             Lexicon P/N: (TBD - owner).
// IN 224XL:   DMEM (7.5): U59 - sequences the DRAM RAS/CAS strobes (Fig 3.3);
//             the 30 / 60 / 150 ns taps are wired.
//
// PINOUT (DIP-14):   *** tap-pin order is NON-monotonic - read exactly ***
//    1  IN          14  VCC
//    2  NC          13  NC
//    3  NC          12  TAP1 (30 ns)
//    4  TAP2 (60ns) 11  NC
//    5  NC          10  TAP3 (90 ns)
//    6  TAP4(120ns)  9  NC
//    7  GND          8  TAP5 (150 ns)
//   => IN=1, TAP1=12, TAP2=4, TAP3=10, TAP4=6, TAP5=8, GND=7, VCC=14 ; NC=2,3,5,9,11,13
//
// FUNCTION:
//   TAPk(t) = IN(t - 30ns*k)   for k = 1..5   (buffered TTL taps).
//============================================================================
// SRC: pinout read from the Bel Fuse 0447 datasheet (datasheets/belfuse-0447.pdf),
//      owner-confirmed 2026-06-26; specs (5 taps, 30 ns/tap, 0447-0150-02) datasheet-
//      verified. Confirm in-circuit tap usage against schematic 060-02512 (dmem_U59).
