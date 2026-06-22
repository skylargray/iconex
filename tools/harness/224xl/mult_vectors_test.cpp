// Multiplier + saturation unit tests for the 224XL ARU primitives.
// Anchors: the Service-Manual multiplier diagnostic exercises coefficients
// +21/32, +42/32, +63/64 and x1, x1/2, x-1, x1/4, x5/4, and states "the last two
// coefficients should set the saturation" (Lexicon 224X Service Manual 5.3,
// E80-EB3). The 7-bit/128 first-cut datapath cannot represent x1, 42/32, 5/4
// exactly (that is the OPEN coeff-denominator/2-LSB item) - those exact
// coefficients become assertions once that knob resolves. This test pins the
// representable mechanics: sign-magnitude scaling, floor-shift, and saturation.
#include "sgdsp/reverb/224xl.hpp"
#include <cstdio>
#include <cstdint>

using sgdsp::reverb::aruMac;
using sgdsp::reverb::aruSat16;
using sgdsp::reverb::AruAccum;

static int g_fail = 0;

static void check(const char* name, AruAccum got, AruAccum want)
{
    if (got != want) {
        std::printf("FAIL %-28s got=%lld want=%lld\n", name,
                    (long long)got, (long long)want);
        ++g_fail;
    } else {
        std::printf("ok   %-28s = %lld\n", name, (long long)got);
    }
}

int main()
{
    // Representable coefficients (signed 7-bit magnitude, applied as coeff>>7):
    //   +1/2  -> coeff 64   (64/128)
    //   +1/4  -> coeff 32
    //   +21/32-> coeff 84   (84/128 == 21/32)
    //   +63/64-> coeff 126  (126/128 == 63/64)
    // MAC from acc=0: (x*coeff)>>7.
    check("half of 1000",        aruMac(0, 1000,  64),  500);   // 1000*64>>7 = 500
    check("quarter of 1000",     aruMac(0, 1000,  32),  250);   // 1000*32>>7 = 250
    check("21/32 of 3200",       aruMac(0, 3200,  84), 2100);   // 3200*84>>7 = 2100
    check("63/64 of 6400",       aruMac(0, 6400, 126), 6300);   // 6400*126>>7 = 6300

    // Floor division on negatives: a non-exact case proves floor (toward -inf),
    // not truncation toward zero:  (-5 * 1) >> 7 == -1 (floor); -5/128 == 0 (trunc).
    check("floor neg small",     aruMac(0,   -5,   1),   -1);

    // Standalone product cannot saturate at 16-bit scale (max coeff 127):
    check("126/128 of 32767",    aruMac(0, 32767, 126), 32255); // 32767*126>>7 = 32255

    // Saturation trips come from ACCUMULATION (the Manual's "last two coefficients
    // set saturation"): start near the rail, add more.
    check("sat from big acc",    aruMac(32000, 1000, 126), 32767);
    check("sat negative rail",   aruMac(-32000, 1000, -126), -32768);

    // accumulate then saturate (sat applied to acc+prod each step)
    check("accumulate then add", aruMac(100, 1000, 64), 600);   // 100 + 500

    std::printf(g_fail ? "\n%d FAILURE(S)\n" : "\nALL PASS\n", g_fail);
    return g_fail ? 1 : 0;
}
