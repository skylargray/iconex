// 224XL primitive-vector test: checks the C++ gate-array port (224xl_booth.hpp
// combArray/loadSR/shiftRight2 via raw3) and the back-end adder + sat-mux
// (224xl.hpp backend20) against vectors exported from the Python reference
// (tools/export_golden_224xl_rtl.py, running tools/aru_freerun22_rtl.py raw3 /
// backend20 on the gate model tools/aru_booth.py).
//
// booth_vectors.bin layout (packed little-endian):
//   header <4sII>  magic "B224", n_raw, n_be
//   n_raw x <HB3I> {opnd_phys u16, cmag u8, rawA u32, rawB u32, rawC u32}
//   n_be  x <IIBI> {acc u32, raw u32, cs u8, out u32}
//
// Replaces the obsolete mult_vectors_test.cpp (pre-0022 value-domain
// primitives) in the build.
//
// Usage: booth_vectors_test <path-to-booth_vectors.bin>
#include "sgdsp/reverb/224xl.hpp"
#include "golden_io.hpp"
#include <cstdio>

using namespace sgdsp::reverb;

int main(int argc, char** argv)
{
    const std::string path = (argc > 1) ? argv[1] : "golden_rtl/booth_vectors.bin";
    std::vector<uint8_t> b = golden::readBytes(path);
    if (b.size() < 12 || b[0] != 'B' || b[1] != '2' || b[2] != '2' || b[3] != '4') {
        std::printf("ERROR: cannot read booth vectors at %s\n", path.c_str());
        return 2;
    }
    const uint32_t nRaw = golden::leU32(&b[4]);
    const uint32_t nBe  = golden::leU32(&b[8]);
    const size_t kRawRec = 2 + 1 + 3 * 4;   // <HB3I>
    const size_t kBeRec  = 4 + 4 + 1 + 4;   // <IIBI>
    if (b.size() != 12 + nRaw * kRawRec + nBe * kBeRec) {
        std::printf("ERROR: booth_vectors.bin size %zu inconsistent with header (%u,%u)\n",
                    b.size(), nRaw, nBe);
        return 2;
    }

    int fail = 0;

    // sanity: the zero-rail comb baseline (cmag 0 -> PR = 0xFFFFF, operand-independent)
    {
        uint32_t a, bb, c;
        aru224::raw3(0xFFFF, 0, a, bb, c);
        if (a != aru224::kRawIdle || bb != aru224::kRawIdle || c != aru224::kRawIdle) {
            std::printf("FAIL zero-rail baseline: raw3(0xFFFF,0) = %05X %05X %05X (want 0xFFFFF x3)\n",
                        a, bb, c);
            ++fail;
        }
    }

    // raw3 vectors (gate array: NAND taps + carry chain + shifter)
    size_t off = 12;
    uint32_t rawFail = 0;
    for (uint32_t i = 0; i < nRaw; ++i, off += kRawRec) {
        const uint16_t opnd = golden::leU16(&b[off]);
        const uint8_t  cmag = b[off + 2];
        const uint32_t eA = golden::leU32(&b[off + 3]);
        const uint32_t eB = golden::leU32(&b[off + 7]);
        const uint32_t eC = golden::leU32(&b[off + 11]);
        uint32_t gA, gB, gC;
        aru224::raw3(opnd, cmag, gA, gB, gC);
        if (gA != eA || gB != eB || gC != eC) {
            if (rawFail < 10)
                std::printf("FAIL raw3 #%u opnd=%04X cmag=%02u: got %05X %05X %05X want %05X %05X %05X\n",
                            i, opnd, cmag, gA, gB, gC, eA, eB, eC);
            ++rawFail;
        }
    }
    if (rawFail) { std::printf("raw3: %u/%u MISMATCH\n", rawFail, nRaw); ++fail; }
    else         std::printf("raw3: %u/%u bit-exact\n", nRaw, nRaw);

    // backend20 vectors (sub-XOR + 20-bit sum + sat-mux, clamp into both paths)
    uint32_t beFail = 0, nSat = 0;
    for (uint32_t i = 0; i < nBe; ++i, off += kBeRec) {
        const uint32_t acc = golden::leU32(&b[off]);
        const uint32_t raw = golden::leU32(&b[off + 4]);
        const uint8_t  cs  = b[off + 8];
        const uint32_t exp = golden::leU32(&b[off + 9]);
        const uint32_t got = aru224::backend20(acc, raw, cs);
        if (exp == 0x3FFFFu || exp == 0xC0000u) ++nSat;
        if (got != exp) {
            if (beFail < 10)
                std::printf("FAIL backend20 #%u acc=%05X raw=%05X cs=%u: got %05X want %05X\n",
                            i, acc, raw, cs, got, exp);
            ++beFail;
        }
    }
    if (beFail) { std::printf("backend20: %u/%u MISMATCH\n", beFail, nBe); ++fail; }
    else        std::printf("backend20: %u/%u bit-exact (%u clamp-rail records)\n", nBe, nBe, nSat);

    std::printf(fail ? "\nBOOTH VECTORS FAILED\n" : "\nBOOTH VECTORS PASSED\n");
    return fail ? 1 : 0;
}
