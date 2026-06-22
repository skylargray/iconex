#pragma once
// Minimal readers for the golden artifacts written by tools/export_golden_224.py.
// Binary files are little-endian int64 arrays; JSON is parsed with a tiny scanner
// sufficient for the flat, generator-produced shapes (no general JSON needed).
#include <cstdint>
#include <cstdio>
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

inline std::vector<int64_t> readI64(const std::string& path)
{
    std::vector<uint8_t> b = readBytes(path);
    std::vector<int64_t> out(b.size() / 8);
    for (size_t i = 0; i < out.size(); ++i) {
        int64_t v = 0;
        for (int k = 0; k < 8; ++k) v |= (int64_t)b[i*8+k] << (8*k);
        out[i] = v;
    }
    return out;
}

// One decoded field record from <id>_fields.json (flat objects, integer values).
struct Field { int s, offset, coeff, ZERO, b3, XFER, WA, RA; };

// Scan flat JSON like [{"s":0,"offset":123,"coeff":-7,"ZERO":0,"b3":0,"XFER":1,"WA":0,"RA":1}, ...].
inline std::vector<Field> readFields(const std::string& path)
{
    std::vector<uint8_t> bytes = readBytes(path);
    std::string j(bytes.begin(), bytes.end());
    std::vector<Field> out;
    size_t i = 0;
    auto readKeyVal = [&](const char* key, int& dst) {
        // assumes keys appear in object order; find next "key": then parse int
        std::string pat = std::string("\"") + key + "\":";
        size_t p = j.find(pat, i);
        if (p == std::string::npos) return false;
        p += pat.size();
        dst = std::strtol(j.c_str() + p, nullptr, 10);
        i = p;
        return true;
    };
    while (true) {
        size_t obj = j.find('{', i);
        if (obj == std::string::npos) break;
        i = obj;
        Field f{};
        if (!readKeyVal("s", f.s)) break;
        readKeyVal("offset", f.offset);
        readKeyVal("coeff", f.coeff);
        readKeyVal("ZERO", f.ZERO);
        readKeyVal("b3", f.b3);
        readKeyVal("XFER", f.XFER);
        readKeyVal("WA", f.WA);
        readKeyVal("RA", f.RA);
        out.push_back(f);
        size_t end = j.find('}', i);
        if (end == std::string::npos) break;
        i = end + 1;
    }
    return out;
}

// Pull a single integer value for `key` out of a flat meta.json.
inline int readMetaInt(const std::string& path, const char* key, int dflt)
{
    std::vector<uint8_t> bytes = readBytes(path);
    std::string j(bytes.begin(), bytes.end());
    std::string pat = std::string("\"") + key + "\":";
    size_t p = j.find(pat);
    if (p == std::string::npos) return dflt;
    return (int)std::strtol(j.c_str() + p + pat.size(), nullptr, 10);
}

} // namespace golden
