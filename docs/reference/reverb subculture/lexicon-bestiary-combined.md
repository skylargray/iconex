# Lexicon Reverbs: A Brief Bestiary — COMBINED (Pages 1–14)

**Source thread:** https://gearspace.com/board/high-end/362930-lexicon-reverbs-brief-bestiary.html
**Forum:** High End @ Gearspace · 14 pages · 407 posts
**Compiled from:** lexicon-bestiary-pages-01-05.md / 06-10.md / 11-14.md

---

## WHO'S WHO — Reader's Guide

Read this before diving into the thread. It tells you whose posts to trust, what each person knows, and what to watch for.

---

### ★★★★★ Nobody Special = Michael Carnes
**Lexicon DSP Engineer → Exponential Audio (founder) → iZotope**

**Identity confirmed in thread:** Post #335 quotes him as "Michael Carnes." Posts #346 and #355 address him as "Michael." Post #355 (April 4, 2019, exactly 10 years after his original post) says *"congrats on the sale of exponential to izotope... you would have left Lexicon, created your own plug in company."* Post #337: *"I haven't been at Lexicon for more than two years."* He confirms by responding in character, referencing "Exponential's" verbs.

**What he knows (primary source):**
- Literally wrote the PCM96 firmware AND the plugin versions: *"I wrote the code for both."*
- Designed the Hall, Room, Vintage Plate (plugin-only), LARES port to 960L and DNA/Wenger chip.
- One of "4–5 people in the world who ever programmed a Lexichip 3."
- Knew David Griesinger and Barry Blesser personally; consulted both on algorithm history.
- On the 224: *"The actual source code was lost many many years ago."* He worked from Blesser's extracted diagrams + Griesinger conversations — not original code.
- PCM96 uses SDRAM (8MB) plus internal SHARC memory — corrected Casey's public mischaracterization.
- Will self-correct when wrong (conceded Depth/Shape&Spread question to Sean Costello).

**Trust level:**
- PCM96, 960L, 480L, 300, 90/91 internals: ★★★★★ (he wrote the code)
- 224-era algorithm genealogy: ★★★★☆ (secondhand but high-quality)
- 224 internal mechanics: ★★★☆☆ (manual + Griesinger, not source code)

**Watch for:** Algorithm bestiary posts (p.1), preferred algorithms by genre (p.3), SDRAM debate with Casey (p.3), Pantheon/Lexicon plugin genealogy, Random Ambience (p.10 post #279 — confirms he had left Lexicon).

---

### ★★★★★ Casey
**Co-designer, Bricasti M7 (formerly Lexicon-adjacent)**

User info explicitly says "Bricasti." NS calls him "a competitor." He refers to the M7 in third person. He had private conversations with Griesinger (~2004). Deep insider knowledge of the 480L, its algorithms, and early Lexicon history — almost certainly had direct access at some point.

**What he knows:**
- Walked the Reverb Subculture thread through building an EMT-250-type reverb from scratch, step by step.
- Deep 480L internals: the HD/Surround cart algorithm uses ALL 4 cores (320 instructions); standard algs use 2 cores (80 steps × 2); *"The 480 also uses an 8 bit microprocessor which re-writes the 80 step microcode in the ARUs to provide the dynamic reverb modulation."* (Post #300 — gold for your project.)
- Lexichip-3: 256 steps. 960L: 4 Lexichip-3s plus two 8-bit microprocessors for dynamic microcode.
- Confirmed: SST-282 history, Constant Density Plate as Griesinger's EMT-250 response.
- On 224 modulation: *"David's 224 randomization method was really pretty cool. Just different enough to make it magic!"*
- Favorite Lexicon algorithm: David's last 480 reverb (Surround/HD), which used the entire 480.
- PCM91 Random Hall ≠ 480L Random Hall in same sense; 300/480 Random Hall are very close.
- Surround/HD cart = "dense" algorithm, NOT based on Random Hall (corrects Sean's taxonomy, p.4 post #119).

**Caution:** Made one wrong public assumption about PCM96 memory architecture; NS corrected him; he apologized gracefully. His knowledge of PCM96 internals is external inference, not first-hand.

**Watch for:** ARU/microprocessor architecture post (#300), algorithm taxonomy corrections (#119), favorite algorithm (#106), Griesinger 224 modulation comments (#291/#292).

---

### ★★★★☆ dale116dot7
**DIY DSP Engineer and Vintage Lexicon Repair Tech**

Has personally read and worked from the 224XL, PCM70, LXP1, DN780, and PCM91 service manuals. Has repaired PCM60s, PCM70s, PCM91s, LXP1s. Has reverse-engineered PCM70 and LXP1 firmware. Builds his own reverb hardware (AL3201-based then DSP56366 + 512k SRAM).

**What he knows (most relevant to 224XL project):**

**Post #183 (p.7) — THE CRUX POST:**
> *"The 224XL service manual indicates that the program is 100 steps. However, the microcode actually could do 128 steps — the program counter is cleared by writing an address with bit 3 set to the I/O space. The 224 (non-XL) version shows the same sort of thing — the WCS resets the PC. Though many of the Lexicons have a 128-step program counter, not all of them actually use all 128 steps."*

This directly from the service manual. The PC is 7-bit (128 max), programs use 100, and the reset is triggered by a WCS write to I/O with bit 3 set — not a dedicated hardware reset line. This is the primary external confirmation of the session-0021 128-step hypothesis.

**Post #298 (p.10) — Full architectural breakdown:**
- 224/224X: 16-bit ARU, 6-bit multiply, 8 clock ticks/instruction, 100-instruction program. RAM: 224=16k, 224X=32k or 64k. Based on 74S283 fast adders.
- 200: 74F181 ALU, 3–4 bit multiplier, 128 microinstructions @ 3 clock ticks.
- PCM70: Same ARU design as 200 in ASIC, 18-bit version, same program length, higher sample rate, 16-bit A/D D/A.
- 480L: 4-core, 4-bit multiply, 80 instructions/core × 4 = 320/sample.
- Lexichip-1/-2: Faster 200-type ARU, expanded to 20-bit, 128 program steps.
- 300L: Two Lexichips, 16-bit A/D D/A. PCM91: Two Lexichips, 20-bit A/D D/A.
- PCM80: One Lexichip + DSP56002 for effects.
- (Casey corrects: no overhead moving samples between 480L cores; all standard algs use 2 cores, HD uses all 4.)

**Watch for:** Posts #183, #298, and the chorus/allpass implementation discussions (p.1–2 of Reverb Subculture thread, not this bestiary).

---

### ★★★★☆ seancostello (Sean Costello)
**Founder, ValhallaDSP**

Deep algorithmic reverb theory. Familiar with Schroeder, Jot, Gerzon, Gardner, Dattorro, Blesser (book), SST-282, 1984 Puckette/Stautner CMJ paper, Griesinger's psychoacoustics papers. Implemented reverbs commercially since ~2000. Forensic listener — identifies artifacts, modal density, interpolation noise by ear.

**What he knows:**
- Best systematic taxonomy of Lexicon algorithms by unit (post #118, p.4) — cross-checked and corrected by NS and Casey.
- Systematic modulation breakdown by unit (post #172, p.6): all 224XL algorithms used time-varying chorus; PCM60 none; PCM70 chorus on Concert Hall only; 480L Spin/Wander on Random Hall/Ambience/Surround; etc.
- Identified that 224 algorithms have a different sound from 480L-era, likely related to 6-bit multiplier constraints.
- Reverse-analyzed the EMT250 algorithm block diagram from the UA video in real time.

**Trust level:** Very high on algorithm theory and comparative listening. Moderate on Lexicon internals (manual-derived). Honest about his guesses.

**Watch for:** Algorithm taxonomy (#118 p.4), modulation breakdown (#172 p.6), blind listening test analysis, 224XL Depth parameter question (p.2 post #36, #38).

---

### ★★★★☆ Larry the O
**Arrived Lexicon 1979; Lead bench tech on 224X**

One-time poster but primary source on pre-NS Lexicon history. Posts #242 and #247 (pp.8–9).

**What he knows (first-hand):**
- Arrived Lexicon 1979, week of PrimeTime and 224 release parties. Lead bench tech through 224X introduction.
- *"The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once. Man, he worked every line of that stuff."* — Direct eyewitness confirmation.
- Detailed Griesinger origin story: Harvard professor, 10 years of AES back-issues, missed Schroeder (15 years earlier), met Blesser who pointed him to Schroeder papers, described them as *"nasty little rooms"*, then developed independently, approached Lexicon's Dr. Francis Lee at a Boston AES chapter meeting.
- Gary Hall wrote 224X effects microcode (Resonant Chords, Multi-band Delays, etc.) AND the PCM41/42 microcode (using a microcontroller Gary developed at home on his own time). The PCM70 LXP series etc. heavily influenced by Gary Hall.
- The 224X Chorus program used the SAME random modulation as the reverberators — not LFO. This is the *mechanism* behind the Lexicon sound. Made it as far as PCM70 v3; gone in v4. ("I kept one of my PCM70s at v3.")
- Convened a 1986 Mix magazine roundtable: Griesinger, Agnello, Moorer, Neatrour (5-part series).

**Trust level:** ★★★★★ for early Lexicon history (1979–early 1980s, pre-NS). Memory caveats noted by author himself. Confirmed by NS: *"Gary went on to do a lot of good work at Sonic Solutions as well."*

**Watch for:** Posts #242, #247 (p.8–9).

---

### ★★★☆☆ zmix
**Independent — Serious Vintage Reverb Collector and Critical Listener**

Has owned: 1979-era original 224 (for ~10 years), PCM70 (×2, current), PCM96, EMT 250 (1977), Audio Damage Eos. Spent 2 years helping UA get their 224 emulation correct. Knows Barry Blesser personally. Deep preference for pre-480L algorithms.

**What he knows:**
- Ran blind listening tests with 24-bit WAV files: EMT250, 224, PCM96, Eos (revealed in reverse price order).
- Detailed modulation analysis of 224 vs PCM70 vs PCM96 Concert Hall, with spectrograms and audio examples.
- Key 224 structural observation (post #394): *"The stereo inputs on the various 224s are really interesting as the reverb is essentially a large loop with inputs 180° on either side and the outputs 90° rotated from them."* — The 224's stereo structure is a topological feature that convolution cannot replicate.
- Estimate: *"the entire Concert Hall algo is only 120 instructions."* (Consistent with 100-step WCS + overhead.)
- Made custom MIDI controllers for PCM-70 (all 29 parameters accessible via DAW, Mackie C4).
- On the 224 modulation: *"I have tweaked and tweaked modulation placements, waveforms, rates and intensities in order to get the sort of evenness that the 224 Concert Hall exhibits. They NAILED it."*
- PCM-70 OS versions: v1.2 = bug fixes, v2 = more features, v3 = Inverse Room + MIDI sysex.
- Corrected gear-use myths: Jeff Buckley = SPX-90 + 224XL (Andy Wallace, not Quadraverb); Budd/Eno "First Light" = EMT 250 + multiple passes.

**Trust level:** High for perceptual/listening claims with hardware in hand. Moderate for internal technical claims. His audio files are primary-source data.

**Watch for:** Blind test (p.8), modulation analysis (pp.9–10), post #394 (p.14) on 224 stereo topology, post #375 (p.13) on 224 FDN structure, post #404 (p.14) on 224 vs PCM-70 difference.

---

### ★★★☆☆ Warp69
**Independent — Serious Lexicon Collector**

Owns: 480L (classic card + surround/HD card), 224XL, PCM91. Rigorous technical questioner; catches errors in NS and Sean's posts.

**What he knows:**
- 480L/480L Classic Card/Surround/HD parameter details from hands-on use.
- PCM91: Constant density achievable only in Concert Hall algo with Definition at max; Diffusion controls density.
- The Surround and HD algorithms are the same — HD just mixes 4 surround outputs to stereo internally.
- Surround/HD has an early reflection engine; only one other algorithm (Ambience) has one.
- 480L Wander maxes at 10ms at 39m room size.
- Correctly identified that Random Ambience's 3-part structure (DRY + ER + REV) is not shown correctly in the 300L manual.

**Watch for:** Parameter-level corrections throughout, post #122 (algorithm taxonomy), posts #269–275 (Random Ambience deep dive with living sounds).

---

### Notable One-Time Contributors

**locust_tree (post #375, p.13):** Owned a ca.1979 224 for over a decade. Best user-perspective description of the original 224's FDN structure: adjustable diffusion within the reverb FDN (not just input diffusion), 3 sets of output taps mixed by "depth" parameter, 20.6 kHz sample rate on original 224, sample rate increased on 224X/XL. Era-1 random modulation in *"the FDN allpass network."*

**henge (post #283, p.10):** Identifies both NS and Sean by their real names in the same post, cross-confirming identity. Sean responds confirming they met at an AES convention. NS responds confirming.

---

## Notes for 224XL Hardware Research

### Dale's Post #183 + Post #298: The Hardware Bible
Two posts by dale116dot7 constitute the most hardware-specific external evidence for the 224XL reconstruction:

- **Program is 100 steps; PC can do 128** (from service manual). The PC is cleared by *"writing an address with bit 3 set to the I/O space"* — i.e. the RESET is a firmware-initiated WCS write, not a dedicated external hardware line. This is the primary external confirmation of the session-0021 128-step / natural-wrap hypothesis.
- **224 ARU: 16-bit, 6-bit multiply, 8 ticks/instruction, 100 steps, 74S283 fast adders.**
- **Multiply precision is 6-bit** — *"the 224 uses a 6-bit multiplier which would be on the ragged edge of being able to pull off a chorus in two lines"* (on this, he and Sean Costello agree).

### Larry's Post #242: Eyewitness Confirmation
*"The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once."* Primary source, present at Lexicon in 1979.

### Casey's Post #300: Dynamic Microcode Mechanism
*"The 480 also uses an 8 bit microprocessor which re-writes the 80 step microcode in the ARUs to provide the dynamic reverb modulation."* This is how modulation works on the 480L — the host CPU rewrites WCS microcode steps every sample period. The 224XL would use its 8080 analogously. This is architecturally consistent with your T&C microword rewrite model.

### NS on the 224 Source Code
*"The actual source code was lost many many years ago."* Authoritative statement from the principal PCM96 engineer. Validates the reverse-engineering approach entirely.

### zmix's 224 Stereo Topology (Post #394)
*"The reverb is essentially a large loop with inputs 180° on either side and the outputs 90° rotated from them, so as a sound enters the left input it comes out the left after a certain period of time, and then much later comes out the right channel."* This is the actual 224 Concert Hall topology as described by someone who owned one for a decade — stereo inputs are not symmetric but are offset around the loop.

---

---

# THREAD CONTENT: Pages 1–14

---

## Page 1

---

### Post #1 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880302&postcount=1>

**About Lexicon reverbs**


I often see lots of comments about the naturalness or effect-y-ness of Lexicon reverbs.  I think it's worth taking a few minutes to point out the differences in reverbs and how you can use them for either natural or effect-y applications.  After all, there are more than 30 years of history in Lexicon reverbs and they're not all the same.  As we go through them, you'll see me mention two parameters named '*Spin*' and '*Wander*'.  These are often the source of great confusion, and it doesn't help that they're a little different in each of the 'verbs.  In general, their intent is to provide a smoother frequency response for complex material.  In some of the algorithms, they're not really even noticeable as modulation effects. They can often be turned off with no harm, depending on material.


You'll find variants of these algorithms in lots of our verbs, but my descriptions apply most closely to the PCM96.

Concert Hall

This is the granddaddy of Lexicon reverbs and it dates back to the 224.  It was the definitive 80's reverberator.  It is prone to coloration and is best used with very large room sizes.  This is the only algorithm without Spin and Wander.  Instead, it has a pair of chorus controls.  It's a nifty effect for the right material, but you can hear strong pitch effects. While I like the sound, I can't ever imagine using it for any natural sort of mix.

Plate

There've been a few minor tweaks on this, but the PCM96 has a version that close to the 480L, although much cleaner.  In this algorithm, Spin and Wander can be used to smooth the frequency response. They're not really intended for chorus-type effects.  Even with large amounts, pitch should be quite stable.  If you find that you still hear modulation effects you don't want, simple turn Spin down or off.  It will sound fine.

Chamber

Extremely high reflection density and rapid onset--just like you'd expect from a live chamber.  Once again,  spin and wander are present and available to smooth out problem material.  I generally like Chamber with spin turned all the way off.  Alternatively, moderate Spin with a low Wander value ( under 3 milliseconds) will be effective at smoothing frequency response without creating noticeable modulation.

Random Hall

This algorithm dates back the the 480L and you'll find versions in every one of our high-end reverbs after that.  This algorithm is the basis of a lot of good mixes, and is more responsible for the term "Lexicon Sound" than any other reverb.  But it has quite noticeable modulation, especially with smaller room sizes.  I wouldn't suggest messing too much with Spin and Wander for this algorithm.  It is what it is, and that's nice.

Hall

This algorithm was introduced with the PCM96.  It has many of the characteristics of the 480L, without the strong sense of modulation.  If you have material that's strongly colored, then high values for Spin and Wander will help smooth out the material with very little sense of modulation.  At the same time,  for many applications you can turn Spin down completely and have a stable, natural tail.

Room

This one is also new with the PCM96 (there are some old boxes with an algorithm called Room, but those were much closer to a Hall).  While the primary focus of this is post-production, careful programming can give some very nice hall sounds as well.  The early reflections are quite stable and and possible modulation occurs at low levels in the tail where it's helpful in reducing coloration.  If I ever have time, there are a great many presets I'd like to do with this one.  It can be made to sound quite clean and natural.

One other thing

There are a couple of other parameters call Shape and Spread.  They're used to delay injection of energy into the reverb--giving something of an envelope to the early stages of verb.  In some cases, they may appear to cause some late motion in the tail. That's not really what's happening, but it can sound that way.  Reducing either or both of those parameters may be helpful.

Finally

So let me encourage you to spend some time playing with presets based on our different algorithms.  Presets often represent the mindset of the person doing the presets, and a given series of presets may explore only one facet of the algorithm.  You might find that a bit of editing time will open up new possibilities.  We used to throw around a phrase at Lex "We give you the rope...".  I think it still applies.


It appears that many people identify with the Lexicon sound that was available in the decade they entered the business.  With the PCM96, we've tried to incorporate the sounds from all four of those decades.

---

### Post #2 -- Page 1
**User:** drBill
**Info:** Joined: Jul 2006Posts: 22,967My Studio🎧 15 years | Posts: 22,967My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880525&postcount=2>

Thanks NS.  Most helpful.  


What's the closest starting place to on the 96 to get the great Hall sound on the 480?  Also, how about the small wood room (is that what it's called...??) on the 480?


Great explanations.  LOVE IT!!!!


bp

---

### Post #3 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880614&postcount=3>

Quote: > Originally Posted bydrBill➡️Thanks NS.  Most helpful.What's the closest starting place to on the 96 to get the great Hall sound on the 480?  Also, how about the small wood room (is that what it's called...??) on the 480?Great explanations.  LOVE IT!!!!bpIf you're working from the front panel interface, look under any of the halls folders for presets with the RHall name.  Those are based on the RandomHall algorithm.  If you're using the plugin interface, then just load Random Hall.


I'm afraid I don't have a 480 close by, so I can't tell you about the wood room.  But a good starting place for small spaces is the Rooms folder (front panel) or the Room algorithm (plugin).

---

### Post #4 -- Page 1
**User:** Jonathan Starr
**Info:** Joined: Apr 2005Posts: 1,045🎧 20 years | Posts: 1,045
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880893&postcount=4>

This is really helpful. 


Thanks. & Encore Please (Hana Hou !)

---

### Post #5 -- Page 1
**User:** yeloocproducer
**Info:** Joined: Dec 2004Posts: 1,790My Studio2 Reviews written🎧 20 years | Posts: 1,790My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3892662&postcount=5>

Any other hints on getting the PCM96 to get to sound specifically like some notable presets on the 200, 224, 300, or 480?  Or presets in the PCM96 that were specifically designed to replace some "retro" favorites?  The Rhall note for 480 types is helpful... thanks.


PCM70 "tiled room"?  Anything close?  480 silica beads?


Just got the reverb today and looking forward to firing it up.

---

### Post #6 -- Page 1
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3892988&postcount=6>

Excellent post, NS!!! Thanks.

---

### Post #7 -- Page 1
**User:** Terry McInturff
**Info:** Joined: Mar 2007Posts: 751🎧 15 years | Posts: 751
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3893011&postcount=7>

Yes, a million kudos to you for this information.


Back to the ancient (and zero current profitability) PCM 70...what programs are like Tiled Room, Bright Plate...and any other signature PCM 70 stuff?


Masny thanks, you are very generous!

---

### Post #8 -- Page 1
**User:** Dopamine
**Info:** Joined: Nov 2002Posts: 2,002🎧 20 years | Posts: 2,002
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3894456&postcount=8>

Seems like Lex should include presets on the 96 that are similar to some of the classics:  obviously the PCM70 Tiled Room and 480 Hall.

---

### Post #9 -- Page 1
**User:** synthetic
**Info:** Joined: Aug 2005Posts: 515🎧 20 years | Posts: 515
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3896051&postcount=9>

They've been busy on software and other products, it seems. I wouldn't be surprised if we see some "Classic" programs released down the road. After all it's a simple enough software rev.

---

### Post #10 -- Page 1
**User:** audiomichael
**Info:** Joined: Mar 2005Posts: 2,303🎧 20 years | Posts: 2,303
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3897360&postcount=10>

I kinda like the genericness of the titles, but it would be cool to see a "best of" preset category.  I'd throw the 91's "Deep Blue" into that mix.

---

### Post #11 -- Page 1
**User:** Brad_Wood
**Info:** Joined: Aug 2006Posts: 106My Recordings/Credits🎧 15 years | Posts: 106My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3897388&postcount=11>

Quote: > Originally Posted bydrBill➡️how about the small wood room (is that what it's called...??) on the 480?bpI love love love the small wood room from the 480L & have found the Altiverb versions to be really close to the real thing. 


Best- Brad

---

### Post #12 -- Page 1
**User:** Jack Weaver
**Info:** Joined: Jan 2005Posts: 360🎧 20 years | Posts: 360
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3898454&postcount=12>

Thanks NS -


It helps place many things in perspective. Very good of you to give us this info. 


I can only imagine that if there were a software release resembling "Best of..."

that word would get around fast in the purchasing circles.

---

### Post #13 -- Page 1
**User:** mattssons
**Info:** Joined: Feb 2004Posts: 301My Recordings/CreditsMy Studio🎧 20 years | Posts: 301My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3898565&postcount=13>

Thanks for a great post.


Do you know anything about Lexicon 200? I have one, like a lot especially considering it´s age! /Toby

---

### Post #14 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3899195&postcount=14>

Many good remarks here about favorite presets and such.  I'd certainly be interested in getting as close as possible to some old classics.  I'd also like to gather up some user-generated presets.  We don't have a good way to organize such an effort just yet, but I'd think something with MIDI bulk dump might be one way to get there.


I do hope that some of you have been rolling up your sleeves and getting into programming the box (or even some of your older Lexes).  One thing I've learned is that different people--with different applications, different ears, and different points of view--can come up with some unique and useful sounds.  I know that we've just scratched the surface of what the box can do, and I've love to offer a folder of user favorites.


Toby, hang onto that 200.  It's like your favorite old aunt.  She's crotchety and a little limited for sure, but even if you found a replacement, it would never be the same.


I've been a bit busy of late, but I hope I can get back in here before too long and cover a few more areas of interest.

---

### Post #15 -- Page 1
**User:** audio ergo sum
**Info:** Joined: Oct 2008Posts: 3,644🎧 15 years | Posts: 3,644
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3899714&postcount=15>

Hi NS, is the 96 surround shipping yet in quantities?

---

### Post #16 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3900285&postcount=16>

Quote: > Originally Posted byaudio ergo sum➡️Hi NS, is the 96 surround shipping yet in quantities?It started going out a few weeks ago.  If your dealer doesn't have any yet, it shouldn't be too long.

---

### Post #17 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3926870&postcount=17>

Hi NS (1st time poster here):


How much consistency is there between algorithms of the same name over Lexicon history? For example, is the Rich Chamber of the 224XL similar to the PCM70 room/chamber, and how much do things change with the 480L and later reverbs?


Also, is time variation generally found on the high end Lexicons only, or does it make its way into the lower priced units as well? I remember using the 224XL, and the Mode Optimization seemed like some sort of chorusing, while I presume the 480L and later use some different type of time variation.


Thanks,


Sean Costello

---

### Post #18 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927153&postcount=18>

Quote: > Originally Posted byseancostello➡️Hi NS (1st time poster here):How much consistency is there between algorithms of the same name over Lexicon history? For example, is the Rich Chamber of the 224XL similar to the PCM70 room/chamber, and how much do things change with the 480L and later reverbs?Also, is time variation generally found on the high end Lexicons only, or does it make its way into the lower priced units as well? I remember using the 224XL, and the Mode Optimization seemed like some sort of chorusing, while I presume the 480L and later use some different type of time variation.Thanks,Sean CostelloHi Sean,

Some things change, but many things remain consistent (wishy-washy answer but it's true).  Back when David Griesinger was doing products like the 224, there were zillions of things he wanted to do that the hardware wouldn't allow.  As hardware became more powerful, fewer corners needed to be cut.  On top of that, time, thought and experimentation led to better ways to make a reverb algorithm.  So there's been a continual process of improvement.  Lots of times, customers may not see it that way:  if you cut your first hit record with a 224, the last thing you want is to see it change.  But on our side of the fence, we're always looking for some way to make things sound better.  But still there are some things that make a plate a plate, and we try to respect and extend that.


In terms of specific products, the 70 was a simplified version of the 224 and the algorithms sound pretty similar.  The 480 extended that with a better S/N ratio and more algorithms.  The 960 was a further extension.  It was a little lighter and more transparent: some people loved it and some people hated it.  The PCM96 incorporates qualities of both, and can be leaned in either direction.  It was also our first floating-point processor, with considerably better performance.


The chorusing sound of the 224 family was a characteristic of the ConcertHall algorithm.  It's the only algorithm that works that way.  You'll also find variants of that sound in the PCM91 and PCM96.  As I indicated in an earlier post, it sure isn't realistic but it might just be the thing you need.  Other algorithms approach time variance (we call it randomization) in other ways and for other purposes.  Ideally, it's not something you should hear as chorusing.  It's intended to break up room modes and improve frequency response.


Randomization has been a feature of most of our products in recent years.  Ten years ago it came down as far as the PCM90/91.  A few years later it came down as far as the MPX100.  Now it's in everything.  It's obviously a little slicker in the high-end products, but even in a product like the MX-200 it's more complex that the 480.  I kinda like Moore's law.

---

### Post #19 -- Page 1
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927250&postcount=19>

Quote: > Originally Posted byseancostello➡️I remember using the 224XL, and the Mode Optimization seemed like some sort of chorusing, while I presume the 480L and later use some different type of time variation.The Decay Optimization in some of the 480L algorithms have nothing to do with chorusing. And the same is true for the 224XL.


Did you mean Mode Enhancement?

---

### Post #20 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927333&postcount=20>

Quote: > Originally Posted byWarp69➡️The Decay Optimization in some of the 480L algorithms have nothing to do with chorusing. And the same is true for the 224XL.Did you mean Mode Enhancement?Yep. I just mixed the two terms up. Decay Optimization seems like something used to reduce certain artifacts for impulsive sounds.


Sean

---

### Post #21 -- Page 1
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927554&postcount=21>

Quote: > Originally Posted byWarp69➡️The Decay Optimization in some of the 480L algorithms have nothing to do with chorusing.This is becoming a great historic record, thanks for starting it NS.


Early on decay optimization was simply turning down the level of reverb when no input signal was present. Over time it transformed into a switch which coupled/decoupled the size parameter from the reverb time. (If I recall correctly!)


More importantly; NS I don't believe that you mentioned Davids 480 surround algorithm, which I believe he is quite proud of. I will add that it rocks, even in stereo, and makes finding a surround option cart for the 480 a requirement for 480 fans.


-Casey

---

### Post #22 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927722&postcount=22>

Quote: > Originally Posted byCasey➡️This is becoming a great historic record, thanks for starting it NS.Early on decay optimization was simply turning down the level of reverb when no input signal was present. Over time it transformed into a switch which coupled/decoupled the size parameter from the reverb time. (If I recall correctly!)More importantly; NS I don't believe that you mentioned Davids 480 surround algorithm, which I believe he is quite proud of. I will add that it rocks, even in stereo, and makes finding a surround option cart for the 480 a requirement for 480 fans.-CaseyAlmost.  Decay optimization had to do with managing allpasses (could be my memory giving out.  Got a virus of some sort today).  The decoupling parameter was called "Link".  It 'disappeared' and hasn't been missed.  David's nice surround algorithm was based on the Random Hall and was 2-in/4-out.  I don't think we have any of the carts left, so you'd have to pursue them on the open market.  The 480L cart format was based on the cart for the PC-Junior.  In retrospect, that perhaps wasn't the best choice...

---

### Post #23 -- Page 1
**User:** Waltz Mastering
**Info:** Joined: Mar 2008Posts: 4,057My Studio1 Review written🎧 15 years | Posts: 4,057My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928247&postcount=23>

Hi NS,


The "Ambience" program in the 300 is probably my fave of all Lex verbs.

Any background or info you can give on that would be greatly appreciated.


TW

---

### Post #24 -- Page 1
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928277&postcount=24>

Quote: > Originally Posted byWaltz Mastering➡️Hi NS,The "Ambience" program in the 300 is probably my fave of all Lex verbs.Any background or info you can give on that would be greatly appreciated.TWIt always comes back to Symphony Hall. Do you know the story?


Long before convolution reverbs were possible, there was a statement put forth that you could identify a specific seat in Symphony Hall by collecting the stereo sound energy of the Hall over each 10 millisecond interval and then play that energy back in the form of ambience. This is the 300 Ambience program, with a best attempt reverb following the early ambience.


In a private conversation with David about 5 years ago he told me that he thought the whole notion was rather silly, but there it is.


The forerunner to todays convolution reverbs.


I agree, it is really very nice.


-Casey

---

### Post #25 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928501&postcount=25>

Quote: > Originally Posted byCasey➡️It always comes back to Symphony Hall.So is that why there are so many reverb people in Boston? I always thought it was due to having so many local tech schools that were good, but maybe having a good local hall as a reference inspired people to create better sounding algorithms. I have never been to a concert in Symphony Hall, and I don't know if Seattle has any particularly inspiring acoustical areas, apart from that huge cistern at Fort Warden with the 45 second RT60. Not many people out here were trying to model the Kingdome back in the 1970's and 1980's...


Since we are on the subject of Lexicon reverbs, here's a question: Can you break down the different Lexicon units by the original origins of their algorithms, or are the algorithms constantly evolving by increments? For example, the 224XL (by reading the manuals) seems to have algorithms that weren't in the original 224. The PCM60, PCM70, and M200 all seem to be based upon the 224XL algorithms to some degree, with varying amounts of control. The 480L seems like it was a big leap forward in algorithm design, with the introduction of some new type of randomization, many new algorithms, and the Shape and Spread controls. The PCM90/91 and M300 are obviously descended from the 480L, but many of the lower end Lexicons that followed (PCM80/81, LXP1/5/15) seem like they were based on the 224XL algorithms, at least by the descriptions of the parameters. The current Lexicons all seem to be based solely on the 480L and the 960L style algorithms, with the exception of the PCM96 which brings back the original 224 Concert Hall (and adds a few new algorithms). Is this a correct interpretation of things ("punctuated equilibrium" in evolution terms) or are the algorithms constantly evolving, even when they keep the older parameters and algorithm names? 


Sean

---

### Post #26 -- Page 1
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928957&postcount=26>

Quote: > Originally Posted byNobody Special➡️About Lexicon reverbsPlateThere've been a few minor tweaks on this, but the PCM96 has a version that close to the 480L, although much cleaner.  In this algorithm, Spin and Wander can be used to smooth the frequency response. They're not really intended for chorus-type effects.  Even with large amounts, pitch should be quite stable.  If you find that you still hear modulation effects you don't want, simple turn Spin down or off.  It will sound fine.Thank you very much for the description of the different algorithms inside the PCM96. I already own the 480L (incl. classic card & surround/HD card), 224XL and the PCM91, so I would appreciate if you could pinpoint the benefits of buying the PCM96 in terms of algorithms/quality.


I don't think that my 480L have a dedicated plate algorithm (excluding the Rich Plate in the Classic card), but it does use the dense algorithm for both plates and rooms - that algorithm doesn't have any modulation i.e. spin, wander or chorus. When you mentioned the plate version from the 480L, did you refer to the dense algorithm with additional modulation? If thats the case, I presume that you could recreate most of the room and plate programs from the 480L, including the previous mentioned small/large wood room.


Regarding the Concert Hall - The PCM96 version have shape and spread parameters, whereas the 224XL, the Classic card and the PCM91 have the depth parameter - those sets of parameters works differently - is it possible to mimic the behaviour of the depth parameter with shape and spread?


Do you have any plans for additional algorithms, like Random Ambience and Constant Density Plate B? Or the bandwidth limitation of the 224XL?

---

### Post #27 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3929550&postcount=27>

Quote: > Originally Posted byWarp69➡️Regarding the Concert Hall - The PCM96 version have shape and spread parameters, whereas the 224XL, the Classic card and the PCM91 have the depth parameter - those sets of parameters works differently - is it possible to mimic the behaviour of the depth parameter with shape and spread?Also, the pre-480L boxes had Inverse Room programs. Is it safe to assume that the Shape and Spread parameters allow for this behavior to be emulated, or did the Inverse Room algorithm reappear in later units?


Sean

---

### Post #28 -- Page 1
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3929978&postcount=28>

Quote: > Originally Posted byseancostello➡️Also, the pre-480L boxes had Inverse Room programs. Is it safe to assume that the Shape and Spread parameters allow for this behavior to be emulated, or did the Inverse Room algorithm reappear in later units?SeanThere's an Inverse/non linear algorithm in the PCM91.

---

### Post #29 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3930544&postcount=29>

Quote: > Originally Posted byWarp69➡️I presume that you could recreate most of the room and plate programs from the 480L, including the previous mentioned small/large wood room.Regarding the Concert Hall - The PCM96 version have shape and spread parameters, whereas the 224XL, the Classic card and the PCM91 have the depth parameter - those sets of parameters works differently - is it possible to mimic the behaviour of the depth parameter with shape and spread?Do you have any plans for additional algorithms, like Random Ambience and Constant Density Plate B? Or the bandwidth limitation of the 224XL?Hi.  Yes, I believe you could cover most or all of the older plate sounds.  We've probably already gotten there with more generic names for the presets.  As I've said elsewhere, time and personnel allowing, we might try to do some closer name-for-name matches.


As far as ConcertHall goes, Shape and Spread are in the original (although perhaps by a different name--I don't have a 224) as well as the new version.  The chorus/depth parameters are in the new one as well.


Do I have plans for additional algorithms?  Yes.  I can't say anything about them until we release them, but the DSP has the power to do many interesting things.

---

### Post #30 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3930574&postcount=30>

Quote: > Originally Posted byseancostello➡️Also, the pre-480L boxes had Inverse Room programs. Is it safe to assume that the Shape and Spread parameters allow for this behavior to be emulated, or did the Inverse Room algorithm reappear in later units?SeanHi Sean.  Believe it or not, we always thought that the Inverse algorithm was a half-assed way to do what we really wanted.  The new Room algorithm has about 4 dozen reflection patterns.  There's a reverse parameter that allows you to flip any of those patterns backwards.  You can also scale them and do a few other things.  It's a much better way to get that reversed sound.  The best way to learn how that works is to go into one of the Playroom presets and fiddle around.


Having said that, you can get something very much like Inverse out of any of the reverbs.  Here's how:
Room Size: pretty big

    Reverb Time:  All the way down *(very important)*

    Shape and Spread: High values

    Tap Slope: +10
You can doodle around with the Size/Shape/Spread and get some interesting effects that are pretty similar to Inverse.  The Diffusion parameter will also have an important effect.


---


---

# FULL THREAD — Pages 1–14

# Lexicon Reverbs: A Brief Bestiary -- Gearspace High End Thread

**Thread URL:** https://gearspace.com/board/high-end/362930-lexicon-reverbs-brief-bestiary.html
**Forum:** High End @ Gearspace
**Total Pages:** 14

A technical thread covering the Lexicon reverb hardware family: architecture,
algorithms, and the lineage from early ARU-based units through the 480L and beyond.


---

## Page 1

---

### Post #1 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880302&postcount=1>

**About Lexicon reverbs**


I often see lots of comments about the naturalness or effect-y-ness of Lexicon reverbs.  I think it's worth taking a few minutes to point out the differences in reverbs and how you can use them for either natural or effect-y applications.  After all, there are more than 30 years of history in Lexicon reverbs and they're not all the same.  As we go through them, you'll see me mention two parameters named '*Spin*' and '*Wander*'.  These are often the source of great confusion, and it doesn't help that they're a little different in each of the 'verbs.  In general, their intent is to provide a smoother frequency response for complex material.  In some of the algorithms, they're not really even noticeable as modulation effects. They can often be turned off with no harm, depending on material.


You'll find variants of these algorithms in lots of our verbs, but my descriptions apply most closely to the PCM96.

Concert Hall

This is the granddaddy of Lexicon reverbs and it dates back to the 224.  It was the definitive 80's reverberator.  It is prone to coloration and is best used with very large room sizes.  This is the only algorithm without Spin and Wander.  Instead, it has a pair of chorus controls.  It's a nifty effect for the right material, but you can hear strong pitch effects. While I like the sound, I can't ever imagine using it for any natural sort of mix.

Plate

There've been a few minor tweaks on this, but the PCM96 has a version that close to the 480L, although much cleaner.  In this algorithm, Spin and Wander can be used to smooth the frequency response. They're not really intended for chorus-type effects.  Even with large amounts, pitch should be quite stable.  If you find that you still hear modulation effects you don't want, simple turn Spin down or off.  It will sound fine.

Chamber

Extremely high reflection density and rapid onset--just like you'd expect from a live chamber.  Once again,  spin and wander are present and available to smooth out problem material.  I generally like Chamber with spin turned all the way off.  Alternatively, moderate Spin with a low Wander value ( under 3 milliseconds) will be effective at smoothing frequency response without creating noticeable modulation.

Random Hall

This algorithm dates back the the 480L and you'll find versions in every one of our high-end reverbs after that.  This algorithm is the basis of a lot of good mixes, and is more responsible for the term "Lexicon Sound" than any other reverb.  But it has quite noticeable modulation, especially with smaller room sizes.  I wouldn't suggest messing too much with Spin and Wander for this algorithm.  It is what it is, and that's nice.

Hall

This algorithm was introduced with the PCM96.  It has many of the characteristics of the 480L, without the strong sense of modulation.  If you have material that's strongly colored, then high values for Spin and Wander will help smooth out the material with very little sense of modulation.  At the same time,  for many applications you can turn Spin down completely and have a stable, natural tail.

Room

This one is also new with the PCM96 (there are some old boxes with an algorithm called Room, but those were much closer to a Hall).  While the primary focus of this is post-production, careful programming can give some very nice hall sounds as well.  The early reflections are quite stable and and possible modulation occurs at low levels in the tail where it's helpful in reducing coloration.  If I ever have time, there are a great many presets I'd like to do with this one.  It can be made to sound quite clean and natural.

One other thing

There are a couple of other parameters call Shape and Spread.  They're used to delay injection of energy into the reverb--giving something of an envelope to the early stages of verb.  In some cases, they may appear to cause some late motion in the tail. That's not really what's happening, but it can sound that way.  Reducing either or both of those parameters may be helpful.

Finally

So let me encourage you to spend some time playing with presets based on our different algorithms.  Presets often represent the mindset of the person doing the presets, and a given series of presets may explore only one facet of the algorithm.  You might find that a bit of editing time will open up new possibilities.  We used to throw around a phrase at Lex "We give you the rope...".  I think it still applies.


It appears that many people identify with the Lexicon sound that was available in the decade they entered the business.  With the PCM96, we've tried to incorporate the sounds from all four of those decades.

---

### Post #2 -- Page 1
**User:** drBill
**Info:** Joined: Jul 2006Posts: 22,967My Studio🎧 15 years | Posts: 22,967My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880525&postcount=2>

Thanks NS.  Most helpful.  


What's the closest starting place to on the 96 to get the great Hall sound on the 480?  Also, how about the small wood room (is that what it's called...??) on the 480?


Great explanations.  LOVE IT!!!!


bp

---

### Post #3 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880614&postcount=3>

Quote: > Originally Posted bydrBill➡️Thanks NS.  Most helpful.What's the closest starting place to on the 96 to get the great Hall sound on the 480?  Also, how about the small wood room (is that what it's called...??) on the 480?Great explanations.  LOVE IT!!!!bpIf you're working from the front panel interface, look under any of the halls folders for presets with the RHall name.  Those are based on the RandomHall algorithm.  If you're using the plugin interface, then just load Random Hall.


I'm afraid I don't have a 480 close by, so I can't tell you about the wood room.  But a good starting place for small spaces is the Rooms folder (front panel) or the Room algorithm (plugin).

---

### Post #4 -- Page 1
**User:** Jonathan Starr
**Info:** Joined: Apr 2005Posts: 1,045🎧 20 years | Posts: 1,045
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3880893&postcount=4>

This is really helpful. 


Thanks. & Encore Please (Hana Hou !)

---

### Post #5 -- Page 1
**User:** yeloocproducer
**Info:** Joined: Dec 2004Posts: 1,790My Studio2 Reviews written🎧 20 years | Posts: 1,790My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3892662&postcount=5>

Any other hints on getting the PCM96 to get to sound specifically like some notable presets on the 200, 224, 300, or 480?  Or presets in the PCM96 that were specifically designed to replace some "retro" favorites?  The Rhall note for 480 types is helpful... thanks.


PCM70 "tiled room"?  Anything close?  480 silica beads?


Just got the reverb today and looking forward to firing it up.

---

### Post #6 -- Page 1
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3892988&postcount=6>

Excellent post, NS!!! Thanks.

---

### Post #7 -- Page 1
**User:** Terry McInturff
**Info:** Joined: Mar 2007Posts: 751🎧 15 years | Posts: 751
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3893011&postcount=7>

Yes, a million kudos to you for this information.


Back to the ancient (and zero current profitability) PCM 70...what programs are like Tiled Room, Bright Plate...and any other signature PCM 70 stuff?


Masny thanks, you are very generous!

---

### Post #8 -- Page 1
**User:** Dopamine
**Info:** Joined: Nov 2002Posts: 2,002🎧 20 years | Posts: 2,002
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3894456&postcount=8>

Seems like Lex should include presets on the 96 that are similar to some of the classics:  obviously the PCM70 Tiled Room and 480 Hall.

---

### Post #9 -- Page 1
**User:** synthetic
**Info:** Joined: Aug 2005Posts: 515🎧 20 years | Posts: 515
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3896051&postcount=9>

They've been busy on software and other products, it seems. I wouldn't be surprised if we see some "Classic" programs released down the road. After all it's a simple enough software rev.

---

### Post #10 -- Page 1
**User:** audiomichael
**Info:** Joined: Mar 2005Posts: 2,303🎧 20 years | Posts: 2,303
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3897360&postcount=10>

I kinda like the genericness of the titles, but it would be cool to see a "best of" preset category.  I'd throw the 91's "Deep Blue" into that mix.

---

### Post #11 -- Page 1
**User:** Brad_Wood
**Info:** Joined: Aug 2006Posts: 106My Recordings/Credits🎧 15 years | Posts: 106My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3897388&postcount=11>

Quote: > Originally Posted bydrBill➡️how about the small wood room (is that what it's called...??) on the 480?bpI love love love the small wood room from the 480L & have found the Altiverb versions to be really close to the real thing. 


Best- Brad

---

### Post #12 -- Page 1
**User:** Jack Weaver
**Info:** Joined: Jan 2005Posts: 360🎧 20 years | Posts: 360
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3898454&postcount=12>

Thanks NS -


It helps place many things in perspective. Very good of you to give us this info. 


I can only imagine that if there were a software release resembling "Best of..."

that word would get around fast in the purchasing circles.

---

### Post #13 -- Page 1
**User:** mattssons
**Info:** Joined: Feb 2004Posts: 301My Recordings/CreditsMy Studio🎧 20 years | Posts: 301My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3898565&postcount=13>

Thanks for a great post.


Do you know anything about Lexicon 200? I have one, like a lot especially considering it´s age! /Toby

---

### Post #14 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3899195&postcount=14>

Many good remarks here about favorite presets and such.  I'd certainly be interested in getting as close as possible to some old classics.  I'd also like to gather up some user-generated presets.  We don't have a good way to organize such an effort just yet, but I'd think something with MIDI bulk dump might be one way to get there.


I do hope that some of you have been rolling up your sleeves and getting into programming the box (or even some of your older Lexes).  One thing I've learned is that different people--with different applications, different ears, and different points of view--can come up with some unique and useful sounds.  I know that we've just scratched the surface of what the box can do, and I've love to offer a folder of user favorites.


Toby, hang onto that 200.  It's like your favorite old aunt.  She's crotchety and a little limited for sure, but even if you found a replacement, it would never be the same.


I've been a bit busy of late, but I hope I can get back in here before too long and cover a few more areas of interest.

---

### Post #15 -- Page 1
**User:** audio ergo sum
**Info:** Joined: Oct 2008Posts: 3,644🎧 15 years | Posts: 3,644
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3899714&postcount=15>

Hi NS, is the 96 surround shipping yet in quantities?

---

### Post #16 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3900285&postcount=16>

Quote: > Originally Posted byaudio ergo sum➡️Hi NS, is the 96 surround shipping yet in quantities?It started going out a few weeks ago.  If your dealer doesn't have any yet, it shouldn't be too long.

---

### Post #17 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3926870&postcount=17>

Hi NS (1st time poster here):


How much consistency is there between algorithms of the same name over Lexicon history? For example, is the Rich Chamber of the 224XL similar to the PCM70 room/chamber, and how much do things change with the 480L and later reverbs?


Also, is time variation generally found on the high end Lexicons only, or does it make its way into the lower priced units as well? I remember using the 224XL, and the Mode Optimization seemed like some sort of chorusing, while I presume the 480L and later use some different type of time variation.


Thanks,


Sean Costello

---

### Post #18 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927153&postcount=18>

Quote: > Originally Posted byseancostello➡️Hi NS (1st time poster here):How much consistency is there between algorithms of the same name over Lexicon history? For example, is the Rich Chamber of the 224XL similar to the PCM70 room/chamber, and how much do things change with the 480L and later reverbs?Also, is time variation generally found on the high end Lexicons only, or does it make its way into the lower priced units as well? I remember using the 224XL, and the Mode Optimization seemed like some sort of chorusing, while I presume the 480L and later use some different type of time variation.Thanks,Sean CostelloHi Sean,

Some things change, but many things remain consistent (wishy-washy answer but it's true).  Back when David Griesinger was doing products like the 224, there were zillions of things he wanted to do that the hardware wouldn't allow.  As hardware became more powerful, fewer corners needed to be cut.  On top of that, time, thought and experimentation led to better ways to make a reverb algorithm.  So there's been a continual process of improvement.  Lots of times, customers may not see it that way:  if you cut your first hit record with a 224, the last thing you want is to see it change.  But on our side of the fence, we're always looking for some way to make things sound better.  But still there are some things that make a plate a plate, and we try to respect and extend that.


In terms of specific products, the 70 was a simplified version of the 224 and the algorithms sound pretty similar.  The 480 extended that with a better S/N ratio and more algorithms.  The 960 was a further extension.  It was a little lighter and more transparent: some people loved it and some people hated it.  The PCM96 incorporates qualities of both, and can be leaned in either direction.  It was also our first floating-point processor, with considerably better performance.


The chorusing sound of the 224 family was a characteristic of the ConcertHall algorithm.  It's the only algorithm that works that way.  You'll also find variants of that sound in the PCM91 and PCM96.  As I indicated in an earlier post, it sure isn't realistic but it might just be the thing you need.  Other algorithms approach time variance (we call it randomization) in other ways and for other purposes.  Ideally, it's not something you should hear as chorusing.  It's intended to break up room modes and improve frequency response.


Randomization has been a feature of most of our products in recent years.  Ten years ago it came down as far as the PCM90/91.  A few years later it came down as far as the MPX100.  Now it's in everything.  It's obviously a little slicker in the high-end products, but even in a product like the MX-200 it's more complex that the 480.  I kinda like Moore's law.

---

### Post #19 -- Page 1
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927250&postcount=19>

Quote: > Originally Posted byseancostello➡️I remember using the 224XL, and the Mode Optimization seemed like some sort of chorusing, while I presume the 480L and later use some different type of time variation.The Decay Optimization in some of the 480L algorithms have nothing to do with chorusing. And the same is true for the 224XL.


Did you mean Mode Enhancement?

---

### Post #20 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927333&postcount=20>

Quote: > Originally Posted byWarp69➡️The Decay Optimization in some of the 480L algorithms have nothing to do with chorusing. And the same is true for the 224XL.Did you mean Mode Enhancement?Yep. I just mixed the two terms up. Decay Optimization seems like something used to reduce certain artifacts for impulsive sounds.


Sean

---

### Post #21 -- Page 1
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927554&postcount=21>

Quote: > Originally Posted byWarp69➡️The Decay Optimization in some of the 480L algorithms have nothing to do with chorusing.This is becoming a great historic record, thanks for starting it NS.


Early on decay optimization was simply turning down the level of reverb when no input signal was present. Over time it transformed into a switch which coupled/decoupled the size parameter from the reverb time. (If I recall correctly!)


More importantly; NS I don't believe that you mentioned Davids 480 surround algorithm, which I believe he is quite proud of. I will add that it rocks, even in stereo, and makes finding a surround option cart for the 480 a requirement for 480 fans.


-Casey

---

### Post #22 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3927722&postcount=22>

Quote: > Originally Posted byCasey➡️This is becoming a great historic record, thanks for starting it NS.Early on decay optimization was simply turning down the level of reverb when no input signal was present. Over time it transformed into a switch which coupled/decoupled the size parameter from the reverb time. (If I recall correctly!)More importantly; NS I don't believe that you mentioned Davids 480 surround algorithm, which I believe he is quite proud of. I will add that it rocks, even in stereo, and makes finding a surround option cart for the 480 a requirement for 480 fans.-CaseyAlmost.  Decay optimization had to do with managing allpasses (could be my memory giving out.  Got a virus of some sort today).  The decoupling parameter was called "Link".  It 'disappeared' and hasn't been missed.  David's nice surround algorithm was based on the Random Hall and was 2-in/4-out.  I don't think we have any of the carts left, so you'd have to pursue them on the open market.  The 480L cart format was based on the cart for the PC-Junior.  In retrospect, that perhaps wasn't the best choice...

---

### Post #23 -- Page 1
**User:** Waltz Mastering
**Info:** Joined: Mar 2008Posts: 4,057My Studio1 Review written🎧 15 years | Posts: 4,057My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928247&postcount=23>

Hi NS,


The "Ambience" program in the 300 is probably my fave of all Lex verbs.

Any background or info you can give on that would be greatly appreciated.


TW

---

### Post #24 -- Page 1
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928277&postcount=24>

Quote: > Originally Posted byWaltz Mastering➡️Hi NS,The "Ambience" program in the 300 is probably my fave of all Lex verbs.Any background or info you can give on that would be greatly appreciated.TWIt always comes back to Symphony Hall. Do you know the story?


Long before convolution reverbs were possible, there was a statement put forth that you could identify a specific seat in Symphony Hall by collecting the stereo sound energy of the Hall over each 10 millisecond interval and then play that energy back in the form of ambience. This is the 300 Ambience program, with a best attempt reverb following the early ambience.


In a private conversation with David about 5 years ago he told me that he thought the whole notion was rather silly, but there it is.


The forerunner to todays convolution reverbs.


I agree, it is really very nice.


-Casey

---

### Post #25 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928501&postcount=25>

Quote: > Originally Posted byCasey➡️It always comes back to Symphony Hall.So is that why there are so many reverb people in Boston? I always thought it was due to having so many local tech schools that were good, but maybe having a good local hall as a reference inspired people to create better sounding algorithms. I have never been to a concert in Symphony Hall, and I don't know if Seattle has any particularly inspiring acoustical areas, apart from that huge cistern at Fort Warden with the 45 second RT60. Not many people out here were trying to model the Kingdome back in the 1970's and 1980's...


Since we are on the subject of Lexicon reverbs, here's a question: Can you break down the different Lexicon units by the original origins of their algorithms, or are the algorithms constantly evolving by increments? For example, the 224XL (by reading the manuals) seems to have algorithms that weren't in the original 224. The PCM60, PCM70, and M200 all seem to be based upon the 224XL algorithms to some degree, with varying amounts of control. The 480L seems like it was a big leap forward in algorithm design, with the introduction of some new type of randomization, many new algorithms, and the Shape and Spread controls. The PCM90/91 and M300 are obviously descended from the 480L, but many of the lower end Lexicons that followed (PCM80/81, LXP1/5/15) seem like they were based on the 224XL algorithms, at least by the descriptions of the parameters. The current Lexicons all seem to be based solely on the 480L and the 960L style algorithms, with the exception of the PCM96 which brings back the original 224 Concert Hall (and adds a few new algorithms). Is this a correct interpretation of things ("punctuated equilibrium" in evolution terms) or are the algorithms constantly evolving, even when they keep the older parameters and algorithm names? 


Sean

---

### Post #26 -- Page 1
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3928957&postcount=26>

Quote: > Originally Posted byNobody Special➡️About Lexicon reverbsPlateThere've been a few minor tweaks on this, but the PCM96 has a version that close to the 480L, although much cleaner.  In this algorithm, Spin and Wander can be used to smooth the frequency response. They're not really intended for chorus-type effects.  Even with large amounts, pitch should be quite stable.  If you find that you still hear modulation effects you don't want, simple turn Spin down or off.  It will sound fine.Thank you very much for the description of the different algorithms inside the PCM96. I already own the 480L (incl. classic card & surround/HD card), 224XL and the PCM91, so I would appreciate if you could pinpoint the benefits of buying the PCM96 in terms of algorithms/quality.


I don't think that my 480L have a dedicated plate algorithm (excluding the Rich Plate in the Classic card), but it does use the dense algorithm for both plates and rooms - that algorithm doesn't have any modulation i.e. spin, wander or chorus. When you mentioned the plate version from the 480L, did you refer to the dense algorithm with additional modulation? If thats the case, I presume that you could recreate most of the room and plate programs from the 480L, including the previous mentioned small/large wood room.


Regarding the Concert Hall - The PCM96 version have shape and spread parameters, whereas the 224XL, the Classic card and the PCM91 have the depth parameter - those sets of parameters works differently - is it possible to mimic the behaviour of the depth parameter with shape and spread?


Do you have any plans for additional algorithms, like Random Ambience and Constant Density Plate B? Or the bandwidth limitation of the 224XL?

---

### Post #27 -- Page 1
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3929550&postcount=27>

Quote: > Originally Posted byWarp69➡️Regarding the Concert Hall - The PCM96 version have shape and spread parameters, whereas the 224XL, the Classic card and the PCM91 have the depth parameter - those sets of parameters works differently - is it possible to mimic the behaviour of the depth parameter with shape and spread?Also, the pre-480L boxes had Inverse Room programs. Is it safe to assume that the Shape and Spread parameters allow for this behavior to be emulated, or did the Inverse Room algorithm reappear in later units?


Sean

---

### Post #28 -- Page 1
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3929978&postcount=28>

Quote: > Originally Posted byseancostello➡️Also, the pre-480L boxes had Inverse Room programs. Is it safe to assume that the Shape and Spread parameters allow for this behavior to be emulated, or did the Inverse Room algorithm reappear in later units?SeanThere's an Inverse/non linear algorithm in the PCM91.

---

### Post #29 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3930544&postcount=29>

Quote: > Originally Posted byWarp69➡️I presume that you could recreate most of the room and plate programs from the 480L, including the previous mentioned small/large wood room.Regarding the Concert Hall - The PCM96 version have shape and spread parameters, whereas the 224XL, the Classic card and the PCM91 have the depth parameter - those sets of parameters works differently - is it possible to mimic the behaviour of the depth parameter with shape and spread?Do you have any plans for additional algorithms, like Random Ambience and Constant Density Plate B? Or the bandwidth limitation of the 224XL?Hi.  Yes, I believe you could cover most or all of the older plate sounds.  We've probably already gotten there with more generic names for the presets.  As I've said elsewhere, time and personnel allowing, we might try to do some closer name-for-name matches.


As far as ConcertHall goes, Shape and Spread are in the original (although perhaps by a different name--I don't have a 224) as well as the new version.  The chorus/depth parameters are in the new one as well.


Do I have plans for additional algorithms?  Yes.  I can't say anything about them until we release them, but the DSP has the power to do many interesting things.

---

### Post #30 -- Page 1
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3930574&postcount=30>

Quote: > Originally Posted byseancostello➡️Also, the pre-480L boxes had Inverse Room programs. Is it safe to assume that the Shape and Spread parameters allow for this behavior to be emulated, or did the Inverse Room algorithm reappear in later units?SeanHi Sean.  Believe it or not, we always thought that the Inverse algorithm was a half-assed way to do what we really wanted.  The new Room algorithm has about 4 dozen reflection patterns.  There's a reverse parameter that allows you to flip any of those patterns backwards.  You can also scale them and do a few other things.  It's a much better way to get that reversed sound.  The best way to learn how that works is to go into one of the Playroom presets and fiddle around.


Having said that, you can get something very much like Inverse out of any of the reverbs.  Here's how:
Room Size: pretty big

    Reverb Time:  All the way down *(very important)*

    Shape and Spread: High values

    Tap Slope: +10
You can doodle around with the Size/Shape/Spread and get some interesting effects that are pretty similar to Inverse.  The Diffusion parameter will also have an important effect.


---

## Page 2

---

### Post #31 -- Page 2
**User:** Empty Planet
**Info:** Joined: Nov 2003Posts: 1,307🎧 20 years | Posts: 1,307
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3930768&postcount=31>

Really interesting material, thank very much for sharing it.  


If you have data that's more PCM70-specific I would dearly love to hear it.  


Cheers.

---

### Post #32 -- Page 2
**User:** Waltz Mastering
**Info:** Joined: Mar 2008Posts: 4,057My Studio1 Review written🎧 15 years | Posts: 4,057My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3930799&postcount=32>

Quote: > Originally Posted byCasey➡️The forerunner to todays convolution reverbs.Thanks for the info.


TW

---

### Post #33 -- Page 2
**User:** Dan
**Info:** Joined: Mar 2004Posts: 1,677🎧 20 years | Posts: 1,677
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3931014&postcount=33>

Hi Quality thread.  Thanks!

---

### Post #34 -- Page 2
**User:** mark714
**Info:** Joined: Oct 2004Posts: 772🎧 20 years | Posts: 772
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3931146&postcount=34>

If only all threads were like this...

---

### Post #35 -- Page 2
**User:** DanDan
**Info:** Joined: Aug 2003Posts: 16,4331 Review written🎧 20 years | Posts: 16,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3931208&postcount=35>

Interesting thread, thanks to nobodyspecial. I noted the One Other Thing near the end of the thread. Shape and Spread were mentioned briefly and how to minimise problems caused by them!  I hope they are not being phased out or disregarded. IMHO they were THE LEX sound or at least the part of it that I loved and found indispensible. i.e. 480 

I just love that ghostly after bloom of reflections, which is kind of like a soft delay but  much richer more complex and more mysterious. I miss that now because I can't hire a 480 anymore. My 91 makes an attempt at the same thing but... I will have look into those Altiverb samples. 

I do hope the 96 proves a success.  Lex, like Neumann, Urei, GML, have always been one of the pillars of my world and I would like to see them continue. 

Best Regards, DD
[Sound Sound - Homepage](http://www.soundsound.ie)

---

### Post #36 -- Page 2
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3931385&postcount=36>

Quote: > Originally Posted byNobody Special➡️As far as ConcertHall goes, Shape and Spread are in the original (although perhaps by a different name--I don't have a 224) as well as the new version.Are you sure about that? The 224XL manual I have shows a Depth control, which sounds somewhat different from Shape and Spread. Depth sounds like it controls virtual "microphones" from within the Hall, while Shape and Spread seem to control the energy injection into the hall. I am wondering if Tap Slope on the PCM96 is a better analogy for Depth in the 224XL Halls.


The illustration of the Hall algorithms in the 224XL manual shows 4 lines from each side (left right) of the reverb block going into the box marked "Depth," with one of the lines from each side delayed by a block marked "Fine Predelay." Presumably the Depth control adjusts the relative slope of these "microphones," although I am not presuming that the illustration is an accurate reflection of the exact internals of the algorithm.


For people that express preference for the pre-480L boxes, is it safe to presume that setting Shape and Spread to their minimums would be a good suggestion for emulating this sound with the PCM96? Or is the sound of the older units due to fixed point issues / frequency bandwidth / converter differences / all in people's heads and not really based on any truth?


I would also like to join in the chorus of thanks to NS, and to the others who are adding to this thread. 


Sean

---

### Post #37 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3931449&postcount=37>

Quote: > Originally Posted byDanDan➡️Shape and Spread were mentioned briefly and how to minimise problems caused by them!  I hope they are not being phased out or disregarded. IMHO they were THE LEX sound or at least the part of it that I loved and found indispensible.Sound Sound - HomepageNot to worry.  Shape and Spread have compromising photographs of several Lexicon engineers.  No way they're going anyplace.  Thanks for the nice remarks.

---

### Post #38 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3931509&postcount=38>

Quote: > Originally Posted byseancostello➡️Are you sure about that? The 224XL manual I have shows a Depth control, which sounds somewhat different from Shape and Spread. Depth sounds like it controls virtual "microphones" from within the Hall, while Shape and Spread seem to control the energy injection into the hall. I am wondering if Tap Slope on the PCM96 is a better analogy for Depth in the 224XL Halls.Hmm.  Now you've got me stymied.  I worked from an old diagram that Barry Blesser extracted about fifteen years ago.  That was augmented by discussions with Dave Griesinger more recently.  The actual source code was lost many many years ago.  I don't have a 224, so I'm going to wing it on this one.  First of all, tap slope isn't an analogy for anything in the 224 (of course if you discover one, I'll claim I knew it all along).  Tap slope is the tweakiest of parameters, with a decreasing effect as reverb time increases.  The only time you're going to notice much about it is with very short reverb times, as in my description of *Inverse* earlier today. Was that on this thread?


The *Depth* parameter on the PCM96 version of Concert Hall affects the amount of time modulation in the chorus, while *Rate* affects the rate of modulation. Turn them both up and say goodbye to lunch.  There is another parameter called *Definition* which may be closer to what you're describing.  It controls the reflection density within the reverb.
Quote: > For people that express preference for the pre-480L boxes, is it safe to presume that setting Shape and Spread to their minimums would be a good suggestion for emulating this sound with the PCM96?ConcertHall was the only Lexicon algorithm that ever worked the way it does.  None of the other algorithms sound remotely like it.  By the way, Dave G thought I was nuts to try to bring it back.  While I agree with him that it's not very useful for the classical music I primarily enjoy, I still thought it was valuable for other applications.


I'd focus on *Definition* and the two *Chorus* controls.  I think that Shape and Spread are primarily doing what you described with the 4 pseudo-microphones.  Minimizing those values may make a preset "pop" more immediately.  That's not always good. I'd recommend experimenting with those until you get the effect you like.
Quote: > Or is the sound of the older units due to fixed point issues / frequency bandwidth / converter differences / all in people's heads and not really based on any truth?It's certainly true in some areas.  The 224 had a very limited bandwidth and a notably dark sound.  That in part is why I put damping controls and optional 2-pole filters in the PCM96. The converters certainly played a part in it, but who could say how much? Converters in those days were pretty nasty.  DSP limitations and memory bit depth are responsible for a lot of the sound that some people describe as grainy.
Quote: > I would also like to join in the chorus of thanks to NS, and to the others who are adding to this thread.SeanThank you Sean.  I do hope that folks will dive a little deeper into programming these boxes over time, and then share what they've learned.  I always enjoy being surprised by what someone has discovered (Well, not always.  Sometimes they discover bugs).  I think I've babbled enough for one day.  Good night, everyone.

NS

---

### Post #39 -- Page 2
**User:** labcomp
**Info:** Joined: Jul 2006Posts: 110🎧 15 years | Posts: 110
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3936018&postcount=39>

While we have the experts ear, what current machines if any can accurately reproduce the 'vocal jiz' preset found on our old nuverbs? The reason I ask, is that we have some archived scores that need brought out, which used this preset (with only pre-delay times altered), and must be done exactly as were originally printed. (Just in higher resolution mixes)


Regards,

DLevy

mgr, Legacy Lab

---

### Post #40 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3936521&postcount=40>

Quote: > Originally Posted bylabcomp➡️While we have the experts ear, what current machines if any can accurately reproduce the 'vocal jiz' preset found on our old nuverbs? The reason I ask, is that we have some archived scores that need brought out, which used this preset (with only pre-delay times altered), and must be done exactly as were originally printed. (Just in higher resolution mixes)mgr, Legacy LabSorry, I don't know the preset.  Probably your best bet is to make note of the underlying algorithm and the parameters, then try matching them up on another box.  Nuverb was a low-fat version of the 300, so you could probably match it directly there.  The PCM91 would probably get you close, as would the PCM96.  Ranges of some of the parameters are likely to differ, so some experimenting would be in order.  Good luck!

---

### Post #41 -- Page 2
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3936651&postcount=41>

one of my favorite *WTF?!* effects is in the PCM90. Route an LFO to stereo pan and let the seasick inducing roller coaster ride begin!  stereo panning goes from mono to stereo to out of phase and back again with one number (+/- 360).  the sound folds in on itself then gets unnaturally wide...


dub madness  


this application is rather comical.. but having a number for fluid stereo panorama is great, especially for the out of phase widening tricks... 


in more subtle doses it can really add movement without really drawing the attention of the listener to what exactly is causing the movement... which is whatcha want with ear candy...

---

### Post #42 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3936683&postcount=42>

Quote: > Originally Posted by11413➡️one of my favoriteWTF?!effects is in the PCM90. Route an LFO to stereo pan and let the roller coaster ride begin...  stereo panning goes from mono to stereo to out of phase and back again with one number (+/- 360).  the sound folds in on itself then gets unnaturally wide...dub madnessthis application is rather comical.. but having a number for fluid stereo panorama is great, especially for the out of phase widening tricks...My, you *do* have unusual tastes.  There's a parameter on all the 960L and PCM96 stereo reverbs called "Tail Width".  It's the same thing.  Neither box has the same sort of LFO as the PCM90/91, but you can automate via MIDI and get the same thing.  Most people can't take too much of it.


BTW, if you set the width to -22 degrees (or +338 degrees), you'll get a reverb tail that encodes nicely into any stereo matrix.  With a decoder like Logic 7, ProLogic2 or Circle Surround, you'll end up with a nice multichannel 'verb.  It's both stereo and mono-compatible, too.  We put it there for people whose delivery medium was stereo but who wanted a little more if the recording was played back on a matrix decoder.  The early reflections are still anchored in the front channels in case there's still something like a PhazeChaser (nasty thing) in the circuit.

---

### Post #43 -- Page 2
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3987705&postcount=43>

Another question for NS:


Do you know how to classify the reverb algorithm used in many of the LXP15 algorithms (Delay/Reverb, Pitch/Delay, etc.)? My guess is that it isn't a plate, as the Plate algorithm is also present, and sounds a lot like the Rich Plate I have heard elsewhere. Is the reverb algorithm a Chamber, Hall, other?


Thanks,


Sean Costello (who just picked up an LXP15 today)

---

### Post #44 -- Page 2
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3987725&postcount=44>

It's a dumbed down 480 type hall. Similar to the Lexiverb hall that was available as a protools plugin. The same basic algorithm was used as the "hall" setting in several home stereo products.


-Casey

---

### Post #45 -- Page 2
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3987933&postcount=45>

Thanks Casey. I presume that this is different from the Random Hall algorithm? I don't have access to a 480L.


Also, are the Shape and Spread controls from the 480L incorporated and just preset, or are they left out of the simpler algorithms?


Thanks,


Sean Costello

---

### Post #46 -- Page 2
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3987936&postcount=46>

There will always be some specific shape and spread. It's just fixed in some cases.


-Casey

---

### Post #47 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=3989161&postcount=47>

Quote: > Originally Posted byseancostello➡️Another question for NS:Do you know how to classify the reverb algorithm used in many of the LXP15 algorithmsCasey's descriptions are accurate.  I'll add that the basic hall reverb in the LXP-15 is the same one in the LXP-1, Alex and Reflex.  They may have been tweaked just a teensy from box to box,  but not enough to make any real difference.


Many of the parameters available in the larger boxes were still there, with preset values as Casey indicates.  If you ever tried to *edit* an LXP-1, you'll know why we simplified.

---

### Post #48 -- Page 2
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4032728&postcount=48>

I am wondering about the 'Moore's Law' aspect of, say, the PCM96 against some of the older boxes and how that relates to 'the sound'. I have a pretty good idea of the computational power of the older boxes (224 - PCM70 - LXP1-5-15 are similar, 300/PCM91 are about double that, and 480 is about double that again) -  observations that come mostly from fixing them. Oh my, the 480 sure has a lot of chips in it.


Obviously it should be quite easy to recreate, say, the older PCM60 and 480L algorithms on a newer, faster processor (provided you don't have to reverse engineer the old box to extract how it works). Certainly it should be easier to design an algorithm without having to manually split up that algorithm between two or more Lexichips.


What I'm interested in is more 'progress' and 'process' rather than digging backwards, and how that makes something like the PCM96 an improvement over a 480L both from a user's perspective - the sound - and from a developer's perspective - the approach to writing a new reverb or effect algorithm.

---

### Post #49 -- Page 2
**User:** Tube World
**Info:** Joined: Jan 2008Posts: 2,4025 Reviews written🎧 15 years | Posts: 2,402
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4032763&postcount=49>

Thanks for giving us this information on Lexicon. That helps confirm that the PCM 96 is not just a 91 that can record up to 96. It also confirms that your not stuck with the lush reverb of the Lexicon past, but you can obtain some cleaner reverbs as well. thumbsup

---

### Post #50 -- Page 2
**User:** raal
**Info:** Joined: Dec 2004Posts: 5,958My Studio1 Review written🎧 20 years | Posts: 5,958My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4032820&postcount=50>

wonderful thread.


can't believe no one's mentioned autopark for rock n' roll toms.

---

### Post #51 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4033769&postcount=51>

Quote: > Originally Posted bydale116dot7➡️What I'm interested in is more 'progress' and 'process' rather than digging backwards, and how that makes something like the PCM96 an improvement over a 480L both from a user's perspective - the sound - and from a developer's perspective - the approach to writing a new reverb or effect algorithm.Hi,

The more powerful processor in something like the PCM96 brings a lot of advantages.  You'll be hearing more of them as time goes along.  I can give you few ideas.  The older processors all required strange assembly languages (there are only 4-5 people in the world who ever programmed a Lexichip 3).  Now we can use high-level languages.  This makes prototyping new algorithms much faster and more intuitive.  The sheer number of algorithms in the box is a testament to this. This also shows up in the new reverbs by their much-more flexible equalization architecture.  This allows us to approach the dark sound of the 480 as well as the lighter sound of the 960--all within the same algorithm.  And of course, we're now working in floating-point as opposed to the rather strange version of fixed-point in the earlier processors.  This gives higher dynamic range, better signal-to-noise and considerably fewer math artifacts.

---

### Post #52 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4033773&postcount=52>

Quote: > Originally Posted byraal➡️can't believe no one's mentioned autopark for rock n' roll toms.Now someone has.

---

### Post #53 -- Page 2
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4033850&postcount=53>

So is it true the PCM91 and 300  have roughly the same processing power? Because to my ears the 300 always sounded better (denser, rounder, more natural, better depth perception) etc. and most people I know agree. And is it true a single (stereo) instance of th 480l uses twice the processing power of the 300?

---

### Post #54 -- Page 2
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4033989&postcount=54>

Quote: > Originally Posted byliving sounds➡️So is it true the PCM91 and 300  have roughly the same processing power? Because to my ears the 300 always sounded better (denser, rounder, more natural, better depth perception) etc. and most people I know agree.The 300 sounds better because the algorithms are better.


The 91 Halls are derived from 224/70 series halls. IMO the 91 hall algorithm used the extra resource available to overdo a good thing and as a result they lost a bit of the earlier quality.


The 300 halls are very (90%) similar to the 480 halls.

Quote: > Originally Posted byliving sounds➡️And is it true a single (stereo) instance of th 480l uses twice the processing power of the 300?No. The 300 has about 20% more processing power than a single 480 machine.


-Casey

---

### Post #55 -- Page 2
**User:** NoFalsetto
**Info:** Joined: Feb 2009Posts: 84🎧 15 years | Posts: 84
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4034190&postcount=55>

I was always quite fond of the 200. It was great for the big '80's snare drum. The 480 was always great and I simply loved the PCM 90 for it's rhythmic delays a Bee Gees must have. In my early days I couldn't do without the PrimeTime it's best feature was the voltage control I used to control it with an ARP 2600. Today... I like waves plugins

---

### Post #56 -- Page 2
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4034711&postcount=56>

Thanks Casey! So last question: Does the Nuverb differ from the 300 in terms of processing power or algorithmic quality (apart from the fact that it has less algorithms)? Because to my ears, as far as I can remember, they sounded the same with the same presets.

---

### Post #57 -- Page 2
**User:** Bob Ross
**Info:** Joined: Mar 2005Posts: 5,587My Studio🎧 20 years | Posts: 5,587My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4035260&postcount=57>

Quote: > Originally Posted byNobody Special➡️That's not really what's happening, but it can sound that way.Cognitive scientists would have a field day with that sentence!


Quote: > Originally Posted byNobody Special➡️Other algorithms approach time variance (we call it randomization) in other ways and for other purposes.  Ideally, it's not something you should hear as chorusing.It's intended to break up room modesand improve frequency response.Are you referring to the "simulated" room modes in the "virtual" room created (implied, suggested, emulated, whatever) by the reverberator, or do you literally mean actual room modes captured by the microphones in the source material?

---

### Post #58 -- Page 2
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4035458&postcount=58>

Quote: > Originally Posted byCasey➡️No. The 300 has about 20% more processing power than a single 480 machine.Is that 300 = 20% faster than one of the two boards in a 480, or a 480 total (both boards)? Since I've done recent repairs on a 91, I recall that the 91 should be about 40% faster than a 300, but that's just from memory of a number stamped on a part on the board, and my memory's starting to get a bit intermittent.


Thanks for the insight on algorithm design, that's sort of what I thought.

---

### Post #59 -- Page 2
**User:** Duardo
**Info:** Joined: Jul 2002Posts: 4,154🎧 20 years | Posts: 4,154
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4035667&postcount=59>

Quote: > The 480 extended that with a better S/N ratio and more algorithms. The 960 was a further extension. It was a little lighter and more transparent: some people loved it and some people hated it. The PCM96 incorporates qualities of both, and can be leaned in either direction. It was also our first floating-point processor, with considerably better performance.So is the PCM96 now your flagship processor, or will you be coming out with a higher-end LARC-type piece in the future?

---

### Post #60 -- Page 2
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4035979&postcount=60>

Quote: > Originally Posted byDuardo➡️So is the PCM96 now your flagship processor, or will you be coming out with a higher-end LARC-type piece in the future?Sorry Duardo,

I can only discuss products we have available or have announced. The PCM96 is currently the king of the hill. There will be even more algorithms for it, but I can't say anything further at the moment.


---

## Page 3

---

### Post #61 -- Page 3
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4035992&postcount=61>

Quote: > Originally Posted byliving sounds➡️Does the Nuverb differ from the 300 in terms of processing power or algorithmic quality (apart from the fact that it has less algorithms)? Because to my ears, as far as I can remember, they sounded the same with the same presets.The guts (if you will) of the Nuverb are pretty much a 300. So the reverb processing capability is the same IIRC. The difference is in the soft control vs the HW 300 front panel (or LARC) control. These are not identical, so you do pick up some small changes related to that in how the presets are constructed.

Quote: > Originally Posted bydale116dot7➡️Is that 300 = 20% faster than one of the two boards in a 480, or a 480 total (both boards)?I'm sorry for the confusion in my wording. The 300 is 20% faster than one of the two boards in a 480.


-Casey

---

### Post #62 -- Page 3
**User:** Animus
**Info:** Joined: Feb 2005Posts: 10,671🎧 20 years | Posts: 10,671
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4037811&postcount=62>

Quote: > Originally Posted byNobody Special➡️Sorry Duardo,I can only discuss products we have available or have announced. The PCM96 is currently the king of the hill. There will be even more algorithms for it, but I can't say anything further at the moment.I am a big lover of Lexicon reverbs.  I have 3 Nuverb cards, a PCM80 and a PCM90.   But I must confess, I have a Eventide DSP4k coming tomorrow!  I will have my effects covered.


One thing I would die for is a modern pci express dsp card (a la Nuverb) that ran some Lexicon goodness.  I think Nuverb was an awesome idea and wouldl like to see a modern implementation.  Or better yet, develop something for the UAD2 card.  People would go nuts.

---

### Post #63 -- Page 3
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4038329&postcount=63>

Quote: > Originally Posted byCasey➡️I'm sorry for the confusion in my wording. The 300 is 20% faster than one of the two boards in a 480.-Casey

Just for clarification: So for a given stereo instance the 300 has actually more power than the 480? But again, the latter sounds better due to better algorithms?

---

### Post #64 -- Page 3
**User:** labcomp
**Info:** Joined: Jul 2006Posts: 110🎧 15 years | Posts: 110
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4038630&postcount=64>

Any guesses folks, where we can get memory RAM cards for our PCM91?


Regards,

DLevy

mgr, Legacy Lab

---

### Post #65 -- Page 3
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4038637&postcount=65>

Quote: > Originally Posted byCasey➡️I'm sorry for the confusion in my wording. The 300 is 20% faster than one of the two boards in a 480.Thanks, that's what I thought. It sounds like the PCM96 has enough guts to do all of the various algorithms in any of the older boxes, plus new ones. The new ones are interesting to me. I wanted to try one out, but as soon as it arrived at our local recording store, someone bought it. I guess it's a toss-up between the 96 and the M7.


Memory cards? You might want to try Digi-key, I think they still have PCMCIA SRAM cards. I haven't used them as I haven't filled up the internal registers in my '91 yet.

---

### Post #66 -- Page 3
**User:** bleen
**Info:** Joined: Nov 2002Posts: 3,041My Recordings/Credits6 Reviews written🎧 20 years | Posts: 3,041My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4038772&postcount=66>

Quote: > Originally Posted byAnimus➡️One thing I would die for is a modern pci express dsp card (a la Nuverb) that ran some Lexicon goodness.Gimme! I'd jump all over something like this!

---

### Post #67 -- Page 3
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4039336&postcount=67>

Quote: > Originally Posted byliving sounds➡️Just for clarification: So for a given stereo instance the 300 has actually more power than the 480? But again, the latter sounds better due to better algorithms?Or, are there algorithms on the 480L that use both of the boards together?

---

### Post #68 -- Page 3
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4039345&postcount=68>

Quote: > Originally Posted byseancostello➡️Or, are there algorithms on the 480L that use both of the boards together?You can use them "together", but that means chaining one through the other. No real combined algorithms.

---

### Post #69 -- Page 3
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4039493&postcount=69>

Quote: > Originally Posted byliving sounds➡️Just for clarification: So for a given stereo instance the 300 has actually more power than the 480?Yes.

Quote: > Originally Posted byliving sounds➡️But again, the latter sounds better due to better algorithms?My "better algorithms" comment was comparing the 300 to the 91. 


As to whether a 300 or 480 sounds better is up to you! Both are great.

Quote: > Originally Posted byliving sounds➡️You can use them "together", but that means chaining one through the other. No real combined algorithms.There is a combined algorithm. It is available in the optional surround cart for the 480. The surround alg can be used for stereo.


-Casey

---

### Post #70 -- Page 3
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4041342&postcount=70>

Quote: > Originally Posted byCasey➡️There is a combined algorithm. It is available in the optional surround cart for the 480. The surround alg can be used for stereo.Does the surround algorithm use all of the surround outputs, combined to stereo? Or is this something that has to be done by the user outside of the box?


Also, are there any Lexicon algorithms of past or present that DON'T work well when summed to mono? All of the ones I have played with seem to work well both in stereo and mono, which is not true of many other reverb designs.


Sean Costello

---

### Post #71 -- Page 3
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4041586&postcount=71>

Any word on what is different about the 480 HD card? Warp sended me some impulses and I loved the colour/smoothness of that sound.

---

### Post #72 -- Page 3
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4041623&postcount=72>

Quote: > Originally Posted byseancostello➡️Does the surround algorithm use all of the surround outputs, combined to stereo? Or is this something that has to be done by the user outside of the box?The surround and the HD use the exact same algorithm, where the HD  combine the 4 surround outputs to stereo inside the algorithm.

---

### Post #73 -- Page 3
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4041628&postcount=73>

Quote: > Originally Posted byFroombosch➡️Any word on what is different about the 480 HD card? Warp sended me some impulses and I loved the colour/smoothness of that sound.The HD & Surround algorithm have an early reflection engine - only one other algorithm use an early reflection engine and thats the Ambience algorithm.

---

### Post #74 -- Page 3
**User:** qtuner
**Info:** Joined: May 2005Posts: 720🎧 20 years | Posts: 720
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4061689&postcount=74>

Nobody Special, Casey


I'm a professional software developer, and i'm curious what the tools and environment are like for developing software for the pcm96 and other lexicon products.  Have the tools made it easier for you guys to get software out the door?  You touched on this earlier, can you elaborate a little bit without giving anything away?  Feel free to comment about obsolete machines, they would probably be more interesting anyway.  


What challenges have rising requirements complexity, ie plug-in integration, firewire, ethernet, etc posed?


How many developers are working on the pcm96?  


I'm a software consultant that writes boring business code all day so i can go home and play in my studio.  I love programming and playing in my studio, and I've always wondered what it would be like to marry the two.  Can you give some insight on what it is like?  Do you guys all work together out of a source repository?  What is integration like?   When you're building something cool, it's even cooler to test.  I would be super motivated to be more productive so I could do more testing of the PCM96.  Do you find working on products like the pmc96 have a feedback loop like this?  On a side note, I've been looking for a good reason to take a guitar or mic to work for a long time.  


On second thought, I bet you can't actually answer any of these.  Anyhow, I envision that you guys are using a really cool design tool from the dsp manufacturer with some custom in house tweeks or tools, using some cool agile methodologies.  


Sorry to everyone else for geeking out in this thread.

---

### Post #75 -- Page 3
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4062184&postcount=75>

Quote: > Originally Posted byqtuner➡️Nobody Special, CaseyI i'm curious what the tools and environment are like for developing software for the pcm96 and other lexicon products.  Have the tools made it easier for you guys to get software out the door?I've been a professional software developer for nearly thirty years.  It never gets any easier.  The tools get much more powerful, but that simply increases your ambition to do more.  So you end up in a pickle no matter what.


I can't speak for Casey (he's a competitor after all), but I'd wager there are many similarities in the way he works and the way I do.  Your toolkit is always a mix of what's commercially available and what you have to invent.  For proprietary processors like the Lexichip family, you've got to write assemblers and debuggers.  On top of that, there are various sorts of compiler-like tools you must develop.  They're typically only used by a handful of people, so they're seldom polished.  They're usually butt-ugly, to tell you the truth.


If you need to do research, it gets even crazier.  There are commercial tools like Matlab that may be useful, but you're more likely to cobble up some sort of tool on your own.  As you explore more deeply into a problem, the code usually looks worse and worse.  I don't have a clue how many tools I've written that served a purpose and were then abandoned.


Oftentimes you can find free stuff on the web that can be quite helpful.  CSound might be one.  SoundHack is one I've used a lot.  I have both a PC and a Mac in my office, so I'm pretty agnostic about platforms (OK, OK, I like the Mac better).  You can do what you need on either.

Quote: > What challenges have rising requirements complexity, ie plug-in integration, firewire, ethernet, etc posed?They can create real problems and they typically require very special expertise.  Harman has a very strong commitment to networking (our System Architect program can set up an entire stadium from a single laptop), so we're continually building strength in that area.  But integrating all that stuff is really hard.  There are still aspects of the Firewire streaming that we're working on.

Quote: > How many developers are working on the pcm96?Can't really tell you, but it varies quite a lot depending on the phase of a project.

Quote: > I love programming and playing in my studio, and I've always wondered what it would be like to marry the two.That's something you can find out for yourself with the simple commitment of your time.  You can explore the VST API, or AudioUnits or Juce, and play around with plugins, using whatever DAW you like.  There is often source code provided for examples and there are a number of open-source projects you can look at.  If you're curious about the kind of chips we use, you can download a free 90-day evaluation copy of the Analog Devices tools (with a simulator) and play around with your own ideas.  I mentioned SoundHack which is a nice little Mac tool.  Csound is available on any platform and source code is available.


Audio programming requires a mix of skills, not all of them related to audio. The early parts of my engineering career were dedicated to real-time programming and control systems.  I've found ways to make that helpful in DSP.  I'm sure that some of the skills you've developed in business programming will be useful as well.

Quote: > Sorry to everyone else for geeking out in this thread.Heck, we're all nerds here.


NS

---

### Post #76 -- Page 3
**User:** qtuner
**Info:** Joined: May 2005Posts: 720🎧 20 years | Posts: 720
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4062650&postcount=76>

thanks for the detailed reply. I think this is the first time i've had dialogue with an actual DSP engineer.  I got the answer i was really hoping for.....90 day license of analog devices tools.  I've written VST plugs, and wasn't too into it because I write code for PC's all day.  It's not what I want to do in my spare time, and i'm not sure dsp code is either, but I plan on checking out the tools.  Thanks for the direction.  


What are your feelings on convoluton reverb in general as a reverb solution?  I personally suspect that we see convolution a lot in VST's because of its ease of implementation rather than the merits of convolution itself.  


How heavy is the math involved in desiging a reverb?  


In the next 10 years, what areas in effects processing do you think will see the most innovation?  Will we see big advances in algorithms/new algorithms or is effort mostly concentrated on DAW integration?  (I hope not).  I think the latest realtime hardware effect to be  invented is the Access Music atomizer on the Virus TI.

---

### Post #77 -- Page 3
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4063110&postcount=77>

I don't do this for a living, and my effects are not intended for sale, but....


I'm a professional embedded systems programmer, and other than buying Lexicons (PCM60/70/91, LXP15), I build some of my own effects boxes, too. I picked one of the same processors that I use at work (MC9S08AW60) for the host, and since I'm very fast at writing in assembler, I did the host (UI) that way. A little 20x2 VFD, a couple rotary encoders, and a few pushbuttons. My first reverb/effects design started out with two Wavefront AL3201 chips in series. I wrote a new  assembler because Wavefront's did not do what I wanted. I wanted to have the assembler also have parameter numbers embedded in the code, as well as base addresses to allow the host to easily modify the DSP code, and having an automatic link between the UI and the DSP. As for learning how to program those chips, there is some example code out there, and there is the 'infamous' publishing of one reverse-engineered Lexicon algorithm. I tend to write 'effects' rather than reverbs because I have so many of those in my racks that I don't really need to.


A lot of the older reverbs had very short programs, so assembly is nice for that type of platform. The AL3201 is like that, and I've worked a bit with the DSP56300 family. Most of the VLIW DSP's need high-end toolsets, that's why I picked the DSP56k family. Easy to write in assembly, cheap dev tools. That one uses a MCF51AC256 host, a DSP56366, and 512kx24 SRAM. I'm also working on an effect-specific FPGA which should be impressive when I'm done.


IMHO, if you reverse engineer something, it might be ok to learn something from it, but DON'T publish it, and DON'T copy it. The original engineers spent a lot of time designing that algorithm and I'm inclined to give them my money to buy their product. I've done some reverse engineering of various products, it is easy to forget that there are people out there that can take an EPROM and figure out how an engine controller (my day job), or a PCM70, or a KT780, or an obsolete automation system for a mixing console works.

---

### Post #78 -- Page 3
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4063297&postcount=78>

Quote: > Originally Posted byqtuner➡️I've written VST plugs, and wasn't too into it because I write code for PC's all day.  It's not what I want to do in my spare time, and i'm not sure dsp code is either, but I plan on checking out the tools.  Thanks for the direction.Don't be in too big a hurry to ditch VST.  The key to understanding audio programming is understanding what's happening to the samples.  C and C++ are a very nice way to do this.  In addition, it's generally much easier to run with breakpoints on a Mac or PC than on a proprietary chunk of gear.

The real key to writing DSP is to have an understanding of the chip you're running on.  It's about placing things in the right chunk of memory so that your busses are all busy and you're not starving the processor.  SHARCs, Blackfins and TigerSHARCs are nicely tailored to do that sort of thing.  But your plain old PC is pretty powerful too.  If the PC feels too much like work, you could pick up a Mac Mini for $600 (development tools are free).  That might then feel like a "play" machine.
Quote: > What are your feelings on convoluton reverb in general as a reverb solution?  I personally suspect that we see convolution a lot in VST's because of its ease of implementation rather than the merits of convolution itself.Convolution can be very nice and is a useful tool for things other than reverb.  But it always gives you a fixed impulse pattern recorded from point source(s) to point destination(s).  Real reverberation is a little less linear and real performers rarely cluster in a fixed point.  In making a mix, you're generally interested in getting the right sound for a particular instrument or group.  An algorithmic reverb is easy to adjust.  With a convolver, you've got to go looking for another impulse response.

Quote: > How heavy is the math involved in desiging a reverb? It can get a little

hairy way off in the corners, but for the most part it isn't bad at all.

Quote: > In the next 10 years, what areas in effects processing do you think will see the most innovation?Can I answer that question in 10 years?  If I was that good at predicting things, my 401K would still be worth something.


NS

---

### Post #79 -- Page 3
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4064878&postcount=79>

Quote: > Originally Posted byNobody Special➡️The real key to writing DSP is to have an understanding of the chip you're running on.  It's about placing things in the right chunk of memory so that your busses are all busy and you're not starving the processor.  SHARCs, Blackfins and TigerSHARCs are nicely tailored to do that sort of thing.Some SHARCs. Stay away from the 2126x series, up through the 21364. Writing reverbs for these was dreadful, due to the chips having no external memory interface. All external memory interfacing was through a DMA. So, for every sample accessed from external memory, you had to spend about 50 cycles for "waitForPPDMA" or some such subroutine to finish up. The 21369 and later SHARCs restored the memory access pins.

Quote: > But your plain old PC is pretty powerful too.And your plain old PC probably has several MB of cache, which helps get around most of the slow memory problems.

Quote: > Convolution can be very nice and is a useful tool for things other than reverb.  But it always gives you a fixed impulse pattern recorded from point source(s) to point destination(s).  Real reverberation is a little less linear and real performers rarely cluster in a fixed point.  In making a mix, you're generally interested in getting the right sound for a particular instrument or group.  An algorithmic reverb is easy to adjust.  With a convolver, you've got to go looking for another impulse response.You can redesign an impulse response on the fly if it is synthesized, or you can apply amplitude and filter envelopes to an existing response, resample the response, etc. However, it will always be time-invariant, which is not the case for a real room or hall. Plus, convolution is a resource hog compared to an algorithmic reverb running on most machines. I have seen a time-varying convolution algorithm, that cross-fades between different inpulse responses, which seems completely wasteful from a resource perspective. Using 70% of a modern CPU to emulate a reverb that originally ran on a 6 MHz part...


Sean Costello

---

### Post #80 -- Page 3
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4064899&postcount=80>

Cheesy, softball on-thread question for NS and Casey:


What are your FAVORITE Lexicon algorithms of the past 30 years? And why?

---

### Post #81 -- Page 3
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4064905&postcount=81>

Quote: > Originally Posted byqtuner➡️thanks for the detailed reply. I think this is the first time i've had dialogue with an actual DSP engineer.Well, there are at least 6 of them on this page of the thread...

---

### Post #82 -- Page 3
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4065453&postcount=82>

Quote: > Originally Posted byseancostello➡️convolution is a resource hog compared to an algorithmic reverb running on most machines. I have seen a time-varying convolution algorithm, that cross-fades between different inpulse responses, which seems completely wasteful from a resource perspective. Using 70% of a modern CPU to emulate a reverb that originally ran on a 6 MHz part...so why can't someone design a decent reverb plug-in?


hardware is still king in this realm

---

### Post #83 -- Page 3
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4065489&postcount=83>

Quote: > Originally Posted byseancostello➡️Cheesy, softball on-thread question for NS and Casey:What are your FAVORITE Lexicon algorithms of the past 30 years? And why?Sean, I'm probably incapable of answering that honestly, because I don't really know.  David Griesinger's favorite algorithm was always the one he'd most recently worked on, and it's probably a little true for me as well.  He never understood why someone would want to use one of the older algorithms when there was a better solution available.  Of course, if you just mixed a hit record with ConcertHall, why would you want to change? But the choice also depends heavily on the sort of material you're working with.


For pop music, I like RandomHall in both the 480L and PCM96 variants.  But I don't listen to much pop or rock music, to tell you the truth.  Since popular music in its many incarnations was never about recreating a live experience, the modulation of that algorithm adds a pleasant background.


For jazz, I like the 960L or PCM96 Chamber.  Just sounds appropriate, considering the history of jazz recordings.  I like some of the smaller settings of the PCM96 Room for individual instruments or small groups as well.


For classical, which is where my ears spend most of their time, I like the PCM96 Hall. While it's time-variant, its modulation isn't noticeable.  Its initial onset is also just a little less dense than RandomHall, so I think it's easier to slot into a mix.


For post, I really like the room algorithm for its more problematic (and realistic) spaces. This was the result of a long-ago conversation with Tomlinson Holman where he complained that our reverbs were too sweet for ADR.  Of course, the PCM96 is relatively new and has only been on dub stages for a few months, so I'm going to have to talk to some dialog and foley mixers and see if it's really being used that way.


Ask me again in a couple of years and I'll probably have a different answer!

NS

---

### Post #84 -- Page 3
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067013&postcount=84>

Quote: > Originally Posted byseancostello➡️All external memory interfacing was through a DMA. So, for every sample accessed from external memory, you had to spend about 50 cycles for "waitForPPDMA" or some such subroutine to finish up. The 21369 and later SHARCs restored the memory access pins.The Freescale DSP56364 is like that, too. I should have checked the manuals before picking up a couple of them. I also bought some 56366 which does have a real memory bus. The difference is night-and-day in terms of code efficiency.
Quote: > And your plain old PC probably has several MB of cache, which helps get around most of the slow memory problems.This is important with DRAM. Most people just do not believe that today's DDR SDRAM's really don't access memory orders of magnitude faster than DRAM's of two decades ago. They can burst the data out faster, but at random access, they generally aren't that great. But most people can't read and understand a timing diagram. Since I don't worry about cost on a one-off, I just use a 512k by 32 SRAM.
Quote: > Using 70% of a modern CPU to emulate a reverb that originally ran on a 6 MHz part...Sometimes I find it amazing that Windows can't boot in under a minute, where my 40 MHz engine controllers do a full bootup in about 15 milliseconds, and have an interrupt latency of usually two or three microseconds.

---

### Post #85 -- Page 3
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067088&postcount=85>

Quote: > Originally Posted bydale116dot7➡️Most people just do not believe that today's DDR SDRAM's really don't access memory orders of magnitude faster than DRAM's of two decades ago. They can burst the data out faster, but at random access, they generally aren't that great. But most people can't read and understand a timing diagram. Since I don't worry about cost on a one-off, I just use a 512k by 32 SRAM.I have two words for you Dale; Strip Mining.


Todays DDR SDRAMS are much faster than the SRAM you are using. What do you have against burst access?


Nobody Special never really bought into burst access. I don't know why. The PCM96 does not use SDRAM for it's main reverb loops. The PCM96 uses a SHARC with barely enough internal memory to run a pair of Lexicon reverbs. This is a huge limitation on advancing the quality of Lexicons algorithms.


This is either because NS does not understand how to use modern SDRAM, or much more likely, by keeping the memory cycles in the chip, it makes it harder to reverse engineer the algorithms. Neither explaination is a satisfactory reason to limit the capabilities of a high end system IMO.


-Casey

---

### Post #86 -- Page 3
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067121&postcount=86>

Quote: > Originally Posted byCasey➡️I have two words for you Dale; Strip Mining.Todays DDR SDRAMS are much faster than the SRAM you are using. What do you have against burst access?Nobody Special never really bought into burst access. I don't know why. The PCM96 does not use SDRAM for it's main reverb loops. The PCM96 uses a SHARC with barely enough internal memory to run a pair of Lexicon reverbs. This is a huge limitation on advancing the quality of Lexicons algorithms.This is either because NS does not understand how to use modern SDRAM, or much more likely, by keeping the memory cycles in the chip, it makes it harder to reverse engineer the algorithms. Neither explaination is a satisfactory reason to limit the capabilities of a high end system IMO.-CaseyCan't tell you how wrong you are about that Casey, but thanks for the chuckle.  I'm not sure what puts you in a position to know anything about the internals of the PCM96, how it's coded, or what I might know about SDRAM. Why might there be 8 megawords of SDRAM on the PCM96?  How do I manage to run a pair of very high quality reverbs at 96K on a single chip (unlike other boxes which require multiple chips to run a single algorithm)?  I think your mind-reading implant may need a new battery.

---

### Post #87 -- Page 3
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067146&postcount=87>

Quote: > Originally Posted bydale116dot7➡️This is important with DRAM. Most people just do not believe that today's DDR SDRAM's really don't access memory orders of magnitude faster than DRAM's of two decades ago. They can burst the data out faster, but at random access, they generally aren't that great.Dale, you're basically correct here (with a big caveat that I'll get to).  I think Casey missed the point you were making.  I might substitute the word SRAM for your DRAM, but that's a minor point.  SDRAMs (and DDRAMs) are extremely fast when doing contiguous accesses, generally running at full buss speed.  But as soon as you start hopping around (as you might do with a traditionally-coded reverberator) you may easily incur 12-15 wait-states for every access.

Normally SDRAMs are used in systems with decent-sized caches, so you can take advantage of the speed when pulling in a burst (without as much penalty from the random accesses).  Caches on most DSP chips don't quite work as efficiently, so you have to adjust the way you code so you can still get all the goodies.


So if you're working with regular DRAM or static RAM, one memory access is pretty much the same as another.  But those parts are obsolete. SD/DDRAMs are in the sweet spot for cost/performance, so you have to learn to get the most out of them.

---

### Post #88 -- Page 3
**User:** AB3
**Info:** Joined: Feb 2005Posts: 5,807My Studio1 Review written🎧 20 years | Posts: 5,807My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067176&postcount=88>

The PCM 96 sounds great.  It is a great reverb.  I have not tried the M7, but I have not heard anyone complain about the sound of that reverb - it is so unanimous - that I have to assume that it is great.


What is not great is the following: People who represent manufacturers, distributors or dealers arguing about the products of others.  All that goes out of my evaluation or decision-making process when reading posts on this board.   I would advise others to do the same.


There should be a code for posts that are by "plain old consumers" that are not connected with any dealer, distributor or manufacturer.


Now when a dealer, distributor or manufacturer is kind enough (and many are) to answer questions about THEIR OWN products, that is certainly courteous and appropriate.  It is when they discuss the products of others, that I tune out.  And I have to imagine that others do as well.


I do not mean to be judgmental.  These are probably hard times for all manufacturers, distributor and dealers, and I am grateful to all of them for the competition and gear that is produced.

---

### Post #89 -- Page 3
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067225&postcount=89>

Quote: > Originally Posted byAB3➡️What is not great is the following: People who represent manufacturers, distributors or dealers arguing about the products of others.Get off your High Horse AB3. This is a discussion of Lexicon and other reverb architectures. It has become very technical. I commented on the latest Lexicon technology. NS corrected me. Start a Bricasti technology thread and I'll comment on Bricasti technology. If you have the technical chops then chime in. Not everything is a sales pitch.


-Casey

---

### Post #90 -- Page 3
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067245&postcount=90>

Quote: > Originally Posted byAB3➡️Now when a dealer, distributor or manufacturer is kind enough (and many are) to answer questions about THEIR OWN products, that is certainly courteous and appropriate.  It is when they discuss the products of others, that I tune out.  And I have to imagine that others do as well.I'm all for courtesy, especially in forums, where it often falls by the wayside. However, the particular posts above that you are referring to (and I just made a copy of them in case cooler heads prevail and edit their posts) are NOT simply competitors sniping at each other.


What we have here are 2 reverb designers. Each one is the principal architect (I am presuming) of the highest end reverberation processors currently available. The discussion, although it has gotten heated, is not about which processor is better, but about very technical issues regarding the design of such processors. This is not the sort of thread you usually see outside of comp.dsp, and you will never see a discussion this specific outside of boothside arguments at AES, or perhaps in internal company meetings. This is about design philosophy, not sales.


The RAM arguments are fascinating. And very technical. And there are a number of us that are reading every word of this thread eagerly, if for no other reason than it is so rare to be able to talk shop in this very secretive industry.


Sean Costello


---

## Page 4

---

### Post #91 -- Page 4
**User:** AB3
**Info:** Joined: Feb 2005Posts: 5,807My Studio1 Review written🎧 20 years | Posts: 5,807My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067308&postcount=91>

My horse ran away.  Carry on.  And someday I hope to be a proud Bricasti owner. 


Quote: > Originally Posted byCasey➡️Get off your High Horse AB3. This is a discussion of Lexicon and other reverb architectures. It has become very technical. I commented on the latest Lexicon technology. NS corrected me. Start a Bricasti technology thread and I'll comment on Bricasti technology. If you have the technical chops then chime in. Not everything is a sales pitch.-Casey

---

### Post #92 -- Page 4
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067432&postcount=92>

Quote: > Originally Posted byAB3➡️


-Casey

---

### Post #93 -- Page 4
**User:** outofphasePosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067479&postcount=93>

Quote: > Originally Posted byCasey➡️I have two words for you Dale; Strip Mining.Todays DDR SDRAMS are much faster than the SRAM you are using. What do you have against burst access?Nobody Special never really bought into burst access. I don't know why. The PCM96 does not use SDRAM for it's main reverb loops. The PCM96 uses a SHARC with barely enough internal memory to run a pair of Lexicon reverbs. This is a huge limitation on advancing the quality of Lexicons algorithms.This is either because NS does not understand how to use modern SDRAM, or much more likely, by keeping the memory cycles in the chip, it makes it harder to reverse engineer the algorithms. Neither explaination is a satisfactory reason to limit the capabilities of a high end system IMO.-CaseyOUCH

---

### Post #94 -- Page 4
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067502&postcount=94>

WTF just happened here? This thread started off great - incredibly informative - then it took an entirely unnecessary turn and dove off a cliff. It's gone embarrassingly unprofessional and the point has been hijacked.

---

### Post #95 -- Page 4
**User:** qtuner
**Info:** Joined: May 2005Posts: 720🎧 20 years | Posts: 720
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067504&postcount=95>

If there is gonna be a reverb architect showdown, shouldn't you guys record your voices with your best voice of god algorithm, and let us decide the which one sounds the fiercest?  j/k


I'm geeking out on the memory architecture discussion.  Keep it up.  Last I checked great hardware will never make shitty software run better whereas the converse is true.


I don't think the thread is dead.  There is a lot that you can pull out of this information.  We can see that the direction of both the PCM96 and Bricasti M7 have completely different directions of thinking.  This will lead to innovation.  We can clearly see there is strong sense of competition, this is awesome for us.  These guys are going to duke it out with their respective technology, and thats very cool.  Remember with text it is so easy to read oppositie of what is intended and it's even easier to type something that will be taken out of context.  


I'm intentionally trying to ask pointed questions to get these guys to geek out because it reveals so much.  It is obvious these guys are passionate about their development, and engineers who are passionate are typically misinterpreted.  As far as i'm concerned, Lexicon and Bricasti are demonstrating that they're going to be leading the way in the next couple years.  Where is TC?  Where is Eventide?  not here.  I'm in these companies prime demographic, and I'm paying attention.


I'm dying to know what dsp's are in each reverb?  and how they accomplished certain things?  and how things are built, but it is proprietary information, and it's a waste of time to even ask.

---

### Post #96 -- Page 4
**User:** OurDarkness
**Info:** Joined: Feb 2008Posts: 5,060🎧 15 years | Posts: 5,060
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067764&postcount=96>

Quote: > Originally Posted byqtuner➡️As far as i'm concerned, Lexicon and Bricasti are demonstrating that they're going to be leading the way in the next couple years.Leading the way to Reverb technology or FX in general? I hardly think there is a competition between Lexicon or Bricasti and Eventide, for instance. I always thought that Lexicon and Bricasti are primarily reverb-oriented whereas Eventide machines do so much more.

---

### Post #97 -- Page 4
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067896&postcount=97>

Quote: > Originally Posted byOurDarkness➡️I always thought that Lexicon and Bricasti are primarily reverb-oriented whereas Eventide machines do so much more.Did you know the PCM96 also has flange/chorus, various sorts of delay algorithms, resonators and pitch shifters?  While it's certainly true that we don't do the sort of harmonization that Eventide does (we leave that to the Vocalist series of our sister company Digitech), the shifter is still very good for video pulldown corrections or other pitch effects.  One of the shifters in the 96 Surround has 15 independently-shifting voices.  Some of the presets proved to be very upsetting to some of my colleagues.heh


Eventide is very good at what they do, and they've got some good folks working there.  Just wanted to point out that we haven't conceded on the non-reverb effects front.


'OurDarkness' is kind of a scary handle, I must say.

---

### Post #98 -- Page 4
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067929&postcount=98>

I didn't mean to start a flame war... stike
Quote: > Originally Posted byNobody Special➡️Dale, you're basically correct here (with a big caveat that I'll get to)....But as soon as you start hopping around (as you might do with a traditionally-coded reverberator) you may easily incur 12-15 wait-states for every access.That's what I was referring to. Obviously you could code around it, processing whatever effect you wanted to, doing it in chunks, or interleaving the delay lines, or any other number of other ways of doing it. All I said is that for a cost-insensitive one-off of any box I build for myself, I just toss down one (or more) 5ns or maybe 10ns SRAM's - cache memories - so that if I want to code a long digital delay on a sample-by-sample without paying attention to what's in a cache, it costs me the same wait states (one on a DSP56366 - that's the minimum for an external RAM access) regardless of where I go. So if I want to code a multitap delay that mimics what daisy-chaining three dozen Studer tape decks with a single tape loop going through them, that only costs 72 clock cycles, and it doesn't matter that the taps are in very different pages of RAM - or even different RAM chips.
Quote: > Normally SDRAMs are used in systems with decent-sized caches, so you can take advantage of the speed when pulling in a burst (without as much penalty from the random accesses).  Caches on most DSP chips don't quite work as efficiently, so you have to adjust the way you code so you can still get all the goodies.So if you're working with regular DRAM or static RAM, one memory access is pretty much the same as another.  But those parts are obsolete. SD/DDRAMs are in the sweet spot for cost/performance, so you have to learn to get the most out of them.From a hardware point of view, a relatively fast (60ns) obsolete (1994) DRAM access time and write precharge time totals 120ns. Taking a relatively slow SDRAM (166 MHZ SDR - I picked it because have the datasheet right in front of me), a single read or write access takes 60 ns, but you can burst at 6ns, so accessing 11 words takes only twice as long as accessing one. A 35ns EDO RAM also indicates the same 60ns read/precharge time.


This similarity does not surprise me because the column read amplifiers are still an array of analogue comparators and analogue circuit advances tend to motor along at a slow but steady rate. A static RAM also has an array of read amplifiers but the signal strength of the output of a six-transistor SRAM cell is much higher (close to standard digital levels) than that of a single-transistor DRAM. Other single-transistor memory types - EPROM, EEPROM, and FLASH - also tend to have an access time that does not routinely beat 15 or 20ns, where SRAM is routinely available in the sub-2ns region.


I doubt that SRAM will go obsolete any time soon. There are a number of embedded applications that need the reliability, wide temperature range, and steady operation of SRAM. It's just relatively expensive. Also, cache RAM = SRAM.

---

### Post #99 -- Page 4
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067979&postcount=99>

Quote: > Originally Posted bydale116dot7➡️I doubt that SRAM will go obsolete any time soon. There are a number of embedded applications that need the reliability, wide temperature range, and steady operation of SRAM. It's just relatively expensive. Also, cache RAM = SRAM.You're right there of course.  What I meant to say was that from a manufacturer's point of view, SDRAM/DDRAM make much more sense in terms of cost, density, availability and so on.

---

### Post #100 -- Page 4
**User:** Fishmed
**Info:** Joined: Jun 2007Posts: 1,1511 Review written🎧 15 years | Posts: 1,151
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4067982&postcount=100>

Quote: > Originally Posted byNobody Special➡️Did you know the PCM96 also has flange/chorus, various sorts of delay algorithms, resonators and pitch shifters? While it's certainly true that we don't do the sort of harmonization that Eventide does (we leave that to the Vocalist series of our sister company Digitech), the shifter is still very good for video pulldown corrections or other pitch effects. One of the shifters in the 96 Surround has 15 independently-shifting voices. Some of the presets proved to be very upsetting to some of my colleagues.hehEventide is very good at what they do, and they've got some good folks working there. Just wanted to point out that we haven't conceded on the non-reverb effects front.'OurDarkness' is kind of a scary handle, I must say.This may be OT, but why doesn't Harman, shift the "Lower-End" reverb/effects from Lexicon to Digitech? Would that not improve the overall marketing and image of both brands? They could then market Digitech with Lexicon reverb/effects & DBX compression.

---

### Post #101 -- Page 4
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068020&postcount=101>

Quote: > Originally Posted byelambo➡️WTF just happened here? This thread started off great - incredibly informative - then it took an entirely unnecessary turn and dove off a cliff. It's gone embarrassingly unprofessional and the point has been hijacked.casey makes the best digital reverb i've ever heard... so i accept his word as AUTHORITY until someone makes a better one.

---

### Post #102 -- Page 4
**User:** AB3
**Info:** Joined: Feb 2005Posts: 5,807My Studio1 Review written🎧 20 years | Posts: 5,807My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068055&postcount=102>

Lots of people I trust think the Bricasti is the best.   And I would LOVE to have one ASAP!


And that deserves its own thread (of which there probably already are some.)


Read the original post again and please tell me what this thread is about?


And this is not meant as anything against Casey from Bricasti.  I have read enough of his posts to where I see him being fair about his competitors, in many ways that a couple of others on GS have not been.  So he is obviously a good guy.


But still - what is this topic as related to the first post???   And does that ever really matter on this board??? heh


Quote: > Originally Posted by11413➡️casey makes the best digital reverb i've ever heard... so i accept his word as AUTHORITY until someone makes a better one.

---

### Post #103 -- Page 4
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068060&postcount=103>

Quote: > Originally Posted byNobody Special➡️Can't tell you how wrong you are about that Casey, but thanks for the chuckle.Yes alright, I assumed and made an ass of myself.


Reading through some of your earlier posts, I came away with the the sense that you were using the internal RAM to run your entire loop. The large TigerSHARC surprisingly does have enough memory to do it.


Sorry everybody for the unprofessional comments that were clearly based on my incorrect assumption. tutt


-Casey

---

### Post #104 -- Page 4
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068067&postcount=104>

Quote: > Originally Posted byCasey➡️Yes alright, I assumed and made an ass of myself. ... Sorry everybody for the unprofessional comments that were clearly based on my incorrect assumption. tuttyou're forgiven, provided you release v2 for the M7 sometime in 2009

---

### Post #105 -- Page 4
**User:** AB3
**Info:** Joined: Feb 2005Posts: 5,807My Studio1 Review written🎧 20 years | Posts: 5,807My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068079&postcount=105>

Casey - humility is a great human quality and sometimes lacking on GS.    


You are a class act in my book.   It only makes me want to get your product even more.

---

### Post #106 -- Page 4
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068138&postcount=106>

Quote: > Originally Posted byAB3➡️humility is a great human quality.Yes, but it's never an excuse for poor performance!


I think I'll go back to the safe softball question;


My favorite Lex algorithm was Davids last reverb on the 480 that I am aware of. He developed the Surround (or HD for stereo) algorithm that used the entire 480.


I really like it's chorusing in both the very unique earlies and in the reverb itself. Of course David would kill me for saying that as he considers these to be undesirable artifacts. It also has this really interesting modulating lowend that actually sounds kind of bad on it's own, but really sounds great on the right source and in a mix.


-Casey

---

### Post #107 -- Page 4
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068396&postcount=107>

Quote: > Originally Posted byNobody Special➡️So if you're working with regular DRAM or static RAM, one memory access is pretty much the same as another.  But those parts are obsolete. SD/DDRAMs are in the sweet spot for cost/performance, so you have to learn to get the most out of them.Techie Lexi question: Were there any problems adapting any of the older algorithms (480L, Concert Hall) to work with modern RAM/DSP/cache-based system designs? 


Another techie question: How much of the memory for the PCM96 is managed manually, versus handled by the compiler?


Sean Costello

---

### Post #108 -- Page 4
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068412&postcount=108>

Quote: > Originally Posted by11413➡️casey makes the best digital reverb i've ever heard... so i accept his word as AUTHORITY until someone makes a better one.Be careful how much blind trust you put in your authorities... From Casey:


"Reading through some of your earlier posts, I came away with the the sense that you were using the internal RAM to run your entire loop. The large TigerSHARC surprisingly does have enough memory to do it."


Casey's brain is filled with some of the most relevant data about reverb, and he's the man when it comes to the Bricasti, but, as he himself has now admitted, he doesn't (yet) know everything about the 96.

---

### Post #109 -- Page 4
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068426&postcount=109>

Quote: > Originally Posted byCasey➡️Sorry everybody for the unprofessional comments that were clearly based on my incorrect assumption. tuttIf I had a nickel for every time I made a false assumption and posted something about it... well, I'd need a big coin jar.


No sweat Casey. Cool of you to mention it. You're still the man.

---

### Post #110 -- Page 4
**User:** OurDarkness
**Info:** Joined: Feb 2008Posts: 5,060🎧 15 years | Posts: 5,060
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068435&postcount=110>

Quote: > Originally Posted byNobody Special➡️Did you know the PCM96 also has flange/chorus, various sorts of delay algorithms, resonators and pitch shifters?  While it's certainly true that we don't do the sort of harmonization that Eventide does (we leave that to the Vocalist series of our sister company Digitech), the shifter is still very good for video pulldown corrections or other pitch effects.  One of the shifters in the 96 Surround has 15 independently-shifting voices.  Some of the presets proved to be very upsetting to some of my colleagues.hehEventide is very good at what they do, and they've got some good folks working there.  Just wanted to point out that we haven't conceded on the non-reverb effects front.'OurDarkness' is kind of a scary handle, I must say.Hi NobodySpecial,


good to know that the PCM96 has some extra goodies in it. To be honest, I didn't know it had any of the stuff you mentioned - as far as I am concerned they are good to be around in case someone needs them. 


Could you explain a little if you can do various kind of routings between these presets? Can you mention a very heavy DSP-wise chain? I will be buying a new reverb in the not too-distant feature so I have my eye on both the Lexicon and the Bricasti. I asked in another thread for the kind of difference between the reverbs of Bricasti and Lexicon compared to the ones in the Eventide H-8000 FW and TC Electronic M-3000 and didn't get a very satisfactory answer. I think I am going to have to toss a coin since it's difficult to me to audition these units without buying them first...


Anyway, my nickname is one of the best electro tracks I have ever heard. Check this out:

[YouTube - Anne Clark - Our Darkness (1984) (Remix)](https://www.youtube.com/watch?v=ZHANw73GUxE)


Not scary after all, eh?

---

### Post #111 -- Page 4
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068562&postcount=111>

Quote: > Originally Posted byOurDarkness➡️Hi NobodySpecial,Could you explain a little if you can do various kind of routings between these presets? Can you mention a very heavy DSP-wise chain? ...I asked in another thread for the kind of difference between the reverbs of Bricasti and Lexicon compared to the ones in the Eventide H-8000 FW and TC Electronic M-3000 and didn't get a very satisfactory answer.DSP routing depends in large part on whether you're running as a plugin or standalone. For plugin, the routing is dependent on how you structure your effects inserts. If you've got stereo strips, then you can instantiate two plugins with any algorithm you like in either one. Or you could pop someone else's plugin into that same signal flow.


If you're running standalone, then we give you several system configurations to choose from. For example, the stereo cascade gives you two stereo machines. Input comes from your desk to one machine, is processed and internally routed into the other machine for more processing, and then comes back to your desk. You can put any algorithm you want in either machine. The PCM96 ships with several of these system-level presets. For example, there are several nifty reverb->flange arrangements. If I remember correctly, I put in a couple of verb->pitch-shifter presets (*not* for use right after eating). You can create and save your own as well.


We don't currently have algorithms with a deeper level of internal routing as you might have found in the MPX-1. What we have is a little simpler to understand but still quite powerful.


Now to your question concerning the difference between reverbs in TC, Eventide, Bricasti and Lex. The nature of a forum like this means that there's always going to be some bias in descriptions. People tend to prefer whatever they just dropped a chunk of money on. And of course we don't really have a very good descriptive language anyway. If someone's interest is in metal, then they're going to be tuned into different things than someone mixing choirs. Every product you've mentioned has some real strengths, but they may not be in the areas most important to you. Ideally you'd be able to grab something from a rental house and spend a couple of weeks with it before deciding. I'd be delighted if you took home a new PCM96. But I think it best if I let Casey answer questions specific to Bricasti and reps/users of TC/Eventide talk about their products. And I'll try to help with the Lex stuff.

---

### Post #112 -- Page 4
**User:** OurDarkness
**Info:** Joined: Feb 2008Posts: 5,060🎧 15 years | Posts: 5,060
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4068634&postcount=112>

Quote: > Originally Posted byNobody Special➡️DSP routing depends in large part on whether you're running as a plugin or standalone. For plugin, the routing is dependent on how you structure your effects inserts. If you've got stereo strips, then you can instantiate two plugins with any algorithm you like in either one. Or you could pop someone else's plugin into that same signal flow.If you're running standalone, then we give you several system configurations to choose from. For example, the stereo cascade gives you two stereo machines. Input comes from your desk to one machine, is processed and internally routed into the other machine for more processing, and then comes back to your desk. You can put any algorithm you want in either machine. The PCM96 ships with several of these system-level presets. For example, there are several nifty reverb->flange arrangements. If I remember correctly, I put in a couple of verb->pitch-shifter presets (notfor use right after eating). You can create and save your own as well.We don't currently have algorithms with a deeper level of internal routing as you might have found in the MPX-1. What we have is a little simpler to understand but still quite powerful.Now to your question concerning the difference between reverbs in TC, Eventide, Bricasti and Lex. The nature of a forum like this means that there's always going to be some bias in descriptions. People tend to prefer whatever they just dropped a chunk of money on. And of course we don't really have a very good descriptive language anyway. If someone's interest is in metal, then they're going to be tuned into different things than someone mixing choirs. Every product you've mentioned has some real strengths, but they may not be in the areas most important to you. Ideally you'd be able to grab something from a rental house and spend a couple of weeks with it before deciding. I'd be delighted if you took home a new PCM96. But I think it best if I let Casey answer questions specific to Bricasti and reps/users of TC/Eventide talk about their products. And I'll try to help with the Lex stuff.Thanks for the detailed answer NS!

---

### Post #113 -- Page 4
**User:** aeonlux
**Info:** Joined: Aug 2007Posts: 732🎧 15 years | Posts: 732
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4070077&postcount=113>

Thanks so much for the discussion and information provided here in this thread. I have learned things, and in so doing, enjoyed it.


I have a number of reverb devices, and my two Lexicon NuVerbs, PCM-81, and LXP-15II rank highly among them.


The NuVerbs in particular achieve a sound for ambient electronic music that little else can, in my experience.


My other main reverb tools include an Eventide H8000FW, two Kurzweil KSP8s, t.c. electronic M3000, Sony DPS-V77, Roland SRV-330, and Roland RSS-303.


I hope to have a Bricasti M7 be among them at some point.


Algorithmic reverb rules! 


cheers,

Ian

---

### Post #114 -- Page 4
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4070107&postcount=114>

Quote: > Originally Posted byaeonlux➡️Algorithmic reverb rules!cheers,Ian


-Casey

---

### Post #115 -- Page 4
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4070306&postcount=115>

I agree. Convolution is excellent when you need a chameleon which can cover a slew of styles, but it never covers them excellently. The best IRs are still only "very good" - not on the level of the algorithmic reverbs we're talking about. The longer their tails trail off the more you recognize their artificiality.

---

### Post #116 -- Page 4
**User:** prism
**Info:** Joined: Mar 2009Posts: 36🎧 15 years | Posts: 36
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4071161&postcount=116>

how do you find the ksp8 next to the h8000 ? are imagined these would be very similiar in character ? ( clean and  ' nu ' abd crystal clear ) I have looked at the ksp8 a bit but i always worried it would bea  bit to similiar to the h8000 - ?


Lexicon wise i still love my old lxp5  - with soundiver its superb and great fun to edit.


>My other main reverb tools include an Eventide H8000FW, two Kurzweil >KSP8s, t.c. electronic M3000, Sony DPS-V77, Roland SRV-330, and Roland

---

### Post #117 -- Page 4
**User:** prism
**Info:** Joined: Mar 2009Posts: 36🎧 15 years | Posts: 36
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4071164&postcount=117>

convolution ?


i will say these impulses below are superb though some days though not as good as the real machines but i dont think the average listener could hear the difference.


[Untitled Document](http://music.hyperreal.org/artists/ishq/vsynthesis/products/h8000.html)

[Untitled Document](http://music.hyperreal.org/artists/ishq/vsynthesis/products/h3000.html)

[Untitled Document](http://music.hyperreal.org/artists/ishq/vsynthesis/products/Kyma.html)


Quote: > Originally Posted byelambo➡️I agree. Convolution is excellent when you need a chameleon which can cover a slew of styles, but it never covers them excellently. The best IRs are still only "very good" - not on the level of the algorithmic reverbs we're talking about. The longer their tails trail off the more you recognize their artificiality.

---

### Post #118 -- Page 4
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4072319&postcount=118>

Here's a list of the algorithms described so far, as well as an attempt to match algorithms to Lexicon units. Feel free to add on to this list, or suggest other boxes that use the listed algorithms.


Concert Hall: 224, 224X/XL, PCM70, PCM91 with additions (according to Casey), PCM96. Was this in the 200 as well?


Random Hall: 480L, 300, PCM90/91, PCM96


"New" Hall: 480L, PCM90/91, 300, LXP1, LXP15, Reflex, Alex, Lexiverb. Is this similar to the "dense" algorithm that Warp69 mentioned?


Blesser Hall: PCM96. I know this isn't the name, but this is to differentiate the algorithm from earlier Hall algorithms.


Surround Hall: 480L w/Surround Cart. Based on Random Hall.


Plate: 224


Small Plate: 224X/XL


Constant Density Plates: 224X/XL


Rich Plate: 224X/XL, probably every Lexicon that came afterwards


Room: PCM96

Earlier rooms used Hall-esque algorithms, or algorithms closer to the Chamber algorithm


Chamber: 224X/XL


Rich Chamber: 224X/XL

Were the later chambers closer to the Rich Chamber algorithm?


Ambience: 300, PCM91 (I might be missing some)


Inverse: PCM70, PCM91, probably others


Infinite: I haven't seen this mentioned yet, but it usually appears as a variant on the Chamber algorithm.


General changes over time: 


Early modulation was chorusing (in the Concert Hall). Later modulation was something else.

Shape/Spread parameters introduced (or added to interface) in 480L, used in all later Lexicon units


Two more questions:


- Are the reverb algorithms in the PCM80 closer to the 224XL/PCM70 era, the 480L era, or some mixture of both? The Concert Hall description sounds like the PCM70, while other algorithms have Spin, Shape and Spread, much like the 480L and later units.


- Would the reverb algorithms in the PCM80 be close to some of the simpler algorithms in the PCM91 - I forget their name, but the ones that are designed to be run in parallel?


Thanks, 


Sean Costello

---

### Post #119 -- Page 4
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4072390&postcount=119>

Quote: > Originally Posted byseancostello➡️Here's a list of the algorithms described so far, as well as an attempt to match algorithms to Lexicon units.Wow, that's some list. I think the main thing to keep in mind is that in most cases these algorithms varied more or less from machine to machine. Just a couple of comments:


Concert Hall: PCM91 with additions (different enough to be it's own alg), Was this in the 200 as well (yes)


Random Hall: PCM90/91 (Not in the same sense as 300/480 random hall)


"New" Hall: Is this similar to the "dense" algorithm that Warp69 mentioned? (No)


Surround Hall: 480L w/Surround Cart. Based on Random Hall. (Not really based on random hall, this is the "dense" algorithm mentioned by Warp69)


-Casey

---

### Post #120 -- Page 4
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4072497&postcount=120>

Quote: > Originally Posted byCasey➡️Random Hall: PCM90/91 (Not in the same sense as 300/480 random hall)Different principle, or just simpler than the 300/480 Random Hall? Is the randomization type the same?

Quote: > Surround Hall: 480L w/Surround Cart. Based on Random Hall. (Not really based on random hall, this is the "dense" algorithm mentioned by Warp69)Does this use Random Hall type randomization?


I really need to HEAR a good example of Random Hall one of these days - I keep looking for Lexicon bargains in the local Craigslist, but have only managed to find an LXP15. Are there any good sound files out there where I can hear Random Hall in action? Preferably with the settings turned up too high.


Thanks,


Sean Costello


---

## Page 5

---

### Post #121 -- Page 5
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4072522&postcount=121>

Quote: > Originally Posted byseancostello➡️Different principle, or just simpler than the 300/480 Random Hall? Is the randomization type the same?Does this use Random Hall type randomization?I'm sorry Sean, but that is beyond what I can say.

Quote: > Originally Posted byseancostello➡️I really need to HEAR a good example of Random Hall one of these days - I keep looking for Lexicon bargains in the local Craigslist, but have only managed to find an LXP15. Are there any good sound files out there where I can hear Random Hall in action? Preferably with the settings turned up too high.Thanks,Sean CostelloDidn't NS post an example of the PCM96 random hall a while back?


-Casey

---

### Post #122 -- Page 5
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4072650&postcount=122>

Quote: > Originally Posted byseancostello➡️Here's a list of the algorithms described so far, as well as an attempt to match algorithms to Lexicon units. Feel free to add on to this list, or suggest other boxes that use the listed algorithms.As Casey pointed out - the algorithms varies more or less between the machines and sometime they're very different, but they usually use the same principles.


Concert Hall : 224(X/XL), PCM90/91, 480L (Classic card)

Random Hall : PCM90/91, 480L

6 Voices/Dense : 480L (the first algorithm available for the 480L)

Surround/HD : 480L (Surround/HD card)

Rich Plate : 224(X/XL), PCM90/91, 480L (Classic card)

(Random) Ambience : PCM90/91, 480L


224(X/XL) : Small Plate, Constant Density A/B, Room, Chamber............ etc

PCM90/91 : Room, Chamber, Inverse

480L : FX


Regarding shape/spread : Some of the 224(X/XL) algorithms have Attack as a parameter - more or less the same as Shape.

---

### Post #123 -- Page 5
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4073153&postcount=123>

Sean, that's quite a novel! A few additions.
Quote: > Originally Posted byseancostello➡️Concert Hall: 224, 224X/XL, PCM70, PCM91 with additions (according to Casey), PCM96. Was this in the 200 as well?4-and 5-channel versions in the PCM96 Surround. Don't know about the 200.


Quote: > Random Hall: 480L, 300, PCM90/91, PCM96960L


Quote: > Blesser Hall: PCM96. I know this isn't the name, but this is to differentiate the algorithm from earlier Hall algorithms.Also 4-and 5-channel versions in the PCM96 Surround.


Quote: > Surround Hall: 480L w/Surround Cart. Based on Random Hall.4-and 5-channel versions in the 960L and PCM96 Surround. Not the same as in the 480L.


Quote: > Rich Plate: 224X/XL, probably every Lexicon that came afterwards4-and 5-channel versions in the 960L and PCM96 Surround.


Quote: > Room: PCM964-and 5-channel versions in the 960L and PCM96 Surround.


Quote: > Rich Chamber: 224X/XLWere the later chambers closer to the Rich Chamber algorithm?There's a new Chamber (a little denser and less colored) in the 960L, PCM96 and PCM96 Surround. The 960L and 96 Surround have 4/5 channel surround versions.


Quote: > Ambience: 300, PCM91 (I might be missing some)960L in stereo, 4 and 5 channel. In addition, the ambience reflection pattern is also included in the PCM96 (4-5 channel versions in the 96 Surround).


Quote: > Inverse: PCM70, PCM91, probably othersRather than recode inverse (which was essentially a cheap hall with a truncated reverb loop), we added a reverse parameter to the PCM96 room algorithm. Any of the room patterns can be reversed.  In addition, any of the 960L or PCM96 reverbs (excepting ConcertHall) can be made to do something very similar by setting TapSlope to Max, driving MidRT all the way down, and using high values for Shape and Spread.  Tweaky or what?


Quote: > Infinite: I haven't seen this mentioned yet, but it usually appears as a variant on the Chamber algorithm.With the exception of ConcertHall, all reverbs in the PCM96 have an infinite parameter which works the same way.


Quote: > Are the reverb algorithms in the PCM80 closer to the 224XL/PCM70 era, the 480L era, or some mixture of both? The Concert Hall description sounds like the PCM70, while other algorithms have Spin, Shape and Spread, much like the 480L and later units.Essentially correct. Barry Blesser changed a few aspects of some reverbs in the PCM80.


Quote: > Would the reverb algorithms in the PCM80 be close to some of the simpler algorithms in the PCM91 - I forget their name, but the ones that are designed to be run in parallel?Yep. As in the PCM80/81 those algorithms had to be squeezed into a single Lexichip2, so they don't sound as rich as the full PCM90/91 algs.

Thanks for adding new beasts to the bestiary.

---

### Post #124 -- Page 5
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4073309&postcount=124>

Quote: > Originally Posted byNobody Special➡️Sean, that's quite a novel!Thanks for adding new beasts to the bestiary.Your novel, your beasts. I was the typist.


Did Barry Blesser officially work for Lexicon, or was he a consultant? Or pal?


Thanks for all the info on this subject.


Sean

---

### Post #125 -- Page 5
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4073474&postcount=125>

Quote: > Originally Posted byseancostello➡️Did Barry Blesser officially work for Lexicon, or was he a consultant? Or pal?Barry's been all of those things.  He was one of the first employees, writing the software for the Delta-T 101.  He came back in for a year or two and served as the project manager for the PCM80 back in the early nineties.  Since then he's consulted once or twice, but has been a good sounding board the whole time.


If you're listing designers, you need to add a few (and I'm sure I'm missing a couple):- Jim MacArthur - instrumental in the MPX-1 and Vortex (a truly strange box)
- Frank Cunningham - a lot of work on the LXPs, 300 and 480.
- Jim Muller - MPX 100-550, as well as the automatic EQ that's in Lex receivers and JBL speakers.
- Tom Hegg - EQs and more in Opus.
- Gary Hall - PCM41-42


As you can see Dave G was the public face for a long time, but there have been a lot of very sharp people who've been part of building the brand.

---

### Post #126 -- Page 5
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4073578&postcount=126>

To my ears, the PCM70 hall sounds quite a bit different, maybe even a bit ringy, compared to the halls in the PCM91. I would guess they're quite a bit different inside based on the difference in sound. Most other reverbs across the PCM70 and the PCM91 and the PCM80 sound similar to my ears. The 91 sounds more refined, though. I rather like 'Vocal Magic', my 91 hardly strays from that preset.


I was looking more carefully at SDRAM timing. I missed a key feature. You could efficiently run a 'traditional' reverb coding method (sample-by-sample) by having four parallel threads and interleaving the memory accesses between banks - and interleaving the algorithms.

---

### Post #127 -- Page 5
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4073925&postcount=127>

Quote: > Originally Posted bydale116dot7➡️I was looking more carefully at SDRAM timing. I missed a key feature. You could efficiently run a 'traditional' reverb coding method (sample-by-sample) by having four parallel threads and interleaving the memory accesses between banks - and interleaving the algorithms.You are of course right. If your product ran 4 "machines" this would work great. But I'm not clear on why burst accesses are anathema to you. It is after all the way SDRAM was designed to work. Why not go with the flow?


Maybe these discussions would be better moved to the geekslutz forum? I never see any general reverb technology discussions there, and yet some of the questions on this thread seem to run in that direction. It would be much easier to discuss technology in general terms on a technology thread as opposed to a commercial thread. There does seem to be a reverb subculture here that would be interested. Start one up!


-Casey

---

### Post #128 -- Page 5
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4073942&postcount=128>

Quote: > Originally Posted byseancostello➡️Did Barry Blesser officially work for Lexicon, or was he a consultant? Or pal?Buy his book, it's a great read.


-Casey

---

### Post #129 -- Page 5
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4074019&postcount=129>

Quote: > Originally Posted byCasey➡️Maybe these discussions would be better moved to the geekslutz forum?Yes, please! This is a great "bestiary" for Lexicon, and for the history of reverb in general, but some of the coding and SDRAM discussions seem like mental hurdles for the original topic. Or maybe I'm just simple.

---

### Post #130 -- Page 5
**User:** Hysteria
**Info:** Joined: Jan 2005Posts: 357🎧 20 years | Posts: 357
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4074846&postcount=130>

This is a wonderful thread! I've been wondering about what algs were used in what devices (etc)for a long time and read many people's thoughts on what has what but never felt they were in a position to really know. 


Couple of extra questions:


What about the MPX1. Does it have the 80/81 algs or something different. Presumably the Lexichip 2 is the same device in both units...?


Fellow Harmon company, Digitech is using Lexicon reverbs on its recent (and maybe not so recent) products. How might say the reverb in one of its guitar processors (such as GSP 1101) compare to those in the MPX/PCM ranges? 


Is it a totally different alg? How much processing power would the AudioDNA2 (is that what Digitech calls its custom chips?) bring to bear on such an alg.


I ask as I've owned a PCM91/MPX1 and the GSP and I find the GSP Lexicon algs (halls expecially) to be subjectively surprisingly 'lush'.


When the MPX x00 line came out, I remember reviews comparing say the MPX500 to the MPX1 and citing sonic differences in favour of the MPX1.  I wondered at the time if Lexicon would have bothered re-engineering algs to be subtly different for between say the MPX1, 500, 550. After all, if you already have an alg that's in the right ballpark I would imagine it being most cost-effective to say 'just use the MPX1 alg in those new devices'


thanks again guys!


Simon

---

### Post #131 -- Page 5
**User:** Acousticas
**Info:** Joined: Oct 2008Posts: 130🎧 15 years | Posts: 130
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075538&postcount=131>

Quote: > Originally Posted byNobody Special➡️Convolution can be very nice and is a useful tool for things other than reverb.I am a little bewildered by the fact that an industry leader, such as yourself, with extensive knowledge of reverberation, would make such a comment about the convolution technology.


A person of your caliber, surely, is capable of distinguishing the advantages which convolution technology has over

"algorithmic  technology" and vice versa.


The purpose of any reverberator is to simulate "space".

The "sound" of a "space" is something that "man" created by designing architectural constructs or should I say "containers",

in which, people may seek shelter from the forces of nature. One could argue, that "man" did not create the forrest or the mountains which also yield multiple echoes which translates into what we refer to as "space".


Be that as it may, the fact remains that human beings find the atmospheric echoes of a "container" or room to be pleasant and given the fact, that most people prefer the sound of a symphony orchestra recorded in an orchestra hall, over the symphony orchestra recorded on a large poppy field with no forrest or mountain vicinity, warrants the development of:


1) The construction of a designed "container" or venue, yielding "space" = "Natural" Reverberator

2) Convolution reverb using an Impulse Response or "captured recording" derived from any venue  = "Natural" Reverberator

3) Algorithmic Reverberators, producing a series of distance-varying reflections (echoes) and/or modulation based on advanced algorithms = Artificial Reverberator.


Artificial or Natural, both are merely words representing a meaning which in this case is not meant to be good or bad.


**"Natural" Reverberation**


Placing single or multiple sound generators, typically speaker(s), inside the venue enables the user to "bus" or place, his source of sound into that venue.

The result is captured, live, by single or multiple microphones which are bussed into the signal chain.

Disregarding the fact that speakers and microphones, vary in quality and linearity, this approach is the closest that one can get to "placing" a sound source, recorded elsewhere, into a "foreign" real-world construction.


An impulse response, derived from the example above, enables its user to "apply" the exact* same "space",

using a convolution reverb


* In todays processor-realm, this would only be possible with off-line** application calculation, at least if the application(Plug-in) is considering more than 12 or 24 analyzation bands.

Todays convolution plug-ins have to find compromises for accuracy versus cpu efficiency and instantiation counts.

The quality of today's online convolution is however, great, although mathematically it could be better. Whether one is capable of hearing the difference, is a very different question. An analogy could be 48khz versus 96khz. Theoretically, latter is better but there are many claiming they cannot hear the difference. 

But as the processing power rises, so does the accuracy(bands of analyzation) of "online***" convolution reverbs.


** Offline analogy = Digidesign - Audio Suite

*** Online analogy = Digidesign - RTAS


Advantages of Natural and Convolution Reverberators are that they yield the information, or acoustical "finger print" which the actual venue produces once excitation occurs.

Those "finger prints" contain every little detail such as; beads, fillets, boarders, walls, ceiling, floor, furniture, screws, door-handles, lamps etc etc etc... All which consist of different materials and thus reflection-capabilities. Spending years within such a single construct or venue, would still make it impossible for an algorithmic reverb programmer to re-create all its aspects and reflection-sources.


The "disadvantage" of natural reverberation, is that the given construct is only capable of yielding "one" "result". One could, of course, alter the interior decoration or place objects inside of it to modify its reflection capability but that is connected with a large and often financial effort and is very, relationally, time consuming. Still, such effort would not be able to completely re-design the "result" of the construct, i.e a wooden room would never be able to yield the sound of a large church. So if natural reverberation is an instinct and obsession that one possesses, one would have to commence with the construction of a church in his backyard, unless he changed his mind and purchased an algorithmic reverberator. 

**Algorithmic Reverberator**


Algorithmic Reverberators respond with with an algorithm which generates as many reflections (echoes) and/or "modulations" as the algorithm dictates, once any given source has caused its excitation. Depending on manufacturer and device, the user has control over various parameters which are interacting with the algorithm(s).

Depending on the supplied algorithms, the algorithmic reverb is capable of changing sound, instantly. Meaning, that its user can, apply to his source, instantly and again depending on device and algorithm, any given construct that "man" can imagine, by the turn of a wheel or knob. That is the great advantage of the algorithmic reverberator, which compared to a "natural" reverberator is a "sound chameleon".


The "disadvantage" of of the Algorithmic Reverberator is its incapability of, accurately, recreating a real venue and all its interior, gadgets, furniture, non-symmetrical walls and ceiling, material and even flaws. Even the slightest "bend" or curve in a wall or different material used in/on those, will cause the reflection of the sound wave to behave differently and ultimately alter the "sound". 


We have, recently, entered into the process of making our own convolution and algorithmic reverbs, and find that, both "styles" of achieving reverberation are warranted and/or needed in the recreation of "space" for recorded material.

Both have their share of pros and cons.


I believe that it is irresponsible, of any industry leader in this field, to communicate to his audience, that either of above mentioned "styles" of reproducing "space", is unnecessary or "inferior" to the other, in oder to falsely advance his own choice of technology and thus ultimately his sales(s).


It seems that a "feud" exists, between those who prefer algorithmic over convolution reverberation technology and vice versa. A "feud" which in my opinion is totally unwarranted, as both technologies are capable of producing wonderful results and are here to stay and more importantly, here to advance and maybe even benefit from one another.


Simply using convolution technology for "measurement purposes" and disregarding it for reverberation, would be like buying a Lamborghini Diablo and never exceeding a speed of 20 mph.


Additionally, I would like to add that I find the Algorithmic Reverberator-hardware-manufacturer's hostility towards the Algorithmic Reverberator-PlugIn-manufacturer totally unwarranted and uncalled for.

Both cook with the same ingredients; water, as they both use software to communicate with hardware.

The programmer with the best ear for great sound will/should prevail.


**Does the new Raw Processing-Power-Capabilities equal great sound.**


Lexicon(Prior to 960) and EMT-Frantz are legends in reverberation and both generated and still generates wonderful results using technology, which today fits into a "*Pocket Calculator*" and still made history. Even today, with superior processing power, more advanced than what the EMT or Lexicon programmers, back then, had dared daydreaming about, algorithmic reverberation manufacturers are still chasing the tails (some their own tail) of those legends.


Does algorithmic reverberation sound better today, with the new technology? IMO, absolutely not. And that goes to show that RAW processing power has nothing to do with great sound.


You may well argue, that Acousticas is merely a company, ripping off other people's inventions and have no idea of reverberation, what so ever. Up until this point in time, all we offer, are impulse response libraries of what we refer to as legends.

Reason for that endeavor was simply that, lately, it has become extremely difficult if not impossible to actually repair those legends as the parts simply dont exist anymore. So getting them inside of the DAW, call it archival, in high and unmistakably quality, was of high priority to us. A nice "side Effect", of course, was the possibility of multiple instantiations of the devices granted by a convolution reverb.


Surely, if one would want to derive impulses from every single Lexicon parameter, he would have to conduct more than a million measurements. Which is impossible. However, what one can do with convolution technology, is to "record" and thus achieve eternalization of a particular setting of the device in question. And that is what we have done. And the tails of our impulses are not governed by artifacts, suggested numerous times, in many threads, on this very forum. 


What everyone strives to achieve in one's mix, is a great sound with a great atmosphere.

Does it really matter whether one accomplishes that with an algorithmic or convolved result, as long as one accomplishes.

And is it really necessary for makers of algorithmic and convolution reverberators to undermine and battle each other ?

---

### Post #132 -- Page 5
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075701&postcount=132>

Quote: > Originally Posted byAcousticas➡️I am a little bewildered by the fact that an industry leader, such as yourself, with extensive knowledge of reverberation, would make such a comment about the convolution technology.I guess you'll remain a little bewildered then. A convolver is no more a representation of a *real* space than an algorithmic reverb is. It's an accurate represention of an impulse reponse from a speaker or two to a single listener position. As I said before, a real orchestra is spread out in space. So is the audience. The impulse response from the second clarinet to seat 7C is different than the impulse response from the *first* clarinet to the same seat. A convolver effectively squishes the entire orchestra into a couple of points, quite accurately mimicking descent into a black hole.


On top of all that, you simply don't hear every single reflection in a hall. That's not the way the auditory cortex works. You may hear discrete reflections for a few tens of milliseconds, but after that, reverberation becomes a frequency effect (with interaural phase differences being quite important). If you do that part well, the listener is satisfied.


I didn't say that convolvers were bad. Sometimes they sound very nice. But to somehow say that they are natural and algorithmic reverbs are artificial shows a little too much susceptibility to marketing. News flash: They are *both *artificial.

---

### Post #133 -- Page 5
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075748&postcount=133>

Quote: > Originally Posted byHysteria➡️What about the MPX1. Does it have the 80/81 algs or something different. Presumably the Lexichip 2 is the same device in both units...?Yes, it's the Lexichip 2. The delay and modulation processing takes place on an old Analog Devices part. Audio is shipped over to the reverberator for processing and then back to the ADI part. The reverbs are similar to those in the PCM80/81 but without randomization.

Quote: > How might say the reverb in one of its guitar processors (such as GSP 1101) compare to those in the MPX/PCM ranges?You know I really ought to listen to those pieces, but I tend to think that electric guitar reached its zenith with an L5 through a Twin Reverb. I think that the Digitech/Lex verbs are much closer to the Pantheon plugin that goes along with some of our I/O boxes.

Quote: > How much processing power would the AudioDNA2 (is that what Digitech calls its custom chips?) bring to bear on such an alg.The DNA chips are pretty decent for low-cost reverbs. They're actually more powerful than the Lexichips were.

Quote: > I wondered at the time if Lexicon would have bothered re-engineering algs to be subtly different for between say the MPX1, 500, 550.Sometimes the algorithms are different because they DSP designer preferred a slight change (Dave G often disagreed with himself) . Sometimes it's necessary because the new target chip can't quite do it the same way, so you have to make adjustments. It's fun to listen to users when they discuss these differences.

---

### Post #134 -- Page 5
**User:** Acousticas
**Info:** Joined: Oct 2008Posts: 130🎧 15 years | Posts: 130
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075819&postcount=134>

Quote: > Originally Posted byNobody Special➡️I guess you'll remain a little bewildered then. A convolver is no more a representation of arealspace than an algorithmic reverb is. It's an accurate represention of an impulse reponse from a speaker or two to a single listener position. As I said before, a real orchestra is spread out in space. So is the audience. The impulse response from the second clarinet to seat 7C is different than the impulse response from thefirstclarinet to the same seat. A convolver effectively squishes the entire orchestra into a couple of points, quite accurately mimicking descent into a black hole.On top of all that, you simply don't hear every single reflection in a hall. That's not the way the auditory cortex works. You may hear discrete reflections for a few tens of milliseconds, but after that, reverberation becomes a frequency effect (with interaural phase differences being quite important). If you do that part well, the listener is satisfied.I didn't say that convolvers were bad. Sometimes they sound very nice. But to somehow say that they are natural and algorithmic reverbs are artificial shows a little too much susceptibility to marketing. News flash:They arebothartificial.I dont think you understood my point.


What I was trying to make clear is that any source, i.e., a vocal sent into a real room and fed back to microphones for reverberation can also be achieved with convolution, without the actual room. You would, of course need to have derived an impulse from "some" venue in order to be able to convolve it.


Placing "natural" in quotes **did** have a meaning and was not done randomly ;-)

Yes, all applied "space" is basically artificial. I was referring to the derivative of the applicator.


Of course, the result of the impulse response changes, based on where the microphone/ear and emitter is/are/were located.

But so does the result of exciting a real-world-room with a source to be reverberated, depending on emitter and microphone/ear positioning.

Just like it was done in the early days. No one ever strived to place the microphones where it sounded "bad" but where it sounded "good".... 

Newsflash: *Capturing a venue is not about capturing a venue from every theoretical and/or possible listening location of that venue. It is about capturing the venue itself, where it sounds the best. Which, may of course be highly opinionated*


I dont know how you act when you are at a concert. Myself, I try to find tickets for a "nice" listening location. I dont run around the concert hall all the time to be able to say; that I head the orchestra from every imaginable position, when I get home and tell the story.

You may be thinking too much in terms of mathematical possibility. But that will not derive a great impulse response from any venue. :-)

---

### Post #135 -- Page 5
**User:** noiseflaw
**Info:** Joined: Dec 2005Posts: 3,133🎧 20 years | Posts: 3,133
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075873&postcount=135>

Interesting thread...


Bit above my head though. Thankfully we live in a an audio world that has both Algorithmic and Convolution based models. Am very interested in Vienna Instruments new MIR project - exciting times ahead - will probably need a new Mac though!


Carry on Boffins.

---

### Post #136 -- Page 5
**User:** Acousticas
**Info:** Joined: Oct 2008Posts: 130🎧 15 years | Posts: 130
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075885&postcount=136>

Quote: > Originally Posted bynoiseflaw➡️Thankfully we live in a an audio world that has both Algorithmic and Convolution based models. .That is a wonderful summarization !

---

### Post #137 -- Page 5
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075909&postcount=137>

Quote: > Originally Posted bynoiseflaw➡️Interesting thread...Bit above my head though. Thankfully we live in a an audio world that has both Algorithmic and Convolution based models. Am very interested in Vienna Instruments new MIR project - exciting times ahead - will probably need a new Mac though!Carry on Boffins.Beyond my total grasp as well, but as the owner of the best convolution currently has to offer (thanks to Acousticas' sampling of Lexicon verbs), the owner of a PCM96, and having heard enough samples of the Bricasti to have a good sense of its general character, I have a clear and strong preference for algorithmic reverbs. The density, complexity and realism are unsurpassed.


However, I've been following Vienna's MIR convolution reverb very closely and I believe that it will set the new standard for conv. verb. Will it equal algorithmic? I'm skeptical, but open-minded. I know it's going to be a beast on CPU when running wide-open.

---

### Post #138 -- Page 5
**User:** studio3
**Info:** Joined: Oct 2007Posts: 13🎧 15 years | Posts: 13
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075925&postcount=138>

Quote: > Originally Posted byCasey➡️I'm sorry Sean, but that is beyond what I can say.Didn't NS post an example of the PCM96 random hall a while back?-Casey Nord Electro 2 Organ/(PCM 91)

---

### Post #139 -- Page 5
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075933&postcount=139>

Got WAVs? (or AIFs)

---

### Post #140 -- Page 5
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4075956&postcount=140>

Quote: > Originally Posted byAcousticas➡️I dont think you understood my point. I understood your point perfectly well. I've been hearing convolution 'verbs since Lake Audio demonstrated them years and years ago.

Quote: > Newsflash:Capturing a venue is not about capturing a venue from every theoretical and/or possible listening location of that venue. It is about capturing the venue itself, where it sounds the best. Which, may of course be highly opinionatedThe impulse reponse doesn't 'capture the venue'. It captures the venue from a single source/destination perspective. Convolving a signal through that impulse response gives you the effect of the whole orchestra squeezed into that point. And as Barry Blesser has pointed out in a paper (don't know if he published it), the impulse response of a space differs, depending on signal strength. None of the convolvers that I'm aware of take this point under consideration.

Quote: > You may be thinking too much in terms of mathematical possibilitySorry, but we developers are bound by the physical laws of the universe we inhabit. Like you, I find a good seat in a concert hall and enjoy the music. But I can't help but notice that the orchestra appears to be spread out in space, sitting in different chairs and all that. And some of them move. I myself might move my head a bit as I listen. All of that plays hell with the impulse response. My brain manages to average that in such a way that I hardly notice. That sort of tells me that a 'pure' impulse response isn't what it's about.


You might consider starting up another thread if you want to go into greater depth on your topic.

---

### Post #141 -- Page 5
**User:** Acousticas
**Info:** Joined: Oct 2008Posts: 130🎧 15 years | Posts: 130
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4076045&postcount=141>

Quote: > Originally Posted byNobody Special➡️You might consider starting up another thread if you want to go into greater depth on your topic.OK, point taken. Did not want to "HiJack" this thread. Sorry ;-)

---

### Post #142 -- Page 5
**User:** space2012
**Info:** Joined: Oct 2008Posts: 1,953🎧 15 years | Posts: 1,953
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4076091&postcount=142>

[Found:: Reverb plugin vs. rack unit tests http://www.diasonicdesign.com/tech/reverbs/](https://gearspace.com/board/gear-shoot-outs-sound-file-comparisons-audio-tests/380416-found-reverb-plugin-vs-rack-unit-tests-http-www-diasonicdesign-com-tech-reverbs.html#post4076073)

---

### Post #143 -- Page 5
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4077363&postcount=143>

Quote: > Originally Posted byAcousticas➡️It seems that a "feud" exists, between those who prefer algorithmic over convolution reverberation technology and vice versa. A "feud" which in my opinion is totally unwarranted, as both technologies are capable of producing wonderful results and are here to stay and more importantly, here to advance and maybe even benefit from one another.But what does it say when you have 3 products that are convolution impulses taken from algorithmic reverbs? It is hard to make the argument that the impulse responses of the Lexicon 224XL, Lexicon 300, and EMT 245 will sound better than an algorithmic reverb that implements those algorithms. 


A snapshot does not capture the time-varying behavior of real-world objects, and standard convolution is no more than a snapshot. Real acoustic spaces have lots of time variation, due to temperature variations, and this is not captured by convolution, which assumes LTI behavior. As has been mentioned in this thread, most of the higher end Lexicons (and most all Lexicons today) used time variation. Adding some chorusing on the output of the convolution does not adequately simulate this behavior.


Sean

---

### Post #144 -- Page 5
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4077658&postcount=144>

I haven't tried acoustica's products, but I've made impulses from my hardware units via various methods and used various convolver plugins for testing. The hardware always won. IMHO the convolver makes a muddy bass and artificial sounding highs, the wet signal doesn't blend well with the source.

---

### Post #145 -- Page 5
**User:** Sigma
**Info:** Joined: May 2006Posts: 6,814My Recordings/CreditsMy Studio🎧 20 years | Posts: 6,814My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4077787&postcount=145>

the 224 was a god send during the early drum machine days..the short room settings put "air" around the dead dry lynn drum samples [remember 1 chip per soud and changing chips in the org lynn?]


i forget which sofware ver but there was an early 224 that had a really fat sound the got lost on subsiquent versions


my father and i used i forget what raw setting and made it short  and then set  a 200 hz x over and a  2 k roll off..it made lead voacls especailly dynamic ones with singers who got nasal have some thickness without eq when the person started wailing


i remeber phil ramone coming in and saying }if i can't call up a setting on a piece of gear i just try another piec of gear..LOL the 480's on sure had enough pages LOL


i really liked the delays [and things you could do with them and the repeats] in them also


i think we had like 4 224's 2 480's and 2 960's at one point plus a number of pcm 42's, 70's and 90's [uhhh "tile room" LOL]


i used the old warm ver 224 during mixes with the 960 as an reverb also..they sounded sooo different it was nice having both flavors

---

### Post #146 -- Page 5
**User:** scottkrk
**Info:** Joined: Apr 2009Posts: 301🎧 15 years | Posts: 301
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4077798&postcount=146>

NS,


I really appreciate that you take the time to participate in this forum.


A couple of quick questions.


1. Is the MX500 totally MIA? I notice there is still an info page on your website [Lexicon Pro](http://www.lexiconpro.com/ProductIndex.aspx?ProductID=146)


2. Am I correct in assuming that the reason Lexicon don't release high quality plugins is a commercial choice (users pirating and competitors copying your IP) rather than a technical choice?


3. How good is Pantheon compared to say LXP-15 or MPX-1?


Cheers,


Scott

---

### Post #147 -- Page 5
**User:** Acousticas
**Info:** Joined: Oct 2008Posts: 130🎧 15 years | Posts: 130
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4078105&postcount=147>

Quote: > Originally Posted byseancostello➡️But what does it say when you have 3 products that are convolution impulses taken from algorithmic reverbs? It is hard to make the argument that the impulse responses of the Lexicon 224XL, Lexicon 300, and EMT 245 will sound better than an algorithmic reverb that implements those algorithms.A snapshot does not capture the time-varying behavior of real-world objects, and standard convolution is no more than a snapshot. Real acoustic spaces have lots of time variation, due to temperature variations, and this is not captured by convolution, which assumes LTI behavior. As has been mentioned in this thread, most of the higher end Lexicons (and most all Lexicons today) used time variation. Adding some chorusing on the output of the convolution does not adequately simulate this behavior.SeanHi Sean,


I respect NS' thread and topic and we should seize getting off the original topic of this thread. Therefore, I am going to send you a PM and try to respond to your message. Maybe, a new thread about convolution and algorithmic reverbs would be a good idea.

---

### Post #148 -- Page 5
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4078149&postcount=148>

Quote: > Originally Posted byAcousticas➡️Hi Sean,I respect NS' thread and topic and we should seize getting off the original topic of this thread. Therefore, I am going to send you a PM and try to respond to your message. Maybe, a new thread about convolution and algorithmic reverbs would be a good idea.There's a more technical thread about algorithmic reverbs - [https://gearspace.com/board/geekslut...ubculture.html](https://gearspace.com/board/geekslutz-forum/380233-reverb-subculture.html) - 


You could start an additional thread regarding convolution vs algorithmic reverbs and more people could participate.

---

### Post #149 -- Page 5
**User:** aeonlux
**Info:** Joined: Aug 2007Posts: 732🎧 15 years | Posts: 732
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4078290&postcount=149>

**Lexicon NuVerb** *Single* Algos:
- Random Hall
- Random Ambience
- Rich Plate
- Stereo Adjust

**Lexicon NuVerb** *Dual Mono/Cascade* Algos:
- Dual Delay
- Split Chamber
- Compressor
- PONS


cheers,

Ian

---

### Post #150 -- Page 5
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4078304&postcount=150>

Quote: > Originally Posted byscottkrk➡️1. Is the MX500 totally MIA? I notice there is still an info page on your websiteLexicon ProThe MX500 is not to be. After a tremendous amount of work, we decided it wasn't going to be the product we'd hoped.
Quote: > 2. Am I correct in assuming that the reason Lexicon don't release high quality plugins is a commercial choice (users pirating and competitors copying your IP) rather than a technical choice?Sorry but I can't comment on internal company stuff.

Quote: > 3. How good is Pantheon compared to say LXP-15 or MPX-1?It's a different fish. Pantheon is a single reverb algorithm (a little less capable than those you'll find in the MX-series, but not bad). The LXP-15 and MPX-1 both provided many different reverb algorithms as well as FX of various sorts. Pantheon is awfully convenient in a DAW environment, but either of those older boxes could do good service on a AUX path.



---


---

## Page 6

---

### Post #151 -- Page 6
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4078699&postcount=151>

Quote: > Originally Posted byNobody Special➡️The LXP-15 and MPX-1 both provided many different reverb algorithms as well as FX of various sorts. Pantheon is awfully convenient in a DAW environment, but either of those older boxes could do good service on a AUX path.just to confirm this, the LXP-15 (especially with mk2 chip) is a great box for strange sounds.... it also has 5 cv inputs for pedals or a slider box for some realtime control.... if you get 2 and run em in dual mono you can get some really nice reverbs with em.


call me crazy but i'd rather have 2 LXP-15mk2s (and the leftover cash) than a pcm-90/1.  the pcm-90 is too thin for my tastes....  I like the old pcm60s for their simplicity too.


simplicity is under rated.... lex pcm 60, eventide 2016, bricasti m7

---

### Post #152 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4078846&postcount=152>

Quote: > Originally Posted by11413➡️just to confirm this, the LXP-15 (especially with mk2 chip) is a great box for strange soundsOK, any differences between reverb algorithms on LXP-15 and LXP-15 mk II? Also, is the mk2 chip still available? 


Thanks,


Sean (reverb geek, LXP-15 owner)

---

### Post #153 -- Page 6
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4079131&postcount=153>

Quote: > Originally Posted byseancostello➡️OK, any differences between reverb algorithms on LXP-15 and LXP-15 mk II? Also, is the mk2 chip still available?i did the update a LONG time ago... so no help on getting the proms now.


i remember they sounded better with v2 and the OS was faster... paging around didnt seem so sluggish.  


i think the chips used to cost $75 or so.... maybe ebay if they're no longer sold?

---

### Post #154 -- Page 6
**User:** zmoorhs
**Info:** Joined: Feb 2009Posts: 330🎧 15 years | Posts: 330
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4081627&postcount=154>

Hi guys, 


What's a reasonable price range for a second hand LXP-15 these days? I'm thinking that I'd like to get one.

---

### Post #155 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4088040&postcount=155>

Quote: > Originally Posted byzmoorhs➡️What's a reasonable price range for a second hand LXP-15 these days? I'm thinking that I'd like to get one.I paid $100 off of Craigslist about a month ago. Most of the prices I have seen are somewhat higher, in the $150 to $175 range. It is definitely worth $100. It is a very deep unit, physically, but the power supply is built in - no wall wart.


Sean

---

### Post #156 -- Page 6
**User:** zmoorhs
**Info:** Joined: Feb 2009Posts: 330🎧 15 years | Posts: 330
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4089068&postcount=156>

Quote: > Originally Posted byseancostello➡️I paid $100 off of Craigslist about a month ago. Most of the prices I have seen are somewhat higher, in the $150 to $175 range. It is definitely worth $100. It is a very deep unit, physically, but the power supply is built in - no wall wart.SeanThanks for the info Sean. I saw one for £160 which is over $200, so I guess it wasn't much of a bargain after all. I kinda went off the idea of a mkI anyway, after reading more about the mkII improvements.

---

### Post #157 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4089321&postcount=157>

Quote: > Originally Posted byzmoorhs➡️Thanks for the info Sean. I saw one for £160 which is over $200, so I guess it wasn't much of a bargain after all. I kinda went off the idea of a mkI anyway, after reading more about the mkII improvements.I just got an email from Lexicon, that they did not have the update ROMs for the LXP-15. You'd think that they would have ROM images and a burner, but oh well. I'll track down the ROMs at some point.


Sean

---

### Post #158 -- Page 6
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4089794&postcount=158>

To the owners of the PCM96 : what is your preferred algorithm?

---

### Post #159 -- Page 6
**User:** rolo95
**Info:** Joined: Jun 2006Posts: 301🎧 20 years | Posts: 301
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090051&postcount=159>

This question is for NobodySpecial

or anyone that can answer it...


Why Lexicon Pantheon Plugin , dont resemble any of the hardware LEX units...


it sound harshy and metallic....


it is not smooth....


Seems that they have used code that was not used on their hardware units...


Any light on this ?

Thanks

---

### Post #160 -- Page 6
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090064&postcount=160>

Quote: > Originally Posted byWarp69➡️To the owners of the PCM96 : what is your preferred algorithm?It's tough to beat a good Lexicon Hall and these are very good. I also like the plates and chambers.

---

### Post #161 -- Page 6
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090264&postcount=161>

Quote: > Originally Posted byrolo95➡️Why Lexicon Pantheon Plugin , dont resemble any of the hardware LEX units...it sound harshy and metallic....it is not smooth....Seems that they have used code that was not used on their hardware units...Yep, it's just not up to the level of the hardware units, I'm afraid.

---

### Post #162 -- Page 6
**User:** rolo95
**Info:** Joined: Jun 2006Posts: 301🎧 20 years | Posts: 301
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090300&postcount=162>

so Lexicon is afraid to roll out any of the "big boys" code in VST form 

because of reverse engineering... or hack/ stole of the code... ?


or just they want to make people BUY Hardware units as they also make profit on the metal frames and hardware  parts....


Any insights ??

---

### Post #163 -- Page 6
**User:** raal
**Info:** Joined: Dec 2004Posts: 5,958My Studio1 Review written🎧 20 years | Posts: 5,958My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090340&postcount=163>

Quote: > Originally Posted byrolo95➡️so Lexicon is afraid to roll out any of the "big boys" code in VST formbecause of reverse engineering... or hack/ stole of the code... ?or just they want to make people BUY Hardware units as they also make profit on the metal frames and hardware  parts....Any insights ?? of course plugins are a good source of revenue, and protecting their code is only logical - whatever the case it's their company and they have the right to do as they like with their products. the buyer has the right to buy them or not.


speculating about why they do this or that i think is kind of a waste of time...

---

### Post #164 -- Page 6
**User:** rolo95
**Info:** Joined: Jun 2006Posts: 301🎧 20 years | Posts: 301
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090390&postcount=164>

Agreed

---

### Post #165 -- Page 6
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090610&postcount=165>

Further agreement.


The question isn't merely bait, it's bait with an insult.

---

### Post #166 -- Page 6
**User:** Fishmed
**Info:** Joined: Jun 2007Posts: 1,1511 Review written🎧 15 years | Posts: 1,151
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090623&postcount=166>

Quote: > Originally Posted byrolo95➡️This question is for NobodySpecialor anyone that can answer it...Why Lexicon Pantheon Plugin , dont resemble any of the hardware LEX units...it sound harshy and metallic....it is not smooth....Seems that they have used code that was not used on their hardware units...Any light on this ?ThanksI thought the Patheon sounds close to the MPX-100.

---

### Post #167 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4090828&postcount=167>

Quote: > Originally Posted byrolo95➡️so Lexicon is afraid to roll out any of the "big boys" code in VST formbecause of reverse engineering... or hack/ stole of the code... ?My guess is that it would be MUCH harder to reverse engineer a plugin, in order to copy an algorithm, than to get the same algorithm from a piece of hardware. PC disassembly is kinda nightmarish. So I doubt that Lexicon is emphasizing hardware in order to protect their IP from reverse engineering.


Hacking of the copy protection, on the other hand, is fairly easy. At least I presume so, looking at the number of plugins that are cracked. So, Lexicon may be afraid of people stealing the plugins themselves. Which seems like a pretty justified concern.

Quote: > or just they want to make people BUY Hardware units as they also make profit on the metal frames and hardware  parts....Probably. It turns out that a lot of business plans involve profit.


Plus, the metal frames and hardware make the algorithms harder to steal than if it was in plugin form. You'd have to go into a store, grab it, and run, like ol' time stealing.


If Lexicon put their algorithms into plugin form, it would undoubtedly make using the algorithms easier for most users of DAWs. However, just because it would be more convenient does not make having Lexicon algorithms in plugin form an inalienable right for anyone.


Sean

---

### Post #168 -- Page 6
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4091406&postcount=168>

Quote: > Originally Posted byelambo➡️It's tough to beat a good Lexicon Hall and these are very good. I also like the plates and chambers.The Lexicon PCM96 have 3 Hall algorithms - Random Hall, Hall and Concert Hall - which one do you use the most?

---

### Post #169 -- Page 6
**User:** rolo95
**Info:** Joined: Jun 2006Posts: 301🎧 20 years | Posts: 301
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4091601&postcount=169>

Sean


your last post bring me to this question....


Then why the pantheon sound so "bad" compared to their hardware counterparts...


or in more explicit way


Why they rolled out that VST that have nothing to do with a real Lexicon Verb...


The only thing that the Pantheon have good is the name LEXICON on it...

otherwise.... nothing....nada.... 

Rolo.

---

### Post #170 -- Page 6
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4091772&postcount=170>

Quote: > Originally Posted byWarp69➡️The Lexicon PCM96 have 3 Hall algorithms - Random Hall, Hall and Concert Hall - which one do you use the most?I lean towards the Hall for vocals and Concert Hall for orchestral work, two things I often use the 96 for, but even those are interchangeable.


I don't pull up the Random Hall simply out of habit to try the others first. I don't dislike it, I just don't remember to try it.

---

### Post #171 -- Page 6
**User:** rolo95
**Info:** Joined: Jun 2006Posts: 301🎧 20 years | Posts: 301
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4093941&postcount=171>

So you prefer a Hall instead of a Plate for vocals....

Can you tell some more why you like a hall better....

---

### Post #172 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4110671&postcount=172>

A little more info on the various Lexicon machines, based upon the manuals:


It looks like all of the algorithms on the 224XL were time-varying, using what Lexicon refers to as "Chorus." Presumably this was implemented by changing the length of interpolated delay lines within the recursive part of the reverb, although the actual number of modulated delay lines, the location within the topology, and the type of modulation used probably varied between the algorithms.


The later reverbs in the pre-480L generation generally did not use time-variation, except for in the Concert Hall algorithm. 


The 480L and later reverbs introduced a different type of time variation, with the terms Spin and Wander. I am unsure of how this was implemented, and it seems like the actual implementation varied between algorithms and possibly machines.


A breakdown of the some of the machines, with regards to time variation:


- 224XL: Chorus on all algorithms. An educated guess would be that Dark Hall has more modulation than the other algorithms.


- PCM60: No time variation


- PCM70: Chorus on Concert Hall only (well, chorus in the Chorus algorithm as well - I'm talking about reverb algorithms here)


- M200: Unknown. Since there is a shared lineage between the M200 and PCM70, I am going to guess that the Concert Hall has Chorus on it, at some preset value. I could be totally wrong.


- 480L: Spin and Wander on Random Hall, Ambience, and Surround/HD reverb. The Classic Cart has Chorus on Concert Hall, but not on Rich Plate for some reason (it was definitely listed for Rich Plate in the 224XL manual).


- 300: Spin and Wonder on Random Hall, Random Ambience. The Rich Plate and Split Chamber algorithms have something called "Randomization." Not sure what type of time-variation this is. Is this the Chorus parameter from the 224XL, or a variation of Spin/Wander?


- LXP1: No time variation


- LXP15: No time variation


- PCM80/81: Concert Hall has Chorus, other algorithms have Spin (presumably related to Spin/Wander).


- PC90/91: Random Hall and Ambience have Spin/Wander, Concert Hall has Chorus, other algorithms have Spin only.


- MPX1: No time variation.


- Lexiverb: Spin in Chamber and Plate algorithms.


It would be interesting to match people's Lexicon reverb preferences with the modulation types listed above, and see if any type of pattern emerges. 


Sean

---

### Post #173 -- Page 6
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4120390&postcount=173>

I've used the PCM70, PCM60, PCM91, LXP1, MPX550.  kept the PCM91, and I should have kept the PCM70. I'm keeping an eye out for a broken one.

---

### Post #174 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4153148&postcount=174>

A few more Lexicon questions:


- There is a recent Digitech pedal, the Hardwire RV-7, that is advertised as having Lexicon algorithms. Are these closest to the MX series of boxes? How close are they to the Pantheon reverb?


- In the 224XL, there were algorithms labeled "Constant Density Plate." Did any similar algorithms make it into later Lexicons under a different name? 


Sean

---

### Post #175 -- Page 6
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4153639&postcount=175>

Quote: > Originally Posted byseancostello➡️A few more Lexicon questions:- There is a recent Digitech pedal, the Hardwire RV-7. Are these closest to the MX series of boxes? How close are they to the Pantheon reverb?Sean, I'm pretty sure that they owe their heritage to the MX boxes.  I'll issue a correction if I find out anything different.  Pantheon is more or less a one-off.

Quote: > - In the 224XL, there were algorithms labeled "Constant Density Plate." Did any similar algorithms make it into later Lexicons under a different name?There are a few things at Lex that predate even me.  The 224 is one of them.  I'd wager that the plate you're speaking of passed on a lot of its DNA to the 480L, and from there on to everything else.  I'll have to investigate that one of these days.

---

### Post #176 -- Page 6
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154133&postcount=176>

Quote: > Originally Posted byNobody Special➡️I'll have to investigate that one of these days.Sean, NS,


The constant density plate was Davids response to a very interesting time in the early days of digital reverberation.


I am glad you brought this up because this classic page should be included in this thread;

[SST282_History](http://www.sevenwoodsaudio.com/SST282_History.htm)


Alas, the CD plate did not survive the early days. It was a casualty of Davids penchant for advancing technology and leaving older "less desirable" work behind.


-Casey

---

### Post #177 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154284&postcount=177>

Quote: > Originally Posted byCasey➡️Sean, NS,The constant density plate was Davids response to a very interesting time in the early days of digital reverberation.I am glad you brought this up because this classic page should be included in this thread;SST282_HistoryThe SST algorithm is very nifty, for sure. How does it relate to the CD Plate? I have some ideas how a constant density plate would be done, just based on the name, but I wouldn't think that the SST would be very close. I could be totally wrong, of course. The SST has an increasing echo density. Unstable, to be sure, but the modulation is a very clever way of getting around this: move the resonances before they result in oscillation. My experiments with this algorithm back in the early oughts showed that the modulation allowed you to use about 3x the feedback gain of the non-modulated version before things got too ugly.

Quote: > Alas, the CD plate did not survive the early days. It was a casualty of Davids penchant for advancing technology and leaving older "less desirable" work behind.What other algorithms got left behind? It seems like both the chamber and plate algorithms went through a few iterations before their final form; any other orphaned algorithms? Any of them, besides the constant density plate, worth remembering?


Or are you talking about the general progress of Lexicon algorithms from the 224XL to the 480L and onwards? 


With the C++/floating point environment of the PCM96, it seems like a perfect opportunity to set the wayback machine to the early Lexicon days, and revive some of the older algorithms that have a good reputation nowadays. Additionally, some of the older tricks could be included as options (i.e. add 224XL-type Chorus to the algorithms, in addition to Shape and Spread). I am woefully ignorant about the algorithms of modern Lexicons, so these characteristics might already be in place.


A "classic Lexicon revival" might be horribly boring to NS, as he has mentioned that he has a huge stack of new ideas to try out as time permits. However, having a single box that implemented EVERY classic Lexicon algorithm from the high end boxes of the past, as well as the new hotness algorithms, would be a pretty desirable product for a lot of people. 


Sean

---

### Post #178 -- Page 6
**User:** synthetic
**Info:** Joined: Aug 2005Posts: 515🎧 20 years | Posts: 515
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154338&postcount=178>

Isn't the sound of those older Lexicons as much about the early ADDAs of the time as the algorithms? The PCM96 already covers the best of Lexicon's past. I would rather see NS coding some new algorithms than porting older ones. Especially since the ones that got dropped along the way were probably the ones that didn't sound as good.

---

### Post #179 -- Page 6
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154398&postcount=179>

Quote: > Originally Posted bysynthetic➡️I would rather see NS coding some new algorithms than porting older ones.Maybe there are other Lexicon/Harman engineers that could aid in the porting task. I'm not trying to create boring work for NS, although I would certainly hope that a single poster's ideas on one forum would not have any impact on his job. 

Quote: > Especially since the ones that got dropped along the way were probably the ones that didn't sound as good.I'm sure this is true. Reading the 224XL manual, you come across algorithms like "Small Plate" and "Chamber" that seem like they were not as nice as the Rich Plate and Rich Chamber that followed. However, the CD Plates have a good rep, and the 224XL algorithms in general seem to have a different sound than the 480L and later units (with the exception of the 480L Classic Cart).


Sean

---

### Post #180 -- Page 6
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154412&postcount=180>

Quote: > Originally Posted byseancostello➡️I have some ideas how a constant density plate would be done, just based on the name....................Casey described a constant density plate algorithm in another thread - not exactly like an EMT250, but similar.


Not many algorithms from the 224 has survived - only the Concert Hall?


---

## Page 7

---

### Post #181 -- Page 7
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154423&postcount=181>

Quote: > Originally Posted byseancostello➡️.............224XL algorithms in general seem to have a different sound than the 480L and later units (with the exception of the 480L Classic Cart).Was David responsible for the Classic card for the 480L???

---

### Post #182 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4154440&postcount=182>

Quote: > Originally Posted byWarp69➡️Casey described a constant density plate algorithm in another thread - not exactly like an EMT250, but similar.Yep. I consider the "constant density" to refer to the fact that the echo density would not increase with time. This is found in algorithms with parallel combs with no cross coupling and no embedded or nested allpasses. The original Schroeder algorithms were constant density, as well as the EMT250-esque algorithm Casey describes. The "plate" implies a fairly high echo density, which can be realized in a number of ways - lots of output taps, series allpasses, lots of parallel combs, etc.

Quote: > Not many algorithms from the 224 has survived - only the Concert Hall?I am unsure how much later plates and chambers have in common with the 224XL. As far as the original 224 (no X or XL), apparently these algorithms sound fairly different from the 224XL. One of the Concert Hall algorithms in the 224XL is apparently the same as the original 224 Concert Hall. Some of the other 224XL Concert Halls seem to add chorusing to additional locations within the algorithm (Dark Hall), which implies that the 224XL had a few more cycles than the original 224.


Sean

---

### Post #183 -- Page 7
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4156106&postcount=183>

Quote: > Originally Posted byseancostello➡️Some of the other 224XL Concert Halls seem to add chorusing to additional locations within the algorithm (Dark Hall), which implies that the 224XL had a few more cycles than the original 224.The 224XL service manual indicates that the program is 100 steps. However, the microcode actually could do 128 steps - the program counter is cleared by writing an address with bit 3 set to the I/O space. The 224 (non-XL) version shows the same sort of thing - the WCS resets the PC. Though many of the Lexicons have a 128-step program counter, not all of them actually use all 128 steps.


To multiply with sufficient precision to do a linear interpolate, I would guess that four lines of code are likely needed for each chorus certainly on something like the PCM70 or 480L. But the 224 uses a 6-bit multiplier which would be on the ragged edge of being able to pull off a chorus in two lines.

---

### Post #184 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4156185&postcount=184>

Quote: > Originally Posted bydale116dot7➡️To multiply with sufficient precision to do a linear interpolate, I would guess that four lines of code are likely needed for each chorus certainly on something like the PCM70 or 480L. But the 224 uses a 6-bit multiplier which would be on the ragged edge of being able to pull off a chorus in two lines.Ragged edge is probably good enough for this application. The SST-282 that Casey brought up used NO interpolation for its modulated feedback taps. It just went ahead and moved them.


Casey's interpolation example used 32 discrete steps between samples. This was probably not meant to be an ideal example, of course. It seems like the 224 might have 64 possible steps for its interpolation if using the two line chorusing, which may produce acceptable results.


Sean

---

### Post #185 -- Page 7
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4157873&postcount=185>

Quote: > Originally Posted byseancostello➡️Ragged edge is probably good enough for this application. The SST-282 that Casey brought up used NO interpolation for its modulated feedback taps. It just went ahead and moved them.Chris didn't like that but it would be difficult with the SST architecture to do anything much about it without adding many more PROMs to the design. He even commented on it in the brochure. You'd have to make the gain prom pretty big, and run another state machine for tap fadeins before moving the tap.
Quote: > Casey's interpolation example used 32 discrete steps between samples. This was probably not meant to be an ideal example, of course. It seems like the 224 might have 64 possible steps for its interpolation if using the two line chorusing, which may produce acceptable results.If you updated the chorus gain coefficients and addresses on every sample, that would be the same granularity as a 4 Hz chorus of a 3ms depth, even if you had a more precise multiplier you'd have that granularily anyways. That's a faster chorus than I would expect in a reverb, but a two-line chorus would be at least not in the grunge area of granularity.

---

### Post #186 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4158131&postcount=186>

Quote: > Originally Posted bydale116dot7➡️If you updated the chorus gain coefficients and addresses on every sample, that would be the same granularity as a 4 Hz chorus of a 3ms depth, even if you had a more precise multiplier you'd have that granularily anyways.That's an interesting way of looking at it. 

Quote: > That's a faster chorus than I would expect in a reverb, but a two-line chorus would be at least not in the grunge area of granularity.You can get some nice effects with faster chorus settings. Very Budd/Eno. I think they used the modulation from a Lexicon Prime Time in their work, with a medium speed LFO, around 3-4 Hz, and ran this in feedback with an EMT-250.


Sean

---

### Post #187 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4190539&postcount=187>

One more box to ask about****: LARES. Do these run a 480L-type Random Hall algorithm, or something totally different?

---

### Post #188 -- Page 7
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4190939&postcount=188>

Quote: > Originally Posted byseancostello➡️One more box to ask about: LARES. Do these run a 480L-type Random Hall algorithm, or something totally different?The reverb itself is the surround or HD algorithm found on the 480 surround cart.


The strong chorusing on the early portion of this algorithm was designed in part to increase the gain before feedback needed for the live LARES application.


-Casey

---

### Post #189 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4191565&postcount=189>

Quote: > Originally Posted byCasey➡️The reverb itself is the surround or HD algorithm found on the 480 surround cart.The strong chorusing on the early portion of this algorithm was designed in part to increase the gain before feedback needed for the live LARES application.Thanks for the info. This fits in with what Peter Svensson found in his research, that delay line modulation was the most effective technique of reducing feedback in reverberation enhancement systems, although phase modulation (via Hilbert technique) was more effective for lower frequencies.


If I read correctly, the LARES systems currently run on Lexichips, which would imply that the HD algorithm was ported over to that hardware at some point.


Sean

---

### Post #190 -- Page 7
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4201345&postcount=190>

I was flipping through my PCM91 preset list, and noticed that most 'rooms' use either the concert hall or random hall presets - a lot of random hall. Not many 'rooms' on there actually use the room/chamber algorithm. A big surprise for me was to find that 'Saxy Hangar' with its long tail uses the Ambience algorithm. Is this a common thing to do - abuse the algorithms?

---

### Post #191 -- Page 7
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4201387&postcount=191>

Quote: > Originally Posted bydale116dot7➡️Is this a common thing to do - abuse the algorithms?You bet your bippy!  The name of the preset is (and always has been) an indication of the  sound, not an indication of the underlying algorithm.  Lex algorithms are generally quite flexible and sometimes we get a better effect by 'abusing' the algorithm.  Once you get to the 960L and PCM96, you'll even find rooms made from delay algorithms (on the PCM96, there are even rooms made from chorus and pitch shift).


I've been amused that another thread has latched onto a hall preset called "EM7", believing it to be our attempt at modeling the Bricasti.  In fact, that preset is based on the new "Room" algorithm and was simply a tip of the hat.  Just as a hall can be used to make a room, a room can be used to make a hall!


Confused enough?

---

### Post #192 -- Page 7
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4201411&postcount=192>

Quote: > Originally Posted byseancostello➡️If I read correctly, the LARES systems currently run on Lexichips, which would imply that the HD algorithm was ported over to that hardware at some point.Almost, but not quite.  LARES was originally a separate algorithm for the 480L (not provided in the standard unit).  Dave G used a few aspects of LARES for his HD algorithm, but HD isn't a full LARES implementation.


Several years ago, LARES was ported to the 960L and has been the basis of LARES systems for about the last 5-6 years.  Another version was ported to the DNA chip (another Harman chip) and is used in the Wenger practice room.  For those that don't know the Wenger room, it's pretty cool.  It's used at conservatories and provides a realistic rehearsal space for musicians.  Simply dial in where you'd like to be and start playing.

---

### Post #193 -- Page 7
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4202103&postcount=193>

Quote: > Originally Posted byNobody Special➡️You bet your bippy!  The name of the preset is (and always has been) an indication of the  sound, not an indication of the underlying algorithm.  Lex algorithms are generally quite flexible and sometimes we get a better effect by 'abusing' the algorithm.  Once you get to the 960L and PCM96, you'll even find rooms made from delay algorithms (on the PCM96, there are even rooms made from chorus and pitch shift).Makes sense, if the parameters are set right. On the PCM70, 'Tunnel' which sounds like it shold be a reverb algorithm is really just a six-voice delay. I guess I never paid much attention to the actual algorithm used until we've started these discussions. I just dial up 'vocal magic' or 'just plate' or whatever, and either just use it, or diddle with some of the settings a bit. Usually I pick a preset and diddle with either size or RT or the RT EQ, that's normally enough.

---

### Post #194 -- Page 7
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4207748&postcount=194>

Quote: > Originally Posted byseancostello➡️That's an interesting way of looking at it.You can get some nice effects with faster chorus settings. Very Budd/Eno. I think they used the modulation from a Lexicon Prime Time in their work, with a medium speed LFO, around 3-4 Hz, and ran this in feedback with an EMT-250.SeanSean, 


I've enjoyed reading your posts on the subject of artificial reverb in these many threads, thanks for contributing..! What's your background in DSP? ( EDIT: I read your blog.. we must speak! )


Every track on those Eno / Budd records used a different signal chain.. nothing to my ears as warbley as 3-4hz.. plenty of modulations and recirculated signal routings, to be sure.  Possible the most interesting soundscapes I've encountered, though!!!  I'd love to see a gearlist for the "Ambient 2" and "The Pearl".. right?   I have some doubts about the use of an EMT 250 simply due to it's scarcity and price (given the budget of those records).  In a related bit of trivia, the 250 has some very very slow modulation in it's algo. A remarkably effective and simple algo it is (4 delay / diffusor stages)...


CZ

---

### Post #195 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4209403&postcount=195>

Quote: > Originally Posted byzmix➡️I read your blog.. we must speak!So you're the one person I got hits from! 

Quote: > I'd love to see a gearlist for the "Ambient 2" and "The Pearl".. right? I have some doubts about the use of an EMT 250 simply due to it's scarcity and price (given the budget of those records).I was basing this off of a Daniel Lanois interview I read:

[Music Glob » Blog Archive » Daniel Lanois Interview](http://musicglob.com/exclusives/daniel-lanois-interview/)


The later ambient work that Eno and Lanois worked on apparently made heavy use of the Lexicon 224. The Concert Hall algorithm was used for its modulated ambience, and the 6-voice Chorus added modulation to long feedback paths. The various Lexicon Concert Hall algorithms I have heard (PCM-70, PCM91) have internal modulation, which creates an effect similar to the Budd/Eno work.

Quote: > In a related bit of trivia, the 250 has some very very slow modulation in it's algo. A remarkably effective and simple algo it is (4 delay / diffusor stages)...Casey has written about an EMT-esque algorithm here on Gearslutz:

[https://gearspace.com/board/geekslut...ubculture.html](https://gearspace.com/board/geekslutz-forum/380233-reverb-subculture.html)


Probably not the exact EMT algorithm, but still interesting. 


Sean Costello

---

### Post #196 -- Page 7
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4211033&postcount=196>

Quote: > Originally Posted byseancostello➡️I was basing this off of a Daniel Lanois interview I read:https://gearspace.com/board/geekslut...ubculture.htmlThe later ambient work that Eno and Lanois worked on apparently made heavy use of the Lexicon 224. The Concert Hall algorithm was used for its modulated ambience, and the 6-voice Chorus added modulation to long feedback paths. The various Lexicon Concert Hall algorithms I have heard (PCM-70, PCM91) have internal modulation, which creates an effect similar to the Budd/Eno work.Casey has written about an EMT-esque algorithm here on Gearslutz:https://gearspace.com/board/geekslut...ubculture.htmlProbably not the exact EMT algorithm, but still interesting.Sean CostelloI'm quite familiar with the EMT 250 and have spoken with Barry Blesser about some small aspects of it.  I find early digital reverb research fascinating stuff.  


As for the Lanois Interview.. both of those links you provided point to the same thread, which I had already seen, but I am interested in reading the interview you cited.

---

### Post #197 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4211175&postcount=197>

Quote: > Originally Posted byzmix➡️As for the Lanois Interview.. both of those links you provided point to the same thread, which I had already seen, but I am interested in reading the interview you cited.Sorry - yesterday was a long day. The proper link is

[Music Glob » Blog Archive » Daniel Lanois Interview](http://musicglob.com/exclusives/daniel-lanois-interview/)


I fixed my post as well.


Sean

---

### Post #198 -- Page 7
**User:** Honch
**Info:** Joined: May 2008Posts: 3591 Review written🎧 15 years | Posts: 359
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4290557&postcount=198>

I've been readin this thread for quite a while, with great amusement and find most of it quite intriguing. I find it peculiar though, that no one has mentioned the "**ECM reverb**" yet. 

**To those of you who works at Lex, can you hear what preset they use on ECM recordings?** I e by engineer Jan-Erik Kongshaug and/or Manfred Eicher?


For those who doesn't know: 


ECM is a SMALL record label (German/Norwegian) specialising in chamber jazz music, and uses a lot of silence and - especially - space in their recordings. I e lots of ambience added to their production. Known artists are Keith Jarrett, Pat Metheny and so on. Critics have been labeling the label such as "the most beautiful sound next to silence" and "the only label not in need to ever remaster their back catalog". But that's another thread, topic and discussion.

*But to me, that label has always been the one to promote and pitch "Lexicon reverb" sound the most, to me anyway*. A whole demo label for Lexicon, so to speak. Although, in some instances, too excessively. Violinist Paul Giger, and some Pat Metheny Group productions comes to mind, for overdoing it. Pat left the label when he thought Manfred Eicher went over the top adding excessive reverb to his material.

**Can you hear that they're using (or was) Lexicon units at all? And what presets or algorithms?**


/Honch

---

### Post #199 -- Page 7
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4290994&postcount=199>

Quote: > Originally Posted byhonch➡️i've been readin this thread for quite a while, with great amusement and find most of it quite intriguing. I find it peculiar though, that no one has mentioned the "ecm reverb" yet.to those of you who works at lex, can you hear what preset they use on ecm recordings?i e by engineer jan-erik kongshaug and/or manfred eicher?For those who doesn't know:Ecm is a small record label (german/norwegian) specialising in chamber jazz music, and uses a lot of silence and - especially - space in their recordings. I e lots of ambience added to their production. Known artists are keith jarrett, pat metheny and so on. Critics have been labeling the label such as "the most beautiful sound next to silence" and "the only label not in need to ever remaster their back catalog". But that's another thread, topic and discussion.but to me, that label has always been the one to promote and pitch "lexicon reverb" sound the most, to me anyway. A whole demo label for lexicon, so to speak. Although, in some instances, too excessively. Violinist paul giger, and some pat metheny group productions comes to mind, for overdoing it. Pat left the label when he thought manfred eicher went over the top adding excessive reverb to his material.can you hear that they're using (or was) lexicon units at all? And what presets or algorithms?/honchEMT 250.  It has only one reverb algorhythm available (on a button marked "REVERB").


On the other hand, Windham Hill Records used a Lexicon 224 on all of their early 'new age' albums (George Winston, etc).  Three years ago I nearly purchased that very 224 from Steven Miller (the engineer on all those records), but alas, he sold it out from under me...

---

### Post #200 -- Page 7
**User:** Honch
**Info:** Joined: May 2008Posts: 3591 Review written🎧 15 years | Posts: 359
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4291205&postcount=200>

Quote: > Originally Posted byzmix➡️EMT 250. It has only one reverb algorhythm available (on a button marked "REVERB").On the other hand, Windham Hill Records used a Lexicon 224 on all of their early 'new age' albums (George Winston, etc). Three years ago I nearly purchased that very 224 from Steven Miller (the engineer on all those records), but alas, he sold it out from under me...Ok, it was a EMT 250... one algorithm. I thought that ECM was Lexicon all the way.

Ahha, so WH used a 224? I heard difference from them anyway. ECM and WH. They're different music altogether in spite of using mostly acoustic instruments. I think that ECM one, EMT 250 must have been swapped out over at ECM (or Rainbow studios in Oslo) a long time ago. Although ECM started out in 1969 it sounds as if - almost - they were made for big ambient production from the start on, and when EMT 250 came around, it must've been their wet dream come through. I'll bet they're using Bricasti nowadays...  no seriously, they can use whatever. TC if they like. And also I think that - today - you can mimick the EMT250 algorithm inside any PC and software/convolution reverb anyway. Not to one hundred percent though, but damm near close. Get a decent one anyway, but without all the editing tweaks of a real EMT 250.


/Honch

---

### Post #201 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4329967&postcount=201>

Reviving a dormant thread...


I have already asked about the difference between the 480L Random Hall and PCM90/91 Random Hall, but Casey was unable to answer, probably due to agreements with ex-employers, trade secrets, and the like. So, is anyone else able to describe the differences between these algorithms? I'm not sure if anyone who owns a 480L would buy a PCM91, but if anyone has both, can you describe the sonic differences between these algorithms?


Thanks,


Sean Costello

---

### Post #202 -- Page 7
**User:** DanDan
**Info:** Joined: Aug 2003Posts: 16,4331 Review written🎧 20 years | Posts: 16,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4331413&postcount=202>

Money doesn't talk, it shouts! I have used the 480L extensively and I own a 91. 

I doubt if I am technically correct,  but my opinion of the sonics goes like this:-

The 480 has say 4 engines. Two full stereo reverbs.

The 91 has two engines, which can be harnessed together in a single reverb.

These two 91 engines working together on one reverb sound like a single one of the 480 engines. 

Not bad at all, but the 480 absolutely rules.

DD

---

### Post #203 -- Page 7
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4332312&postcount=203>

Quality of reverb algorythms is not always depnding on brute CPU force.  Remember that the 250 is a loved reverbmachine with relative few (K)MIPS.  Good algos with low CPU power are better then a supercomputer with a lesser algo. It is the sound that counts in the end.

---

### Post #204 -- Page 7
**User:** 11413Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4333390&postcount=204>

Quote: > Originally Posted byDanDan➡️Money doesn't talk, it shouts! I have used the 480L extensively and I own a 91.I doubt if I am technically correct,  but my opinion of the sonics goes like this:-The 480 has say 4 engines. Two full stereo reverbs.The 91 has two engines, which can be harnessed together in a single reverb.These two 91 engines working together on one reverb sound like a single one of the 480 engines.Not bad at all, but the 480 absolutely rules.DDyeah, the 91 is wimpy.... i actually liked the sound of the Nuverb TDM card more... the only thing i liked in the 90/91 better was having stereo width on a 360 degree LFO.. and that was for one crazy WTF effect.... i actually found this used on a record if anyone is curious what it sounds like...


it's on the NIN/Oliver Stone/Natural Born Killers soundtrack... i'll have to find the specific track.


I still love the PCM 60 for it's simplicity..... same reason i eventually want a princeton/eventide 2016.... one knob, one function, learn your instrument, no pages.... it also forces me to get a unique setting each time... interact with the music.. make a unique decision... instead of dialing up a preset.  


it's the difference between having a modular synthesizer and a rompler.... i also like to "play" the knobs when i'm printing effects so i can emphasize lil things and make ear candy... all the type of stuff which comes out in repeated listening...


or stuff you'd do with a LARC/midi slider box.


one of the coolest things about the LXP-15 was the FIVE cv pedal inputs..... you can modulate parameters with a modular synth or cv/gate sequencer...  actually, erase that from your mind... the price of LXP-15s will go thru the roof now like the jam mans did a few years ago. 

*these arent the droids you're looking for *waves hand*
you don't need to see his identification *waves hand*
he can move along...*

---

### Post #205 -- Page 7
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4333687&postcount=205>

Quote: > Originally Posted byseancostello➡️I have already asked about the difference between the 480L Random Hall and PCM90/91 Random Hall,They're very close, Sean. The PCM90/91 Random Hall came from the 300 Random Hall, which is very, very close to the 480L. The PCM90/91 has a 20-bit memory as opposed to the 18-bit memory in the 480L. It also has an extra bit in its coefficient architecture. These result in a slightly cleaner sound in the PCM version.

---

### Post #206 -- Page 7
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4333748&postcount=206>

Thanks for sharing this info!

---

### Post #207 -- Page 7
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4334449&postcount=207>

Thanks, NS!

---

### Post #208 -- Page 7
**User:** jnorman
**Info:** Joined: Sep 2004Posts: 3,788My Recordings/CreditsMy Studio3 Reviews written🎧 20 years | Posts: 3,788My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4334770&postcount=208>

i see a few comments on how lame the pantheon plugin is/was.  it has now been updated with the pantheon II plugin - has anyone used it, and is ti any good?  thanks.

---

### Post #209 -- Page 7
**User:** audio ergo sum
**Info:** Joined: Oct 2008Posts: 3,644🎧 15 years | Posts: 3,644
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4336916&postcount=209>

Quote: > Originally Posted byNobody Special➡️They're very close, Sean. The PCM90/91 Random Hall came from the 300 Random Hall, which is very, very close to the 480L. The PCM90/91 has a 20-bit memory as opposed to the 18-bit memory in the 480L. It also has an extra bit in its coefficient architecture. These result in a slightly cleaner sound in the PCM version.Nobody Special, I recently worked with a PCM 96 and found the manual very short, missing information about the preset's parameters.


Do you have a list of all the parameters of the presets in a handy excel spreadsheet on Lexicon's website?


Not everybody has time, to listen carefully to the difference between RandomHall 2 and RandomHall 3 etc.


That would be something very easy to do and of great help, also if you could include a column for remarks, pointing out those presets that were created after 480 or 960 predecessors etc.


Does this make sense to you? I find the manual disturbingly short and simplistic and when it comes to describing the presets there is nothing.

---

### Post #210 -- Page 7
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4337337&postcount=210>

Quote: > Originally Posted byaudio ergo sum➡️Does this make sense to you? I find the manual disturbingly short and simplistic and when it comes to describing the presets there is nothing.Makes all sorts of sense, and I'm sorry we don't have such a document for you.  To be completely truthful, I'm not sure when we'll have it.  Only thing I can suggest is simply to audition the presets with your source audio and choose what you like.  In the end, that's the measure that matters.


To carry that a bit farther, the names themselves *are* descriptive up to a point.  You know a percussion-labeled preset will be more diffuse so that transients don't rattle around.  You know that a vocal-labeled preset will be less-diffuse, with perhaps a hint of discrete echo.  But I'm not at all sure how I'd draw a meaningful text distinction between ElephantShoe1 and ElephantShoe2.  They'll be similar, but depending on your particular snare drum (or Ophicleide) either one could be the preset of choice.


N.S.


---

## Page 8

---

### Post #211 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4337633&postcount=211>

Quote: > Originally Posted byNobody Special➡️They're very close, Sean. The PCM90/91 Random Hall came from the 300 Random Hall, which is very, very close to the 480L. The PCM90/91 has a 20-bit memory as opposed to the 18-bit memory in the 480L. It also has an extra bit in its coefficient architecture. These result in a slightly cleaner sound in the PCM version.I have a 300.  What presets correspond to Random Hall?  Large Hall?


Thanks,

R

---

### Post #212 -- Page 8
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4337694&postcount=212>

Quote: > Originally Posted byRKrizman➡️I have a 300.  What presets correspond to Random Hall?  Large Hall?RThey may be listed in the manual, but you can easily learn which algorithm is underneath the preset you're running.  Load the preset and hold a button (I'm pretty sure it's the Prog/Banks button) for two seconds.  It will then show you the name of the algorithm.


If I got the button wrong (don't have a 91 close by at the moment), just try the others.  A lot of people don't know that the 81 and 91 have online help by holding the buttons down.

---

### Post #213 -- Page 8
**User:** DanDan
**Info:** Joined: Aug 2003Posts: 16,4331 Review written🎧 20 years | Posts: 16,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4337769&postcount=213>

I have a 480 memory  Cartridge here. I haven't used it for years. Would anyone like to have it? Free, just pay the postage. 

DD
[Sound Sound - Homepage](http://www.soundsound.ie)

---

### Post #214 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4338043&postcount=214>

Quote: > Originally Posted byNobody Special➡️They may be listed in the manual, but you can easily learn which algorithm is underneath the preset you're running.  Load the preset and hold a button (I'm pretty sure it's the Prog/Banks button) for two seconds.  It will then show you the name of the algorithm.If I got the button wrong (don't have a 91 close by at the moment), just try the others.  A lot of people don't know that the 81 and 91 have online help by holding the buttons down.Found it in the 300 manual, thanks.


-R

---

### Post #215 -- Page 8
**User:** audio ergo sum
**Info:** Joined: Oct 2008Posts: 3,644🎧 15 years | Posts: 3,644
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4340979&postcount=215>

Quote: > Originally Posted byNobody Special➡️Makes all sorts of sense, and I'm sorry we don't have such a document for you.  To be completely truthful, I'm not sure when we'll have it.  Only thing I can suggest is simply to audition the presets with your source audio and choose what you like.  In the end, that's the measure that matters.To carry that a bit farther, the names themselvesaredescriptive up to a point.  You know a percussion-labeled preset will be more diffuse so that transients don't rattle around.  You know that a vocal-labeled preset will be less-diffuse, with perhaps a hint of discrete echo.  But I'm not at all sure how I'd draw a meaningful text distinction between ElephantShoe1 and ElephantShoe2.  They'll be similar, but depending on your particular snare drum (or Ophicleide) either one could be the preset of choice.N.S.Thank you. Having a table to look at would give one a quick idea what was intended.


That can't be difficult to do. Just a column for each parameter and a line for each preset.


What happened in the last years at Lexicon? Do you find explaining your presets and algorithms redundant? I certainly don't.


Couldn't you even copy/paste a lot of stuff from the older manuals?

---

### Post #216 -- Page 8
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4573790&postcount=216>

Hi all:


I have been doing some reading, listening, and the like about the early Lexicon plates. As far as I can tell, there are a couple of varieties of plate reverbs available in the early Lexicons. The 224 has a couple of Plates, as well as a Constant Density Plate. In the M200, there are 2 types of plates described - one simply referred to as Plate, the other as Rich Plate. The Lexicon 224XL has Plates, Constant Density Plates, and Rich Plates. 


Can anyone describe the sonic differences between these plates? I know that the Constant Density Plates are, well, constant density, and are probably kinda close-ish to the EMT250. I've heard Rich Plate. How do the other plates compare? What do people prefer? Why did Rich Plate end up the winner, in the Darwinian sense ("survival of the fittest"="survival of those that survive")?

---

### Post #217 -- Page 8
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4963786&postcount=217>

Reviving an old thread:


The PCM96 has 2 plate algorithms, Vintage Plate and just plain ol' Plate. NS, if you are reading this, can you give a quick summary of the differences between these?


There are a lot of different Lexicon plates. The 224, 224XL and 200 all had a plate algorithm that seemed to be abandoned after Rich Plate came on the scene. The Constant Density Plate went away after the 224XL. The 480L introduced a new algorithm that was used for plates (I don't know much about that one, except that it seems different from the old Rich Plate). I guess if you are working on something for 30 years, you will come up with a bunch of different algorithms.

---

### Post #218 -- Page 8
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4965219&postcount=218>

Quote: > Originally Posted byseancostello➡️Reviving an old thread:The PCM96 has 2 plate algorithms, Vintage Plate and just plain ol' Plate. NS, if you are reading this, can you give a quick summary of the differences between these?Forgot about this thread.  I think the Vintage Plate is a bit 'platier'.  It has a softer attack that's a bit more diffuse.  Some aspects of it come from the PCM70, but the back end has the more advanced EQ from the PCM96.  Overall, I prefer it to the regular PCM96 plate.

---

### Post #219 -- Page 8
**User:** Sput
**Info:** Joined: Jul 2005Posts: 375🎧 20 years | Posts: 375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4971168&postcount=219>

Quote: > Originally Posted byNobody Special➡️Forgot about this thread.  I think the Vintage Plate is a bit 'platier'.  It has a softer attack that's a bit more diffuse.  Some aspects of it come from the PCM70, but the back end has the more advanced EQ from the PCM96.  Overall, I prefer it to the regular PCM96 plate.Vintage Plate?? Is that a different algorythm??

I don't recall my PCM96 having more than 1 plate algorythm...  but I've been wrong in the past! 


Are you refering to "colored plate" preset??


Thanks!

---

### Post #220 -- Page 8
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4972328&postcount=220>

Quote: > Originally Posted bySput➡️Vintage Plate?? Is that a different algorythm??I don't recall my PCM96 having more than 1 plate algorythm...  but I've been wrong in the past!Are you refering to "colored plate" preset??Thanks!Sorry, but Vintage Plate isn't in the hardware.  It's currently a plugin-only algorithm.

---

### Post #221 -- Page 8
**User:** thermos
**Info:** Joined: Jul 2004Posts: 7,658My Studio1 Review written🎧 20 years | Posts: 7,658My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4972604&postcount=221>

Quote: > Originally Posted byNobody Special➡️Sorry, but Vintage Plate isn't in the hardware.  It's currently a plugin-only algorithm.I like that one a lot more than the regular plate algo too, I'm surprised more people haven't talked about it. It's kind of a standout in the bundle to me. 

It should really be in the hardware I would say.

---

### Post #222 -- Page 8
**User:** Sput
**Info:** Joined: Jul 2005Posts: 375🎧 20 years | Posts: 375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4973097&postcount=222>

Quote: > Originally Posted bythermos➡️I like that one a lot more than the regular plate algo too, I'm surprised more people haven't talked about it. It's kind of a standout in the bundle to me.It should really be in the hardware I would say.I certainly would say so too!!


Thanks god I have a REAL vintage plate around for those duties...

---

### Post #223 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4977366&postcount=223>

Quote: > Originally Posted byNobody Special➡️Sorry, but Vintage Plate isn't in the hardware.  It's currently a plugin-only algorithm.What!?  I'm calling a technical foul.


-R

---

### Post #224 -- Page 8
**User:** DarkSky Media
**Info:** Joined: Jun 2009Posts: 4,623🎧 15 years | Posts: 4,623
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4979707&postcount=224>

Quote: > Originally Posted byNobody Special➡️Forgot about this thread.  I think the Vintage Plate is a bit 'platier'.  It has a softer attack that's a bit more diffuse.  Some aspects of it come from the PCM70, but the back end has the more advanced EQ from the PCM96.  Overall, I prefer it to the regular PCM96 plate.So, NS... Is an update for hardware owners in the works, or do we need to contemplate the obsolescence of our hardware units and go get the software in order to have access to Vintage Plate?

---

### Post #225 -- Page 8
**User:** Dan
**Info:** Joined: Mar 2004Posts: 1,677🎧 20 years | Posts: 1,677
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4981218&postcount=225>

Quote: > Originally Posted byDSM Interactive➡️So, NS... Is an update for hardware owners in the works, or do we need to contemplate the obsolescence of our hardware units and go get the software in order to have access to Vintage Plate?and I was wondering if a working 10.6 driver is coming out.  It seems lexicon is taken the tried and true MOTU approach of coming out with new stuff instead of fixing what they've already sold.

---

### Post #226 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4981623&postcount=226>

Yeah, what's with that.  We shelled out good bucks for a hardware unit that does not work as advertised.  Now we miss out on updates?


-R

---

### Post #227 -- Page 8
**User:** jrakarl
**Info:** Joined: Jul 2009Posts: 992My Recordings/CreditsMy Studio4 Reviews written🎧 15 years | Posts: 992My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5282456&postcount=227>

Quote: > Originally Posted byseancostello➡️The PCM90/91 and M300 are obviously descended from the 480L, but many of the lower end Lexicons that followed (PCM80/81, LXP1/5/15) seem like they were based on the 224XL algorithms, at least by the descriptions of the parameters. SeanDamn, I wish I'd known that prior to investing in a PCM80!

---

### Post #228 -- Page 8
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5283239&postcount=228>

Quote: > Originally Posted byjrakarl➡️Damn, I wish I'd known that prior to investing in a PCM80!You should actually be happy.

---

### Post #229 -- Page 8
**User:** jrakarl
**Info:** Joined: Jul 2009Posts: 992My Recordings/CreditsMy Studio4 Reviews written🎧 15 years | Posts: 992My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5305389&postcount=229>

Hi NobodySpecial and everyone here - you guys seem to know a lot about this stuff, so I thought I'd put it out there...  

I have seen an advertisement from someone selling a PCM90 and in that ad it apparently quotes someone from Lexicon, saying that the 80 and the 90 are intended to work together to form some sort of awesome reverb / effects monster... I'll quote! 


  "The PCM 90 features a range of versatile high-quality reverberation programs which derive their heritage from Lexicon's top-of-the-line studio processors, the 480L and Model 300. Its unique dual-processor architecture -- featuring two of Lexicon's proprietary reverb DSP ICs, the Lexichip(TM) II, allows unparalleled flexibility in reverberation quality and control. It's companion product, the PCM 80, offers the highest quality effects, with reverb heritage from the Lexicon's legendary PCM 70. "**The two units are designed to be able to be used as a system**," says Lexicon's Director of Product Management, Steve De Furia "and while you can, of course, use the units independently, together they're phenomenal." Both units feature true stereo capability with 1 8-bit A/D converters as well as digital inputs, and a 24-bit internal digital bus.


**As a system, the PCM 80 and PCM 90 offer as many as 4 independent inputs and outputs, digital or analog. The PCM 90 ships with 250 all-new presets designed with real-world applications in mind. Banks and rows are labeled logically and clearly so you can find the sounds you want as you scroll through the presets"**


So my question is this.. are these units somehow able to be linked together, or are there some specific applications where these units used together can create something that individually they cannot?  What are the major differences between these units that suggests that they are 'together' the answer to my reverb prayers?  Is one better bypassing these and going thraight into PCM96 plug-in territory?


I have a newly acquired PCM80 and am considering whether a PCM90 would be a worthwhile addition on top of this... ????


Thank you all...

Quote: > Originally Posted byNobody Special➡️Many good remarks here about favorite presets and such. I'd certainly be interested in getting as close as possible to some old classics. I'd also like to gather up some user-generated presets. We don't have a good way to organize such an effort just yet, but I'd think something with MIDI bulk dump might be one way to get there.I do hope that some of you have been rolling up your sleeves and getting into programming the box (or even some of your older Lexes). One thing I've learned is that different people--with different applications, different ears, and different points of view--can come up with some unique and useful sounds. I know that we've just scratched the surface of what the box can do, and I've love to offer a folder of user favorites.Toby, hang onto that 200. It's like your favorite old aunt. She's crotchety and a little limited for sure, but even if you found a replacement, it would never be the same.I've been a bit busy of late, but I hope I can get back in here before too long and cover a few more areas of interest.

---

### Post #230 -- Page 8
**User:** jrakarl
**Info:** Joined: Jul 2009Posts: 992My Recordings/CreditsMy Studio4 Reviews written🎧 15 years | Posts: 992My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5305396&postcount=230>

Quote: > Originally Posted byShy➡️You should actually be happy.I'm trying to get the best bang for the buck but also cover bases...  I'm happy .. or will be when it arrives

---

### Post #231 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5305405&postcount=231>

Quote: > Originally Posted byNobody Special➡️Sorry, but Vintage Plate isn't in the hardware.  It's currently a plugin-only algorithm.Bumping this comment.  Should have never leaned over to pick up the soap.


-R

---

### Post #232 -- Page 8
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5306703&postcount=232>

Quote: > Originally Posted byjrakarl➡️So my question is this.. are these units somehow able to be linked together, or are there some specific applications where these units used together can create something that individually they cannot?I have a newly acquired PCM80 and am considering whether a PCM90 would be a worthwhile addition on top of this... ????No, the units don't link up in any way.  I don't remember the line from Steve DeFuria that you quoted, even though I worked with him for years.  It's not untrue, but it's perhaps a little hard to parse.


The PCM80 is an effects unit with a decent 'verb.  You wouldn't use the verb for a main reverb, but it's fine for an individual track.  Its strength is effects and the ability to cascade those effects with reverb.  The PCM90 is strictly reverb with little in the way of effects, and has much stronger reverb.


The two boxes together cover a lot of ground in a mix, but I've never thought of them as a 'system'.


If you're considering a PCM90, you might want to think about a '91 instead.  Same sounds and more, and easier to service.

---

### Post #233 -- Page 8
**User:** Steve Honest
**Info:** Joined: Aug 2006Posts: 1,118My Studio🎧 15 years | Posts: 1,118My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5307089&postcount=233>

hi chaps 

i need to buy a LARC for my 480L

if your seliing one , i would live to hear from you

steve

---

### Post #234 -- Page 8
**User:** Fishmed
**Info:** Joined: Jun 2007Posts: 1,1511 Review written🎧 15 years | Posts: 1,151
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5307434&postcount=234>

Quote: > Originally Posted bySteve Honest➡️hi chapsi need to buy a LARC for my 480Lif your seliing one , i would live to hear from yousteveThere is a WTB (Want to Buy) section in the Classifieds section.

---

### Post #235 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5309023&postcount=235>

Quote: > Originally Posted byNobody Special➡️If you're considering a PCM90, you might want to think about a '91 instead.  Same sounds and more, and easier to service.Hey NS, since you're still floating around here how about chiming in on some of the threads where people are unhappy that their PCM 96s don't work as advertised?


-R

---

### Post #236 -- Page 8
**User:** drBill
**Info:** Joined: Jul 2006Posts: 22,967My Studio🎧 15 years | Posts: 22,967My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5309082&postcount=236>

Quote: > Originally Posted byRKrizman➡️Hey NS, since you're still floating around here how about chiming in on some of the threads where people are unhappy that their PCM 96s don't work as advertised?-RYes.  How about Lexicon addressing some of the issues they have created, and then abandoned.  Lexicon is on the precipice of a huge PR avalanche unless they step up and do the right thing by their customers.


I've been a long standing Lexicon customer, and as of now, I'll never buy another no matter HOW good it is.


So how about it NS?  Care to address any of the issues?


Need a link to that thread?  Here you go.....

[https://gearspace.com/board/high-end...regrets-5.html](https://gearspace.com/board/high-end/465416-lexicon-pcm-96-regrets-5.html)

---

### Post #237 -- Page 8
**User:** SoZo
**Info:** Joined: Dec 2004Posts: 1,226My Studio🎧 20 years | Posts: 1,226My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5309224&postcount=237>

not to mask the above users concerns but I had a question... 


Im currently running it in Nuendo spdif with a Raydat... 


how much different does the PCM91 sound going through its XLR's rather then its spdif ?

---

### Post #238 -- Page 8
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5309291&postcount=238>

Quote: > Originally Posted bydrBill➡️So how about it NS?  Care to address any of the issues?As I've said any number of times, an update to the FW driver is in development right now.  Our best driver engineer has been at it quite a while and currently has the code in internal testing.  There has been considerable work to improve networking stability in addition.  I'm guessing it will be in Beta pretty soon (I think we have enough testers--*please* don't contact me for early copies).


We're hardly ignoring our customers.  Sometimes these things take a while.

---

### Post #239 -- Page 8
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5310962&postcount=239>

Quote: > Originally Posted byNobody Special➡️As I've said any number of times, an update to the FW driver is in development right now.  Our best driver engineer has been at it quite a while and currently has the code in internal testing.  There has been considerable work to improve networking stability in addition.  I'm guessing it will be in Beta pretty soon (I think we have enough testers--pleasedon't contact me for early copies).We're hardly ignoring our customers.  Sometimes these things take a while.Will the new driver address someone running Protools 7.4 on Mac OS 10.411?


Thanks,

-R

---

### Post #240 -- Page 8
**User:** Budda
**Info:** Joined: Jan 2010Posts: 793🎧 15 years | Posts: 793
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5311124&postcount=240>

Not to cross-post (because I've posted in the "Regrets" thread), but quickly:


I was told a beta would be out end last month. Then I was told there was a "breakthrough" on April 2nd, with a beta to be released within about a week. Now I've been told April 23rd. This beta is supposed to run on SL, but is supposed to also enhance any remote control stuff - Ethernet control, FW audio and control. It's apparently tied up with including Harman HiQ (network) stuff, for whatever reason, so it's got to play nice with other devices they may be writing the code for.


So...

If you can hold your breath for a week or so, some of us may be able to know whether they're on the right track or what.


Still been TOO LONG, though.


Then again, 2 years for Bricasti v2 and no one is beeyatching about that. At least their v1 works properly.


Potato, poh-ta-toe. Everyone has their different issues.


Now, back to talking about Lexicon reverbs.


---

## Page 9

---

### Post #241 -- Page 9
**User:** RKrizman
**Info:** Joined: Jun 2002Posts: 7,762🎧 20 years | Posts: 7,762
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5312833&postcount=241>

Quote: > Originally Posted byBudda➡️Then again, 2 years for Bricasti v2 and no one is beeyatching about that. At least their v1 works properly.Potato, poh-ta-toe. Everyone has their different issues.Now, back to talking about Lexicon reverbs.Bricasti V1 works as advertised.


-R

---

### Post #242 -- Page 9
**User:** Larry the O
**Info:** Joined: Dec 2008Posts: 20🎧 15 years | Posts: 20
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5448596&postcount=242>

Well, I've spent WAY too long reading through this entire thread from the top, but it's almost like old home week.


If memory serves (and that's getting to be more questionable by the day), I may be able to fill in a few holes from before NS's time. I arrived at Lexicon in 1979 the week they had release parties for the PrimeTime and 224, rather fortuitous timing in my book. I worked as a bench tech up through the 224X (on which I was the lead tech when it was introduced), and did double-duty working on the Lexicon booth at trade shows. (In those days, it was basically Keith Worsley, Gary Hall, and myself manning the booth.) A good handful of my presets made it into the 224X release. In those days, that was novel and fun.


My recollection of the Constant Density Plate program was that it was pretty consciously a response on Dave G's part to the EMT250. Remember that when the 224 first hit, there was the 250, the QuadEight reverb, and *maybe* one other I'm forgetting, but that was it. And the 250 had established a market for digital reverberators.


The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once. Man, he worked every line of that stuff.


I have always thought that Gary Hall never really fully got his due for the work he did at Lexicon. Gary, who has been a close friend for 35 years, was the person who convinced David to put effects into the 224X. In classic Dave G fashion, he didn't quite understand the applications of the programs Gary was asking him to code, but he trusted Gary enough to believe that there were sufficient people who would have such applications as to justify expending time and energy on them. (I don't believe any of those algorithms have been listed either: Resonant Chords, Multi-band Delays, etc.)


Gary also wrote the microcode for the Super PrimeTime (pretty bug-free code given the size of the honkers he was smoking on the way in to work) and was a strong contributor to the PCM70, the LXP series, the MRC, and a good deal more. He was the first actual musician to be involved in Lexicon marketing, and provided the phenomenally rare service of having fluency in the languages of both the Engineering and Marketing departments. He suffered for serving the go-between role, but it was an invaluable contribution.


And, of course, he was The Man behind the PCM41 and 42. The 41 was a great box, but Gary added some great touches in the 42, including the crude analog limiter in the front end which kept guitarists from slamming the ADC through the roof, and the use of a microcontroller for the front panel. Microcontrollers were brand new at the time, and Lexicon would not authorize Gary to spend any time trying to develop their use, so he did it at home on his own time and brought it in to show them when it was a fait accompli. He also developed a whole family of mods for the 41 and 42, including the memory extension/loop record mod that eventually evolved into the Jam Man.


Re: algorithms. No one has mentioned what might be my favorite Lexicon effect algorithm (tonight; tomorrow I might have a different favorite), which was the Chorus program. Why did I like the Chorus program so much? Because in the 224X it used the same random modulation on the delay voices that was used in the reverberators, rather than LFO modulation of the voices. What a difference! 


The "random chorus" (as it was never called) made it as far as PCM70 v3 software, but the one preset using it was gone in the v4 software. Consequently, I kept one of my PCM70s at v3. 


Did anyone mention the Split Halls and Plates and the Plate/Chorus algorithms?


The introduction of digital reverb at Lexicon obviously changed things forever. One of the ways it did that was that Dave G brought a much more systematic and rigorous listening evaluation program (as one might expect from a professor of low-energy nuclear physics) to product development there than had been used before.

---

### Post #243 -- Page 9
**User:** Sounds Grand
**Info:** Joined: May 2010Posts: 94🎧 15 years | Posts: 94
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5448989&postcount=243>

Quote: > Originally Posted byLarry the O➡️Well, I've spent WAY too long reading through this entire thread from the top, but it's almost like old home week.If memory serves (and that's getting to be more questionable by the day), I may be able to fill in a few holes from before NS's time. I arrived at Lexicon in 1979 the week they had release parties for the PrimeTime and 224, rather fortuitous timing in my book. I worked as a bench tech up through the 224X (on which I was the lead tech when it was introduced), and did double-duty working on the Lexicon booth at trade shows. (In those days, it was basically Keith Worsley, Gary Hall, and myself manning the booth.) A good handful of my presets made it into the 224X release. In those days, that was novel and fun.My recollection of the Constant Density Plate program was that it was pretty consciously a response on Dave G's part to the EMT250. Remember that when the 224 first hit, there was the 250, the QuadEight reverb, and *maybe* one other I'm forgetting, but that was it. And the 250 had established a market for digital reverberators.The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once. Man, he worked every line of that stuff.I have always thought that Gary Hall never really fully got his due for the work he did at Lexicon. Gary, who has been a close friend for 35 years, was the person who convinced David to put effects into the 224X. In classic Dave G fashion, he didn't quite understand the applications of the programs Gary was asking him to code, but he trusted Gary enough to believe that there were sufficient people who would have such applications as to justify expending time and energy on them. (I don't believe any of those algorithms have been listed either: Resonant Chords, Multi-band Delays, etc.)Gary also wrote the microcode for the Super PrimeTime (pretty bug-free code given the size of the honkers he was smoking on the way in to work) and was a strong contributor to the PCM70, the LXP series, the MRC, and a good deal more. He was the first actual musician to be involved in Lexicon marketing, and provided the phenomenally rare service of having fluency in the languages of both the Engineering and Marketing departments. He suffered for serving the go-between role, but it was an invaluable contribution.And, of course, he was The Man behind the PCM41 and 42. The 41 was a great box, but Gary added some great touches in the 42, including the crude analog limiter in the front end which kept guitarists from slamming the ADC through the roof, and the use of a microcontroller for the front panel. Microcontrollers were brand new at the time, and Lexicon would not authorize Gary to spend any time trying to develop their use, so he did it at home on his own time and brought it in to show them when it was a fait accompli. He also developed a whole family of mods for the 41 and 42, including the memory extension/loop record mod that eventually evolved into the Jam Man.Re: algorithms. No one has mentioned what might be my favorite Lexicon effect algorithm (tonight; tomorrow I might have a different favorite), which was the Chorus program. Why did I like the Chorus program so much? Because in the 224X it used the same random modulation on the delay voices that was used in the reverberators, rather than LFO modulation of the voices. What a difference!The "random chorus" (as it was never called) made it as far as PCM70 v3 software, but the one preset using it was gone in the v4 software. Consequently, I kept one of my PCM70s at v3.Did anyone mention the Split Halls and Plates and the Plate/Chorus algorithms?The introduction of digital reverb at Lexicon obviously changed things forever. One of the ways it did that was that Dave G brought a much more systematic and rigorous listening evaluation program (as one might expect from a professor of low-energy nuclear physics) to product development there than had been used before.One of the best posts I have ever seen on gearslutz


Thanks!

---

### Post #244 -- Page 9
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5449072&postcount=244>

Yep - great post!

---

### Post #245 -- Page 9
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5450580&postcount=245>

Thanks Larry.  Good post.  Gary went on to do a lot of good work at Sonic Solutions as well.

---

### Post #246 -- Page 9
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5497369&postcount=246>

Quote: > Originally Posted byLarry the O➡️My recollection of the Constant Density Plate program was that it was pretty consciously a response on Dave G's part to the EMT250.Apparently the timing of the first several reflections in the CD Plate matches the EMT250 early reflections pretty closely.

Quote: > The first programs were, indeed, only 100 lines of microcode; I can remember David being delighted at the realization of a code change he could make that would remove lines from two different code functions at once.Is there a chance that Griesinger moved from the original Schroeder allpass topology to the 2-multiply topology that Moorer introduced in his 1979 paper? This seems like it could make things more efficient.

Quote: > (I don't believe any of those algorithms have been listed either: Resonant Chords, Multi-band Delays, etc.)Seems like these would be worthy additions to the thread.

Quote: > Re: algorithms. No one has mentioned what might be my favorite Lexicon effect algorithm (tonight; tomorrow I might have a different favorite), which was the Chorus program. Why did I like the Chorus program so much? Because in the 224X it used the same random modulation on the delay voices that was used in the reverberators, rather than LFOWas this similar to the randi type modulation found in the Music-N languages, or something different? Also, did each of the voices have independent modulation? 


I used the 224XL chorus back in 1992 in a studio recording, and it is an INCREDIBLE sound. My guess is that the Lexicon chorus was a "secret weapon" for Eno/Lanois during the 1980's - a DX7 doesn't sound that lush on its own.


Thanks for your detailed post.

---

### Post #247 -- Page 9
**User:** Larry the O
**Info:** Joined: Dec 2008Posts: 20🎧 15 years | Posts: 20
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5519632&postcount=247>

Quote: > Originally Posted byseancostello➡️Apparently the timing of the first several reflections in the CD Plate matches the EMT250 early reflections pretty closely.Is there a chance that Griesinger moved from the original Schroeder allpass topology to the 2-multiply topology that Moorer introduced in his 1979 paper? This seems like it could make things more efficient.Well, the timing of all of this is key. I remember Dave telling me how he came to design what became the Lexicon reverb. He was both a classical musician (vocalist) and recording engineer. He was recording a lot of music in really horrible sounding churches and such around Boston, so he often would more or less close mic to minimize how much of the natural reverb he captured. (He didn't close mic as in pop production, but closer than he would have preferred for classical.)


Since his recordings now didn't have enough ambience, he set out to find a way to add more. He said he tried everything: setting up speakers in good-sounding spaces and recording that, plate reverbs, etc. None of it pleased him. 


As a professor at Harvard, he had become aware of these new things called "microprocessors" and set out teaching himself how to program them. He then combed ten years of back issues of the AES Journal to see what he could find about digital reverb and found nothing, so he proceeded on his own to breadboard a prototype digital reverb. In this case, the breadboard was literally a piece of plywood with the circuitry affixed to it.


He got it working, but was not able to get it to sound right. Around this time, he bumped in Barry Blesser and mentioned what he was doing. Blesser asked him if he had started with the Schroeder algorithms and Dave said, "The what?" It turns out that Schroeder's original reverb papers had appeared in AES Journal *fifteen* years before, which is why he hadn't found them only combing the previous ten years' journals. (Just goes to show how far ahead of his time ol' Manfred was!)


David got the Schroeder papers and tried the algorithms, but he described the Schroeder algorithms to me as sounding like "nasty little rooms." Still, they set him on the right track and he went about modifying and further developing some of Schroeder's concepts, as well as introducing some of his own. Eventually, he started to get it to sound pretty good.


He had gotten wind of the existence of Lexicon, who was, at the time, making the Delta-T series of digital delays and the Varispeech, a forgotten product for the blind that was WAY ahead of its time: a variable-speed Wollensak cassette recorder with a custom chip in it that provided pitch shift to compensate for the upward shift when the cassette deck was speeded up. Keep in mind, this is the mid- to late-1970s, and these guys were doing pitch shifting and custom ICs!


Anyway, David went to a Boston AES chapter meeting, walked up to Dr. Francis Lee (the inventor of digital delay and founder of Lexicon), who was attending the meeting with David Dunetz, a Lexicon engineer, and said to them "I have something you want. You need to come hear it."


Lee and Dunetz were a bit nonplussed at this direct approach, but they followed up and thus did Lexicon acquire Dave G's reverb and his services.


Now, as I mentioned the 224 was released in mid-1979, so David certainly had not seen Andy's paper. At the time, there were maybe half a dozen people in the world fooling with digital reverb, Dave G and Andy M being two of them. (Tony Agnello of Eventide was another.) That's not to say that David didn't use any of the techniques Andy suggested, I don't know about that one way or another. But my understanding is that he worked quite alone in his development, though I'm sure he got some feedback, tips, and kibitzing from Blesser and a few other choice friends.

Quote: > Was this similar to the randi type modulation found in the Music-N languages, or something different? Also, did each of the voices have independent modulation?My recollection is that the voices all have independent modulation, which is why it sounded so great.

Quote: > I used the 224XL chorus back in 1992 in a studio recording, and it is an INCREDIBLE sound. My guess is that the Lexicon chorus was a "secret weapon" for Eno/Lanois during the 1980's - a DX7 doesn't sound that lush on its own.That program is one of the biggest reasons I intend to resurrect my 224X by hook or by crook.

Quote: > Thanks for your detailed post.My pleasure. Best that I get some of that stuff on the record before I am entirely feeble.


Maybe I already said this (warning: approaching feebleness!), but back in '86 or so I convened a roundtable discussion on digital reverb with Dave G, Tony Agnello, Andy Moorer, Richard Neatrour (from ART), and one other person I can't remember right now. The discussion appeared as a five-part series (!) in Mix magazine. Sometime before too long, I hope to post that in the Article Archives on my website ([Toys In the Attic](http://www.toysintheattic.org)).


One of the things I remember from that is Tony Agnello fantasizing about being able to have a reverb where you could design a room and all the materials in it...exactly what Universal Audio's Dreamverb (and probably some other reverbs) now does.

---

### Post #248 -- Page 9
**User:** Larry the O
**Info:** Joined: Dec 2008Posts: 20🎧 15 years | Posts: 20
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5519637&postcount=248>

Oh, and just to fill in a bit more of Gary Hall's CV:


he also worked for Sony supporting their earliest digital recorders, mixer, and editor. He did that for six months with neither training nor schematics! I believe when he left Sony was when he returned for his second stint at Lexicon (glutton for punishment).


I believe he worked for Auris, a very early virtualization company started by some guys from U of I Champaign Urbana, and he was a technical editor for Electronic Musician for several years. THEN he went to Sonic Solutions. He worked for another DVD authoring manufacturer after Sonic Solutions, then decided to retire to Thailand, where he lives now.

---

### Post #249 -- Page 9
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5519860&postcount=249>

Thank you very much for this great information.

Quote: > Originally Posted byLarry the O➡️Maybe I already said this (warning: approaching feebleness!), but back in '86 or so I convened a roundtable discussion on digital reverb with Dave G, Tony Agnello, Andy Moorer, Richard Neatrour (from ART), and one other person I can't remember right now. The discussion appeared as a five-part series (!) in Mix magazine. Sometime before too long, I hope to post that in the Article Archives on my website (Toys In the Attic).I will be looking forward to read it

---

### Post #250 -- Page 9
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5524894&postcount=250>

Wow, thanks for the history! A few questions:

Quote: > Originally Posted byLarry the O➡️Now, as I mentioned the 224 was released in mid-1979, so David certainly had not seen Andy's paper. At the time, there were maybe half a dozen people in the world fooling with digital reverb, Dave G and Andy M being two of them. (Tony Agnello of Eventide was another.) That's not to say that David didn't use any of the techniques Andy suggested, I don't know about that one way or another. But my understanding is that he worked quite alone in his development, though I'm sure he got some feedback, tips, and kibitzing from Blesser and a few other choice friends.Do you know if Griesinger had read the Michael Gerzon reverb papers from Studio Sound at that point? Gerzon introduces nested allpasses in his 1972 paper. I know that Griesinger mentioned Gerzon's papers in his 1989 AES paper, but this doesn't mean that he had read the Gerzon papers by the time of the 224. The nested allpass concept was originally described by Schroeder in his 1962 AES paper, but it is unclear if Schroeder grasped how it was a far different algorithm than just using 5 allpasses in series.

Quote: > That program is one of the biggest reasons I intend to resurrect my 224X by hook or by crook.How similar is the PCM70 Chorus algorithm to that in the 224X?

Quote: > Maybe I already said this (warning: approaching feebleness!), but back in '86 or so I convened a roundtable discussion on digital reverb with Dave G, Tony Agnello, Andy Moorer, Richard Neatrour (from ART), and one other person I can't remember right now. The discussion appeared as a five-part series (!) in Mix magazine. Sometime before too long, I hope to post that in the Article Archives on my website (Toys In the Attic).I look forward to seeing those!

---

### Post #251 -- Page 9
**User:** SIXTWOFOUR
**Info:** Joined: Feb 2010Posts: 665My Studio🎧 15 years | Posts: 665My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5540725&postcount=251>

I will say that I have a lexicon 200 and a 480L and nothing does what they do. I have almost every other reverb made and nothing sounds like a lexicon. BTW there new stff does not compare to there old stuff. I also have a bricasti and it destroys the NEW Lexicon stuff but I will never sell my 480!

---

### Post #252 -- Page 9
**User:** Beyersound
**Info:** Joined: Dec 2007Posts: 3,803My Studio1 Review written🎧 15 years | Posts: 3,803My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5540780&postcount=252>

Quote: > Originally Posted byLarry the O➡️Re: algorithms. No one has mentioned what might be my favorite Lexicon effect algorithm (tonight; tomorrow I might have a different favorite), which was the Chorus program. Why did I like the Chorus program so much? Because in the 224X it used the same random modulation on the delay voices that was used in the reverberators, rather than LFO modulation of the voices. What a difference!The "random chorus" (as it was never called) made it as far as PCM70 v3 software, but the one preset using it was gone in the v4 software. Consequently, I kept one of my PCM70s at v3.Nice post Larry! You reminded me of something I hadn't thought about for years. I had forgotten how much I loved that Chorus program as well. Back in the early 90s I had the pleasure of mixing Warren DiMartini (and Ratt) live. He had one of the best guitar sounds I have have ever heard to this day. He used a ver3 PCM-70 into a Soldano with that same amazing chorus. I have worked with many great guitarists and tones, but that Lexicon was just flat out the best I ever heard in a guitar rig. What's cool is that the sound is used in the studio through his rig all through the Mike Shipley mixed "Detonator" record, and shimmers like nothing else. Anyone who hasn't heard that chorus should take a listen to that record (Shipley's mix kicks a**!).  Thanks Larry

---

### Post #253 -- Page 9
**User:** rapfreak
**Info:** Joined: Jun 2005Posts: 2,835🎧 20 years | Posts: 2,835
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5565605&postcount=253>

Quote: > Originally Posted byLarry the O➡️That program is one of the biggest reasons I intend to resurrect my 224X by hook or by crook.The last time I talked to Jim Fabiano (a month or so ago) he still has a number of parts for the 224's.

---

### Post #254 -- Page 9
**User:** Voyage.One
**Info:** Joined: May 2010Posts: 766My Studio🎧 15 years | Posts: 766My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5591032&postcount=254>

I'm still waiting for when somewhone can algorithmically

model the Byzantine Cistern

---

### Post #255 -- Page 9
**User:** jrakarl
**Info:** Joined: Jul 2009Posts: 992My Recordings/CreditsMy Studio4 Reviews written🎧 15 years | Posts: 992My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5596100&postcount=255>

Quote: > Originally Posted byNobody Special➡️The two boxes together cover a lot of ground in a mix, but I've never thought of them as a 'system'.If you're considering a PCM90, you might want to think about a '91 instead.  Same sounds and more, and easier to service.Hi NS.  Thank you for your response and thank you so much for being an active part of the community.  Folks like you and Larry add enormous value.

I've since purchased a PCM70 and will certainly consider a '91  when it comes time for me to invest in newer equipment.  


Kind regards,

Julian

---

### Post #256 -- Page 9
**User:** ianm2
**Info:** Joined: May 2009Posts: 41🎧 15 years | Posts: 41
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5890998&postcount=256>

wow this is an incredible thread very informative.


I am a llittle confused as to the first post, you say some algorithms are only just 1st introduced into the pcm96, wheras its quite obvious that a pcm80 has halls and rooms, whilst I applaud your total transparancy, its not entirely obvious, a slight contradiction however you say below that one, can't remember, hall or room is actually closer to a diffferent algorithm so that must be the case with the contradictory one.


There are a few things I would like to ask and hope you would be gracious enough to explain them.


1/Whilst I understand that the comlplexity is in the programming, the 480l is revered but really is quite ancient, one would have thought the electronics design would limit it and it would be quite easy to surpass, measurement-wise, is the programmikng THAT good that even things say 10 years later llike the pcm91 can't approach it? must be something then....


2/ a few algos in the 480 I don't really get...


1/ teh prime times, I am trying to relate them to conventional delays, so max pitch event would be oscillator rate? and max pitch change mod. depth? I can see you;'ve tried to extend the ability of the modulation, but I just don't quite get the controls, its a bit obtuse.


2/ the 40 voice fx, again, how can you thicken without detuning?


3/ in the pcm80/1 the glide algo again, I haven't a clue what a 2 tap glide delay is really, as far as I can tell, glide simply means pitch change/mod, as in a conventional mod. delay time with a lfo. sometimes these changes of lingo are unhelpful as one cannot really grasp the concepts.


and if it pitch mods, why the need for a separate chorus algo?


these above are changes on conventional fx that have never been done by anyone else, why? ppl like TC elec. are, equally respected for their quality, and am sure are capable of it, one wonders...I feel any new twist on fx is useful, we all get a bit bored of a mod. dly after a while...


its fascinating to see your orignal mans ideas on new algos that he thoght the concet hall wasn't worth re-implementing? 


why did he think that? I am qutie fascinated about design decisions, why one thing is done and another not.


please try to take a few mins to answer my questions, I appreciate your time and thanks for your input, lovely to see a maker doing such

---

### Post #257 -- Page 9
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5892208&postcount=257>

Hi.  I'm sorry, but I'm going to have to pick and choose on answers to your questions.  I'm a bit busy, but more importantly, I haven't recently had my hands on some of the pieces you ask about.  It's one of the perils of R&D: I know a lot more about what I'm doing now than what I did then.

Quote: > Originally Posted byianm2➡️am a llittle confused as to the first post, you say some algorithms are only just 1st introduced into the pcm96, wheras its quite obvious that a pcm80 has halls and rooms, whilst I applaud your total transparancy, its not entirely obvious, a slight contradiction however you say below that one, can't remember, hall or room is actually closer to a diffferent algorithm so that must be the case with the contradictory one.You do run out of names after a while.  "Hall" is still the best description of a particular type of reverb, even if the details have changed.  The PCM96 (as well as our newer plugins) certainly includes many architectural aspects of early boxes like the 480, 81, etc.  But it introduces many other new concepts. While it has the character of older boxes in many regards, it goes places the others can't.
Quote: > 1/Whilst I understand that the comlplexity is in the programming, the 480l is revered but really is quite ancient, one would have thought the electronics design would limit it and it would be quite easy to surpass, measurement-wise, is the programmikng THAT good that even things say 10 years later llike the pcm91 can't approach it? must be something then....The 480L is a creature of its age.  In terms of bit depth, CPU speed, audio quality or any other measurement, it is orders of magnitude behind what's available now.  In spite of that, many people like it specifically because of the many artifacts, and perhaps because of their long experience with it.  If someone is happily mixing with a 480L, the last thing I would do is to try to talk them out of it.  I do appreciate some aspects of that character, and have brought them forward.  I've been less interested in re-introducing quantization error and coefficient zippering.

Quote: > these above are changes on conventional fx that have never been done by anyone else, why? ppl like TC elec. are, equally respected for their quality, and am sure are capable of it, one wonders...I feel any new twist on fx is useful, we all get a bit bored of a mod. dly after a while...A lot of the effects have become so much a part of mixing vocabulary that you exclude them at your peril.  There *are* some pretty weird new effects in the PCM96, though.  For example the multivoice pitch shifter is a complex delay with separate pitch shifts on each tap.

Quote: > its fascinating to see your orignal mans ideas on new algos that he thoght the concet hall wasn't worth re-implementing?why did he think that?Dave G is a classical musician.  So am I (played a bit of rock several decades ago, but that was then).  We're both interested in unobtrusive, natural modeling of space.  ConcertHall isn't exactly unobtrusive, so Dave bypassed it in favor of more promising directions.  I do think the sound is pretty neat, and I'm glad it's back, but I couldn't imagine using it in a mix of classical music.


NS

---

### Post #258 -- Page 9
**User:** ianm2
**Info:** Joined: May 2009Posts: 41🎧 15 years | Posts: 41
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5894777&postcount=258>

this is just a comment post, so no need to reply to it, I appreciate your busy.


I read the first post and a few pages with great interest, but by the time I made my reply, I had forgotten the specifics of the particular algorithms you mentioned, but I was aware one of them, hall or room, that you said was new, had appeared long ago, you mentioned 2 of them with a qualifier on one that it was closer to a different algo. so I assumed that must've been the case with the other, as well.


In reality, I should have checked the first post again, but I wasn't really terribly anal about that point really, it merely appeared from the readers POV contradictory or with some error, however, I knew like I said there must've been some explanation from where you where coming from.


Its not important.


perhaps as a theoretical point, it MAY be interesting to incoroporate a "best of" not in preset types, but perhaps algos that appeared in other units, eg. make an all in one device that would replace all these revered units so you could have all the old ones and the new one, too in one box, but that would be perhaps nigh on a lifetimes work. be nice tho'


evey lex unit in one box uncompromised. hah imagine that


to engineers and companies, items are merely a job to be implemented, and a tool to make profit, us gearsluts come to know and love these as items of history and indispensible work tools, we recognise the sweat, hard work and long hours you make and appreciate the engineering quality, sadly many of them have disappeared into obscurity, other items I refer to, 


sadly perhaps, some makers consider certain devices to be a loser, inconvenience where we cherish and love them, I partic. refer to jap mass production items here, some of which are being re-discovered, of any nature. what was once muck has suddenly become a diamond.


say a classic car for instance, you buy a car one day, find out its great, love and cherish it over the years, then call the maker one day, being a nerdish sad jerk, and the maker thinks you are mad, that car is 20 years old, the people who designed and built it are long retired or dead, we have no info on it.


yes but we have lived with it,and have come to love it and wish to know more about it, surely for something so great you must've kept archives and libraries of records?


nope...its just a job, a product, we have much better things now, things move on so fast, that'll never make us money anymore...


that's a kind of consumer vs. maker POV.


I am waffling but the point is, some of us get a little rose tinted and sentimental about some things in the past for some reason, I think its to do with the modern things being a bit teccy and lacking in character, the failings of the time instill some character which progress takes away.


here's a q., perhaps sensitive...!!


are you able to give us some insight into the direction lexicon is now heading, ie a kind of roadmap, it seems to be at some kind of mid life crisis ( some of the products have been bizarre, a foray into guitar amps, a very good one BTW, home theatre multi channel power amps) hint stick with what your good at, ie DSP implementation of fx


, perhaps a bit harsh, but in the new age, one always has to question ones direction and way forward. what I meant was its an awkard time, probly always has been. any new items planned that your at liberty to divulge?


meant in the nicest way.thanks again! always nice to speak with someone who takes time esp. a maker, Intel were superb once to me, I phoned them on a holiday and someone was SO helpful.


I almost forgot, this is an intersting point, I am sure you have, well, considered a sampling reverb, on the lines of a sony or yamaha one, and presumable rejected it.


these are expensive devices and are meant to be good, however, in the synth arena, modelling synths are considered superior to sample and synthesize, however, it appears to be the opposite in the reverb world, a sampled space is better than a dsp reproduced one...that is an apparent contradiction


as an aside, I notice on the rear of the 960 there is a cheap computer switch mode psu to power it...no nvidia sli gaming hi end power supplies..may make it sound better

---

### Post #259 -- Page 9
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5894961&postcount=259>

As for product "consumer" vs maker point of view, no one in the company dismisses the old products' sound quality in any way and if anything, many explanations and observations of factors that affect the perception of sound quality in the old products have been made by some in the company as well as customers. Along with that, the current reverb designer in the company has explained his perspective and preferences that affected his design aesthetics.


People forget that behind the brands and products there are individuals responsible for a "product" and that the sound design behind this type of product is, after all, in very big part an art and not just a bunch of technicalities. One cannot be expected to do a good artwork if he's not passionate about it and if it doesn't fit his personal preferences. Just like you can't expect a song writer or a painter to produce something in the style of another, the same applies here. You know one may be able to imitate another, but it's far from guaranteed to have the same effect, especially if the maker was not passionate about it.


So, it's not really about "we have moved on", it's about "that was then, this is now" and "person A is not person B and therefore product A is not product B" and "in a perfect world, machine code could be perfectly or even feasibly portable between vastly different machines, but it's not".


Regarding "sampled space is better", I disagree to say the least, not just because this method has many technical flaws, but because it never sounds nearly as good as a good algorithm to me and it doesn't even matter if the sampled impulse response was taken in a world class concert hall, it always sounds like a bad, rough sketch compared to it, unsurprisingly.

---

### Post #260 -- Page 9
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5896508&postcount=260>

Quote: > Originally Posted byianm2➡️are you able to give us some insight into the direction lexicon is now headingNorth!  No, I mean West...  Sorry, but I really can't talk about things in the queue or a longer term roadmap.  The guitar amps are ten years gone.  The home theater stuff has long been worked on by a completely different group of engineers, although we're happy to share ideas.


I really do appreciate your interest.  Sorry I'm not able to offer longer responses.


NS

---

### Post #261 -- Page 9
**User:** nickelironsteel
**Info:** Joined: Jul 2012Posts: 2,652🎧 10 years | Posts: 2,652
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8230254&postcount=261>

Ive stumbled across the term "Constant Density" a lot of times... does anyone know which reverbs use this design, cause i appear to be a sucker for what they do to a mix

---

### Post #262 -- Page 9
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8230355&postcount=262>

Quote: > Originally Posted bynickelironsteel➡️Ive stumbled across the term "Constant Density" a lot of times... does anyone know which reverbs use this design, cause i appear to be a sucker for what they do to a mixYes.


The most popular constant density reverbs on the market were the EMT 250, AMS RMX16, the SONY DRE 2000, SONY MUR-201 / IBANEZ SDR 1000, SONY R7, etc... The Ensoniq DP/2 and DP/4 and DP/pro have separate diffusion parameters for the input and the "tank" network, so you can create constant density reverbs with them as well.


The telltale characteristic of a constant density algorhythm is that the reflection pattern repeats (sounds a bit  like a pebble skimming across water), where a "non-constant density" algo grows more dense and diffuse as the reverb decays.

---

### Post #263 -- Page 9
**User:** Ghosted
**Info:** Joined: Jul 2012Posts: 677🎧 10 years | Posts: 677
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8230586&postcount=263>

I have a PCM96 Surround and a 300. What's the closest algorithm to the "Random Ambiance" from the 300 on the 96? I love that algorithm.

---

### Post #264 -- Page 9
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8231521&postcount=264>

Quote: > Originally Posted byGhosted➡️I have a PCM96 Surround and a 300. What's the closest algorithm to the "Random Ambiance" from the 300 on the 96? I love that algorithm.The Random Ambience algorithm is not available on the PCM96 - I believe the closest algorithm would be Room (with all the different ER patterns).

---

### Post #265 -- Page 9
**User:** nickelironsteel
**Info:** Joined: Jul 2012Posts: 2,652🎧 10 years | Posts: 2,652
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8231878&postcount=265>

Quote: > Originally Posted byzmix➡️Yes.The most popular constant density reverbs on the market were the EMT 250, AMS RMX16, the SONY DRE 2000, SONY MUR-201 / IBANEZ SDR 1000, SONY R7, etc... The Ensoniq DP/2 and DP/4 and DP/pro have separate diffusion parameters for the input and the "tank" network, so you can create constant density reverbs with them as well.The telltale characteristic of a constant density algorhythm is that the reflection pattern repeats (sounds a bit  like a pebble skimming across water), where a "non-constant density" algo grows more dense and diffuse as the reverb decays.thanks, let me be more precise model-wise: how about the 


EMT 244, 245, 246, 251, 252?

SONY: so basically all sony reverbs except the DRE777?

LEXICON 224, 224X, 224XL, M300, 300L, 480L ?

QUANTEC QRS, QRS/XL, Yardstick 2402

URSA MAJOR SST-282

YAMAHA REV 1, REV 5, REV 7


cheers, this helps a lot explaining to me why i dig those units so much

---

### Post #266 -- Page 9
**User:** cowudders
**Info:** Joined: Jan 2006Posts: 1,022🎧 20 years | Posts: 1,022
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8236422&postcount=266>

Quote: > Originally Posted byWarp69➡️The Random Ambience algorithm is not available on the PCM96 - I believe the closest algorithm would be Room (with all the different ER patterns).According to Mr. Carnes, the Early Reflections are time-variant in the 300 and 960. 

(EDIT: According to Mr. Carnes it's really only the 960, that has time-variant ER's.)

The Room algo in the Native Bundle (I suppose it's the same on the hardware, eg 96 + 92) is not, according to my tests.


Any chance for the random ambience in your LX plug, Mr. Warp?

---

### Post #267 -- Page 9
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8237240&postcount=267>

Quote: > Originally Posted bycowudders➡️According to Mr. Carnes, the Early Reflections are time-variant in the 300 and 960.On further--ahem--reflection, I don't think the 300 had time-variant early stuff.  It was as direct a port of the 480 as Dave and Frank Cunningham could make it.  I think the 960 was the only beast with randomized reflections.

---

### Post #268 -- Page 9
**User:** Ghosted
**Info:** Joined: Jul 2012Posts: 677🎧 10 years | Posts: 677
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8237256&postcount=268>

Quote: > Originally Posted byDeleted Nobody Special ➡️On further--ahem--reflection, I don't think the 300 had time-variant early stuff.  It was as direct a port of the 480 as Dave and Frank Cunningham could make it.  I think the 960 was the only beast with randomized reflections.Correct, on the 300 the early reflections consist of a matrix of static delays around the reverberator.

---

### Post #269 -- Page 9
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8238870&postcount=269>

Quote: > Originally Posted byDeleted Nobody Special ➡️I don't think the 300 had time-variant early stuff.  It was as direct a port of the 480 as Dave and Frank Cunningham could make it.  I think the 960 was the only beast with randomized reflections.The Random Ambience algorithm from 480L does have randomized delays controlled by the Wander parameter. It can't be a direct port if the 300 doesn't have randomized delays. Is "Wander" then a dummy parameter on the 300 version of the 'Random' Ambience algorithm?

---

### Post #270 -- Page 9
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8238877&postcount=270>

Quote: > Originally Posted byWarp69➡️The Random Ambience algorithm from 480L does have randomized delays controlled by the Wander parameter. It can't be a direct port if the 300 doesn't have randomized delays. Is "Wander" then a dummy parameter on the 300 version of the 'Random' Ambience algorithm?The "Wander" parameter definitely makes a difference tweaking the 300. But it might not affect the ER, only the tail.


---

## Page 10

---

### Post #271 -- Page 10
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8238891&postcount=271>

Quote: > Originally Posted byliving sounds➡️The "Wander" parameter definitely makes a difference tweaking the 300. But it might not affect the ER, only the tail.What happens if you dial down the tail by using 'LEV'? Rememer that Wander needs a non-zero Spin value to function.

---

### Post #272 -- Page 10
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8239479&postcount=272>

Quote: > Originally Posted byWarp69➡️What happens if you dial down the tail by using 'LEV'? Rememer that Wander needs a non-zero Spin value to function.Just tested it, the randomization (at least using the "Random Hall" algorithm) only affects the reverb, not the delays. The structure diagram makes this clear as well: The incoming signal ist first diffused, then gets fed into the "reverberator" module and the delay lines in parallel. Since the spin and wander parameter both reside inside the "reverberator" module the delays on the "outside" are unaffected. The signal resulting from the "reverberator" module as well as the two delay lines per channel then get summed into a low pass filter, that's it.

---

### Post #273 -- Page 10
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8239598&postcount=273>

Quote: > Originally Posted byliving sounds➡️Just tested it, the randomization (at least using the "Random Hall" algorithm) only affects the reverb, not the delays.We were talking about the Random Ambience algorithm 


If you turn down the reverb tail with the RLVL parameter you would only get the early reflections part.


I can see that the parameter range is different between 480L and 300L

---

### Post #274 -- Page 10
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8239658&postcount=274>

Quote: > Originally Posted byWarp69➡️We were talking about the Random Ambience algorithmIf you turn down the reverb tail with the RLVL parameter you would only get the early reflections part.I can see that the parameter range is different between 480L and 300LOK, checked that one, too. Random Ambience is different, even with the reverb level all the way down (delays only) spin/wander affect the signal. The diagram says different and is obviously incorrect.

---

### Post #275 -- Page 10
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8239701&postcount=275>

Quote: > Originally Posted byliving sounds➡️OK, checked that one, too. Random Ambience is different, even with the reverb level all the way down (delays only) spin/wander affect the signal. The diagram says different and is obviously incorrect.You can't use the diagram as such - the Random Ambience actually has three parts : DELAY (DRY) + ER + REV. This is not displayed in the manual where ER + REV is shown as one block.


When the Reverb Level is way down, you still get the sound of the ER part. As I can understand from your post - there're infact randomized delay lines in the ER part of the Random Ambience algorithm in the 300L, just like in the 480L.

---

### Post #276 -- Page 10
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8239744&postcount=276>

Quote: > Originally Posted byWarp69➡️When the Reverb Level is way down, you still get the sound of the ER part. As I can understand from your post - there're infact randomized delay lines in the ER part of the Random Ambience algorithm in the 300L, just like in the 480L.There have to be, since the randomization parameters audibly affect the signal even with reverb level all the way down.

---

### Post #277 -- Page 10
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8239920&postcount=277>

Quote: > Originally Posted bynickelironsteel➡️thanks, let me be more precise model-wise: how about theLEXICON 224, 224X, 224XL, M300, 300L, 480L ?224, 224X, and 224XL have the Constant Density Plates. The other algorithms all have density that increases with time, although this can be controlled by the DEFINITION parameter in some algorithms.

Quote: > QUANTEC QRS, QRS/XL, Yardstick 2402Echo density increases with time. The Yardstick has a parameter (diffusion? I don't remember) that may allow the reverb to become a sparse constant density reverb.

Quote: > URSA MAJOR SST-282Density increases with time, in a really weird and unstable way. The Lexicon and Quantec reverbs use allpass delays embedded within larger delay loops to increase the echo density, but the SST uses a whole bunch of time varying taps summed together for its feedback signal. This will increase the echo density over time, but the feedback gain is limited before things blow up. The time variation allows the feedback gain to be increased by about 3X, but this still results in a fairly short maximum decay time, compared to the Lexicon and Quantec units.

---

### Post #278 -- Page 10
**User:** Ghosted
**Info:** Joined: Jul 2012Posts: 677🎧 10 years | Posts: 677
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8240621&postcount=278>

Quote: > Originally Posted byMichael Carnes➡️Do I have plans for additional algorithms?  Yes.  I can't say anything about them until we release them, but the DSP has the power to do many interesting things.Please try and port over the "Random Ambiance" algorithm into the PCM96 Surround. It's the only one I really miss on that box.


Is it possible to add a "quality" control, some sort of quantize noise parameter to more accurately imitate the old units? The verbs on the 96 sound *too clean* sometimes. Dirt can be an effect in itself.


The "band pass delays" algorithm from the PCM-80 is another classic.


Just ideas...

---

### Post #279 -- Page 10
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8240951&postcount=279>

Quote: > Originally Posted byGhosted➡️Please try and port over the "Random Ambiance" algorithm into the PCM96 Surround. It's the only one I really miss on that box.Is it possible to add a "quality" control, some sort of quantize noise parameter to more accurately imitate the old units? The verbs on the 96 soundtoo cleansometimes. Dirt can be an effect in itself.Sorry I can't help you.  I haven't been with Lexicon since early January.  Any decisions about new stuff at Lex are out of my hands.


I've experimented with some dirty stuff (I didn't die--I'm just not at Lex) and found it to be pretty challenging. The real things that add the dirt are not always obvious and seem to rely on a somewhat 'compromised' data pathway from start to finish. Floating point just doesn't lend itself to that sort of stuff.  Don't get me wrong--you can add schmutz, but it doesn't sound the same.  I'm probably not going to spend any more time on that experiment for quite some time.

---

### Post #280 -- Page 10
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8240988&postcount=280>

Quote: > Originally Posted byseancostello➡️224, 224X, and 224XL have the Constant Density Plates. The other algorithms all have density that increases with time, although this can be controlled by the DEFINITION parameter in some algorithms.That's an interesting topic, but not really for the reasons we think.  I'm sure Sean is more than a little aware of this, but even the non-constant-density reverbs hit a brick wall in terms of the number of reflections.  The Nyquist theorem is in full force.  At 44.1, you quite simply can't have more than 22K reflections in a second, no matter how many allpasses or how long the tail.


The group delay that we moan about (for good reasons--it is the cause of many reverbs sounding metallic) also brings along some real benefits. Even though the maximum density of the reverb is reached pretty quickly, the pseudo-reflections line up against one another in different patterns as the sound ages. Although the tail appears to have a pretty regular spectral signature--typically the highs die away faster--in a local sense the frequency response is much more irregular.  It's not truly chaotic, but it has a certain chaotic sense.


In the same way that the frequency response is irregular in a moment-to-moment sense, the phase of various frequencies relative to one another is also changing rapidly (if they're going through a typical network of long allpasses). This is a very helpful feature in maintaining mono/stereo compatibility, and also is more natural-sounding as long as group delay issues are managed well.


So in a certain very real sense, all reverbs are constant density after a couple-hundred milliseconds or so.

---

### Post #281 -- Page 10
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8241054&postcount=281>

Quote: > Originally Posted byMichael Carnes➡️I've experimented with some dirty stuff (I didn't die--I'm just not at Lex) and found it to be pretty challenging. The real things that add the dirt are not always obvious and seem to rely on a somewhat 'compromised' data pathway from start to finish.My guess is that a lot of the dirt stems from some of the coefficient quantization issues that were described by Oppenheim & Schafer back in 1975. A fixed point filter will have noise and distortion. The 1st order filters used by the older algorithms tend to be cleaner than 2nd order filters, but a little bit of noise, times a few hundred passes through a delay feedback loop, can result in a lot of noise. 


A possibility: This noise would definitely be different between output channels. I know that adding some bandpass filtered noise to the output channels, with decorrelated noise sources for each channel, can create a wider stereo image if used subtly. Maybe this coefficient quantization noise adds "depth" to the hardware reverbs. Or maybe not. Just thinking as I type here.

Quote: > Floating point just doesn't lend itself to that sort of stuff.  Don't get me wrong--you can add schmutz, but it doesn't sound the same.  I'm probably not going to spend any more time on that experiment for quite some time.Program everything in fixed point MMX or SSE, and you could probably get the schmutz back. You would need to do a lot of bitwise operations to get the wordlengths and saturation headroom correctly. I've thought about doing this, then thought "nah." 


I've programmed things on a fixed point DSP that is fairly close to the fixed point Lexicon hardware (the Spin Semiconductor FV-1), and I don't hear any particular "magic" versus the floating point that makes moving over to fixed point worthwhile.  Maybe I need to listen to this with fresh ears.

---

### Post #282 -- Page 10
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8242159&postcount=282>

Quote: > Originally Posted byseancostello➡️Program everything in fixed point MMX or SSE, and you could probably get the schmutz back. You would need to do a lot of bitwise operations to get the wordlengths and saturation headroom correctly. I've thought about doing this, then thought "nah."That's basically it. There are some small issues in coefficient management like rounding vs truncation, but the main trick is to make sure you throw out lots of subtle detail.  I've come to the same conclusion as you, partly for reasons of the P.I.T.A. factor and also personal taste.  I've spent years trying to get that crap out of there, and I'm not keen to put it back.  I am aware that there are people who like it, but I expect they'll always be happier with an old hardware unit anyway.


Many of these preferences are probably related to the particular musical styles that mixers like and many may be a pleasant association with their first successful mixes.  I'd imagine there are generational differences as well.  I certainly appreciate the usefulness of 'effect-y' reverbs--they can be quite musical--but I just don't feel the love for grindy coefficients and quantization error.


Having gotten that off my chest, I am aware that an awful lot of my work has ended up on 64K mp3 files.  I appreciate the irony.

---

### Post #283 -- Page 10
**User:** henge
**Info:** Joined: May 2003Posts: 3,628My Recordings/CreditsMy Studio2 Reviews written🎧 20 years | Posts: 3,628My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8242310&postcount=283>

Quote: > Originally Posted byCasey➡️Sean, NS,I am glad you brought this up because this classic page should be included in this thread;SST282_History-CaseyI loved this thread when it started and just reread the whole thing.

Very interesting to see what happened to the cast of characters since the thread started 3 years ago!

One burning question though. What's with the beards in that article?? Griesinger,Moore,Agnello,Blesser...

Casey why no beard? Sean I demand a pic of you with a beard or Vroom and the rest of your products a banished from my computer. Same to you Mr.Lind.

Mr Carnes, whatever your brewing up at Exponential better be done with a beard growing or I ain't interested.

Just kidding. It's been a strange day....

---

### Post #284 -- Page 10
**User:** cowudders
**Info:** Joined: Jan 2006Posts: 1,022🎧 20 years | Posts: 1,022
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8242404&postcount=284>

Quote: > Originally Posted byWarp69➡️You can't use the diagram as such - the Random Ambience actually has three parts : DELAY (DRY) + ER + REV. This is not displayed in the manual where ER + REV is shown as one block.When the Reverb Level is way down, you still get the sound of the ER part. As I can understand from your post - there're infact randomized delay lines in the ER part of the Random Ambience algorithm in the 300L, just like in the 480L.Just checked out the IK Multimedia CSR Room. Of course the Earlies are modulated here, even if the tail is set to zero! And it sounds just great.


It has not to be underestimated what you are getting with the CSR suite.

---

### Post #285 -- Page 10
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8242408&postcount=285>

Quote: > Originally Posted byhenge➡️I loved this thread when it started and just reread the whole thing.Very interesting to see what happened to the cast of characters since the thread started 3 years ago!One burning question though. What's with the beards in that article?? Griesinger,Moore,Agnello,Blesser...Casey why no beard? Sean I demand a pic of you with a beard or Vroom and the rest of your products a banished from my computer. Same to you Mr.Lind.Mr Carnes, whatever your brewing up at Exponential better be done with a beard growing or I ain't interested.Just kidding. It's been a strange day....[https://valhalladsp.wordpress.com/20...-reverb-beard/](https://valhalladsp.wordpress.com/2010/12/21/the-reverb-beard/)


My beard has only gotten greyer since I wrote this. And my wife's views on beards haven't changed. I should get a fake ZZ Top beard to put on while I am coding.


When I met Michael Carnes at an AES convention many years ago, he was clean shaven.

---

### Post #286 -- Page 10
**User:** henge
**Info:** Joined: May 2003Posts: 3,628My Recordings/CreditsMy Studio2 Reviews written🎧 20 years | Posts: 3,628My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8242464&postcount=286>

Quote: > Originally Posted byseancostello➡️https://valhalladsp.wordpress.com/20...-reverb-beard/My beard has only gotten greyer since I wrote this. And my wife's views on beards haven't changed. I should get a fake ZZ Top beard to put on while I am coding.When I met Michael Carnes at an AES convention many years ago, he was clean shaven." Beard Voltron".

---

### Post #287 -- Page 10
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8243107&postcount=287>

Quote: > Originally Posted byseancostello➡️When I met Michael Carnes at an AES convention many years ago, he was clean shaven.Guys, I don't really need to look any older...

---

### Post #288 -- Page 10
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8243129&postcount=288>

Quote: > Originally Posted byJim Williams➡️Does Lexicon have a future? Is the PCM92 the last hardware product under production? Do they have future plans in hardware reverbs?I'm sorry Jim, I don't have any contact with the company and I have no idea what plans are over there. It wouldn't really be fair for me to speculate on a public forum. Anything I said would come across as either privileged information or sour grapes.  Perhaps the best thing for you to do would be to stay in touch with current owners and see how their support experiences go.

---

### Post #289 -- Page 10
**User:** waveterm
**Info:** Joined: Jan 2004Posts: 1,984🎧 20 years | Posts: 1,984
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8243134&postcount=289>

Hey Sean,


what´s up with this :


"Nowadays, I use the term “Reverb Beard” (or “Reverbskägg” in Swedish) "


Taken from your blog. You swedish ?


WT

---

### Post #290 -- Page 10
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8243834&postcount=290>

Quote: > Originally Posted bywaveterm➡️Hey Sean,what´s up with this :"Nowadays, I use the term “Reverb Beard” (or “Reverbskägg” in Swedish) "Taken from your blog. You swedish ?WTI'm from the US (Seattle area, to be precise). IIRC, when I was first writing about "reverb beards," some Swedish Twitter follower provided the "Reverbskägg" translation, so I put it in the blog post.

---

### Post #291 -- Page 10
**User:** Ghosted
**Info:** Joined: Jul 2012Posts: 677🎧 10 years | Posts: 677
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8243881&postcount=291>

Reverbskägg? That doesn't sound very attractive.

![](https://static.gearspace.com/util/imgext.php?u=http%3A%2F%2Fprofile.ak.fbcdn.net%2Fhprofile-ak-ash2%2F50499_310223407457_2992763_n.jpg&h=615fda2c34fad98c5d79ebfb597e2f9f)

---

### Post #292 -- Page 10
**User:** waveterm
**Info:** Joined: Jan 2004Posts: 1,984🎧 20 years | Posts: 1,984
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8244331&postcount=292>

Ok !


WT

---

### Post #293 -- Page 10
**User:** MagnusD
**Info:** Joined: Sep 2012Posts: 1🎧 10 years | Posts: 1
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8244653&postcount=293>

This has been a fascinating read, and I recognise many of the details.


I'd love a summary of the technological advances in the Lexicon line, I guess bit-width, form of realization etc. changed. Micro-steps per sample etc. I assume that the early stuff was TTL or AMD bit-sliced. I have seen the dedicated chips for the PCM70 and 480L which supported the 16/"pseudo-18" bit. Next integration level was the Lexichip, which I think supported 20 bit, but I only saw the 16-bit realizations in the LXP-1/5, unsure about the LXP-15 and I think I saw it when I lifted the hood of the 300L.


We have seen some of the side-effects of these advances glean through the comments of the giants, but it would be nice to see the architectural differences and how they affected the sound.


As it happens, I have been designing a DSP with toolchain, but not for direct audio use, but it times audio and video production throughout the world.


Cheers,

Magnus

---

### Post #294 -- Page 10
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8245269&postcount=294>

Quote: > Originally Posted byJim Williams➡️That's a bit too late for me. I need to know what the heck is going on inside that company, are they solvent? I can't afford to invest in expensive hardware not knowing if the company is going to fix it. Like Scotty, fool me twice, shame on me.My decision is not based on the product, but the condition of the company that makes it. Yes, that is new for me too. A sad commentary on the current pro audio "industry". The products are healthy, the companies are not.Well, the company that owns Lexicon is on the NYSE, so you can look at the stock ticker and see for yourself how they are performing:

[NYSE, New York Stock Exchange > Listings > Listings Directory](http://www.nyse.com/about/listed/lcddata.html?ticker=HAR)


Of course, the importance of Lexicon within the grand scheme of Harman can't be determined by the stock ticker.

---

### Post #295 -- Page 10
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,235🎧 20 years | Posts: 5,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8245296&postcount=295>

Quote: > Originally Posted byseancostello➡️Well, the company that owns Lexicon is on the NYSE, so you can look at the stock ticker and see for yourself how they are performing:NYSE, New York Stock Exchange > Listings > Listings DirectoryOf course, the importance of Lexicon within the grand scheme of Harman can't be determined by the stock ticker.Totally OT, but the shareholder value thing is what made so many audio companies suck in the first place IMO. Harman is a "good" example for it...

---

### Post #296 -- Page 10
**User:** ActiveSoundLarry
**Info:** Joined: Nov 2013Posts: 1🎧 10 years | Posts: 1
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9569485&postcount=296>

Chris Noyes worked for Lexicon in the 80's and designed some of the original 224 algorithms. I believe he was responsible for the Resonance program. After leaving Lexicon he was at Sony for a while and taught a class at Berklee as well. Last time I saw him was at an AES convention in the early 90's. Anyone know what he's doing now? 


My first piece of digital gear was a Lexicon Prime Time, then the Model 200 which was my main reverb for 10 years. 


The Lexicon 200 was very expensive at the time because it was designed to be upgraded in many ways. If you look at the box you can see many slots, cutouts and space for future upgrades that never happened. They only came out with one real upgrade and then pretty much abandoned it after that.


When I worked at Pro Audio Design, I sold the 200 to Al Di Meola because he needed it for a tour. One of the many things (Lexicon Prime Time, Vox Continental, Trident Console, etc.) that I'll always regret selling!


Good info here - [Lexicon Model 200 digital reverb](http://www.retrosynth.com/~analoguediehard/studio/effects/lexicon_model-200/)

---

### Post #297 -- Page 10
**User:** Atlanta Bliss
**Info:** Joined: Nov 2010Posts: 296🎧 15 years | Posts: 296
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9841855&postcount=297>

Hi, this is a great thread!  I'm learning a lot from this so thank you to everyone. Anyway I am not super au fait with the various Lexicon models but am thinking about buying one. There's a 480L version 3  nearby that I can check out, test etc and maybe buy. I think the main base I would be trying to cover in getting this would be the "classic" 80s Lexicon sound, from what I understand a 300L might be what I want but if I can get a 480L and get the classic cartridge to cover that base, the extra algorithms on the 480 would be great to have too (and maybe I might even use them as much or more in the long run?) -  So my question is:  were the classic algorithms only available as an extra cartridge on the 480 version 3? Did any of them come standard?  I've seen that classic cartridge available on ebay but it was for 480L version 4.1 - was it also available for version 3? If available is it super rare?  Also, from reading the posts here (have only read the first 6 pages so far to be honest)  I get the impression that the classic algorithms from the 200 and 300 sound a bit different when they're on the 480?  But it's not much of a difference? Any thoughts on that? 

 Anyway, essentially I want to know if I get a 480L version 3 will I be able to do the classic presets of the 300 and 200 (224?) and will they sound very close on the 480L v3 ?? 

  Any thoughts or advice greatly appreciated - thanks!

---

### Post #298 -- Page 10
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9864047&postcount=298>

Quote: > Originally Posted byMagnusD➡️I'd love a summary of the technological advances in the Lexicon line, I guess bit-width, form of realization etc. changed. Micro-steps per sample etc. I assume that the early stuff was TTL or AMD bit-sliced. I have seen the dedicated chips for the PCM70 and 480L which supported the 16/"pseudo-18" bit. Next integration level was the Lexichip, which I think supported 20 bit, but I only saw the 16-bit realizations in the LXP-1/5, unsure about the LXP-15 and I think I saw it when I lifted the hood of the 300L.224 and 224X were similar, 16 bit ARU but with a 6-bit multiply coefficiency per cycle. It did this by processing two coefficient bits per cycle. The A-D and D-A was 12-bit with gain staging to get the equivalent of 14 bits. The 224 had 16k of RAM; the 224X could be set up with either 32k or 64k. The microcode length was 100 instructions with 8 clock ticks per instruction. The ARU was based on fast adders (74S283). I have never seen a Lexicon using the bit-slice product families although Eventide and EMT have used the AM2901 quite a bit.


The 200 shared the same A-D converter structure, a 3-bit or 4-bit multiplier(depending on the timing of the following cycle). I believe this unit can accept 128 microinstructions per sample at 3 clock ticks per instruction. This ARU was based on the 74F181 ALU commonly used in 1970's era minicomputers. This design was moved into the first 16-bit ARU ASIC used in the PCM60.


The PCM70 shares the same basic ARU design as the 200 except it was implemented in an ASIC and at least my PCM70 has the 18-bit version of the ARU. The 74F181 ALU (or ASIC equivalent) are replaced with a simple adder and a couple of 18-bit multiplexors. Cycle timing (3 states) and program length are pretty much the same but the sample rate is raised a bit. The A-D and D-A are upgraded to 16-bit.


Next, the 480L... here there is a 4-core processor. The ARU is the same as the PCM70 but the sample rate is raised to accommodate digital I/O and the multiplier precision is raised to 4-bit instead of 3-bit - one extra clock cycle is used. As such, program length is limited to 80 instructions because of timing constraints of the ARU but there are four cores or 320 instructions per sample. Shuffling data between the cores does add some overhead, though.


The Lexichip-1 and -2 look to be a faster version of one section of the 480L HSP board - one ARU, CMU, MMU, and WCS. The ARU seems to be expanded to 20 bits. At least the Lexichip-2 supports both a parallel A-D/D-A converter as well as a serial interface. Multiplier precision is the same but clock speed is faster - a full 128 program steps are available.


The 300 used two Lexichips, 16-bit A/D and D/A.


PCM91 also used two Lexichips but 20-bit A/D and D/A.


PCM80 uses one Lexichip and one DSP56002 for the effects side of things.


Most of the newer boxes use the Lexichip-3 and I have not studied this part at all.

---

### Post #299 -- Page 10
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9864164&postcount=299>

Quote: > Originally Posted byAtlanta Bliss➡️Hi, this is a great thread!  I'm learning a lot from this so thank you to everyone. Anyway I am not super au fait with the various Lexicon models but am thinking about buying one. There's a 480L version 3  nearby that I can check out, test etc and maybe buy. I think the main base I would be trying to cover in getting this would be the "classic" 80s Lexicon sound, from what I understand a 300L might be what I want but if I can get a 480L and get the classic cartridge to cover that base, the extra algorithms on the 480 would be great to have too (and maybe I might even use them as much or more in the long run?) -  So my question is:  were the classic algorithms only available as an extra cartridge on the 480 version 3? Did any of them come standard?  I've seen that classic cartridge available on ebay but it was for 480L version 4.1 - was it also available for version 3? If available is it super rare?  Also, from reading the posts here (have only read the first 6 pages so far to be honest)  I get the impression that the classic algorithms from the 200 and 300 sound a bit different when they're on the 480?  But it's not much of a difference? Any thoughts on that?Anyway, essentially I want to know if I get a 480L version 3 will I be able to do the classic presets of the 300 and 200 (224?) and will they sound very close on the 480L v3 ??Any thoughts or advice greatly appreciated - thanks!Hi there!

I would search GS Threads and one in particular named "Is it still worth buying a 480L in 2013? I'd also Google the subject and highlight the GS paged Google results as these results bring up much older threads (Pages of them) as opposed to the often more recent when doing a GS search as quite often doing a "GearSlutz Search" brings up newer threads, where Google will bring up the really dusty and mouldy threads when all units were in full usage thus... possibly expanding thoughts on the units uses & usage that may be more relevant to your needs if looking to buy! 


Yes, your going to need 4.x.1 Software for Classic Cart Software on the 480L. That can give you the Lexicon sound from PCM-42, PrimeTime, 22X-XL, 300 & PCM-80 Sounds as well as 480L Algorithms etc. Basically making the 480L a huge unit, add Surround/HD and PrimeTime 3 Cart and you've got a huge FX/Reverb unit. Benden Tech Fixes Lexicon in the UK! Maybe chat to them? I'd say you might be better off with a PCM81 and 300L For ITB/OTB use with Mod Con's etc such as AES, Analog, SMPTE, Midi etc would bode much better for you though without the performance or potential Door Stop issues that buying a 480L can bring etc. Just a thought!


Regards

TheLastByte

---

### Post #300 -- Page 10
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9864171&postcount=300>

Quote: > Originally Posted bydale116dot7➡️Shuffling data between the cores does add some overhead, though.Actually no overhead is incurred when moving a sample between cores.


All of the standard 480 algs run on 2 cores. Only the HD alg on the optional surround cart used 4 cores. 


The 480 also uses an 8 bit microprocessor which re-writes the 80 step microcode in the ARUs to provide the dynamic reverb modulation.

Quote: > Originally Posted bydale116dot7➡️Most of the newer boxes use the Lexichip-3 and I have not studied this part at all.The Lexichip 3 provides 256 steps. This same ARU is used in the MPX series and in the 960. The 960 of course had 4 of them to support 4 stereo machines. The 960 also added two 8 bit microprocessors to work with the 4 ARUs for dynamic microcode changes.


-Casey



---


---

## Page 11

---

### Post #301 -- Page 11
**User:** aramism
**Info:** Joined: Feb 2009Posts: 1,219🎧 15 years | Posts: 1,219
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9864868&postcount=301>

this thread is awesome

---

### Post #302 -- Page 11
**User:** Atlanta Bliss
**Info:** Joined: Nov 2010Posts: 296🎧 15 years | Posts: 296
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9865109&postcount=302>

Quote: > Originally Posted byTheLastByte➡️Hi there!I would search GS Threads and one in particular named "Is it still worth buying a 480L in 2013?I'd also Google the subject and highlight the GS paged Google results as these results bring up much older threads (Pages of them) as opposed to the often more recent when doing a GS search as quite often doing a "GearSlutz Search" brings up newer threads, where Google will bring up the really dusty and mouldy threads when all units were in full usage thus... possibly expanding thoughts on the units uses & usage that may be more relevant to your needs if looking to buy!Yes, your going to need 4.x.1 Software for Classic Cart Software on the 480L. That can give you the Lexicon sound from PCM-42, PrimeTime, 22X-XL, 300 & PCM-80 Sounds as well as 480L Algorithms etc. Basically making the 480L a huge unit, add Surround/HD and PrimeTime 3 Cart and you've got a huge FX/Reverb unit. Benden Tech Fixes Lexicon in the UK! Maybe chat to them? I'd say you might be better off with a PCM81 and 300L For ITB/OTB use with Mod Con's etc such as AES, Analog, SMPTE, Midi etc would bode much better for you though without the performance or potential Door Stop issues that buying a 480L can bring etc. Just a thought!RegardsTheLastByte Thanks TheLastByte !  After reading everything I could I went for a 224xl. Am looking forward to it's arrival.  Maybe I'll get a 224 or pcm70 or a 300 if one comes up later .... or maybe AMS....... I would like a lexicon prime time 2 though.

---

### Post #303 -- Page 11
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9865111&postcount=303>

Quote: > Originally Posted byCasey➡️Actually no overhead is incurred when moving a sample between cores.I was thinking something like a very long delay line - one that needs two cores worth of RAM. To do that you'd have to read the end of the delay on HSP 1, write it to the transfer register, then do the appropriate operations on HSP 2 to fetch the data and put it in RAM. You just need to use a couple of instructions to do that.

---

### Post #304 -- Page 11
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9869683&postcount=304>

Quote: > Originally Posted byAtlanta Bliss➡️Thanks TheLastByte !  After reading everything I could I went for a 224xl. Am looking forward to it's arrival.  Maybe I'll get a 224 or pcm70 or a 300 if one comes up later .... or maybe AMS....... I would like a lexicon prime time 2 though.Congratulations Atlanta Bliss!

Great Stuff! Benden Tech in The UK actually specialise in 224/XL units, so should (fingers crossed) anything go burp, pop, growl, power-down etc you will be covered... and it's indeed a much loved and well used device with many a sage mind on the subject, in fact Digikey in the USA still carry 224 HSP PCB Boards! I'd say many of my top 100 recordings (Album wise) have a 224/XL Sound, lovely grainy, warm and those verbs & Fx somehow wrap around the Tracks recorded. Great Choice, If I had the support where I live, I would buy one in a heartbeat! As for the PrimeTime M95 MKII's I have 2 Units and after a nice getting to know you very well period, man I can dial in anything from Phaser, Flanger, ADT's, Pitch Shifting and Cyborg Effects etc. Certainly a recommended device!


Regards

TheLastByte

---

### Post #305 -- Page 11
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9873118&postcount=305>

Quote: > Originally Posted byCasey➡️The 480 also uses an 8 bit microprocessor which re-writes the 80 step microcode in the ARUs to provide the dynamic reverb modulation.Quote: > The 960 also added two 8 bit microprocessors to work with the 4 ARUs for dynamic microcode changes.Did the Lexicons generate 8 bit modulation waveforms, or was higher precision used at times?

---

### Post #306 -- Page 11
**User:** Atlanta Bliss
**Info:** Joined: Nov 2010Posts: 296🎧 15 years | Posts: 296
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9873566&postcount=306>

Quote: > Originally Posted byTheLastByte➡️Congratulations Atlanta Bliss!Great Stuff! Benden Tech in The UK actually specialise in 224/XL units, so should (fingers crossed) anything go burp, pop, growl, power-down etc you will be covered... and it's indeed a much loved and well used device with many a sage mind on the subject, in fact Digikey in the USA still carry 224 HSP PCB Boards! I'd say many of my top 100 recordings (Album wise) have a 224/XL Sound, lovely grainy, warm and those verbs & Fx somehow wrap around the Tracks recorded. Great Choice, If I had the support where I live, I would buy one in a heartbeat! As for the PrimeTime M95 MKII's I have 2 Units and after a nice getting to know you very well period, man I can dial in anything from Phaser, Flanger, ADT's, Pitch Shifting and Cyborg Effects etc. Certainly a recommended device!RegardsTheLastByte

 Thanks Last Byte!  I imagine I'll be hitting you back for some advice re: "which prime time?!"  at some point in the future! 


 In regs to favorite albums that use the 224xl, which are your favorite?  I noticed in the promo video for UA 's plug in emulation of the 224 that they list a whole lot of albums as using the 224  - but I wondered if some of them actually used the 224xl as some were more early mid 80s rather than early 80s.  ?? 


 Hope I'm not getting too away from the thread topic there, which is more technical. Apologies if I have.

---

### Post #307 -- Page 11
**User:** Crash
**Info:** Joined: Oct 2003Posts: 2,560My Studio🎧 20 years | Posts: 2,560My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9874246&postcount=307>

Quote: > Originally Posted byTheLastByte➡️Congratulations Atlanta Bliss!Great Stuff! Benden Tech in The UK actually specialise in 224/XL units, so should (fingers crossed) anything go burp, pop, growl, power-down etc you will be covered...Just another shout out to Steve Lenham of Benden Tech. He helped me out with a newly aquired M300 that had a dead VFD when he totally didn't have to, considering he is in the UK and I am in Texas. It made no sense for me to send it across the water to him as much as I would have liked to. Anyway via email, he entertained all of our troubleshooting and theories to a fixed unit. Good dude! Now, back to your original scheduled program.

---

### Post #308 -- Page 11
**User:** Atlanta Bliss
**Info:** Joined: Nov 2010Posts: 296🎧 15 years | Posts: 296
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9874375&postcount=308>

Quote: > Originally Posted byCrash➡️Just another shout out to Steve Lenham of Benden Tech. He helped me out with a newly aquired M300 that had a dead VFD when he totally didn't have to, considering he is in the UK and I am in Texas. It made no sense for me to send it across the water to him as much as I would have liked to. Anyway via email, he entertained all of our troubleshooting and theories to a fixed unit. Good dude! Now, back to your original scheduled program. Agreed, Steve seems to be a great guy, I emailed him with a few questions regarding various lexicon units and his advice was great.

---

### Post #309 -- Page 11
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9875846&postcount=309>

Quote: > Originally Posted byCrash➡️Just another shout out to Steve Lenham of Benden Tech. He helped me out with a newly aquired M300 that had a dead VFD when he totally didn't have to, considering he is in the UK and I am in Texas. It made no sense for me to send it across the water to him as much as I would have liked to. Anyway via email, he entertained all of our troubleshooting and theories to a fixed unit. Good dude! Now, back to your original scheduled program.Totally agree....though if your replacing all your Op Amps in a PCM-60 don't expect any sympathy (From Any Tech) should you not use schematics and totally F**k it Up...This happened very recently to a forum member, as he wanted the PCM-60 which tops out at 8-10Khz to have a "Light, Modern & Bright Sound"  The exact reason you'd buy a PCM-60! DIY people can expect even less sympathy as many Tech's will no longer touch a unit a non tech has had a go at especially Lexicon! Those offenders have been warned! Hmmm?....Now back to normal transmission!


Regards

TheLastByte

---

### Post #310 -- Page 11
**User:** MadDaddy
**Info:** Joined: Feb 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9876219&postcount=310>

Hi all. Just joined. Just saw this thread. My first post. I had a limited amount of success in the '80's & '90's and used to use a single LARC to control a 224XL and a 480L. I can safely say that there was one 480L preset that I have used, albeit highly tweeked, on almost every gold and platinum project that I have ever mixed. What's that you're wondering? The 2 most beautiful words you could ever see in a LARC display... Brick Wall. It made the AMS RMX-16 non-lin preset sound anemic in comparison! Also Tiled Room in a PCM-70 was another regular. I'm currently shopping for a 480L and another one of my all-time faves, a Quantec QRS. I'm so happy to see that these boxes are still around!

---

### Post #311 -- Page 11
**User:** T_R_S
**Info:** Joined: Sep 2004Posts: 8,245My Studio1 Review written🎧 20 years | Posts: 8,245My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9876273&postcount=311>

If you have a major problem with your Lexicon Reverb from 30 years ago - good luck getting it repaired.

If you have a 30 year old Eventide box - you will BE ABLE to get it repaired.

FWIW I have 9 lexicon reverbs and 2 Eventides so I have some first hand experience with this.

---

### Post #312 -- Page 11
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9876285&postcount=312>

Just in case someone with a rather large Investment goes down! These companies offer Lexicon Repairs. 21/2/2014


USA:Beamish Electronics Chicago: Fixes 224/200/300/480L etc


UK: Benden Tech: London Fixes 224/200/300/480L etc

---

### Post #313 -- Page 11
**User:** MadDaddy
**Info:** Joined: Feb 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9876306&postcount=313>

Quote: > Originally Posted byT_R_S➡️If you have a major problem with your Lexicon Reverb from 30 years ago - good luck getting it repaired.If you have a 30 year old Eventide box - you will BE ABLE to get it repaired.FWIW I have 9 lexicon reverbs and 2 Eventides so I have some first hand experience with this.If I had a 30 year old 2016 die I'd bury it. If I had a 480L die, I would move heaven and earth to revive it. Just sayin'. (Note: Beamish is in Cleveland)

---

### Post #314 -- Page 11
**User:** Pianolando
**Info:** Joined: Sep 2012Posts: 512My Studio1 Review written🎧 10 years | Posts: 512My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9876653&postcount=314>

Quote: > Originally Posted byMadDaddy➡️Hi all. Just joined. Just saw this thread. My first post. I had a limited amount of success in the '80's & '90's and used to use a single LARC to control a 224XL and a 480L. I can safely say that there was one 480L preset that I have used, albeit highly tweeked, on almost every gold and platinum project that I have ever mixed. What's that you're wondering? The 2 most beautiful words you could ever see in a LARC display... Brick Wall. It made the AMS RMX-16 non-lin preset sound anemic in comparison! Also Tiled Room in a PCM-70 was another regular. I'm currently shopping for a 480L and another one of my all-time faves, a Quantec QRS. I'm so happy to see that these boxes are still around!Nice info  What kind of a preset was it, what algorithm?

---

### Post #315 -- Page 11
**User:** Voyage.One
**Info:** Joined: May 2010Posts: 766My Studio🎧 15 years | Posts: 766My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9877321&postcount=315>

Hi there. I have a burning question. Say I was to buy a standard M300 (front panel controlled) then buy a LARC at a later date, can LARCs be used with the standard 3.5 software or is there hoops to jump through??

---

### Post #316 -- Page 11
**User:** MadDaddy
**Info:** Joined: Feb 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9878167&postcount=316>

Quote: > Originally Posted byPianolando➡️Nice infoWhat kind of a preset was it, what algorithm?It's been so  long now I don't remember. Halls or Rooms I would imagine. I remember it came out in the 2nd release of software. The first release had actual names for halls like "Concertgebouw" (an actual concert hall in Amsterdam, NL). The second release had names like Brick Wall and Silica Beads.

---

### Post #317 -- Page 11
**User:** MadDaddy
**Info:** Joined: Feb 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9881659&postcount=317>

Wild Spaces perhaps?

---

### Post #318 -- Page 11
**User:** dale116dot7
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9881941&postcount=318>

Quote: > Originally Posted byTheLastByte➡️Just in case someone with a rather large Investment goes down! These companies offer Lexicon Repairs. 21/2/2014USA:Beamish Electronics Chicago: Fixes 224/200/300/480L etcUK: Benden Tech: London Fixes 224/200/300/480L etcAnd I fix them although I'm not that fast at doing it these days and I don't really want to do a lot of them. Mostly I buy the broken ones off ebay, fix them, and either resell or add them to my collection.

---

### Post #319 -- Page 11
**User:** Antiphones
**Info:** Joined: Dec 2011Posts: 24🎧 10 years | Posts: 24
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9883480&postcount=319>

Does anyone know if the PCM91 St John's Hall preset can be recreated with the PCM plugin (or PCM 96)?  Or if anyone has a PCM 91 and they wouldn't mind sending me a message with a list of the parameters for this patch I'd be really grateful.  I'm currently using an IR of this patch but would love to recreate something close to it with the PCM plugin.

---

### Post #320 -- Page 11
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9889360&postcount=320>

Quote: > Originally Posted byVoyage.One➡️Hi there. I have a burning question. Say I was to buy a standard M300 (front panel controlled) then buy a LARC at a later date, can LARCs be used with the standard 3.5 software or is there hoops to jump through??Hi There,

The Software for an M/L300 or as you are asking is specifically for an M300and that is 3.5L software and this involves the Larc Software though also requires a 224/XL/480L or 300L Larc that uses a 10-20 Volt DC Wall Wart Adapter @800 Milliamps (No the 224XL and 480L do not require this nor a 300L Mainframe although an M300 Does.) Basically the Larc has a DC Current input, a touch like a controller interface that requires current as the M300 9 Pin D-Sub Output does not have the power for the Larc Install the M300 3.5L (Not 3.5x) Larc software as well as adding the 800 Ma DC Wall Wart to the Larc, Reset the M300 and the front Panel will power down (No Fluro Display)….that will be gone, and you will have Mach A & B from the front panel of the Larc.


One thing to take into mind is that if your using an M/L300 Digitally lower the Input/Output of the M/L300 in AES/EBU or even Analog as the total headroom of the unit is +26dBm and that is fine though not for Cranking and riding heavy returns via AES, so although once set to 20 bit AES your down to near + 7/8 dBm of actual Headroom, (Not a huge amount in all consideration) so....drop the Level by -10dBm and you've got much more power to use on Sends and Returns. In fact this goes for Analog or Any Digital In/Out mode on an M/L300, as yes you do have headroom, though certain programs and presets are arranged to use that actual gain in a Patch... so a work around is dropping the Input/Output Levels on purpose there by giving the M/L300 and it's Convertors more headroom in all scenarios. The 480L has a trim screw for this that you can set with a meter, though an M/L300 does not! Dropping the levels give you a much "Deeper and Harder Reverb/FX" type of work out!


Hope that answers your question.


Regards

TheLastByte

---

### Post #321 -- Page 11
**User:** Voyage.One
**Info:** Joined: May 2010Posts: 766My Studio🎧 15 years | Posts: 766My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9890981&postcount=321>

Quote: > Originally Posted byTheLastByte➡️Hi There,The Software for an M/L300 or as you are asking is specifically for anM300and that is 3.5L software and this involves the Larc Software though also requires a 224/XL/480L or 300L Larc that uses a 10-20 Volt DC Wall Wart Adapter @800 Milliamps (No the 224XL and 480L do not require this nor a 300L Mainframe although an M300 Does.) Basically the Larc has a DC Current input, a touch like a controller interface that requires current as the M300 9 Pin D-Sub Output does not have the power for the Larc Install the M300 3.5L (Not 3.5x) Larc software as well as adding the 800 Ma DC Wall Wart to the Larc, Reset the M300 and the front Panel will power down (No Fluro Display)….that will be gone, and you will have Mach A & B from the front panel of the Larc.One thing to take into mind is that if your using an M/L300 Digitally lower the Input/Output of the M/L300 in AES/EBU or even Analog as the total headroom of the unit is +26dBm and that is fine though not for Cranking and riding heavy returns via AES, so although once set to 20 bit AES your down to near + 7/8 dBm of actual Headroom, (Not a huge amount in all consideration) so....drop the Level by -10dBm and you've got much more power to use on Sends and Returns. In fact this goes for Analog or Any Digital In/Out mode on an M/L300, as yes you do have headroom, though certain programs and presets are arranged to use that actual gain in a Patch... so a work around is dropping the Input/Output Levels on purpose there by giving the M/L300 and it's Convertors more headroom in all scenarios. The 480L has a trim screw for this that you can set with a meter, though an M/L300 does not! Dropping the levels give you a much "Deeper and Harder Reverb/FX" type of work out!Hope that answers your question.RegardsTheLastByteSo it is possible to use a LARC with V3.5, just I’d have to pick up a cheap wall wart.

---

### Post #322 -- Page 11
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9893362&postcount=322>

Quote: > Originally Posted byVoyage.One➡️So it is possible to use a LARC with V3.5, just I’d have to pick up a cheap wall wart.NO....! Not 3.5.x

You need **3.5L.x Software** and an **M300**, with **Larc** & **DC Power**. Did you not read my Post?


Regards

TheLastByte

---

### Post #323 -- Page 11
**User:** Voyage.One
**Info:** Joined: May 2010Posts: 766My Studio🎧 15 years | Posts: 766My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9893785&postcount=323>

Quote: > Originally Posted byTheLastByte➡️NO....! Not 3.5.xYou need3.5L.x Softwareand anM300, withLarc&DC Power. Did you not read my Post?RegardsTheLastByteOkay, 3.5L software is required. I read a post somewhere saying that the M300 has jumper switch inside when activated supplies the 12V DC to the commport.

---

### Post #324 -- Page 11
**User:** TheLastByte
**Info:** Joined: May 2009Posts: 5,099🎧 15 years | Posts: 5,099
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9893826&postcount=324>

Quote: > Originally Posted byVoyage.One➡️Okay, 3.5L software is required. I read a post somewhere saying that the M300 has jumper switch inside when activated supplies the 12V DC to the commport.Well disinformation is riff on many topics. The com port (D-sub 9 pin) on the M300 is used for a special M300 Lexicon diagnostic software, so if need be, problems with internals can and are cycled thru, and found. The M300 and Larc is different to an L300 and Larc. No external power is required as there is no front display to power etc! Where is this Gem of M/l300 12-V -DC

switching? I've written many, many M/L300 posts over years on GS, and maybe I just have not run across it, is it on GS, REP or another forum? As it's clearly wrong! Are you trying to put an M300 & Larc together or an L300 etc? maybe give me an idea of what your looking to cobble together and I can help you achieve what your obviously trying to do!


[edit] Don't get me wrong, the 9 pin D-sub carries power, it's just the M300 as opposed to a 224/XL, 480L or L300 has this power, hence the M300 & Larc requiring a DC 800ma Supply!


Cheers

TheLastByte

---

### Post #325 -- Page 11
**User:** Wayne
**Info:** Joined: Dec 2003Posts: 4,513🎧 20 years | Posts: 4,513
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9894359&postcount=325>

Quote: > Originally Posted byAntiphones➡️I would give anything to have the PCM91 St John's Hall preset available in a plugin.I rely on this particular patch for my main guitar sound, its become almost part of my signature sound.   I have spent some time with the PCM 96 plugin, but was unable to recreate the special sound of this patch.  I think this is simply because I'm not sure what path to follow with all the controls available.If Michael or anyone else can tell me how the St John's Hall sound can be recreated (if it can be done) I would be eternally grateful (and I'd buy the plugin tomorrow!).  Thanks.The Chamber/Room split called 'Cathedrals' ?

---

### Post #326 -- Page 11
**User:** cowudders
**Info:** Joined: Jan 2006Posts: 1,022🎧 20 years | Posts: 1,022
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9894694&postcount=326>

Quote: > Originally Posted byPianolando➡️Nice infoWhat kind of a preset was it, what algorithm?As MadDaddy wrote, it's in the 'wild spaces' bank, uses the 'Plate' algorithm, I attached the setting from the 480 manual.


BTW: The relab 480lx 'brick wall' preset has wrong settings, you'll have to set the decay optimization 'correctly'.

---

### Post #327 -- Page 11
**User:** Pianolando
**Info:** Joined: Sep 2012Posts: 512My Studio1 Review written🎧 10 years | Posts: 512My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9896595&postcount=327>

Quote: > Originally Posted bycowudders➡️As MadDaddy wrote, it's in the 'wild spaces' bank, uses the 'Plate' algorithm, I attached the setting from the 480 manual.BTW: The relab 480lx 'brick wall' preset has wrong settings, you'll have to set the decay optimization 'correctly'.Thanks a lot! I like and use Relab480 a lot, but the documentation and support is a bad joke  I downloaded some Preset folders but only have Banks 1,2,4,6,11,13 and 14 but I just now realized I could copy the rest from the manual instead.. Have you downloaded any more presets from somewhere?

---

### Post #328 -- Page 11
**User:** cowudders
**Info:** Joined: Jan 2006Posts: 1,022🎧 20 years | Posts: 1,022
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9896675&postcount=328>

Quote: > Originally Posted byPianolando➡️Thanks a lot! I like and use Relab480 a lot, but the documentation and support is a bad jokeI downloaded some Preset folders but only have Banks 1,2,4,6,11,13 and 14 but I just now realized I could copy the rest from the manual instead.. Have you downloaded any more presets from somewhere?Attached are the Banks 3, 12, a 'corrected' version of the 'Brick Wall' and some programs from the Classic Card manual I typed in and edited a bit, they will not sound right because the relab does not (yet?) have the CC algorithms, but they make good use of the ER delays - and still sound great to me.

---

### Post #329 -- Page 11
**User:** Space Station
**Info:** Joined: Oct 2004Posts: 3,531My Studio🎧 20 years | Posts: 3,531My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9901095&postcount=329>

Quote: > Originally Posted byMadDaddy➡️What's that you're wondering? The 2 most beautiful words you could ever see in a LARC display... Brick Wall. It made the AMS RMX-16 non-lin preset sound anemic in comparison!DN-780 "Alive" algorithm is another I consider much nicer than Non-Lin on the AMS if you wanted that kind of sound.

---

### Post #330 -- Page 11
**User:** Pianolando
**Info:** Joined: Sep 2012Posts: 512My Studio1 Review written🎧 10 years | Posts: 512My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9901552&postcount=330>

Quote: > Originally Posted bycowudders➡️Attached are the Banks 3, 12, a 'corrected' version of the 'Brick Wall' and some programs from the Classic Card manual I typed in and edited a bit, they will not sound right because the relab does not (yet?) have the CC algorithms, but they make good use of the ER delays - and still sound great to me.Awesome, thanks a lot!


---

## Page 12

---

### Post #331 -- Page 12
**User:** everyday
**Info:** Joined: Jul 2004Posts: 709My Studio🎧 20 years | Posts: 709My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9902748&postcount=331>

Thank you so much!!!


Quote: > Originally Posted bycowudders➡️Attached are the Banks 3, 12, a 'corrected' version of the 'Brick Wall' and some programs from the Classic Card manual I typed in and edited a bit, they will not sound right because the relab does not (yet?) have the CC algorithms, but they make good use of the ER delays - and still sound great to me.

---

### Post #332 -- Page 12
**User:** MadDaddy
**Info:** Joined: Feb 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9943281&postcount=332>

Quote: > Originally Posted bySpace Station➡️DN-780 "Alive" algorithm is another I consider much nicer than Non-Lin on the AMS if you wanted that kind of sound.Couldn't agree more. I had a DN-780 in my racks back in those days. I used to cart around 2 16U ATA racks and a 192pt. TTL patchbay from studio to studio. Had Mogami snakes with DL's that coiled up in the lids.

---

### Post #333 -- Page 12
**User:** Nowak
**Info:** Joined: Jun 2002Posts: 1,554My Studio🎧 20 years | Posts: 1,554My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9948839&postcount=333>

Can I ask the Lexicon guys... 


Is the PCM bundle Plug In a direct porting of code? Or a re-write/dumb down? or perhaps an impulse response? 


Stefan.

---

### Post #334 -- Page 12
**User:** Nowak
**Info:** Joined: Jun 2002Posts: 1,554My Studio🎧 20 years | Posts: 1,554My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9948841&postcount=334>

Can I ask the Lexicon guys... 


Is the PCM bundle Plug In a direct porting of code? Or a re-write/dumb down? or perhaps an impulse response? 


Stefan.

---

### Post #335 -- Page 12
**User:** hyposonic
**Info:** Joined: Oct 2012Posts: 755🎧 10 years | Posts: 755
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9949070&postcount=335>

Quote: > Originally Posted byNowak➡️Can I ask the Lexicon guys...Is the PCM bundle Plug In a direct porting of code? Or a re-write/dumb down? or perhaps an impulse response?Stefan.Quote: > Originally Posted byMichael Carnes➡️I wrote the code for both, so I don't need to interpret anything.  The computer is more than capable of running that code without compromise.  Found a few minor bugs in the PCM96 code which I've fixed here.  But I intend to take those fixes back to the 96 when I can.  I left the input panners out of these algs because it's easier to do it in the DAW. That's the only difference.But I fully expect non-double-blind tests to 'prove' the 96 is better because it's hardware.

---

### Post #336 -- Page 12
**User:** Nowak
**Info:** Joined: Jun 2002Posts: 1,554My Studio🎧 20 years | Posts: 1,554My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9949103&postcount=336>

Thanks!

---

### Post #337 -- Page 12
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9950918&postcount=337>

Quote: > Originally Posted byNowak➡️Thanks!I probably should point out that the post you've quoted is very old.  I haven't been at Lexicon for more than two years.  While it was my intent to take those bug fixes back to the hardware boxes, Harman may have different plans for what they're going to do.

---

### Post #338 -- Page 12
**User:** aramism
**Info:** Joined: Feb 2009Posts: 1,219🎧 15 years | Posts: 1,219
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10379480&postcount=338>

I got a 224x a few months back and it is just the most beautiful reverb. 


Btw for those asking, beamish electronics in Ohio still service all the old lexicon stuff. Had my 224x serviced there and they did a hell of a job. 


I'm still not done exploring this thing. I have several other "high end" and "vintage" reverb units but this one has the most character. Before I got a manual I had no clue what was what and was totally flying blind just pressing buttons. but everything I put it on just sounded good. After I got a manual after a few months it turned out the old concert hall was my favorite for a big lush "real estate consuming" sound.

---

### Post #339 -- Page 12
**User:** aramism
**Info:** Joined: Feb 2009Posts: 1,219🎧 15 years | Posts: 1,219
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10379482&postcount=339>

I got a 224x a few months back and it is just the most beautiful reverb. 


Btw for those asking, beamish electronics in Ohio still service all the old lexicon stuff. Had my 224x serviced there and they did a hell of a job. 


I'm still not done exploring this thing. I have several other "high end" and "vintage" reverb units but this one has the most character. Before I got a manual I had no clue what was what and was totally flying blind just pressing buttons. but everything I put it on just sounded good. After I got a manual after a few months it turned out the old concert hall was my favorite for a big lush "real estate consuming" sound.

---

### Post #340 -- Page 12
**User:** anguswoodhead
**Info:** Joined: Feb 2008Posts: 3,073My Recordings/CreditsMy Studio🎧 15 years | Posts: 3,073My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13137932&postcount=340>

On a budget it sounds like the PCM91 is the best way to get that Lexicon sound (specifically Random Hall) in hardware form correct?

---

### Post #341 -- Page 12
**User:** icenine18
**Info:** Joined: Oct 2007Posts: 31🎧 15 years | Posts: 31
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13138132&postcount=341>

Quote: > Originally Posted byanguswoodhead➡️On a budget it sounds like the PCM91 is the best way to get that Lexicon sound (specifically Random Hall) in hardware form correct?I'm no lex expert, but that sounds like your best bet.  I love mine.  


Unfortunately after owning it for the last four years, it stopped powering up a couple months ago.  Going to take a look at it soon...hoping its something easy to fix.

---

### Post #342 -- Page 12
**User:** Fishmed
**Info:** Joined: Jun 2007Posts: 1,1511 Review written🎧 15 years | Posts: 1,151
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13138156&postcount=342>

Quote: > Originally Posted byicenine18➡️I'm no lex expert, but that sounds like your best bet.  I love mine.Unfortunately after owning it for the last four years, it stopped powering up a couple months ago.  Going to take a look at it soon...hoping its something easy to fix.The power on my PCM-91 gets a little finicky at times.

---

### Post #343 -- Page 12
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13138741&postcount=343>

Both our PCM80 and 90 stopped powering on. We ended up throwing one of them away because replacement parts were unavailable. The other sits in a rack somewhere in storage. Power issues aren't uncommon, so, although it might be the cheapest option, maybe a used PCM isn't the best path.

---

### Post #344 -- Page 12
**User:** Wayne
**Info:** Joined: Dec 2003Posts: 4,513🎧 20 years | Posts: 4,513
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13138824&postcount=344>

It's kind of sad to see these 80 and 90's dying out. They're such amazing and deep boxes- especially the 80. I still have one each still hanging in thankfully... so far.

---

### Post #345 -- Page 12
**User:** Grimulkan
**Info:** Joined: Mar 2015Posts: 653My Studio🎧 10 years | Posts: 653My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13139122&postcount=345>

True, very sad, though I have not encountered issues yet.


I feel a lot of 90s gear falls into this (expanding?) dark age category where stuff is too integrated/proprietary to repair without official support.


I've fully functional through-hole gear that's older than I am, with drawers full of replacement parts. But the shelf is full of later Ensoniqs and TCs that have sung their last and I fear they beckon to the Lexis.

---

### Post #346 -- Page 12
**User:** ziggysane
**Info:** Joined: Jan 2014Posts: 919🎧 10 years | Posts: 919
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13894858&postcount=346>

Quote: > Originally Posted byqtuner➡️In the next 10 years, what areas in effects processing do you think will see the most innovation?  Will we see big advances in algorithms/new algorithms or is effort mostly concentrated on DAW integration?
Quote: > Originally Posted byDeleted Nobody Special ➡️Can I answer that question in 10 years?  If I was that good at predicting things, my 401K would still be worth somethingThis is one of the all time great GS threads, IMO.  For me it’s a humbling trip to read back through Sean picking Michael and Casey’s brains and learning some of the answers to the questions that he in turn answers down the road in the Valhalla discussions a few years later.


So Michael, what do you think the biggest advancements of the last 10 years have been?

---

### Post #347 -- Page 12
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13895048&postcount=347>

Quote: > Originally Posted byziggysane➡️So Michael, what do you think the biggest advancements of the last 10 years have been?
Quote: > Originally Posted byMichael Carnes➡️Can I answer that question in 10 years?

AARRRRGGGHHHH 


I HAVE HAD THIS BOOKMARKED FOR YEARS SO I COULD ASK HIM THIS ON APRIL 4TH AND YOU HAD TO BLOW YOUR LOAD EARLY. 


I'm not even joking. I've had this saved at the top of my bookmarks and even thought about posting this a few days ago but decided against it because if I waited this long, then shooting early like a high schooler would have just ruined the whole thing.


Anyway, I'll still ask Michael on April 4th since I've had this saved for years, so Michael, kindly refrain from answering so this can be done the right way on April 4th and actually answered 10 years to the day.

---

### Post #348 -- Page 12
**User:** Deleted ab0a387Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13896304&postcount=348>

(responding for subscribe)

---

### Post #349 -- Page 12
**User:** anguswoodhead
**Info:** Joined: Feb 2008Posts: 3,073My Recordings/CreditsMy Studio🎧 15 years | Posts: 3,073My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13896341&postcount=349>

I ended up selling my PCM models 

And bought 480L & 224XL

So good !!!!!

---

### Post #350 -- Page 12
**User:** Snoggin
**Info:** Joined: Apr 2011Posts: 1,131My Studio🎧 15 years | Posts: 1,131My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13896431&postcount=350>

Quote: > Originally Posted byanguswoodhead➡️I ended up selling my PCM modelsAnd bought 480L & 224XLSo good !!!!!I’m with you   I have 480L,2 bricasti,eventide H8k and Orville all with remotes and located in machine room. Also 2 moog delays ,and also 2 moog ladders 


Have a fultone tte I need to fix and get up and running again   I just like hardware

---

### Post #351 -- Page 12
**User:** anguswoodhead
**Info:** Joined: Feb 2008Posts: 3,073My Recordings/CreditsMy Studio🎧 15 years | Posts: 3,073My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13896492&postcount=351>

Quote: > Originally Posted bySnoggin➡️I just like hardware100% with you there.

---

### Post #352 -- Page 12
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13897213&postcount=352>

Quote: > Originally Posted byionian➡️Anyway, I'll still ask Michael on April 4th since I've had this saved for years, so Michael, kindly refrain from answering so this can be done the right way on April 4th and actually answered 10 years to the day.

---

### Post #353 -- Page 12
**User:** raal
**Info:** Joined: Dec 2004Posts: 5,958My Studio1 Review written🎧 20 years | Posts: 5,958My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13897753&postcount=353>

Quote: > Originally Posted byionian➡️Anyway, I'll still ask Michael on April 4th since I've had this saved for years, so Michael, kindly refrain from answering so this can be done the right way on April 4th and actually answered 10 years to the day.

---

### Post #354 -- Page 12
**User:** Sigma
**Info:** Joined: May 2006Posts: 6,814My Recordings/CreditsMy Studio🎧 20 years | Posts: 6,814My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13899187&postcount=354>

lol phil ramone and i were joking about it..i mentioned spin and wander and before i could say i never got to those pages he goes.."if i can't hit 1 or 2 buttons on page one and get what i want i  go to another piece of gear

---

### Post #355 -- Page 12
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13905141&postcount=355>

Quote: > Originally Posted byqtuner➡️In the next 10 years, what areas in effects processing do you think will see the most innovation?  Will we see big advances in algorithms/new algorithms or is effort mostly concentrated on DAW integration?  (I hope not).  I think the latest realtime hardware effect to be invented is the Access Music atomizer on the Virus TI.
Quote: > Originally Posted byMichael Carnes➡️Can I answer that question in 10 years?  If I was that good at predicting things, my 401K would still be worth something.Hey Michael - You posted this on April 4th, 2009.  Today is April 4th 2019, making it** EXACTLY** 10 years **TO THE DAY** of this post!  Where do you think the most innovation has been done in effects processing?  Do you think algorithmic reverbs have become kind of stale?  Have there been advances in it or is it all just variations on a theme?


Also congrats on the sale of exponential to izotope.  I'm sure 10 years ago when you posted this you never would have imagined that you would have left Lexicon, created your own plug in company.  Released a number of high quality plugs, and then had the company bought by izotope!  A lot can happen in 10 years.

---

### Post #356 -- Page 12
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13905409&postcount=356>

That's quite a set of questions!  I'll have to respond in a fairly brief way (as you can imagine, things are busy right now), but perhaps we can keep the line open for a while
Quote: > Originally Posted byionian➡️Hey Michael - You posted this on April 4th, 2009.  Today is April 4th 2019, making itEXACTLY10 yearsTO THE DAYof this post!  Where do you think the most innovation has been done in effects processingAn awful lot has happened and I don't think there's any single winner.  But I think there have been enormous advances in restoration software.  I've used RX for quite a while (that part should be obvious).  I've cleaned up modern recordings (took a passing group of Harleys out of a string quartet once) and given new life to recordings that are 40 years old.  Tools of this nature have become indispensable.  There are also great new mastering tools.  Our knowledge of what loudness really is has grown a lot.  And all the sorts of digital distribution have really forced us to cope with this.  Tools have gotten good and they'll get a lot better.


And there are plugins that emulate just about every vintage piece of hardware that ever was.  As the boxes die, people who want those sounds will have affordable alternatives.
Quote: > Do you think algorithmic reverbs have become kind of stale?  Have there been advances in it or is it all just variations on a theme?If ever there was a leading question, that's one.  I can't really speak about verbs other than Exponential's.  I've only been interested in making mine do what I think they should, and I've never done any sort of competitive research. But from my point of view, a lot has happened and a lot more will happen in the next ten years.  Ten years ago, did you envision an in-the-box reverb that could do immersive audio--going as high as 22.2?  Did you imagine that you could run multiple copies in one computer? Did you image that you could do all of that at high sample rates?  You can now: better, and for a lot less money than a hardware alternative just a few years  back.


There are probably two basic threads going along in algorithmic reverb development.  There are quite a few (generally convolvers) that work to emulate a specific physical space--based entirely on provable physics. Many of those work very well, but it's not an area of much interest to me.  In my world, I'm driven by what you actually *hear*.  That's not the same thing as what happened in the room.  Your brain throws away most of the information that comes into your ears--a super computer couldn't deal with all that data in real time.  There's an amazing sort of data reduction that goes on, and I'm not aware that we have much understanding of what's happening neurologically.  At any rate, one of the things that's left over is the phenomenon we call reverberation.  A lot of what algorithmic reverbs do is based on that.


Then finally, I (and others) have done a lot of work to make algorithmic reverbs into more flexible tools.  And there's still room for improvement.  So no, the field is not at all stale.
Quote: > Also congrats on the sale of exponential to izotope.  I'm sure 10 years ago when you posted this you never would have imagined that you would have left Lexicon, created your own plug in company.  Released a number of high quality plugs, and then had the company bought by izotope!  A lot can happen in 10 years.Yeah, that's the part I didn't see coming.  I don't think I'll be moving into the field of fortune-telling.

---

### Post #357 -- Page 12
**User:** Crazy4Jazz
**Info:** Joined: Mar 2016Posts: 1,535🎧 10 years | Posts: 1,535
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13906628&postcount=357>

Can you talk a little about what’s in store in restoration software?

---

### Post #358 -- Page 12
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13906800&postcount=358>

Quote: > Originally Posted byCrazy4Jazz➡️Can you talk a little about what’s in store in restoration software?Not from any position of actual knowledge.  I suspect that software will have better ways to determine what you want and what you don't We might have better ways to clean up distorted signals and perhaps we might be able to tell an alto sax from a tenor.  Who knows?


I don't think we'll quite be able to move the mic to where it should have been in the first place or undo overdone pitch correction.  But one skill builds on another and I do think we're just getting started.

---

### Post #359 -- Page 12
**User:** mattdaddy1970
**Info:** Joined: Feb 2019Posts: 19🎧 5 years | Posts: 19
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13908423&postcount=359>

Hey all - I sure hope you can help (and that this is the correct place to post)... I just recently was handed a Lex 224x that was in storage for 20 (+?) years.  One heck of a gift for sure!  Great condition, all things considered.  No error messages on the blue remote and in good shape, all around.  BUT!  Output is all noise, with the exception of very faint reverb in the way background (I can make out tweaks to the programs even, but so much noise!)

Now - I dug in a bit (not an engineer, but know a little and have done exhaustive research on this piece) and found the hardware diagnostic led's.  The ARUCK Error (on the T&C card) led is dark (a good thing) but there are two other led's that are lit.  In the manual it states that there are two led's on the DMEM board (MS Generator error and Row Select error).

Here is where it gets weird and I am flummoxed: The two led's that ARE lit are actually on the OPT/NVS card (top row of the stack),  not the DMEM board - and as far as I can tell, the DMEM card HAS NO LED'S at all!  The OPT card actually has 3 led's but they are labelled ER1, ER2 and ER3 (not MS Gen or Row Sel).  Could these be battery indicators?  I thought the cards might have been switched and replaced in the wrong shelf, but both clearly state what they are on the card, and they are where they should be.

Can anyone chime in on this?  So many thanks for any and all help! 

(I'm still getting my sea legs for using the site, so apologies if this is posted in the wrong place!)

---

### Post #360 -- Page 12
**User:** Deleted Nobody Special 🎙️Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13908539&postcount=360>

I'm afraid I can't help you with that.  There might be someone else on this thread who knows a bit.  If you hunt around on the forum, you might find Jim Williams.  I believe he's got some experience working on those older pieces.  Good luck on putting it back to work!


---

## Page 13

---

### Post #361 -- Page 13
**User:** anguswoodhead
**Info:** Joined: Feb 2008Posts: 3,073My Recordings/CreditsMy Studio🎧 15 years | Posts: 3,073My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13908584&postcount=361>

Quote: > Originally Posted bymattdaddy1970➡️Hey all - I sure hope you can help (and that this is the correct place to post)... I just recently was handed a Lex 224x that was in storage for 20 (+?) years.  One heck of a gift for sure!  Great condition, all things considered.  No error messages on the blue remote and in good shape, all around.  BUT!  Output is all noise, with the exception of very faint reverb in the way background (I can make out tweaks to the programs even, but so much noise!)Now - I dug in a bit (not an engineer, but know a little and have done exhaustive research on this piece) and found the hardware diagnostic led's.  The ARUCK Error (on the T&C card) led is dark (a good thing) but there are two other led's that are lit.  In the manual it states that there are two led's on the DMEM board (MS Generator error and Row Select error).Here is where it gets weird and I am flummoxed: The two led's that ARE lit are actually on the OPT/NVS card (top row of the stack),  not the DMEM board - and as far as I can tell, the DMEM card HAS NO LED'S at all!  The OPT card actually has 3 led's but they are labelled ER1, ER2 and ER3 (not MS Gen or Row Sel).  Could these be battery indicators?  I thought the cards might have been switched and replaced in the wrong shelf, but both clearly state what they are on the card, and they are where they should be.Can anyone chime in on this?  So many thanks for any and all help!(I'm still getting my sea legs for using the site, so apologies if this is posted in the wrong place!)[http://https://www.proharmonic.com](http://https://www.proharmonic.com)


My 224XL had issues

Rob Squire from ProHarmonic in Adelaide Australia got it working perfectly. 

Here’s his website

Send him a message.

---

### Post #362 -- Page 13
**User:** ziggysane
**Info:** Joined: Jan 2014Posts: 919🎧 10 years | Posts: 919
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14311517&postcount=362>

Since this is the Godfather of all Lexicon related threads...


I found the original 480 manual online (I don’t even remember what I was looking for; possibly something about saving a vocal where the singer was eating the mic), and wow: that manual is a thing of beauty. 


It was fascinating to see the amount of detail and thought that went into each preset in each program, along with suggestions with how they might be used based on the original intended design. I know that read the manual is a cliché nowadays, but I would highly recommend checking the 480L manual out if you never have.

---

### Post #363 -- Page 13
**User:** italo de angelis
**Info:** Joined: Oct 2010Posts: 2,069🎧 15 years | Posts: 2,069
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14311844&postcount=363>

Quote: > Originally Posted byziggysane➡️Since this is the Godfather of all Lexicon related threads...I found the original 480 manual online (I don’t even remember what I was looking for; possibly something about saving a vocal where the singer was eating the mic), and wow: that manual is a thing of beauty.It was fascinating to see the amount of detail and thought that went into each preset in each program, along with suggestions with how they might be used based on the original intended design. I know that read the manual is a cliché nowadays, but I would highly recommend checking it out if you never have.THAT manual is a thing of beauty! It belongs to a time when most companies would write excellent documentation and provide details on algorithms, drawings, tech specs and even "white papers" topics.

Today the user manual is a joke. Even the tech details are disappeared or are incorrect and that should not be legal. The dumbness of content is embarassing and offensive to the user. This trash trend about "simplicity" makes no sense.

Technolgy in its artform deserves good info and plenty of it. Let's just hope the tide shifts... or we doomed!

---

### Post #364 -- Page 13
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14312001&postcount=364>

Where can we find the online manual for the 480L?

---

### Post #365 -- Page 13
**User:** ziggysane
**Info:** Joined: Jan 2014Posts: 919🎧 10 years | Posts: 919
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14312309&postcount=365>

Quote: > Originally Posted byelambo➡️Where can we find the online manual for the 480L?[https://www2.spsc.tugraz.at/add_mate...80l_manual.pdf](https://www2.spsc.tugraz.at/add_material/audiotechnik/manuals/10_RP1/Lexicon/lexicon_480l_manual.pdf)

---

### Post #366 -- Page 13
**User:** elambo
**Info:** Joined: Aug 2004Posts: 17,4331 Review written🎧 20 years | Posts: 17,433
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14312386&postcount=366>

Quote: > Originally Posted byziggysane➡️https://www2.spsc.tugraz.at/add_mate...80l_manual.pdfThank you!

---

### Post #367 -- Page 13
**User:** locust_tree
**Info:** Joined: Feb 2012Posts: 701My Studio1 Review written🎧 10 years | Posts: 701My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14312404&postcount=367>

Quote: > Originally Posted byitalo de angelis➡️THAT manual is a thing of beauty! It belongs to a time when most companies would write excellent documentation and provide details on algorithms, drawings, tech specs and even "white papers" topics.Today the user manual is a joke. Even the tech details are disappeared or are incorrect and that should not be legal. The dumbness of content is embarassing and offensive to the user. This trash trend about "simplicity" makes no sense.Technolgy in its artform deserves good info and plenty of it. Let's just hope the tide shifts... or we doomed!Even the paper stock that those old Lex manuals was printed on was a heavy, high gloss stock nicer than most magazines. Quality documentation indeed!

---

### Post #368 -- Page 13
**User:** italo de angelis
**Info:** Joined: Oct 2010Posts: 2,069🎧 15 years | Posts: 2,069
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14312534&postcount=368>

Quote: > Originally Posted byelambo➡️Where can we find the online manual for the 480L?Several revisions manuals AND the mighty Classic Cart, adding 224 magic to the 480:
[https://lexiconpro.com/en-US/products/m480l](https://lexiconpro.com/en-US/products/m480l)

---

### Post #369 -- Page 13
**User:** acidtechno
**Info:** Joined: Dec 2018Posts: 529My Studio🎧 5 years | Posts: 529My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14377324&postcount=369>

Does anyone have any information on how many different “custom algorithm fx & preset cards” were created for the units?

---

### Post #370 -- Page 13
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14377819&postcount=370>

Two from Lexicon. HD cart is the other one. 


-Casey

---

### Post #371 -- Page 13
**User:** Jim Williams
**Info:** Joined: Feb 2004Posts: 18,048My Recordings/Credits1 Review written🎧 20 years | Posts: 18,048My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14377876&postcount=371>

For over 20 years I've used the excellent Analog Devices AD823 fet opamp for Lexicon sample and hold duties. It features a fast settllng time with minimal overshoot compared to the older LF353. One drawback is it's 18 nv/hz/sq noise spec.


AD has released the new ADA4625-2 dual fet opamp. This rail to rail part has a faster slew rate, less overshoot and a better settling time. At 3.3 nv noise, it's also the second lowest noise fet opamp available after the OPA1652. Like the AD823AN, it's also expensive. You do get what you pay for as the performance is stellar. In an old SPX-90 it offers "main frame" performance and density if you also up the speed of the multiplexers to match.

---

### Post #372 -- Page 13
**User:** locust_tree
**Info:** Joined: Feb 2012Posts: 701My Studio1 Review written🎧 10 years | Posts: 701My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14395670&postcount=372>

Greetings slutz, figured this was the right thread to share some general thoughts about vintage Lexicon gear as I own a fair amount of it (LXP1 and 5 with MRC, PCM70 and a pair of Model 300s).


In my mind the "Lexicon sound" seems to divide into roughly 2 eras - the 200 series and its derivations (224, X and XL, 200, PCM60 and 70), characterized by a grittier top end character, less density and movement in the early reflections and tails, and a more pronounced modulation style - and the later 480 derived sound which could include the 300 all the way down to the lowly LXPs, Alex and Reflex which AFAIK were running heavily bastardized and dumbed-down 480 algos.


Although I adore my PCM70 (and on the right sources nothing else will do), I have always found it strange to see the 70 recommended as the go-to "entry point" for vintage mid-hi-end Lex, since for my money even the LXP1 and a Reflex I used long ago are closer to what I think most people hear in their heads when imagining the Lex sound, at least as regards tail density and reflection characteristics. Obviously those early attempts at "budget" Lex have far less granularity of control and the delay lines are nowhere near as powerful as a 70, not to mention their build quality (my LXPs are hobbling along on life support) but speaking strictly about the sound of the reverb algos, I think they are closer to the mark than the 70 unless you need the big Vangelis modulated concert hall thing. 


Apparently the 70's algorithms were ported from the 224X, which I've never had the pleasure of using, but on many sources the 70 sounds a little threadbare and I have a hard time imagining that's what a 224X sounded like. For what it's worth I have a "power user" 3.01 unit with the version 2 presets in the user registers. (I find myself wondering how exactly Tiled Room was used on drums since it's one of those sneaky "reverb? What reverb?" presets that seems to work best with its width reduced and giving way to a longer plate sound from another unit panned hard). The 70's strong points to me are its incredibly flexible 6 delays and modulated 224-style halls. It would not be even close to my first recommendation for someone looking for a strictly reverb box.


My 300s of course are on a whole 'nother level from everything I've mentioned so far but that's another post for another time. Not really sure where I was going with all this but it's nice to talk about Lexicon stuff.

---

### Post #373 -- Page 13
**User:** anguswoodhead
**Info:** Joined: Feb 2008Posts: 3,073My Recordings/CreditsMy Studio🎧 15 years | Posts: 3,073My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14395741&postcount=373>

Quote: > Originally Posted bylocust_tree➡️Greetings slutz, figured this was the right thread to share some general thoughts about vintage Lexicon gear as I own a fair amount of it (LXP1 and 5 with MRC, PCM70 and a pair of Model 300s).In my mind the "Lexicon sound" seems to divide into roughly 2 eras - the 200 series and its derivations (224, X and XL, 200, PCM60 and 70), characterized by a grittier top end character, less density and movement in the early reflections and tails, and a more pronounced modulation style - and the later 480 derived sound which could include the 300 all the way down to the lowly LXPs, Alex and Reflex which AFAIK were running heavily bastardized and dumbed-down 480 algos.Although I adore my PCM70 (and on the right sources nothing else will do), I have always found it strange to see the 70 recommended as the go-to "entry point" for vintage mid-hi-end Lex, since for my money even the LXP1 and a Reflex I used long ago are closer to what I think most people hear in their heads when imagining the Lex sound, at least as regards tail density and reflection characteristics. Obviously those early attempts at "budget" Lex have far less granularity of control and the delay lines are nowhere near as powerful as a 70, not to mention their build quality (my LXPs are hobbling along on life support) but speaking strictly about the sound of the reverb algos, I think they are closer to the mark than the 70 unless you need the big Vangelis modulated concert hall thing.Apparently the 70's algorithms were ported from the 224X, which I've never had the pleasure of using, but on many sources the 70 sounds a little threadbare and I have a hard time imagining that's what a 224X sounded like. For what it's worth I have a "power user" 3.01 unit with the version 2 presets in the user registers. (I find myself wondering how exactly Tiled Room was used on drums since it's one of those sneaky "reverb? What reverb?" presets that seems to work best with its width reduced and giving way to a longer plate sound from another unit panned hard). The 70's strong points to me are its incredibly flexible 6 delays and modulated 224-style halls. It would not be even close to my first recommendation for someone looking for a strictly reverb box.My 300s of course are on a whole 'nother level from everything I've mentioned so far but that's another post for another time. Not really sure where I was going with all this but it's nice to talk about Lexicon stuff.Nice post

I had 224XL - forced to sell sadly...

I bought PCM60 to use where I was using 224XL - instrument ambience

I use my 480L for main vocal verb and drum room

Lexicon is the best IMHO

Although I do have a TC Electronics Hall Of Fame reverb pedal on my guitar peal board and it's incredible.

---

### Post #374 -- Page 13
**User:** Oldone
**Info:** Joined: Dec 2002Posts: 3,605My Studio🎧 20 years | Posts: 3,605My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14395886&postcount=374>

locust_tree


Really great and useful post. I want to hear those 300 stories as I have one with the last rev of algos and chips. Thanks for posting.

---

### Post #375 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14396658&postcount=375>

Quote: > Originally Posted bylocust_tree➡️Greetings slutz, figured this was the right thread to share some general thoughts about vintage Lexicon gear as I own a fair amount of it (LXP1 and 5 with MRC, PCM70 and a pair of Model 300s).In my mind the "Lexicon sound" seems to divide into roughly 2 eras - the 200 series and its derivations (224, X and XL, 200, PCM60 and 70), characterized by a grittier top end character, less density and movement in the early reflections and tails, and a more pronounced modulation style - and the later 480 derived sound which could include the 300 all the way down to the lowly LXPs, Alex and Reflex which AFAIK were running heavily bastardized and dumbed-down 480 algos.Although I adore my PCM70 (and on the right sources nothing else will do), I have always found it strange to see the 70 recommended as the go-to "entry point" for vintage mid-hi-end Lex, since for my money even the LXP1 and a Reflex I used long ago are closer to what I think most people hear in their heads when imagining the Lex sound, at least as regards tail density and reflection characteristics. Obviously those early attempts at "budget" Lex have far less granularity of control and the delay lines are nowhere near as powerful as a 70, not to mention their build quality (my LXPs are hobbling along on life support) but speaking strictly about the sound of the reverb algos, I think they are closer to the mark than the 70 unless you need the big Vangelis modulated concert hall thing.Apparently the 70's algorithms were ported from the 224X, which I've never had the pleasure of using, but on many sources the 70 sounds a little threadbare and I have a hard time imagining that's what a 224X sounded like. For what it's worth I have a "power user" 3.01 unit with the version 2 presets in the user registers. (I find myself wondering how exactly Tiled Room was used on drums since it's one of those sneaky "reverb? What reverb?" presets that seems to work best with its width reduced and giving way to a longer plate sound from another unit panned hard). The 70's strong points to me are its incredibly flexible 6 delays and modulated 224-style halls. It would not be even close to my first recommendation for someone looking for a strictly reverb box.My 300s of course are on a whole 'nother level from everything I've mentioned so far but that's another post for another time. Not really sure where I was going with all this but it's nice to talk about Lexicon stuff.I agree that there are essentially 2 schools of thought in the Lexicon retrospective, and I much prefer the early algos, ranging from the 224 (non "x" or "xl") to the PCM-70 and my interest in Lexicon diminished greatly after the 480 was introduced.


For over a decade I owned a mint ca~1979 224 (the one with the beige metal remote on a DB25 parallel interface to the CPU) and know it intimately.  When people talk about "The Lexicon Sound" this is what they mean. It was groundbreaking in terms of it's flexibility and introduced parameters to the user that no other reverb before allowed access to while at the same time none of the user adjustments "broke" the algos. For example, by rev 3 they allowed the user to control the diffusion within the reverb FDN, increasing the diffusion here meant that the reverb "density" increased as the sound decayed, allowed for very smooth reverb tails, or very sparse reflections depending on the setting. Other reverbs of the time from Sony, AMS, EMT, Eventide, etc had fixed diffusion at the input to the FDN and sometimes had audible loops and reflections in the reverb tails, these are known as "Constant Density" reverbs.  


When people describe digital reverbs as "grainy" they are usually referring to low diffusion, due to the audibility of the individual taps, and sadly it's become an annoyingly demeaning and generically overused misapprehension of what is actually happening in the reverb itself, I've even heard people ascribe that sound to the converters or analog stages, but it's complete nonsense, it's all in the algos.


 The 224 had no "size" parameter but did offer a proportionally scaled down version of the concert hall called the "Small Chamber".  It also had a unique parameter to adjust the mix of 3 sets of output taps called "depth" that allowed you to simulate a source placed at various distances. 


When the 224X and later the XL (which introduced the "LARC" plastic remote on a 9 pin serial cable), they increased the sample rate (and by necessity the memory) - the original 224 had a 20.6kHz (IIRC) sample rate - and as the complexity and sophistication increased over the life of that product they had introduced even more user adjustments, including "Size"  several controllable early reflections, the ability to adjust the diffusion at the input or in the FDN (so you could get any combination of diffused tails or constant density).


These last "Lexicon Era 1" reverb algos were ported to the PCM-70, with only 2 minor differences - a slightly lower 15kHz bandwidth (still 50% higher than the original 224) and only a mono input.  To be fair, most studios at the time were multing their aux send to both inputs of the 224 anyway.  These "Era 1" algos all had a specific type of random modulation in the FDN allpass network which is also a primary feature of the "Lexicon Sound" , it's just beautiful and dreamy and evocative and haunting.  It was later deemed "unnatural"  and subsequent Lexicon reverbs used a random stepped interpolation to break up the resonant modes which exhibited no pitch modulation.  Ho hum.. this is where I lost interest. I currently use 2 PCM-70s in my mix room.

---

### Post #376 -- Page 13
**User:** raal
**Info:** Joined: Dec 2004Posts: 5,958My Studio1 Review written🎧 20 years | Posts: 5,958My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14396952&postcount=376>

Really interesting posts!  Guess i'm more of a 480L guy, maybe because they we're popular in the 80's which is when i got my feet wet. Most 224s had been phased out by then (at least that's my recollection). Still have a 480L. Have also had PCM 70's through the years but my recollection is they had a fair amount of self-nosie, and i found myself reaching for them only after having run out of more preferred reverbs (480L, AMS, TC 5000 etc.).

---

### Post #377 -- Page 13
**User:** Deleted dbbd9a8Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14397089&postcount=377>

Quote: > Originally Posted byitalo de angelis➡️THAT manual is a thing of beauty! It belongs to a time when most companies would write excellent documentation and provide details on algorithms, drawings, tech specs and even "white papers" topics.Today the user manual is a joke. Even the tech details are disappeared or are incorrect and that should not be legal. The dumbness of content is embarassing and offensive to the user. This trash trend about "simplicity" makes no sense.Technolgy in its artform deserves good info and plenty of it. Let's just hope the tide shifts... or we doomed!Man,your post remembers me the shameful user manual of my Roland SE-02.

It's the same for all Roland boutique synths.

I had never seen a so bad user manual in my entire life.

---

### Post #378 -- Page 13
**User:** acidtechno
**Info:** Joined: Dec 2018Posts: 529My Studio🎧 5 years | Posts: 529My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14400326&postcount=378>

does anyone here have any insight about the different PCM-70 OS versions?

---

### Post #379 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14400439&postcount=379>

Quote: > Originally Posted byacidtechno➡️does anyone here have any insight about the different PCM-70 OS versions?In the most cursory sense, here are the main differences: Version 1.2 was the earliest update and fixed some bugs, Version 2 added more features and version 3 added a new effect algo ("Inverse Room") and expanded the MIDI functionality to include parameter access via sysex.

---

### Post #380 -- Page 13
**User:** acidtechno
**Info:** Joined: Dec 2018Posts: 529My Studio🎧 5 years | Posts: 529My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14400574&postcount=380>

Quote: > Originally Posted byzmix➡️In the most cursory sense, here are the main differences: Version 1.2 was the earliest update and fixed some bugs, Version 2 added more features and version 3 added a new effect algo ("Inverse Room") and expanded the MIDI functionality to include parameter access via sysex.thank you

---

### Post #381 -- Page 13
**User:** locust_tree
**Info:** Joined: Feb 2012Posts: 701My Studio1 Review written🎧 10 years | Posts: 701My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14401301&postcount=381>

Quote: > Originally Posted byanguswoodhead➡️Nice postI had 224XL - forced to sell sadly...I bought PCM60 to use where I was using 224XL - instrument ambienceI use my 480L for main vocal verb and drum roomLexicon is the best IMHOAlthough I do have a TC Electronics Hall Of Fame reverb pedal on my guitar peal board and it's incredible.Would love to hear your thoughts on how well the the PCM60 does the 224XL's job. I have seen them mentioned more often lately. The no-fuss button interface looks nice but I also remember reading a warning from someone here on GS saying to pass it up for a 70 - something like "oh, PCM60s are very versatile - they can sound like any submarine or oil drum you like" 


As for TC I'd still jump at the chance to try one of their nicer units. Played with an M-One XL years ago and it left me cold, but I have heard amazing vocal plate clips from a Reverb 4000 (granted this was a solo'd vocal so who knows how they sit in a mix).

Quote: > Originally Posted byOldone➡️locust_treeReally great and useful post. I want to hear those 300 stories as I have one with the last rev of algos and chips. Thanks for posting.My pleasure. Both my 300's are also running v3.5 - do you ever get the impression that it's not quite a stable software? Extreme RT and mod settings can make most of the halls start self-oscillating and some of the split patches make the unit slow down so much that even the front meter ballistics get screwed up.


This seems a good time to clarify that the 300 was not and never will be a true *dual stereo engine* unit. The split patches run compromised algorithms and there is no configuration where you get each engine generating discrete stereo wet signal! I think this needs to be shouted from the rooftops as the hype surrounding v3.5 has reached a fever pitch with some GS users advising others to walk away, no questions asked, from any Model 300 running a lower firmware.


At any rate, the good far outweighs the bad with these units. This is when Lex made the jump to Delta-Sigma conversion so the converters impart far less color than those of the 480L, which is probably why most who have owned both say they prefer the 480. However I remember Casey from Bricasti saying that the 300 algos are in some ways more advanced than the 480's, with greater density (maybe due to more memory? I'm spotty on the specifics). I was originally driven to buy one because years ago I was given an old set of Voxengo IR's from a version 1 unit and I drove myself insane trying to recreate those sounds on my other outboard verbs - none could even get close. 


To own one is to constantly shake off the uncanny feeling of having heard these sounds on so many great records (particularly early 90s Nashville stuff) and the feeling that you're cheating in some way because running a 300 with a console just gets it sounding like a record so fast. One thing that took getting used to - especially coming from the PCM70 - is that every algorithm and preset works on everything, i.e. even the hall presets sound killer on drums with minor tweaks to RT. You can get away with so much wet signal and it just sounds like the source is moving further into the simulated room.


Quote: > Originally Posted byzmix➡️I agree that there are essentially 2 schools of thought in the Lexicon retrospective, and I much prefer the early algos, ranging from the 224 (non "x" or "xl") to the PCM-70 and my interest in Lexicon diminished greatly after the 480 was introduced.For over a decade I owned a mint ca~1979 224 (the one with the beige metal remote on a DB25 parallel interface to the CPU) and know it intimately.  When people talk about "The Lexicon Sound" this is what they mean. It was groundbreaking in terms of it's flexibility and introduced parameters to the user that no other reverb before allowed access to while at the same time none of the user adjustments "broke" the algos. For example, by rev 3 they allowed the user to control the diffusion within the reverb FDN, increasing the diffusion here meant that the reverb "density" increased as the sound decayed, allowed for very smooth reverb tails, or very sparse reflections depending on the setting. Other reverbs of the time from Sony, AMS, EMT, Eventide, etc had fixed diffusion at the input to the FDN and sometimes had audible loops and reflections in the reverb tails, these are known as "Constant Density" reverbs.When people describe digital reverbs as "grainy" they are usually referring to low diffusion, due to the audibility of the individual taps, and sadly it's become an annoyingly demeaning and generically overused misapprehension of what is actually happening in the reverb itself, I've even heard people ascribe that sound to the converters or analog stages, but it's complete nonsense, it's all in the algos.The 224 had no "size" parameter but did offer a proportionally scaled down version of the concert hall called the "Small Chamber".  It also had a unique parameter to adjust the mix of 3 sets of output taps called "depth" that allowed you to simulate a source placed at various distances.When the 224X and later the XL (which introduced the "LARC" plastic remote on a 9 pin serial cable), they increased the sample rate (and by necessity the memory) - the original 224 had a 20.6kHz (IIRC) sample rate - and as the complexity and sophistication increased over the life of that product they had introduced even more user adjustments, including "Size"  several controllable early reflections, the ability to adjust the diffusion at the input or in the FDN (so you could get any combination of diffused tails or constant density).These last "Lexicon Era 1" reverb algos were ported to the PCM-70, with only 2 minor differences - a slightly lower 15kHz bandwidth (still 50% higher than the original 224) and only a mono input.  To be fair, most studios at the time were multing their aux send to both inputs of the 224 anyway.  These "Era 1" algos all had a specific type of random modulation in the FDN allpass network which is also a primary feature of the "Lexicon Sound" , it's just beautiful and dreamy and evocative and haunting.  It was later deemed "unnatural"  and subsequent Lexicon reverbs used a random stepped interpolation to break up the resonant modes which exhibited no pitch modulation.  Ho hum.. this is where I lost interest. I currently use 2 PCM-70s in my mix room.Amazing stuff Chuck, thank you! I have more or less given up ever coming across an original 224 in the wild, so descriptions like this help me put my PCM70 in context a little better. Some of your post goes a little over my head (I'm guessing FDN is a Feedback Delay Network?) but agree completely that "graininess" as a term of abuse should be retired. Sometimes it's exactly what's called for in a mix (I was surprised by the PCM70's Vox Plate preset and how all the 70's weaknesses became strengths on a vocal - the "spitty" quality cuts right through a track and the ringing you hear isn't the clangy digital ringing of cheap 80s units but more like the ringing you get in a real plate.)


Also agree about the modulation - even on its most extreme settings my 300s don't exhibit that haunting pitch instability. That's what makes the 70 so indispensable on clean guitars and synths, and the reason I will probably never sell it (alongside the irrational sentimental reason that it was the first piece of high-end rack gear I saved up for). Cheers!

---

### Post #382 -- Page 13
**User:** anguswoodhead
**Info:** Joined: Feb 2008Posts: 3,073My Recordings/CreditsMy Studio🎧 15 years | Posts: 3,073My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14401348&postcount=382>

I love the 60's simplicity.

224XL was amazing of course - just beautiful

I'm using the PCM60 Plate on instruments

Just to give each element a sense of space and a small tail

Not overly audible in a mix

Works well.

---

### Post #383 -- Page 13
**User:** researchtriangle
**Info:** Joined: Mar 2015Posts: 275🎧 10 years | Posts: 275
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404337&postcount=383>

Love the PCM70 info in this thread, really interesting.


My only gripe with it is the menu diving needed to tweak sounds (not incredibly awful by some standards, I know - I'm spoiled).


I'm building a nice editor for it so that I can easily visualize and tweak sounds, and it's really opened up the unit for me. I wonder how many of you out there would be interested in software like this? I'm about 75% done with supporting all parameters of all the different algos, I may make the push to make it "production grade" if people are actively looking for a way to supercharge their workflow on the PCM70.

---

### Post #384 -- Page 13
**User:** elegentdrum
**Info:** Joined: Mar 2011Posts: 6,801My Studio🎧 15 years | Posts: 6,801My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404403&postcount=384>

Quote: > Originally Posted byzmix➡️I agree that there are essentially 2 schools of thought in the Lexicon retrospective, and I much prefer the early algos, ranging from the 224 (non "x" or "xl") to the PCM-70 and my interest in Lexicon diminished greatly after the 480 was introduced.For over a decade I owned a mint ca~1979 224 (the one with the beige metal remote on a DB25 parallel interface to the CPU) and know it intimately.  When people talk about "The Lexicon Sound" this is what they mean. It was groundbreaking in terms of it's flexibility and introduced parameters to the user that no other reverb before allowed access to while at the same time none of the user adjustments "broke" the algos. For example, by rev 3 they allowed the user to control the diffusion within the reverb FDN, increasing the diffusion here meant that the reverb "density" increased as the sound decayed, allowed for very smooth reverb tails, or very sparse reflections depending on the setting. Other reverbs of the time from Sony, AMS, EMT, Eventide, etc had fixed diffusion at the input to the FDN and sometimes had audible loops and reflections in the reverb tails, these are known as "Constant Density" reverbs.When people describe digital reverbs as "grainy" they are usually referring to low diffusion, due to the audibility of the individual taps, and sadly it's become an annoyingly demeaning and generically overused misapprehension of what is actually happening in the reverb itself, I've even heard people ascribe that sound to the converters or analog stages, but it's complete nonsense, it's all in the algos.The 224 had no "size" parameter but did offer a proportionally scaled down version of the concert hall called the "Small Chamber".  It also had a unique parameter to adjust the mix of 3 sets of output taps called "depth" that allowed you to simulate a source placed at various distances.When the 224X and later the XL (which introduced the "LARC" plastic remote on a 9 pin serial cable), they increased the sample rate (and by necessity the memory) - the original 224 had a 20.6kHz (IIRC) sample rate - and as the complexity and sophistication increased over the life of that product they had introduced even more user adjustments, including "Size"  several controllable early reflections, the ability to adjust the diffusion at the input or in the FDN (so you could get any combination of diffused tails or constant density).These last "Lexicon Era 1" reverb algos were ported to the PCM-70, with only 2 minor differences - a slightly lower 15kHz bandwidth (still 50% higher than the original 224) and only a mono input.  To be fair, most studios at the time were multing their aux send to both inputs of the 224 anyway.  These "Era 1" algos all had a specific type of random modulation in the FDN allpass network which is also a primary feature of the "Lexicon Sound" , it's just beautiful and dreamy and evocative and haunting.  It was later deemed "unnatural"  and subsequent Lexicon reverbs used a random stepped interpolation to break up the resonant modes which exhibited no pitch modulation.  Ho hum.. this is where I lost interest. I currently use 2 PCM-70s in my mix room.How do you wire the return from a stereo send? Assuming you have them MIDI together as a pair, do you have to use 4 returns or 2 returns?

---

### Post #385 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404487&postcount=385>

Quote: > Originally Posted byelegentdrum➡️How do you wire the return from a stereo send? Assuming you have them MIDI together as a pair, do you have to use 4 returns or 2 returns?I'm not using the 2 PCM-70s a a single stereo reverb, they are used as 2 completely independent reverb units.


I use 2 mono sends, one goes to each PCM-70 and then I return each to it's own stereo channel.

---

### Post #386 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404506&postcount=386>

Quote: > Originally Posted byresearchtriangle➡️Love the PCM70 info in this thread, really interesting.My only gripe with it is the menu diving needed to tweak sounds (not incredibly awful by some standards, I know - I'm spoiled).I'm building a nice editor for it so that I can easily visualize and tweak sounds, and it's really opened up the unit for me. I wonder how many of you out there would be interested in software like this? I'm about 75% done with supporting all parameters of all the different algos, I may make the push to make it "production grade" if people are actively looking for a way to supercharge their workflow on the PCM70.Yes, the 6 pages of parameters accessible only through that front panel is insane.


I have created a plugin that allows me to access all 29 of the PCM-70 parameters within my DAW, and the parameters appear on my mackie C4 control surface's 32 encoders, as well as being fully automatable. It also allows complete recall for each project.


Here is the one for the Concert Hall algo.

![Lexicon reverbs: a brief bestiary-screen-shot-2019-12-24-9.15.23-pm.jpg](https://gearspace.com/board/attachments/high-end/859480d1577240500-lexicon-reverbs-brief-bestiary-screen-shot-2019-12-24-9.15.23-pm.jpg)

---

### Post #387 -- Page 13
**User:** researchtriangle
**Info:** Joined: Mar 2015Posts: 275🎧 10 years | Posts: 275
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404566&postcount=387>

Quote: > Originally Posted byzmix➡️Yes, the 6 pages of parameters accessible only through that front panel is insane.I have created a plugin that allows me to access all 29 of the PCM-70 parameters within my DAW, and the parameters appear on my mackie C4 control surface's 32 encoders, as well as being fully automatable. It also allows complete recall for each project.Here is the one for the Concert Hall algo.Fantastic! So you've gone down a path similar to what I'm exploring now. All the fun little formulas to get the display values correct.

---

### Post #388 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404589&postcount=388>

Quote: > Originally Posted byresearchtriangle➡️Fantastic! So you've gone down a path similar to what I'm exploring now. All the fun little formulas to get the display values correct.Oh yes, hours of fun..  what's yours like? Is it an editor or a plugin controller?

---

### Post #389 -- Page 13
**User:** acidtechno
**Info:** Joined: Dec 2018Posts: 529My Studio🎧 5 years | Posts: 529My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404914&postcount=389>

Quote: > Originally Posted byzmix➡️Yes, the 6 pages of parameters accessible only through that front panel is insane.I have created a plugin that allows me to access all 29 of the PCM-70 parameters within my DAW, and the parameters appear on my mackie C4 control surface's 32 encoders, as well as being fully automatable. It also allows complete recall for each project.Here is the one for the Concert Hall algo.have you tried this with other models of the PCM lineage?

---

### Post #390 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14404994&postcount=390>

Quote: > Originally Posted byacidtechno➡️have you tried this with other models of the PCM lineage?No, I have not, because I don't own any of those, nor will I likely ever own them.. As I mentioned in my lengthier post above, I lost interest in Lexicon reverbs after the PCM-70.  I did buy a PCM-92 when it came out and felt like it was mislabeled ("How is *this* a Lexicon?"), even though it promised to have the original Concert Hall algo from the 224 it was not at all similar, I was so disappointed,(though I must say the "plate" algo in the PCM-92 is spectacular and reminds me of my Sony DRE and R7 reverbs). I sold the PCM-92 and bought an original 1979 era 224, and after having it for more than a decade I only sold it about a year ago, and then bought a PCM 70, and more recently bought another.  I made these software controllers for myself, so that I could have easy mix recalls and the ability to adjust every parameter via a knob on my control surfaces.


---

## Page 14

---

### Post #391 -- Page 14
**User:** researchtriangle
**Info:** Joined: Mar 2015Posts: 275🎧 10 years | Posts: 275
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405055&postcount=391>

Quote: > Originally Posted byzmix➡️Oh yes, hours of fun..  what's yours like? Is it an editor or a plugin controller?Mine is a web-based editor\librarian...I built almost like a web version of Sounddiver, but modernized. I'm steadily releasing modules for different pieces of hardware...PCM70 will likely be in there soon. Like you, I started building this for myself. [www.tonetweak.com](http://www.tonetweak.com) <= shameless plug

Quote: > Originally Posted byacidtechno➡️have you tried this with other models of the PCM lineage?I'm also working on modules for the PCM80 and PCM81.

---

### Post #392 -- Page 14
**User:** massimo
**Info:** Joined: Jan 2005Posts: 1,656🎧 20 years | Posts: 1,656
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405076&postcount=392>

Quote: > Originally Posted byzmix➡️I (...) bought an original 1979 era 224, and after having it for more than a decade I only sold it about a year ago, and then bought a PCM 70, and more recently bought another.Do you miss the 224? Or you consider the 70 an "improvement" over the 224 (non x/xl) so no looking back?


Happy Holidays

Massimo

---

### Post #393 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405090&postcount=393>

Quote: > Originally Posted byresearchtriangle➡️Mine is a web-based editor\librarian...I built almost like a web version of Sounddiver, but modernized. I'm steadily releasing modules for different pieces of hardware...PCM70 will likely be in there soon. Like you, I started building this for myself.www.tonetweak.com<= shameless plugInteresting approach..!  


As a mixing engineer, I am more concerned with "access" than with "presets", so what I've made is a tool for myself using the "[ctrlr.app](https://ctrlr.org/)" that works both as a standalone app as well as a plugin in my audio workstation, and in the plugin version it passes all the parameters and their names to the workstation so that they appear in the automation (and hence the control surfaces), my PCM-70s sit across the room in a rack and I have full access to every parameter.  


TBH I did not incorporate the equations needed to determine the correct display value of the pre-delay based on the size parameter (to others reading this, due to the finite amount of RAM in the PCM-70 the available pre-delay time varies with the scaling of the "size" parameter), based on the following  three reasons:


1: The range of the pre-delay sysex parameter values are the same regardless of the actual resultant pre-delay time, so essentially the control goes from "none" to "full" across it's range, so the calculations are not that important to the functionality, plus the actual value is displayed on the PCM-70.


2: I tend to make adjustments by ear (with my eyes closed, even).


3: It introduces a level of complexity that exceeded the utility for me, but if it were a commercial product, it might be important to others.

---

### Post #394 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405110&postcount=394>

Quote: > Originally Posted bymassimo➡️Do you miss the 224? Or you consider the 70 an "improvement" over the 224 (non x/xl) so no looking back?Happy HolidaysMassimoThe original 224 is a very special box, it has a beautiful expanse to it and can produce a broad range of textures from hyper aggressive to sublime and moody, it really set the standard..  The PCM-70 to me sounds like the 224xl, it's sweeter, most certainly more "refined", I used to use them a lot back in the 80s and 90s and my first impression upon revisiting it after the 224 was that is was a considerable step up from the 224, with a more 'realistic' engagement as a listener, it's certainly more subtle, and also possibly more aggressive than the 224. They are just different.  I spent 2 years helping UA to get their 224 emulation correct and I think it's 90% there, and I use it as I did the hardware.

The PCM-70 is much more tweakable (as is the 224xl) and with my controller do a lot more sculpting of the discrete delays and diffusion / attack (which is most similar to the "depth" parameter of the 224) / definition than I ever did from the front panel.


The stereo inputs on the various 224s are really interesting as the reverb is essentially a large loop with inputs 180˚ on either side and the outputs 90˚ rotated from them, so as a sound enters the left input it comes out the left after a certain period of time, and then much later comes out the right channel, so you hear a characteristic "panning" effect as the sound blooms across the sound stage, as it would if the source in a hall was off to one side.

No impulse based reverb can do that, period.   And this is one aspect I do miss on the PCM-70.

---

### Post #395 -- Page 14
**User:** massimo
**Info:** Joined: Jan 2005Posts: 1,656🎧 20 years | Posts: 1,656
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405142&postcount=395>

zmix,


thanks so much for your informative reply. I am a fan of those old Lexicons, and have both the 70 and 200 (love the interface and sound), and like them very much. The 224 typically costs twice the price of a 200, and I was wondering if it was just a matter of collectors price now or if it made any actual sense sonically, already having the others...

---

### Post #396 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405154&postcount=396>

Quote: > Originally Posted bymassimo➡️zmix,thanks so much for your informative reply. I am a fan of those old Lexicons, and have both the 70 and 200 (love the interface and sound), and like them very much. The 224 typically costs twice the price of a 200, and I was wondering if it was just a matter of collectors price now or if it made any actual sense sonically, already having the others...I love the sound of the 200, but it has a very stripped down set of controls compared to the 224, however, if you don't tend to dive deeply into the reverbs you use, it's got all the important functions, and between it and the PCM-70 you're pretty well covered.

---

### Post #397 -- Page 14
**User:** researchtriangle
**Info:** Joined: Mar 2015Posts: 275🎧 10 years | Posts: 275
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405205&postcount=397>

Quote: > Originally Posted byzmix➡️As a mixing engineer, I am more concerned with "access" than with "presets", so what I've made is a tool for myself using the "ctrlr.app" that works both as a standalone app as well as a plugin in my audio workstation, and in the plugin version it passes all the parameters and their names to the workstation so that they appear in the automation (and hence the control surfaces), my PCM-70s sit across the room in a rack and I have full access to every parameter.That sounds blissful. I will eventually support control surfaces, but admittedly as I'm not working with VST, I miss out on that sort of DAW integration.  

Quote: > Originally Posted byzmix➡️TBH I did not incorporate the equations needed to determine the correct display value of the pre-delay based on the size parameter (to others reading this, due to the finite amount of RAM in the PCM-70 the available pre-delay time varies with the scaling of the "size" parameter), based on the following  three reasons:1: The range of the pre-delay sysex parameter values are the same regardless of the actual resultant pre-delay time, so essentially the control goes from "none" to "full" across it's range, so the calculations are not that important to the functionality, plus the actual value is displayed on the PCM-70.2: I tend to make adjustments by ear (with my eyes closed, even).3: It introduces a level of complexity that exceeded the utility for me, but if it were a commercial product, it might be important to others.All very good points, and completely valid. As I'll be offering this as a paid module, I'm obliged to implement these little functions to produce labeling accuracy...plus trying to parse out the ambiguous nature of Lexicon's documentation for the PCM70 is fun in a weird way.


Cool to see that others are making control editors for this unit, though! Cheers.

---

### Post #398 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=14405226&postcount=398>

Quote: > Originally Posted byresearchtriangle➡️That sounds blissful. I will eventually support control surfaces, but admittedly as I'm not working with VST, I miss out on that sort of DAW integration.All very good points, and completely valid. As I'll be offering this as a paid module, I'm obliged to implement these little functions to produce labeling accuracy...plus trying to parse out the ambiguous nature of Lexicon's documentation for the PCM70 is fun in a weird way.Cool to see that others are making control editors for this unit, though! Cheers.Yes there are a few errors in the SYSEX implementation in the manual..!

---

### Post #399 -- Page 14
**User:** glenesis
**Info:** Joined: Oct 2007Posts: 72My Recordings/CreditsMy Studio🎧 15 years | Posts: 72My Recordings/CreditsMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15622687&postcount=399>

Quote: > Originally Posted byresearchtriangle➡️Mine is a web-based editor\librarian...I built almost like a web version of Sounddiver, but modernized. I'm steadily releasing modules for different pieces of hardware...PCM70 will likely be in there soon. Like you, I started building this for myself.www.tonetweak.com<= shameless plugI'm also working on modules for the PCM80 and PCM81.Thank you for your shameless plug! I need this web app! Have a fantastic, amazing weekend

---

### Post #400 -- Page 14
**User:** Seeker of Rock
**Info:** Joined: Dec 2008Posts: 240🎧 15 years | Posts: 240
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16167045&postcount=400>

Epic thread. I came across this YouTube vid comparison from ‘17. Guy doesn’t say if these are plugs but see some of the hardware boxes on his desk and he has some high quality amps in the room. 


Don’t know how he’s running each through the clips either but I have some subjective opinions, one being the PCM70 settings should be tweaked on the outputs in the registers. I have one and it can sound way thicker than his stock presets with the same organic beauty.

 The second, some surprising sounds out of a few pedals. 

The third is (subjectively) the 480 is the undisputed king of huge,  sound that melts away on decays (at least on the only 480 clip he posted, Hall). In the 96 and Bricasti I heard too many artifacts of delay in the decay, the structured cycling tails (my words and how I describe what I hear). Still they both sounded nice. I really (surprisingly) loved the Kemper. Also liked the Roland in one of the settings but forget which. PCM70 tiled room ruled the roost in the plate category but it’s not a setting I use much. Pure awesomeness though.  At least in this vid I can appreciate the love for the 480. It was a ‘wow!’ moment for me hearing that powerful and robust sound next to the others he demo’d. Just one guitar, but ability to handle an entire multi-track main reverb, I can see what all of the 480 buzz is about.

[https://m.youtube.com/watch?v=xkDIhTtyoes](https://m.youtube.com/watch?v=xkDIhTtyoes)

---

### Post #401 -- Page 14
**User:** Deleted 372319bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16167150&postcount=401>

In a completely related yet unrelated comment - I was surprised to find a Creative Labs Sound Blaster PCI card inside the Lexicon 960L!

---

### Post #402 -- Page 14
**User:** Seeker of Rock
**Info:** Joined: Dec 2008Posts: 240🎧 15 years | Posts: 240
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16217434&postcount=402>

Quote: > Originally Posted byDeleted 372319b➡️In a completely related yet unrelated comment - I was surprised to find a Creative Labs Sound Blaster PCI card inside the Lexicon 960L!I wonder if they put one of those in the old 480 and that’s why it sounds so good?

---

### Post #403 -- Page 14
**User:** paulg
**Info:** Joined: Jul 2007Posts: 52🎧 15 years | Posts: 52
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17182672&postcount=403>

Quote: > Originally Posted byzmix➡️No, I have not, because I don't own any of those, nor will I likely ever own them.. As I mentioned in my lengthier post above, I lost interest in Lexicon reverbs after the PCM-70.  I did buy a PCM-92 when it came out and felt like it was mislabeled ("How is *this* a Lexicon?"), even though it promised to have the original Concert Hall algo from the 224 it was not at all similar, I was so disappointed,(though I must say the "plate" algo in the PCM-92 is spectacular and reminds me of my Sony DRE and R7 reverbs). I sold the PCM-92 and bought an original 1979 era 224, and after having it for more than a decade I only sold it about a year ago, and then bought a PCM 70, and more recently bought another.  I made these software controllers for myself, so that I could have easy mix recalls and the ability to adjust every parameter via a knob on my control surfaces.I love the newer lexicon sounds.... 960 is what first gave me the goose bumps in the studio.  

Love the PCM 92 and native plugs.


Just stating this in case someone from ac different musical generation may think they HAVE to go 224 or 480 to be 'valid'.


Just like some prefer 60's 70's or 80's music or later... all great.... all musical....all wonderful


Just different

---

### Post #404 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17182683&postcount=404>

Quote: > Originally Posted bypaulg➡️I love the newer lexicon sounds.... 960 is what first gave me the goose bumps in the studio.Love the PCM 92 and native plugsJust stating this in case someone from ac different musical generation may think they HAVE to go 224 or 480 to be 'valid'.Just like some prefer 60's 70's or 80's music or later... all great.... all musical....all wonderfulJust differentThat's a very odd response.  If you like something and it inspires you, then it's "valid".


I'm not 'virtue signaling' here, I'm stating my preference for the original 224 and PCM-70 for a specific reason:  All Lexicon reverbs after those changed the approach to modulation within the reverb.  The newer designs eliminate any pitch modulation (because they then considered it 'unnatural') and instead use a sort of paged memory modulation that changes the lengths without affecting the signal in memory.


To me this change makes the reverbs sound stiff, harsh and metallic.  I prefer the mysterious, even 'spooky' sound of the original pseudo-random pitch modulation of the 224 and PCM-70.

---

### Post #405 -- Page 14
**User:** ddy
**Info:** Joined: Feb 2024Posts: 5,848 | Posts: 5,848
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17182977&postcount=405>

Quote: > Originally Posted byzmix➡️That's a very odd response.not at all: that's a matter of taste - i also prefer the later models!

---

### Post #406 -- Page 14
**User:** spockstudio
**Info:** Joined: Sep 2007Posts: 217My Studio🎧 15 years | Posts: 217My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17202713&postcount=406>

Quote: > Originally Posted byzmix➡️That's a very odd response.  If you like something and it inspires you, then it's "valid".I'm not 'virtue signaling' here, I'm stating my preference for the original 224 and PCM-70 for a specific reason:  All Lexicon reverbs after those changed the approach to modulation within the reverb.  The newer designs eliminate any pitch modulation (because they then considered it 'unnatural') and instead use a sort of paged memory modulation that changes the lengths without affecting the signal in memory.To me this change makes the reverbs sound stiff, harsh and metallic.  I prefer the mysterious, even 'spooky' sound of the original pseudo-random pitch modulation of the 224 and PCM-70.Mysterious is a great way to describe it. To me, the 224X is the crowned jewel.

---

### Post #407 -- Page 14
**User:** monophreak
**Info:** Joined: Dec 2023Posts: 127 | Posts: 127
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17565347&postcount=407>

I really enjoyed this thread. I've posted this a few times before on Gearspace so I'll be brief.


LXP-5 editor: [https://youtu.be/F-lcXAhI72E](https://youtu.be/F-lcXAhI72E)

LXP1, 15 and Reflex being built.

Considering to build a PCM81/91.


Using midi fx plugins, you can extend the original hardware (e.g. add a LFO where you want in the chain) via things like Logic Pro's modulation plugin and add in automation and preset recall.


