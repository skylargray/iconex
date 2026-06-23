// Multiplier + saturation unit tests for the 224XL ARU primitives (firmware/
// schematic-resolved datapath; authority is tools/aru_datapath.py).
//
// The resolved per-multiply is:
//   * 6-bit signed coeff  Cs = +/-(abs(coeff7) >> 1)              [aruCoeff6]
//   * operand = x << 3,  prod = (operand * Cs) >> 6  (arith. >>)  [aruProd]
//     (net gain x * Cs / 64; the <<3/>>6 is the 17->20 bit operand alignment)
//   * 20-bit saturating accumulator, rails +/-524287              [aruSat20 / aruMac]
//   * result register RES = sat16(ACC >> 3), rails [-32768,32767] [aruSat16]
//
// Anchors: the firmware ADD'L MULT mapping confirms coefficient magnitude 124 ->
// C = 62 -> gain 62/64 = 0.969 (Service Manual 5.3 multiplier diagnostic).
// This test pins the representable mechanics: coeff folding, the <<3/>>6 product,
// floor-shift on negatives, and both saturation rails.
#include "sgdsp/reverb/224xl.hpp"
#include <cstdio>
#include <cstdint>

using sgdsp::reverb::aruCoeff6;
using sgdsp::reverb::aruProd;
using sgdsp::reverb::aruMac;
using sgdsp::reverb::aruSat16;
using sgdsp::reverb::aruSat20;
using sgdsp::reverb::AruAccum;

static int g_fail = 0;

static void check(const char* name, AruAccum got, AruAccum want)
{
    if (got != want) {
        std::printf("FAIL %-30s got=%lld want=%lld\n", name,
                    (long long)got, (long long)want);
        ++g_fail;
    } else {
        std::printf("ok   %-30s = %lld\n", name, (long long)got);
    }
}

int main()
{
    // ---- 6-bit coefficient folding: Cs = +/-(abs(coeff7) >> 1) ----
    check("coeff6 124 (ADD'L MULT 62)", aruCoeff6(124),  62);   // gain 62/64 = 0.969
    check("coeff6 126",                 aruCoeff6(126),  63);   // 126>>1
    check("coeff6 64",                  aruCoeff6(64),   32);   // 64>>1
    check("coeff6 1 (floors to 0)",     aruCoeff6(1),     0);   // 1>>1 == 0
    check("coeff6 -124",                aruCoeff6(-124),-62);   // sign via CSIGN
    check("coeff6 -1 (floors to 0)",    aruCoeff6(-1),    0);   // -(1>>1) == 0

    // ---- product term: prod = (x<<3)*Cs >> 6  (== x*Cs/64, floored) ----
    // 1000 * 62 / 64 = 62000/64 = 968.75 -> floor 968.  Via (8000*62)>>6 = 496000>>6 = 7750? no:
    // careful: (1000<<3)=8000; 8000*62=496000; 496000>>6 = 7750. The net scale is x*Cs/8
    // for this representation: operand<<3 then >>6 == <<3 net only when... no -> it is /8.
    // (x<<3)*Cs>>6 = x*Cs*8/64 = x*Cs/8. So 1000*62/8 = 62000/8 = 7750. Confirmed.
    check("prod 1000 * 62 (=/8)",   aruProd(1000,  62), 7750);   // 1000*62/8
    check("prod 1024 * 32",         aruProd(1024,  32), 4096);   // 1024*32/8
    check("prod 100 * 63",          aruProd( 100,  63),  787);   // 6300/8 = 787.5 -> 787 floor
    check("prod 100 * -63",         aruProd( 100, -63), -788);   // -6300/8 = -787.5 -> -788 floor

    // Floor division (toward -inf) on negatives: (-5<<3)*1>>6 = -40>>6 = -1 (floor),
    // not 0 (truncation toward zero).
    check("floor neg small",        aruProd(  -5,   1),   -1);   // -40>>6 = floor(-0.625) = -1
    check("floor neg one",          aruProd(  -1,   1),   -1);   //  -8>>6 = floor(-0.125) = -1
    check("pos under one floors 0", aruProd(   1,   1),    0);   //   8>>6 = 0

    // ---- MAC: sat20(acc + prod) ----
    check("mac accumulate",         aruMac(100, 1024, 32), 4196); // 100 + 4096
    check("mac neg coeff",          aruMac(  0, 1000,-62),-7750); // -(1000*62/8)

    // ---- 20-bit accumulator saturation (the Manual's "last coefficients set sat") ----
    // prod 1000*63/8 = 7875; 524000 + 7875 = 531875 -> rail +524287.
    check("sat20 high rail",        aruMac( 524000, 1000,  63),  524287);
    check("sat20 low rail",         aruMac(-524000, 1000, -63), -524287);
    check("sat20 passthrough hi",   aruSat20( 524287),  524287);
    check("sat20 passthrough lo",   aruSat20(-524287), -524287);
    check("sat20 clamp over",       aruSat20( 600000),  524287);
    check("sat20 clamp under",      aruSat20(-600000), -524287);

    // ---- 16-bit result-register saturation: RES = sat16(ACC>>3) ----
    // ACC at full positive rail: 524287>>3 = 65535 -> sat16 -> 32767.
    check("res from acc hi rail",   aruSat16(524287 >> 3),  32767);  // 65535 clamps
    check("res from acc lo rail",   aruSat16(-524287 >> 3), -32768); // -65536>>... clamps
    check("sat16 passthrough hi",   aruSat16( 32767),  32767);
    check("sat16 passthrough lo",   aruSat16(-32768), -32768);
    check("sat16 clamp over",       aruSat16( 40000),  32767);
    check("sat16 clamp under",      aruSat16(-40000), -32768);
    // A mid-range result that does NOT saturate: ACC=80000 -> 80000>>3 = 10000.
    check("res mid no sat",         aruSat16(80000 >> 3),  10000);

    std::printf(g_fail ? "\n%d FAILURE(S)\n" : "\nALL PASS\n", g_fail);
    return g_fail ? 1 : 0;
}
