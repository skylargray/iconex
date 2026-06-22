// 224XL diff harness: proves the C++ core reproduces the Python aru_datapath
// reference integer-exact for one program.
//   Layer 1 (microcode parity): core decode of <id>_wcs.bin == <id>_fields.json.
//   Layer 2 (arithmetic parity): per-step probes + per-sample energy == golden.
// Usage: diff_harness <golden_dir> <id_hex2>   e.g.  diff_harness ./golden 01
#include "sgdsp/reverb/224xl.hpp"
#include "golden_io.hpp"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

using namespace sgdsp::reverb;

int main(int argc, char** argv)
{
    if (argc < 3) { std::printf("usage: diff_harness <golden_dir> <id_hex2>\n"); return 2; }
    const std::string dir = argv[1];
    const std::string id  = argv[2];
    const std::string base = dir + "/" + id + "_";

    const int nsamp       = golden::readMetaInt(base + "meta.json", "nsamp", 0);
    const int traceWindow = golden::readMetaInt(base + "meta.json", "trace_window", 0);
    const int impVal      = golden::readMetaInt(base + "meta.json", "imp", 0);
    const int nActiveMeta = golden::readMetaInt(base + "meta.json", "n_active", 0);
    if (nsamp == 0) { std::printf("ERROR: cannot read %smeta.json\n", base.c_str()); return 2; }

    std::vector<uint8_t> wcs = golden::readBytes(base + "wcs.bin");
    if (wcs.size() != 512) { std::printf("ERROR: %swcs.bin not 512 bytes\n", base.c_str()); return 2; }
    std::vector<golden::Field> fields = golden::readFields(base + "fields.json");
    std::vector<int64_t> esumGold = golden::readI64(base + "esum.bin");
    std::vector<int64_t> stepsGold = golden::readI64(base + "steps.bin");

    static AruWord dmem[65536];
    static Lexicon224XLCore<65536, 2> core;
    core.prepare(34130, dmem);
    core.loadProgram(wcs.data());

    // ---------- Layer 1: microcode decode parity ----------
    int l1fail = 0;
    if (core.activeStepCount() != (int)fields.size()) {
        std::printf("L1 FAIL: active step count core=%d gold=%zu\n",
                    core.activeStepCount(), fields.size());
        ++l1fail;
    }
    int nCmp = core.activeStepCount() < (int)fields.size()
               ? core.activeStepCount() : (int)fields.size();
    for (int i = 0; i < nCmp; ++i) {
        const AruStep& c = core.step(i);
        const golden::Field& g = fields[i];
        if (c.s != g.s || (int)c.offset != g.offset || c.coeff != g.coeff ||
            c.zero != g.ZERO || c.b3 != g.b3 || c.xfer != g.XFER ||
            c.wa != g.WA || c.ra != g.RA) {
            std::printf("L1 FAIL @active %d (step %d): "
                        "core{off=%u coeff=%d Z=%d b3=%d XF=%d WA=%d RA=%d} "
                        "gold{off=%d coeff=%d Z=%d b3=%d XF=%d WA=%d RA=%d}\n",
                        i, c.s, c.offset, c.coeff, c.zero, c.b3, c.xfer, c.wa, c.ra,
                        g.offset, g.coeff, g.ZERO, g.b3, g.XFER, g.WA, g.RA);
            if (++l1fail >= 10) { std::printf("...stopping after 10\n"); break; }
        }
    }
    if (!l1fail) std::printf("L1 OK: %d active steps decode-match\n", core.activeStepCount());

    // ---------- Layer 2: arithmetic parity ----------
    const int nActive = core.activeStepCount();
    (void)nActiveMeta;
    std::vector<Probe> probes(nActive > 0 ? nActive : 1);
    int l2fail = 0;
    size_t gIdx = 0;                       // index into flattened stepsGold (8 ints/record)
    for (int n = 0; n < nsamp; ++n) {
        const AruWord in = (n == 0) ? (AruWord)impVal : 0;
        AruWord outL, outR; (void)outL; (void)outR;
        int np = 0; int64_t esum = 0;
        core.processFixedTraced(in, probes.data(), &np, &esum);

        if (esum != esumGold[n]) {
            std::printf("L2 FAIL esum @sample %d: core=%lld gold=%lld\n",
                        n, (long long)esum, (long long)esumGold[n]);
            if (++l2fail >= 10) break;
        }
        if (n < traceWindow) {
            for (int k = 0; k < np; ++k) {
                if (gIdx + 8 > stepsGold.size()) {
                    std::printf("L2 FAIL: golden steps exhausted at sample %d "
                                "(core emitted more probes than golden recorded)\n", n);
                    ++l2fail; break;
                }
                const Probe& p = probes[k];
                const int64_t* g = &stepsGold[gIdx];
                gIdx += 8;
                if (p.n!=g[0]||p.s!=g[1]||p.addr!=g[2]||p.dab!=g[3]||
                    p.racc_in!=g[4]||p.prod!=g[5]||p.acc!=g[6]||p.res!=g[7]) {
                    std::printf("L2 FAIL probe @sample %d step %lld: "
                        "core{addr=%lld dab=%lld racc=%lld prod=%lld acc=%lld res=%lld} "
                        "gold{addr=%lld dab=%lld racc=%lld prod=%lld acc=%lld res=%lld}\n",
                        n, (long long)p.s,
                        (long long)p.addr,(long long)p.dab,(long long)p.racc_in,
                        (long long)p.prod,(long long)p.acc,(long long)p.res,
                        (long long)g[2],(long long)g[3],(long long)g[4],
                        (long long)g[5],(long long)g[6],(long long)g[7]);
                    if (++l2fail >= 10) { std::printf("...stopping after 10\n"); break; }
                }
            }
            if (l2fail >= 10) break;
        }
    }
    if (!l2fail) std::printf("L2 OK: %d samples energy + %d-sample probe trace match\n",
                             nsamp, traceWindow);

    const int rc = (l1fail || l2fail) ? 1 : 0;
    std::printf(rc ? "\nDIFF FAILED\n" : "\nDIFF PASSED (integer-exact vs reference)\n");
    return rc;
}
