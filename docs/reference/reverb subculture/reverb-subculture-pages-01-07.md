# Reverb Subculture -- Gearspace GeekZone Thread

**Thread URL:** https://gearspace.com/board/geekzone/380233-reverb-subculture.html
**Forum:** GeekZone @ Gearspace
**Total Pages:** 36 (~1,059 posts)
**Started:** 8th April 2009

A legendary technical thread on algorithmic reverb design, DSP implementation, and digital audio effects. Features contributions from professional reverb designers including Casey (Bricasti), Sean Costello (ValhallaDSP), and many DIY builders.

---

## Page 1

---

### Post #1 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4074137&postcount=1>

**Reverb Subculture**

Reverbs and other DSP stuff.... moved?

The thread on high-end was very interesting but probably should be here....

To answer an earlier question about SDRAM... I (and most DIY DSP'ers) are often 'stuck with' some sort of DSP that might not be ideal. I picked the Freescale DSP's because of the development tool costs of the TI and ADI parts. I'm sorry but a DIY'er can't justify several thousand dollars for a functioning development suite, and we normally can't finish a project in the 30-day eval period. So that limits the part choices quite a bit. Also, VLIW architectures do not lend themselves to assembly coding without the optimizers and schedulers. So what DSP to do a DIY 'verb with?

My first choice (not the best choice - but perhaps the simplest choice) was the Wavefront AL3201 - a picoverb on a chip. But you can code a lot of allpasses, if you want fifty allpasses in sequence, that's not a problem. It's a bit short on memory - only 32k samples. But it was a simple chip to learn about reverbs and other effects on.

My next choice was the DSP56366 which seems pretty good, and development tools (gcc) are free. I just use the assembler portion of it. But that DSP supports EDO DRAM but not SDRAM. Then I started looking at SDRAM controllers, and that opened up a can of worms - you can't just buy an SDRAM controller. You can, however, get a SDRAM controller IP core for an FPGA.

I don't like the overhead of round-robin delay lines - it's an extra few clock cycles per allpass or delay. Maybe I could build the round-robin delay lines into the FPGA with the SDRAM controller as well. Well, now that I've committed to put on an FPGA and incorporate an address generation unit, why don't I just build a effects-oriented DSP on an FPGA? I don't need that many instructions, how hard could it be?

---

### Post #2 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4074247&postcount=2>

Very nice, thanks for starting this thread!

Dale, I think you are on the money with FPGAs. I think that is the future of DSP, and a great choice for DIY. But today AD DSP still has a significant edge in cost per internal memory and computational performance. Then you have to also consider the awesome power of an Intel processor.

So, I think there are many implementation strategies that are going to appeal to different folks in different situations. It might be interesting to abstract out specific implementations initially and take a look at the basic reverb building blocks. Move on to overall reverb structures, and then see how they might map onto specific implementation strategies. What do you think?

-Casey

---

### Post #3 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4074832&postcount=3>

> Originally Posted by **Casey**:
> Dale, I think you are on the money with FPGAs. I think that is the future of DSP, and a great choice for DIY. But today AD DSP still has a significant edge in cost per internal memory and computational performance. Then you have to also consider the awesome power of an Intel processor.
>
> So, I think there are many implementation strategies that are going to appeal to different folks in different situations. It might be interesting to abstract out specific implementations initially and take a look at the basic reverb building blocks. Move on to overall reverb structures, and then see how they might map onto specific implementation strategies. What do you think?

Here's what I've been thinking:

A lot of building blocks of reverbs are pretty hush-hush, and for good reason. Some are relatively public - Schroeder, Jot, Gerzon, Gardner. A common trend seems to be needing allpasses, combs, and relatively low-Q filters (6dB). And a delay line is pretty much used for all of them, though a filter only needs a single delay and could be done outside of a delay line structure.

Since I've worked with the AL3201, and since I've also repaired PCM70's and 60's and even a couple of newer units, I have a pretty good idea how the memory management works there - identical to the AL3201. So why not make the DSP just have a sample counter that decrements once each sample and add that to the offset? An adder in an FPGA is pretty quick. I need to present an address to the adder, and it does the delay line roundabout for me. I would need to have a separate path available to do chorus functions for other effects - and to break up modes in some of the allpass loops.

The second thing is what kind of memory. I like SRAM, but SDRAM is cheaper for the same amount of memory - by far. Looking at SDRAM, interleaving would be nice. If the design has started by being a super AL3201, doing four parallel threads would be good. That means that I need to have at least four accumulators. The RAM timing looks good for interleaving, I can keep the data bus at 100% for SDR SDRAM. But I need four threads and four accumulators.

At some point you need to pick the part. So I looked at the Xilinx Spartan-3E. It has fixed dual-port RAM blocks (good to store the program, and also for a register file), and also 18x18 signed multipliers - a few of them. Excellent. A rough drawing of a data flow diagram and distribution of the multipliers indicates that an allpass can be done in two cycles:

```
r0 += k1 * (r1 = mem<tail>)
mem<head> = r0 ; r1 = -k * r0
```

Similarly, a one-cycle low-pass filter would be trivial:
```
r3 = k1 * mem<input> + (1-k1) * r3
```

One more line makes a high-pass. With a 256-sample register file, that's a lot of filters.

And a multitapped delay is obvious...

```
mem<head> = r0
r1 = k1 * mem<addr1>
r1 += k2 * mem<addr2>
r1 += k3 * mem<addr3>
io<dacl> = r1
```

That looks good. To generate the chorus waveforms, another ALU could be used, or since the chorus waveforms are pretty slow-changing, a soft processor can be put on the FPGA to do it - there are some 32-bit ones, and a couple of 8-bits. There's an 8051 and a Z80 for the 8-bit ones. I like the Z80 since the last job I worked at used them for just about everything (actually, the Z80181). But the 8051 isn't too bad either. It just has to generate some LFO coefficients so it'll be loafing, anyways. Probably I'll pick the one that takes fewer gates.

Anyways, that was my line of thinking. I would have liked the AL3201 chip better if it had two serial audio ports and double the RAM. Then I would just build an array of them. This seems pretty good to me - a familiar design method (sample-by-sample), an architecture that is already familiar to me (the AL3201), a fair bit of performance (around 40 MIPS with 8-bit SDRAM, 80 with 16-bit SDRAM), and an effects-centred instruction set. The cost should be pretty low - around $20 for the FPGA plus SDRAM in single-piece quantities.

I know of one other company that has done DSP with an FPGA. International Rectifier did a control chip for motor drives that was originally an FPGA then was changed to a hard-programmed gate array later in the development. It's a nice part - does all of the PID's and PWM's and encoder interfaces that you need to build a variable frequency drive... IRMCK301/303.

-Dale

---

### Post #4 -- Page 1
**User:** audioawake
**Info:** Registered User | Joined: Jun 2007 | Posts: 96
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4074884&postcount=4>

Wow that's a great thread

I have one question, that google couldn't answer: what would be algorithmic interpretation of all-pass filter? I mean y[k]=x*....

And another one is how to interpret those z-1 in filter transfer functions?

I'm a newbie so I'm sorry if it's a stupid question. Thanks in advance

---

### Post #5 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4075791&postcount=5>

In a sample-by-sample processor, probably it is most efficient to be implemented as a lattice structure:

[Harmony Central - Digital Allpass Filter](http://www.harmony-central.com/Effects/Articles/Reverb/allpass.html)

I can't speak for any professional reverb implementer, but after spending a bunch of time with the block diagrams of the Schroeder reverberators and my 'DSP for Dummies book' and the AL3201 programmer's guide, the lattice seems to be the easiest way to do it. In AL3201 assembler, it looks like this:

```
MEM diff 48
RAPB diff' k=-0.726
WBP diff k=0.726
```

and takes two clock cycles (or 325 nanoseconds).

The first instruction reads the end of the delay line, stores that value in B (a temporary register), and also takes that value times -0.726 and adds it to the accumulator. Note that the accumulator holds the input.

The second instruction stores the result from the previous multiply into the start of the allpass delay line, and takes the output of the delay line (that was in the B register), and adds the result of the first instruction times 0.726 to that, and the output is now in the accumulator.

If you are cascading allpasses, then you do this:

```
MEM diff1 48
MEM diff2 109
RAPB diff1' k=-0.726
WBP diff1 k=0.726
RAPB diff2' k=-0.726
WBP diff2 k=0.726
```

And if you want a time delay in between, you can do this:

```
MEM diff1 48
MEM diff2 109
MEM dly1 960

RZP ADCL k=0.5   ' read input registers
RZP ADCR k=0.5
RAPB diff1' k=-0.726
WBP diff1 k=0.726
WZP dly1
RZPB dly1'
RBPB diff2' k=-0.726
WBP diff2 k=0.726
```

and then to mix in a little of in between the allpasses into the output you can add to the end:

```
RAP dly1" k=-0.15
WAP DACL k=0     ' write to output
```

This line takes the halfway point between the two allpasses and adds it to the output of the allpass - then sends it to the D-A converter. In terms of a simple reverberator, what this does is take the first early reflections (allpass 1), runs that through a predelay (dly1), then the later reverberator (allpass 2), and sum a bit of the earlier reflections to the output of the second allpass. This reverb will sound awful, but you get the idea. You need to add some filtering... a first-order lag filter after an allpass will look like this:

```
RBPB diff3' k=-0.726
WBP diff3 k=0.726
WAP dummy k=0.750
RAP dly3+1 k=0.250
WAP dly3 k=0
```

You can have fun cascading and summing allpasses, filters, combs (which are an allpass with not identical coefficients), delays, and multiple delay taps. Most of the time you get something that sounds awful (except maybe for a sci-fi special effect), but sometimes you get something useful. You can implement a Schroeder reverb quite easily. Although it doesn't sound excellent, it does sound ok. Adding more stages can smooth it out.

Sometimes a creation you make sounds awful but if you know where it rings, you can add a chorus to that allpass to break that up, or you can retune the delay line lengths to move the ringing where it is pretty even. Doing reverb development this way (what I call the 'crash and burn' software development method) is time consuming. It would be far better to implement the algorithm using 'C' or Java or Fortran or something like that, listen to it on a PC, then once it's working, write it for the DSP you're using.

Even though allpasses are nominally flat, they still can 'ring' since in a reverberator, allpasses are usually relatively long and on an impulse you can hear ringing as 'bunching' of the impulses when you look at it in the time domain. If it 'bunches' on an impulse, it will ring when you put audio through it. Another bad artifact is 'repetition' - where you hear a repeating 'tape loop' pattern in the reverb tail. From what I can tell, it means that you have too much long allpass and not enough short allpass.

An interesting thing about the lattice implementation of an allpass is that the audio signal within the allpass is useable, too, where in the middle of a comb filter or probably another allpass implementation it may not be.

A 'z' is a unit delay, if I run the AL3201 at its nominal design frequency (48 kHz sample rate), then a z-1 is 20.8 microseconds, or z-48 is one millisecond. I've occasionally seen the delays specified in milliseconds, too.

The 'crash and burn' software method is an oldie but a goodie. You try running your box (whether it's a reverb or a mobile data terminal or whatever), and when it crashes, you pull out the EPROM chip and burn another one. I'm sure the reverb developers here have been through it. I picked the AL3201 to show the code since it is a very reverb-centered instruction set and it is pretty easy to understand how it works.

Now, Casey will probably correct me on a bunch of points, but that's what I've learned so far.

---

### Post #6 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4075884&postcount=6>

Great stuff Dale.

Could I talk you into using easier to read notation? I'm not familiar with the part you are using or the assembler instructions. But hey, no complaints, you are really laying a lot out there!

One point on allpasses that I'm sure you are aware of, but is worth mentioning, is their behavior when looking at group delay (or phase) vs. frequency.

Because an allpass filter will delay some frequencies more than others, the frequencies which are delayed longer stick around until the end of the tail, while the other frequencies that are delayed for a shorter time through the allpass fade out before the tail has completed.

This is particularly true when the same signal is passed over and over again through the same allpass, (like in a loop!), because the delayed frequencies compound over time.

What this sounds like is a "metalic" finish to the tail.

The best way to hear this is to excite the entire loop with white noise (all frequencies) then stop the white noise and listen to the tail. You will hear a strong correlation between the size and gain of the allpass filters and the amount and character of the metalic finish to the tail.

One word of warning. White noise is potent stuff, don't sit all day tweaking with white noise if you don't want to hear your ears ringing when you go to bed that night!

-Casey

---

### Post #7 -- Page 1
**User:** audioawake
**Info:** Registered User | Joined: Jun 2007 | Posts: 96
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4075917&postcount=7>

Thank you very much dale116dot7!

> Originally Posted by **Casey**:
> This is particularly true when the same signal is passed over and over again through the same allpass, (like in a loop!), because the delayed frequencies compound over time.

How about a little randomization in filters phase response, if it's even possible with all-pass filters in general?

---

### Post #8 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 8th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4075957&postcount=8>

> Originally Posted by **audioawake**:
> How about a little randomization in filters phase response, if it's even possible with all-pass filters in general?

Oh yes, certainly.

-Casey

---

### Post #9 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4076656&postcount=9>

I just cut+pasted from my source code. What the allpass is doing is (in 'C') is:

```c
float diff1[48];
float input;
float output;
float k=0.725;

diff1[0] = input + k * diff1[47];
output = -k * diff1[0] + diff1[47];
```

Where diff1 is a simple delay line. Somewhere else is located essentially this:
```c
for(c=47;c!=0;c--)
    diff1[c]=diff1[c-1];
```

This would be inefficient. You just don't do a delay line by copying all of the data one spot over in memory. That is about as (in)efficient as convolution. It just demonstrates how it works.

If 'k' is set to zero, you get a simple delay line. If it's set at 1 or higher, you get an oscillator. Practically, values between 0.25 and 0.75 or maybe 0.85 are useful.

In practice you would do the delay by decrementing an address (in 'C' they call it a pointer, in a real language it's an address) every sample, if you're doing a sample-at-a-time algorithm. Some reverbs (the TC M5000, the K-T DN780, the Alesis units, and probably a lot more) do the sample shifting in hardware by messing with the address sent to memory.

For hardware archeologists, the K-T DN780 is actually a pretty good 'by the book' example of an older reverb-specific processor using no custom IC's (except for a couple of bipolar PROM's), and the service manual is available for examination of the DSP hardware. If you're looking, IC29-34, IC36, and IC38 on the DSP board form the address 'mangler'. IC36 and IC38 make up a 16-bit counter, the remainder of those chips are a 16-bit adder. If you're not a hardware geek, then don't worry about this. If you are a hardware geek either you already knew how it was done, or you do now.

-Dale

---

### Post #10 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4077147&postcount=10>

So Dale, thanks for converting to C! Much more clear.

Leaving allpass filters aside for a moment;

When looking at the entirety of an interesting reverb loop(s), it is important to identify which elements represent feed back paths and which elements represent feed forward paths.

Each path will have a specific frequency response, and a gain which will determine how close to being flat in the frequency domain the element is. Typically, flatter is better. Typically, frequency peaks that are fat and round will sound better than those which are more needle like.

This understanding can give some insight into the behavior of a reverb of any topology, increasing the predictive nature of the design process and reducing the required amount of trial and error.

Of course reverb topologies are defined by many characteristics, but the purposeful decisions made as to how feed back and feed forward paths are used is a good place to start any design from.

-Casey

---

### Post #11 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4077345&postcount=11>

I haven't really thought about that so much. But perhaps implementing an algorithm in C, then playing noise through it (input in a raw audio file format, same with output), then doing a spectrum or waterfall plot of that file - would that be a good approach?

And if there's a peak, can one put a 'snooper' to find the offending path? For example, write the 'output' audio files, but also a few files at selected points? I suppose once the algorithm is written and tested in C, it can be ported into a DSP box either by direct compiling, or hand compiling into assembler.

I just finished up a reverb algorithm (on the AL3201) that is just somewhere around 45 or so allpasses in series. It has a bit of a ring, and a very slow buildup. So I took taps from the first 20 allpasses using sloped tap coefficients with pseudo-random signs, and sum that to the output. That improved the buildup - without it the buildup is rather unnatural. The only thing is that it dies out unnaturally, so some feedback should help, but I've been afraid to try that due to ringing. It sounds kind of like a gated and inverse reverb combined, actually.

---

### Post #12 -- Page 1
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4078420&postcount=12>

> Originally Posted by **Casey**:
> One point on allpasses that I'm sure you are aware of, but is worth mentioning, is their behavior when looking at group delay (or phase) vs. frequency.
>
> Because an allpass filter will delay some frequencies more than others, the frequencies which are delayed longer stick around until the end of the tail, while the other frequencies that are delayed for a shorter time through the allpass fade out before the tail has completed.

Barry Blesser has a recent patent that addresses this issue. Blesser introduces a filter type called "notchpass," where the group delay peaks are matched to corresponding minimums in the frequency response. In the feedback loop of a comb filter, the result is a reduction or elimination of the metallic sounding frequencies sticking around.

I haven't tried this, as I first read about it in an issued patent, and it was not in any prior art that I know of. I tend to deal with these allpass issues by reducing the coefficients to lower levels, by randomizing things over time, or by not using allpasses.

Sean

---

### Post #13 -- Page 1
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4078469&postcount=13>

> Originally Posted by **Casey**:
> Dale, I think you are on the money with FPGAs. I think that is the future of DSP, and a great choice for DIY. But today AD DSP still has a significant edge in cost per internal memory and computational performance. Then you have to also consider the awesome power of an Intel processor.

One possibility is using the Linux tools for the Blackfin DSP:

[Blackfin Koop](http://blackfin.uclinux.org/gf/)

Free compilers, instead of $4K. The development board is very low cost as well, and schematics are available for it. I am not sure how efficient the compiler is, but you might be able to rip some useful render loops out of the source code for VisualAudio:

[VisualAudio 2.6 Audio Software Development Tools and Libraries | Blackfin Processors | Analog Devices](http://www.analog.com/en/embedded-processing-dsp/blackfin/content/visualaudio_software_tool/fca.html)

The modules assume block based processing, which will work well with cache based systems and SDRAM access. It would obviously be a fair amount of work to extract the useful code, but easier than creating audio modules from scratch, especially since there is a fair amount of hand-tweaked inner loops in there.

Another possibility, which you had suggested, is to use an FPGA for your memory management, and have a DSP hook up to this. In such a situation, the FPGA would deal with grabbing groups of samples out of the SDRAM, as well as the circular buffering. I'm not that versed in FPGAs (or the hardware side of embedded designs, for that matter), so I don't know how this would work, but it is an idea to toss out there. I think that Al Clark of Danville Signal Processing has implemented such a SDRAM controller using an FPGA on one of his SHARC development boards.

> Originally Posted by **dale116dot7**:
> I just finished up a reverb algorithm (on the AL3201) that is just somewhere around 45 or so allpasses in series. It has a bit of a ring, and a very slow buildup.

I view this as the central limit theorem in action. If you have enough of any filtering block in series, the impulse response ends up looking like a Gaussian bell curve. This can be annoying or useful, depending on the application.

> Originally Posted by **dale116dot7**:
> So I took taps from the first 20 allpasses using sloped tap coefficients with pseudo-random signs, and sum that to the output. That improved the buildup - without it the buildup is rather unnatural.

About 9 years ago, my coworker and I were working on an implementation of the "Dattorro" reverb for a client. To save cycles, we ripped the taps out of the network, and just took the outputs from the existing delay lines. The result had very lumpy attack characteristics. My theory is that the output taps in allpass loop reverbs are used to eliminate the buildup issues that occur with a bunch of allpasses in series, as well as to add echo density during the attack phase.

A few of the older plugin reverbs (Silververb for Logic, some other reverb found in Arboretum's HyperPrism) consisted of a bunch of allpasses in a comb filter loop, with the output taken from the end. The resulting sound had a definite buildup in the attack.

Sean

---

### Post #14 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4078600&postcount=14>

OK, maybe this can be fun.

Let's build a simple little reverb from scratch, while thinking about some of the issues already mentioned.

Let's start with a modest 16k samples for our entire reverb section.

Divide those samples up into three unequal loops.

Three is nice because we can think of these loops as the 3 dimensions of a room and we can use a tool like this [RealTraps - ModeCalc](http://www.realtraps.com/modecalc.htm) to look at how we might size the loops to achieve the flattest response (or fewest modes anyway).

Then just put an output tap in the middle of each loop (for now). And a gain element at the end of each loop to reduce the energy in the loops over time.

Send signal into the loops identically, and sum the 3 taps for the output.

OK so this is 3 feedback elements (the loops), and 3 feedforward elements (the tapped delay lines.)

This is just a start, it won't sound great but it gives a lot of material for gaining some intuition over the basic elements.

You will find that the sound is adjusted by changing the size of the loops and adjusting the gains at the end of the loops.

-Casey

---

### Post #15 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 9th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4079095&postcount=15>

Ok, I'll try that sometime this weekend. Just three recirculating delay lines, that's it? I would assume the 'golden ratio' should result in fewest modes, but maybe not? Treat the output as mono for now?

To test this, I'll be using my AL3201 box, I can add this new algorithm and the control knobs for each of the gains and sizes in about five minutes.

I was working up a delay line setting last night and put it in as a factory preset. It's titled 'Johnny'. One delay line, 142 milliseconds, a bit of rolloff, and a bit of feedback. I also managed to get a decent vocal plate setting. I think I tend to use too high of allpass coefficients, generally, as when I drop them down I get much less ringing, though I get a bit of a 'loopy' tail.

---

### Post #16 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4080238&postcount=16>

Here's what I came up with for observations:

At any delay less than about 50ms it sounds like a pitch. Above that it sounds like a tape loop. If I set one loop to about 100ms, another at 130ms, and another at about 160ms, the tape loops seem to be much less. But the other thing which was very noticeable was that even though the last delay loop would hide the tape loop effect anywhere from 140-195ms, the pitchiness of the noise (or snare drum) changed quite a lot. Around 160ms seemed to be pretty even, though I did not use a spectrum analyzer. With noise, the spectrum changes a lot. If I move the 160ms tap out to 180ms, the low end of the snare drum really pops out.

If I use something like a snare drum as opposed to a noise source as the input, the 'tape loop' sounds a lot like a helicopter. Adding a second loop at 130ms makes that sound totally go away and it sounds like a bad reverb. Adding 160ms sounds like a better bad reverb. Also, if you stop the sound, the tail of this (bad) reverb sounds pretty even - no particular 'ring' seems to stick out.

At feedbacks less than 0.5, it sounds like a couple of delay lines. At around 0.7 it starts to sound like there's a reasonable tail. Setting the levels at about the same volume level for each loop seemed to sound most natural to me.

What seems tricky here is getting a good frequency response (no peaks), and at the same time getting a good time response (nice reverb tail). One combination of delays seemed to work. Interestingly, those times didn't ratio very well. I got another reasonably nice sounding one at 50ms, 73ms, and 89ms, which have different ratios than the first set of numbers.

Setting one loop fairly short tends to make a 'tunnel' sound - very resonant.

Does this sound familiar?

---

### Post #17 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4080373&postcount=17>

OK, great!

All of your observations sound familiar.

So...

Now remove the single tap from each loop.

Stay with three loops.

Instead, place 3 taps on each loop. For now keep the gain of each tap the same.

Lets double our sample memory to 32k samples, to give some room for the additional taps.

Again using three taps allows the use of the modecalc tool to at least see what three taps looks like in a group.

Still feed all the loops identically (mono in), but now lets pick five taps to sum for the left and 4 taps to sum for the right.

The left and right channels should have at least one tap from each loop.

Now this is the first mention of psychoacoustics; the brain loves to hear a rocking back and forth of sound from the left then from the right then from the left...

So, while finding optimal tap positions on each loop, try to make sure that the taps chosen for the left and the right are interleaved in time (make the first left tap first overall) at least as far as you can, since this will be complicated by the loop sizes.

So now the possible adjustments include loop size, loop gain and now tap locations.

Still no good sound but more variables to contend with.

-Casey

---

### Post #18 -- Page 1
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4080412&postcount=18>

> Originally Posted by **Casey**:
> Now this is the first mention of psychoacoustics; the brain loves to hear a rocking back and forth of sound from the left then from the right then from the left...

Any citations for this?

I'm curious to see where your tutorial leads...

---

### Post #19 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4080448&postcount=19>

David Griesinger mentions in a paper a left right rocking in the low frequencies as being optimal for generating a sense of space. The extrapolation to all frequencies is for ease of implementation for this case at hand.

Of course it could be right first, it's the rocking thats important.

-Casey

---

### Post #20 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4081394&postcount=20>

Ok, this morning's playing around...

Delay 1 = 130ms
Delay 2 = 173ms
Delay 3 = 207ms

Feedback = 73% on all loops.

Taps, delay 1, at:
- 21ms, -4dB
- 71ms, -6.5dB
- 102ms, -9dB

Taps, delay 2, at:
- 47ms, -4dB
- 112ms, -7dB
- 152ms, -8dB

Taps, delay 3, at:
- 40ms, -8dB
- 101ms, -11dB
- 147ms, -14dB

I started in mono. I found that just twirling the delay dial to roughly distribute all of the taps seemed to be not horrible for even time response - a drummer's count-in shows a whole bunch of sharp 'ticks' that don't bunch too much - just a bit. But moving each tap around just a little on snare or noise made a difference. But then I put in vocals, and I found that moving the taps around just a bit made the tone of the vocals change quite a lot - frequency colouration, I think. There's no feedback mechanism to ring at any frequency due to changing the taps around so it's just frequency response of a not particularly well windowed FIR filter.

Then I moved the pan pots on my console out to the extremes. That messes with your head. I was using headphones. The taps were distributed hard left and hard right. It sounded better with the pan pots at 9 or 10 o'clock and 2 or 3 o'clock, and also levelling out the left and right so they were about the same in level seemed to make things work for me.

On impulsive sounds, this sounds pretty awful yet, but on vocals it's not a disaster, and on clarinet and melodica it's actually got a nice, spacey sound that suited what I was listening to - my band's rendition of 'People are Strange' with a lot of back-and-forth between those two wind instruments. The tail still has repetition, but I think that could be tweaked out a bit with matching tap and loop gains. I should be able to make an Excel spreadsheet to calculate those out. I guess another approach would be to distribute several small gain multiplies throughout each loop and keep the tap levels consistent.

Sloping the taps tends to reduce the 'tape looping' effect quite a lot, and to me it seems as though it should. In theory, I would think the gain should slope so that by the time the sound got from the last tap, through the feedback multiply, and back to the first, the slope should be about the same. I didn't do any math this morning (no coffee yet), so I just tweaked. I also left all of the gains of the same polarity, flipping those around should change the character of the frequency response, too.

The other thing that seems unnatural is something like the drummer's count-in. The sound stays too sharp for way too long. That's easy - put a first-order lowpass in each delay loop. I haven't done that yet, but it seems like that would improve the sound quite a lot.

What is interesting is that when you have all of these knobs to fiddle with, you can isolate things. For example, I found that one loop had more repetition than the other, so I just turned off all but that loop and fiddled until two of the loops had similar decay times and repetition. I can only have 60 knobs in my software, and now I'm wishing that I had finished the 'save effect settings' software. Ahhh, assembly code at six in the morning.

For those here who don't know how I'm doing this, I use a MC9S08AW60, 20 MHz, running the user interface. It interfaces to two in-series AL3201 'digital reverb engine' chips by Wavefront Semi, each of which can do about 110 instructions per program loop - I believe each AL3201 chip is roughly similar in performance to maybe a 224XL or maybe a PCM70, just judging from the information in the service manuals for those boxes. A CODEC, a 2x20 vacuum display, an input level bargraph, a few pushbuttons, and a rotary encoder completes the board.

---

### Post #21 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4081491&postcount=21>

![dale366verb board photo](http://www.10000cows.com/dale366verb.jpg)

It is real... there's blue jumper wires on there.

---

### Post #22 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4081655&postcount=22>

Nice looking board! Did you build that yourself?

So you are right on with both the tap slopes and the low pass filters on each delay loop. You might want to add a pair of low pass filters in series right on the input that would get you a 12dB rolloff at around 12khz.

Now put 3 allpass filters on each output. Play around with the sizes but to start out, take around 70% of the length of your smallest loop. Then divide this in two using the golden ratio you mentioned earlier. Make two allpass filters in series out of these delays times. Then add a third one that is fairly small say around 2.5 ms. from largest to smallest use say .35, .45, .6 for the gains.

Then reduce the size of all of the allpasses on the left by 5%, and increase the size of the allpasses on the right by 5%. Also alternate negative then positive then negative feedback on the three series allpasses on the left, and do just the opposite on the right, positive, then negative, then positive.

Now there is more to play with.

-Casey

---

### Post #23 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 10th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4081866&postcount=23>

Yes, I did the layout and hand-built two of them. I'm planning on migrating from the AL3201 processor to that 'real' DSP - the DSP56366. I gave it 512k of SRAM, but I mapped it in two chunks with a hole in the middle so the number of address lines on the outside of the chip cause the memory to wrap around so you can use a simple delay line without using the modulus operator, which in the DSP56300 family, is limited to 32k.

Ok, I'll try that probably tomorrow morning. This is getting interesting. The three separate loops are really neat. I am amazed at how the three loop simple 'slapback' delay actually begins to sound like a reverb and not just a simple Sun Records style of delay. I know the original allpass loop arrangement didn't do this, I've not actually seen this sort of arrangement except in the context of an FDN.

Another thing that is popping out at me is to cross-couple the loops a bit to simulate corner modes.

I've also got a pretty big inventory of other DSP's - at least for a hobbyist. I have a few Spartan-3E FPGA's, a tray (60) of the older DSP56002's, and about 20 of the AL3201's in a rail.

---

### Post #24 -- Page 1
**User:** zmoorhs
**Info:** Registered User | Joined: Feb 2009 | Posts: 330
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4082872&postcount=24>

> Originally Posted by **Casey**:
> Now put 3 allpass filters on each output. Play around with the sizes but to start out, take around 70% of the length of your smallest loop. Then divide this in two using the golden ratio you mentioned earlier...

Sorry if this is a dumb question, but what type of allpasses are you talking about? Is there only one type used in reverbs?

---

### Post #25 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083021&postcount=25>

> Originally Posted by **zmoorhs**:
> Is there only one type used in reverbs?

Well yes, but you may consider nested or modulated versions as new types, but in general there is just the one type. Have I misunderstood your question?

-Casey

---

### Post #26 -- Page 1
**User:** zmoorhs
**Info:** Registered User | Joined: Feb 2009 | Posts: 330
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083127&postcount=26>

> Originally Posted by **Casey**:
> Well yes, but you may consider nested or modulated versions as new types, but in general there is just the one type. Have I misunderstood your question?

No, I'm probably just missing something. I thought there were more than one type of allpass, one of the differences being the decay slope, or am I getting confused with combs with that?

---

### Post #27 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083184&postcount=27>

> Originally Posted by **zmoorhs**:
> No, I'm probably just missing something. I thought there were more than one type of allpass, one of the differences being the decay slope, or am I getting confused with combs with that?

Hmmmm, not really sure what you might be thinking.

Perhaps you are thinking of the gain of a particular allpass? This would effect the "decay time" of the allpass.

-Casey

---

### Post #28 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083208&postcount=28>

> Originally Posted by **seancostello**:
> Barry Blesser has a recent patent that addresses this issue. Blesser introduces a filter type called "notchpass," where the group delay peaks are matched to corresponding minimums in the frequency response. In the feedback loop of a comb filter, the result is a reduction or elimination of the metallic sounding frequencies sticking around.
>
> I haven't tried this, as I first read about it in an issued patent, and it was not in any prior art that I know of. I tend to deal with these allpass issues by reducing the coefficients to lower levels, by randomizing things over time, or by not using allpasses.

I would agree with you on how you deal with allpass filters.

I have listened carefully to this idea in practice. It has the most applicability in longer reverbs that pass the same signal through many passes of the same allpass (or notchpass using Barry's method).

It is very clever and absolutely does what you say; it eliminates metallic qualities in the tail.

The problem is that it colors the early part of the reverb in an undesirable way. The argument is that the early reverb is dominated by the dry signal, but I still feel that (with all it's artifacts) modulated allpasses still sound better.

-Casey

---

### Post #29 -- Page 1
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083309&postcount=29>

With the allpasses added, it sounds like a reverb. Still, some looping sounds, but ignoring those, the rest sounds pretty good now. I evenly spaced out all of the taps, made the loops equal to 20k (at 48kHz) and split them up 1:1.272:1.618. I needed close to 10k for the output allpasses and I only have 32k on this chip to work with. The allpasses were made to your suggestions, though I didn't play with the allpass size yet. With no gain in the output allpasses, the signal was pretty close to what I had dialed in last time. Adding the allpasses makes it sound like a reverb. I just used your gains, though I could scale them up so I can try too much of a good thing. By changing the tap location in the loops, you can change the colouration quite a bit, just like last time. Close to evenly spaced seems to work well. I have an 8-bit scalar for tap locations (actually, all parameters), so you can't dial in to the nearest sample from a knob, but that probably makes it so that the taps aren't exactly at multiples of each other thanks to rounding.

I can see one of my next steps probably should be to calculate the tap slope to correspond to the decay value used at the end, which should get rid of, or at least tame, the repetition, then go back and revisit the tuning of the taps without output diffusion so you can hear that part better.

---

### Post #30 -- Page 1
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083345&postcount=30>

Great!

Now (I hope you have the cycles for this) we need to introduce modulation.

As you mentioned the position of the taps have a large impact on the coloration of the reverb. To reduce this, the taps should be randomly modulated within a 5 ms window.

The modulation should be random as opposed to a chorus pattern. This can be accomplished using a table of random offsets. The taps can be moved using linear interpolation with at least 16 steps between samples. Use the table to define a new offset for whichever tap finishes it's traversal during the current sample time processing.

Play with the speed of the tap movement (and the resulting pitch effect) to meet your subjective taste.

It's going to start sounding nice now, but there are a few more steps to consider and a lot of tuning to go.

-Casey


---

## Page 2

---

### Post #31 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083367&postcount=31>

Ok, I think I understand what you're looking for here. I haven't tried anything other than a sinusoidal chorus on the AL3201 so this will be interesting. I've used 37 cycles out of 105 available so far, the AL3201 doesn't do support math except for a sinusoid or triangle chorus, so the 9S08 will have to do the modulation unless it's a sinusoid or triangle. Unfortunately, I can't read or write the chorus offset registers in the AL3201. It can also only update one instruction per wordclock plus a bit of a safety delay. Can I just fade in one tap as the other one fades out or should I glide between the taps like the LXP15 'glide delay' function? I'd guess that it should be a 'glide'. I think I can come up with random numbers pretty easily. I might have to experiment with how quickly I move taps around, too.

---

### Post #32 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083391&postcount=32>

> Originally Posted by **dale116dot7**:
> Can I just fade in one tap as the other one fades out?

Yes, I think this is a way to look at it. In that each tap is really two taps next to each other. The value that should be summed to the output will be a linear combination of the two neighboring taps ie.

`27/32*mem[n] + 5/32*mem[n+1]`, then `26/32*mem[n] + 6/32*mem[n+1]`, then `25/32*mem[n] + 7/32*mem[n+1]`...

then a memory address change occurs when the sequence reaches this point:

`1/32*mem[n] + 31/32*mem[n+1]`, then `0/32*mem[n] + 32/32*mem[n+1]`, then `31/32*mem[n+1] + 1/32*mem[n+2]`...

if you use 32 steps between each sample.

It's of course OK if a tap doesn't move during a given sample time, if it takes multiple sample times to set up the new move.

The lead sample will be either n+1 or n-1 depending on which direction the tap is moving.

-Casey

---

### Post #33 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083487&postcount=33>

> Originally Posted by **Casey**:
> Yes, I think this is a way to look at it. In that each tap is really two taps next to each other.

How about taps not next to each other? Blesser mentions this in his book, page 269:

"Alternatively, any gain can be changed by slowly moving its value, which does not require interpolation. Typically, a randomizer gradually fades the gain of a path between two values, or reduces its gain to zero, moves the path, and then gradually increases the gain up to full value."

Also, why modulate the output taps, and not the ends of the combs? I would have thought that this would result in an overly chorused sound, but I haven't tried delay length interpolation of the output taps.

Dale: For random modulation, can you have the 9S08 change the frequency of the sine/triangle LFO to a random value + fixed offset every N samples? For the triangle LFO, this would produce a result similar to randi, the linearly interpolated low frequency noise generator found in most computer music languages since the 1960's. A sine LFO would be similar, but smoother. The random update of LFO frequency can happen at a VERY slow rate - 3 times a second has worked well for me in the past.

Nice thread. The fun little reverb project has gone from Schroeder 101 to some very cool concepts, in very easily digestible form.

Sean

---

### Post #34 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083508&postcount=34>

> Originally Posted by **seancostello**:
> How about taps not next to each other? Blesser mentions this in his book, page 269...

No fair reading ahead Sean!

We can go there after establishing a working reverb that can be tuned to sound pretty good.

There are lessons to be learned in working with a complete reverb and then taking the next steps.

Like you said, nice digestible steps.

---

### Post #35 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4083946&postcount=35>

I guess what I was asking was whether Sean's approach would be ok or if interpolation (gliding) was the way to do it. Sounds like either approach would work ok. The 'easiest' way to do a gliding delay on a 3201 is to use the chorus instructions, set them to sine or triangle or something like that, and either run them or don't run them for some random amount of time. Essentially, rather than having the random number generate a tap offset, that random number will generate an integration time (at a fixed rate so the 'chorus' effect is controlled), which will be randomly run. I'll try that first. By ramping the integration rate from, say, 1Hz to 0Hz, then back up randomly over a period of a few seconds, that should result in tap movements that sort of 'move' once in a while.

I found it interesting how well adding just a couple of allpasses on the outputs would result in such an improvement.

---

### Post #36 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4084264&postcount=36>

> Originally Posted by **dale116dot7**:
> I guess what I was asking was whether Sean's approach would be ok or if interpolation (gliding) was the way to do it.

Gliding will work, and it sounds like you have an interesting strategy for getting it done efficiently in your system.

Sean, could you elaborate on the specifics of your approach?

-Casey

---

### Post #37 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4084450&postcount=37>

> Originally Posted by **Casey**:
> Sean, could you elaborate on the specifics of your approach?

The idea comes from granular synthesis, and some of the pitch shifter work I have done (the pitch shifter in SuperCollider works in a similar way):

- Crossfade between a pair of taps that are separated by many samples, up to the maximum modulation width.
- When the volume of one of the taps is at a minimum, randomly change the tap location, within a range specified by modulation width.

This also works with individual taps, each with their own volume envelope, which is closer to most granular synthesis approaches. The tap rate can be constant, or can be randomly varied each time the volume is at zero. Working with pairs of taps would help to create a more constant tap density, as you could use some form of equal power panning. You could also crossfade between more than two taps, using a multiphase oscillator.

My guess is that this technique has been used before in reverbs (and possibly some old pitch shifters), and it seems similar to what Blesser describes in his book. The AL3201 could probably do this if the modulation is driven by the microcontroller.

Sean

---

### Post #38 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4084472&postcount=38>

It seems like you would hear the varying comb filter coloration of crossfading taps that are within a couple of ms of each other?

-Casey

---

### Post #39 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 11th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4084504&postcount=39>

> Originally Posted by **Casey**:
> It seems like you would hear the varying comb filter coloration of crossfading taps that are within a couple of ms of each other?

Yes. However, it is a time-varying comb filter. For pitch shifters, it ends up sounding way better than the fixed comb-filtering effect you get with non-intelligent pitch shifting (no looking for splice points). For reverbs, I'm not sure yet. The artifacts can sound like low bit rate MPEGs at times. I'm not using this in my current work.

I see your point, though. Perhaps there should be a minimum distance between taps that are crossfaded. In this situation, the corresponding time-invariant case would be 2 output taps from the example reverb, rather than a single tap.

Sean

---

### Post #40 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 12th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4086391&postcount=40>

I'm going to try using the 'gated chorus oscillator' approach this morning. If you had not three, but maybe twenty taps in each loop, could you not just fade one out, then fade another in? That tap would disappear briefly but missing one of twenty for a few milliseconds might not be as noticeable as missing one of three.

---

### Post #41 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 12th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4086544&postcount=41>

Ok, I tried this out. It does prevent 'buildup' or 'cancellation' on average. While running vocals or percussion through it, I don't really hear buildup. With a pure-sounding tone (clarinet, in this case, but the test oscillator on the console pinpoints this in an annoying way), buildup or cancellation happens but after a fraction of a second it goes away. What is noticeable when it comes to switching then staying at a particular tap is that the cancellation or reinforcement 'sticks around' then goes away. Perhaps running a very low-speed chorus in parallel with switching taps would help? ie. Rather than freezing the taps, then moving them a bit, you move them around at very low speeds, maybe a couple samples per second, then you randomize a faster move on top of that. Or is there something else you have in mind for this?

I am guessing that in 'Lexicon' terms this would be kinda-sorta like the 'Wander' parameter? Also, by using a 5ms tap movement, that works but I probably need to lower the tap movement if I lower the size of the loops (for a smaller room). Does that sound right? Right now my 'room' totals 416 ms, but divided down, the smallest dimension is 100ms or 33 metres. A 5ms chorus is equivalent to 1.6 metres, but if the room is scaled down in size the distance the taps move is quite a bit relative to the room size.

Since I'm doing this with the LFO's, I notice a tap movement rate where the tap movement becomes noticeable. A tap rate movement of about 100 samples per second can be noticed on pure tones or during the tail decay. Under about 50 isn't easy to notice - the more output diffusion, the less noticeable it is. In a busy song, much faster tap movements are possible unless they happen to fall in a bad time where you might hear them. When you have drum leakage into other mics, you get a funny 'whoosh' effect when a tap moves.

I'm still curious as to how to get rid of the tape looping effect more completely, but I guess we'll get to that. The rest of the algorithm is sounding pretty good. Still some cleanup in the tap movements and further improving (actually, reducing) the tape looping should make it possible to use this in a mix. I think I'll do a mix of some kind of song in a few days so people can hear this. It'll be a mix with way too much reverb, so you can hear the processing.

So far I have 44 free instructions after adding the chorus, but I also have another 100 instructions left in the other chip. The two chips are in series (a true cascade arrangement) with only left and right audio between them. I would probably put input conditioning - predelay, input filters, maybe some allpasses on the inputs - in that part.

---

### Post #42 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4087849&postcount=42>

> Originally Posted by **dale116dot7**:
> Rather than freezing the taps, then moving them a bit, you move them around at very low speeds, maybe a couple samples per second, then you randomize a faster move on top of that.

So, my understanding of the modulation that you are using is that it is delay time modulation, using the built-in linear interpolation, where the modulation starts and stops. Is this correct?

It seems like you would want to have constant motion in the taps, with randomly changing amount of motion, and/or direction of motion.

> A tap rate movement of about 100 samples per second can be noticed on pure tones or during the tail decay. Under about 50 isn't easy to notice - the more output diffusion, the less noticeable it is.

Diffused chorusing is a much different sound than chorused diffusion. Since Casey is using some pretty big output diffusors here, low amounts of modulation would probably be smoothed out, and not sound like obvious chorusing. Once you break the LTI constraints of the reverb (in this case, it is no longer time-invariant), the ordering of the different blocks makes a difference. Some good ideas to try out.

Sean

---

### Post #43 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4087913&postcount=43>

Yes, what I'm doing is running one of the four LFO's at any given time with the other three frozen. The times I switch the LFO's vary with a pseudo-random value. I actually read the executable code from start to finish to get that randomized value. Perhaps a better approach is to use that random value to multiply the average tap movement rate and keep all of the taps moving, though at randomized rates, which should, when integrated by the LFO, result in randomized locations. I changed the coding of the host software so the LFO sizes vary with the master loop size parameter.

I might add, scaling the loop size parameter really does make the room size change from a pretty decent-sized hall to a pretty small room. It actually sounds more like a finished reverb in the 5-10 metre region (sizing 332 m/s and the shortest loop), above that is where the looping sound happens. The 'looping' that remains I think is simply the content of the input signal recirculating throughout the loop.

In between reverb experiments, I've been coming up with digital delay patches for that mode of operation. One thing I find with the AL3201 is not enough memory. 32k just isn't enough for really big spaces.

-Dale

---

### Post #44 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4088126&postcount=44>

I tried distributing loop gains, and that helped the tape looping a bit, so my output tap levels are obviously not right - they need to track the RT multiplier better. But by distributing that loop gain around, the length of loop, the RT becomes a bit grainy since all gains are the same. I also tried cross-coupling the loops, but at any setting that got rid of the looping I found artifacts that I didn't much care for - strange ringing between the loops.

I tried this reverb with the distributed gains on some music, and it sounds pretty good - not quite as good as 'vocal magic' on the '91, but still, pretty good. I think the looping is the biggest difference between the quality of the sound of the '91 and this algorithm.

---

### Post #45 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4088170&postcount=45>

Let's save cross coupling for later. It's a great next step but it is a bit of a can of worms.

Two things to accomplish before tuning this topology.

Make sure that each loop RT and high frequency reduction is identical.

Keep the modulation moving. Just simplify the design and use a standard chorus on each tap. This is just an artifact of your implementation. There is nothing wrong with that. Work with something between 10 and 50 samples per second. And split the chorus phases exactly into 40 degrees between each tap.

If it sounds a bit too chorused, well that can be randomized better when you go to the 56k, for now just call it a feature!

What you have now is the topology of the EMT 250. If you have access to an IR set of the 250 then you have something to tune against.

I encourage you to tune your current design until you can beat the 250 IRs. To be fair, vocal and snare would be the most useful comparisons, as these are where the 250 is most often used.

The thing that will separate this topology from the others is the snare reverb will have a tail that sounds like "cawhhhh" and not "chchshssssss". The next steps will change this, and this is a downside!

In the next step we will look at ways to further eliminate the tape loop sounds. But for now, the tuning steps I mentioned will help the tape loop problem and the left right balance. Adjust the tap gains/slope to help in both of these issues as well.

-Casey

---

### Post #46 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4088361&postcount=46>

> Originally Posted by **Casey**:
> Work with something between 10 and 50 samples per second. And split the chorus phases exactly into 40 degrees between each tap.

The AL3201 doesn't have the ability to arbitrarily set phases between the built-in LFOs. One option would to be to use 2 of the cosine LFOs, as these have quadrature outputs. It is easy to get 4 phases out of a single AL3201 LFO, separated by 90 degrees. Not sure what to do with that last tap.

> What you have now is the topology of the EMT 250.

WOW! I had wondered if you were describing something similar, but this is cool to see. I will give this a try tomorrow.

One question: Should there be any modulation of the comb lengths, in addition to the modulation of the comb tap outputs?

Sean

---

### Post #47 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4088623&postcount=47>

> Originally Posted by **Casey**:
> Let's save cross coupling for later...

Yes, I figured that out... it's easy to make an oscillator.

It is a bit easier to randomize the chorus phases, it actually would be pretty easy to do. There are four LFO's with +/- SIN and COS outputs. If I randomly modulate the LFO frequency, I should get random phasing between the taps.

I don't have a 250 IR (I'm out-of-the-box), though I probably could arrange it. But I do have a PCM91, TC M5K, and a REV7 to 'tune' towards. Are there any settings on a '91 that are close?

To me one obvious cure for looping is simply to put a loop allpass in each loop, k=0.4 to 0.5, maybe 1/3 the length of the loop or so. That should smear the 'impulse' looping at very long RT's when a sharp something happens just before silence and all you hear is the tail.

-Dale

---

### Post #48 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089432&postcount=48>

> Originally Posted by **dale116dot7**:
> To me one obvious cure for looping is simply to put a loop allpass in each loop...

This topology is a "constant echo density" topology. Adding allpasses in the feedback loops will change this, sort of moving away from one of the charms of this very early design.

I think that getting everything possible through tuning this topology, though possibly frustrating, will establish a level of intuition as to what can and cannot be achieved with this most simple use of a couple of basic building blocks.

-Casey

---

### Post #49 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089463&postcount=49>

> Originally Posted by **seancostello**:
> WOW! I had wondered if you were describing something similar, but this is cool to see.

This is the basic topology, but does differ in specific details. I used the number 3 quite a bit so that the room dimension analogy could be used for example.

> One question: Should there be any modulation of the comb lengths, in addition to the modulation of the comb tap outputs?

Yes, this will move the frequency spikes of the feedback loops, reducing the build up and audibility of them. Good next step.

One other note, we are using linear interpolation rather loosely in this design. This will act as a moving filter which at it's deepest cut will reduce the frequencies that are roughly at 1/4 of your sample rate.

I mentioned earlier that a 2 pole input filter should be used. This is to sort of cover up this effect. If the frequency wavering becomes too audible, just reduce the input filter down from 12k to say 8k or 9k to help mask it further.

-Casey

---

### Post #50 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089521&postcount=50>

> Originally Posted by **Casey**:
> This topology is a "constant echo density" topology.

"Constant Density Plate"?

---

### Post #51 -- Page 2
**User:** Warp69
**Info:** Lives for gear | Joined: Sep 2004 | Posts: 714
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089640&postcount=51>

> Originally Posted by **Casey**:
> ...if you use 32 steps between each sample.

Would you consider a 32 steps interpolation good enough for high-end reverbs?

I currently use 256 steps - the high quality interpolators in Eventides uses 128 steps.

---

### Post #52 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089680&postcount=52>

The 12dB filter was easy to add, and yes, I also heard the filtering artifact from the chorus with the EQ turned off. But you also hear a high frequency reverb that you just don't hear in real life. Another option would be to use allpass interpolation, though I've not determined if it is possible to implement this on the AL3201.

I now see how a few more of the parameters in the PCM91 relate to constants in the DSP portion, but what I'd like to know is if there is a way to get a constant density sound on it. I don't see a 'constant density' algorithm in the '91, though I might have missed it. I would guess cranking up the diffusion and cranking up definition might do that, but I don't really know how the host processor in the '91 converts a knob setting into the gains used by the Lexichip.

---

### Post #53 -- Page 2
**User:** Warp69
**Info:** Lives for gear | Joined: Sep 2004 | Posts: 714
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089724&postcount=53>

> Originally Posted by **dale116dot7**:
> I don't see a 'constant density' algorithm in the '91...

It's only possible to get constant density with the Concert Hall algorithm by having a max value for Definition. Diffusion will control the density.

---

### Post #54 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4089750&postcount=54>

> Originally Posted by **dale116dot7**:
> ...in this modified algorithm there are a total of seven allpasses

I probably wasn't clear but I tried to mention using 3 allpasses on each output (the last being around 2.5ms.)

But it sounds like what you have is working for you, so just stick with that.

When do we get to hear it?

-Casey

---

### Post #55 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4090219&postcount=55>

Maybe I do have three on each output, I forgot about the little ones. I don't have the code at work. But things smoothed out with more allpasses - I put them on the input.

I'll do a quick mix with 'way too much' reverb tonight, including a 'stop' so you can hear the tail. I'll try two RT settings, too, one is 'reasonable', and the other is 'RT of a canyon with a size of a high school gym'. I'll also do it with and without the input allpasses.

-Dale

---

### Post #56 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 13th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4090315&postcount=56>

Just leave them in. It sounds like you have a nice sound now.

I think it would be more interesting to hear differing amounts of chorusing using the method you came up with. A little chorusing can sound nice. I think it would be interesting to see peoples comments on how much you can "get away with" for different sources.

I would also include some mixes with a "tasteful" amount of reverb, since this is what many folks are used to judging. I assume this thread will be around for a while, and I would hate to miss this chance to showoff what you have now, before the next steps are taken.

-Casey

---

### Post #57 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 14th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4090813&postcount=57>

All of these are a size of 33 metres (100 ms shortest delay).

[Audio Files Page](http://www.10000cows.com/AudioFiles.htm)

- 2 = just some random settings, input diffusion set on
- 3 = super long RT
- 4 = super long RT with chorus at 3.25 Hz (default is 0.27 Hz)
- 5 = similar to 4, chorus adjusted
- 6 = no input diffusion, chorus at 1 Hz
- 7 = no input diffusion but a 3-tap multitap at around 0, 18, 25, 32, 45ms ahead of reverb
- 8 = reasonable RT and level, 'close' settings
- 9 = what we're starting with (dry)

You probably want to be on DSL or other highspeed, I left them as WAV so you would not hear any of the funny MP3 processing that's pretty obvious.

The input diffusion is covering up a ringing that I don't like. I think I was battling the 'loop' sound and didn't quite catch that. I have to move a tap or two in the output section.

---

### Post #58 -- Page 2
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 14th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4091121&postcount=58>

Hi Dale:

I listened to most of your settings, and it sounds pretty good to me. The main flaw that I heard is probably inherent with a 3 comb system: not enough modal density. I have been playing with a similar system today, using 4 combs (I cheated and cross-coupled them). No matter what type of modulation I use, it just doesn't sound as good as my larger reverbs that use at least twice as much delay memory.

As far as the ringing, you should see if it is from the combs, versus the output allpasses. I found that putting the allpasses on the output seems to magnify any ringing in them, versus having the allpasses on the inputs to the combs. Not sure why this is. It might make sense to tune the comb taps first, then work on the output allpasses delay lengths.

Sean

---

### Post #59 -- Page 2
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 14th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4091309&postcount=59>

Wow Dale, very impressive. What is that, just one week of part time work!

I agree with Sean there does seem to be some needed tuning of those output allpasses, I'm sorry my sizes were probably not ideal.

> Originally Posted by **seancostello**:
> No matter what type of modulation I use, it just doesn't sound as good as my larger reverbs that use at least twice as much delay memory.

You can increase your modal density by implementing the simplest form of the FDN. Simply take the output of loop1 and instead of feeding it back to loop1 feed it back to loop2, then loop2 to loop3 and loop3 to loop1.

Now your modal density is greatly improved and the modal peaks and valleys of your feedback loop will be much softer. This is because the amplitude of the modal peaks is proportional to the overall gain in the feedback loop. The gain will be less as the feedback path now moves through three gain reductions around the loop.

This change also tilts the design to a more balanced feed forward/feed back design as the loop now has 3 feedforward paths as well as the feed forward paths of the taps. Each of the 3 feed forward paths in the loop will provide its own modal pattern on top of the single feedback modal pattern.

-Casey

---

### Post #60 -- Page 2
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 14th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4092103&postcount=60>

I checked out a frequency response, and this is probably what I hear, and what the input diffusion seems to cover up quite a bit.

Below about 200 Hz, there are some peaks and valleys but generally ok. There's one buildup at 81 Hz that's a bit higher than I'd like to see. At 315 Hz there is a 20dB notch, and at about 630 Hz there's the top again. At 960 Hz, it's another notch, and again at 1545 and 2206 Hz and 2842 Hz. A classic comb. But I don't see anything that many samples apart, that's with the output allpasses turned off. Turning on the chorus changes the average so over a 20 second spectrum plot it's pretty flat. Also, without the chorus but with more allpasses on the input, it flattens that out pretty well. It seems to me that the depth of the comb response is the problem, not that there is a comb response. It's pretty dramatic. When listening to a test tone, sometimes the output signal just up and disappears, returning in a fraction of a second. But where do I look if I can't see anything that is that many samples of delay? I think it should be a 76 sample delay to generate that pattern at 48 kHz Fs.

## Page 3

---

### Post #61 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 14th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4092259&postcount=61>

> *Originally Posted by Casey:*
> I agree with Sean there does seem to be some needed tuning of those output allpasses, I'm sorry my sizes were probably not ideal. You can increase your modal density by implementing the simplest form of the FDN. Simply take the output of loop1 and instead of feeding it back to loop1 feed it back to loop2, then loop2 to loop3 and loop3 to loop1.

Ok, I see. There are still three sets of three taps, three injection points, but one 'big loop' instead. That should reduce the looping sensitivity as the sounds loop through different delay lines and more particularly, through all of the RT multipliers, so that should automatically match the RT gains between the loops. But before I do that, I would like to get the 300 Hz comb under control. Even though the chorus moves the taps around and makes that drift around, I still hear it as a colouration that I don't like.

I guess one of the things I could do is invert one tap at a time and see when the 300 Hz null turns into a 300 Hz peak. That should be the culprit.

---

### Post #62 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 15th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4094947&postcount=62>

Tonight's progress...
I coupled the loops as you described, that stabilizes the tail quite a bit. I also added host software to slope the taps with the RT multiplier, and that also helps. At longer RT settings (a gain of greater than 0.7), it sounds pretty good. I put it up against the PCM91 'Vocal Magic' preset, and I would put it in a similar quality level to that - similar enough that I could use either as a vocal reverb and be happy with either.

I also added three loop allpasses with a setting that allows you to turn them off (0), turn them up to a reasonable level (50), or turn them up so much that they ring (100). On vocals the effect is subtle, I wouldn't mind either one. On percussion, the change is dramatic. I like the idea of one algorithm doing both a constant density and a building density with the twist of a knob.

The one thing that happens now is for shorter RT's, the left output decays faster than the right output - you hear a dramatic 'twist' to the tail. At long RT's that 'twist' goes away. I have my taps arranged as follows:

R: dly1[1371], dly1[6056], dly2[5230], dly3[2217], dly3[10252]
L: dly1[4113], dly2[1742], dly2[9473], dly3[6656]
fb: dly1[8227], dly2[10462], dly3[13312]

Also, for short sizes, the sound gets a bit choppy or something. I set the program for a maximum size of about 56 metres, and it goes down to 12 metres and sounds ok, but below that it sounds a tad bit odd.

---

### Post #63 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 15th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4095079&postcount=63>

Wow, that is terrific!

As for the delay fading on the left, did you try evening out the output allpass sizes? Looking at your tap layout you might want to make the left output allpass sizes a bit larger than the right.

Also, could it be from output taps that are within a loop allpass? (does it happen when the loop allpass gains are at 0?)

I'll bet the choppy sound is something not being sized correctly (taps outside of loops, that sort of thing)

I can't wait to hear it.

-Casey

---

### Post #64 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 15th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4095645&postcount=64>

Turns out that my left allpasses are shorter than my right allpasses. I'll try reversing the sizes.

I'm not so sure that the 'choppiness' isn't actually some amplitude variation through the loops that sort of wavers gently at large sizes, but then gets faster - and more noticeable - at smaller sizes. It happens with or without loop allpasses, and it comes on gradually with size reductions. That would indicate either my output tap gain or loop gain tuning needs a bit of work. Since I use an algorithm to calculate that out, that probably needs some work. It also gets better at extremely long RT's and worse at shorter RT's, so it seems as though it's in the feedback path, which is pretty simple - three gain multipliers. I should check the calculations on those feedback path numbers.

I'll run some more rough mixes through once I get the remaining problems fixed. The combing is gone, I must have had a programming mistake because when I split the algorithm up into the two chips, I needed to change about four lines to transfer the raw tap data from one chip to the other. The problem went away as soon as I did that, so I probably had one instruction in the output tap section that didn't clear the accumulator when I expected it to be zero.

---

### Post #65 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 16th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4098185&postcount=65>

Does the "wavering" happen when the chorus it turned off?

I wonder if this is just the hf rolloff that is caused by the linear interpolation?

-Casey

---

### Post #66 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 16th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4098512&postcount=66>

I did it with and without chorus. After redoing my calculations for tap and feedback amplitudes, it's a lot better. I calculate the RT's and tap gains for each of the loops based on a continous slope, and after the RT feedback, the first tap will be at close to the 'correct' level had the loop been unrolled. It works well with the innermost feedback gain set to 0.45 or higher. Below this, the sound is pretty uneven and choppy. I would suspect that is because the number of taps vs. how long the sound stays in the loop makes the sound disappear before the output allpasses have had a chance to build up any energy - thus a choppy sound. The room size no longer causes a waver, but it also doesn't really sound that great under about 10 metres - using 32k split between the three loops comes out to about 52 metres for the shortest distance.

---

### Post #67 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 16th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4099472&postcount=67>

I think a solution to the small-size sound would be to size the output allpasses not linearly with the loop size, but in some other relationship 'tweaked' to get the sound right. It sounds close, but not quite right. A table lookup and interpolate is trivial, so making them nonlinear is easy.

Above 10 metres (about 6k of memory used), it is fine. Above 20 metres it sounds quite good. That is a 5:1 range of sizes for one algorithm, that has about the same ratio limits as the PCM70's plate and chamber algorithm size range (they go from around five metres to around thirty). It is possible that changing the output taps around at a small size might make it sound better smaller, and then it should sound good when sized up. Do you ever find the need to shift the output taps any way but linearly with size? Also, is there any reason to increase the number of taps on this algorithm? Is that something to experiment with? Or do you have another 'next thing to do' that's even better?

---

### Post #68 -- Page 3
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 16th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4099719&postcount=68>

Regarding the sound at small sizes, one important thing is what your total modal density is at that size setting. The length of the longest delay is used in some reverbs to determine size, but I would think that it would be more important to try and match the sum of the delay lengths to the room size. Of course, a large hall has a few orders of magnitude more resonances than what a digital reverb usually has, but perhaps there is some metric that would be useful.

One possibility is to have the Size control match up with the predicted Schroeder frequency of a space. In other words, your average density of resonances per Hz for your artificial reverberator (which, for a conventional delay based single band reverberator, is constant across all frequencies) matches the modal density at the Schroeder frequency of an "ideal" rectangular space with the longest dimension corresponding to size. Someone who has had more sleep than me can probably explain this better, or better explain why my idea is totally wrong.

EDIT: OK, my idea is probably wrong, in that I think that the Schroeder frequency is DEFINED by having X amount of resonances per Hz. So, maybe a better idea is to match the resonance density of the reverb (totalDelay/samplingRate) to the resonance density of the modeled space at some particular frequency, like 1000 Hz or so.

Of course, the structure that Casey was discussing was loosely based on the EMT-250, which didn't have enough modal density to emulate anything but the tiniest of spaces. The modulation tricks Casey is discussing are used to turn the discrete resonances into statistical peaks. The goal of the modulation is that the peaks become wide enough to "fill in the gaps" between each other, thus emulating the effect of having far more peaks per Hz. Again, others can explain this better than I can, with Barry Blesser's work being a good start. I always view the resonances as a picket fence, with the modulation moving the fence back and forth such that it appears to be a solid surface with some degree of transparency.

Another idea is to not worry about emulating a physical space with this algorithm, and make it more of a "plate." Some recent papers I have read suggest that plates have a fairly constant modal density across the audio range - around 1.27 resonances per Hz on average. So, give yourself 60K of total delay time for a 48K sampling rate, and then put in taps and allpasses and scattering and stuff until it sounds like a plate. Just that simple.

I love this thread, BTW. Love love love it. I have been following along with my VST code, and my algorithms are improving as a result. My EMT-250 type algorithm sounds OK, although I am having some technical issues with the modulation on my end, but working on this resulted in some breakthroughs on modulation in general that I can apply to my existing code.

*Last edited by seancostello; 16th April 2009. Reason: I was tired and had the tired stupids going on.*

---

### Post #69 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 16th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4100099&postcount=69>

I'm going to start backing out slowly now with respect to specific "next steps".

I think an important goal has been reached. The basic building blocks are now set out, and through just the first week or so of this thread, I think it has been shown that these blocks can sound great, even when put together in the most basic ways.

The more general "next steps" are to refine understanding and use of these building blocks, and how to further manipulate them to match your desired model and future goals when you feel comfortable moving beyond existing models.

I would love to keep chiming in on the technical aspects though. In particular there seems to be gaps in many basic descriptions of what is going on within a room or an artificial reverb.

The modal density question is a good one. Knowing what defines it in an artificial reverb is the first step to knowing how to control it.

The modal density is the superposition of the frequency response of all of the feedback and feedforward paths in the recirculation part of the topology, excluding the ones within any allpasses.

What defines the recirculation part of the topology?

What defines a feedback path, and what defines a feedforward path?

I mentioned earlier that having a balance of both types of paths is a good thing; why is this?

-Casey

---

### Post #70 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 17th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4101404&postcount=70>

No recirculation or no feedback gives a slapback or a bunch of slapbacks. That can sound good if you have enough taps.... convolution. Without recirculation you should get an 'inverse' or 'gate' effect - or an RT that is only as long as the memory you have with an abrupt and unnatural cutoff. Seen that here.

Although an interesting effect is the 'black hole' reverb - something like fifty or so allpasses in series, with the output at the end and no recirculation except the feedback paths in each allpass. It gives a very slow buildup, and an almost symmetrical tail. I call it an effect because it is just that. But perhaps taking some taps throughout can shape this to be a useful reverb. It's on an Eventide.

Speaking of inverse or gated reverbs, if you can't recirculate because of the desired sound - after all, a gated reverb is supposed to cut off - I guess what you'd have to do is unroll the loops (just use a straight multitap with lots of taps) to the length or 'gate time' that you wanted, and use the slope of the output taps to shape the envelope.

---

### Post #71 -- Page 3
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 19th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4110525&postcount=71>

> *Originally Posted by Casey:*
> The modal density question is a good one. Knowing what defines it in an artificial reverb is the first step to knowing how to control it.
>
> The modal density is the superposition of the frequency response of all of the feedback and feedforward paths in the recirculation part of the topology, excluding the ones within any allpasses.

I presume that you are referring to the delays within input or output diffusion allpasses, and not the delays within allpasses embedded within the recursive part of the reverb.

I was thinking about modal density versus the "size" parameter. In most reverbs I have seen, increasing size by a factor of 2 simply scales the delays by a factor of 2. This maps size to the length of the longest delay in the room, or how long it takes for an input signal to bounce back.

In a real acoustic space, increasing the room sizes by a factor of 2 will increase the volume by a factor of 8; in other words, the volume increases as the square of the size increase. However, the Schoeder frequency is calculated as 2000*sqrt(RT60/volume), so the Schroeder frequency maps more linearly to the size parameter - as the size is increased by 2, the Schroeder frequency is decreased by 2.

Reverberators based around digital delay lines have a resonance density that is constant across all frequencies, versus real acoustic spaces where the density increases with the square of frequency. In a digital reverberator, the average modal density will vary linearly with frequency, and the Schroeder frequency will vary as the inverse of the size decrease. So it seems like mapping the size parameter linearly to the increase in the delay line lengths seems like a good idea, at least from a perceptual perspective.

Sean

---

### Post #72 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 21st April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4114975&postcount=72>

> *Originally Posted by seancostello:*
> I presume that you are referring to the delays within input or output diffusion allpasses, and not the delays within allpasses embedded within the recursive part of the reverb.

The feedback and feedforward paths of allpass filters in the recirculation part of the reverb play no role in determining the modal density.

To the extent that the allpass filter also contributes delay (as you are pointing out) to a feedback path that is separate from it's own feedback path, it does contribute to the modal density of the containing feedback path.

-Casey

---

### Post #73 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 21st April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4114984&postcount=73>

> *Originally Posted by dale116dot7:*
> At longer RT settings (a gain of greater than 0.7), it sounds pretty good. I put it up against the PCM91 'Vocal Magic' preset, and I would put it in a similar quality level to that - similar enough that I could use either as a vocal reverb and be happy with either.

I can't wait to hear it!

-Casey

---

### Post #74 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 21st April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4117726&postcount=74>

Besided doing a nice session in my studio the last few evenings, I've been working away at my DSP56366 board with the intent of putting this (and other effects) algorithms into it. I've managed to get a lot of the basics running, after many hours of work. I still have to write parameter passing software between the DSP and the Coldfire UI processor, but after that, I should be pretty close to ready to implement this algorithm on the new PC board.

This might be a bit much to ask, but I'll ask it anyways. The DSP56366 has a modulus addressing mode to make circular buffers (ie. delays). But the maximum circular buffer size is 32,768 samples. Would you use this and just make a bunch of them in memory, or would it be better to just use memory mirroring and make the entire 512k look like one huge shift register?

-Dale

---

### Post #75 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 22nd April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4117800&postcount=75>

> *Originally Posted by dale116dot7:*
> The DSP56366 has a modulus addressing mode to make circular buffers (ie. delays). But the maximum circular buffer size is 32,768 samples. Would you use this and just make a bunch of them in memory, or would it be better to just use memory mirroring and make the entire 512k look like one huge shift register?

Congrats on getting another board up and running!

I have always used multiple small buffers. But that is just how I like to organize things. I'm sure we have both seen it done either way.

-Casey

---

### Post #76 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 22nd April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4118703&postcount=76>

That makes sense with the hardware at hand. With the Lexicon PCM70/480L and earlier hardware it makes sense to treat the memory as a big shift register as you don't really have any other option.

I'm just starting to work on the host-DSP interface. I've started to figure out how I should be setting up the DMA channels to support that, and I'm using an interrupt line from the host to the DSP signalling the start of a transmission. Hopefully I'll try that tomorrow.

---

### Post #77 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 24th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4127077&postcount=77>

I've been trying to figure out if there's a more efficient way of doing this:

```asm
move x:(r3)+,x1 ; grab number of allpasses
move x:(r3)+,x0 ; grab coefficient
move x:(r3)+,r4 ; grab start of allpass pointer...
do x1,allpassloop
move x:(r3)+,r5 ; grab end of allpass pointer
move y:(r4+n4),a ; get input (start of allpass)
move y:(r5+n5),y0 ; get end of allpass.. generates pipeline stall by using r5
macr -x0,y0,a y0,b ; multiply end data to
move a,y1 ; save result for now... generates pipeline stall by reading accumulator
macr y1,x0,b x:(r3)+,x0 ; mac to generate output, next coeff
move a,y:(r4+n4) ; first mac, send back to input
move x:(r3)+,r4 ; grab start of allpass pointer, generates pipeline stall by fetching pointer r4 being reused at top of loop
move b,y:(r5+n5) ; store end of allpass
allpassloop:
```

It's an allpass, if you guys haven't guessed. It takes about 15 clock cycles per loop (one loop per allpass) which seems pretty high to me. I'm used to the AL3201 which does it in two cycles. Too many stalls, the assembler is talking, I'm hearing, but not understanding. Any ideas? Any DSP56300 programmers out there???

---

### Post #78 -- Page 3
**User:** Nishmaster
**Info:** Registered User | Joined: Dec 2004 | Posts: 335
**Date:** 24th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4127583&postcount=78>

I don't really know anything at all about ASM, or that DSP, but doing some google hunting and manual reading seems to suggest that data ALU operations take 2 cycles to complete, perhaps that's what you're running into here:

> macr -x0,y0,a y0,b ; multiply end data to
> move a,y1 ; save result for now... generates pipeline stall by reading accumulator

Dale, I've been following your progress both here and on groupdiy and it certainly fascinates me. I'm a programmer more than an analog designer, so do keep me in the loop with what you have going on with this project. Here's the 56300 Family Manual that I found:

[56300 Family Manual](http://ridl.cis.rit.edu/products/manuals/Motorola%20DSP/56300fm.pdf)

---

### Post #79 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 25th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4127791&postcount=79>

Thanks for looking at that. I cycle counted as per the instruction sheet in the family manual's instruction timings. The frustrating thing I am finding is a lot of pipeline stalls, but I haven't managed to figure out how to get the algorithm to work with more parallel moves and no pipeline stalls. I probably just have to work away at it to see if there's a better way. I can see shortening it slightly by block processing the allpass but I don't see saving that many cycles. I'm still in a sample-by-sample way of thinking, but I don't see more than a cycle or two of savings here by eliminating reloading of coefficients because I'd just get more ALU stalls from the looks of it. If I were using SDRAM and caches it would certainly be a lot different as we've discussed before. Perhaps processing two allpasses in parallel using more instructions but doing two at once (interleaved) might be more efficient.

I can see an advantage of a VLIW architecture in terms of optimizing data flows through the pipeline registers. I actually could use a read of a register during the pipeline stall period for a useful function but the 56k doesn't allow that. But on the other hand, I've only spent a few days writing 56k code and I already have the audio and host interfaces, memory management, loop gains, and multitap summers tested and working, and the allpass is the one I'm battling now. The learning curve of the 56k is quite low, I've programmed in assembler on a 68k and the 56k is in the same line of thinking from a programmer's point of view.

I might be able to speed up the processor clock another 20 MHz - I'm at 98 MHz and it's a 120 MHz part, but then I'd have to go to two wait states on the SRAM and with four accesses here, it would be faster to stay at one wait state (the minimum) and run at 98 MHz. I am actually quite surprised that the data bus running at 100 MHz doesn't appear to get thrashy at all even on a two-layer PC board. But the bottom is uninterrupted copper, and that was a bear to lay out. Basically, the whole data and address bus - 19 address, 3 control, and 24 data bus lines all on one side of the board, with ground plane on the back. Perhaps I should try it at 120 MHz to check my timing margins.

-Dale

---

### Post #80 -- Page 3
**User:** Nishmaster
**Info:** Registered User | Joined: Dec 2004 | Posts: 335
**Date:** 27th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4134448&postcount=80>

> *Originally Posted by dale116dot7:*
> I actually could use a read of a register during the pipeline stall period for a useful function but the 56k doesn't allow that.

That's odd. My understanding was that the assembler just inserted NOOPs where it detects pipeline stalls. If you can fill the NOOP periods with useful instructions, wouldn't that work?

---

### Post #81 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 27th April 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4134614&postcount=81>

The assembler doesn't - the DSP56300 pipeline scheduler does that for you, but the assembler does warn you. But I did up a quick multitap delay and a few delay loops and allpasses, and found that the actual application speed (in terms of all-passes or taps or filters or loops) is about triple that of the AL3201 that I'm used to - and multitaps are quite quick, actually. I am looking at modifying my multitap algorithm to alternate taps, requiring an even number of taps, but doing MAC's to both accumulators, and summing the two up at the end. That would make taps pretty cheap - probably three clock cycles per tap. If you were looking for a straight FIR-based multitap delay, you could do 500 taps that way per sample. Or a 'convolution' of 10 milliseconds. I'd probably offer both algorithms - one for 4 or fewer where it's cheaper not to take the cycles to sum at the end.

The DSP56k is not nearly as impressive as the ADI Tigersharc or any of the VLIW processors in terms of performance, but reasonably easy to work with for a DIY box.

---

### Post #82 -- Page 3
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 5th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4156253&postcount=82>

> *Originally Posted by Warp69:*
> Would you consider a 32 steps interpolation good enough for high-end reverbs?
>
> I currently use 256 steps - the high quality interpolators in Eventides uses 128 steps.

I just posted about Lexicon interpolation in the Lexicon Bestiary thread, and this prompted me to look at some old Blackfin code of mine from July 2006. I figured this thread would be the better place for the DSP geek stuff.

The code implemented cubic interpolation, for control rate modulation of delay lines, in a VisualAudio feature that was never implemented. I used a 32-bit signal for the modulation, and had the modulation width as an argument to my function. From the maximum modulation width, I calculated the shift and scale amount for the cubic interpolation. What is weird is that the amount of bits in the fractional signal would vary depending on what I set the modulation width at. I am kind of impressed with myself for figuring that out (I haven't touched fixed point DSP in years, and was looking at the code thinking, "I wrote THAT?"), but in retrospect, it would have made more sense to assign a fixed number of bits to the fractional part of the interpolation, and work from there.

Having the modulation width as an argument may have also been a way of dealing with memory access issues on some of the ADI parts. I had an idea back then about using a precalculated modulation width to tell the DSP how much memory should be brought into cache, or how large of a DMA should be started, such that the interpolation could be performed on the memory on the chip (cache for the Blackfin, internal memory for the SHARC). I don't think that this ever got implemented, but it would certainly make sense for small amounts of modulation, where you are not randomly jumping around large distances on a sample-by-sample basis.

IIRC, Dattorro mentioned the idea of using 256 steps for his allpass interpolation, as this helped avoid issues when the allpass coefficient got too close to +-1.0. It is interesting to consider how many steps are considered good enough. If your numeric system is based around 16 bit fixed point, it seems like the number of steps in your interpolation will be determined by what your modulation width needs are. For microtonal modulation such as in reverbs and choruses, you will probably want to have 6 to 8 bits of precision for the integer part of your delay modulation, with the rest assigned to the fractional part. For pitch shifting...wow, I don't know. Double precision, maybe?

My instinct is that, if it is good enough for Eventide, then go for it. I think that most of the Eventide boxes nowadays are based around Freescale 56K processors, so the modulation signal would have 24 bits in single precision. 128 steps for interpolation yields 128K of addressable integer delay locations, which sounds like a lot, but is probably necessary for some of the pitch shifting operations with large windows. The interpolation coefficients are probably updated at the control rate, since it is a control rate operation. I don't know what the Eventide control rate is.

Most of my recent code has been floating point, and I haven't used fixed point for the interpolation, but I may try this out again. I would need to write fixed point modulators, otherwise there would still be a float to int cast, which is probably where most of the cost of my interpolation lies.

Sean

---

### Post #83 -- Page 3
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 5th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4156301&postcount=83>

> *Originally Posted by seancostello:*
> The code implemented cubic interpolation.

Don't get hung up on yesterdays constraints. Today, most algorithms are expected to run at 96k. At this sample rate, linear interpolation will only impinge down to roughly 24k (which I cannot hear.)

> *Originally Posted by seancostello:*
> IIRC, Dattorro mentioned the idea of using 256 steps for his allpass interpolation, as this helped avoid issues when the allpass coefficient got too close to +-1.0.

Whisky Tango Foxtrot??? When (I mean really when) are you going to allow allpass coefs to get any where near +-1.0?

-Casey

---

### Post #84 -- Page 3
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 5th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4156346&postcount=84>

> *Originally Posted by Casey:*
> Don't get hung up on yesterdays constraints. Today, most algorithms are expected to run at 96k. At this sample rate, linear interpolation will only impinge down to roughly 24k (which I cannot hear.)

Yeah, but us plugin folks still run things at 48K much of the time, where linear interpolation is quite audible. I put an Infinite button on one of the reverbs I have been working on, and after about a minute, the high end had gone away. I was using linear interpolation. Meanwhile, the same controls on an algorithm with allpass interpolation resulted in a nice ambient pad that went on and on without any high end loss.

Plus, the VisualAudio code was developed on a Blackfin EZ-KIT, with a fixed 48K sampling rate. Not to mention the noisy convertors that pass DC. Oh wait, I guess I did mention that. Anyway, we couldn't presume high sampling rates, or high end audio for that matter. At the time, folks at ADI were amazed that we were getting any sort of decent audio quality out of the Blackfin, as the Blackfin was originally developed as a chip for a laser printer. The Bricasti was one of the first products that demonstrated that the Blackfin could be used for high quality audio - I think it was Denis Labrecque that dragged me over to your booth at an AES show to see an early demo of the reverb.

The linear interpolation sampling rate argument makes a lot of sense for hardware boxes that run at higher sampling rates, or for running in an upsampled environment, such as might be used for tape echo or vintage BBD flangers with distorted feedback.

> *Originally Posted by Casey:*
> Whisky Tango Foxtrot??? When (I mean really when) are you going to allow allpass coefs to get any where near +-1.0?

1st order allpass with single sample delay, not the allpass delays we have been talking about in this thread. In 1st order allpass interpolation, instead of cross-fading between two delay locations separated by a sample, the fractional part of the interpolation signal is used to control the coefficient of a 1st order allpass filter.

The coefficient can get very close to +-1.0 as the interpolation approaches the integer boundaries of the delay line. Coefficients that are too close to +-1.0 result in a ringing allpass, with the sonic result being unpleasant noise and distortion in the output. Warping the fractional part of the interpolation signal to better approximate linear control over the allpass delay helps, as the warping function (an approximation of (1-frac)/(1+frac)) results in the allpass coefficient spending far less time in the extreme coefficient settings. However, quantizing the coefficients to 256 settings would also help with this.

As far as delay based allpasses having their coefficients being set too close to 1.0, I have heard this in a few commercial systems. One was the reverb that came with the original Unreal video game engine, that was clearly an allpass cascade with no global feedback, similar to the original Schroeder design, or to Chamberlin's reverb in his book. The allpass coefficients were used to control the reverb decay, which became obvious when really long reverb settings resulted in the straight signal becoming much louder than the reverb signal. I can cut them some slack, as having a reverb at all was an admirable achievement for video game engines at the time. The reverb sounded better than the Half-Life engine, for example.

My Ensoniq DP/2 also seems to have the ability to set the allpass coefficients way too close to +-1.0. The Large Hall algorithm sounds similar to the PCM70 Concert Hall algorithm that I have heard, but the Ensoniq has STUPID coefficient ranges. Turning up the Definition to 99 seems to set some of the loop allpasses to coefficients of 0.99. I don't mind giving the user enough power to do cool things, but giving someone raw control over this, without explaining what ranges to avoid, will inevitably result in horrible sounding patches.

Sean

---

### Post #85 -- Page 3
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 7th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4162606&postcount=85>

It's interesting that you brought this up right now. I've just gotten most of the 'basics' on my DSP56366 reverb working. No presets, no saving of effects, and only a single algorithm. But I can vary the parameters manually, and reload firmware to adjust the algorithm.

Just to test the performance, I set up 72 output taps, three loops, eight allpasses, and two low-pass filters. That all takes 8.3 microseconds. That ends up being about double that (double the speed - half the time) of an AL3201, or I would guess about three times the performance of a Lexichip, which isn't hugely fast, but not bad, either. But I can see how I could cut that almost in half - I just need to rewrite the multitap summer to not waste half of the clock cycles in pipeline stalls.

Anyways, glides and chorus are the next set of algorithms I want to look at. One option I was thinking of was making a high-boost EQ after the interpolate that varied its coefficient with the rate of change of the modulation signal in order to compensate for the high frequency loss. Similar idea to having the read head speed change in a BBD - if you decrease the read head speed you get a lower pitch. With a moving tap, the tap 'sees' each sample for a slightly different amount of time - longer time seeing a sample when moving in the same direction as the signal, shorter time when moving towards the read head (lower pitch when moving towards or away from the write pointer?) It seems to me that it's the duty cycle change that causes the filtering - and a boost EQ that varies with the duty cycle change should at least partially compensate for the first-order loss. I wonder if that actually makes any sense.

---


## Page 4

---

### Post #91 -- Page 4
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 30th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4233620&postcount=91>

You are really going to town with your new designs.

248k words is still a little short for the best quality at 48kHz. Why not SRC down to 16kHz? Now you have the internal memory to do a really nice reverb. I think this is a reasonable tradeoff.

-Casey

---

### Post #92 -- Page 4
**User:** Deleted ab87343
**Info:** Posts: n/a
**Date:** 30th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4233729&postcount=92>

> *Originally Posted by dale116dot7:*
> NS: That's enough RAM to do some sampling like the 480L SME. Any programs like that on the '96?

A few people liked the SME board on the 480, but it was never a good seller. I think there are many superior solutions for sampling and sample replacement. Don't think you'll be seeing it on the PCM96.

---

### Post #93 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 30th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4234097&postcount=93>

> *Originally Posted by Casey:*
> You are really going to town with your new designs. 248k words is still a little short for the best quality at 48kHz. Why not SRC down to 16kHz? Now you have the internal memory to do a really nice reverb. I think this is a reasonable tradeoff.

Could do that, I guess. Or what I was thinking is putting longer stuff - long delays - into an external SDRAM, and keep shorter things in internal RAM. There's a bit of overhead there, but not so bad if I manage memory movement. I guess another approach, actually, would be to daisy-chain two 56721's (actually, it's the 56720 with external SDRAM interface - the 56721 has no external memory interface but you can get it in an 80-pin LQFP which is relatively trivial to solder). Anyways, two daisy-chained units with a couple of serial lines between them should work, although you have to design the algorithms to keep that in mind. But there's a lot of serial I/O ports available, so shuffling data back and forth wouldn't be that bad. I know that the PCM8x, PCM9x, 480L, and REV7 all used two (or more) DSP cores and passed some amount of data back and forth. The REV7 uses a serial line between the two cores, so it can't be that much data there. Given that the 563xx family really isn't that quick, perhaps using two of them isn't such a bad idea with that amount of memory on each chip. The parts are $14 in 1k quantities, so popping a pair of them on there really isn't such a bad thing.

I like to design things, and I usually like to have a jumperless design, so I do one layout and get it about right, then I do one 'final' layout, then make maybe half a dozen of them, then I move on to the next project. With the reverbs, the host software seems like the majority of the work. The actual DSP software is relatively trivial in terms of building blocks. Including init code, the DSP code sits in just under 512 words. The host code is in 'C' and compiles so far into about 49000 bytes - and I only have the basic effect editor, preset fetch, and reverb setup stuff in place. I don't have any MIDI code yet, nor storing effects into EEPROM, nor a way to fetch them from EEPROM. I can only do presets so far. My wife just can't believe how much effort goes into one of these boxes. She was mostly surprised that it only took me about a week to go from a concept to having a prototype built in a box, then several months of intense work on software before it even makes a squeak.

---

### Post #94 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 30th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4234107&postcount=94>

> *Originally Posted by Nobody Special:*
> A few people liked the SME board on the 480, but it was never a good seller. I think there are many superior solutions for sampling and sample replacement. Don't think you'll be seeing it on the PCM96.

Yea, I guess that's probably right. I'm still a bit of a luddite in that I don't have a PC or Mac anywhere near my studio, so for sampling I need hardware to do that. But even in the hardware world, there are boxes made specifically for sampling. I guess if I wanted to do it, I could just write up some more software.

---

### Post #95 -- Page 4
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 30th May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4235441&postcount=95>

> *Originally Posted by Casey:*
> 248k words is still a little short for the best quality at 48kHz. Why not SRC down to 16kHz? Now you have the internal memory to do a really nice reverb. I think this is a reasonable tradeoff.

Ahhh, you kids nowadays, with your 30+ seconds of fast delay memory, and your Blackfins, and your bang bang music!

In all seriousness, isn't 248k x24bits about 5 seconds of fast delay memory @ 48 kHz? Older reverb designs got by just fine with about 1 second of delay memory; double or triple that and things can sound really nice. I would doubt that a single Freescale DSP would have the cycles to fill up 15 seconds of memory with enough taps / allpasses / whatever to get the required echo density.

> *Originally Posted by Casey:*
> You are really going to town with your new designs.

Dale is a sharp guy.

Sean

---

### Post #96 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 31st May 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4237934&postcount=96>

> *Originally Posted by seancostello:*
> In all seriousness, isn't 248k x24bits about 5 seconds of fast delay memory @ 48 kHz? Older reverb designs got by just fine with about 1 second of delay memory; double or triple that and things can sound really nice. I would doubt that a single Freescale DSP would have the cycles to fill up 15 seconds of memory with enough taps / allpasses / whatever to get the required echo density.

That, and memory bandwidth, too. I'm not sure what the performance of some of these ADI DSP's are, but the 56k seems slow. The only reason that I am sticking to it is relative ease of programming, cheapness of dev tools, and not insignificantly, ease of soldering a prototype together. BGA's offer great packaging density but prototyping is a bit of a bear. I'm actually having a problem finding 1.8V SDRAM in TSOP packaging - I can find 90-ball BGA's but I don't want to solder those down. Level-shifting takes too long on a high-speed bus and I don't want the extra time delays.

I just did up a brute-force reverb using two strings of about 25 or so allpasses in a row followed by a single-pole HF rolloff filter. Eight of the allpasses modulate. It's a bit unnatural but huge sounding. About 50 allpasses and eight modulations take about 10 microseconds and I'm running the processor at 96 MHz, and one wait state to delay RAM. Cascaded allpasses could be written more efficiently, because I wrote my allpass to assume that take a delay line and run the input into the allpass, then write the output back to RAM. I think cascaded allpasses could have about double the throughput if I optimized things for cascading without delays between them.

The processor can run at 120 MHz but I run it a bit slower because at 120 MHz I run out of setup time for the SRAM address and I would have to add one wait state which would slow things down. The 56720 would not have that problem as with that much RAM on-chip, I could run full-tilt and not worry about wait states. Ahh, the life of the hardware designer.

-Dale

---

### Post #97 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 5th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4253483&postcount=97>

I've been playing around with various gain multipliers, and what I've managed to figure out is that it is relatively easy to make a set of tap spacings and gains sound good, but resizing it or changing the RT makes everything have to change - just doing a linear (or log or power - depending on what is being changed) ratio doesn't seem to work quite right.

Is there a better approach than going to every size and RT combination and tabulating a couple dozen gain and tap locations - resorting to massive lookup tables? Or is it a case of needing to work harder at getting 'optimum' tap spacing and gains that work well for a wide range of size and RT settings? That is my biggest struggle now - I can tweak things to sound good but then I change the size from 18 metres to 25 metres and everything sounds horrible until I tweak almost every gain and tap location in the loop. It's like you get combing come in and out at some sizes. I've checked tap locations and gains being calculated (a debug screen), and so far I can't see anything being calculated wrong.

---

### Post #98 -- Page 4
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 5th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4253709&postcount=98>

> *Originally Posted by dale116dot7:*
> Is there a better approach than going to every size and RT combination and tabulating a couple dozen gain and tap locations - resorting to massive lookup tables?

What are you modulating?

Are any taps in the feedback portion of an allpass?

Or are you first getting your basic loops set up with out allpasses?

It is certainly possible to have a single set of taps with constant ratios that are scaled with size, or used with any number of RT values.

-Casey

---

### Post #99 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 5th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4253933&postcount=99>

> *Originally Posted by Casey:*
> What are you modulating?

I've done a bit on various portions - taps, allpasses, loop size. But if I turn modulation off, I don't get nearly as smooth of a response as, say, any of the algorithms on my PCM91 with their chorus functions also turned off. I check for chorus being turned off by watching for modulation with a tone. Sometimes strange things will cause chorus enabling like using spread and shape in the random hall algorithm.

I can modulate up to eight taps at once. I have not set up a queue structure, though, to allow modulation or glides of more than eight taps 'in turn' - where eight things modulate simultaneously, then you sub out something that is modulating with another tap that is frozen - rotating the modulations. I could do that, I just haven't written the code to do that because I thought that eight modulating taps should be enough.

> *Originally Posted by Casey:*
> Are any taps in the feedback portion of an allpass?

I've done it both ways. With high allpass gains (any higher than about 0.6) the signal in the feedback portion appears a bit odd. But at allpass gains less than about 0.4, the audio in the feedback portion of a lattice allpass appears pretty useable - it doesn't really sound odd to me.

> *Originally Posted by Casey:*
> Or are you first getting your basic loops set up with out allpasses?

Yes, and I do find that the combing comes and goes with or without allpasses. It has to be created by interference between tap locations. At high gains, the allpasses have a 'grainy' or 'ringy' sound to them with impulses. It doesn't sound allpass but it measures that way. You can hear them get 'excited'. With real audio, that mostly goes away. But if I run the same test with the PCM91, there is still a repeating pattern, but the grain goes away and that makes the excited frequencies not sound so much. It does even without chorus turned on. Should I be changing the feedback gains on the allpasses based on the allpass length or size?

Would a valid way of figuring out reasonable allpass gains would be to change the allpass into a comb by imbalancing the feedback and feedforward terms, then adjust the gains to flatten the frequency response of the combined combs? I have a feeling that if I can manage to get a flatter allpass response, I should have a better sounding algorithm. Or perhaps feed an impulse in it and do an FFT of the result and adjust the gains to flatten it?

> *Originally Posted by Casey:*
> It is certainly possible to have a single set of taps with constant ratios that are scaled with size, or used with any number of RT values.

I would have guessed that it should be done that way - the RT should change the recirculation gains, and size should be able to just resize the array linearly. But I've been struggling a bit to get it all to work - not from a technical perspective because that is just plain coding - but from an sound point of view - something that sounds good.

For reference, I set up the 'infamous' Dattorro/Lexicon algorithm, and that algorithm does sound pretty good using the same building blocks as what I am using for the newer algorithms. I did that just as a sanity check to make sure that the base building-block algorithms are doing what I expect them to do. It sounds similar to (though not exactly like) a PCM91 'Room' setting.

-Dale

---

### Post #100 -- Page 4
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 5th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4253996&postcount=100>

> *Originally Posted by dale116dot7:*
> I can modulate up to eight taps at once. I thought that eight modulating taps should be enough. Yes, and I do find that the combing comes and goes with or without allpasses. It has to be created by interference between tap locations.
>
> At high gains, the allpasses have a 'grainy' or 'ringy' sound to them with impulses. It doesn't sound allpass but it measures that way.
>
> Should I be changing the feedback gains on the allpasses based on the allpass length or size?

How are you modulating the taps? How many taps do you have. What is your tap spacing in msecs?

An allpass is flat. The ringing comes from the frequency dependent delay of an allpass. So some frequencies stick around longer than others. This is particularly noticable at higher RTs because the same signal goes through the same allpass multiple times. If you can change the allpass before the same signal hits it again, then the ringing can be reduced.

Generally longer allpasses will ring more because they have longer delay vs frequency times. So reducing the gain on larger allpasses is useful.

-Casey

---

### Post #101 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4254783&postcount=101>

> *Originally Posted by Casey:*
> How are you modulating the taps? How many taps do you have. What is your tap spacing in msecs?

Triangle with random (or maybe not random enough) direction changes, amplitude of maybe 1ms, at about 1/2 Hz. The tap spacing of my larger tap count algorithm - three loops but lots of taps per loop - varies as per the room size, so it will vary from maybe a millisecond up to maybe 30 or 40 milliseconds at larger room sizes.

> *Originally Posted by Casey:*
> An allpass is flat. The ringing comes from the frequency dependent delay of an allpass...

So perhaps I have to make sure that the triangle ramp rate and the loop time don't make a pattern so that the allpass times aren't ever the same one pass through - even maximize the difference if possible. Would putting a small modulated allpass within the feedback of another allpass break up that one ring? I know putting a modulated tap for the feedback tends to reduce ringing, but would another small allpass help more, or just hurt things more? I would think that it should break up the 'mode' into three or maybe four different frequencies.

> *Originally Posted by Casey:*
> Generally longer allpasses will ring more because they have longer delay vs frequency times. So reducing the gain on larger allpasses is useful.

I should do that. I guess I could turn each allpass off in turn and adjust each gain to get the same length of ring time. That should mask the ringing.

I'm playing shows most of this weekend, so I doubt I'll get much work done on the 'verb. I'm playing upright bass with a folk/bluegrass group tonight.

---

### Post #102 -- Page 4
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4254911&postcount=102>

Dale, Something that Barry Blesser and others did back in the 1970s with the EMT and also Lexicon is to add random amplitude modulations, particularly in the feedback loops...

---

### Post #103 -- Page 4
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4255251&postcount=103>

> *Originally Posted by zmix:*
> Dale, Something that Barry Blesser and others did back in the 1970s with the EMT and also Lexicon is to add random amplitude modulations, particularly in the feedback loops...

Uhhhh, No.

-Casey

---

### Post #104 -- Page 4
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4255290&postcount=104>

> *Originally Posted by dale116dot7:*
> Triangle with random (or maybe not random enough) direction changes, amplitude of maybe 1ms, at about 1/2 Hz.

Try 10ms at 2 Hz

> *Originally Posted by dale116dot7:*
> The tap spacing of my larger tap count algorithm...

Tap spacing should be such that there is a good chance that the delay between taps can be seen as enough to assure decorrelated signals. Statistically it turns out that 50ms or more will work on average over many tap pairs. Without statistical decorrelation you will have, as you have found, very strong comb filtering effects.

> *Originally Posted by dale116dot7:*
> So perhaps I have to make sure that the triangle ramp rate and the loop time don't make a pattern so that the allpass times aren't ever the same one pass through

Yes!

> *Originally Posted by dale116dot7:*
> Would putting a small modulated allpass within the feedback of another allpass break up that one ring?

No! The larger allpass will dominate.

-Casey

---

### Post #105 -- Page 4
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4255346&postcount=105>

> *Originally Posted by Casey:*
> Uhhhh, No.

I had thought the same thing (that the loop feedback had random amplitude modulation), when looking at the Blesser patent, as well as a 1978 book chapter that he wrote. In the book chapter, Blesser shows a chorus, with several delay taps that are randomly modulated both in delay length and in amplitude. In his 1980 patent (I think that's the date), it seems as though the feedback taps are modulated in amplitude. However, I think that was Blesser's way of describing linear interpolation, or at least some random cross fading between two taps which may or may not be contiguous to each other, as opposed to a single tap that is randomly amplitude modulated. That part of the patent is confusing to me.

The patent does describe random amplitude mixing of the tap outputs, but this is different than random amplitude in the feedback loops. Plus, I am not confident that the EMT-250 is really that close to the patent, although I would think that at least a few of the claimed ideas were used in the EMT-250.

I have tried random amplitude modulation in the feedback loops, and the result is a very uneven decay. It doesn't sound good, IMO. Delay length modulation sounds good in feedback loops. Other types of modulation can sound good, but you want to maintain as flat a magnitude response as you can with the modulation, and also avoid building up enough energy to make the system unstable. You want to preserve the total energy of the system, and be specific with your losses - i.e. have the losses controlled as a factor of RT60.

Sean

---

### Post #106 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4256612&postcount=106>

> *Originally Posted by Casey:*
> Try 10ms at 2 Hz. Tap spacing should be such that there is a good chance that the delay between taps can be seen as enough to assure decorrelated signals. Statistically it turns out that 50ms or more will work on average over many tap pairs. Without statistical decorrelation you will have, as you have found, very strong comb filtering effects.

Perhaps that is why an algorithm that sounds good at as big of a setting as possible may sound good, but as the size goes down, the combing gets worse? Would I be smart to fade taps out (so they drop out gradually) at small sizes? A tap spacing of 50-80ms at canyon size becomes 5ms in a smallish living room. Keeping the same amount of chorus becomes much more noticeable in a small size. A 50ms tap spacing would result in a 20 Hz peak which is nice and low. At 5ms it gets to be 200 Hz - mudfest.

Or should I be looking at changing the tap gains - rather than trying to get a smooth decay, try to reduce combing by alternating and modifying tap gains somehow? I've been adjusting them for a smooth decay at canyon sizes so far. I would think that alternating tap gain signs would change the combing but maintain the density - maybe to half the frequency? What about applying acoustical diffusor patterns to the tap gains, spacings, and signs? Those equations are pretty well known, and I think I have them in an acoustic design book I have somewhere.

---

### Post #107 -- Page 4
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4256832&postcount=107>

> *Originally Posted by seancostello:*
> I had thought the same thing (that the loop feedback had random amplitude modulation)... I have tried random amplitude modulation in the feedback loops, and the result is a very uneven decay...

Sean, Both from papers that Dr Blesser has sent to me and the reading of the original patents I have seen references to amplitude modulations. I have had good results with small random amplitude fluctuations in the feedback loop (very small, less than a dB).

Casey, care to elaborate with something more insightful than "no"? (please...?)

---

### Post #108 -- Page 4
**User:** Warp69
**Info:** Lives for gear | Joined: Sep 2004 | Posts: 714
**Date:** 6th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4257359&postcount=108>

> *Originally Posted by zmix:*
> Dale, Something that Barry Blesser and others did back in the 1970s with the EMT and also Lexicon is to add random amplitude modulations, particularly in the feedback loops...

What do you mean by amplitude modulations in the feedback loop? Amplitude modulation of what? Gains? Taps? Coefficients?

---

### Post #109 -- Page 4
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 7th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4257465&postcount=109>

According to [Dr Blesser's patent](http://mixonline.com/online_extras/blesser-patent.pdf), quoted below from column 4 line 67 on:

> FIG. 3 shows in more detail a part of the loop which is shown in FIG. 2, including the delay circuit 4 or tA.
>
> **Outputs from the delay circuit 4 or tA are fed back to the summing circuit 6 at the input of the delay circuit through a plurality of damping elements**, of which two damping elements **gz1** and **gz2** are shown.
>
> **These damping elements are operated by known random noise generators or random signal generators** which are not shown.
>
> Control of the damping elements by signals from the random noise generators is schematically represented by Z1 and Z2 for the two damping elements **fz1** and **fz2** shown. In the same way as in FIG. 2, a further damping element **g1** is provided in the feedback line.
>
> The outputs of the damping elements fz are furthermore connected to the summing circuit 8 at the output 9 of the loop, though this is not shown in FIG. 3. The circuit arrangement shown in FIG. 3 provides a random-controlled length variation of the delay times.

**Attached:** fig-2-fig-3.jpg (Blesser patent figures)

---

### Post #110 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 7th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4258592&postcount=110>

> *Originally Posted by zmix:*
> According to Dr Blesser's patent...

It may be in a patent, but how is it implemented, or is it even in a product? The only ways to tell are to either ask him (and he may not remember), or read the ROMs and disassemble the code and figure out what it does - and I would guess for an EMT250 that might take three to five months after you have a copy of the ROMs. A schematic would be useful here. Having an EMT250 and a logic analyzer hooked up to its guts is an alternative, though I don't know many people with logic analyzers lying around in their basements.

As he refers to variable damping in the text, to me that would imply to me that he is likely talking about the variable frequency response of a gliding tap using linear interpolation - that provides close-to-random damping, and essentially, a random amplitude variation of high frequency content, though practically no variation at low frequencies.

If the main processor is not synchronized with the DSP and can't update the chorus coefficients fast enough, there will be an amplitude variation some of the time, when the two values (1-x) and (x) are not correct. If you have this happening, you can't chorus very quickly before you get nasty modulation noise.

---

### Post #111 -- Page 4
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 16th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4288976&postcount=111>

> *Originally Posted by dale116dot7:*
> If the main processor is not synchronized with the DSP and can't update the chorus coefficients fast enough, there will be an amplitude variation some of the time...

This is assuming that (1-x) is being calculated on the host, and not on the DSP. For that matter, the modulation signals might be generated on the DSP as well. I always generated my modulation signals on the DSP, although this was due to being limited to generic hardware - the EZ-KITs didn't have embedded microcontrollers of any note.

Sean

---

### Post #112 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 18th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4293438&postcount=112>

Yes, that is the assumption there. If the AES Blesser paper (the one describing the hardware of an audio processor) describes the EMT250 processor, then the DSP does have the primitives needed to make an oscillator and fiddle with addresses. Something like the M200/PCM70/480L, also the Lexichip1 and 2 requires the host to do it. Since the service manuals for the 480L and LXP15 tell you that the slave Z80 is used to implement the pitch shift and chorus functions, as well as ramped coefficient adjustments, I'll take the manuals at their word.

I've done my LFO's on the host, though I plan on moving that over to the DSP when I get around to it. I did it on the host because it was just faster for me to write it that way. The only problem I have with that approach is that for a single chorus, the update rate is fine, when you have half a dozen of them, I can only update them at about 2kHz or so - and at high chorus rates, you get modulation noise at that frequency. I used the serial host interface, and that is the limiting factor. Had I used the faster parallel host interface and a processor with DMA, I could have easily done the chorus functions on the host, with a 1WC or maybe at most 2WC update of all of the chorus values.

---

### Post #113 -- Page 4
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 18th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4293505&postcount=113>

> *Originally Posted by dale116dot7:*
> I've done my LFO's on the host, though I plan on moving that over to the DSP when I get around to it...

Is this due to the inability to update x and (1-x) at the same time, or due to quantization of the modulation signal? I used to perform chorusing at 1/10 to 1/16th of the sample rate, and it sounded fine. However, maybe my ears weren't as good. If the problem is due to sync errors with the 2 linear interpolation coefficients, a few ideas:

- Calculate x on the microcontroller, and 1-x on the DSP. It will take an additional cycle or two per interpolation, but it might fix the problems.

- Use 1st order allpass interpolation. This works with a single coefficient - read Dattorro pt. 2 for details. Sounds nice for reverb modulation, not good for pitch shifting.

Sean

---

### Post #114 -- Page 4
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 18th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4293826&postcount=114>

I calculate x and x-1 on the micro, then send it to the DSP - into a buffer. The DSP waits until the end of the reverb loop, then copies any queued coefficient and address updates from the buffer into the main parameter memory.

[Post truncated in fetch]

---


## Page 5

---

### Post #121 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 22nd June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4307435&postcount=121>

> *Originally Posted by zmix:*
> Hi Sean, Have you ever listened to a Bode Frequency shifter?

I have been programming these since 1999 - it was one of my first goals in learning digital audio. I've done a lot with them since then, including putting them in the feedback path of allpass loop reverbs. I didn't like the results that much, at least as far as producing a modulated reverb sound.

> *Originally Posted by zmix:*
> There is a fair example in the Logic built in plugins called "Ringshifter"...

Here's a way to test things:

Run sine waves of different frequencies (100 Hz, 500 Hz, 1000 Hz, 2000 Hz) through the algorithms in question. See if the beat rates sound similar. If the beat rates are similar, then the modulation is some form of amplitude modulation (which frequency shifting can be classified as in some weird sense), which produces a beat rate that does not vary with input frequency. If the beat rates get higher with the input frequency, it is probably delay modulation.

> *Originally Posted by zmix:*
> The chorusing LFO in the PCM96 sounds like a square wave and has a maximum rate of 1.5hz. It is not randomized.

This sounds like the modulation produced by a triangle wave LFO, which produces an up/down modulation when used to modulate a delay line. In most digital systems, a square wave LFO ends up producing different delay lengths with no pitch change, except for a glitch when changing between the LFO output values.

Of course, this is based on one method of calculating delay modulation, while other methods could result in a square wave LFO producing the up/down modulation, and a triangle wave sounding more like a sine wave. It all depends if you are adding the modulation as an offset to your delay address, or doing something else. For BBD-based effects, the delay modulation LFO is usually controlling the clock rate, so a square wave LFO can end up producing an up/down pitch change.

Sean

---

### Post #122 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 22nd June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4307545&postcount=122>

Excellent points, Sean.

The modulation artifacts I'm demonstrating here may not be phase shift networks but the tonality is similarly disturbing. I just cannot believe that these algos made it to final release... When the original EMT 250 and 224 were developed the sheer man hours involved in listening and tweaking must have been boggling.!

---

### Post #123 -- Page 5
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 23rd June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4309599&postcount=123>

> *Originally Posted by zmix:*
> When the original EMT 250 and 224 were developed the sheer man hours involved in listening and tweaking must have been boggling.!

Not mind boggling, just dedication to the art. Anything less shows a lack of respect. Today we have examples of mad love available at every level, including free...

...the memories of sounds that once held sway, like apartment lights passed by on the freeway, are life scenes that just begin to register, replaced by two point beams, fading the once best or, yield an ambassador, to a new world held, by those that care and are willing to spell, the towers, and glory, of the past elite, that will be troubled, humbled, and without a seat, no beat, because the music stops, in the time they keep...

-Casey

---

### Post #124 -- Page 5
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 23rd June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4309633&postcount=124>

I've been working on less fun parts of the reverb. Being able to store a user-defined effect, edit its name before storing it, and dumping effects via MIDI to a PC for eventual inclusion into the presets - or just for storage. No new algorithm news yet, I was getting frustrated with the lack of storing carefully created effect settings so I decided to take many days and write all of that code. The most bearish code was writing to the flash. If it's wrong, the processor just resets thanks to the watchdog timer, with little evidence to lead you to the problem. What ends up happening is the flash memory gets taken over by the programming instruction, and if it's wrong, the flash does not return to the CPU and the program just goes bye-bye. Anyways, that's working, including a plea to please name the effect something meaningful. I used a 2x40 display and my effect names are 30 characters long.

Next order of business is to calculate the RT's for display in a more meaningful way. Just trying to get some cleanup done before getting too far ahead of myself.

---

### Post #125 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 23rd June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4310298&postcount=125>

> *Originally Posted by Casey:*
> Not mind boggling, just dedication to the art...

Preaching to the choir here Casey... I appreciate the intense amount of work involved in voicing a reverb. I certainly spend weeks listening listening listening then making small tweaks, and more listening listening. I wonder if a publicly held company can afford to postpone a product release until it's 'right'? Perhaps I should post those PCM examples with the modulation OFF so that my point is a bit more obvious. Maybe if I hadn't spent the last several decades "immersed in reverb" I would agree with the reviewers... Barry Blesser describes this phenomenon nicely in an AES paper he sent to me recently:

> **Barry Blesser:**
> An artificial reverberation algorithm designed by an amateur is likely to sound very good to an inexperienced listener. The author, who has spent hundreds of hours listening to artificial reverberation algorithms, has informally observed an improvement in sensitivity to certain subtle artifacts by at least 20 dB. Informal learning is not always apparent. Designers of artificial reverberators and virtual auditory displays must therefore be warned: users often experience an unintentional learning after extensive use. By transforming themselves from naive listener to "golden ears," they can become intolerant to the "degraded" performance. It is hard to predict whether the tolerance to imperfections will rise or fall with use, since both happen.

---

### Post #126 -- Page 5
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 24th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4314002&postcount=126>

> *Originally Posted by zmix:*
> I wonder if a publicly held company can afford to postpone a product release until it's 'right'?

Thanks to flash memory, that's less of an issue than it used to be. You can send out a product with known deficiencies or maybe just missing that last algorithm that isn't right, then send out an update that users can do with little more than a USB cable or a MIDI adapter.

---

### Post #127 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 24th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4315601&postcount=127>

> *Originally Posted by zmix:*
> The modulation artifacts I'm demonstrating here may not be phase shift networks but the tonality is similarly disturbing. I just cannot believe that these algos made it to final release...

My guess is that they are intentional, not accidental. What sounds bad to some ears can sound great to others. The modulation may sound bad on piano, but really nice on drums. Some aspects of the PCM96 may have been half-baked upon release (the Firewire implementation sounds like it had some issues), but the algorithm developer has been developing reverbs at Lexicon for the better part of a few decades at this point, so I am sure that all sonic artifacts are intended.

I will admit that the chorus on the PCM96 Concert Hall sounds very dissimilar to the PCM70 Concert Hall chorus, so I am wondering how accurate of a port there was of the 224 Concert Hall. However, it has been close to 2 decades since I have worked with a 224XL, and I have never seen a 224, so maybe this is what it sounded like.

Sean Costello

---

### Post #128 -- Page 5
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4317013&postcount=128>

> *Originally Posted by zmix:*
> I appreciate the intense amount of work involved in voicing a reverb...

So many right words.

---

### Post #129 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4317333&postcount=129>

**ET (Eigentone) phone home**

I've decided to post another comparison of the PCM96 "Concert Hall" and the PCM-70 (while I am waiting for the 224 to arrive).

This time the reverbs are in STEREO and you will hear the 'wet' signal only.

In order to hear the tail better, I stretched the decay out to 6.3 seconds. All settings are the same on each unit, no early reflections, however, I found that I needed to increase the size of the PCM96 to 53m in order to match the loop length of the PCM-70 at 33.3m...

In the previous examples you could hear that the PCM96 modulation was quite different from the 224/PCM70 modulation. Now you will hear what the algos sound like with no modulation....

**Attached Files:**
- [No Mod PCM70 Concert Hall 6.mp3](https://gearspace.com/board/attachments/geekzone/126353d1245937565-reverb-subculture-no-mod-pcm70-concert-hall-6.mp3) (975.4 KB)
- [No Mod PCM96 Concert Hall 6.mp3](https://gearspace.com/board/attachments/geekzone/126354d1245937565-reverb-subculture-no-mod-pcm96-concert-hall-6.mp3) (975.4 KB)

---

### Post #130 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4317504&postcount=130>

> *Originally Posted by zmix:*
> Now you will hear what the algos sound like with no modulation....

The algorithms sound more similar without the modulation. They also sound SUPER ringy.

Sean

---

### Post #131 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4317561&postcount=131>

> *Originally Posted by seancostello:*
> The algorithms sound more similar without the modulation. They also sound SUPER ringy. Sean

Can you be more specific or elaborate on your observations a bit for us? Also, you mentioned above that: "the algorithm developer has been developing reverbs at Lexicon for the better part of a few decades" who are you referring to?

When I listen to these I do not find these two versions of the same algo all that similar...

Listen to the stereo spread. What accounts for the narrow phasey tail in the PCM96?

As for the actual algo design, I find that the ringing in the PCM-70 is much more benign and shows better eigentone distribution than the PCM96. The PCM96 actually changes the chord voicing of the piano! This characteristic is present in ALL of the PCM96 algos, btw.

Why do we modulate taps and FB in the first place? To tame the runaways! The chorusing in the PCM-70 (and the 224) is magical and lovely. The PCM96 is cyclic, grindy and not very pretty. Combine the wooley ringy algos and unsatisfying modulation and we have... a commercial release from a major brand name?

Is there no 'there' there anymore?

---

### Post #132 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4317955&postcount=132>

> *Originally Posted by zmix:*
> Can you be more specific... who are you referring to?

Nobody Special - the user name on Gearslutz, not a snide answer. Check out his Gearslutz profile. Also, read his posts on the Lexicon bestiary thread:

[Lexicon reverbs: a brief bestiary](https://gearspace.com/board/high-end/362930-lexicon-reverbs-brief-bestiary.html)

> *Originally Posted by zmix:*
> Listen to the stereo spread. What accounts for the narrow phasey tail in the PCM96?

It sounds wide to me, but I am using headphones. I would think that there might be a difference between the mono summing of the PCM70, and the true stereo of the PCM96 (and the 224).

> *Originally Posted by zmix:*
> As for the actual algo design, I find that the ringing in the PCM-70 is much more benign...

I just hear discrete echos and metallic allpass ringing in both of the reverbs with the modulation off. It seems like this particular algorithm REQUIRES modulation to sound halfway decent. The PCM70 sounds like it has a bit more high frequency attenuation, but I hear some very pronounced sine waves ringing out in the tail. If I listened closer, I could probably hear more subtle differences, but since both of the algorithms sound bad without chorusing, this is where I will stop.

If the Concert Hall algorithm is as dependent on modulation as your examples would indicate, then the particular type of chorusing is probably critical to the sound.

Sean

---

### Post #133 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4317989&postcount=133>

Not taken as snide, Sean...

> *Originally Posted by seancostello:*
> It sounds wide to me, but I am using headphones.

1: you cannot image using headphones.
2: Mono source in both cases, and this shouldn't affect the tail. I am convinced that there is something wrong with the PCM96 routing.

I'll post more examples of different algos. I cannot afford to 'stop' as you say since I'm trying to incorporate this box into my current mix setup, or bail on it entirely. As it stands I may have to stockpile vintage Lex parts unless I can get to the bottom of this 96 voicing problem.

---

### Post #134 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318069&postcount=134>

Not to toot my own horn or anything (and I will now proceed to do so), but have you checked out Eos? Chris Randall is a big fan of the PCM70 Concert Hall algorithm, so I designed something with a similar sonic goal, but with less coloration (even with modulation turned off) and more echo and eigenmode density. It isn't a Lexicon clone, so there are undoubtedly sonic characteristics that are far different from the PCM70, but I think it sounds pretty good. The modulation is different from both of the Concert Hall examples you posted, so it will not directly emulate that part of the PCM70, but I can get similar results with reduced modulation depth and increased modulation speed.

Sean

---

### Post #135 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318324&postcount=135>

Sean, Eos sounds quite interesting, it is certainly very 'pretty' (which is exactly what I was hoping for from Lexicon).

Congrats on a successful product...!

Quite a bold move to leave off the size parameter...why?

---

### Post #136 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318368&postcount=136>

> *Originally Posted by zmix:*
> Quite a bold move to leave off the size parameter...why?

Size is on the top left, second parameter down. Under predelay, over decay.

Sean

---

### Post #137 -- Page 5
**User:** Warp69
**Info:** Lives for gear | Joined: Sep 2004 | Posts: 714
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318527&postcount=137>

> *Originally Posted by zmix:*
> 2: Mono source in both cases, and this shouldn't affect the tail. I am convinced that there is something wrong with the PCM96 routing.

Do you feed both channels with the same signal on the PCM96?

---

### Post #138 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318601&postcount=138>

> *Originally Posted by Warp69:*
> Do you feed both channels with the same signal on the PCM96?

Yes, a mono source to all reverbs.

---

### Post #139 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318637&postcount=139>

Here's an interesting contrast to the previously posted examples:

This is Sean's [Eos](http://www.audiodamage.com/effects/product.php?pid=AD023) reverb same settings as above, 33.3m, no modulation, 6.3s Hall algo etc...

**Attached Files:**
- [No Mod Eos Super Hall 6.3s.mp3](https://gearspace.com/board/attachments/geekzone/126407d1245962665-reverb-subculture-no-mod-eos-super-hall-6.3s.mp3) (975.4 KB)

---

### Post #140 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 25th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4318867&postcount=140>

**Plates mod and not**

Here are a collection of algo based HW and SW plate reverbs, with and without modulation. All 17.7m, 2.3/3.6 seconds, etc.

**Attached Files:**
- [NoMod PCM70Plate 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126409d1245966392-reverb-subculture-nomod-pcm70plate-17.7m-2.3s.mp3)
- [NoMod PCM96Plate 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126410d1245966392-reverb-subculture-nomod-pcm96plate-17.7m-2.3s.mp3)
- [NoMod SONY R7 Plate.mp3](https://gearspace.com/board/attachments/geekzone/126411d1245966392-reverb-subculture-nomod-sony-r7-plate.mp3)
- [NoMod Eos Plate1 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126412d1245966392-reverb-subculture-nomod-eos-plate1-17.7m-2.3s.mp3)
- [NoMod Eos Plate2 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126416d1245966867-reverb-subculture-nomod-eos-plate2-17.7m-2.3s.mp3)
- [Mod PCM96Plate 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126417d1245966867-reverb-subculture-mod-pcm96plate-17.7m-2.3s.mp3)
- [Mod Eos Plate1 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126418d1245966867-reverb-subculture-mod-eos-plate1-17.7m-2.3s.mp3)
- [Mod Eos Plate2 17.7m 2.3s.mp3](https://gearspace.com/board/attachments/geekzone/126419d1245966867-reverb-subculture-mod-eos-plate2-17.7m-2.3s.mp3)

---

### Post #141 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 26th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4319396&postcount=141>

> *Originally Posted by zmix:*
> Here are a collection of algo based HW and SW plate reverbs...

The mod rate and depth is set kinda high on the Eos examples, IMO. For the plate algorithm, I tend to set the freq around 0.7 Hz or so, and the depth around 1/3 to 1/2. The parameters give the user enough rope to hang themselves, if deliberately chorusy reverbs are desired, but the plate algorithms tend to work with lower amounts of modulation than the hall algorithm, at least when I was working with it.

Thank you for posting these examples, BTW. It is nice to hear the same audio example for all of these platforms. I haven't heard the Sony R7 before - it sounds quite nice.

Speaking of modulated halls, have you tried the Ensoniq DP/2 and DP/4 Large Halls in comparison with the PCM70 and PCM96? It was my understanding that these algorithms shared some DNA with the 224 algorithms.

Sean

---

### Post #142 -- Page 5
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 26th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4320069&postcount=142>

That was the point of my demonstration. I matched the modulation rate and amount in the PCM96 and the Eos specifically to illustrate the odd placement of the modulation in the PCM.. what were they thinking? I think that you've come very close to some of the 'prettier' reverb sounds I tend to gravitate towards with your Eos, but to my tastes it's the Plate 1 algo that has the best magic.

I have several early Sony reverbs. The R7 is the only 'modern' one. They are incredible. SONY put so much R&D into these algos.. and they are fantastic. Nothing in them is modulated or randomized, they are simply tweaked to perfection.

As I mentioned before, I worked as a consultant with Ensoniq to develop the DP/4+, DP/2 and ultimately the DP/Pro. Many of the reverb presets in the DP/2 and DP/Pro are my work. The DP/Pro has the famous "Dattorro algorithm". I pleaded with Jon to give me access to modulation for some of the taps and we did end up with a very powerful device. I own a DP/2, a DP/4+ and two DP/Pro (including one with a prototype Digital I/O). That piano track I have been using for the examples comes from a record I mixed a few weeks ago and on the actual mix, I used the DP/pro with a factory preset I created called "Black 224"....

I printed the reverb return back to tape, and here it is. Note the low density, high modulation and late 1970s primitivism....

**Attached Files:**
- [CZ DP Pro Black 224.mp3](https://gearspace.com/board/attachments/geekzone/126445d1245990784-reverb-subculture-cz-dp-pro-black-224.mp3) (422.4 KB)

---

### Post #143 -- Page 5
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 26th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4320315&postcount=143>

> *Originally Posted by zmix:*
> I think that you've come very close to some of the 'prettier' reverb sounds...

That algorithm is less Lexicon, more EMT. It isn't really EMT, any more than Superhall is Lexicon, but it shares some design goals. I've never heard an EMT-250 in person, so my understanding was based on impulse responses and the like.

> *Originally Posted by zmix:*
> I have several early Sony reverbs... SONY put so much R&D into these algos..

I am reminded of the Bricasti samples / impulses I have heard. Super high echo density (almost like convolution with noise), but with no ringing at all. The decay does not sound entirely exponential to me, which I am sure is by design.

> *Originally Posted by zmix:*
> The DP/Pro has the famous "Dattorro algorithm".

Is this "the" Dattorro algorithm, or "a" Dattorro algorithm? The Halls on the DP/2 I have sound considerably different from the Small and Large Plate algorithms, and much closer to the Lexicon PCM70 Concert Hall algorithm I have heard.

> *Originally Posted by zmix:*
> ...factory preset I created called "Black 224"...

Which algorithm? One of the Expert Reverbs?

> *Originally Posted by zmix:*
> Note the low density, high modulation and late 1970s primitivism....

Nice. It doesn't sound low density to me at all, but that could be the modulation masking this.

Sean

---

### Post #144 -- Page 5
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 26th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4321136&postcount=144>

Tuning is starting to drive me a bit crazy. There are a few things I'm hearing that I really need to understand a bit better how to solve. Allpass ringing. With modulation it smooths out standing wave buildup but there's still a lot of ringing when you hit it with something like a rim shot, unless the gains are set very low. But then the looping tap pattern is obvious. It's a grainy ringy sort of sound - a combination of the loop length and tap pattern (as you'd expect), along with a ringy allpass sound. The tap pattern you can change to randomize the sound, but even modulated allpasses have a periodic 'ringing' sort of sound.

Am I being too hard on myself or is a clean rim shot sound a good tuning tool? I find that running vocals or other instruments through pretty much any reverb seems to sound 'ok' unless you listen for a while to really tune your ears to it, but running a rim shot through it seems to point to faults in the algorithm or tuning right away. I've especially noticed that when I compare a PCM91 to the multi-loop algorithm from earlier, they both sound pretty good on vocals. But the sound is much smoother on the '91 on a rim shot - you can hear individual taps but all of the reflections sound pretty random in time.

I usually use the 'vocal magic' preset on the '91, that's probably my favorite vocal setting unless I'm doing something really dry - then I use some ambience setting, or something really spacey - then I use a PCM90 with a bunch of chorus and reverb and crank it up way too high.

---


## Page 6

---

### Post #151 -- Page 6
**User:** thermos
**Info:** Lives for gear | Joined: Jul 2004 | Posts: 7,654
**Date:** 27th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4323201&postcount=151>

> *Originally Posted by Casey:*
> David spoke with me many times and in great detail about the concert hall algorithm and the modulation methods it used. PM me.
>
> AFAIK David does still have the 224 code base. It was the 480 code base that was somehow destroyed.
>
> In fact, David has wondered as to whether it would make sense to re-release the 224 as a plugin. Perhaps he and Barry will get together. Barry has mentioned to me that he would like to re-release the 250. We were speculating on another thread that perhaps this is the reason that UAD has been talking up the 250 in their recent news letter.

What stops David and Barry from making plugs of them? Is it really whether or not people would be interested? Thats got to be one of the silliest questions and most obvious answers in the history of mankind. I hope we see those plugs some day. That would be a huge contribution to society.

---

### Post #152 -- Page 6
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 27th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4323257&postcount=152>

> *Originally Posted by Casey:*
> David spoke with me many times and in great detail about the concert hall algorithm and the modulation methods it used. PM me.
>
> AFAIK David does still have the 224 code base. It was the 480 code base that was somehow destroyed.
>
> In fact, David has wondered as to whether it would make sense to re-release the 224 as a plugin. Perhaps he and Barry will get together.

I love this thread.

---

### Post #153 -- Page 6
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 27th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4323299&postcount=153>

> *Originally Posted by thermos:*
> What stops David and Barry from making plugs of them?...

I agree.

-Casey

---

### Post #154 -- Page 6
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 27th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4324056&postcount=154>

> *Originally Posted by Casey:*
> AFAIK David does still have the 224 code base. It was the 480 code base that was somehow destroyed.

The code is obviously contained in many hundreds of EPROM's out there. If you really want source code regenerated from a binary image extracted from EPROM's, that technology exists. It's painstaking work, but I've had to do it a few times when source code went missing (ie the computer was stolen) or when a subcontractor went out of business and disappeared without leaving source code. But it can be done. If you wrote it the first time, and had to decipher it from an EPROM, it's not that bad. If it's written originally in assembly code, it's easier than if it was compiled from some other language. Not bad if you wrote the code in 'C' but a bear if someone else wrote the code and you are the one having to reverse it. If it's all fixed point (which my engine control projects always are), it's a lot easier than floating point (which I never use anyways). If you own the compiler that was used, it's also a lot easier because you can reverse the libraries and that gets all of the math subroutines defined. Try tracing through a floating-point divide routine... or is it a multiply routine or a square root.. I just can't tell.

---

### Post #155 -- Page 6
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 27th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4324529&postcount=155>

I need to correct myself.

As I was thinking back over the related conversation, it wasn't that David was thinking about doing a plugin, he was wondering about doing new algorithms for existing 224s.

Sorry for confusing the issue.

-Casey

---

### Post #156 -- Page 6
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 27th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4324946&postcount=156>

> *Originally Posted by Nobody Special:*
> Hmm. What's a programmer supposed to sound like on a B.B. thread?
>
> zmix, I'm sorry you've taken such a dislike to the PCM96. There are an awful lot of very good people in the industry who've told us it's the best-sounding box we've ever made...

Dear N.S.

In posting my comments and various examples I intended not to simply complain, but to open up a discussion with other reverb aficionados and to share what I am hearing in these algos, what I am missing, and hopefully to inspire Lexicon for further development of the PCM96 platform.

I have been mixing records professionally since the early 1980s. Back then I used the Lexicon 224, 224x, and later, the PCM 70. I sort of "lost interest" in new Lexicons reverbs around the time the 300/480 were introduced.

The primary attraction to the PCM96 for me was the claim that the original "Concert Hall" algorithm had been reintroduced. I bit hard on that lure. Imagine a 224 with instant recall! When I received my PCM96 I immediately began recalling some of my favorite 224 settings (by ear, not copying parameter values... which were obviously different in the PCM96). I could not get it happening and instantly buyers remorse set in.

Each algo shared a similar characteristic that I had never heard in my favorite Lexicons of the past. I can pinpoint the characteristic of the PCM96 as having excessive ringing in the lower frequency modes and an overly "tonal" quality to the reverb, certain notes would simply linger unnaturally and the end result was a muddy track with altered chord voicings. Using the modulation to break up these modes lead to a lumpy response and odd image shifts. I found that my programming became focused on taming artifacts rather than pursuing the sound I heard in my head.

Not happy to simply opine, I decided to measure the differences in the basic modulation LFO. First of all the PCM-70 modulation oscillator is a mixture of a 2.3hz triangle wave and a much slower random waveform (around 0.5hz). The chorusing LFO in the PCM96 has a maximum rate of 1.5hz, and is not randomized.

I am delighted that Casey has offered to discuss the 224 Concert Hall modulation with you. I think the PCM96 as a platform has tremendous potential and I'd love to see that realized.

-[Chuck Zwicky](http://www.esession.com/ChuckZwicky)

---

### Post #157 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 30th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4332341&postcount=157>

> *Originally Posted by zmix:*
> Note the low density, high modulation and late 1970s primitivism....

This sounds a lot like an effect and not a reverb, but I can imagine where it can be used. It has alot of Eventide style inside.

I'll look if I can add H8000 / Eclipse reverbs to this thread...

---

### Post #158 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 30th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4332346&postcount=158>

+1

---

### Post #159 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 30th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4332356&postcount=159>

Converting the 224 algo to a new machine would be an awesome plan. Or placing it inside for example the 96 platform. An interesting job for a good dsp-engineer... Not all vintage stuff is better, but these old machines have a really high quality level.

---

### Post #160 -- Page 6
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 30th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4332705&postcount=160>

Hi Harrie, I agree. How nice would it be to have those early algos preserved in a representative form! Look at how retro-obsessed the plugin market is at the moment.

-CZ

---

### Post #161 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 30th June 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4332806&postcount=161>

When I watch GS I see that there are quit a few oldies high on the 'best reverbs' list. That will be partly because of the hype, partly because of the sound. There are a lot of great sounding old machines to be ported over to newer formats.

These oldschool algos are fun to play around with. Generating enough randomness is important to making smooth and lush reverbs with this kind of reverbs.

When building reverbtanks (three series of four small delay blocks) I listen to first series of delays, spacing them up, then adding the next series. Then tweaking the second delaytimes so it generates the most smooth (least ringy) responce. I also did this with the third series. The outcome is a bit different when comparing it to the golden ratios known.

I am using VSIG on the H8000 for developing new algos. ATM we are porting some of those algos over to VST-format. I am amazed how much difference these ports make. VSIG is fast and fun to work with, but not always superaccurate.

---

### Post #162 -- Page 6
**User:** Casey
**Info:** Bricasti | Joined: May 2003 | Posts: 1,796
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4338688&postcount=162>

Let's talk about coloration in reverb caused by allpass filters.

The first thing that any designer learns is that allpass filters are great at increasing echo density when placed in the inner loop of a reverb algorithm. This is often desirable and the reason for using the allpass filter in the first place. Unfortunately, the next thing he learns is that while an allpass is flat in the frequency spectrum, it has a comb shaped group delay characteristic that causes ringing in the tail because certain frequencies are delayed longer than others. Since the group delay of an allpass filter is comb shaped, it is regular and leads to a pronounced metallic sound in the tail.

OK, I was wrong, the first thing that a designer learns is not to put allpass filters in parallel. Every text says so, right? Why is this? Well since the group delay of an allpass is comb shaped, two differing allpass filters in parallel will cause outputs that have phase relationships that are directly related to the super position of the two group delay comb shapes.

And yet, we see many designs that have allpass filters in parallel. No? Even if the inner loop consists of allpass filters in series, look again. Follow every input path to every output path and often you will find that the inner loop does have many paths that place the allpass filters in parallel.

So how do these algorithms get away with breaking this fundamental rule of no allpass filters in parallel? Well, the best answer is to trace every input/output path that places the allpass filters in parallel, and make sure they are spaced out enough (say > 200 msecs) that the sound in each path is decorrelated just by being far enough away in time. Much closer than this and coloration starts to show up in the lower frequencies.

If this is not possible, (and it rarely is) then randomizing the allpass filters is typically used to keep moving the comb shaped group delays so that the ear doesn't pick up a constant coloration.

A method has recently been published by Blesser, which modifies the allpass filter in order to eliminate the ringing tail problem brought about by the comb shaped group delay. At first this seems like a pure win, but in reality there is a price to pay in the coloration of the running reverb. Blesser's method alters the allpass filter coefficients so as to turn the allpass into a comb filter. Essentially adding coloration to the running reverb in order to eliminate metallic sounding tails. This is particularly problematic in that the coloration is constant.

It is also beyond the abilities of typical computing resources to randomize these modified allpass filters given the math outlined in the Blesser publication. So nothing can be done to eliminate the primary coloration caused by parallel (in this case modified) allpass filters.

For years we have been taught to listen for impurities in the reverb tail. It is just as important to listen for unnatural coloration in the running reverb.

-Casey

---

### Post #163 -- Page 6
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4338935&postcount=163>

Awesome and thought provoking post, Casey...

Parallel Comb filters are not all that unusual in some reverb topologies, are they? In the Lexicon 224x there were some "constant density" plate algos, were these based on such a topology?

Also, someone at Lexicon mentioned that the PCM96 hall employs a new (patented) technique developed by Barry Blesser, do you suppose the paper you mentioned has anything to do with the new Hall algo?

---

### Post #164 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339128&postcount=164>

Why not delete these all-pass filters in the tank and only set them in series before the reverb tank?

---

### Post #165 -- Page 6
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339218&postcount=165>

> *Originally Posted by Froombosch:*
> Why not delete these all-pass filters in the tank and only set them in series before the reverb tank?

Allpass filters in a tank result in an echo density that builds with time, as found in real 3-dimensional acoustic spaces, as well as 2-dimensional spaces such as plates. Allpass filters in series before the reverb tank will result in an increased initial echo density, but no build of density as the reverb decays.

Sean

---

### Post #166 -- Page 6
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339713&postcount=166>

Harrie, Sean, Isn't this topology used in Jon Dattorro's algo?

---

### Post #167 -- Page 6
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339732&postcount=167>

> *Originally Posted by Casey:*
> So how do these algorithms get away with breaking this fundamental rule of no allpass filters in parallel?...

But if I look at a loop algorithm in a certain well-known reverb, I see a lot of allpasses that are closer than 200ms. In fact, all of them at most sizes less than a canyon. Somewhere around 13ms at the smallest size setting. But the allpasses on either side of that delay are 8.9ms and 4.7ms - the total of which is about the same as the delay between them. Is it more the ratio of allpass length to delay length that is important here? Or to keep the amount of delay within allpasses of the loop to less than, say, 1/3 of the straight delay time in the loop?

Then what about the 'black hole' reverb (I think it was on an Eventide 8000) which is simply a sequence of something like 32 allpasses in series? It has an interesting sound - a very slow buildup and a decay that is about as fast as the buildup. Very unnatural sounding to me. Almost like a tunnel drive-by except without the doppler effect.

---

### Post #168 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339834&postcount=168>

Correct. On the other side we are using modulation to decorrelate the reflections. This has no equivalent in normal hall reflections. Maybe moving walls ;)

---

### Post #169 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339863&postcount=169>

> *Originally Posted by zmix:*
> Isn't this topology used in Jon Dattorro's algo?

I do not think so. The diffusers divide the reflections more after every feedback return. So this topology had increased amount of reflections.

---

### Post #170 -- Page 6
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4339879&postcount=170>

> *Originally Posted by dale116dot7:*
> Then what about the 'black hole' reverb...

I do not know how they made it. I can try to figure out using VSIG. I love the sound of it and use it as an effect on a lot of my recordings.

---

### Post #171 -- Page 6
**User:** dale116dot7
**Info:** Lives for gear | Joined: Dec 2003 | Posts: 1,142
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340035&postcount=171>

I looked at it in VSIG and I understand how it's put together but it sort of breaks the allpass separation guideline.

---

### Post #172 -- Page 6
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340147&postcount=172>

Each output channel of the Black Hole reverb consists of a single series chain of allpasses, with the output taken from the end of the chain. If you look at the output channels in parallel, there are parallel allpasses, but the issues that Casey is talking about are less objectionable when the signals are being mixed in the air, as opposed to in the box.

The structure uses a single chain of a bunch of allpass delays for a mono input signal (derived from a sum of left and right input signals), and then has 2 parallel allpass delay chains to decorrelate left and right signals.

*Last edited by seancostello; 2nd July 2009. Reason: More about Black Hole*

---

### Post #173 -- Page 6
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340159&postcount=173>

The Block diagram and parameter list for the Ensoniq DP/Pro implementation show six diffusors in series feeding the reverb tank. I'll listen to some impulses to see how the density builds up....

---

### Post #174 -- Page 6
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340161&postcount=174>

> *Originally Posted by Froombosch:*
> On the other side we are using modulation to decorrelate the reflections. This has no equivalent in normal hall reflections. Maybe moving walls ;)

Variable speed of sound, due to temperature variations within a large space. A small amount of temperature variation in different places within a hall, or moving air currents, will cause very small random pitch changes of the reflections. Multiply this by a few orders of reflections, and you can have a fairly significant spread of frequencies over time.

---

### Post #175 -- Page 6
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340180&postcount=175>

According to Dr. Blesser's citation in his "artificial Reverberation" paper, the speed of sound varies due to thermal currents at an (average) equivalence to 2ms at a rate of 0.2hz.

If you want to simulate this effect you need to tailor your randomization to resemble wind! The largest DSP hogs in my reverb algos are the randomizers....

---

### Post #176 -- Page 6
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340512&postcount=176>

> *Originally Posted by zmix:*
> Isn't this topology used in Jon Dattorro's algo?

Yes it is. The Dattorro algorithm, at least as published in the JAES, uses series allpasses both within a feedback loop (to build echo density over time and decorrelate the recirculating tank signal), and outside of the feedback loop (to turn impulsive sounds into tight clusters of echos).

---

### Post #177 -- Page 6
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4340570&postcount=177>

The Black Hole reverb points out one of the fundamental issues with allpass delays in series, or for that matter any sort of filtering operation in series: As the order of the series increases, the impulse response of the output begins to resemble a Gaussian bell curve more and more. This causes a very distinctive "fade in" sound that can be used to great effect if intended, as in the Black Hole reverb, but will cause problems if not intended.

I have heard simpler digital reverbs, such as the SilverVerb in Logic, that are clearly based around comb filters with a lot of series allpasses embedded in the delay loop, and a single output tap at the end. The output of such reverbs can be very "open," but will also demonstrate that fading in quality, as opposed to an impulsive attack followed by an exponential decay.

The solution is to tap in between allpass stages, as shown in the Gardner and Dattorro papers, and later on in the Dahl/Jot papers with the absorbent allpasses.* This allows you to grab the signal before it becomes overly "Gaussian." Of course, this also creates the parallel allpass artifacts which Casey refers to above. So there is no neat and tidy solution, just a bunch of compromises and heuristic tricks.

Or, you can avoid using allpasses altogether. Lots of reverbs only use short allpasses outside of the feedback loop (if at all), and rely on a combination of parallel combs, feedback delay networks, and/or cleverly arranged output taps to get the required echo density. Having said that, so many of the classic digital reverbs seemed to use the allpasses embedded inside of recursive loops, that the artifacts are probably considered desirable for many listeners out there.

I was starting to write about this stuff on my blog ([The Halls of Valhalla](http://valhalladsp.wordpress.com)), but it seems like there are <10 people out there that are really actively pursuing this stuff right now, and most of them are posting to this thread.

Sean

\* "Absorbent allpasses" are subject to a patent by Creative Labs. However, the use of them embedded within feedback delay network structures (which can include a single comb) was first mentioned in Jot's 1992 PhD thesis, so the validity of the claims concerning those allpasses is questionable. Plus, Gerzon showed frequency dependent allpasses in his 1972 and 1976 papers, and Date/Tozuka showed analog circuits for implementing these as early as 1966.

---


## Page 7

---

### Post #181 -- Page 7
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 2nd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4341241&postcount=181>

> *Originally Posted by Nobody Special:*
> Since you've been talking about allpasses, I'll pass along an observation. Although the traditional view is that allpasses increase reverb density, that's only true up to a point. The number of reflections per second is still limited by the Nyquist theorem (and probably by the auditory cortex as well). With well-chosen allpass values, that limit can be reached quite rapidly. After that point, the significant effects are phase and frequency.

This is an interesting point. We have been discussing "constant density" algorithms in this thread. If the initial echo density approaches the maximum density supported by the Nyquist theorem, or the maximum density that can be perceived by our ears, then having an echo density that increases over time is a moot point.

From the discussion of the EMT-esque algorithm, and listening to older reverberators, it appears that there were many algorithms that took such a constant density approach. Some of these seem to be improved Schroeder algorithms, others undoubtedly use far different algorithms - there are a lot of ways to get density quickly.

One of the big problems with any algorithmic reverberator, be it constant density or increasing with time, is the ability of the ears to quickly pick up repetitive patterns in seemingly random signals. Most delay based time invariant reverberators will have an audible repetition rate for long decays, where the repetition rate occurs at the sum of all of the delay lengths for a well tuned reverb (and at a much faster rate or series of rates for a poorly tuned reverb). The initial use of randomizers within reverbs seems to have been to reduce or eliminate this repetition artifact.

The time variation found in most commercial reverbs can go far beyond what would be found in most real-world situations. Boston Symphony Hall may have randomization of the delay times, but an algorithm like the PCM70 Concert Hall, or the Eos Superhall, or the DP/Pro Expert Reverb displays artifacts that would probably not be present without some extensive modifications to that building, such as a series of active bonfires within the structure. This larger-than-life artifact has now become part and parcel of many styles of electronic and ambient music. The Brian Eno / Harold Budd albums display some pitch artifacts that I am now able to hear as part and parcel of the EMT250 used on those songs, and the music would not be nearly as cool without those sidebands decaying into the aether.

---

### Post #182 -- Page 7
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4341977&postcount=182>

**Actual Subculture Question**

I had a nice summer walk today, and was thinking about reverb, and why I think about reverbs. In some ways, it is like being obsessed with Sodoku or Go or chess or something like that - there are an endless variety of structures that can be mentally manipulated.

My question is for the people that have been posting on this thread, and build reverberators for a living, or at least as a serious hobby: How did you end up making reverberators? Was it through a EE route, or as a musician, or something else entirely?

---

### Post #183 -- Page 7
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4342318&postcount=183>

When starting a recordingstudio I always had the idea I needed an Eventide processor. I bought myself an Eclipse and started building presets for them. I was very active with Eventidehelps and enjoyed the building of presets and the active community there. Finally I bought myself a H8000 and started constructing new presets. I build a few presets for this machine (Dimension D replica etc), that are now inside the H8000. Finally I got interested in reverb technology and am now working on some algos that will be ported over to VST world.

---

### Post #184 -- Page 7
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4342426&postcount=184>

Anyone any thoughts on the reflections that exist inside a wood? Anyone who has found a paper on this topic?

---

### Post #185 -- Page 7
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4342794&postcount=185>

> *Originally Posted by seancostello:*
> How did you end up making reverberators?

What a fun question, Sean. All of these are factors for me.

Growing up in Catholic school and listening to the priests (speaking and singing) and of course the pipe organ in the Cathedral. The rolling quality to that reverb is something I have seldom heard in an artificial reverb.

Much later, on an early visit to a studio hearing the tape stop during a mix and hearing just the reverb tail... this made a huge impression.

"Coming of age" in the technology obsessed late 1970s and the reverb drenched 1980s fueled the obsession with sculpting space. Getting an Electrical engineering degree was simply more gasoline on that fire.

Discovering object oriented DSP construction software which allowed me to quickly test theories and produce the 'echos in my head' that had eluded me until then.

---

### Post #186 -- Page 7
**User:** Nobody Special (Deleted ab87343)
**Info:** Posts: n/a
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4342878&postcount=186>

> *Originally Posted by seancostello:*
> How did you end up making reverberators?

Happened in a lot of ways for me. Childhood was a mix of science and music. I spent early adulthood on the road as a guitarist. Musical interests matured so I went back to school and got a couple of music degrees. During this time I fell into computing, having been invited to participate in computer music at MIT (and I wasn't even in school there). I've run a lot of new music concerts in all sorts of spaces and even conducted a few times (luckily stopping before anyone was seriously injured). Early engineering years included speech recognition, operating systems design, medical computing. When I came to Lexicon it was a good opportunity to put it all together. I was doing other things there for several years before I had an opportunity to work on the 'verbs and other FX. At this point it's a mix of science, engineering and intuition. And I'm still doing the new music concerts when I can. I suspect most of us are mongrels in one way or another.

---

### Post #187 -- Page 7
**User:** Nobody Special (Deleted ab87343)
**Info:** Posts: n/a
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4342904&postcount=187>

> *Originally Posted by seancostello:*
> If the initial echo density approaches the maximum density supported by the Nyquist theorem... then having an echo density that increases over time is a moot point.

There's still a lot of interesting stuff that goes on after you reach maximum density. Even though there are no more reflections to be had, the impulse response is still constantly changing as peaks and troughs line up in different combinations. As has been pointed out, there are still many hazards to face when going through the same old allpasses time after time. Part of the art is on knowing how to minimize those effects.

---

### Post #188 -- Page 7
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4343213&postcount=188>

The "constant density" algorithms seem to take the solution of avoiding allpasses in recursive loops. If things are dense enough, why put allpasses in there?

---

### Post #189 -- Page 7
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4343227&postcount=189>

> *Originally Posted by Froombosch:*
> Anyone any thoughts on the reflections that exist inside a wood?

[AES E-Library: A Digital Reverberator Modeled After the Scattering of Acoustic Waves by Trees in a Forest](http://www.aes.org/e-lib/browse.cfm?elib=14801)

---

### Post #190 -- Page 7
**User:** Nobody Special (Deleted ab87343)
**Info:** Posts: n/a
**Date:** 3rd July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4343356&postcount=190>

> *Originally Posted by seancostello:*
> The "constant density" algorithms seem to take the solution of avoiding allpasses in recursive loops. If things are dense enough, why put allpasses in there?

Because they're still doing the other good thing they do, which is to modify phase.

---

### Post #191 -- Page 7
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 4th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4344315&postcount=191>

OK here's a quick synopsis of the Dattorro "Expert Reverb" algo in the Ensoniq DP/Pro:

Lo Cut/Hi Cut frequency and gain parameters. Pre Delay 0-100ms. 6 series diffusors on each input (6 left, 6 right, each adjustable 0.00 to 23.0ms). Master Diffuser Size 0-100%. Diffusion amount scaler -100% to +100%.

Reverb Tank: Master Reverb Size scaler 0-100%. Mid Decay: 0.00 to 1000s. Low Decay 0%-400%. Low-Mid Xover 3hz-20khz. HF Damping 3hz-20khz. Density 0%-100% (controls diffusion within the reverb tank - setting to 0% creates "constant density" reverb). 8 delays in the reverb tank each adjustable 0.00ms-200.0ms. 4 modulation LFOs with depth 0.00ms-200.0ms and rate 0.00hz-1.760khz.

**Attached Files:** DPpro Expert Reverb comparison examples (4 mp3 files)

---

### Post #192-194 -- Page 7
[Posts 192-194: seancostello and zmix discussing the Expert Reverb's FDN structure, whether delays are allpass delays, and how Ensoniq gave users too much control over dangerous parameters]

---

### Post #195 -- Page 7
**User:** Froombosch
**Info:** Registered User | Joined: Jun 2004 | Posts: 1,190
**Date:** 5th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4347416&postcount=195>

Thanks! I will get a copy of that paper!

---

### Post #196 -- Page 7
**User:** seancostello
**Info:** ValhallaDSP | Joined: Feb 2009 | Posts: 4,769
**Date:** 6th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4349540&postcount=196>

> *Originally Posted by zmix:*
> Discovering object oriented DSP construction software...

What software? I have played around with a bunch of different environments (MAX/MSP, Pd, Supercollider, Reaktor), and haven't found anything that really does what I need it to do, except for my own C++ modules.

As far as my own background, I am kind of a mutt. Studied at CCRMA as an undergraduate, but majored in Anthropology. Did the Seattle guitar slacker thing, got obsessed with fuzz boxes. Computer music seemed like a more fruitful path, so talked my way into a year long course at the University of Washington. Did really well from a technical perspective, for some unknown reason. Ended up getting a job in the Bay Area with some CCRMA PhDs.

I first worked with reverbs as it seemed like a good way of getting some complex sounds with minimum CPU cycles. I could matrix together 4 modulated delay lines with near-infinite gain, and get sounds almost identical to granular textures using 100 grains, at about 1/100th of the DSP of the granular processes. 1998 and 1999 were spent learning the basics, the early 2000's were spent on developing different structures, and the late 2000's have been spent learning how to make the structures sound good.

---

### Post #197 -- Page 7
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 6th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4350459&postcount=197>

**Dattorro Algo "Expert Reverb"** - detailed parameter listing and comparison examples of Expert Reverb 1 vs Expert Reverb 2, with various Diffusion and Density settings. Includes diffusor chain delay times and tank delay times.

**Attached Files:** 4 comparison mp3 files

---

### Post #198 -- Page 7
**User:** zmix
**Info:** Lives for gear | Joined: Jan 2005 | Posts: 931
**Date:** 7th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4353625&postcount=198>

Pitch modulation images from the Lexicon 224 v4.x - graphical depictions of pitch modulations from "Small Concert Hall - B" and "Percussion Plate - A" programs. Depth approximately 6 cents. 45 seconds shown.

**Attached:** Two images showing modulation waveforms

---

### Post #199-200 -- Page 7
[Posts 199-200: seancostello asking zmix for 224 sound files and clarification on the pitch modulation images]

---

### Post #201 -- Page 7
**User:** samiam
**Info:** Terminologist | Joined: Sep 2002 | Posts: 290
**Date:** 7th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4353947&postcount=201>

Long post discussing Voxengo Impulse Modeler (ray-tracing based reverb generation), comparisons with PCM-90 algorithms, SRV-2000, and the potential for real-time ray-tracing reverbs. Includes an attached Hall-2-ir.wav impulse response file.

---

### Post #202 -- Page 7
**User:** Nobody Special (Deleted ab87343)
**Info:** Posts: n/a
**Date:** 7th July 2009
**Link:** <https://gearspace.com/board/showpost.php?p=4354339&postcount=202>

> *Originally Posted by samiam:*
> [discussing convolution and ray-tracing]

You're describing something similar to the 'Room' algorithm in the PCM96. There are 48 real-world impulse responses that can optionally be dumped into a standard reverb. The impulse responses don't use a full convolver. Instead, they're mathematically reduced into a form that allows some realtime modification. Unlike a convolver, the impulses can easily be rubberbanded in time, EQ'ed and reversed.

I have no wish to get into the convolution vs. algorithmic debate (well only a small wish). The best convolved reverbs sound excellent. They're just a little hard to match up with material sometimes. Algorithmic reverbs offer greater flexibility in terms of EQ and other important characteristics. For that reason I don't see them going anywhere.

Ray-tracing is similar. Your example sounded very good, but it didn't sound necessarily superior to a well-done algorithmic or convolved reverb.

N.S.

---


---

## Coverage Notes

**Pages completed:** 1-7 (posts #1-202, with some gaps noted below)
**Known post gaps:** #86-90 (end of p3), #115-120 (end of p4), #145-150 (end of p5), #178-180 (end of p6), #203-210 (end of p7)
**Remaining:** Pages 8-36 (posts ~211-1059)

These gaps are due to web_fetch token limits truncating each page before the final ~5-10 posts. Use the companion scraper script to fill gaps and complete pages 8-36.
