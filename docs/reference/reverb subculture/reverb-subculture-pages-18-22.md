
---

## Page 18

---

### Post #511 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204392&postcount=511>

Quote: > Originally Posted byFroombosch➡️Thank you and Casey for your responces . Food for thought.I should also add that plenty of "classic" reverb algorithms used linear interpolation for modulated delays.

---

### Post #512 -- Page 18
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204427&postcount=512>

Quote: > Originally Posted byseancostello➡️No problem - just make sure that you adjust your delay lengths to take into account the block delay in the feedback path. For example, if you want a 1000 sample comb filter, and your block size is 32 samples, you would use a delay of (1000-32)=968 samples.How you handle internal block delays is your own problem.hehhehheh


It is the alignment issue that must be attended to. Delays cannot be multiples of some block size.


So, and Dale alludes to this, some head and tail processing must take place to allow delays to be of arbitrary length.


Really, this is just for the record, I know you understand this!



-Casey

---

### Post #513 -- Page 18
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204447&postcount=513>

Quote: > Originally Posted byseancostello➡️I should also add that plenty of "classic" reverb algorithms used linear interpolation for modulated delays.Yeah i found that out also. ...


Harrie

---

### Post #514 -- Page 18
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5205622&postcount=514>

Quote: > Originally Posted byCasey➡️I would have to look back, but I seem to recall that Rob King donated that sample.Really? Well, you would be the one to ask- when these come out, may I put up mp3 clips using those dry samples (in other words, what's on this thread?) on Gearslutz? I think it would help people if they could hear a clip right in their browser, and I don't do that as often as I should. I'll give credit for the help this thread has been

---

### Post #515 -- Page 18
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5205977&postcount=515>

Quote: > Originally Posted byCasey➡️How you handle internal block delays is your own problem.hehhehhehIt is the alignment issue that must be attended to. Delays cannot be multiples of some block size.So, and Dale alludes to this, some head and tail processing must take place to allow delays to be of arbitrary length.Really, this is just for the record, I know you understand this!Processing by-block is probably fine, but actually, by-sample probably isn't that much more once the samples are moved into internal RAM - it should hopefully be whatever the programmer wanted to do, not necessarily a limitation of the hardware. Even processing by blocks can be tricky with SDRAM as the SDRAM page length probably doesn't line up with the desired delay line lengths.


What I would be tempted to do is make an internal RAM delay line equal to the desired delay line length (and making the basic delay line non-tappable except at the output end), then you subtract out however many 'blocks' you need out of the middle, leaving maybe 100 or 200 samples in the internal SRAM. Then you can DMA into and out of the middle of the array, although care must be taken about delay line wraparound, since the DMA controller must be programmed to reload its address register once it gets to the end. The modulus DSP addressing mode takes care of the code of an arbitrary length circular buffer, but the DMA controller may not be that sophisticated. If the delay is less than, say, 300 samples or so, then don't bother moving the data around - just leave it in SRAM. There would be a bit of work in the memory management control software, but it only needs to run to completion at least every 'N' samples where 'N' is the transfer block size (which may or may not be equal to the algorithm block size). But in this way, a delay line can be interpolated at the end (in SRAM), and it can be an arbitrary length. The algorithm that takes the reverb descriptor tables and allocates memory based on programmed reverb size would need to manage setting all of this up. You also could program sample-by-sample if you wanted to, or in blocks. In this way, the SRAM delay line acts as the arbitrary length adjustment, and also as a (manually maintained) data cache.


I know there are more ways to do this than this, but it should work ok. Another option is to have two circular buffers. The write buffer is, say, double the transfer block size. Once the write pointer gets halfway, write the first half. Once it wraps around, write the other half. The read buffer would be similar - the same length. The phase offset between the read and write pointers, plus the length of the bulk SDRAM delay would determine the delay line length. I can only think of maybe five ways of managing the SDRAM to SRAM data shuffle, and a couple of ways of doing the calculations in-place.


There are three main time delays in SDRAM that are important from what I can tell out of the datasheets. The first delay and the last delay are obvious - the open page and close page operations. The other delay is address supply to data available, and that applies to in-page accesses. And to make matters worse, if your block size aligns to a page length in SDRAM (which it should), that would be fine, but also for efficient access to SDRAM by the software, you either will have to misalign the writes (open and close two pages for one operation) or misalign the reads, unless the delay size is also a multiple of the block size (which also aligns with SDRAM page size). SDRAM also does not necessarily do well when you try to interleave writes and reads to the same bank, though that depends on the SDRAM controller built into the DSP.


This is interesting, I think one thing that's missing from people developing software these days is how the software actually has to mess with chips.

---

### Post #516 -- Page 18
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5206078&postcount=516>

Quote: > Originally Posted bydale116dot7➡️for efficient access to SDRAM by the software, you either will have to misalign the writes (open and close two pages for one operation) or misalign the reads.And what about those pesky allpass filters that like to read AND write at both ends.heh



-Casey

---

### Post #517 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5206266&postcount=517>

Could an FPGA be used to aid with getting data out of the SDRAM and into the DSP / local SRAM system? Maybe with modulo math? 


Of course, if you have an FPGA doing the delay line management with the cheaper chips, it would be tempting to create a full reverb solution based around said FPGA.


This conversation is reminding me of having to deal with the 2126x SHARCs during the ADI days, before the 21369 came out. The 2126x chips had the memory access pins removed, due to some large customer requesting this. So all external memory access had to go through DMA, which was horribly slow. The block based processing helped a little, but not much. The Blackfin DSPs were coming out at that time, and were viewed as underachievers for audio by most of the higher ups at ADI. In our little group, we were able to get much higher performance out of the Blackfins than the 2126x for delay based algorithms. The 2136x series restored the memory access pins, thus saving face for the SHARC line.

---

### Post #518 -- Page 18
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5208401&postcount=518>

Quote: > Originally Posted byCasey➡️And what about those pesky allpass filters that like to read AND write at both ends.hehIf your allpass is in-line (ie. one big memory loop and not several segments that are kept separate), then you should not need to read and write both ends simultaneously. If you consider the input to an allpass as coming from somewhere else (say, the end of another delay line that is totally separate), and consider the output as going to somewhere else (the start of another delay line that is totally separate), then you need to read feedback from the end of the allpass, write to the start of the allpass, and write the output to the head of its own delay line. You will waste some SDRAM this way, but SDRAM's pretty cheap and there's lots of it. Provided that there is at least one transfer block size of empty space in the SDRAM between delays, then there should not be an issue. Or am I missing something?

---

### Post #519 -- Page 18
**User:** cleartrueblue
**Info:** Joined: Mar 2006Posts: 65🎧 20 years | Posts: 65
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5227992&postcount=519>

Quote: > Originally Posted byCasey➡️I would have to look back, but I seem to recall that Rob King donated that sample.-CaseyCould be wrong but I think that orchestral example is of a VSL mock-up by Berlin composer Andreas Koslik - posted on a German site when the M7 first came out.   Actually, those files posted then are what sealed my purchase!

---

### Post #520 -- Page 18
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5228330&postcount=520>

What about the guitar clip? That's awfully well suited to a smaller room ambience.

---

### Post #521 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5350427&postcount=521>

Just found this:

[https://ccrma.stanford.edu/~dattorro/Griesinger.jpg](https://ccrma.stanford.edu/~dattorro/Griesinger.jpg)


For those of us that were always fascinated by the Dattorro papers - and the story behind them - this letter sheds some light on the subject.


Interesting to read what Griesinger says about the Gardner reverbs as well.

---

### Post #522 -- Page 18
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5396081&postcount=522>

Very interesting. Thanks for the paper

---

### Post #523 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5397042&postcount=523>

Something I just noticed in Griesinger's letter:


"I know it is possible to decode algorithms, and have done it myself."


I wonder if this might be a reference to the Constant Density Plates in the 224 and 224X/L, with regards to the EMT250. Otherwise, I wouldn't know what Griesinger would have wanted to reverse engineer during his tenure at Lexicon.


Or maybe Griesinger is talking about decoding the older Lexicon algorithms, after the development machines were, um, lost.

---

### Post #524 -- Page 18
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5398488&postcount=524>

Reverse engineering is a way to get some information on the famous old algos. Doing without is like reinventing and that is not the easy route. The shared information like in this thread is but also in the datorro papers are very valuable, because they give real insight.  


I did start effectprocessor.com in 2004 to share some of the information I gathered.

---

### Post #525 -- Page 18
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5426420&postcount=525>

I'm really happy to see an open discussion of this.   I've read through the thread (and related threads) several times and carefully taken notes, and I'm trying to digest all the papers and patents I can find on the subject.  I was going to just work on it by myself, but it seems more in the spirit of things to share my observations and questions.


I'm building reverberators and other effects in Pure Data.  After a few initial experiments, a couple "cloned" algorithms, and some increasingly stupid ideas, I think I can safely clear all effect processors, hardware and software, from my wanted list.  That probably sounds excessive, but my tastes tend toward the exotic, so I don't mind making things that turn single piano notes into underwater reverse bowed Balinese gong tone clusters.  Making something that resembles an actual acoustic space seems quite difficult, but "outlandish" can be a lot more forgiving.  I've only been messing with these for a few weeks but I'm really surprised at how quickly I'm able to make and refine them.  As I become accustomed to the freedom I'm allowed here, I suspect even the most powerful Eventide/TC boxes would feel limiting.


Some ideas and things that I've tried:


1. Frequency shifters in feedback loops.  I suspect Isao Tomita may have done this with a Bode frequency shifter and AKG BX20, results are interesting but it's perhaps too tempting to take it to total excess.


2. Dispersion filters- I saw that Sean participated in a paper modeling spring reverb (I don't have the full paper), and I saw a patent (4955057) suggesting 20-ish allpass analog phase shifter stages in a reverb feedback loop, which I tried.  It's interesting in comparison to normal APFs, since an impulse is spread into a chirp, but it's sort of computationally intensive.  Gary Kendall wrote a paper (The Decorrelation of Audio Signals and Its Impact on Spacial Imagery, 1995) 

suggesting time variant decorrelating filters made from long chains of allpass biquads- maybe this is another option?  I imagine sticking these inside normal APFs could be useful, computing power permitting.  Anyone tried it?


3. That random delay Yamaha patent that Sean mentioned (553150)- I didn't expect a lot but I tried it with 16 delays and got interesting results.  A single "comb" made this way can't handle much feedback due to the amplitude modulation of the crossfade, but modulated APFs and additional feedback paths (sort of a naive FDN) can actually make things quite smooth.  Without feedback it can be used as a weirdly modulating "early reflection" FIR.  It's really interesting and I'll have to play with it a lot more.


4. Long APF chain with random taps: I chained 16 APFs per channel and randomly crossfade between taps at each stage for output, feedback, etc.  This can be used in a relatively sane way, or to make reverbs with a sort of dynamic "envelope", building slowly or quickly or panning from right to left or whatever.  It's pretty cool so far, but I need to extend it.


Some questions and things:


1.  I've had trouble finding some papers.  I have a healthy pile of user manuals, service manuals, patents, papers that the authors have made available on their websites, DAFX ones, etc. but I'm missing some Computer Music Journal/JAES/etc. ones that are probably fairly important- in particular Schroeder, Blesser, Jot, Gerzon, and the Agnello one describing the Eventide SP2016.  Anyone got these handy?  


2.  I've gotten the impression that it's best to modulate "in the loop" APF delay times (one paper suggested modulating feedback coefficients, though Sean described poor results), but are there limits to this?  Is it a logical conclusion, given adequate processing power, to just "modulate everything"?  Does it make more sense to use one n-phase sinusoidal or triangular modulator for everything, or to break it down into separate 2/3/4 phase modulators running at different rates?  Or independent randomized (piecewise linear or whatever) modulators?  Is it preferred to apply complementary modulation to consecutive APFs?  There are a huge number of options, and I'm not sure I'm perceptive enough to find the "best".


3. I'm not a huge fan of FIR "early reflections", but they do come in handy sometimes.  I've found they're quite hard to make from scratch and generating them randomly just results in 10000 flavors of crap.  I've gotten a few from papers and such, but is there any sort of repository or some that people wouldn't mind sharing?


3.14159... Speaking of which, Moorer notes that an APF with a non-allpass filter in the loop can be made allpass if preceded by its time reverse.  It seems like a multitap FIR type thing used this way could take care of early reflections and diffusion all at once- anyone tried it?


4. Regarding multi-band reverbs, is there much advantage here besides independent control over reverb times?  I know Yamaha did this a lot, but did anyone else?  Do different delay times for different bands result in a smoother sound?


Christ, I've nearly written a doctoral thesis myself...

---

### Post #526 -- Page 18
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5426607&postcount=526>

Hello Acreil,


Thats a lenghty post. There are a few papers and patents in the effectprocessor forum and some older discussions on building algos. Feel free to add more if you have found some. 


My work is in the constant density reverb type, so most of your questions are for other people around here. I am not a big fan of allpass filters.  I am working now with inversed feedback combfilters. The darkening sound of these filters sound more natural to me.

---

### Post #527 -- Page 18
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5445868&postcount=527>

I'll probably be doing a constant density thing sometime soon, some sort of extended Moorer/Ursa Major 8x32 type algorithm with some EMT-inspired enhancements (and whatever else I can think of).  Even with all the design metrics that have come up over the years, they still seem more difficult to tune than the "big loop with a bunch of APFs" topologies.


The best hardware reverb I have at the moment is an Ibanez SDR-1000, which was very well received in this thread (anyone got the "+" OS ROMs?).  While there's no modulation, it's a quite nice sounding constant density reverb, so I'm not really worried about making some sort of gold standard.


Part of what got me curious about reverb is pondering what makes vintage boxes so desirable, and if there was some cheap and overlooked shortcut to the "vintage sound"- turns out the SDR-1000 was a pretty good choice.  I'm still perpetually intrigued by some other "underdog" boxes, the Dynacord DRP-20, Korg DRV-3000, etc.  but if my synth buying habits have taught me anything, it's that obscure and overlooked items, while sometimes very interesting, aren't always the most useful.

---

### Post #528 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5445895&postcount=528>

Quote: > Originally Posted byacreil➡️I'll probably be doing a constant density thing sometime soon, some sort of extended Moorer/Ursa Major 8x32 type algorithm with some EMT-inspired enhancements (and whatever else I can think of).  Even with all the design metrics that have come up over the years, they still seem more difficult to tune than the "big loop with a bunch of APFs" topologies.I think that this is the trickiest part of reverb design: tuning the delays, and knowing how to tune them for a given topology. The allpass loops are fairly forgiving; feedback delay networks / parallel combs less so; FDNs / parallel combs with lots of output taps even less so. Once you start embedding allpasses within FDNs, it gets ridiculous. I spent the first half of the 2000's learning how to create stable structures, and the second half learning how to make those sound good. 


As far as papers, if you have a local university, try going there and see if they have subscriptions to the journals in question. I head over to the University of Washington all the time, and email papers to myself.

---

### Post #529 -- Page 18
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5467984&postcount=529>

Quote: > Originally Posted byseancostello➡️I think that this is the trickiest part of reverb design: tuning the delays, and knowing how to tune them for a given topology.That certainly seems to be the consensus.  Some of the (obviously more encouraging) topologies I've tried sound almost acceptable just on the first "mash the number pad" test.  It seems related to the total delay time in the loop(s), ignoring the APFs, which I guess isn't surprising.  I saw your posts with Keith Barr on the Spin Semiconductor forum, and I think his "one big loop" topology really has a lot of advantages that way.  When I built it I didn't have any context and didn't expect much (it's a tutorial, after all), but it was immediately surprising.  Multiple parallel loops seem to "fight against each other" a lot more.  Tuning a single loop algorithm feels more like "enhancing and improving" rather than "making it less obviously bad".


I wonder if the constant density parallel comb filter case can be improved by using fewer combs and adding more output taps per delay... I suspect it's really only trading one problem for another...

---

### Post #530 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5509480&postcount=530>

Quote: > Originally Posted byacreil➡️Multiple parallel loops seem to "fight against each other" a lot more.  Tuning a single loop algorithm feels more like "enhancing and improving" rather than "making it less obviously bad".The thing that is nice about a single loop is that the output taps will always have the same relationship to each other. Make those sound nice, and you're in business. The allpasses within the loop can be viewed as adding phase randomization to the loop, although they can also cause artifacts if not tuned properly.

Quote: > I wonder if the constant density parallel comb filter case can be improved by using fewer combs and adding more output taps per delay... I suspect it's really only trading one problem for another...I look at each comb as a wheel, and the taps as spokes. You have wheels rotating at different rates, and they are on top of each other. Each time the spokes of one or more wheels are at the same place, an unpleasant resonance is formed. So...is it easier to reduce the overlap with a bunch of wheels with less spokes, or less wheels and more spokes?

---

### Post #531 -- Page 18
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5510078&postcount=531>

acreil, I think the Ibanez became the Sony DPS box, there's a Roger Nichols article that refers to that. Still a very nice sound.

---

### Post #532 -- Page 18
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5516108&postcount=532>

Quote: > Originally Posted byseancostello➡️I look at each comb as a wheel, and the taps as spokes. You have wheels rotating at different rates, and they are on top of each other. Each time the spokes of one or more wheels are at the same place, an unpleasant resonance is formed. So...is it easier to reduce the overlap with a bunch of wheels with less spokes, or less wheels and more spokes?One wheel would get a more evently distributed spoke density, but would repeat itself. Repeating can be seen/heared. It is not easy to build a good distribution with two, three or more wheels, but why take the easy route??

---

### Post #533 -- Page 18
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5516215&postcount=533>

Quote: > Originally Posted byFroombosch➡️One wheel would get a more evently distributed spoke density, but would repeat itself. Repeating can be seen/heared. It is not easy to build a good distribution with two, three or more wheels, but why take the easy route??Repetition can be heard with 2, 3, or 20 "wheels" (tapped combs) as well. For time-invariant reverbs, the best you can do is to have a repetition rate that is the sum of all of the delay lengths. 16 parallel combs with a total delay of 500 msec and a single delay line with lots of taps and embedded allpasses with a total length of 500 msec will both have a repetition artifact of 500 msec.

---

### Post #534 -- Page 18
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5516677&postcount=534>

Quote: > Originally Posted byseancostello➡️The thing that is nice about a single loop is that the output taps will always have the same relationship to each other. Make those sound nice, and you're in business. The allpasses within the loop can be viewed as adding phase randomization to the loop, although they can also cause artifacts if not tuned properly.I look at each comb as a wheel, and the taps as spokes. You have wheels rotating at different rates, and they are on top of each other. Each time the spokes of one or more wheels are at the same place, an unpleasant resonance is formed. So...is it easier to reduce the overlap with a bunch of wheels with less spokes, or less wheels and more spokes?The thing I'm sorta wondering is whether it would be worthwhile to make a "multitap delay with single feedback path" where the multitap part is fairly dense.  Of course this will be annoyingly periodic, but maybe if several of these were used in parallel it would reduce the easily perceived periodicity without (er, hopefully) making it much harder to tune.  Maybe a single very dense FIR could be "decomposed" by alternately assigning taps to different loops, such that the initial output (before the input signal reaches the feedback taps) would be identical to the original impulse response.  Then, uh, put a modulated APF on the feedback tap and hope for the best.


What got me thinking along these lines is that the "single loop" topology basically reduces to a multitap with feedback if all the APF coefficients are zero.  This initially didn't strike me as a great idea, but the results are good.

---

### Post #535 -- Page 18
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5516808&postcount=535>

This is an example of my random delay based reverb.  


There are 8 delays per channel, each with crossfading random delay taps (separate "audition" and "feedback" taps), followed by 2 APFs with both piecewise continuous random and sinusoidal modulation.  There are 3 feedback paths- a delay can feed back into its own input, into the next delay's input, or groups of 4 delays can be mixed and fed into the 4 delays on the other channel.


Don't take the "granular" name too seriously, I don't think it really has anything to do with granular synthesis as described by Barry Truax, it just needed a name.


Obviously this is an extreme example with less than compelling source material (crappy Yamaha TG77 marimba sample), but I was rather surprised that the tail does smooth out without turning into a mess.  Somehow a bunch of apparent no-nos combined to form something useful (to me, at least).  It can be toned down but probably not to the extent that I'd consider it a general purpose style effect.

---

### Post #536 -- Page 18
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5540830&postcount=536>

Quote: > Originally Posted byacreil➡️...The best hardware reverb I have at the moment is an Ibanez SDR-1000, which was very well received in this thread (anyone got the "+" OS ROMs?).  While there's no modulation, it's a quite nice sounding constant density reverb, so I'm not really worried about making some sort of gold standard.Part of what got me curious about reverb is pondering what makes vintage boxes so desirable, and if there was some cheap and overlooked shortcut to the "vintage sound"- turns out the SDR-1000 was a pretty good choice.  I'm still perpetually intrigued by some other "underdog" boxes, the Dynacord DRP-20, Korg DRV-3000, etc.  but if my synth buying habits have taught me anything, it's that obscure and overlooked items, while sometimes very interesting, aren't always the most useful.Don't be fooled.  The Ibanez SDR-1000 was designed by Sony.  They put thousands of man-hours into researching reverb, and their 'first' attempt, the 1979-80 era DRE-2000 is a work of art. The SDR-1000 was comissioned by Ibanez, and represents the next step: it utilized a dedicated VLSI reverb processor (Sony called it the "Presence Chip").  After a falling out with Ibanez, Sony released their own version of the SDR-1000 and called it the MUR-201.  Both the SDR-1000 and the MUR-201 are "True Stereo" devices, too.

---

### Post #537 -- Page 18
**User:** volumetric
**Info:** Joined: Jul 2010Posts: 4🎧 15 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5617828&postcount=537>

Hello Everyone. Something you may want to look at -

[Dattorro - Wikimization](http://www.convexoptimization.com/wikimization/index.php/Dattorro)
[Talk:Dattorro - Wikimization](http://www.convexoptimization.com/wikimization/index.php/Talk:Dattorro)


hmmmmmmm....

---

### Post #538 -- Page 18
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5618616&postcount=538>

[Flux:: sound and picture development](http://www.fluxhome.com/products/Plug_ins/ircam_spat)

Quote: > Flux:: sound and picture developmentIRCAM SPAT - The complete Room Acoustics Simulation and Localisation SolutionWith more than a decade of research performed by the Acoustic and Cognitive Spaces Team at IRCAM, being at the forefront of scientific and technological innovations, the SPAT is the most advanced and sophisticated tool for room acoustics simulation and localisation ever designed, managing both spatialisation (source localisation) and room acoustic simulation in a truly consistent and visually logical way.Designed for surround and multi-channel use, SPAT presents the option to setup the output arrangements providing a variety of stereo and surround configurations, including subwoofer configuration. With eight input and output channels available in SPAT, configurations up to 7.1 and 8.0 are feasible.Each of the up to eight incoming audio channels is internally mapped to a range of Virtual Sources localized in a 3D space, and connected to a room (a reverb). Up to 3 rooms in parallel are provided, presenting the option to simulate complex spaces (coupled room acoustics).SPAT introduce state of the art techniques for room acoustics simulation utilizing advanced perceptive models, concealing the complexity behind the actual algorithms, allowing for intuitive and accommodating user interaction capabilities.The SPAT licence includes the IRCAM Verb as well.

---

### Post #539 -- Page 18
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5618738&postcount=539>

Quote: > Originally Posted byacreil➡️Part of what got me curious about reverb is pondering what makes vintage boxes so desirable, and if there was some cheap and overlooked shortcut to the "vintage sound"I don't think there are any real shortcuts to reverb. Most everything is based on fairly simple topological reasoning and the associated math. Tweaking is really just a way of learning this, as it appears you are finding out!


If you think of convolution as a shortcut; Even there, Sony still has the best example of that technology.



-Casey

---

### Post #540 -- Page 18
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5622839&postcount=540>

Mostly I had naively wondered if the vintage "discrete DSP" architecture had some speed advantage over a general purpose DSP.  I was thinking of how, for example, the hardware implementation of FM in the Yamaha DX7 (and to a lesser extent, the Synergy) is far more efficient than software running on a DSP.  But of course this is based on clever use of shift registers and avoiding multiplication, and doesn't really apply to reverb.


I think a better explanation is that the difficulty of the problem in the early years attracted a more dedicated class of designer that was willing to spend a great deal of time experimenting and refining the algorithms.  They worked well ahead of any published research, without necessarily having a great deal of prior knowledge of artificial reverberation, or even much of a preconceived notion of what digital reverb is supposed to sound like.  


That's extremely impressive, and more than a little humbling when I can get something basic happening in about an hour, but then I'm too lazy to tune it much better than "not completely awful".  


Also, on a somewhat related note, are the Ursa Major products the only ones that used significant analog processing inside the actual reverb engine?


---

## Page 19

---

### Post #541 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5622853&postcount=541>

Quote: > Originally Posted byvolumetric➡️Hello Everyone. Something you may want to look at -Dattorro - WikimizationTalk:Dattorro - Wikimizationhmmmmmmm....If that's what I think it is, it's pretty crazy.  I don't think nested APFs were discussed in any detail beyond "not particularly useful" until what, 1992?


I wonder what the reason is for the separate 1 pole LPFs and shelving filters.  Obviously there's potential for finer control, but everything else I've seen treats it as simply as possible, just "put a filter in the loop".

---

### Post #542 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5623785&postcount=542>

Quote: > Originally Posted byacreil➡️If that's what I think it is, it's pretty crazy.  I don't think nested APFs were discussed in any detail beyond "not particularly useful" until what, 1992?The first nested allpass filter in the literature is from Schroeder's 1962 AES paper. He describes the structure as a way of having an allpass control over mixing the dry signal with the wet signal, but without recognizing that it would also increase the echo density over time.


Michael Gerzon proposed nested allpasses as a way of increasing echo density in his 1972 Studio Sound paper, as well as his 1976 EDN article. The Gerzon allpasses were originally described as being N-channel (i.e. N delays in parallel, mixed together by a unitary matrix, with allpass feedforward/feedback around the whole structure) but 1 channel still counts as N channels.


Bill Gardner, in his 1992 MS thesis, cites a 1984 paper by Barry Vercoe and Miller Puckette that lays out the theory for nested allpasses in reverbs. I have never been able to find a copy of that paper. The 1992 Gardner MS thesis has a LOT of similarities with the reverb on the Dattorro site.

Quote: > I wonder what the reason is for the separate 1 pole LPFs and shelving filters.  Obviously there's potential for finer control, but everything else I've seen treats it as simply as possible, just "put a filter in the loop".These allow for adjusting the reverb time and damping in different frequency ranges.

---

### Post #543 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5624363&postcount=543>

Quote: > Originally Posted byacreil➡️Mostly I had naively wondered if the vintage "discrete DSP" architecture had some speed advantage over a general purpose DSP.  I was thinking of how, for example, the hardware implementation of FM in the Yamaha DX7 (and to a lesser extent, the Synergy) is far more efficient than software running on a DSP.  But of course this is based on clever use of shift registers and avoiding multiplication, and doesn't really apply to reverb.In the early days of reverb, custom hardware had a huge speed advantage compared to general purpose processors and DSPs. For starters, there weren't any single chip DSPs in the late 1970's. At some point, single-chip multipliers became available, but these were quite expensive, even for the 16x16 bit fixed point multiplier that was commonly used. Many of the "classic" reverberators used multipliers that only had a few bits of resolution, such as 16x3 or 16x6 bits. The first Alesis reverb had NO multiplier, and simply used shifts and adds for its operations. This sounds horribly limiting, but if you use the "allpass loop" topology, you'll find that the allpass coefficients don't need a whole lot of precision, at least if you are going for a "classic" sound. 0.5 or -0.5 is a perfectly decent allpass coefficient. The higher precision operations were often reserved for the overall loop feedback time, as these controlled the overall reverb decay.


The big trick that most of the old reverb hardware used was to control memory addressing in such a way that the incrementing and wrapping of the circular buffers happened automatically. I have programmed a lot of reverbs on general purpose CPUs and DSPs, and for each delay line you need to increment your read and write pointers each sample, and do bounds checking to ensure that the pointers don't go outside the range of your memory addresses. This takes cycles. Hardware DSPs often have built-in functions for circular buffers, but general purpose processors don't. Meanwhile, the old reverb hardware platforms would simply specify a location in delay memory to read from or write to, and ALL locations would be automagically incremented and wrapped for each input sample. 


A modern chip that closely resembles the "old school" hardware reverb processors is the Spin Semiconductor FV-1. This chip has a small selection of assembly language instructions (28 or so), 32K words of delay memory, and can execute 128 instructions per input/output sample. It is essentially a 6 MHz processor, when clocked at normal audio rates. However, it has been optimized for a variety of reverb and delay programs (allpass loop and parallel combs reverbs, chorus, flanging, pitch shifting, etc.), and has enough horsepower to execute the "classic" Lexicon algorithms, such as the one listed at the Dattorro site. Some of the tricks used to get this sort of performance out of such a low clock rate:


- Automatic incrementing/wrapping of circular buffers, built into delay memory addressing system.

- Allpass delays that take 2 instructions. Note that these are NOT nested allpass delays, which will take more instructions.

- Built in LFOs, that are automatically updated for each input/output sample.

- Built-in support for linear interpolation.

- A simple MAC that allows a delay tap to be read, scaled, and added to the accumulator, all in one instruction.


This isn't to say that modern DSPs and CPUs can't easily beat the performance of the old custom hardware. A 300 MHz Blackfin has a HUGE amount of raw horsepower. It doesn't really matter that each delay pointer takes a few cycles to be incremented and wrapped, when you have 50X the clock speed of the older units. Modern Intel CPUs have enormous caches, so your entire reverb algorithm can fit in there - this gives you fast memory accesses for your delay lines. Still, we are talking about boxes that are 30+ years old, which hit the market at around the same time as the first digital watches. The performance of those old boxes, in that context, is stunning.

Quote: > I think a better explanation is that the difficulty of the problem in the early years attracted a more dedicated class of designer that was willing to spend a great deal of time experimenting and refining the algorithms.  They worked well ahead of any published research, without necessarily having a great deal of prior knowledge of artificial reverberation, or even much of a preconceived notion of what digital reverb is supposed to sound like.That's extremely impressive, and more than a little humbling when I can get something basic happening in about an hour, but then I'm too lazy to tune it much better than "not completely awful".Larry the O wrote an amazing post about how the original Lexicon algorithms and hardware came into being:

[https://gearspace.com/board/5519632-post247.html](https://gearspace.com/board/5519632-post247.html)


Both the Lexicon 224 and EMT-250 seemed to follow similar development patterns:


- Engineers develop hardware to execute reverb algorithms in real time.

- Engineers program Schroeder algorithms into the new hardware, and find the results lacking.

- Engineers work on new reverb algorithms, using the new real-time hardware as a way of speeding up the development process.


I'm old enough that I started DSP development in a non-real-time environment (Csound). At the time I was working on reverb designs, it would only take a few minutes to render the file and listen to the results, but any parameter tweaking would require a recompile and re-render. This is slower than having a box or program that you can tweak and listen to on the fly. Still, this is NOTHING compared to the early days of computer music, when Schroeder was developing his reverbs. Back then, it took hours to days of computation on a shared mainframe computer. The results were spit out of a custom DAC, and stored on analog tape. IIRC, the DAC was located about 30 miles from the mainframe computer at Bell Labs, so there was a drive involved between putting in your punch cards, waiting for the results to compute, and getting your audio tape to hear your results. The hardware that Blesser and Griesinger were working with sped up the development process for digital reverb algorithms by several orders of magnitude.

Quote: > Also, on a somewhat related note, are the Ursa Major products the only ones that used significant analog processing inside the actual reverb engine?I don't know of any other reverbs that use analog components in the feedback loop. Most of the renowned digital reverbs use "unitary" algorithms, in that the total gain of the system(s) that feedback is applied to is bounded by 0 dB for all frequencies. The Space Station and Stargate used a multitap delay with feedback, that has a VERY bumpy frequency response with feedback. The feedback taps are time-varying, which allows for about a 3X feedback gain before oscillation, but you can still get some tweaky frequencies that can "blow up" in a digital system. The analog feedback path might produce a more pleasant clipping, and certainly avoids the aliasing that would happen if the clipping happened inside of a fixed-point processor.

---

### Post #544 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5624469&postcount=544>

Quote: > Originally Posted byacreil➡️If that's what I think it is, it's pretty crazy.It is.


Another page from the Audio Grimoire has been revealed.

---

### Post #545 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5628663&postcount=545>

Quote: > Originally Posted byseancostello➡️The 1992 Gardner MS thesis has a LOT of similarities with the reverb on the Dattorro site.Yeah, that's what I was thinking of.  Looks like a beast of an algorithm compared to the other one.  Griesinger must have had a great deal of patience.


What I'm trying to get at with the DSP vs. discrete thing is that plenty of later, cheaper developments (ART, Yamaha, etc.) aren't nearly so fondly remembered as the 250/244.  I can't do much to guess what's going on inside their ASICs but I don't imagine them being terribly deficient in terms of instructions per sample compared to the early "discrete DSPs".  I expect the biggest difference is that their design pattern more closely resembled this:


- Company develops in house ASIC for reverb and other effects.

- Engineers program Schroeder algorithms into the new hardware.

- Engineers make moderate refinements and intuitive extensions based on in-demand features and easy selling points (CD quality sound!).

- Sounds like reverb to me, let's ship it.


Tangential but amusing (to me): German organ manufacturer Wersi implemented a digital "reverb" using a single 68B09 microprocessor.  Here are the specs: 4 kHz bandwidth, NE571 compander, 12 bit A/D and D/A, 2k x8 RAM, decay time up to 4 seconds, pseudo-stereo output via TDA3810, 4 programs (short and long reverb, fast and slow echo).  I haven't heard it but it must be rather... remarkable.

Quote: > Still, this is NOTHING compared to the early days of computer music, when Schroeder was developing his reverbs. Back then, it took hours to days of computation on a shared mainframe computer. The results were spit out of a custom DAC, and stored on analog tape. IIRC, the DAC was located about 30 miles from the mainframe computer at Bell Labs, so there was a drive involved between putting in your punch cards, waiting for the results to compute, and getting your audio tape to hear your results.Lately I've been enjoying some of the music that came out of the early computer music era.  There's plenty of bad reverb too.


Sometimes it seems like the most interesting results come from the most difficult conditions.  Not that difficulty is a virtue, but the type of individual attracted to it must have an irrational amount of enthusiasm or inspiration.

---

### Post #546 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5629875&postcount=546>

Quote: > Originally Posted byacreil➡️What I'm trying to get at with the DSP vs. discrete thing is that plenty of later, cheaper developments (ART, Yamaha, etc.) aren't nearly so fondly remembered as the 250/244.True, and I think that you are correct in presuming that the difference has less to do with any inherent capabilities of the hardware, and more to do with the skills of the algorithm developers.

Quote: > Lately I've been enjoying some of the music that came out of the early computer music era.  There's plenty of bad reverb too.Have you heard "Turenas" by John Chowning? Great piece, but the reverb sounds like a swarm of bees. The last time I heard it, it took me a little bit to realize that those weird sustained sine waves were supposed to be reverberation. Pretty cool sound, actually. Undoubtedly this was the 4 comb, 2 allpass Schroeder configuration - the CCRMA guys figured out more complicated Schroeder networks by the mid 1970's.

Quote: > Sometimes it seems like the most interesting results come from the most difficult conditions.  Not that difficulty is a virtue, but the type of individual attracted to it must have an irrational amount of enthusiasm or inspiration.I like limits, whether they are imposed externally or internally. I am always inspired when working with the FV-1 - it is a challenge to find workarounds for what I want to do. Meanwhile, the blank slate presented by Xcode and a blazing fast CPU suggests an infinite number of possibilities, which makes forward progress difficult. Where to begin? Limiting your work to a small fraction of the CPU helps narrow things down somewhat.

---

### Post #547 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5631718&postcount=547>

Quote: > Originally Posted byseancostello➡️Have you heard "Turenas" by John Chowning? Great piece, but the reverb sounds like a swarm of bees. The last time I heard it, it took me a little bit to realize that those weird sustained sine waves were supposed to be reverberation. Pretty cool sound, actually. Undoubtedly this was the 4 comb, 2 allpass Schroeder configuration - the CCRMA guys figured out more complicated Schroeder networks by the mid 1970's.That's exactly the one I was thinking of (and "Sabelithe").  I can't criticize it too much, though, since the point was dynamic spacialization.  I'd assumed he used the "JCRev" algorithm.  The full bandwidth reverb with overly clicky attacks makes a pretty disconcerting effect. 

Quote: > I like limits, whether they are imposed externally or internally. I am always inspired when working with the FV-1 - it is a challenge to find workarounds for what I want to do. Meanwhile, the blank slate presented by Xcode and a blazing fast CPU suggests an infinite number of possibilities, which makes forward progress difficult. Where to begin? Limiting your work to a small fraction of the CPU helps narrow things down somewhat.I think I'm coming to grips with the limitations vs. no limitations thing (speaking as broadly as possible- music and everything else).  I think it helps to start off in a relatively constrained environment (or by studying someone else's work under similar constraints) to grasp the sheer depth of what you're dealing with.  Something more open ended is appropriate once you've built up a cache of ideas that require a lot of resources.  Starting off with wide open possibilities seems to result in either disorganized paralysis or existential confusion.


More on topic, I just realized the "new" Griesinger algorithm has both high and low pass shelving filters- this makes a lot more sense to me now, though the "asymmetric" locations in the loop are a little odd (though I guess a necessity).

---

### Post #548 -- Page 19
**User:** volumetric
**Info:** Joined: Jul 2010Posts: 4🎧 15 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5638362&postcount=548>

acreil wrote:

Looks like a beast of an algorithm compared to the other one.  Griesinger must have had a great deal of patience.


---------------


The larger algorithm shows all the work that goes into creating good sounding reverbs. Very different than the one published in the AES article. 


Just as Dave G. expanded the work of Schroder in the 70s, that larger allpass loop topology is an extend version of the earlier one Dattorro published.


The Audio Amulet has been activated, time to tweek the Talisman Coefficients.

---

### Post #549 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5638750&postcount=549>

Quote: > Originally Posted byvolumetric➡️The larger algorithm shows all the work that goes into creating good sounding reverbs.Has anyone tried the new algorithm with the listed delay lengths? Does it sound any good?

---

### Post #550 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5641041&postcount=550>

I'll probably give it a shot.  One thing needs clarification, though.  Labels (2) and (3) represent linear interpolation, implying that the delay at (1) represents the modulation depth, yes?  But the modulation at (4), 121 samples is much larger than the modulation at (1), 5 samples.  


Should I trust this, or assume that the modulation has somehow "paused" in the middle of modulating and the specific numbers don't represent anything special?  The interpolation coefficients sort of imply that it's "paused".  5 samples of modulation seems really, really subtle.

---

### Post #551 -- Page 19
**User:** volumetric
**Info:** Joined: Jul 2010Posts: 4🎧 15 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5641113&postcount=551>

Quote: > Originally Posted byacreil➡️More on topic, I just realized the "new" Griesinger algorithm has both high and low pass shelving filters- this makes a lot more sense to me now, though the "asymmetric" locations in the loop are a little odd (though I guess a necessity).Does anyone think the shelving filter locations are asymmetic because they add some subtle uneveness to the frequency absorption? A real room does not absorb frequencies evenly at each wall. 


Of course we can't hear individual late reflections, but possibly it makes things sound more natural. Same concept as small phase differences, delay differences etc.

---

### Post #552 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5641198&postcount=552>

Quote: > Originally Posted byacreil➡️I'll probably give it a shot.  One thing needs clarification, though.  Labels (2) and (3) represent linear interpolation, implying that the delay at (1) represents the modulation depth, yes?  But the modulation at (4), 121 samples is much larger than the modulation at (1), 5 samples.Should I trust this, or assume that the modulation has somehow "paused" in the middle of modulating and the specific numbers don't represent anything special?  The interpolation coefficients sort of imply that it's "paused".  5 samples of modulation seems really, really subtle.I'd say "paused." Honestly, I haven't been around a 224XL for about 18 years, so I'm not sure exactly how the modulation works. However, the division of the delay into two blocks certainly implies a fixed delay, and a time-varying delay that is linearly interpolated.

---

### Post #553 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5641228&postcount=553>

Quote: > Originally Posted byvolumetric➡️Does anyone think the shelving filter locations are asymmetic because they add some subtle uneveness to the frequency absorption? A real room does not absorb frequencies evenly at each wall.That is one of Jot's major ideas - associating a filter with each delay line, such that you have a symmetric decay of frequencies versus time. However, plenty of good reverbs were made without the Jot style filters. 


Associating a higher-order filter with each delay line ends up being costly as far as CPU. The new Dattorro (i.e. old Griesinger) reverb looks complicated, but it is actually pretty light on the CPU. It dates back to 1978, when getting anything running in real time in the digital domain was a pretty amazing feat. Having a single shelving filter + high frequency damping filter per "side" ends up producing a pretty consistent sound within this structure. Don't forget that the output of one side will quickly go into the other side. That, plus the smearing of the allpasses, makes it hard to hear any particular left-right spectral imbalances.

---

### Post #554 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5647942&postcount=554>

I just got the new Griesinger algorithm working in PD, at least well enough to listen to.  Haven't made sure it's all bug free yet, or worked out all the details.  I'm trying to make a usable "interface" for it, which I'm not good at and is a huge pain in PD anyway, so that's taken most of the effort.


I made a few changes that I think should be practical.  I lumped some of the gains together and moved the loop gain and "damping" filter to before the input is added.  That should be reasonable, right?  Also I'm not sure what the total length of the modulated delays should be and I may have screwed up the filters.


I also don't fully understand the notation for the output taps so for now I'm just taking them from the second APF.


For modulation I'm using a self-devised piecewise linear thing.  The modulation for the two sides can be complementary or independent.  To that I'm adding a sinusoidal modulator with adjustable phase shift for one side, so the relationship between the two outputs can be quadrature or whatever.  I'd like to think this covers all bases pretty reasonably since it can be periodic or not, and also have combined slow and fast modulation.


Initial impressions of the sound: The algorithm is kind of a "big hall".  As depicted in the diagram (assuming I didn't screw it up, and probably depending some on my output tap arrangement) you mostly hear rather sparse "reflections", with more loop gain it becomes more rich and spacious.  Not a lot of coloration or ringing, but there is some bass resonance, not unlike a real acoustic space.   It sounds nice enough that I don't really want to go "tweaking" (ruining) the delay times.  I don't think you should have a lot of faith in my assessment, though.


So that's how he gets the nested APFs to sound reasonable: the delay times are quite long so they only gradually build density.  My feeble efforts in that direction used short delays and seemed more or less doomed to metallic ringing.

---

### Post #555 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5648248&postcount=555>

I must have screwed something up (surprise), I can't get very long decay times without it turning into poo.  


I'll have to check the 224 manual to guess what algorithm it is (possibly Concert Hall?  Dark Hall?) and figure out how to map the gains to more user friendly parameters.


Also I noticed something interesting:  In the scanned letter from Griesinger to Dattorro saying that he was granted permission to publish the 224 algorithm in the AES article (I've only got a saved .jpg but I think it's from Dattorro's site), he mentions that similar algorithms were independently discovered by Gardner.  That seems to apply to this new one a lot more than the original AES one.


Also the "old one" specifies a sample rate of 29.761 kHz while the "new one" is 34.125 kHz....

---

### Post #556 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5652097&postcount=556>

Quote: > Originally Posted byacreil➡️I must have screwed something up (surprise), I can't get very long decay times without it turning into poo.My guess is that your nested allpasses aren't truly allpass. The ordering of operations is pretty critical for these, and it is tricky to get right in a visual programming language. Don't forget to include the block size in the length of the delays, and to make sure that your block size is small enough to realize all the delays.

Quote: > I'll have to check the 224 manual to guess what algorithm it is (possibly Concert Hall?  Dark Hall?) and figure out how to map the gains to more user friendly parameters.I'd guess Concert Hall. Dark Hall would have more interpolated delay lines. Bright Hall would have the high damping 1-pole in a different location.

Quote: > Also the "old one" specifies a sample rate of 29.761 kHz while the "new one" is 34.125 kHz....Think Ensoniq DP/4 versus Lexicon 224XL.

---

### Post #557 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5654897&postcount=557>

Quote: > Originally Posted byseancostello➡️My guess is that your nested allpasses aren't truly allpass. The ordering of operations is pretty critical for these, and it is tricky to get right in a visual programming language. Don't forget to include the block size in the length of the delays, and to make sure that your block size is small enough to realize all the delays.I think the only order of operations issue I have to worry about here is for delays smaller than one block (64 samples).  There are 3 in the loop but they're all between the APFs. 


You were right though, the nested allpasses aren't allpass, BUT that's because of the decay gains inside the APFs (which seemed a little weird to me from the start).  It does what I expect if I set the decay gains all to 1 and use the loop gain to control decay time.  Not sure what to make of that...


I mean it's strange that the diagram has a fairly low overall loop gain (0.237 per side) and decay gains in locations that will change the frequency response of the whole thing.  Fair enough that he probably wanted to use distributed gains, but it would have been a lot more kosher to put them between the APFs, right?  I'm not sure how the decay control is supposed to map to these gains, since there are 3 different sets.   


I didn't miscalculate either since it will happily go on forever if I set everything to 1.

Quote: > I'd guess Concert Hall. Dark Hall would have more interpolated delay lines. Bright Hall would have the high damping 1-pole in a different location.Interestingly all the algorithms described in the manual show a diffusion stage outside of the main loop.


Could be Dark/Rich Chamber maybe?  I think the sound most closely resembles the descriptions of those in the manual (reading 224X v8.2 user manual).


Anyway this is encouraging.  I'll try to figure out how the output taps are supposed to go, do some minor fine tuning and then maybe post a sample.

---

### Post #558 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5657255&postcount=558>

Quote: > Originally Posted byacreil➡️You were right though, the nested allpasses aren't allpass, BUT that's because of the decay gains inside the APFs (which seemed a little weird to me from the start).  It does what I expect if I set the decay gains all to 1 and use the loop gain to control decay time.  Not sure what to make of that...The allpass topologies as shown might be derived from the original 1962 Schroeder paper. If you set the gains to 1 as shown, you get your standard 2-multiply lattice section.

Quote: > I mean it's strange that the diagram has a fairly low overall loop gain (0.237 per side) and decay gains in locations that will change the frequency response of the whole thing.  Fair enough that he probably wanted to use distributed gains, but it would have been a lot more kosher to put them between the APFs, right?  I'm not sure how the decay control is supposed to map to these gains, since there are 3 different sets.The diagram undoubtedly is taken from the algorithm at a given state. Assume that all sorts of things change depending on the settings, including allpass coefficients, delay lengths, and gain coefficients.

Quote: > Could be Dark/Rich Chamber maybe?  I think the sound most closely resembles the descriptions of those in the manual (reading 224X v8.2 user manual).I'm pretty sure this is Concert Hall, and not one of the "Rich" algorithms, or any form of Chamber.

---

### Post #559 -- Page 19
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5676730&postcount=559>

I always hated the arbitrary adoption of words like "Rich"...


What WAS the difference between the normal and "Rich" chambers, etc?


Nobody Special care to comment?


I know that Rich Hall was a comedian....

---

### Post #560 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5682980&postcount=560>

I doubt we'll get any official word on this since Lexicon apparently still use algorithms derived from this.  I finished the output tap stuff, but haven't done much in the way of fine tuning or debugging.  It sounds great though.


I'll get some proper samples together later, but here's a brief not very good one for now.  It was a mildly disappointing proof of concept that ended up sounding nicer than I expected.  The Lexicon algorithm is in there, but I'm also doing some other stupid stuff so it's not as clear as it should be.

---

### Post #561 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5683028&postcount=561>

Here's the guitar example from a few pages back.

---

### Post #562 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5723954&postcount=562>

Keith Barr, developer of the Alesis reverbs and a whole bunch of other designs for MXR, Alesis and Spin Semiconductor, died today at age 61:

[In Memoriam-Keith Barr 1949-2010](http://mixonline.com/news/keith_barr_obit_2508/)


I've put up a blog post where I've shared Keith's story about the creation of the Midiverb, as well as some of Keith's general approaches to reverb design:

[RIP Keith Barr « The Halls of Valhalla](http://valhalladsp.wordpress.com/2010/08/25/rip-keith-barr/)


My post is apropos to this thread, but in no way reflects the scope of the work Keith Barr did in his life. Truly amazing work, and a genuinely nice guy. May he rest in peace.

---

### Post #563 -- Page 19
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5729584&postcount=563>

Quote: > Originally Posted byseancostello➡️Keith Barr, developer of the Alesis reverbs and a whole bunch of other designs for MXR, Alesis and Spin Semiconductor, died today at age 61:In Memoriam-Keith Barr 1949-2010I've put up a blog post where I've shared Keith's story about the creation of the Midiverb, as well as some of Keith's general approaches to reverb design:RIP Keith Barr « The Halls of ValhallaMy post is apropos to this thread, but in no way reflects the scope of the work Keith Barr did in his life. Truly amazing work, and a genuinely nice guy. May he rest in peace.Thanks Sean, it is a tragic loss...

---

### Post #564 -- Page 19
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5731281&postcount=564>

This man revolutionised recording. ADAT, cheap verbs made it possible for a lot of people to make recordings. His company filled a lot of low and mid budget studios. I did not know him personally, but I've used a lot of his tools.

---

### Post #565 -- Page 19
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5747854&postcount=565>

Sucks about Keith Barr, I was actually recently contemplating asking him some reverb-related questions.  I should probably take this as a sign to pester people more readily.  I seem to have developed an allergic reaction to the Quadraverb's reverb algorithms, but it's still a great product.


Anyway, more on topic, I've long wondered about the Quantec QRS.  I recognize that it's a little controversial among reverb aficionados, but it does seem to have earned its place in history.

[FAQ : QUANTEC Audio Pro](http://www.quantec.com/index.php?id=faq%20FAQ) gives some hints about the algorithm but it seems liberally dosed with marketing bullshit.  I've seen schematics, but as expected they weren't especially illuminating (20 kHz sample rate, IC multiplier...).  One algorithm with adjustable room size (global delay scaling, I guess), stereo in, stereo (or quad) out, no multitap early reflections, no modulation, just one single recirculating tank, increasing density but can be set to constant density (at least in the Yardstick).


And then I found this: [NATIVE INSTRUMENTS : Community : Reaktor User Library](http://www.native-instruments.com/index.php?id=userlibrary&L=1&type=0&ulbr=1&plview=detail&patchid=6584)


I'm a little skeptical at the writer's claim to have reverse-engineered it from impulse responses.  Some of the already known information makes it a little easier, but I've looked at these same impulses before without feeling terribly enlightened.  Having a hardware unit to play with would make it a great deal easier to analyze, obviously.


Well, upon investigating a little further...


I can see from the impulse responses 16 early pulses that may represent the main delay lengths (these are all the same amplitude and present in both channels), followed by 16 attenuated pulses that seem to be associated with each main delay (APF or something?).  Some of the pulses are inverted in one channel (doesn't strike me as a fantastic idea, but okay...), which helps me identify which secondary pulses correspond to which primary pulses.  The secondary pulses are inverted (which also seems to suggest APF) but apparently in the same order as the primary pulses.  Toward the end they start to overlap with more (apparently recirculated?) pulses but it's still fairly clear up to that point.  After that, I dunno, a bunch of stuff.  Impulse responses from specifically chosen settings would help a lot, I'm only working from presets.


This is an alright start, for being based on a partially informed but more or less arbitrary assumption about the topology.  How can I either verify or improve this assumption?  Once pulses begin recirculating and overlapping there's not much I can do to distinguish their sources.  The only thing I can think is to calculate a hypothetical delay time and see if something shows up in the anticipated spot.  Seems like pure tedium, though.


On a possibly related note, is autocorrelation an appropriate way to identify the delay lengths of parallel feedback comb filters?

---

### Post #566 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5751697&postcount=566>

Quote: > Originally Posted byacreil➡️Sucks about Keith Barr, I was actually recently contemplating asking him some reverb-related questions.  I should probably take this as a sign to pester people more readily.  I seem to have developed an allergic reaction to the Quadraverb's reverb algorithms, but it's still a great product.I have been thinking about this a lot. I really wish that I had formally interviewed Keith Barr, with a bunch of questions aimed towards us engineering types. He obviously enjoyed sharing his experience with others.


From one of Keith Barr's emails to me:

Quote: > I’ve forgotten about the Quadraverb. I think it was a 64 instruction engine, may have been 128. Frank would know, he did the chip as I recall. For algorithms, I was the guru at the time, and I was just coming around to putting APs in delays loops and recognizing the need for extensive loop filtering. My guess is that the Quadraverb used 4 parallel loops of 2 X AP +1 delay, outputs from delay taps as the basic structure. I doubt there were any single large loops like I use now.Hopefully that is useful. My general impression of Keith's work is that he started with Schroeder like structures (parallel combs, series allpasses), figured out how to embed allpasses within combs around the time of the Midiverb II or so, and eventually settled upon a single loop with embedded allpasses, with the input injected at various points and taken out from various points.

---

### Post #567 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5751735&postcount=567>

Quote: > Originally Posted byacreil➡️Anyway, more on topic, I've long wondered about the Quantec QRS.  I recognize that it's a little controversial among reverb aficionados, but it does seem to have earned its place in history.I've thought about this algorithm a lot too. My suggestion: Read both the 1982 manual and the newest manual THOROUGHLY, and think about the implications. As far as impulses, I believe that Warp69 has some secret sauce for figuring out things via test signals, but I have no idea what that is. Still, your observation of 16 delay lengths being visible seems significant.


I wish that someone would record Quantec impulses with "degenerate" settings. Things that sound horrible as reverbs can be very useful when figuring out structures. If you can turn diffusion down to zero, this helps a lot. I know that Alesis reverbs allowed for this, while Lexicon verbs (wisely) had a minimum diffusion level (or "definition" level as the case may be), that makes reverse engineering more difficult.

---

### Post #568 -- Page 19
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5751934&postcount=568>

Quote: > Originally Posted byseancostello➡️I believe that Warp69 has some secret sauce for figuring out things via test signals, but I have no idea what that is.Heh - I wish that was true, but sadly no.


There exist extensive amount of information about different reverb topologies on the internet - after many years of trying the different topologies and see how they behave - you get very good at guessing.

---

### Post #569 -- Page 19
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5751964&postcount=569>

Quote: > Originally Posted byWarp69➡️Heh - I wish that was true, but sadly no.There exist extensive amount of information about different reverb topologies on the internet - after many years of trying the different topologies and see how they behave - you get very good at guessing.So, the "secret sauce," in this case, is YOUR BRAIN.

---

### Post #570 -- Page 19
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5752162&postcount=570>

You know how it is - you get this strange idea in the middle of the night and you simply have to try it out on the computer - your wife ask 'Now?!?!' 


Just an example : Jonathan Abel and David Berners release a paper called ' An Emulation of the EMT140 Plate Reverberator Using a Hybrid Reverberator structure'.


Some valuable information about the UAD Plate 140 algorithm : Convolution + FDN. Since you know it contains a FDN, it might use a Hadamard Matrix - a good guess would be a matrix of order 16 - in this case, they might only use, let us say, 14 delay lines instead of 16 delay lines..........


---

## Page 20

---

### Post #571 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5752761&postcount=571>

Quote: > My guess is that the Quadraverb used 4 parallel loops of 2 X AP +1 delay, outputs from delay taps as the basic structure.That would actually be pretty easy to verify with "degenerate impulses".  And if that's actually the case, it wouldn't be so hard to reverse engineer either (so long as the basic topology is known from the start!)

Quote: > Originally Posted byseancostello➡️I wish that someone would record Quantec impulses with "degenerate" settings.I already tried asking someone, he's too busy.  Anyway there's not a lot to "degenerate" here, I was mostly just hoping to find the mono in to quad out mappings.   If my current line of thinking is correct (and that means ignore everything from the previous post...), that should make it possible to uniquely identify all of the delays.  


I've found an impulse response from the Yardstick that doesn't have the usual crazy brickwall filtering, which should make it quite easy to measure delay times and amplitudes.  Actually, the whole thing should be rather easy.  It seems like a very primitive algorithm.

---

### Post #572 -- Page 20
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5753334&postcount=572>

As some have argued earlier - it's not possible to capture the sound of hardware units with impulse responses and it's therefor not possible to extract the reverb topology either.


Most will say the reason for that is modulation, but modulation is only a small part. Even IR of modulation less structures doesn't sound like the original.

---

### Post #573 -- Page 20
**User:** Synæsthesiac
**Info:** Joined: May 2010Posts: 226🎧 15 years | Posts: 226
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5753340&postcount=573>

Quote: > Originally Posted byFroomboschThis man revolutionised recording. ADAT, cheap verbs made it possible for a lot of people to make recordings. His company filled a lot of low and mid budget studios. I did not know him personally, but I've used a lot of his tools.I met him in 2000 at NAMM in L.A. He was like the guy who fixed your A.C. or the UPS man, but was a genius. He sold me on a Masterlink which I still have and use to this day.

---

### Post #574 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5753576&postcount=574>

Quote: > Originally Posted byWarp69➡️As some have argued earlier - it's not possible to capture the sound of hardware units with impulse responses and it's therefor not possible to extract the reverb topology either.Most will say the reason for that is modulation, but modulation is only a small part. Even IR of modulation less structures doesn't sound like the original.The Quantec has no modulation and is based on a simple topology.  The Yardstick (the source of the impulse response I'm studying) is strictly digital input/output, so converters and anti-aliasing filters and other such things aren't coming into play at all.  Assuming the impulse response was competently captured (seems fine to me), I don't see any other factors coming into play.


Inevitably details will be missed, unless I make a cycle accurate clone of the hardware.  But such things are outside the scope of the typical design process, so I don't think a default value judgment of those characteristics is really warranted.  I'm not going to consider it a success or failure on a basis of whether it can distinguished from "the real thing" in a double blind test.  If that were the criteria, I wouldn't bother trying (not without getting at least a Master's out of it).


These things have serious design compromises already, I'm not going to treat it like it's some sacred relic.  I want to be able to use it and to experiment with and expand upon the algorithm.  It isn't that I'm not reasonably discerning, but I'm not going to assume that the factors I'm ignoring or getting wrong necessarily make an unambiguously positive contribution to the end result.  If anything I stand to gain from it- some modulation might be nice, and I don't like that brickwall filter anyway.

---

### Post #575 -- Page 20
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5753825&postcount=575>

I don't doubt you can create a topology out of an impulse response, but it's your interpretation of the **impulse response** and NOT the algorithm that the IR was based on.


My point is that the IR doesn't have enough information for you to recreate the original algorithm. Even the original designer of the Quantec algorithm say the same thing in FAQ.


Let me give you an example of an extremely basic structure without any modulation - it's under 1% of a complete algorithm.


Left channel - is the actual dirac impulse used for the creation of the impulse response in the right channel. Right channel is the result.

[Impulse.wav](https://gearspace.com/board/attachments/geekzone/190833d1283603831-reverb-subculture-impulse.wav?s=2bd1dfff49c5a55ff164fe6c1d6d8042)


Please try to reverse engineer that very basic structure only using the IR.


Now I have picked another signal (sine in this case) going through the exact same structure.

[Sine.wav](https://gearspace.com/board/attachments/geekzone/190834d1283604122-reverb-subculture-sine.wav?s=2bd1dfff49c5a55ff164fe6c1d6d8042)


Left channel = the input signal. Right channel = the result.


This is just a very small example to show that IR doesn't have enough information to recreate the original structure.

---

### Post #576 -- Page 20
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5754411&postcount=576>

Quote: > Originally Posted byacreil➡️..........and I don't like that brickwall filter anyway.That is of course related to the reduced sample rate of the original units - just like Lexicon 224(XL), EMT250 and many others.

---

### Post #577 -- Page 20
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5754629&postcount=577>

That brickwall filter can be essential for some of those designs. When the newer 251 came out it had higher samplerate, but a lot of people liked the darker 250 more.

---

### Post #578 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5755470&postcount=578>

Quote: > Originally Posted byWarp69➡️Please try to reverse engineer that very basic structure only using the IR.It would appear to be a 2 multiply allpass filter with a delay of 90 samples, coefficient of 0.5 and series gain of 0.5.  The sine shows a nonlinearity.


Well that's great but it tells me nothing I didn't know already.  I'm not trying to model a compressor or distortion pedal.  Impulse responses are strictly linear time invariant, that's news to no one.  But I know of no reverb algorithms that include a deliberate nonlinearity anywhere (barring ducking behavior), and I'll be perfectly happy if my model doesn't include clipping or quantization noise.

---

### Post #579 -- Page 20
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5756050&postcount=579>

Quote: > Originally Posted byacreil➡️It would appear to be a 2 multiply allpass filter with a delay of 90 samples, coefficient of 0.5 and series gain of 0.5.  The sine shows a nonlinearity.That's of course the obvious answer, if you use the IR as reference, but it's not correct. As stated earlier - an impulse response doesn't contain enough information to recreate the original algorithm.


I believe we all test our algorithms with signals other than dirac impulses - IR doesn't show everything.

---

### Post #580 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5756439&postcount=580>

Quote: > Originally Posted byWarp69➡️I believe we all test our algorithms with signals other than dirac impulses - IR doesn't show everything.This only true if the system is non-LTI, and I haven't seen anything to suggest that the Quantec algorithm isn't LTI.  If you're suggesting there's some other factor involved (distortion, aliasing, quantization noise, jitter), I'd miss that even with full documentation, and I'd have a hard time believing it would make a positive contribution anyway.  


It's fair enough as well to suggest that there are still some ambiguities- different IIR structures (Direct-Form I/II, etc.) have identical impulse responses, for example, but I don't expect the finer points of those (susceptibility to clipping and quantization) to be relevant here since I'm doing everything in floating point.

---

### Post #581 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5760126&postcount=581>

I'm still working through the Quantec algorithm.  I don't know how much I can tastefully disclose on a public forum.  It's fairly straightforward and anyone who wants to can more or less figure it out anyway (much more easily than with other reverbs).  It's already available for Reaktor and I'm sure it's been done by others too.  Still, I don't know if I want to be "that guy".  


Basically it's this:


There are 16 independent "resonators", each consisting of 2 delays in some sort of increasing density configuration that you can probably guess.  The page with the Reaktor clone said 3 delays (or at least 3 taps), but 2 delays fills up all the original QRS's memory (64k x 26 bit) at max room size.  Decay and amplitude for each channel are sloped to smooth the attack slightly and produce a uniform decay, and the delays in each resonator are weighted in a way that produces a fairly "unique" overall envelope (this depends a lot on the density setting).  Actually this may be a reason for its popularity, not that the design permits a lot of degrees of freedom here.  There are some similarities to Dave Griesinger's "Recent Experiences With Electronic Acoustic Enhancement in Concert Halls and Opera Houses" stuff, and the quite low density/slow build seems to be flattering to many types of sound.  


The spec sheet says the original QRS is 5 MIPS (I guess rounded down from 5.12).  At a sample rate of 20 kHz that's 256 instructions per sample, or 16 per resonator.  Actually there are probably a few more instructions for "first reflections" and reverb wet level.  The address incrementing hardware has to be pretty clever, then, and this may explain why there's only one algorithm.  The "room size" parameter is supposed to change room size by orders of magnitude, but it actually scales delay times by a factor of 2 (not surprising, right?).


The FAQ and manual make much of the "spacial" qualities, which I think this is partly clever design and partly just hyperbole.   Each input feeds half of the resonators, the weighted sum of the delays of each resonator is sent to all outputs, but with with different polarity.  For any 2 outputs, it's 50% in phase and 50% out of phase.  For the plain L and R outputs (I think), the shortest and longest 4 resonators are in phase and the middle 8 are out of phase (you can clearly see this by looking at the impulse response).  This doesn't seem like a great idea to me, and I'd suggest maybe trying the other outputs.  


The later Yardstick models I think just extend this with more resonators which may fed by more inputs.  These also include fancier filters (still shelf filters but more flexible).  The density parameter goes up to 200% in the newer models, but I think just rescales the old values that went up to 80%.  The original QRS didn't have a density parameter, I think it was fixed at 25%.


I'm tempted to just use a rotation matrix for the feedback in each resonator and a mixer on the output.  This seems most flexible and controllable.  Also I've kinda wanted to try the quadrature coefficient modulation described in Barry Blesser's patent 7062337.


Well I'm still reading manuals and taking notes and comparing impulse responses for now.  I found a nice typo in one of the manuals: "This is the role of parameter 2nd Delay described on p. Fehler: Referenz nicht gefunden."

---

### Post #582 -- Page 20
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5760199&postcount=582>

Quote: > Originally Posted byacreil➡️I'm still working through the Quantec algorithm.  I don't know how much I can tastefully disclose on a public forum.  It's fairly straightforward and anyone who wants to can more or less figure it out anyway (much more easily than with other reverbs).  It's already available for Reaktor and I'm sure it's been done by others too.  Still, I don't know if I want to be "that guy".Don't worry, I'm sure anything you could possibly "disclose" wouldn't hurt or bother Quantec in the least. If "figuring it out" was really so easy, life would have been wonderful.

---

### Post #583 -- Page 20
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5760456&postcount=583>

Quote: > Originally Posted byacreil➡️There are 16 independent "resonators", each consisting of 2 delays in some sort of increasing density configuration that you can probably guess.Allpass delay + delay in series? This is what is implied in the Yardstick, when turning up Density increases the RT60. I had thought 3 delays as well - maybe 2AP+1 delay.

Quote: > Decay and amplitude for each channel are sloped to smooth the attack slightly and produce a uniform decay, and the delays in each resonator are weighted in a way that produces a fairly "unique" overall envelope (this depends a lot on the density setting).  Actually this may be a reason for its popularity, not that the design permits a lot of degrees of freedom here.Interesting. I thought that the slow attack was due to series allpasses, as they do the same thing if overused. Are the decay (feedback) coefficients equal for each resonator? 

Quote: > The FAQ and manual make much of the "spacial" qualities, which I think this is partly clever design and partly just hyperbole.   Each input feeds half of the resonators, the weighted sum of the delays of each resonator is sent to all outputs, but with with different polarity.  For any 2 outputs, it's 50% in phase and 50% out of phase.  For the plain L and R outputs (I think), the shortest and longest 4 resonators are in phase and the middle 8 are out of phase (you can clearly see this by looking at the impulse response).  This doesn't seem like a great idea to me, and I'd suggest maybe trying the other outputs.This is an old Schroeder idea. Jot uses something similar, but with the mixing matrices unitary. It is useful in creating decorrelated output signals, but the problem comes when you mix the output channels together. Quantec's solution is "don't do that," but I wonder how such an algorithm works when used in a surround sound codec.

Quote: > I'm tempted to just use a rotation matrix for the feedback in each resonator and a mixer on the output.  This seems most flexible and controllable.  Also I've kinda wanted to try the quadrature coefficient modulation described in Barry Blesser's patent 7062337.If the basic resonators are the allpass/delay units, try running the output of one resonator into the input of the next one. In other words, try turning the 16 parallel comb/allpasses into one big allpass loop, with the input injected in 16 places and taken out from 16 places. This won't change the spatial qualities of the algorithm, given the decorrelation mixing used, but it might improve other qualities of the algorithm. Especially if you decide to make aspects of the algorithm time varying.


The quadrature coefficient modulation does some interesting things, but it is no substitute for delay modulation. I first tried it in the early 2000's, and it really sounds like crossfading between a set of fixed resonances, instead of blurring the resonances.

---

### Post #584 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5763078&postcount=584>

Quote: > Originally Posted byShy➡️Don't worry, I'm sure anything you could possibly "disclose" wouldn't hurt or bother Quantec in the least. If "figuring it out" was really so easy, life would have been wonderful.Yeah, but they're still making money from their "11 secret herbs and spices", even if it is just salt, pepper and MSG in the end.  It does bother me a little, though, that they seemingly depend so heavily on making their products appear "unique" and "essential" when there's not really much to it, especially when the people who actually do develop something new and superior (Bricasti, apparently) prefer to keep their mouths shut and let the product speak for itself.

Quote: > Originally Posted byseancostello➡️Allpass delay + delay in series? This is what is implied in the Yardstick, when turning up Density increases the RT60. I had thought 3 delays as well - maybe 2AP+1 delay.Still working out the specifics, conveniently I changed the subject from "what the hell am I doing?" to "how bout them user manuals."


It's definitely lossless when "freeze" is engaged, this removes the loop filter but the density parameter still applies.

Quote: > Interesting. I thought that the slow attack was due to series allpasses, as they do the same thing if overused. Are the decay (feedback) coefficients equal for each resonator?There aren't any series allpasses, it's mostly just the way the two delays are mixed.  The density coefficients are the same, but the decay isn't.  But I'm mostly just looking at the Yardstick, I don't know if the original QRS was this way or if it was a later refinement.

Quote: > This is an old Schroeder idea. Jot uses something similar, but with the mixing matrices unitary. It is useful in creating decorrelated output signals, but the problem comes when you mix the output channels together. Quantec's solution is "don't do that," but I wonder how such an algorithm works when used in a surround sound codec.I've been kind of taking it on faith that much of what Schroeder suggests is sub-optimal, especially when everyone who followed immediately started using (at some expense) independent L/R taps.  It sounds alright though, and it would probably make the wildest thru-zero flange ever if one were to put the 4 outputs through 4 modulation delays and mix to stereo.


The manuals give some specific recommendations for surround stuff (partly why the 8 in/8 out model exists).  Each input and output has independent delay and filtering, also a single signal can be applied to multiple inputs, which gives it relatively higher reflection density.  It's pretty basic stuff, and it doesn't go as far as it could (since the resonator sections are completely independent), but it seems reasonably flexible.

Quote: > If the basic resonators are the allpass/delay units, try running the output of one resonator into the input of the next one. In other words, try turning the 16 parallel comb/allpasses into one big allpass loop, with the input injected in 16 places and taken out from 16 places. This won't change the spatial qualities of the algorithm, given the decorrelation mixing used, but it might improve other qualities of the algorithm. Especially if you decide to make aspects of the algorithm time varying.I'll probably end up just making a general purpose 2-delay FDN "block" that I can copy and paste into whatever configuration I want.

Quote: > The quadrature coefficient modulation does some interesting things, but it is no substitute for delay modulation. I first tried it in the early 2000's, and it really sounds like crossfading between a set of fixed resonances, instead of blurring the resonances.I figure part of the Quantec "theory" is to accept resonance and coloration as being natural, so I don't think that's really out of line.  Realism isn't really on my agenda anyway, so if it sounds like waterphone or something, that's cool too.

---

### Post #585 -- Page 20
**User:** pathdoc
**Info:** Joined: Aug 2010Posts: 1911 Review written🎧 15 years | Posts: 191
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5763199&postcount=585>

You guys are blowing my mind.  I do have a simple question.

Why not use a real plate reverb?  They can be built easily and cheaply.

---

### Post #586 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5763850&postcount=586>

Quote: > Originally Posted bypathdoc➡️You guys are blowing my mind.  I do have a simple question.Why not use a real plate reverb?  They can be built easily and cheaply.I'll have to try it someday, especially as it offers possibilities beyond just reverb (I'm sure it's a far better percussion/performance instrument than a spring reverb).  But I have a rather huge list of DIY stuff to do, all sorts of crap to fix, modify and build.  Software is just the fastest and most powerful way to do something (for me), and since I'd like to actually use it at some point, it makes more sense right now.

---

### Post #587 -- Page 20
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5763919&postcount=587>

Quote: > Originally Posted bypathdoc➡️You guys are blowing my mind.  I do have a simple question.Why not use a real plate reverb?  They can be built easily and cheaply.I don't think that a 2 foot by 6 foot wooden frame would fit in my laptop bag.


heh


Plates are great - I'm sure everyone here would agree upon that. We just have digital obsessions. Many of us program these things as part of our business, and a plugin is easier to sell online and distribute purely digitally than a few hundred pounds of wood and steel. Plus, an algorithm can be embodied in a stompbox, iPhone app, rackmount, etc. 


In my case, I kinda suck at building physical things. For some reason, I am pretty good at building algorithms that sound cool. So I go with what I know.


A plate is also restricted to a fairly narrow set of parameters. You can control the decay time and a bit of the tone, but otherwise you have a fast onset and exponential decay. In the digital world, you can play around with these elements. On the other hand, a plate in its default parameters sounds really good, while it is fairly difficult to tune a digital algorithm to sound this good.

---

### Post #588 -- Page 20
**User:** pathdoc
**Info:** Joined: Aug 2010Posts: 1911 Review written🎧 15 years | Posts: 191
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5764187&postcount=588>

Yes my plate is actually about 3x6 feet without the frame made of 2x6's. 

You would have a hard time fitting it in a laptop bag.

---

### Post #589 -- Page 20
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5764197&postcount=589>

Yeah I have a tube 140 ST in my studio. Huge and heavy. Next project after finishing v2....

---

### Post #590 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5773598&postcount=590>

Continuing with the Quantec algorithm...


I've confirmed the topology of each unit, it is indeed a comb with embedded APF, but the APF tap that goes to the output comes from the feedback loop after the loop gain, for whatever reason.  This means that the density parameter dramatically changes the envelope and sound of the reverb.  I've translated all the gains and feedback coefficients to a standard FDN topology, it really seems like that's a better way to do it since I'd have more explicit control over how  the signals enter and exit.  I'm not sure whether the feedback matrix as it is would have any advantage over a rotation matrix, I should probably just make both variants and see which I like better.  


I'm still figuring out how the individual tap gains and feedback coefficients are.  The APF output taps have increasing gains (with increasing delay times) and the comb taps increase then decrease.  This shapes the initial response of the reverb.  But I'm actually thinking I could ignore that and do a standard "tap weight exponential decay according to reverb time" thing, and then multiply those by a drawn envelope curve or something.

---

### Post #591 -- Page 20
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5776083&postcount=591>

Quote: > Originally Posted byacreil➡️I've confirmed the topology of each unit, it is indeed a comb with embedded APF, but the APF tap that goes to the output comes from the feedback loop after the loop gain, for whatever reason.OK, I'm trying to get this. It seems like you are describing something like this:


inputSum->delay->(outputTap)->decayScale->allpassDelay->(outputTap)->toInputSum


Is this right?

Quote: > I'm still figuring out how the individual tap gains and feedback coefficients are.  The APF output taps have increasing gains (with increasing delay times) and the comb taps increase then decrease.  This shapes the initial response of the reverb.  But I'm actually thinking I could ignore that and do a standard "tap weight exponential decay according to reverb time" thing, and then multiply those by a drawn envelope curve or something.I would try to retain the increase then decrease thing, as this seems critical to the Quantec sound and feel. You could use a standard 16 delay FDN (or a 16 unit FDN, where each unit is a delay and AP in series), deal with the feedback gain coefficients as you see fit, and bolt on the output tap gain pattern from the Quantec.

---

### Post #592 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5777096&postcount=592>

Quote: > Originally Posted byseancostello➡️OK, I'm trying to get this. It seems like you are describing something like this:inputSum->delay->(outputTap)->decayScale->allpassDelay->(outputTap)->toInputSumIs this right?Close, it's actually this:


inputSum->allpass->(outputTap)->delay->loopFilter->(outputTap)->decayScale->toInputSum


The output tap from the allpass is scaled by the density parameter since it's taken from the feedback loop.  The two output taps are just summed.  Also, the density is always negative.


Crappy FDN representation, hopefully the notation isn't too bastardized:


Here A is the allpass delay and B is the comb delay, D is density, FB decay feedback, Wa is the output weight for delay A, and Wb is the output weight for delay B.  D is constant for all resonator units but FB, Wa and Wb vary per resonator.


Input [in->delA, in->delB] = [1-D^2, D]


Output  [delA->out, delB->out] = [-D*Wa, Wb-D^2*Wa*FB]


Feed forward in->out = Wa*(1-D^2)


Feedback, delay A [delA->delA, delA->delB] = [-D, 1]


Feedback, delay B [delB->delA, delB->delB] = [FB*(1-D^2), FB*D]


I wrote out some equations to solve for the parameters and the first few pulses, and the results seem to match the impulse response.  Not sure how much I really trust its correctness, though...

---

### Post #593 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5780728&postcount=593>

I built a quick prototype to play with, it's a little sloppy but it implements everything but the tap weighting.  I used the FDN representation described above and it seems to have paid off- I have independent control over the input/output mixing, and this is a lot more flexible than the density parameter affecting everything.  I don't think my loop filter is authentic either, but it's usable and doesn't cause stability problems.  It isn't stable if I invert the density.


I've also added delay modulation (haven't tried the rotation matrix thing yet).  It's definitely pleasant but fairly different from the Lexicon 224 "Concert Hall" thing.  I think the notable part of the Concert Hall's nested APF modulation is that the signal circulates through it so many times that it comes out resembling narrow band noise rather than pitch modulation.  If the modulation is fairly fast, it doesn't sound detuned but it loses some clarity, especially in the treble range where the harmonics are closer together.  The Quantec algorithm already has some perceptible "motion" in the tail due to resonances beating against each other, modulation sort of enhances this.  And for percussive sounds where you'd ordinarily hear individual reflections, the modulation spreads them out a little.  Each resonator has reflections at  summed multiples of the delay times,  and each of these reflections is the sum of several "sub reflections" that arrive by different paths (i.e. delA->delB->delA versus delB->delA->delA).  Delay time modulation means that they don't line up perfectly, so that each reflection turns into a little mini-cluster that's different each time.   


The other thing I'm noticing is that (like the marketing suggests...) it's a quite versatile algorithm, usable at all different sizes.  Small sizes are definitely resonant, but in a not unpleasant way, sort of like tapping on a piano soundboard.  So it covers useful territory where most algorithms show flaws- small spaces, short decays.  Modulation is useful in all of these cases.


All of this comes with a pretty serious penalty, though.  It's really not efficient if everything has to be done 16 or 32 times.  That Lexicon Concert Hall algorithm  only needs 2 modulated delays and 2 loop filters.  CPU usage is very low (around 1 or 2% if I remember correctly).  The Quantec algorithm uses about 30% (inefficiently implemented on an old computer, but still...).  Scaling this one up or doing anything fancy very quickly requires substantial resources. 


I also tried the "mix the 4 outputs through independent modulation delays" thing I mentioned before.  It's not bad but far less exciting than I'd expected.  Panning the resonator outputs right and left rather than mixing them in or out of phase gives it a more "traditional" stereo reverb sound, but the apparent density is lower.  


I think that's all I have for now...

---

### Post #594 -- Page 20
**User:** mdroberts1243
**Info:** Joined: Aug 2010Posts: 2🎧 15 years | Posts: 2
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5787121&postcount=594>

Hi All,


   First post!


   This thread has been incredible... I've only begun to mine it, but have skimmed through most.  I'd love to see more on the process of 'tuning' a reverb... I suspect there must be some methodical approach.


   It has inspired me to code a reverb from scratch into my Spin FV-1 hardware... [Spin Semiconductor :: View topic - A Spin on the Dattorro Plate Reverb](http://www.spinsemi.com/forum/viewtopic.php?t=236) 

   I wanted to work from a documented algorithm so chose to do the Dattoro Plate Reverb and directly follow the block diagram from his paper that was posted earlier in the thread.  Great learning experience as it forced me to work around the short-form allpass and filter instructions built into the FV-1 in order to apply coefficients and build simple filters as per the paper.


   I think I've eliminated all the NooB coding errors and have a faithful version of the reverb in the paper, but there is a disturbing artifact that I wanted to get feedback on from the forum...


   It seems that even if you turn down/off the major 'tank' parameters you still get a very substantial 'tail' out of the reverb (I'm suspecting the allpasses in the tank, which are used to form part of the output signal).  This is disturbing because you get the feeling you can't get the 'room' small enough and the 'residual' tail is fairly harsh... I turn decay all the way down and damping all the way up so there can't be much in the way of global feedback happening in the tank!


   Is the nature of the output signal generation in this reverb causing this?  Is this a 'normal' thing? (Some of the VST plugins derived from Dattorro don't seem to exhibit this).  Is there a way to fix this and keep the character/architecture of the reverb?  Have I missed something in the paper and screwed up?


Thanks,

-mark.

---

### Post #595 -- Page 20
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5787282&postcount=595>

Quote: > Originally Posted bymdroberts1243➡️It seems that even if you turn down/off the major 'tank' parameters you still get a very substantial 'tail' out of the reverb (I'm suspecting the allpasses in the tank, which are used to form part of the output signal).  This is disturbing because you get the feeling you can't get the 'room' small enough and the 'residual' tail is fairly harsh... I turn decay all the way down and damping all the way up so there can't be much in the way of global feedback happening in the tank!Is the nature of the output signal generation in this reverb causing this?  Is this a 'normal' thing? (Some of the VST plugins derived from Dattorro don't seem to exhibit this).  Is there a way to fix this and keep the character/architecture of the reverb?  Have I missed something in the paper and screwed up?This is due to the fixed delay lengths that you have to use in the FV-1. Even with the decay turned down all the way, you still have several series allpasses and a few output taps. The overall delay of the output taps (before the first decay multiplier), and the decay that comes from the allpasses, create the impression of an acoustic space of a given size. 


The perceived size will probably be bigger than the overall output tap delay, as these have identical amplitudes in the Dattorro algorithm. This suggests a longer reverb that has been truncated - the perceptual clues that point to a big acoustic space contradict the relatively short impulse duration.


Two ways of dealing with this in the Dattorro Small Plate algorithm:


- Shape the output tap amplitude, such that they are decaying away at short decay times. Difficult to do on the FV-1. Plus, you still have the allpasses with their decay times.


- Use shorter or longer delay times to suggest acoustic spaces of different sizes. This is why the Lexicon reverbs had a Size parameter, which simply scaled all the delays within the algorithm. For the FV-1, you could either have several presets with the same algorithm and different delay scales, or use a variable frequency clock to change the sampling rate of the chip. Apparently you can clock the FV-1 anywhere between 16 KHz and 48 KHz without running into problems. The high frequency cutoff will change, but high frequencies are overrated in reverbs.

---

### Post #596 -- Page 20
**User:** mdroberts1243
**Info:** Joined: Aug 2010Posts: 2🎧 15 years | Posts: 2
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5787460&postcount=596>

Thanks Sean!


I like the reverb in the 'sweet' spot, so perhaps I will fix those values for decay and damping in the code and then find a couple of other interesting parameters to vary, like 'resonance' or something.


-mark.

---

### Post #597 -- Page 20
**User:** Antti H
**Info:** Joined: Sep 2010Posts: 408My Studio🎧 15 years | Posts: 408My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5807012&postcount=597>

Quote: > Originally Posted byseancostello➡️The perceived size will probably be bigger than the overall output tap delay, as these have identical amplitudes in the Dattorro algorithm. This suggests a longer reverb that has been truncated - the perceptual clues that point to a big acoustic space contradict the relatively short impulse duration.What mechanisms cause the perception of size in reverb?

Position of each individual reflection within the first X milliseconds?

Time until reflection density exceeds some value?

Time until energy within X msec window stops varying?


The published research seems to largely avoid answering this and usually resorts to vague handwaving about early reflections.

Quote: > Originally Posted byseancostello➡️Two ways of dealing with this in the Dattorro Small Plate algorithm:- Shape the output tap amplitude, such that they are decaying away at short decay times. Difficult to do on the FV-1. Plus, you still have the allpasses with their decay times.Couldn't you use EXP instruction to calculate the tap amplitudes based on decay time parameter? You'd only need an approximate value, so it shouldn't be that difficult to do.

Another way to fudge it might be to use more taps than necessary and switch / crossfade between sets. Somewhat analogous to the Depth parameter in Lexicon 224.

Quote: > Originally Posted byseancostello➡️- Use shorter or longer delay times to suggest acoustic spaces of different sizes. This is why the Lexicon reverbs had a Size parameter, which simply scaled all the delays within the algorithm.Did the uniform scaling apply even to short allpasses acting (mainly) as input diffusors? This sounds somewhat unintuitive to me although I haven't done more than rudimentary experiments with input diffusor scaling.

---

### Post #598 -- Page 20
**User:** Lukpio
**Info:** Joined: Sep 2005Posts: 151🎧 20 years | Posts: 151
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5808189&postcount=598>

Quote: > Originally Posted byAntti H➡️What mechanisms cause the perception of size in reverb?Position of each individual reflection within the first X milliseconds?Time until reflection density exceeds some value?Time until energy within X msec window stops varying?In my view the perception of size has nothing to do with early reflections, but with modal density. I'd look at the frequency domain rather than the time domain. It's mostly a matter of the lowest set of resonances, that is dependent on the time of the longest delays that recirculate.


Great thread!

---

### Post #599 -- Page 20
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5854378&postcount=599>

There were some interesting discussions earlier this week involving thoughts on pitch changes occurring within real life indoor venues.


I had for many years assumed that folks knew that the whole discussion of pitch changes actually occurring in real spaces was just marketing spin designed to cover the need for modulation in artificial reverb.


I was surprised to find that this assumption is not universally accepted to say the least. What is your take? Can we agree to debunk this myth?



-Casey

---

### Post #600 -- Page 20
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5855626&postcount=600>

Quote: > Originally Posted byCasey➡️marketing spinPun intended?  


I've only ever seen it accompanied by hand waving, with no actual estimation of the sort of air movement it would take for, say, 1 cent pitch fluctuation/detuning.


As much as we've gotten acclimated to synthetic reverb, you'd think people would be more receptive to "this doesn't actually model any acoustic process, but it sounds really super". Simulacrum stuff catches on pretty easily everywhere else, what with ubiquitous samples of DX7 Rhodes patches (an emulation of an emulation of an emulation), but reverb marketing still has to be uniquely opaque and hyperbolic.


---

## Page 21

---

### Post #601 -- Page 21
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5855794&postcount=601>

Even wind available in an outdoor venue can only cause amplitude changes. Still no pitch shift. It's mother natures big mixer!



-Casey

---

### Post #602 -- Page 21
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5855845&postcount=602>

I'd prefer to imagine that modulation simulates an extremely acrobatic performance.

---

### Post #603 -- Page 21
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5855913&postcount=603>

Quote: > Originally Posted byacreil➡️I'd prefer to imagine that modulation simulates an extremely acrobatic performance.Me too. heh



-Casey

---

### Post #604 -- Page 21
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5856131&postcount=604>

Waves bounce out of phase from walls, that is one issue that has some effect. And if you listen to sounds from a distance you hear modulations that are frequency dependant. 


A lot of the rooms/caves that sound more interesting/lush have not a simple rectagular shape. When working with three series of delays, mimicing the three dimensions of a room those irregulatities are not taken into account. Modulations can help to create those irregulaties, that gives us the better sounding rooms. Even when they have unwanted side effects like chorus/flanger modulations.


But I fully agree that the modulations in for example the 250/224 are extreme. That is one of the reasons why I added an alernative algo inside the new empty that has a lot less obvious chorus/phasing like modulation.

---

### Post #605 -- Page 21
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5859264&postcount=605>

Oh, speaking of modulation, does anyone have a favorite random modulator?


I found one that may be, if not ideal for reverb, at least useful for general purposes.  It's a bounded random walk.  The random value (corresponding to slope of the output) is updated at random intervals (Poisson process).  The random slope variable is a uniform distribution but can be messed around to have a minimum absolute slope or to favor motion in a specific direction.  This basically amounts to an oscillator with a random frequency centered around zero, and this can then be shaped to a triangle wave or quadrature sinusoids or whatever.  The additional control over the random distribution can reduce this to a standard fixed frequency oscillator, if desired.


The advantage is that total delay excursion amount, perceived pitch change (slope) and rate of change of modulation are all independently controllable.  So there can be shallow modulation that changes rapidly, yet slowly moves over a very wide range.  This opens the door to reverbs that subtly change character over time (this can be many  minutes as taps slowly "migrate" over a wide range).  I had half expected this to be a useless "10000 flavors of bad" scenario that just deviated from optimal tuning, but I think it's considerably better than that.  There may be better ideas out there, but this seems fairly useful, if somewhat obtuse to control.

---

### Post #606 -- Page 21
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5859309&postcount=606>

It all depends on what you want to modulate... 


Allpass depth, allpass lenght, feedback depth, reverb tank delays lenght,etc.


There are a lot of things that can be modulated and when done simultaniously simple triangle modulators can do a good job IMHO. But it is unpredicable to get good results.

---

### Post #607 -- Page 21
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5861972&postcount=607>

Quote: > Originally Posted byacreil➡️Oh, speaking of modulation, does anyone have a favorite random modulator?I found one that may be, if not ideal for reverb, at least useful for general purposes.  It's a bounded random walk.  The random value (corresponding to slope of the output) is updated at random intervals (Poisson process).  The random slope variable is a uniform distribution but can be messed around to have a minimum absolute slope or to favor motion in a specific direction.  This basically amounts to an oscillator with a random frequency centered around zero, and this can then be shaped to a triangle wave or quadrature sinusoids or whatever.  The additional control over the random distribution can reduce this to a standard fixed frequency oscillator, if desired.I came up with a really cool one for 'Voice of the Starship' and I'll share the concepts behind it.


Suppose you do a random walk, and every sample you flip the polarity of the random value- without that you have instant DC runaway, with flipping the sign bit of the thing what you have is immediate DC wander but it's pink noise. You have to manage the tendency to put in low frequencies and I didn't want to simply filter.


Suppose you take every hundredth, or fiftieth, or tenth sample, and when that sample comes, instead of flipping the sign bit, you make the sign bit be 'towards zero' whatever that is, and then resume flipping the next sample (or just override?). Then you have an artifact introduced which will pull the random noise towards the center, and it will act as a highpass- the artifact is the regularity of the override showing up, which will be audible against the more general pink noise.


Now instead of doing it regularly, do a residue sequence- quadratic, primitive root- something to give a pseudorandom distribution to the override samples. If you do that, you get what I made Voice of the Starship with. You can put in whatever residue sequence you want, and the frequency of overrides will give you the cutoff- and it's CPU efficient, and gives you your random walk that stays within confines. It's able to perfectly avoid unwanted low frequency events because the distribution to a residue sequence has regularity, just not uniformity- heard as a noise source it is a perfect found-sound generator from seashore to storm-winds to various environmental noises, with a very high degree of convincingness.


Totally my favorite random modulator  but then I always liked residue sequences...


Here, I'll attach a clip  I do need to add antialiasing as I just learned there's a near-Nyquist component I don't want...

---

### Post #608 -- Page 21
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5869382&postcount=608>

Quote: > Originally Posted bychrisj➡️Suppose you take every hundredth, or fiftieth, or tenth sample, and when that sample comes, instead of flipping the sign bit, you make the sign bit be 'towards zero' whatever that is, and then resume flipping the next sample (or just override?). Then you have an artifact introduced which will pull the random noise towards the center, and it will act as a highpass- the artifact is the regularity of the override showing up, which will be audible against the more general pink noise.How about waveshaping the "random walk" as if it was a sawtooth? i.e. make the range bipolar, get the absolute value, and scale and offset to get back in the desired range? If you use fixed point tricks, this is easy. Not that expensive in floating point, either.

---

### Post #609 -- Page 21
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5871101&postcount=609>

Acreil, Like this one?

[http://www.musicdsp.org/archive.php?classid=1#269](http://www.musicdsp.org/archive.php?classid=1#269)

---

### Post #610 -- Page 21
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5871254&postcount=610>

Quote: > Originally Posted byseancostello➡️How about waveshaping the "random walk" as if it was a sawtooth? i.e. make the range bipolar, get the absolute value, and scale and offset to get back in the desired range? If you use fixed point tricks, this is easy. Not that expensive in floating point, either.How would that sound? I'm not quite sure what you mean, but if it would sound different I'd love to hear it  what I like about mine is that it's another pseudorandom element getting involved, causing a characteristic sound texture that I like. If you have a different approach it would produce a different sound texture that might be just as good in another direction...

---

### Post #611 -- Page 21
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5871479&postcount=611>

Quote: > Originally Posted byFroombosch➡️Acreil, Like this one?http://www.musicdsp.org/archive.php?classid=1#269Not exactly, it looks like he's got an extra interpolation stage in there.  Mine amounts to a random (uniform or not) input driving a sawtooth oscillator (phasor~ in Pure Data).  The sawtooth takes care of the walking (integrator) and bounded output (wraps to [0,1]), a negative input just reverses the direction.  


I like that it can be made to either quickly change its slope while slowly traversing  its entire output range, or move in a "forward" direction at a random (or even constant) rate.  


(interesting aside: the piecewise linear equation I used to "bias" the random distribution without changing its range turned out to be exactly the same equation used in the Casio Phase Distortion synthesizers to warp the phase of the sine table readout into a pseudo-saw wave).

---

### Post #612 -- Page 21
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5873284&postcount=612>

Quote: > Originally Posted byacreil➡️(interesting aside: the piecewise linear equation I used to "bias" the random distribution without changing its range turned out to be exactly the same equation used in the Casio Phase Distortion synthesizers to warp the phase of the sine table readout into a pseudo-saw wave).Interesting .

---

### Post #613 -- Page 21
**User:** OurDarkness
**Info:** Joined: Feb 2008Posts: 5,060🎧 15 years | Posts: 5,060
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5888990&postcount=613>

This EMT-250 sounds super nice.


Is there a successful emulation of it in the Bricasti M7?


or Eventide H-8000FW? I am lazy to do a search.heh

---

### Post #614 -- Page 21
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5890084&postcount=614>

Quote: > Originally Posted byOurDarkness➡️This EMT-250 sounds super nice.Is there a successful emulation of it in the Bricasti M7?or Eventide H-8000FW? I am lazy to do a search.hehNot in the M7.


Didn't Barry just do one with UAD; What more could you ask for?



-Casey

---

### Post #615 -- Page 21
**User:** Coyoteous
**Info:** Joined: Aug 2006Posts: 4,297🎧 15 years | Posts: 4,297
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5890142&postcount=615>

Quote: > Originally Posted byCasey➡️Didn't Barry just do one with UAD; What more could you ask for?Native Mac RTAS.

---

### Post #616 -- Page 21
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5890145&postcount=616>

Quote: > Originally Posted byCoyoteous➡️Native Mac RTAS.Picky, Picky! True love would find a way. heh


Platform predilections have been nicely absent from this forum. Should we change this? Is this an important part of the discussion?



-Casey

---

### Post #617 -- Page 21
**User:** Coyoteous
**Info:** Joined: Aug 2006Posts: 4,297🎧 15 years | Posts: 4,297
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5890305&postcount=617>

[http://www.valhalladsp.com](http://www.valhalladsp.com)

---

### Post #618 -- Page 21
**User:** OurDarkness
**Info:** Joined: Feb 2008Posts: 5,060🎧 15 years | Posts: 5,060
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5890496&postcount=618>

Quote: > Originally Posted byCasey➡️Not in the M7.Didn't Barry just do one with UAD; What more could you ask for?-CaseyHi Casey.


Unfortunately, I don't have any UAD plugins. I have the H8000FW and a M3000. I remember someone did an emulation of it in the H8000FW but since I never had an EMT-250, I don't know how faithful the emulation is.


M7 is in my to buy-list! So, I thought if there's an EMT-250 in there, then so much the better. Maybe with ver 3.0? heh


Btw, this thread is awesome. I learnt so many things from it. You guys rock!stike

---

### Post #619 -- Page 21
**User:** RobJB06Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5891352&postcount=619>

Anyone know if UAD are planning a 224, 70 or 480L port for their DSP cards? Every since they announced they were collaborating with Harmon / Lexicon i assumed something like this must be in the pipeline...

Maybe Harmon said listen you can do some Lexicon ports after we sell our own Lexicon Native plugs and the PCM hardware for a while.....

Anyone got the scoop on this?

---

### Post #620 -- Page 21
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5898017&postcount=620>

Quote: > Originally Posted byOurDarkness➡️Hi Casey.Unfortunately, I don't have any UAD plugins. I have the H8000FW and a M3000. I remember someone did an emulation of it in the H8000FW but since I never had an EMT-250, I don't know how faithful the emulation is.M7 is in my to buy-list! So, I thought if there's an EMT-250 in there, then so much the better. Maybe with ver 3.0? hehBtw, this thread is awesome. I learnt so many things from it. You guys rock!stikeThere is a 250 algo based version for the H8k in my webshop ;-) It is not exactly the same, but it has simularities. 


Harrie

---

### Post #621 -- Page 21
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5909824&postcount=621>

Quote: > Originally Posted byCasey➡️Even wind available in an outdoor venue can only cause amplitude changes. Still no pitch shift. It's mother natures big mixer!I am presuming that the amplitude changes can be modeled by a random function at a given rate (i.e. a "slow" random function) modulating the amplitude of a signal. A few questions:


- Do the amplitude changes build up sidebands over time? In other words, with a fairly long decay of a windowed sine wave, will the end of the decay have higher levels of sidebands than the beginning of the decay?


- Are the amplitude changes consistent over frequency?


I don't know if anyone has answers for these questions, but I figure they are worth asking. Especially since I am sitting in a pretty boring class right now, and can't boot over to the Windows side of the computer to finish up some coding...

---

### Post #622 -- Page 21
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5909868&postcount=622>

Quote: > Originally Posted byseancostello➡️Do the amplitude changes build up sidebands over time?Only through random luck. IOW no, random is random.

Quote: > Originally Posted byseancostello➡️Are the amplitude changes consistent over frequency?No. Only that they will always be random.

Quote: > Originally Posted byseancostello➡️I don't know if anyone has answers for these questions...101: (interestingly there is a lot more of this relating to (reduction of) road noise, circa 1930)


Here is a bit of useful (and actually correct) internetalgia:


However, when a wind blows, it is re-tarded (you know Jules adults should be allowed to use the word "********" on your forum) at the surface--a sort of boundary layer effect--and increases in speed aloft. This is a wind shear, that can be expressed by a gradient dU/dy, where U is the wind speed and y is the height. A wavefront propagating with the wind will have its top inclined forward, so it will tend to return to the surface, while a wavefront propagating against the wind will be deflected upwards. This is a much better explanation of the fact that sounds can be heard better downwind than upwind.


 Let us consider the case of a horizontally stratified atmosphere with temperature and wind varying with altitude, and a plane wavefront propagating with its normal making an angle φ with the horizontal. Note that this is a different convention than we used above in considering the effect of temperature, where we used the convention familiar from optics. The wind U convects the wavefront, so that the rays are no longer normal to the wavefronts, but deviate slightly in the direction of the wind. Let the inclination of the ray with the horizontal be ψ. The Figure at the right shows how φ and ψ are related. We can use the fact that U is much less than c to simplify the formulas. We assume nothing regarding the magnitude of φ or ψ.


Our analysis is based on the constancy of the trace velocity on horizontal planes, as in the case of temperature, which the present analysis includes. This can be expressed in terms of the ray inclination, making it possible to trace the paths of rays, which are the directions of energy propagation. The result is quite simple, a quadratic equation for sec &psi, that reduces to our previous result if U = 0. We notice (with Rayleigh) that sec φ = 1 corresponds to the boundary for total reflection, and the constant in this case is just c' + U', where the primed quantities are the values at the height of total reflection. This means that rays originating at the ground, assuming U = 0 there, will return to the ground if their initial inclination is less than φ, where sec φ = (c' + U')/c. Therefore, winds high in the atmosphere do affect long-distance propagation of sound, as we have assumed earlier.


The radius of curvature of the rays can be found as shown in the Figure, assuming that c is constant. (If it is not, the algebra becomes much more difficult, but can be carried out in principle). The radius of curvature R reverses if the sign of the wind shear reverses, and, of course, when the direction of propagation changes. We have been cavalier with the signs here, but they can be worked out easily if you are bothered.



What class are you taking?



-Casey

---

### Post #623 -- Page 21
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5925237&postcount=623>

Quote: > Originally Posted byCasey➡️What class are you taking?Unfortunately, not a class that helps me understand what you wrote above.


Javascript. Brushing up on my web development skills, for when DSP work goes dry.

---

### Post #624 -- Page 21
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5925282&postcount=624>

Quote: > Originally Posted byseancostello➡️DSP work goes dry.In what universe? I'm working on 3 things at once right now. If you are bored, propose something that uses huge amounts of DSP (you know you want to) and maybe we can work something out. heh


Oh, and I didn't write the heavy stuff above; I just pulled it off the net. It's so great these days, most of the basics are already posted, so life becomes much more cut and paste. It is very efficient.



-Casey

---

### Post #625 -- Page 21
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5926220&postcount=625>

Quote: > Originally Posted byCasey➡️In what universe? I'm working on 3 things at once right now. If you are bored, propose something that uses huge amounts of DSP (you know you want to) and maybe we can work something out. hehGotta think about that for awhile. Back in my ADI days, I was able to get several hundred delay taps feeding a 16-delay FDN on a single Blackfin core. Figuring out how to fill 6 dual core Blackfins, and having the results be audibly significant (i.e. be worthy of the cycles used) - that is a challenge. 


The phrase "time varying velvet noise" comes to mind for some reason...

---

### Post #626 -- Page 21
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5939556&postcount=626>

Any of youse guys ever work on waveguide reverberation structures? I had created a reverb back in 1999 that had a scattering junction based upon equal impedence waveguides, but it wasn't really a waveguide reverb, as I just made a standard FDN using the scattering junction as the feedback matrix. A true waveguide reverb would use the bi-directional waveguides (i.e. a delay going in each direction). 


I am getting interested in the structures that have more than 1 scattering junction. These seem like they might be useful in emulating certain physical situations. These are also appealing as the Julius Smith / CCRMA patent lapsed a few years back...

---

### Post #627 -- Page 21
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5954133&postcount=627>

I haven't tried a "real" waveguide reverb, I've been under the impression that the actual physical feasibility of a resonator structure doesn't specifically impart any unique acoustic quality to the sound.  But maybe people just tend to favor non-physical FDNs because they can do "kinda sorta the same thing" more easily.


I think there's lots of room for interesting "acoustic resonator" type effects (at least analogous to sympathetic string resonance or instrument bodies, even if no attempt is made at realistic modeling), maybe these fit in somewhere between filter bank/formant effects and reverb.  I've gotten interesting results with Rocchesso's simple "Ball Within The Box" 3 delay FDN example.  Surely more sophisticated variations are possible, but I don't know if waveguides offer much sonically that less constrained FDNs don't.  It would make sense if you're out to model something specific, but it might be a difficult hypothesis to test otherwise...


Currently weirding out with FFT based reverb...

---

### Post #628 -- Page 21
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5956657&postcount=628>

Quote: > Originally Posted byCasey➡️However, when a wind blows, it is re-tarded (you know Jules adults should be allowed to use the word "********" on your forum) at the surface--a sort of boundary layer effect--and increases in speed aloft. This is a wind shear, that can be expressed by a gradient dU/dy, where U is the wind speed and y is the height. A wavefront propagating with the wind will have its top inclined forward, so it will tend to return to the surface, while a wavefront propagating against the wind will be deflected upwards. This is a much better explanation of the fact that sounds can be heard better downwind than upwind.Let us consider the case of a horizontally stratified atmosphere with temperature and wind varying with altitude, and a plane wavefront propagating with its normal making an angle φ with the horizontal. Note that this is a different convention than we used above in considering the effect of temperature, where we used the convention familiar from optics. The wind U convects the wavefront, so that the rays are no longer normal to the wavefronts, but deviate slightly in the direction of the wind. Let the inclination of the ray with the horizontal be ψ. The Figure at the right shows how φ and ψ are related. We can use the fact that U is much less than c to simplify the formulas. We assume nothing regarding the magnitude of φ or ψ.Our analysis is based on the constancy of the trace velocity on horizontal planes, as in the case of temperature, which the present analysis includes. This can be expressed in terms of the ray inclination, making it possible to trace the paths of rays, which are the directions of energy propagation. The result is quite simple, a quadratic equation for sec &psi, that reduces to our previous result if U = 0. We notice (with Rayleigh) that sec φ = 1 corresponds to the boundary for total reflection, and the constant in this case is just c' + U', where the primed quantities are the values at the height of total reflection. This means that rays originating at the ground, assuming U = 0 there, will return to the ground if their initial inclination is less than φ, where sec φ = (c' + U')/c. Therefore, winds high in the atmosphere do affect long-distance propagation of sound, as we have assumed earlier.The radius of curvature of the rays can be found as shown in the Figure, assuming that c is constant. (If it is not, the algebra becomes much more difficult, but can be carried out in principle). The radius of curvature R reverses if the sign of the wind shear reverses, and, of course, when the direction of propagation changes. We have been cavalier with the signs here, but they can be worked out easily if you are bothered.-CaseyAs far as I understand this:

The speed of the sound is influenced by the curves it makes because of the boundary layer effect. And normal wind is not constant, but flackering.


When the speed of sound varies depending on this effect, will not give it (small) pitch-changes??

---

### Post #629 -- Page 21
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5996162&postcount=629>

Quote: > Originally Posted byFroombosch➡️As far as I understand this:The speed of the sound is influenced by the curves it makes because of the boundary layer effect. And normal wind is not constant, but flackering.When the speed of sound varies depending on this effect, will not give it (small) pitch-changes??The speed of the sound is not influenced by it. If the **source** of the sound is moving, then a doppler effect can be created, or mach waves. A boundary layer may cause measurable and perhaps perceivable irregularities in the pitch change of the moving sound source (if that source is somehow caught in and affected by an amazingly huge boundary layer..). But that's all irrelevant in a musical context.

---

### Post #630 -- Page 21
**User:** Radardoug
**Info:** Joined: Oct 2009Posts: 2,048🎧 15 years | Posts: 2,048
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5999201&postcount=630>

Listen to a big p.a. from 400 m or so. You will hear phasing. So the variations in the air are causing differences. Especially bad on an orchestra doing an outdoor concert.


---

## Page 22

---

### Post #631 -- Page 22
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6000381&postcount=631>

Quote: > Originally Posted byRadardoug➡️Listen to a big p.a. from 400 m or so. You will hear phasing. So the variations in the air are causing differences. Especially bad on an orchestra doing an outdoor concert.Phasing is not pitch shifting and it's not variations in the air that cause it. The sound that reaches your ears from hundreds of meters away is significantly effected by reflections/echoes from many very different sources in many locations, and still, there is no pitch shifting/modulation in it.

---

### Post #632 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6001031&postcount=632>

I live in the country site with sometimes a festival in distances of more then 3-4 miles during the summertime. Atmospheric effects I hear are not only high and low frequencies loss and the gain modulations, but also (small) pitch changes. I am now looking back in my memory and have not measured the effect. I guess I have to wait and try to measure it next summer 


I do agree that the effect is very small compared to the modulations we have in 224,480, 250's.

---

### Post #633 -- Page 22
**User:** Radardoug
**Info:** Joined: Oct 2009Posts: 2,048🎧 15 years | Posts: 2,048
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6002127&postcount=633>

Quote: > Phasing is not pitch shifting and it's not variations in the air that  cause it. The sound that reaches your ears from hundreds of meters away  is significantly effected by reflections/echoes from many very different  sources in many locations, and still, there is no pitch  shifting/modulation in it.A couple of things. Perhaps you can advise what is causing the constant change in the phasing sound then. Also reflections and the like come from buildings etc that are not moving. They only contribute static effects.

In conditions of high wind these effects become more marked, and are observable as close to the source as 50 metres.

---

### Post #634 -- Page 22
**User:** Radardoug
**Info:** Joined: Oct 2009Posts: 2,048🎧 15 years | Posts: 2,048
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6002175&postcount=634>

From this site
[Calculator pitch change by temperature variation flute clarinet pipe organ calculate frequency tone pitch temperature woodwinds speed of sound speed amplitude level - sengpielaudio](http://www.sengpielaudio.com/calculator-pitchchange.htm)


Quote: > The influence of temperature on the pitch: The speed of sound in air and thus the pitch (frequency)of a note as a column of air of a certain length, is directly proportional to the square root of theabsolute temperature. The absolute temperature is the absolute zero temperature, which isminus 273.15°C. The unit is Kelvin (K); 1 K has the same size as 1°C.Example:The frequency change by the increase in temperature of ϑ 1 = 20°C to ϑ 2 = 24°C is the squareroot of [(273 + 24 = 297 K) / (273 + 20 = 293 K)]1.0069028 ...Therefore, an increased frequency of 440 Hz at 20 C (440 Hz x 1.0069028)443 Hz at 24 ° C.It should be noted that the temperature of the air inside the wind instrument is rather complex.It is between the temperature of the room and the body of the player and by the instrumentheating the tone pitch rises.Is this guy right? Can you hear 3 Hz at 440 Hz? I know I can.

---

### Post #635 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6002560&postcount=635>

Temperature gradients in rooms are in that area. Interesting link

---

### Post #636 -- Page 22
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6002592&postcount=636>

Quote: > Originally Posted byRadardoug➡️From this siteCalculator pitch change by temperature variation flute clarinet pipe organ calculate frequency tone pitch temperature woodwinds speed of sound speed amplitude level - sengpielaudioIs this guy right? Can you hear 3 Hz at 440 Hz? I know I can.This is for columns of air vibrating in a wind instrument, not for the perception of that sound after it leaves the instrument.

---

### Post #637 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6002648&postcount=637>

IMHO this goes deeper. Temperature gradients in rooms can be as high as 2-4 degrees and with large rooms even a lot higher. This means that the speed of sound of reflections is dependent of the hight of these reflections in the room. This could give ideas on why small amounts of pitch-modulations sounds sometimes more realistic then without them.

---

### Post #638 -- Page 22
**User:** Coyoteous
**Info:** Joined: Aug 2006Posts: 4,297🎧 15 years | Posts: 4,297
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6004114&postcount=638>

Reverb fight!

[KVR: Oversampling MVerb](http://www.kvraudio.com/forum/viewtopic.php?t=302405)


Just kidding, interesting read though.

---

### Post #639 -- Page 22
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6010473&postcount=639>

Quote: > Originally Posted byCoyoteous➡️Reverb fight!KVR: Oversampling MVerbJust kidding, interesting read though.I sure hope it doesn't come across as a fight, as that is certainly not my intent. Just different approaches towards getting a "colorless" reverb response, and different views of how much noise is too much in a reverb. Andrew always seems to have interesting things to say in his forum posts.

---

### Post #640 -- Page 22
**User:** Coyoteous
**Info:** Joined: Aug 2006Posts: 4,297🎧 15 years | Posts: 4,297
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6010658&postcount=640>

Quote: > Originally Posted byseancostello➡️I sure hope it doesn't come across as a fight, as that is certainly not my intent. Just different approaches towards getting a "colorless" reverb response, and different views of how much noise is too much in a reverb. Andrew always seems to have interesting things to say in his forum posts.No, it just struck me as the moment to be the kid that runs in from the playground to declare a scuffle, or a physics student spotting a Bohr vs. Einstein debate, though probably somewhere in between. I just don't think yelling "reverb discussion" in even this not-so-crowded special interest room would get much attention.

---

### Post #641 -- Page 22
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6011360&postcount=641>

Quote: > Originally Posted byCoyoteous➡️I just don't think yelling "reverb discussion" in even this not-so-crowded special interest room would get much attention.Maybe not in a special interest room, but try a Concert Hall.

---

### Post #642 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6011456&postcount=642>

or a room with reversed crystals...

---

### Post #643 -- Page 22
**User:** Coyoteous
**Info:** Joined: Aug 2006Posts: 4,297🎧 15 years | Posts: 4,297
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6011836&postcount=643>

I've just about quit using smilies, but sometimes there is no substitute. :-)

---

### Post #644 -- Page 22
**User:** Andrew Souter
**Info:** Joined: Mar 2009Posts: 832🎧 15 years | Posts: 832
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6020422&postcount=644>

Quote: > Originally Posted byseancostello➡️I sure hope it doesn't come across as a fight, as that is certainly not my intent. Just different approaches towards getting a "colorless" reverb response, and different views of how much noise is too much in a reverb.Ya, exactly.  Not a fight.  If everyone did exactly the same thing, why would there be a need for different companies in the market, right? thumbsup


Quote: > Originally Posted byseancostello➡️Andrew always seems to have interesting things to say in his forum posts.Thanks.  I try. heh

---

### Post #645 -- Page 22
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6040231&postcount=645>

I put up a moderately geeky blog post about the history of ValhallaShimmer:

[ValhallaShimmer: a bit of history « The Halls of Valhalla](http://valhalladsp.wordpress.com/2010/11/23/valhallashimmer-a-bit-of-history/)


My goal was to keep things high level, but of course I start yammering about Schroeder and the Central Limit Theorem. I do try to cover some of the creative concepts behind the plugin, with the main idea being to embrace DSP artifacts.

---

### Post #646 -- Page 22
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6135786&postcount=646>

Hi subculture folks,


In case you haven't seen it, here is a thread about hardware versus software that gets some of the "heavy hitters" involved:

[Lexicon: Hardware vs. Software](https://gearspace.com/board/high-end/560224-lexicon-hardware-vs-software.html)


I hope that the holidays are finding you and your loved ones well.

---

### Post #647 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6136350&postcount=647>

Thanks fot pointing out that thread. The subculture guys are all over the place now ....

---

### Post #648 -- Page 22
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6137683&postcount=648>

Comparison between S777 and Reverberate with the exact same IR's :

[S777 Medium Hall B.wav](https://gearspace.com/board/attachments/geekzone/210339d1293004161-reverb-subculture-s777-medium-hall-b.wav?s=2bd1dfff49c5a55ff164fe6c1d6d8042)
[Reverberate Medium Hall B.wav](https://gearspace.com/board/attachments/geekzone/210340d1293004161-reverb-subculture-reverberate-medium-hall-b.wav?s=2bd1dfff49c5a55ff164fe6c1d6d8042)

---

### Post #649 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6137728&postcount=649>

Quote: > Originally Posted byWarp69➡️Comparison between S777 and Reverberate with the exact same IR's :Attachment 210339Attachment 210340That is a HUGE difference even with a forgiving sound and listening on my iPOD ears.

---

### Post #650 -- Page 22
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6137839&postcount=650>

It take it that these are supposed to be without any additional enhancements.  It might be interesting to actually measure the impulse responses of these to see if they're doing what they're supposed to be doing, or to compare with brute force time domain convolution.

---

### Post #651 -- Page 22
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6137864&postcount=651>

The difference between the files (i.e. invert one and sum) is down 29 dB (comparing peak values).  But curiously they're already aligned to the sample.  Am I not the first to try this?

---

### Post #652 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6138229&postcount=652>

The differences are so HUGE that I did not (felt the need to) try the sum and inversing trick. They sound totally different on a forgiving source. I guess that using a snare or percussion will probably enhance the difference in soundstage even more.

---

### Post #653 -- Page 22
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6152520&postcount=653>

Quote: > Originally Posted byCasey➡️There were some interesting discussions earlier this week involving thoughts on pitch changes occurring within real life indoor venues.I had for many years assumed that folks knew that the whole discussion of pitch changes actually occurring in real spaces was just marketing spin designed to cover the need for modulation in artificial reverb.I was surprised to find that this assumption is not universally accepted to say the least. What is your take? Can we agree to debunk this myth?-CaseyIt would be nice to see a discussion on this subject.


  I re-read Dr. Blesser's AES paper: "An Interdisciplinary Synthesis of Reverberation Viewpoints" (JAES Vol. 49 No. 10) and in section 1.3 ("Intractable Measurements") he discusses the effect on arrival times of convection movements in thermal layers, noting that measurements would need to be averaged over an hour or more ( "Thermo-dynamic equilibrium to within a fraction of a degree is not possible.").  Though this section is primarily concerned with frequency dependent arrival time differences due to convection currents (i.e. phase modulation).  


A related paper of interest, by David Griesinger, discusses the psycho-acoustic phenomenon of distance perception as a function of pitch uncertainty: ["Pitch Coherence as a Measure of Apparent Distance and Sound Quality in Performance Spaces"](http://www.davidgriesinger.com/pitch3.doc).


-CZ

---

### Post #654 -- Page 22
**User:** Friedemann
**Info:** Joined: Sep 2006Posts: 1,244🎧 15 years | Posts: 1,244
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6153668&postcount=654>

Quote: > Originally Posted byFroombosch➡️That is a HUGE difference even with a forgiving sound and listening on my iPOD ears.I´m on headphones with my built in laptop soundcard, but I did the foobar ABX and I couldn´t tell them apart. Probability that I guessed: 65%. Huge?

---

### Post #655 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6158891&postcount=655>

Take a listen on your studio monitors, if you can not hear the difference on your laptop. I was amazed I could tell them apart so easy on my iPod ears. In my studio there is a bigger difference, but that is easy on a high rezz monitor system. There is a difference in richness of the decay.

---

### Post #656 -- Page 22
**User:** meloco_go
**Info:** Joined: Nov 2008Posts: 394🎧 15 years | Posts: 394
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6159862&postcount=656>

Quote: > Originally Posted byFriedemann➡️I´m on headphones with my built in laptop soundcard, but I did the foobar ABX and I couldn´t tell them apart. Probability that I guessed: 65%. Huge?You know, once I downloaded the files I tried ABX testing — couldn't pass the test (winABX). After a while I came back, listened more closely and spotted things which change between files. Scored 9/10.

Once you hear the difference it won't go away.

To me, with reverberate, the reverb image sounds kinda detached from the source, like a doubletrack, 777 OTOH sounds like it's glued.

Not sure one is better than another. It might be that dry/wet mix was set differently?


And it's no wonder that Froombosch being reverb designer himself (if I'm not mistaken) picks such differences immediately!


Also a good lesson on what ABX is really is! If you don't hear a difference it just means that **you**  don't hear a difference on **this** moment.

---

### Post #657 -- Page 22
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6246303&postcount=657>

Hi all,


Dropping some reverb science about allpass filters and the ubiquitous Diffusion control:

[Reverbs: Diffusion, allpass delays, and metallic artifacts « The Halls of Valhalla](http://valhalladsp.wordpress.com/2011/01/21/reverbs-diffusion-allpass-delays-and-metallic-artifacts/)

---

### Post #658 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6254764&postcount=658>

Interesting post. I guess this information is really interesting for the users of reverbs with diffusion control. It should be part of a manual, as is important to know. Most manuals are puzzles.

---

### Post #659 -- Page 22
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6255388&postcount=659>

Quick hypothetical question: if I were to analyze the Alesis Quadraverb and Ibanez SDR-1000 algorithms in moderate  but not exacting detail, would that be of interest here or just a total waste of time?  This would include topology, delay lengths, parameter mappings (i.e. at least as much detail as the Dattorro algorithms) but not an exhaustive examination of loop filters or coefficients at specific decay times, etc.

---

### Post #660 -- Page 22
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6255500&postcount=660>

IMHO a waste of time. I had those and did not like the sound of them at all. I know they had their fans and an amazing price/quality ratio in that period.  But it personally would not interest me...

