// 224XL diff harness: proves the C++ core (libs/sgdsp/include/sgdsp/reverb/224xl.hpp,
// the port of the pin-locked RTL engine tools/aru_freerun22_rtl.py) reproduces the
// Python reference BIT-EXACTLY on the RTL22-exported goldens
// (tools/export_golden_224xl_rtl.py -> golden_rtl/).
//
//   Layer 1 (program extraction parity): loadProgram succeeds and
//                                        frameSteps()-1 == meta L.
//   Layer 2 (walk parity): per-frame 4-channel CPU-domain outputs equal over ALL
//                          nsamp frames, AND the per-step phys trace
//                          {step, ACC, RES, DAB, R0..R3} equal for the first
//                          trace_frames frames.
//
// The stimulus is READ from <case>_in.bin (int16 LE, h1/h2 pairs) - never
// regenerated - so C++ and Python consume identical bits.
//
// Usage: diff_harness <golden_dir> [case ...]     (default: d1zero d1max concert)
#include "sgdsp/reverb/224xl.hpp"
#include "golden_io.hpp"
#include <cstdio>
#include <string>
#include <vector>

using namespace sgdsp::reverb;

static AruWord g_dmem[Lexicon224XLCore::kDmemWords];
static Lexicon224XLCore g_core;

static bool runCase(const std::string& dir, const std::string& name)
{
    const std::string base = dir + "/" + name + "_";
    const long nsamp       = golden::readMetaInt(base + "meta.json", "nsamp", -1);
    const long traceFrames = golden::readMetaInt(base + "meta.json", "trace_frames", 0);
    const long metaL       = golden::readMetaInt(base + "meta.json", "L", -1);
    if (nsamp < 0 || metaL < 0) {
        std::printf("[%s] ERROR: cannot read %smeta.json\n", name.c_str(), base.c_str());
        return false;
    }

    const std::vector<uint8_t> wcs   = golden::readBytes(base + "wcs.bin");
    const std::vector<int16_t> inS   = golden::readI16(base + "in.bin");
    const std::vector<int16_t> outsG = golden::readI16(base + "outs.bin");
    const std::vector<int64_t> trG   = golden::readI64(base + "trace.bin");
    if (wcs.size() != 512) { std::printf("[%s] ERROR: wcs.bin not 512 bytes\n", name.c_str()); return false; }
    if ((long)inS.size() != nsamp * 2) {
        std::printf("[%s] ERROR: in.bin has %zu i16 (want %ld)\n", name.c_str(), inS.size(), nsamp * 2);
        return false;
    }
    if ((long)outsG.size() != nsamp * 4) {
        std::printf("[%s] ERROR: outs.bin has %zu i16 (want %ld)\n", name.c_str(), outsG.size(), nsamp * 4);
        return false;
    }

    g_core.prepare(0, g_dmem);
    if (!g_core.loadProgram(wcs.data())) {
        std::printf("[%s] L1 FAIL: loadProgram found no reset word\n", name.c_str());
        return false;
    }

    // ---- Layer 1: program extraction parity ----
    const int nSteps = g_core.frameSteps();
    if (nSteps - 1 != (int)metaL) {
        std::printf("[%s] L1 FAIL: frameSteps()-1 = %d, meta L = %ld\n",
                    name.c_str(), nSteps - 1, metaL);
        return false;
    }
    if ((long)trG.size() != traceFrames * nSteps * 8) {
        std::printf("[%s] ERROR: trace.bin has %zu i64 (want %ld)\n",
                    name.c_str(), trG.size(), traceFrames * nSteps * 8);
        return false;
    }

    // ---- Layer 2: full-run output parity + per-step trace parity ----
    std::vector<StepProbe> probes((size_t)nSteps);
    long outFail = 0, traceFail = 0;
    int32_t out[4];
    for (long n = 0; n < nsamp; ++n) {
        const int32_t h1 = inS[(size_t)n * 2 + 0];
        const int32_t h2 = inS[(size_t)n * 2 + 1];
        if (n < traceFrames) {
            g_core.processFrameTraced(h1, h2, out, probes.data());
            for (int r = 0; r < nSteps; ++r) {
                const int64_t* g = &trG[((size_t)n * nSteps + r) * 8];
                const StepProbe& p = probes[(size_t)r];
                const bool ok = (int64_t)p.step == g[0] && (int64_t)p.acc == g[1] &&
                                (int64_t)p.res == g[2] && (int64_t)p.dab == g[3] &&
                                (int64_t)p.r[0] == g[4] && (int64_t)p.r[1] == g[5] &&
                                (int64_t)p.r[2] == g[6] && (int64_t)p.r[3] == g[7];
                if (!ok) {
                    if (traceFail < 5)
                        std::printf("[%s] L2 TRACE FAIL f%ld s%d: "
                                    "core{ACC=%05X RES=%04X DAB=%04X R=%04X %04X %04X %04X} "
                                    "gold{ACC=%05llX RES=%04llX DAB=%04llX R=%04llX %04llX %04llX %04llX}\n",
                                    name.c_str(), n, r,
                                    p.acc, p.res, p.dab, p.r[0], p.r[1], p.r[2], p.r[3],
                                    (unsigned long long)g[1], (unsigned long long)g[2],
                                    (unsigned long long)g[3], (unsigned long long)g[4],
                                    (unsigned long long)g[5], (unsigned long long)g[6],
                                    (unsigned long long)g[7]);
                    ++traceFail;
                }
            }
        } else {
            g_core.processFrame(h1, h2, out);
        }
        for (int c = 0; c < 4; ++c) {
            const int32_t want = outsG[(size_t)n * 4 + c];
            if (out[c] != want) {
                if (outFail < 5)
                    std::printf("[%s] L2 OUT FAIL f%ld ch%c: core=%d gold=%d\n",
                                name.c_str(), n, 'A' + c, out[c], want);
                ++outFail;
            }
        }
    }

    const bool pass = (outFail == 0 && traceFail == 0);
    std::printf("[%s] %s  (L=%ld, %ld frames x 4 ch, %ld traced frames x %d steps%s)\n",
                name.c_str(), pass ? "PASS" : "FAIL", metaL, nsamp, traceFrames, nSteps,
                pass ? "" : " - see mismatches above");
    if (!pass)
        std::printf("[%s]   mismatches: outputs %ld, trace records %ld\n",
                    name.c_str(), outFail, traceFail);
    return pass;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        std::printf("usage: diff_harness <golden_dir> [case ...]\n");
        return 2;
    }
    const std::string dir = argv[1];
    std::vector<std::string> cases;
    for (int i = 2; i < argc; ++i) cases.push_back(argv[i]);
    if (cases.empty()) cases = {"d1zero", "d1max", "concert"};

    int nPass = 0;
    for (const std::string& c : cases) nPass += runCase(dir, c) ? 1 : 0;

    const bool all = nPass == (int)cases.size();
    std::printf("\n%s (%d/%zu cases bit-exact vs tools/aru_freerun22_rtl.py)\n",
                all ? "DIFF PASSED" : "DIFF FAILED", nPass, cases.size());
    return all ? 0 : 1;
}
