# Reverb Subculture Thread — Research Summary

**Coverage:** "Lexicon Reverbs: A Brief Bestiary" (14 pages, 407 posts) + "Reverb Subculture" (36 pages, ~1,059 posts)
**For full detail:** See source files in this folder. Post numbers reference both threads; bestiary = "B#xxx", subculture = "S#xxx".
**For contributor trust:** See `whos-who.md`.

---

## Part 1 — 224/224XL Hardware Architecture

### 1.1 ARU Chip Specifications (from service manuals, dale116dot7)
**Source:** Bestiary post #298, SubC post #378 (dale116dot7)
**Files:** `lexicon-bestiary-combined.md` p.10, `reverb-subculture-pages-08-12.md` p.10

| Unit | Bit Depth | Multiply | Ticks/Instr | Program Steps | RAM | ADC/DAC |
|---|---|---|---|---|---|---|
| 224 | 16-bit | 6-bit (2 coeff bits/cycle) | 8 | 100 (of 128) | 16k | 12-bit (14-bit equiv) |
| 224X | 16-bit | 6-bit | 8 | 100 (of 128) | 32k or 64k | 12-bit |
| 224XL | 16-bit | 6-bit | 8 | 100 (of 128) | 32k or 64k | 12-bit |
| 200 | 16-bit | 3–4-bit | 3 | 128 max | — | — |
| PCM70 | 18-bit | 3-bit (ASIC) | 3 | 128 | — | 16-bit |
| 480L | 16-bit | 4-bit | — | 80 × 4 cores | — | — |
| Lexichip-1/-2 | 20-bit | same | faster | 128 | — | — |

**Key detail:** 6-bit multiply = 5-bit binary point = coefficient resolution of 1/32 = 0.03125. This limits the precision of chorus/modulation coefficients in the 224 ARU.

**ARU chip family:** 224 uses 74S283 fast adders. 200/PCM70 uses 74F181 ALU (or ASIC equivalent). The "ARU" in the 224 = custom TTL chips, NOT a Lexichip.

### 1.2 Program Counter Architecture
**Source:** Bestiary post #183 (dale116dot7, from service manual); Bestiary post #242 (Larry the O, eyewitness)
**File:** `lexicon-bestiary-combined.md` p.7, p.8–9

- Program is **100 steps** but PC is **7-bit (128-step capable)**
- **PC reset mechanism:** *"The program counter is cleared by writing an address with bit 3 set to the I/O space."* (from 224XL service manual)
- This is a **firmware-initiated WCS write** — the 8080 writes an I/O address with bit 3 set at the end of each sample, which resets the PC. It is NOT a dedicated reset pin in the microword.
- The 224 (non-XL) resets the same way. Steps 100-127 are structurally available but unused.
- Larry the O (eyewitness, 1979): *"The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once."*
- **Implication for RESET-decode (session-0021):** tcWR·OFST3/ being the RESET signal is the hardware gate that fires when the 8080 writes that particular I/O address. The PC wraps at 127→0 naturally. The "reset at step 99" is false-positive detection; the PC never STOPS at 99 — the 8080 writes a reset after step 99 has already executed and the cycle begins again. The 128-step wrap hypothesis is confirmed.

### 1.3 8080 / T&C Timing Constraints
**Source:** SubC post #378 (dale116dot7), SubC post #1028 (Casey), Bestiary post #300 (Casey)
**Files:** `reverb-subculture-pages-13-17.md` p.13, `reverb-subculture-pages-33-36.md` p.33, `lexicon-bestiary-combined.md` p.10

The 8080 at 6 MHz runs the modulation/coefficient update loop:
- **250ns RAM** — barely faster than 8080 instruction execution time; leaves minimal slack
- 8080 can only write WCS coefficients **during DSP NOP cycles** — writing during active DSP cycles would thrash code fetches
- **Casey's critical observation (S#1028):** The 8080 "randomly missed some delay updates... could not quite keep up at times." This is **the mechanism behind the 224's "random" Concert Hall modulation** — the LFO is simple (triangle or similar), but the 8080 drops coefficient writes when it falls behind, creating aperiodic updates that sound random/organic.
- The PCM70 improved this with ACTIVE/INACTIVE dual WCS banks plus a 'COPY' signal to atomically swap them during one wordclock period, enabling a 6-voice chorus without artifacts.
- **For the 480L (Casey, B#300):** Same principle but explicitly stated: *"The 480 also uses an 8 bit microprocessor which re-writes the 80 step microcode in the ARUs to provide the dynamic reverb modulation."*

### 1.4 Sample Rate
**Source:** SubC post #556 (seancostello)
**File:** `reverb-subculture-pages-18-22.md` p.18

- 224/224X: **29.761 kHz**
- 224XL: **34.125 kHz**
- These match the Dattorro published algorithm sample rates (one "old" AES algorithm at 29.761 kHz, one "new" expanded algorithm at 34.125 kHz)

**Discrepancy to investigate:** Project session data shows CONCERT running at 26.667 kHz (= 100 steps × 266.67 Hz clock). The 34.125 kHz figure comes from seancostello matching to Dattorro's published topology, not directly from service manual measurements. Verify with actual service manual clock specs.

---

## Part 2 — Concert Hall Algorithm

### 2.1 Topology Confirmation
**Source:** SubC post #1042 (acreil); SubC posts #548–558 (seancostello, acreil, volumetric)
**Files:** `reverb-subculture-pages-33-36.md` p.33, `reverb-subculture-pages-18-22.md` p.18

acreil (p.33-36, post #1042): *"That image does match actual 224 concert hall IRs up to the three recursive allpass filters part at least (barring minor differences in delay lengths)."*

The Dattorro/Griesinger published Concert Hall diagram is confirmed against real 224 IRs. Key structural elements confirmed:
- Nested recursive allpass filters (3 APFs in the recursion)
- Cross-coupled feedback delay loops
- Modulated tap(s) — interpolated delay

Two published algorithms:
- "Old" at 29.761 kHz = AES-published (earlier 224/224X algorithm)
- "New" at 34.125 kHz = expanded version (224XL Concert Hall)

Seancostello (S#557): *"I'd guess Concert Hall. Dark Hall would have more interpolated delay lines. Bright Hall would have the high damping 1-pole in a different location."*

### 2.2 Modulation Architecture
**Source:** SubC posts #1027–1029 (zmix, Casey); SubC post #156 (zmix); SubC post #378 (dale116dot7); SubC post #1028 (Casey)
**Files:** `reverb-subculture-pages-33-36.md`, `reverb-subculture-pages-08-12.md`, `reverb-subculture-pages-13-17.md`

**What the 224 Concert Hall modulation actually is (synthesis of all evidence):**

1. **One LFO** (zmix S#1027): *"Lexicon only use one LFO in their concert hall."*
2. **LFO waveform** (Larry the O, Bestiary #247): The 224X Chorus program used "the same random modulation on the delay voices that was used in the reverberators." This implies the reverb modulation source is used directly.
3. **The "randomness" mechanism** (Casey S#1028): The 8080 "randomly missed some delay updates... could not quite keep up at times." The LFO itself may be deterministic (triangle or sine); the randomness comes from **missed CPU writes** creating timing jitter in the modulation update sequence.
4. **PCM70 comparison** (zmix S#156): PCM70 modulation = 2.3Hz triangle wave + slower ~0.5Hz random waveform. This is the documented modulation for a later unit; the 224 is similar.
5. **Injection points** (zmix S#1029): *"Single random LFO is injected in a (very) few places...in another algo a simple triangle only injected once in one side of the loop, and what is surprising is that you don't hear it as such."*
6. **Casey on LFO phase** (B#1028): Used in "multiple cases, presumably with every other one in opposition" — same LFO at 0° and 180° phase offset to prevent wholesale pitch shift.
7. **Modulation depth** (zmix S#220): Up to 50 cents at extreme peaks at full HF rolloff.
8. **Modulation resolution** (dale S#378): 6-bit multiplier with 5-bit binary point = coefficient steps of 1/32. Modulation position updates limited by NOP windows.

**Comparison table:**

| Unit | LFO Character | Max Depth | Notes |
|---|---|---|---|
| 224 Concert Hall | One LFO, random-seeming (CPU timing jitter) | ~50 cents | Even distribution, no obvious pitch warble |
| PCM70 Concert Hall | 2.3 Hz triangle + 0.5 Hz random | Similar | Above 60% setting = very pitchy |
| PCM96 Concert Hall | Single unrandomized LFO | Similar | "Sounds like single unrandomized LFO" — zmix |
| 480L Random Hall | Spin/Wander (separate controls) | Up to 22ms wander | Different mechanism entirely |

### 2.3 The "Constant Density Plate" Context
**Source:** Bestiary posts #176-177 (Casey, seancostello); SubC posts #45-50 (Casey)
**Files:** `lexicon-bestiary-combined.md` p.6, `reverb-subculture-pages-01-07.md` p.2

The Constant Density Plate in the 224/224XL was Griesinger's deliberate response to the EMT-250's topology (parallel combs with tapped outputs = constant echo density). Casey confirmed in the Reverb Subculture tutorial that the 3-loop / 9-tap / output-allpass structure *IS* the EMT-250 topology. The CD Plate in the 224 approximates this.

The "Rich" algorithms (Rich Plate, Rich Chamber, Rich Hall) use the Schroeder-derived variable-density approach instead.

### 2.4 The Stereo Topology
**Source:** Bestiary post #394 (zmix, from 10+ years of ownership); SubC post #429 (zmix)
**Files:** `lexicon-bestiary-combined.md` p.14, `reverb-subculture-pages-13-17.md` p.13

*"The reverb is essentially a large loop with inputs 180° on either side and the outputs 90° rotated from them."*

Stereo structure (SubC p.13-17, post #429): "Left string output feeds to right input and vice versa" in a "traffic roundabout" pattern. This means:
- Left input enters loop at 0°
- Right input enters loop at 180°
- Left output is tapped at 90° (between left input and right input injection)
- Right output is tapped at 270°

**Perceptual consequence:** When you inject signal in the left channel, you hear:
1. Left early reflections quickly (near left input tap at 90°)
2. Cross to right as signal recirculates (right tap at 270°, now diffuse)

This characteristic left-to-right bloom is a TOPOLOGY feature, not a parameter. **No impulse response convolution can replicate it** (zmix confirmed).

---

## Part 3 — Algorithm Genealogy

### 3.1 The Two Lexicon Eras
**Source:** SubC post #375 (locust_tree); Bestiary posts #17-22 (NS); SubC post #1020 (acreil)
**Files:** `lexicon-bestiary-combined.md` p.13, p.1

**Era 1 (224 through PCM70):** "Lexicon Era 1" reverbs (locust_tree)
- Random modulation in FDN allpass network
- Pitch modulation present (the "dreamy" sound)
- PCM70 ported from 224XL with only 2 differences: slightly lower 15kHz bandwidth, mono input only
- Modulation: pseudo-random pitch modulation from CPU timing jitter

**Era 2 (480L onward):** Post-480L Lexicon
- Spin/Wander mechanism: "random stepped interpolation to break up resonant modes" (locust_tree)
- "No pitch modulation" — later deemed "unnatural"
- zmix: *"I lost interest in Lexicon reverbs after the PCM70... subsequent Lexicon reverbs used a random stepped interpolation to break up the resonant modes which exhibited no pitch modulation. Ho hum."*
- NS agrees: these approaches just "approach the design differently"

### 3.2 Algorithm Inheritance Map
**Source:** Multiple NS posts (Bestiary); Casey corrections (Bestiary post #119); SubC posts (NS, Casey)
**Files:** `lexicon-bestiary-combined.md` p.4, p.7

```
224 (1979, 29.761 kHz)
├── 224X / 224XL (34.125 kHz, expanded programs, diffusion control)
│   ├── PCM70 (simplified, mono in, 15kHz BW, same core algs)
│   │   └── LXP series, Alex, Reflex (dumbed-down 480-style, NOT 224-style)
│   └── 480L Classic Card (224/70 era algorithms ported back)
│       └── PCM91 Concert Hall (added, PCM91-specific additions)
│
480L (1987, new algorithms: Random Hall, Ambience, Dense/Surround)
├── 300 (90% similar to 480L algs; ~20% more processor than one 480L board)
├── PCM90/91 (Random Hall from 300 Random Hall; 20-bit memory; cleaner)
└── Nuverb TDM card (guts essentially a 300)
    └── LXP series (NOT 224/70-heritage — "dumbed-down 480 type hall")

PCM96 (floating-point SHARC + 8MB SDRAM)
├── Brings back Concert Hall (new code; Dave G thought NS "was nuts")
├── New Hall algorithm (transparent; first use of Blesser Hall technique)
├── New Room algorithm (~4 dozen reflection patterns, reverse parameter)
└── Vintage Plate (plugin-only)

960L
└── LARES (ported from 480L Surround/HD algo; 4 × Lexichip-3 + 2 × 8-bit µPs)
    └── DNA chip / Wenger practice room (another LARES port)
```

**Key correction (Casey, Bestiary #119):** The Surround/HD 480L cart = the "dense" algorithm (6 Voices/Dense), NOT based on Random Hall. The standard 480L algs run on 2 ARU cores; HD uses all 4.

### 3.3 Concert Hall Lineage and Reverse-Engineering
**Source:** SubC posts #702-705 (Casey, NS); SubC post #151 (Casey)
**Files:** `reverb-subculture-pages-23-27.md` p.23

1. Griesinger develops Concert Hall algorithm (~1978-1979)
2. Griesinger has the 224 code base (Casey confirmed in SubC p.01-07 post #151: *"224 code base still exists with David"*)
3. Jeff Stanton (Ursa Major) reverse-engineers Concert Hall from 224 using a logic analyzer
4. Barry Blesser adapts Stanton's RE for the AKG ADR-68K (Ursa Major → AKG sale)
5. Later Lexicon versions incorporate Blesser's version back
6. Dattorro publishes the Griesinger algorithm (with Griesinger's permission letter) — confirmed against real 224 IRs by acreil

**Conclusion:** The Concert Hall algorithm has been publicly reverse-engineered and published. Dattorro's published version is confirmed valid against measured hardware.

---

## Part 4 — DSP Design Theory (from Casey's Tutorial and Thread Discussions)

### 4.1 Casey's Reverb Design Pedagogy
**Source:** SubC posts #2–45 (Casey), confirmed across pages 1–2
**File:** `reverb-subculture-pages-01-07.md` pp. 1–2

Casey walked the thread through building a reverb from scratch. Key steps and conclusions:

**Step 1 — Three feedback loops:** 3 unequal loops (32k samples), sized by room mode calculator (e.g., ModeCalc). One output tap per loop, gains at end. This is already identifiably the EMT-250 topology.

**Step 2 — Multiple output taps:** 9 taps total (3 per loop); 5 for left, 4 for right with taps interleaved in time ("brain loves rocking left-right" — Griesinger psychoacoustic principle). Add 12dB/oct lowpass filter on input at ~12kHz.

**Step 3 — Output allpasses:** 3 series allpasses per output (70% of shortest loop, divided by golden ratio into 2, plus 2.5ms small one). Gains: 0.35, 0.45, 0.6 largest-to-smallest. Alternate feedback signs L/R. Reduce allpass sizes 5% on left, increase 5% on right.

**Step 4 — Modulation:** Random offsets in 5ms window, 16-step linear interpolation minimum, 10-50 samples/second rate.

**Step 5 — Casey confirms: This IS the EMT 250 topology** (SubC p.2, post #45). The EMT-250 is: 3 parallel feedback combs with output taps, fed into allpass diffusers.

**Key design principles extracted:**
- Tap spacing >50ms for statistical decorrelation (closer = audible comb filtering)
- Loop ratio shortest-to-longest: keep under 2:1
- Prime-number delay selection avoids harmonic coincidences (SubC p.28-32)
- Allpass in feedback loop creates ringing; long allpass delays prevent audible ringing (signal becomes noise-like through many passes)
- Modulated allpass coloration at reverb onset is inherent; long loops reduce audibility
- Cross-coupling loops reduces looping artifacts but can cause ringing between loops

### 4.2 Allpass Behavior in Feedback Loops
**Source:** SubC posts #6, #100, #104, #162 (Casey); #12, #68 (seancostello)
**File:** `reverb-subculture-pages-01-07.md` pp. 1–3

- Allpasses create frequency-dependent group delay → frequencies delayed longer persist later in tail
- This causes "metallic" finish audible in long tails
- Solutions: (a) reduce allpass gains, (b) randomize over time with modulation, (c) Blesser's "notch-pass" filter (pairs poles with matching zeros at different frequency locations — traded metallic tail for colored onset; Casey prefers modulation)
- Long nested APF delay times reduce ringing: "signal circulates through so many times that it comes out resembling narrow band noise rather than pitch modulation" (acreil, SubC p.18-22 #554)
- acreil (SubC p.33-36 #974): "The Lexicon 224 models are a lot more impressive once you realize that the hardware isn't very capable. They really got as much as possible out of barely adequate resources. There's probably more ingenuity there than anywhere else."

### 4.3 Constant vs. Variable Density
**Source:** SubC posts #45, #50 (Casey), #347 (Warp69), #277 (NS); Bestiary posts #178–179
**Files:** `reverb-subculture-pages-01-07.md` p.2; `reverb-subculture-pages-08-12.md` p.9

- **Constant density** (EMT-250, AMS RMX-16, Sony DRE-2000, Ursa Major): parallel combs, fixed output taps. Echo density doesn't increase — "pebble skimming across water" character. Reaches Nyquist limit quickly.
- **Variable density** (Schroeder/Lexicon Rich algorithms): allpasses in feedback loops, density builds over time. Denser, more diffuse tail. Can produce "tape loop" artifacts at high RT.
- **Lexicon 224 Concert Hall is variable density** — but the Constant Density *Plates* were Griesinger's response to the EMT-250.
- NS (Bestiary p.10 #280): "all reverbs are constant density after a couple-hundred milliseconds or so" (Nyquist limit applies regardless of topology)

### 4.4 Modulation Type Taxonomy
**Source:** SubC post #380 (Warp69); SubC post #381 (seancostello)
**File:** `reverb-subculture-pages-13-17.md` p.13

Three types identified by Warp69:
1. **Interpolation (LFO)**: Linear, allpass, or Lagrange interpolation on modulated delay tap, with sine/triangle/random LFO. What the 224 uses.
2. **Crossfading between taps**: Fade out one tap, fade in a non-adjacent tap. Yamaha has a patent (553150) on this. Used in "Random Hall" and later algorithms.
3. **Coefficient/matrix manipulation**: Changing FDN matrix values or gain coefficients directly. Blesser patent US7062337. Schlecht 2015 paper.

The 224 Concert Hall modulation = Type 1 (interpolation), with the "randomness" coming from CPU timing jitter (Casey S#1028).

---

## Part 5 — Psychoacoustics and Perception

### 5.1 Griesinger's Psychoacoustic Research
**Source:** SubC posts #17-19 (Casey), #258-263 (zmix, seancostello), #805, #808 (zmix)
**Files:** `reverb-subculture-pages-01-07.md` p.1; `reverb-subculture-pages-08-12.md` p.9; `reverb-subculture-pages-23-27.md` p.23

Key Griesinger claims referenced in thread:
- **Left-right rocking in low frequencies** as optimal for sense of space (cited by Casey S#17-19)
- **Inability to discern exact pitch** as aural cue for distance perception — applies primarily to solo vocalists due to impulsive waveform nature (seancostello S#261; but zmix tested on strings with striking results)
- **1979 article:** "high diffusion not always desirable for first 200ms" — contradicts common assumption
- **Later refuted Early Reflections model** (zmix S#808): the conventional early-reflections-determine-spaciousness model was reconsidered by Griesinger himself
- **50-150ms clarity window**: lecture mention that obstruction in this window degrades clarity; easier to manage in artificial reverb than real rooms (SubC p.13-17)

### 5.2 The "Pitch Modulation = Air Movement" Debate
**Source:** SubC posts #599-638 (Casey, Froombosch, seancostello, Shy)
**File:** `reverb-subculture-pages-18-22.md` p.18-22

Marketing claims that reverb pitch modulation simulates air movement were disputed:
- Casey: pitch changes from wind = zero; wind only causes amplitude modulation (not frequency shift)
- Froombosch: temperature gradients in rooms (2-4°C difference) create height-dependent sound speed affecting reflections; verified pitch shifts at distance
- seancostello: temperature pitch shifts apply to wind instrument air columns, NOT propagated sound
- **Conclusion:** The Lexicon/EMT modulation depths are far larger than any physically plausible air movement mechanism. The modulation is an aesthetic design choice, not physics simulation.

**Blesser confirmed (2001 AES presentation):** Natural acoustic spaces DO have pitch and amplitude randomness from thermal currents — but at much lower depths than commercial reverbs use.

### 5.3 Perception of Room Size
**Source:** SubC posts #597-598 (lukpio); SubC post #811 (Stian)
**Files:** `reverb-subculture-pages-18-22.md`, `reverb-subculture-pages-28-32.md`

- Room size perception is primarily from **modal density** (frequency domain) — the lowest resonances, dependent on longest recirculating delays
- NOT primarily from early reflections (time domain)
- Echo density target for "smooth" perception: ~4000 impulses/second (broadband); ~800 for 1.5kHz lowpass
- "Velvet noise" concept: sparse but spectrally white reflection pattern at ~4000/sec that sounds maximally dense

---

## Part 6 — Reverse-Engineering Evidence and Methodology

### 6.1 What Has Already Been Done
**Source:** Multiple posts; SubC p.23-27 posts #702-807; SubC p.33-36 posts #974, #1042
**Files:** Various

| Unit | Who | Method | Status |
|---|---|---|---|
| 224 Concert Hall | Jeff Stanton (Ursa Major) | Logic analyzer on 224 hardware | Done; used in AKG ADR-68K |
| 224 Concert Hall | Dattorro/Griesinger | Published (with Griesinger's permission) | Published, confirmed by acreil |
| PCM70 | dale116dot7 | Disassembled firmware ROM | Done; cannot share |
| 224 | dale116dot7 | Disassembled firmware ROM | Done; cannot share |
| PCM91 | dale116dot7 | Disassembled firmware ROM | Done; cannot share |
| 480L | dale116dot7 | Disassembled firmware ROM | Done; cannot share |
| Quantec QRS | acreil | Impulse response analysis | Published in thread (SubC #581-592) |
| Midiverb | acreil | Firmware disassembly | Published in thread (simulator written) |
| Sony DRE-2000 | acreil, zmix | IR analysis + ROM dumps | Substantial analysis published |

**dale116dot7 has disassembled the 224 firmware but cannot share it.** He knows the topology from reading the actual microcode.

### 6.2 Impulse Response Analysis Method
**Source:** SubC posts #1020, #1059, #1125-1137 (acreil)
**File:** `reverb-subculture-pages-33-36.md` p.33-36

acreil's methodology (reverse-engineered Quantec QRS and several others):
1. Record impulse response (swept sine or impulse)
2. Open in Audacity; Matlab scripts for analysis
3. Autocorrelation to identify comb filter delay times
4. Extract allpasses by processing IR in reverse through estimated allpasses
5. Identify output tap polarity (positive/negative) from initial sign of peaks
6. Track modulation using sustained sine tones
7. Loop filtering identified from spectral envelope of tail

**Confirmed for 224:** The Dattorro diagram of Concert Hall matches real 224 IRs "up to the three recursive allpass filters part" (acreil S#1042).

### 6.3 acreil's Quantec QRS Reverse-Engineering (Published in Thread)
**Source:** SubC posts #581-592
**File:** `reverb-subculture-pages-18-22.md` p.18

For reference on RE methodology quality:
- 16 independent resonators (comb + embedded APF per resonator)
- 2 delays per resonator; fills 64k×26-bit memory at max room size
- 20 kHz sample rate; 5 MIPS (~256 instructions/sample = ~16 per resonator)
- Output polarity: 50% in-phase, 50% out-of-phase for any 2 outputs
- FDN equations derived: Input[in→delA, in→delB] = [1-D², D], etc.

This level of precision is achievable from IR analysis alone.

---

## Part 7 — Peripheral Threads of Interest

### 7.1 Barry Blesser's "Notch-Pass" Patent
**Source:** Bestiary post #12 (seancostello); SubC posts #877-899 (Casey, zmix, acreil)
**Files:** `lexicon-bestiary-combined.md` p.1; `reverb-subculture-pages-28-32.md` p.28-30

Blesser's 2006 patent addresses allpass metallic ringing by pairing poles with zeros at different frequencies, creating a "notch-pass" that flattens the group delay variation. Casey tested it: eliminates metallic tail but colors the reverb onset. Patent reference: US7062337 (different patent from the notch-pass one — this is the quadrature coefficient modulation one; notch-pass is referenced but may be a separate filing). Considered for use in Lexicon low-cost product.

### 7.2 FDN Delay Length Tuning
**Source:** SubC posts #817-823 (Casey, sirhans)
**File:** `reverb-subculture-pages-28-32.md` p.28

Casey's rules for tuning FDN delay lengths:
- Use prime numbers to avoid repeated modal peaks
- Keep shortest-to-longest ratio under 2:1
- Target 60-120ms delay sets for sufficient echo density
- Post-network: allpass pairs in series with ~2.85 ratio (empirically determined; possibly "1 octave + tritone")
- Hadamard matrices for feedback (distributes energy evenly across delays)

Automated search (sirhans): MATLAB script to find delay combinations minimizing coincident resonances.

### 7.3 The Midiverb Architecture (for comparison)
**Source:** SubC posts #906-930, #1037, #1125 (acreil, seancostello)
**File:** `reverb-subculture-pages-28-32.md`, `reverb-subculture-pages-33-36.md`

The Alesis Midiverb is an extreme case of the same constrained-DSP philosophy as the 224:
- 128-instruction instruction set; 4 core instructions (read-add, read-store, write, write-negate)
- Uses address *increments* rather than base+offset circular buffer addressing
- ~70 instructions typical for complex presets; preset 49 = 21 allpasses
- Evolution (Keith Barr): 4 parallel loops (Quadraverb) → embedded allpasses in combs → single large loop
- Keith Barr (email to seancostello): *"Everything I write today is single loop, with modifications as to input signal injection and output tap selection."*

### 7.4 EMT-250 Algorithm
**Source:** SubC posts #225, #255 (seancostello); SubC post #243 (zmix describing UA video)
**Files:** `reverb-subculture-pages-08-12.md`, `reverb-subculture-pages-01-07.md`

EMT-250 algorithm (from UA promotional video, Blesser Associates June 1977 drawing):
- 3 parallel feedback combs with 3 taps per comb each
- Taps summed into a second section of 3-4 short delay lines
- Linear interpolation implemented as: `out = frac*(read[tap]-read[tap+1]) + read[tap+1]` (2 multiplies or 1 multiply + 2 additions)
- Output polarity: "50% in-phase, 50% out-of-phase" (Quantec is similar)

Casey's tutorial recreates this exactly (posts #14-45 p.1-2). The 224's Constant Density Plates are Griesinger's approximation of this topology.

---

## Part 8 — Post Index (Critical References)

### 224XL Hardware / Architecture
| Source | Post | Author | Content |
|---|---|---|---|
| Bestiary | #183 | dale116dot7 | 100-step program; PC cleared by I/O bit 3 write; 128 steps possible |
| Bestiary | #242 | Larry the O | Eyewitness: "100 lines of microcode"; Griesinger origin story |
| Bestiary | #247 | Larry the O | Schroeder backstory; 224X random chorus = same modulation as reverb |
| Bestiary | #298 | dale116dot7 | Full ARU breakdown: bit widths, multipliers, ticks/instr, program steps |
| Bestiary | #300 | Casey | 480L 8-bit µP rewrites ARU microcode for modulation; Lexichip-3 = 256 steps |
| SubC | #378 | dale116dot7 | 224: 6-bit × 5-bit multiplier; 250ns RAM; WCS NOP window constraint |
| SubC | #556 | seancostello | Sample rates: 224/224X = 29.761 kHz; 224XL = 34.125 kHz |
| SubC | #807 | dale116dot7 | Has disassembled 224/PCM70/PCM91/480L code (cannot share) |

### Concert Hall Algorithm
| Source | Post | Author | Content |
|---|---|---|---|
| Bestiary | #38 | NS | Depth param in PCM96 = chorus amount; Shape/Spread ≠ Depth |
| SubC | #151 | Casey | David still has 224 code base |
| SubC | #156 | zmix | PCM70 modulation: 2.3Hz triangle + 0.5Hz random |
| SubC | #284-292 | zmix/Casey | Concert Hall modulation comparison: 224 vs PCM70 vs PCM96 |
| SubC | #380 | Warp69 | Three modulation type taxonomy |
| SubC | #554 | acreil | Long nested APF → signal becomes noise-like; no metallic ringing |
| SubC | #556 | seancostello | Two Griesinger algorithms: old (29.761 kHz) and new (34.125 kHz) |
| SubC | #557 | seancostello | "Dark Hall = more interpolated delay lines; Bright Hall = damping 1-pole different location" |
| SubC | #1027-1029 | zmix, Casey | 224 uses one LFO; injection in few places; triangle possible |
| SubC | #1028 | Casey | **8080 "randomly missed some delay updates"** — mechanism of "random" modulation |
| SubC | #1042 | acreil | **Dattorro diagram confirmed vs real 224 IRs** |
| Bestiary | #394 | zmix | 224 stereo topology: inputs 180° apart, outputs 90° rotated |

### Algorithm Genealogy / History
| Source | Post | Author | Content |
|---|---|---|---|
| Bestiary | #125 | NS | Lexicon designer credits: Blesser, Cunningham, Hall, MacArthur, Muller, Hegg |
| Bestiary | #175 | NS | Constant Density Plate predates NS; 224 "predates even me" |
| SubC | #151 | Casey | 224 code base still with David; was considering new algorithms |
| SubC | #702 | Casey | Jeff Stanton RE'd 224; Blesser adapted for ADR-68K |
| SubC | #705 | NS | Concert Hall lineage through Blesser/ADR-68K |
| SubC | #805 | zmix | Griesinger 1979: "high diffusion not always desirable for first 200ms" |

### Design Theory
| Source | Post | Author | Content |
|---|---|---|---|
| SubC | #14-45 | Casey | Complete EMT-250-style reverb tutorial (3 loops → output taps → allpasses → modulation) |
| SubC | #104 | Casey | Tap spacing >50ms for decorrelation; modulation rate 10-50 Hz |
| SubC | #165 | seancostello | Allpasses in tank build density over time; allpasses before tank = initial density only |
| SubC | #437 | seancostello | Central Limit Theorem: series allpasses → Gaussian impulse (fade-in effect) |
| SubC | #817-823 | Casey | FDN delay tuning: prime numbers, ratio <2:1, 60-120ms sets, 2.85 allpass ratio |

---

## Part 9 — What Remains Unknown

1. **224XL sample rate vs. project measurement:** seancostello says 34.125 kHz; project session shows 26.667 kHz. Service manual clock specs need to reconcile this.

2. **Exact 224 LFO waveform:** Casey says one LFO "randomly missed updates." Is the base waveform triangle, sine, or something else? zmix says PCM70 = 2.3Hz triangle + 0.5Hz random; the 224 mechanism may differ.

3. **OFST3 / RESET-decode:** The session-0021 crux. dale's service manual reading says PC cleared by I/O write with bit 3 set. This should map to tcWR·OFST3/ in the netlist — but the exact schematic verification of tc_U14 pin1/tc_U33 pin12 needs physical hardware or schematic confirmation.

4. **Steps 100-127:** What, if anything, happens in these 28 unused steps? Are they NOP cycles for 8080 housekeeping? The 8080 needs time between samples to update WCS coefficients; these NOP steps are where it gets that time.

5. **dale's disassembled code:** He has it, can't share it. But the topology can be confirmed from the Dattorro publication + acreil's IR confirmation.

6. **The 224 source code:** "lost many many years ago" per NS. Griesinger may have a copy personally (Casey's 2011 hint). Not obtainable through normal channels.
