#pragma once
// Minimal readers for the golden artifacts written by tools/export_golden_224xl_rtl.py
// (the RTL22-parity flow, plan 024 F1d). Binary files are little-endian; meta.json is
// scanned with a tiny flat-key reader sufficient for the generator-produced shape.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

namespace golden {

inline std::vector<uint8_t> readBytes(const std::string& path)
{
    std::vector<uint8_t> v;
    FILE* f = std::fopen(path.c_str(), "rb");
    if (!f) return v;
    std::fseek(f, 0, SEEK_END); long n = std::ftell(f); std::fseek(f, 0, SEEK_SET);
    v.resize(n > 0 ? (size_t)n : 0);
    if (n > 0) { size_t got = std::fread(v.data(), 1, (size_t)n, f); v.resize(got); }
    std::fclose(f);
    return v;
}

// --- little-endian field readers (all golden binaries are packed LE) ---
inline uint16_t leU16(const uint8_t* p) { return (uint16_t)(p[0] | (p[1] << 8)); }
inline uint32_t leU32(const uint8_t* p)
{
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}
inline int64_t leI64(const uint8_t* p)
{
    uint64_t v = 0;
    for (int k = 0; k < 8; ++k) v |= (uint64_t)p[k] << (8 * k);
    return (int64_t)v;
}

inline std::vector<int16_t> readI16(const std::string& path)
{
    std::vector<uint8_t> b = readBytes(path);
    std::vector<int16_t> out(b.size() / 2);
    for (size_t i = 0; i < out.size(); ++i) out[i] = (int16_t)leU16(&b[i * 2]);
    return out;
}

inline std::vector<int64_t> readI64(const std::string& path)
{
    std::vector<uint8_t> b = readBytes(path);
    std::vector<int64_t> out(b.size() / 8);
    for (size_t i = 0; i < out.size(); ++i) out[i] = leI64(&b[i * 8]);
    return out;
}

// Pull a single integer value for `key` out of a flat meta.json ("key":value).
// strtol skips any whitespace after the colon.
inline long readMetaInt(const std::string& path, const char* key, long dflt)
{
    std::vector<uint8_t> bytes = readBytes(path);
    std::string j(bytes.begin(), bytes.end());
    std::string pat = std::string("\"") + key + "\":";
    size_t p = j.find(pat);
    if (p == std::string::npos) return dflt;
    return std::strtol(j.c_str() + p + pat.size(), nullptr, 10);
}

} // namespace golden
