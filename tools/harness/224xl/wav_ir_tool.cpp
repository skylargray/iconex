// 224XL listening / IR tool: drives the core's FLOAT boundary and writes a WAV.
//   impulse mode: wav_ir_tool ir  <out.wav> [nsamp]   -> dumps the impulse response
//   process mode: wav_ir_tool wav <in.wav> <out.wav>  -> filters a mono 16-bit WAV
// Stereo out (L/R duplicated in the first cut). For ears + spectrogram/EDC, not for
// bit-exact checks (that is diff_harness). Loads CONCERT from the generated header.
//
// NOTE (first cut): the CONCERT tank SUSTAINS rather than decays under the current
// reference arithmetic (ArithProfile) - the result-register shift / coeff denominator
// that set loop gain/decay are OPEN items (see design spec section 8). This tool is
// integer-exact-faithful to tools/aru_datapath.py; a cleanly decaying IR follows once
// that arithmetic is tuned. The IR here is non-silent and bounded, for routing/level checks.
#include "sgdsp/reverb/224xl.hpp"
#include "sgdsp/reverb/224xl_programs.hpp"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

using namespace sgdsp::reverb;

#pragma pack(push, 1)
struct WavHeader {
    char riff[4] = {'R','I','F','F'}; uint32_t chunkSize = 0;
    char wave[4] = {'W','A','V','E'};
    char fmt[4]  = {'f','m','t',' '}; uint32_t fmtSize = 16;
    uint16_t audioFormat = 1; uint16_t numChannels = 2;
    uint32_t sampleRate = 34130; uint32_t byteRate = 34130*2*2;
    uint16_t blockAlign = 4; uint16_t bitsPerSample = 16;
    char data[4] = {'d','a','t','a'}; uint32_t dataSize = 0;
};
#pragma pack(pop)

static bool writeStereoWav(const std::string& path, const std::vector<int16_t>& interleaved,
                           uint32_t sr)
{
    WavHeader h;
    h.sampleRate = sr; h.byteRate = sr*2*2;
    h.dataSize = (uint32_t)(interleaved.size() * sizeof(int16_t));
    h.chunkSize = 36 + h.dataSize;
    FILE* f = std::fopen(path.c_str(), "wb");
    if (!f) { std::printf("ERROR: cannot open %s\n", path.c_str()); return false; }
    const bool okH = std::fwrite(&h, sizeof(h), 1, f) == 1;
    const bool okD = std::fwrite(interleaved.data(), sizeof(int16_t),
                                 interleaved.size(), f) == interleaved.size();
    std::fclose(f);
    if (!okH || !okD) { std::printf("ERROR: short write to %s\n", path.c_str()); return false; }
    return true;
}

// Read a mono 16-bit PCM WAV's samples (skips to 'data'); returns float [-1,1].
static std::vector<float> readMonoWav(const std::string& path, uint32_t& srOut)
{
    std::vector<float> out;
    FILE* f = std::fopen(path.c_str(), "rb");
    if (!f) { std::printf("ERROR: cannot open %s\n", path.c_str()); return out; }
    WavHeader h;
    if (std::fread(&h, sizeof(h), 1, f) != 1) { std::fclose(f); return out; }
    srOut = h.sampleRate;
    // dataSize comes from an untrusted file; cap it to avoid a huge allocation on a
    // malformed header, and resize to what was actually read on a short/truncated file.
    uint32_t dataSize = h.dataSize;
    const uint32_t kMaxData = 256u * 1024 * 1024;   // 256 MB sanity cap for a dev tool
    if (dataSize > kMaxData) {
        std::printf("WARNING: dataSize %u exceeds cap; clamping to %u\n", dataSize, kMaxData);
        dataSize = kMaxData;
    }
    std::vector<int16_t> pcm(dataSize / sizeof(int16_t));
    if (!pcm.empty()) {
        const size_t got = std::fread(pcm.data(), sizeof(int16_t), pcm.size(), f);
        pcm.resize(got);   // truncated file -> process only what was actually read
    }
    std::fclose(f);
    const int ch = h.numChannels ? h.numChannels : 1;
    out.reserve(pcm.size() / ch);
    for (size_t i = 0; i + ch <= pcm.size(); i += ch)
        out.push_back(pcm[i] / 32768.0f);   // take channel 0
    return out;
}

int main(int argc, char** argv)
{
    if (argc < 3) {
        std::printf("usage:\n  wav_ir_tool ir  <out.wav> [nsamp]\n"
                    "  wav_ir_tool wav <in.wav> <out.wav>\n");
        return 2;
    }
    const std::string mode = argv[1];

    static AruWord dmem[65536];
    static Lexicon224XLCore<65536, 2> core;
    core.prepare(34130, dmem);
    core.loadProgram(programs::kCONCERT_HALL_WCS);

    std::vector<int16_t> outBuf;
    uint32_t sr = 34130;

    auto pushOut = [&](float l, float r) {
        auto clamp16 = [](float x){ x*=32768.0f; if(x>32767)x=32767; if(x<-32768)x=-32768;
                                    return (int16_t)(x>=0?x+0.5f:x-0.5f); };
        outBuf.push_back(clamp16(l)); outBuf.push_back(clamp16(r));
    };

    if (mode == "ir") {
        const std::string outPath = argv[2];
        const int nsamp = (argc > 3) ? std::atoi(argv[3]) : 34130; // ~1 s
        if (nsamp <= 0) { std::printf("ERROR: nsamp must be > 0\n"); return 2; }
        for (int n = 0; n < nsamp; ++n) {
            Sample inS = (n == 0) ? 0.61f : 0.0f;   // ~20000/32768 impulse
            Sample l, r; core.process(inS, l, r);
            pushOut(l, r);
        }
        if (!writeStereoWav(outPath, outBuf, sr)) return 1;
        std::printf("wrote IR %s (%d samples)\n", outPath.c_str(), nsamp);
    } else if (mode == "wav") {
        if (argc < 4) { std::printf("usage: wav_ir_tool wav <in.wav> <out.wav>\n"); return 2; }
        std::vector<float> in = readMonoWav(argv[2], sr);
        core.prepare(sr ? sr : 34130, dmem);
        core.loadProgram(programs::kCONCERT_HALL_WCS);
        for (float x : in) { Sample l, r; core.process(x, l, r); pushOut(l, r); }
        if (!writeStereoWav(argv[3], outBuf, sr ? sr : 34130)) return 1;
        std::printf("wrote %s (%zu frames)\n", argv[3], in.size());
    } else {
        std::printf("unknown mode '%s'\n", mode.c_str());
        return 2;
    }
    return 0;
}
