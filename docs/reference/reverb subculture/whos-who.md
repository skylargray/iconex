# Who's Who — Gearspace Reverb Threads

**Sources:**
- "Lexicon Reverbs: A Brief Bestiary" (High End, 14 pages, 407 posts) → `lexicon-bestiary-combined.md`
- "Reverb Subculture" (GeekZone, 36 pages, ~1,059 posts) → `reverb-subculture-pages-01-07.md` through `33-36.md`

---

## Quick-Reference Trust Table

| Handle | Real Identity | Affiliation | 224XL Relevance | Trust |
|---|---|---|---|---|
| **Nobody Special** | **Michael Carnes** | Lexicon → Exponential Audio → iZotope | High (secondary; source code lost) | ★★★★★ |
| **Casey** | **Casey (Bricasti)** | Bricasti Design (formerly Lexicon-adjacent) | High (knows 8080/ARU architecture) | ★★★★★ |
| **Larry the O** | Unknown (arrived Lexicon 1979) | Lexicon 1979–mid-1980s bench tech | **★★★★★ for pre-XL history** | ★★★★★ |
| **dale116dot7** | Dale | DIY DSP engineer; vintage repair | **Highest** (read service manual; has disassembled code) | ★★★★★ |
| **seancostello** | **Sean Costello** | ValhallaDSP (founder) | High (algorithm theory; analyzed algorithms) | ★★★★☆ |
| **acreil** | Unknown | Independent researcher / Pure Data | High (confirmed 224 IR vs Dattorro; RE expert) | ★★★★☆ |
| **zmix** | **CZ** (Chuck Zwicky?) | Independent; collector; Ensoniq DP developer | High (owns hardware; ear witness; documents modulation) | ★★★☆☆ |
| **Warp69** | Unknown | Independent; serious collector | Medium-High (owns 224XL/480L; parameter expert) | ★★★☆☆ |

---

## Full Dossiers

---

### Nobody Special = Michael Carnes
**Lexicon DSP Engineer → Exponential Audio → iZotope**

#### Identity Confirmed
Post #335 (Bestiary p.12) quotes him as "Michael Carnes." Posts #346 and #355 address him as "Michael." Post #355 (April 4, 2019): *"congrats on the sale of exponential to izotope...you would have left Lexicon, created your own plug in company."* Post #337: *"I haven't been at Lexicon for more than two years."* Posts in Reverb Subculture identify him the same way; post #287 (SubC p.10) directly states *"Mr. Carnes, whatever your brewing up at Exponential."* He was still participating in Reverb Subculture after leaving Lexicon (~2012).

#### Career Arc
- Late-1970s: started professional software dev (real-time programming, control systems)
- Joined Lexicon after the original 224 (which "predates even me")
- Left Lexicon ~Jan 2012 (SubC p.10 post #279 says "haven't been with Lexicon since early January")
- Founded **Exponential Audio** (PhoenixVerb, R2, Excalibur)
- Exponential Audio **acquired by iZotope early 2019**

#### What He Knows (Primary Source)
- Wrote PCM96 firmware AND plugin code: *"I wrote the code for both."*
- Designed: PCM96 Hall, Room, and Chamber algorithms; Vintage Plate (plugin-only); LARES port to 960L and DNA/Wenger chip
- One of "4–5 people in the world who ever programmed a Lexichip 3"
- Knew David Griesinger and Barry Blesser personally
- On the 224: *"The actual source code was lost many many years ago."*
- 8MB SDRAM on PCM96 (not just internal SHARC memory as Casey assumed)
- PCM96 uses 32-sample processing blocks (SubC p.13-17, post #504)

#### Trust by Domain
- PCM96, 960L, 480L, 300, 90/91: ★★★★★
- 224-era genealogy (from Griesinger + Blesser diagrams): ★★★★☆
- 224 internal mechanics (no source code): ★★★☆☆

#### Key Claims
- Concert Hall = "the only algorithm that works that way" — no Spin/Wander, uses chorus
- PCM90/91 Random Hall: 20-bit memory vs 18-bit in 480L, extra bit in coefficient architecture
- PCM80/81 algorithms squeezed into single Lexichip2
- Pantheon plugin = "not up to the level of the hardware units"

---

### Casey
**Co-designer, Bricasti M7 (formerly Lexicon-adjacent)**

#### Identity
"Casey" with user info "Bricasti." NS calls him "a competitor." Refers to M7 in third person. Had private conversations with Griesinger (~2004). Deep inside knowledge of 480L and early Lexicon history. He and NS are clearly peers from the same industry era.

#### Career Arc
Co-founded Bricasti Design with Brian Zolner — both are former Lexicon-adjacent engineers. Designed the Bricasti M7, universally regarded as the premier contemporary algorithmic reverb.

#### What He Knows
- **Critical 224 modulation fact (SubC p.33-36, post #1028):** The 8080 microprocessor "randomly missed some delay updates... could not quite keep up at times." This is **why the 224's Concert Hall modulation sounds "random"** — it is literally the CPU falling behind and missing coefficient writes, not intentional randomization design. This is the most important single sentence about 224 modulation in either thread.
- Walked the Reverb Subculture through building an EMT-250 reverb from scratch (posts #14–45, p.1–2)
- 480L ARU: 80-step microcode × 4 cores; standard algs use 2 cores; HD uses all 4. *"The 480 also uses an 8 bit microprocessor which re-writes the 80 step microcode in the ARUs to provide the dynamic reverb modulation."* (Bestiary post #300)
- Lexichip-3: 256 steps. 960L: 4 Lexichips + 2 × 8-bit µPs for dynamic microcode.
- 224 Concert Hall: 120 instructions per zmix estimate; one LFO, "multiple cases, presumably with every other one in opposition" (SubC p.33-36, post #1028)
- M7 algorithm philosophy: 10+ parallel mono reverb algorithms; builds WITH existing stereo image rather than against it
- Knew Griesinger personally; consulted with Chris Moore (Ursa Major), Jeff Stanton (ADR reverse-engineer)

#### Trust
- 480L/Lexichip ARU architecture: ★★★★★
- 224 modulation mechanism (Casey's 8080 claim): ★★★★★ (explains the empirical data)
- PCM96 internals: ★★★☆☆ (made one wrong public assumption; NS corrected him)

---

### Larry the O
**Arrived Lexicon 1979; Lead bench tech on 224X**

One-time poster (Bestiary posts #242, #247, p.8–9). Primary source on pre-NS Lexicon history.

#### What He Knows (First-Hand)
- Arrived Lexicon 1979, week of PrimeTime and 224 release parties; lead bench tech through 224X introduction; wrote several presets in the 224X release.
- **Eyewitness confirmation:** *"The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once. Man, he worked every line of that stuff."*
- Griesinger origin story: Harvard professor, found Schroeder papers (15 years old, why he missed them searching 10 years back), met Blesser who pointed to them, described Schroeder as "nasty little rooms," developed independently, approached Dr. Francis Lee (Lexicon founder) at Boston AES chapter meeting.
- **224X Chorus program:** Used the same random modulation as the reverberators — not LFO. Made it to PCM70 v3; gone in v4. ("I kept one of my PCM70s at v3.")
- Gary Hall wrote 224X effects microcode (Resonant Chords, Multi-band Delays) AND PCM41/42 microcode. The random modulation mechanism in the 224 is Griesinger's invention; the effects programs are Gary Hall's.
- Convened a 1986 Mix magazine reverb roundtable: Griesinger, Agnello, Moorer, Neatrour (5-part series).

#### Trust
★★★★★ for early Lexicon history (1979–early 1980s). Memory caveats self-noted. NS confirmed his account.

---

### dale116dot7
**DIY DSP Engineer and Vintage Lexicon Repair Tech**

#### Identity
"Dale." Professional embedded systems programmer (engine controllers, motor drives). Has personally repaired PCM60s, PCM70s, PCM91s, LXP1s and newer units. Has **disassembled firmware** for 224, PCM70, PCM91, and 480L (cannot share — Bestiary post #807). Built custom reverb hardware (AL3201-based, then DSP56366 + 512k SRAM).

#### Most Relevant Posts for 224XL Project

**Bestiary post #183 (p.7) — THE CRUX POST for session-0021:**
> *"The 224XL service manual indicates that the program is 100 steps. However, the microcode actually could do 128 steps — the program counter is cleared by writing an address with bit 3 set to the I/O space. The 224 (non-XL) version shows the same sort of thing — the WCS resets the PC. Though many of the Lexicons have a 128-step program counter, not all of them actually use all 128 steps."*

Direct from service manual. PC is 7-bit (128 max), programs use 100. Reset is triggered by a WCS I/O write with bit 3 set — not a dedicated hardware reset line.

**Bestiary post #298 (p.10) — Full ARU architectural breakdown:**
- 224/224X: 16-bit ARU, **6-bit multiply, 8 ticks/instruction**, 100-instruction program, 74S283 fast adders, 16k/32k/64k RAM
- 200: 74F181 ALU, 3–4 bit multiplier, 128 microinstructions @ 3 ticks each
- PCM70: Same ARU as 200 in ASIC, **18-bit** version, same program length, higher sample rate
- 480L: 4-core, 4-bit multiply, **80 instructions/core** × 4 = 320/sample
- Lexichip-1/-2: Faster 200-type ARU, 20-bit, **128 program steps**

**SubC pages 13-17, post #378 — WCS Timing Constraints:**
- 224 has 6-bit multiplier with **5-bit binary point** (coefficient resolution = 1/32 = 0.03125)
- **250ns RAM** — only slightly faster than 8080 instruction execution time
- The 8080 can only update coefficients during NOP DSP instructions to avoid thrashing code fetches
- PCM70 improved this with ACTIVE/INACTIVE WCS banks plus a 'COPY' signal, enabling faster updates and 6-voice chorus
- **This explains why the 224XL's modulation update rate is severely limited**

**SubC pages 23-27, post #807:**
- Has disassembled code for 224, PCM70, PCM91, 480L; confirms straightforward DSP architecture with microcode sequencer "openly visible"
- Says 480L interprocessor communication is "complex"

#### Trust
★★★★★ for hardware implementation details from service manuals. Self-corrects. Precise. His 183/298/378 posts are the single most hardware-specific evidence in either thread.

---

### seancostello (Sean Costello)
**Founder, ValhallaDSP**

#### Identity
Full name given in thread. User info "ValhallaDSP." Blog: "The Halls of Valhalla." Worked at Analog Devices ~2003–2004 (SHARC/Blackfin). Co-authored Ambisonics reverb architecture paper with Joseph Anderson (presented at Austrian conference). Worked at CCRMA, Stanford area. Professional reverb designer since ~2000.

#### What He Knows
- Algorithm theory: Schroeder, Gerzon, Jot, Gardner, Dattorro, Blesser (book + patents), Griesinger (psychoacoustics papers), Moorer, Puckette
- Implemented reverbs professionally since ~2000 (first FDN implementation, Dattorro implementation for client)
- Forensic listener: identifies allpass ringing, tape-loop patterns, left-right flutter, modal density by ear
- Worked on Csound, Pure Data, SHARC, Blackfin, FV-1 platforms
- Sean directly corresponded with **Keith Barr** (Alesis/Spin) before Barr's death (2010); obtained emails about Quadraverb topology
- Co-published AES paper on ambisonics reverb (2009)

#### 224XL-Specific
- **Sample rate identification (SubC p.18-22, post #556):** 224/224X = 29.761 kHz; 224XL = 34.125 kHz. (Note: project session data shows CONCERT at 26.667 kHz — verify against hardware.)
- Systematic modulation breakdown by unit (Bestiary post #172, p.6): all 224XL algorithms used time-varying chorus; PCM60 none; PCM70 chorus on Concert Hall only; 480L Spin/Wander on Random Hall/Ambience; etc.
- On 224XL modulation (SubC p.18-22, post #552): *"I haven't been around a 224XL for about 18 years, so I'm not sure exactly how the modulation works. However, the division of the delay into two blocks certainly implies a fixed delay, and a time-varying delay that is linearly interpolated."*
- **Dattorro diagram confirmation discussion:** (SubC p.18-22) identified two Griesinger algorithms — "old one" at 29.761 kHz (AES published) and "new one" at 34.125 kHz

#### Trust
★★★★☆ on algorithm theory and DSP practice. ★★★☆☆ on Lexicon internals (manual-derived, not insider). Honest about what he doesn't know.

---

### acreil
**Independent Algorithmic Reverb Reverse-Engineer**

#### Identity
Username "acreil." Joined May 2010, 3,375 posts in Reverb Subculture thread. Works in Pure Data. No real name given. Expert in deriving algorithm topology from impulse responses. Has built a simulator and disassembler for Alesis Midiverb firmware EPROMs. Has reverse-engineered: Quantec QRS, Sony DRE-2000/SDR-1000/MUR-201, Yamaha REV5, Alesis Midiverb/Midiverb 4, Ibanez SDR-1000.

#### What He Knows
- **Confirmed Dattorro diagram against real 224 IRs (SubC p.33-36, post #1042):** *"That image does match actual 224 concert hall IRs up to the three recursive allpass filters part at least (barring minor differences in delay lengths)."* This validates the Dattorro/Griesinger published Concert Hall topology against measured hardware.
- Quantec QRS reverse-engineering (SubC p.18-22, posts #581–592): 16 resonators (comb + embedded APF), 2 delays each, 20 kHz sample rate, 5 MIPS (~16 instructions/resonator), output polarity mixing (50% in-phase, 50% out-of-phase)
- 224XL parameters (SubC p.8-12, posts #310-315): different delay times, levels, phases vs 224; 7% larger diffusion delays; Diffusion control added in Rev 4 software only; early taps unmodulated; static taps have 12ms+ differences
- Modulation in 224: identifies interpolation as "paused" in Dattorro diagram (5-sample vs 121-sample modulation depth interpretation)
- Reverse-engineering methodology: Audacity + Matlab scripts; autocorrelation for comb identification; reverse-processing through allpasses to extract topology
- On 224 hardware: *"The Lexicon 224 models are a lot more impressive once you realize that the hardware isn't very capable. They really got as much as possible out of barely adequate resources. There's probably more ingenuity there than anywhere else."* (SubC p.33-36, post #974)
- Midiverb: uses address *increments* rather than base offset circular buffer; has written working simulator

#### Trust
★★★★☆ on algorithm reverse-engineering methodology and topology identification. His confirmation of the Dattorro diagram against real 224 IRs is a primary validation. Not an insider; derives from measurements.

---

### zmix
**Independent — Vintage Reverb Collector, Critical Listener, Ensoniq Developer**

#### Identity
Handle "zmix." Signs some posts "CZ." Likely **Chuck Zwicky** based on professional mixing background and Ensoniq connection. Was involved in DP/4+, DP/2, and DP/Pro development at Ensoniq (SubC p.33-36, post #1019) — created the "Expert Verb" algorithm for DP/Pro using the Dattorro topology. Created the "Black 224" factory preset for DP/Pro. Helped UA with their 224 emulation for ~2 years. Has physical possession of: 1979-era original Lexicon 224 (owned 10+ years then sold), PCM70 (×2, current), PCM96, EMT 250 (1977), Audio Damage Eos, Sony DRE-2000 (multiple), SDR-1000, MUR-201. Has schematics and EPROMs for Sony units. Personally knows Barry Blesser.

#### 224-Specific Knowledge
- **Concert Hall LFO (SubC p.33-36, posts #1027, #1029):** *"Lexicon only use one LFO in their concert hall...Single random LFO is injected in a (very) few places...in another algo a simple triangle only injected once in one side of the loop, and what is surprising is that you don't hear it as such."*
- **224 modulation analysis (SubC p.8-12, posts #284, #289):** 224 Mode Enhancement at 01 = greatest modulation depth with NO obvious pitch warble; PCM96 Concert Hall = single unrandomized LFO (no randomization); 224 Concert Hall = ~120 instructions
- **224 stereo topology (Bestiary post #394):** *"The reverb is essentially a large loop with inputs 180° on either side and the outputs 90° rotated from them."* Left input → left out quickly, then right out diffusely (explains characteristic left-to-right bloom)
- **PCM70 modulation documented (SubC p.8-12, post #156):** PCM70 modulation = 2.3Hz triangle wave + slower ~0.5Hz random waveform; PCM96 = 1.5Hz, not randomized
- Comparison tests with audio files: blind test (EMT250, 224, PCM96, Eos), Concert Hall modulation comparison (PCM70, PCM96, 224 at 35-second decay)
- Griesinger 1979 article: "high diffusion not always desirable for first 200ms" (SubC p.23-27, post #805)
- Helped UA for 2 years on 224 emulation; considers result "90% there"

#### Trust
★★★★☆ for perceptual/listening claims with hardware in hand and audio file evidence. ★★★☆☆ for internal technical claims (sophisticated user, not insider). His modulation documentation and stereo topology observation are primary-source data.

---

### Warp69
**Independent — Serious Lexicon Collector**

#### Identity
Anonymous. Owns: 480L (classic card + surround/HD card), 224XL, PCM91.

#### Key Contributions
- 224 vs 224XL structural differences from impulse response analysis (SubC p.8-12, posts #310-315): different delay times, levels, phases; 7% larger diffusion delays in 224XL; Depth range: 224 = 0-71, 224XL = 0-99; Diffusion control (SHIFT+DEPTH, range 01-63) is 224XL-only and added in Rev 4 software
- Concert Hall: PCM70 Chorus parameter 0-99 (below 50 = off, above 60 = very pitchy)
- 224XL early taps unmodulated; static taps have 12ms+ differences
- Identifies three modulation type categories (SubC p.13-17, post #380): #1 interpolation with LFO, #2 crossfading between non-contiguous taps, #3 coefficient/matrix manipulation
- 480L parameter expertise: Wander maxes at 10ms at 39m; Surround/HD = same algo, HD mixes 4 outputs to stereo
- Caught NS and Sean Costello errors on multiple occasions; consistently accurate

#### Trust
★★★★☆ for 480L/224XL parameter observations. ★★★☆☆ for algorithm internals.

---

## Key Peripheral Figures

**Keith Barr** (Alesis/MXR/Spin Semiconductor — deceased 2010)
Designed Midiverb, Quadraverb, Midifex, FV-1. Corresponded with Sean Costello. Evolved from parallel combs → embedded allpass in combs → single-loop topology. Quote (email to Sean, Bestiary post #918, SubC p.28-32): *"Everything I write today is single loop, with modifications as to input signal injection and output tap selection."* Used logic analyzer to watch 224 impulse response on oscilloscope (SubC p.23-27, post #694).

**David Griesinger** (Lexicon 224 designer; Harvard professor; low-energy nuclear physicist)
Not a forum participant but referenced constantly. Designed the original 224 reverb; developed the Concert Hall algorithm. After leaving Lexicon, continued psychoacoustics research. Had the 224 source code (SubC p.23-27, post #461). Later "refuted" the early reflections model (SubC p.23-27, post #808). 1979 article: "high diffusion not always desirable for first 200ms." Competitive relationship with Barry Blesser ("always been just a wee bit competitive" — SubC p.23-27, post #461).

**Barry Blesser** (EMT-250 designer; Lexicon consultant; UAD consultant)
First Lexicon employee (wrote software for Delta-T 101). PCM80 project manager. Has consulted since. Designed UAD EMT-250 emulation. 2006 patent US7062337 on quadrature coefficient modulation. Notch-pass patent for pole removal from allpass filters. AES paper on thermal convection in reverb perception. "Spaces Speak, Are You Listening?" (book).

**Jeff Stanton** (Ursa Major → AKG)
Reverse-engineered the Lexicon 224 Concert Hall algorithm using a logic analyzer. Barry Blesser adapted Stanton's reverse-engineering for the AKG ADR-68K. Later Lexicon versions incorporated Blesser's version back. This means the Concert Hall algorithm has been reverse-engineered before and that re-engineering exists externally (SubC p.23-27, post #702-705).

**Jon Dattorro** (Ensoniq DP series)
Published the Griesinger plate reverb algorithm in AES (with permission from Griesinger letter). His published Concert Hall diagram has been **confirmed against real 224 IRs by acreil** (SubC p.33-36, post #1042) — matches "up to the three recursive allpass filters part." The 34.125 kHz algorithm in his publication is the 224XL Concert Hall topology.

---

## 224XL Research Notes — Critical Findings Ranked

### 1. ★★★★★ The RESET is an I/O Write, Not a Hardware Line
(dale116dot7, Bestiary post #183 from service manual)
*"The program counter is cleared by writing an address with bit 3 set to the I/O space."*
The 8080 triggers reset by writing a specific I/O address. This is a firmware-initiated WCS write, not a dedicated microword bit that drives an external reset pin. The PC wraps naturally at 128. Steps 100-127 are unused, and the "reset" at step 99 is the 8080 writing I/O to start the next sample cycle. Session-0021 hypothesis confirmed from service manual.

### 2. ★★★★★ The 224's "Random" Modulation Is CPU Timing Jitter
(Casey, SubC p.33-36 post #1028)
*"Microprocessor creating LFO 'randomly missed some delay updates...could not quite keep up at times.'"*
The 224 Concert Hall's distinctive random-sounding modulation is not an elaborate pseudo-random algorithm — it's the 8080 falling behind and missing coefficient writes. The WCS can only be updated during NOP DSP instructions (dale post #378). When the 8080 is busy and misses its window, the delay coefficient stays frozen at the previous value, creating irregular/aperiodic modulation. **This is the mechanism.** zmix's observation that "single random LFO is injected in a very few places" is consistent — the LFO is simple (triangle or similar) but the update timing is irregular.

### 3. ★★★★★ Dattorro Diagram Confirmed vs Real 224 IRs
(acreil, SubC p.33-36 post #1042)
*"That image does match actual 224 concert hall IRs up to the three recursive allpass filters part at least (barring minor differences in delay lengths)."*
The published Dattorro/Griesinger Concert Hall topology is a valid representation of the actual 224 Concert Hall algorithm. The topology: nested recursive allpass filters + cross-coupled delay loops + modulated tap(s).

### 4. ★★★★★ WCS Coefficient Resolution: 6-bit, 1/32 Steps
(dale116dot7, SubC p.13-17 post #378)
The 224's multiplier has 6-bit width with 5-bit binary point = coefficient range ±1.0 at 1/32 resolution. WCS updates are constrained to happen during DSP NOP cycles only; 250ns RAM barely fast enough for 8080. PCM70 introduced dual WCS banks with COPY signal to solve this — the 224XL does not have this improvement.

### 5. ★★★★★ Sample Rate: 224XL = 34.125 kHz
(seancostello, SubC p.18-22 post #556)
The 224XL runs at 34.125 kHz (the 224/224X ran at 29.761 kHz). The published Dattorro algorithm uses this sample rate. **Note: project session data shows CONCERT running at 26.667 kHz — this discrepancy needs investigation.** The 26.667 kHz figure is 100 steps × 266.67 Hz = implies a different system clock than expected. Verify with service manual.

### 6. ★★★★☆ 224 Stereo Loop: Inputs 180° Apart, Outputs 90° Rotated
(zmix, Bestiary post #394)
*"The reverb is essentially a large loop with inputs 180° on either side and the outputs 90° rotated from them."* Left input enters the loop at one point; right input enters 180° around the loop. Outputs are taken 90° from the input injection points. This creates the characteristic bloom: sound enters left channel, reappears on the left quickly as an early reflection, then crosses to the right diffusely as the energy recirculates. This is a TOPOLOGY feature, not a parameter.

### 7. ★★★★☆ 224 Algorithm Reverse-Engineered Before
(Casey, SubC p.23-27 posts #702-705)
Jeff Stanton (Ursa Major) reverse-engineered the 224 Concert Hall algorithm using a logic analyzer. Barry Blesser adapted this for the AKG ADR-68K. Later Lexicon versions incorporated Blesser's version back. This external reverse-engineering exists and the algorithm is "known" in the industry.

### 8. ★★★☆☆ 224 vs 224XL Structural Differences
(Warp69, SubC p.8-12 posts #310-315)
224XL diffusion delays are ~7% larger than 224. Depth parameter range: 224 = 0-71, 224XL = 0-99. Diffusion (SHIFT+DEPTH) is 224XL-only, range 01-63, added in Rev 4 software. Early taps unmodulated in 224XL; static taps have 12ms+ differences. Late reverb tank structure differs between 224 and 224XL.
