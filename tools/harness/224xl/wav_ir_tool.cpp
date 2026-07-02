// 224XL listening / IR tool on the RTL-parity core (minimally ported to the
// processFrame surface, plan 024 F1d). For ears + spectrogram/EDC, not for
// bit-exact checks (that is diff_harness).
//
//   impulse mode: wav_ir_tool ir  <wcs.bin> <out.wav> [nsamp] [amp]
//   process mode: wav_ir_tool wav <wcs.bin> <in.wav> <out.wav>
//
// <wcs.bin> = a 512-byte stored WCS image (e.g. golden_rtl/concert_wcs.bin).
// Input is MONO-DUPLICATED onto both FPC halves (h1 = h2). Output WAV is
// stereo L = channel A, R = channel C (the D1-pinned CONCERT pair); the WAV
// rate is the program frame rate rounded to integer Hz.
#include "sgdsp/reverb/224xl.hpp"
#include "golden_io.hpp"
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <string>
#include <vector>

using namespace sgdsp::reverb;

#pragma pack(push, 1)
struct WavHeader {
    char riff[4] = {'R','I','F','F'}; uint32_t chunkSize = 0;
    char wave[4] = {'W','A','V','E'};
    char fmt[4]  = {'f','m','t',' '}; uint32_t fmtSize = 16;
    uint16_t audioFormat = 1; uint16_t numChannels = 2;
    uint32_t sampleRate = 32508; uint32_t byteRate = 32508*2*2;
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

// Read a mono/stereo 16-bit PCM WAV's channel 0 as int16 (skips to 'data').
static std::vector<int16_t> readWavCh0(const std::string& path, uint32_t& srOut)
{
    std::vector<int16_t> out;
    FILE* f = std::fopen(path.c_str(), "rb");
    if (!f) { std::printf("ERROR: cannot open %s\n", path.c_str()); return out; }
    WavHeader h;
    if (std::fread(&h, sizeof(h), 1, f) != 1) { std::fclose(f); return out; }
    srOut = h.sampleRate;
    uint32_t dataSize = h.dataSize;
    const uint32_t kMaxData = 256u * 1024 * 1024;   // sanity cap for a dev tool
    if (dataSize > kMaxData) dataSize = kMaxData;
    std::vector<int16_t> pcm(dataSize / sizeof(int16_t));
    if (!pcm.empty()) {
        const size_t got = std::fread(pcm.data(), sizeof(int16_t), pcm.size(), f);
        pcm.resize(got);
    }
    std::fclose(f);
    const int ch = h.numChannels ? h.numChannels : 1;
    out.reserve(pcm.size() / ch);
    for (size_t i = 0; i + ch <= pcm.size(); i += ch) out.push_back(pcm[i]);
    return out;
}

static AruWord g_dmem[Lexicon224XLCore::kDmemWords];
static Lexicon224XLCore g_core;

int main(int argc, char** argv)
{
    if (argc < 4) {
        std::printf("usage:\n  wav_ir_tool ir  <wcs.bin> <out.wav> [nsamp] [amp]\n"
                    "  wav_ir_tool wav <wcs.bin> <in.wav> <out.wav>\n");
        return 2;
    }
    const std::string mode = argv[1];

    const std::vector<uint8_t> wcs = golden::readBytes(argv[2]);
    if (wcs.size() != 512) { std::printf("ERROR: %s is not a 512-byte WCS image\n", argv[2]); return 2; }
    g_core.prepare(0, g_dmem);
    if (!g_core.loadProgram(wcs.data())) { std::printf("ERROR: no reset word in WCS\n"); return 2; }
    const uint32_t sr = (uint32_t)(g_core.sampleRateHz() + 0.5);
    std::printf("program: %d steps/frame, fs = %.1f Hz\n", g_core.frameSteps(), g_core.sampleRateHz());

    std::vector<int16_t> outBuf;
    int32_t out[4];
    auto runFrame = [&](int32_t x) {
        g_core.processFrame(x, x, out);                    // mono duplication (h1 = h2)
        outBuf.push_back((int16_t)out[0]);                 // L = channel A
        outBuf.push_back((int16_t)out[2]);                 // R = channel C
    };

    if (mode == "ir") {
        const std::string outPath = argv[3];
        const long nsamp = (argc > 4) ? std::atol(argv[4]) : (long)(2.0 * sr);
        const int amp = (argc > 5) ? std::atoi(argv[5]) : 16000;
        if (nsamp <= 0) { std::printf("ERROR: nsamp must be > 0\n"); return 2; }
        for (long n = 0; n < nsamp; ++n) runFrame(n == 0 ? amp : 0);
        if (!writeStereoWav(outPath, outBuf, sr)) return 1;
        std::printf("wrote IR %s (%ld frames, L=A R=C)\n", outPath.c_str(), nsamp);
    } else if (mode == "wav") {
        if (argc < 5) { std::printf("usage: wav_ir_tool wav <wcs.bin> <in.wav> <out.wav>\n"); return 2; }
        uint32_t srIn = 0;
        std::vector<int16_t> in = readWavCh0(argv[3], srIn);
        if (in.empty()) { std::printf("ERROR: no samples in %s\n", argv[3]); return 2; }
        if (srIn && srIn != sr)
            std::printf("NOTE: input rate %u != program rate %u (no resampling)\n", srIn, sr);
        for (int16_t x : in) runFrame(x);
        for (long n = 0; n < (long)(2.0 * sr); ++n) runFrame(0);   // 2 s tail
        if (!writeStereoWav(argv[4], outBuf, sr)) return 1;
        std::printf("wrote %s (%zu frames + tail, L=A R=C)\n", argv[4], in.size());
    } else {
        std::printf("unknown mode '%s'\n", mode.c_str());
        return 2;
    }
    return 0;
}
