
---

## Page 13

---

### Post #361 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517455&postcount=361>

Quote: > Originally Posted byWarp69➡️That's because the dry signal is mixed with the processed sound. It modifies some early taps so you get a faster attack and more tight image just like you descript your own plate.???????  What?


A single sample impulse was the excitation signal for these examples... there is no possible way that 'dry signal is mixed with the processed sound" since they are separated by at least 4ms from the impulse to the 1st reflection and 12ms to the second one...also the signal doesn't modify the taps.. very confused by this assertion.

---

### Post #362 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517523&postcount=362>

Semi-off topic: What do people use on the Mac to view waveforms? Any good free choices?


I want to take a look at the .wav files of the reverbs at different Depth settings, but the view in Logic doesn't look that great.

---

### Post #363 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517534&postcount=363>

Quote: > Originally Posted byseancostello➡️Semi-off topic: What do people use on the Mac to view waveforms?I would recommend Logic.  Double click on the audio file and it will open up in the waveform editor. The cursor position will display in whatever units you desire.

---

### Post #364 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517541&postcount=364>

Quote: > Originally Posted byzmix➡️???????  What?A single sample impulse was the excitation signal for these examples... there is no possible way that 'dry signal is mixed with the processed sound" since they are separated by at least 4ms from the impulse to the 1st reflection and 12ms to the second one...also the signal doesn't modify the taps.. very confused by this assertion.I think that Warp69 was referring to how Depth modified the early taps in the CD Plate, as opposed to the mixing of dry and wet modifying the early taps.

---

### Post #365 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517559&postcount=365>

Quote: > Originally Posted byseancostello➡️I think that Warp69 was referring to how Depth modified the early taps in the CD Plate, as opposed to the mixing of dry and wet modifying the early taps.I guess it's the use of the term "Modifying" that is unclear.  The CD plate has a simple set of 6 delays that are added in parallel to the 'reverb' signal.  The "DEPTH" slider controls the level of these taps as illustrated in the image I posted a few posts up... The addition of these taps does not affect the 'reverb' signal per se... How and where is this "modification" taking place?

---

### Post #366 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517563&postcount=366>

OK, I just looked at the PCM96 Tap Slope impulses in Logic (thanks for the tip zmix!). Warp69 is right, they DO look identical.

---

### Post #367 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4517580&postcount=367>

I hope that N.S. will chime in here and straighten this out, but  I suspect that the "Tap Slope" parameter is broken...


EDIT:I went through every single algo on the PCM96 and not one of them had a working "Tap Slope" in the way that NS or Lexicon describe it....

---

### Post #368 -- Page 13
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4518195&postcount=368>

Quote: > Originally Posted byzmix➡️I hope that N.S. will chime in here and straighten this out, but  I suspect that the "Tap Slope" parameter is broken...EDIT:I went through every single algo on the PCM96 and not one of them had a working "Tap Slope" in the way that NS or Lexicon describe it....Well do the presets use this parameter at all?


If so the preset developers had to have been listening for something.



-Casey

---

### Post #369 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4518213&postcount=369>

Quote: > Originally Posted byCasey➡️Well do the presets use this parameter at all?If so the preset developers had to have been listening for something.-CaseyHa..! Good point.. To be honest I have NEVER used a reverb preset in my life...(I've sure written a lot of them).  I'll have a look-see soon.



EDIT:  I found a "Hall" preset that used the Tap Slope at a value of +1 and printed it. Then I adjusted the value to -1 and printed that... behold:

---

### Post #370 -- Page 13
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4518445&postcount=370>

Quote: > Originally Posted byzmix➡️behold:Sure do sound the same.



-Casey

---

### Post #371 -- Page 13
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4518645&postcount=371>

Quote: > Originally Posted byzmix➡️???????  What?A single sample impulse was the excitation signal for these examples... there is no possible way that 'dry signal is mixed with the processed sound" since they are separated by at least 4ms from the impulse to the 1st reflection and 12ms to the second one...also the signal doesn't modify the taps.. very confused by this assertion.First of all - you have mixed the dry signal (dirac  impulse) with the output of the reverb and it's therefor difficult to hear the actual level change of some of the taps.


If you delete the "single sample impulses" from the files it's quite easy to hear what happens.

Quote: > Originally Posted byzmix➡️guess it's the use of the term "Modifying" that is unclear. The CD plate has a simple set of 6 delays that are added in parallel to the 'reverb' signal. The "DEPTH" slider controls the level of these taps as illustrated in the image I posted a few posts up... The addition of these taps does not affect the 'reverb' signal per se... How and where is this "modification" taking place?I would gategorize a level change as a modification.


The 6 early taps **does** affect the overall reverb sound - the behavior of the Depth parameters on the Plate is similar (yet quite simple) to the attack/shape on other algorithms from 224XL, 480L etc. With higher values of Depth you'll get a fast attack and possible an improvement of the early imaging, just like what Sean described (the Attack control of EOS).

---

### Post #372 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4519449&postcount=372>

Thanks for the clarification Warp..!


I would define a 'modification' as something which has a causal effect on something else, but certainly perceptual differences are an important part of this discussion.   The perceptual masking of the changes in the ER levels by the presence of the initial impulse in the 224 Constant Density plate example above is certainly a valid observation.

---

### Post #373 -- Page 13
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4524115&postcount=373>

Was that directed at me? I don't quite follow you.

---

### Post #374 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4526271&postcount=374>

Quote: > Originally Posted byWarp69➡️Was that directed at me? I don't quite follow you.I was thanking you for clarifying what you meant and complimenting you on your perceptual observations.


I think that perceptual skills are as important if not more important than theory in the development stages of reverb design.

---

### Post #375 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4526805&postcount=375>

Quote: > Originally Posted byzmix➡️I think that perceptual skills are as important if not more important than theory in the development stages of reverb design.I agree with this. I also think that "golden ears" are useful, in terms of having many skilled listeners critiquing your algorithms. Having the little $49 plugin I worked on going head to head against the big hitters was nerve-wracking, but it was great to hear the feedback. I love reading complementary feedback about my work (who doesn't like hearing nice things about what they do?), but the more pointed critiques and discussions are what will lead to progress in the future.

---

### Post #376 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4527045&postcount=376>

I think that it is important to understand that the  context  in which an artificial reverberator is *used* is just as important to this discussion as is the ability that the reverb has to *create a context* (temporal, spacial and gestural) for the source signal, and there is a need to distinguish these as two separate arguments when exploring this broad topic.   Many great reverbs (EMT250, Lexicon 224) might sound 'bad' to a reverb designer today when auditioned without a source signal but satisfy the contextual criteria outlined above better than many more 'sophisticated' reverbs.


"Le mieux est l'ennemi du bien."

---

### Post #377 -- Page 13
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4528053&postcount=377>

Quote: > Originally Posted byseancostello➡️I also think that "golden ears" are useful, in terms of having many skilled listeners critiquing your algorithms, but the more pointed critiques and discussions are what will lead to progress in the future.I agree, but unfortunately not many people have "golden ears" and are able to describe what they hear (or want to hear).

Quote: > Originally Posted byzmix➡️Many great reverbs (EMT250, Lexicon 224) might sound 'bad' to a reverb designer today when auditioned without a source signal but satisfy the contextual criteria outlined above better than many more 'sophisticated' reverbsIt sounds like you have a preference for obvious chorus like modulation (using linear interpolation) instead of other types of modulation found in 480L, PCM96 and Bricasti (Version 1).

---

### Post #378 -- Page 13
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4528690&postcount=378>

Staring at schematics for a while... the 224 has a 6-bit multiplier but a binary point of 5 so for the purposes of interpolation, it's a 5-bit gain. Updates to the WCS are slow because it used 250ns RAM which is only slightly faster than the 224's instruction execution time. The micro (an 8080) can update a coefficient only during a NOP DSP instruction without thrashing DSP code fetches. The PCM70 improved on this by having an active and an inactive WCS, and there's a signal called 'COPY' which copies the inactive one over the active one during one WC period - a very clever couple of logic gates. It allows less grainy (faster) updates to coefficients - and a 6-voice chorus. WCS=writable control storage (DSP code).

---

### Post #379 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4528715&postcount=379>

Quote: > Originally Posted byWarp69➡️Quote:Originally Posted byOriginally Posted by zmixMany great reverbs (EMT250, Lexicon 224) might sound 'bad' to a reverb designer today when auditioned without a source signal but satisfy the contextual criteria outlined above better than many more 'sophisticated' reverbsIt sounds like you have a preference for obvious chorus like modulation (using linear interpolation) instead of other types of modulation found in 480L, PCM96 and Bricasti (Version 1).This isn't what I am saying here.  I am simply pointing out that in many cases, as in the EMT250 and the 224 for example, there were obvious limitations' that are easily overcome today but the perceptual impact isn't completely understood, hence the "better" becomes the enemy of the "good".


Could you please be a bit more specific about how you define the modulation 'types' instead of grouping the 480 , pcm96 and m7?  The pcm96 alone has at least three different modulation types.


Also,  I think it's a gross simplification to state that I prefer 'obvious chorus like modulation" because in fact I detest the 'obvious chorus type modulation' in artificial reverb.  The paper I cited by David Griesinger is  a very good example of how a perceptual goal can be used in a reverb design, particularly when exploring modulation for realism's sake.

---

### Post #380 -- Page 13
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4528824&postcount=380>

Quote: > Originally Posted byzmix➡️Could you please be a bit more specific about how you define the modulation 'types' instead of grouping the 480 , pcm96 and m7?  The pcm96 alone has at least three different modulation types.#1 Interpolation (liniear, allpass, lagrange etc) of delay lines by sine, tri, ran - obvious chorus effect

#2 Crossfading between taps (which probably is close related to both #1 and #3, depending how you define interpolation and coefficients manipulation)

#3 Coefficients manipulation - ex. change the values in the FDN matrix

Quote: > Originally Posted byzmix➡️,  I think it's a gross simplification to state that I prefer 'obvious chorus like modulation" because in fact I detest the 'obvious chorus type modulation' in artificial reverb.  The paper I cited by David Griesinger is  a very good example of how a perceptual goal can be used in a reverb design, particularly when exploring modulation for realism's sake.I would say that obvious chorus like modulation is present on the concert hall algorithms from the 224(XL) and the EMT250 algorithm - it's still a chorus like modulation if you use a pseudo random generator for the modulation. It can be implemented differently - good or bad. I said that it **sounded**  like you have a preference for this kind modulation, since both the EMT250 and the Concert Hall algorithm are in your top 3 reverbs and they have an obvious chorus effect. And it seems that you're most interested in discussing the behaviour of those two algorithms

---

### Post #381 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4529254&postcount=381>

Quote: > Originally Posted byWarp69➡️#1 Interpolation (liniear, allpass, lagrange etc) of delay lines by sine, tri, ran - obvious chorus effectThis seems closest to how nature works, as the microvariations of the speed of sound that can be traced to temperature variation in an acoustic space will result in time/pitch changes. Of course, a real acoustic space will have variations that are closest to very low frequency random generators (0.2 Hz was cited by Blesser). In addition, each reflection will have independent modulation of varying depth, so the effect will be far more subtle than just sticking a few LFOs in an algorithm.

Quote: > #2 Crossfading between taps (which probably is close related to both #1 and #3, depending how you define interpolation and coefficients manipulation)I presume you are referring to non-contiguous taps here. Yamaha has a patent on this, although it sounds like this technique was in use by another big company considerably before Yamaha filed their patent. I need to explore this technique in more detail. For stability reasons, I would presume that this is feed forward only - putting such a crossfader in a feedback loop can rapidly lead to instabilities.

Quote: > #3 Coefficients manipulation - ex. change the values in the FDN matrixSince any delay based reverb can be (hypothetically) described as an FDN, this can describe a number of techniques. Most of the ones I have tried don't sound that great.

---

### Post #382 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4529258&postcount=382>

Quote: > Originally Posted byWarp69➡️#1 Interpolation (liniear, allpass, lagrange etc) of delay lines by sine, tri, ran - obvious chorus effect#2 Crossfading between taps (which probably is close related to both #1 and #3, depending how you define interpolation and coefficients manipulation)#3 Coefficients manipulation - ex. change the values in the FDN matrixWell obviously the EMT250 does a lot of both #1 and #3, it's remained highly useful despite (but probably  *because of*) it's rather low mode density.  The Ursa Major Space station uses a form of #1 and something like #3 though it hasn't really got a similar structure to other reverberators.  The 224 uses these methods as well, but it's quite easy remove all modulation in that machine and still have a very useful reverb.


When I listen to the "Random Hall" algo (which seems to use #2 above) or the later Lex algos with the "Spin" and "Wander'  parameters I hear a lack of 'distance' in the tail.  The sound seems to float like a cloud rather than travel away from the listener.  I think the Griesinger paper provides a compelling argument against this sort of modulation for realistic spaces. 


How would you characterize the differences in depth that you have observed when experimenting with these three methods?

---

### Post #383 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4529366&postcount=383>

Quote: > Originally Posted byzmix➡️Well obviously the EMT250 does a lot of both #1 and #3, it's remained highly useful despite (but probably  *because of*) it's rather low mode density.  The Ursa Major Space station uses a form of #1 and something like #3 though it hasn't really got a similar structure to other reverberators.  The 224 uses these methods as well, but it's quite easy remove all modulation in that machine and still have a very useful reverb.I would describe all 3 of these algorithms as relying on #1 only. [EDIT] I presume that the EMT250 has linear interpolated delay lines in its feedback loops, but I may be mistaken. [/EDIT] Method #3 implies changing the gains of feedback operators, presumably in a unitary fashion. A few examples:


- Parallel delay lines coupled by a feedback matrix, where the matrix is changing values in a unitary method. Blesser has this in his recent patent, but it looks like he removed the claims that cover this particular technique. I had worked with similar ideas around the same time as Blesser, but wasn't too happy with the results. It sounds like cycling through different fixed resonances, instead of smoothly varying the resonant frequencies.


- Changing the coefficients of allpasses embedded within a delay loop. This can result in some nasty sounds, as well as very obvious changes in reverb echo density. When I have tried it, it sounds either like water sploshing in a metal pan (for slow variation speeds), or like tortured souls screaming from the pit of Hell (for faster variation speeds). I used one of my failed experiments as a sound to scare trick or treaters one year.

Quote: > When I listen to the "Random Hall" algo (which seems to use #2 above) or the later Lex algos with the "Spin" and "Wander'  parameters I hear a lack of 'distance' in the tail.  The sound seems to float like a cloud rather than travel away from the listener.  I think the Griesinger paper provides a compelling argument against this sort of modulation for realistic spaces.It seems like you prefer the sidebands to build up over time, instead of staying at a fixed level. Method #2, or any other feedforward method (which could be any of the 3 methods, if you change #3 to include feedforward matrices) will probably be better for preserving the pitch of sustained signals. Having said that, I love the sound of time variation in the feedback loops.

Quote: > How would you characterize the differences in depth that you have observed when experimenting with these three methods?I need to revisit some of the other methods. Most of my experimentation with #3 happened in the early 2000's, when I wasn't as good at setting the delay lengths of a reverb. I have barely tried #2. Method #1 has so many variations, that I have spent much of my time exploring different variations - and I still feel like I have barely scratched the surface.

---

### Post #384 -- Page 13
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4536902&postcount=384>

OK guys, finally had a chance to look and to my surprise there's an error in the way Tap Slope is computed.  While it is still doing stuff, the effect is *considerably* more subtle than I'd intended.  The basic fix is pretty easy from a DSP point of view, but there are a few consequences.  As a result of implementing the parameter correctly, the reverb level is slightly changed.  I have some calibration handles that allow me to correct the level to within a dB or so of the existing presets, at least for a nominal setting of zero.  For positions away from nominal, there may be some noticeable change, no matter what I do.  We'll probably put a tech on individual presets to try to tighten them up, but there will *still* be some minor differences after all that.


This will not be in the release that's currently in Beta.  That's nearly ready to go and it fixes streaming issues for a lot of people.  No point in slowing it down.  This fix will be in a subsequent release.


Sorry I missed this one.  The only thing I can say in my own defense is that I had a number of other irresistibly urgent things on my plate at the time I did presets.  With a little more spare brainpower, I'd have caught it.


N.S.

---

### Post #385 -- Page 13
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4537327&postcount=385>

Quote: > Originally Posted byNobody Special➡️Sorry I missed this one.  The only thing I can say in my own defense is that I had a number of other irresistibly urgent things on my plate at the time I did presets.For those of us who know NS; We will all attest on his behalf that "urgent" understates the issues he had on his plate at the time.


It's all good!



-Casey

---

### Post #386 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4539502&postcount=386>

Well, I am glad that I took the time to write Lexicon about the Tap Slope issue...

---

### Post #387 -- Page 13
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4573706&postcount=387>

Quote: > Originally Posted byNobody Special➡️Sorry I missed this one.  The only thing I can say in my own defense is that I had a number of other irresistibly urgent things on my plate at the time I did presets.  With a little more spare brainpower, I'd have caught it.Well, I am thankful that I NEVER have any bugs in my stuff.


(Note: do not look at the source code of any of my Csound unit generators from 1999. Especially, when I got sine and cosine mixed up in my Hilbert filter. Also, you may want to avoid any of my code in VisualAudio. Or the code I am currently working on...)

---

### Post #388 -- Page 13
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4574605&postcount=388>

Quote: > Originally Posted byseancostello➡️Well, I am thankful that I NEVER have any bugs in my stuff.I used to be perfect.  Right up until the first time I screwed something up.

---

### Post #389 -- Page 13
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4578744&postcount=389>

I've seen bugs in disassembled code that was produced in fairly large quantities. The 1994 GM 6.5L turbo diesel pickup truck had a diagnostic trouble code that would not set reliably. The orignal source code must have been missing a # mark because the code did not make sense, but made perfect sense if you added it in.

---

### Post #390 -- Page 13
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4579692&postcount=390>

Quote: > Originally Posted bydale116dot7➡️I've seen bugs in disassembled code that was produced in fairly large quantities. The 1994 GM 6.5L turbo diesel pickup truck had a diagnostic trouble code that would not set reliably. The orignal source code must have been missing a # mark because the code did not make sense, but made perfect sense if you added it in.And, boy do those diesels sound terrible...


There was a major error in a very popular arcade game and later continued into the home video game market: ["Donkey Kong"](https://en.wikipedia.org/wiki/Donkey_Kong_(video_game)) sold millions of copies in it's various forms and was licenced by over 50 different companies.  The game involves navigating an Ape arround a lattice structured resembling monkey bars..


The error?


The game was supposed to be titled "Monkey Kong"  but a programmer got *one letter* wrong and it became "Donkey Kong"


---

## Page 14

---

### Post #391 -- Page 14
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4580555&postcount=391>

Yea, the Duramax was a welcome change. I know a guy that designs diesel injectors, and he knows a bunch of the guys at Stanadyne - the maker of the DS4 injection pump which was used on the 6.5L. It was a solenoid-actuated version of the old Roosa Master DB pump, but the pressure spikes from modulating the fuel with a solenoid while the plungers travel full-stroke was not something that a DB pump was designed for - it was designed for plunger volume control. They didn't think the pump was ready for production yet, and it wasn't. 20,000 miles per pump for the first version. The last version got 50,000 miles per pump.


Getting back on-topic... are there any other reverb bugs out there that people have discovered while using them?

---

### Post #392 -- Page 14
**User:** Coyoteous
**Info:** Joined: Aug 2006Posts: 4,297🎧 15 years | Posts: 4,297
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4581562&postcount=392>

Quote: > Originally Posted byzmix➡️Well, I am glad that I took the time to write Lexicon about the Tap Slope issue...I'm glad, too... thanks! I guess you can't expect a direct acknowledgement... like when I found WaveBurner to be "bit inaccurate." Things may be kind of tough over there. NS's boss's wife recently reported hundreds of millions of dollars less in worth than before.

Quote: > Originally Posted byzmix➡️The game was supposed to be titled "Monkey Kong"  but a programmer got *one letter* wrong and it became "Donkey Kong"A very long time ago, I did light service and collected money from arcade games... convenience stores, restaurants and uh, strip clubs. Anyway, I always wondered what that game had to do with donkeys.

---

### Post #393 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4582333&postcount=393>

Quote: > Originally Posted bydale116dot7➡️Getting back on-topic... are there any other reverb bugs out there that people have discovered while using them?Most of my bugs come from programming them. Today, for example, I miscalculated the Size parameter by a factor of 11000 or so, resulting in delay lines writing to who knows where. The reverb would "blow up" - not right away (which usually suggests a problem in some 1st or 2nd order filters), but over time, with a low hum building up to a huge rumbling over about 45 seconds. This happens a few times a day for me.


As far as other manufacturer's bugs, most of them I have found seem like shortcuts. My Lexicon LXP15, for example, only pays the barest lip service to the RT settings. A 2 second RT will sound totally different at various settings of Size. I wouldn't call it a "bug" as the thing keeps working, and it doesn't really cause a bad sound, but it seems like the design specs were pretty loose. However, having an accurate reverb time for each setting of size would require a larger table of delay feedback scalers, and possibly the use of higher numerical precision in the DSP process.

---

### Post #394 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4586458&postcount=394>

Do any of the people on this thread know what is currently going on with reverb pioneers like:


- David Griesinger

- Tony Agnello

- Christopher Moore


I know that Griesinger is no longer associated with Harman, but I don't know what he is doing right now (he could be happily retired for all I know). Agnello licensed one of the SP2016 algorithms for the XBox360 a few years back, and Moore had a reissue of the Space Station, but I haven't heard anything for a few years.


I figure this thread would be as good a place as any to ask.


On a similar note, are there any reverb people that haven't got much credit for their work, that anyone wants to call out? For example, I am a huge fan of Michael Gerzon's early 1970's work, that doesn't seem to get much acknowledgment.

---

### Post #395 -- Page 14
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4645831&postcount=395>

Quote: > Originally Posted bydale116dot7➡️Getting back on-topic... are there any other reverb bugs out there that people have discovered while using them?I found a bug. Well, I knew there was a problem, but it took a while to find it. Not a reverb, but a console automation system. I got motivated to find it, though, when automating a reverb return level, so maybe that qualifies. I have a Soundcraft 2400 and found that kinda-sorta randomly, the box would just crash and start ramping up all of the VCA control voltage DAC's to maximum gain... reach for the mute switch quick. I thought I was unique, but the previous owner (from 1984 'till about 4 years ago) had the same thing. It was very sensitive to tape machine alignment.


Well, this was driving me nuts because during sessions the thing would just do this. I hooked up a logic analyzer to the microprocessor and did some magical dances (well, setting up snapshots and generally watching lots of bytes moving around) and I FOUND IT! The error handler which is called whenever a glitch happens in the received automation data from tape (checksum fault) does not have an overflow trap, so it would overwrite the stack if it got a string of four or five bad packets within a couple of seconds. Since it's difficult to patch the code and make sure it runs identically (withouth the original source code), the 'easy' fix was to comment out the error handler by replacing the first byte with 'RTS' and burning a new EPROM. You only use the error handler for alignment and you can do that with a 'scope anyways.


No, I didn't have the original source code but the code is there in the EPROM if you have the patience to look through it.


That's also why I haven't been posting much - I've been using the gear for a project that's in the mixing phase now.

---

### Post #396 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4673872&postcount=396>

Hi reverb nerds,


How many of you went to AES? What are your thoughts about all things reverby and AESy? Seems to be a lot of interesting developments in that realm. 


I just found that a reverb paper of mine was published online. It was presented at a conference this summer that I didn't attend (my co-author is a lecturer at a British university, so he was able to hop over to Austria to present the paper). 


The paper goes into detail about a proposed reverb structure for Ambisonics reverbs. I am not nearly as proficient in Ambisonics theory as my co-author, Joseph Anderson, so I mainly worked on the reverb part. We had discussed various ways of adapting reverb architectures to A and B format Ambisonics back when we worked at ADI (which must have been in 2003 or 2004), but the particular reverb architecture I threw together for the paper. 


Anyway, you can check out the paper here:

[http://ambisonics.iem.at/symposium20..._download/file](http://ambisonics.iem.at/symposium2009/proceedings/ambisym09-josephandersonseancostello-ambireverbarch.pdf/at_download/file)


No idea how the reverb sounds. Like I have that many speakers sitting around the house. heh

---

### Post #397 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4674737&postcount=397>

I was at the AES convention, all 4 days of it.  It was fantastic.  


In terms of reverbs,  Lexicon had a tiny portion of the Harmon booth, and were displaying the PCM96, 96 surround and he new PCM92.  On the floor there was considerable head scratching about the new Lexicon  Plugin reverbs.   On one hand Lexicon boasts about the superior horsepower of the PCM96 platform, but on the other hand they claim that the plugins are exactly the same as the hardware.   As a PCM96 owner I was furious about this move.   Now I have no chance of ever selling my PCM96.   I certainly hope that Lexicon will come up with some useful and unique application for the PCM96 hardware.  


I gave a listen to the new Bricasti v 2 software, and though I didn't scrutinize it parameter-by-parameter, within a few seconds it was clearly obvious that this is a product that has been created by people who 'get it'.   To use an analogy, if the PCM96 is a Hollywood blockbuster and most plugin reverbs are like bad indy films (or homemade YouTube videos), the Bricasti is a timeless and evocative masterpiece of artful film making that may not be immediately apparent to the hollywood or indy crowd, but has been created with such obvious craft and intelligence that one intuitively trusts it as curator of your suspension of disbelief. Nice work Casey!


I also stopped at the Quantec booth as an English 'gentleman' was losing his temper at the woman in the booth... something about how they were there illegally and hadn't paid for the booth.... I dunno.. I listened to their yardstick again...  just not a fan, i guess.  They now have remote control via a PC over ethernet, so there's that.


SSL had their X-verb but when I stopped over, their system was crashed.   I stopped back to check out the recall of the X-rack modules and that system crashed.   I ran into a friend who was having a demo of their new matrix console, and IT crashed.  I decided to leave SSL alone for the remainder of the show.

---

### Post #398 -- Page 14
**User:** Radiance
**Info:** Joined: Feb 2004Posts: 1,6663 Reviews written🎧 20 years | Posts: 1,666
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4675736&postcount=398>

Quote: > Originally Posted byzmix➡️I gave a listen to the new Bricasti v 2 software, and though I didn't scrutinize it parameter-by-parameter, within a few seconds it was clearly obvious that this is a product that has been created by people who 'get it'.   To use an analogy, if the PCM96 is a Hollywood blockbuster and most plugin reverbs are like bad indy films (or homemade YouTube videos), the Bricasti is a timeless and evocative masterpiece of artful film making that may not be immediately apparent to the hollywood or indy crowd, but has been created with such obvious craft and intelligence that one intuitively trusts it as curator of your suspension of disbelief. Nice work Casey!I like your brief review :-)

---

### Post #399 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4676180&postcount=399>

Another one for my reverb nerd brothers:


What sound files do you use for testing? It is hard to find material that is full bandwidth, yet very dry.


I tend to go to my iTunes library. A few faves:


- Suzanne Vega, "Tom's Diner (A Capella)." Always hated the song, so it is fine to hear it several thousand times. Unfortunately, I can now hear that there is a tiny bit of reverb mixed into the background. Which undoubtedly messed up that pitch tracker I was trying many years back.


- Nick Drake, Pink Moon (whole album). Always loved it, so I don't necessarily want to hear it over and over.


- Neil Young, Live 1968 somewhere in Canada (can't remember the exact name). Weird stereo mix - guitar on left, vocals mostly on right. Not much high frequencies. Dry as a bone, though, and fun to try and get the live version of "Expecting to Fly" to sound like the reverb drenched studio version.


- LCD Soundsystem, "New York I Love You." Good song, dry dry dry.


Any other suggestions?

---

### Post #400 -- Page 14
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4676521&postcount=400>

I plug it in to my console and try out the following:- rim shots - listen for decay into noise with a spectrum, not just a bunch of ticks. Listen for even decay, no decay ripples.
- rock + roll snare - listen for attitude
- vocals, song that wants just some ambience - listen for a dry-ish sound that sounds like a record.
- vocals, song that wants to be soaking wet
- acoustic guitar
- tenor sax or trumpet solo - for a big, big space. Listen for an even blending of notes and a smooth, even decay.


I've just been too busy with other stuff to be doing any algorithm development. On the down side, the DSPB56366 just went to 'not recommended for new design'. I liked that part.


-Dale

---

### Post #401 -- Page 14
**User:** mobilemozart
**Info:** Joined: Nov 2006Posts: 907🎧 15 years | Posts: 907
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4679452&postcount=401>

Quote: > Originally Posted byzmix➡️I've been listening quite closely to differences in modulation in several similar algos:The "Concert Hall" algo  in the Lexicon PCM70 ;The original "Small Concert Hall - A" algo from the rev 4 software in the 224 ;The Concert Hall" in the PCM96.The PCM70 "chorus" parameter has a range of  0 to 99, but any setting below 50 is essentially 'off' and any setting above 60 is very pitchy.The 224 "Mode Enhancement" has a range from 16  to 01, with 01  giving the greatest modulation depth but even so, with the depth set to 01 the modulation is even and well distributed, with no  obvious pitch warble.The PCM96 "Concert Hall" sounds like it has a single unrandomized LFO.In the following examples, I stretched out the decay times to 35 seconds.  This is an interesting experiment, hence my post title: "Steering a big ship with a small rudder".. What is the effect of the modulation on the stopped reverb after such an extended decay? How do these different permutations of a basically similar algo fare?PCM96 "RANDOM HALL" ( Just as a reference, this is a *different* sort of randomization....!!)PCM96 "CONCERT HALL" (note how the pitch of the entire  reverb wobbles up and down)PCM-70 "CONCERT HALL" (similar unified pitch theory)224  "CONCERT HALL" (Mode Enhancement = 02) (perfect...)224  "CONCERT HALL" (Mode Enhancement = 01) (2 scoops of perfect, please..!)wow, great! and as always IMHO, the (1979) Lexicon 224 kills it!

---

### Post #402 -- Page 14
**User:** DrFrankencopter
**Info:** Joined: Sep 2003Posts: 1,016My Studio🎧 20 years | Posts: 1,016My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4688772&postcount=402>

This is such a cool thread...reverb always seemed like black magic to me!


zmix, any chance you give more details on how to get the most out of the Dp/Pro's expert reverb parameters. I've got one, and programming the detailed parameters is a painful process. I think I need to take my time and go through this thread a bit more. One cool thing with that box is you can assign LFOs (up to 4 IIRC) to any parameter, maybe that could be used to interesting effect (pun intended) in the expert reverb.


I might actually have some of the ESP2 assembler code for the DP/Pro reverb algos kicking around. I got it from a guy who was developing a reverb plugin for the Ensoniq Paris DAW based off the DP/pro code. If there's interest in it, I'll look thru my files for it.


Cheers,


Kris

---

### Post #403 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4690056&postcount=403>

Quote: > Originally Posted byDrFrankencopter➡️This is such a cool thread...reverb always seemed like black magic to me!I still think of it as magic of sorts. There is a lot of science, but there is a lot of art as well.

Quote: > I might actually have some of the ESP2 assembler code for the DP/Pro reverb algos kicking around. I got it from a guy who was developing a reverb plugin for the Ensoniq Paris DAW based off the DP/pro code. If there's interest in it, I'll look thru my files for it.I'm interested!

---

### Post #404 -- Page 14
**User:** DrFrankencopter
**Info:** Joined: Sep 2003Posts: 1,016My Studio🎧 20 years | Posts: 1,016My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4692571&postcount=404>

Ok, it turns out that finding the actual ESP code for the Expert Reverb was a little more difficult than I thought. But I did find the ESP code, and the C++ front end code for the reverb plugin that was derived from it. 


Code is available in the zip file here:

[Index of /fk824/reverbs](http://web.ncf.ca/fk824/reverbs/)


There were two plugins made, one based on Expert Reverb1, and the other based on Expert Reverb2. I'm not sure which one I have posted...but I have the other one too if there's further interest.


Cheers


Kris

---

### Post #405 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4692840&postcount=405>

Quote: > Originally Posted byDrFrankencopter➡️Ok, it turns out that finding the actual ESP code for the Expert Reverb was a little more difficult than I thought. But I did find the ESP code, and the C++ front end code for the reverb plugin that was derived from it.Code is available in the zip file here:Index of /fk824/reverbsThe .zip file won't open for me. Is there a way of reposting it?


Thanks, 


Sean

---

### Post #406 -- Page 14
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4693146&postcount=406>

Quote: > Originally Posted byseancostello➡️The .zip file won't open for me. Is there a way of reposting it?Im also unable to open the .zip file.

---

### Post #407 -- Page 14
**User:** DrFrankencopter
**Info:** Joined: Sep 2003Posts: 1,016My Studio🎧 20 years | Posts: 1,016My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4693419&postcount=407>

Okay, forget about the zip file...I'm not sure what went wrong there. But I put up some other files (*.e2 are the assembler files, and *.cpp C++) that you should be able to open in a text editor.


If that doesn't work, there might be something wrong with my ftp settings.


Cheers


Kris

---

### Post #408 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4693851&postcount=408>

The text files work great. Thanks!


Now I need to get out my ESP2 assembler manual (available from links at [Jon Dattorro's Homepage. Convex Optimization, Stanford (Datorro, Dattoro, John)](http://www.stanford.edu/%7Edattorro)) and figure out exactly what is going on.


So far, the main structure looks like a stereo reverb, with 6 allpass delays in series for each input channel, performing diffusion. The output of these are sent to an 8-delay feedback delay network, with a fairly sparse feedback matrix. Not sure of the nature of the matrix, or where the outputs are taken from. 


The code for both of the DP/Pro "Expert Reverbs" is included - apparently they are similar structures, with different feedback matrices. So the tuning of the delay lines is left to the Experts. Any DP/Pro Experts reading this? heh

---

### Post #409 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4694324&postcount=409>

Quote: > Originally Posted byseancostello➡️...So far, the main structure looks like a stereo reverb, with 6 allpass delays in series for each input channel, performing diffusion. The output of these are sent to an 8-delay feedback delay network, with a fairly sparse feedback matrix. Not sure of the nature of the matrix, or where the outputs are taken from.The code for both of the DP/Pro "Expert Reverbs" is included - apparently they are similar structures, with different feedback matrices. So the tuning of the delay lines is left to the Experts. Any DP/Pro Experts reading this? hehPresent.  


 I posted all of this information several months back on this thread [(here)](https://gearspace.com/board/4344315-post191.html), including the algo descriptions. As well as audio comparisons of the two algos[(here)](https://gearspace.com/board/4350459-post197.html).


Here is an interesting part of the code for comparison, since the FDN matrix is the only difference between the two:
Quote: > Expert Reverb 1 FDN:MACP -		gprS X t3		> MAC		XOR	 key_x3, key_x32 >	key_x3MAC  +		gprC X t8		> x1		XOR	 key_x1, key_x2 >	key_resultMACP +		gprC X t1		> MAC		BREV key_result		>   key_resultMAC  +		gprS X t5		> x3		XOR	 key_x2, key_result > key_resultMACP +		gprC X t3		> MAC		XOR	 key_x3, key_result > key_resultMAC  +		gprS X t8		> x5		NOPMACP -		gprS X t1		> MAC		MOV  fR				>	MACPMAC  +		gprC X t5		> x7		LSH	 key_serial >> 5	 > key_x32MACP -		gprS X t4		> MAC		ADDV key_result, key_x32 > key_resultMAC  +		gprC X t7		> x2		NEG  ALU_SHIFT			 > ALU_SHIFTMACP +		gprC X t2		> MAC		ADD	 ALU_SHIFT, ONE		 > ALU_SHIFTMAC  +		gprS X t6		> x4		ROL	 key_result			 > key_x1MACP +		gprC X t4		> MAC		XOR	 key_result, key_x1 > key_resultMAC  +		gprS X t7		> x6		SUB	 key_result, key_key > key_diff
Quote: > Expert Reverb 2 FDN:MACP -		gprS X t4		> MAC		XOR	 key_x3, key_x32 >	key_x3MAC  +		gprC X t8		> x1		XOR	 key_x1, key_x2 >	key_resultMACP +		gprC X t1		> MAC		BREV key_result		>   key_resultMAC  +		gprS X t5		> x3		XOR	 key_x2, key_result > key_resultMACP +		gprC X t3		> MAC		XOR	 key_x3, key_result > key_resultMAC  +		gprS X t7		> x5		NOPMACP -		gprS X t1		> MAC		MOV	 fR				>	MACPMAC  +		gprC X t5		> x7		LSH	 key_serial >> 5	 > key_x32MACP -		gprS X t3		> MAC		ADDV key_result, key_x32 > key_resultMAC  +		gprC X t7		> x2		NEG  ALU_SHIFT			 > ALU_SHIFTMACP +		gprC X t2		> MAC		ADD	 ALU_SHIFT, ONE		 > ALU_SHIFTMAC  +		gprS X t6		> x4		ROL	 key_result			 > key_x1MACP +		gprC X t4		> MAC		XOR	 key_result, key_x1 > key_resultMAC  +		gprS X t8		> x6		SUB	 key_result, key_key > key_diff

---

### Post #410 -- Page 14
**User:** DrFrankencopter
**Info:** Joined: Sep 2003Posts: 1,016My Studio🎧 20 years | Posts: 1,016My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4695385&postcount=410>

Quote: > Originally Posted byzmix➡️Present.I posted all of this information several months back on this thread(here), including the algo descriptions. As well as audio comparisons of the two algos(here).Yup, it was your post that reminded me that I had the algo's on one of my PC's.


Cheers


Kris

---

### Post #411 -- Page 14
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4740584&postcount=411>

This is a beautiful thread.

I've been reading the whole list of messages.


I'm working on a reverb, I'm trying to apply a different approach. No feedback at all. A totally "FIR" reverb.


This is a test:

[Hall with Echoes](http://www.sknote.it/Download/Verbera/Verbera_Test_301009_Audio/Verbera_Test_301009_Hall%20Echoes.wav)


Would anybody mind to comment the sound? It would be great.


(I've uploaded more audio samples and the IRs I've used on the homepage [here](http://www.sknote.it), if anybody is interested in testing the response on different audio)


Quinto

---

### Post #412 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4740681&postcount=412>

Quote: > Originally Posted byquintosardo➡️This is a beautiful thread.I've been reading the whole list of messages.I'm working on a reverb, I'm trying to apply a different approach. No feedback at all. A totally "FIR" reverb. QuintoIsn't it?  


The audio sample sounds nice.  Is this a convolution reverb or are you manually defining the FIR impulse response?

---

### Post #413 -- Page 14
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4740757&postcount=413>

I'm designing an algorithmic impulse response generator.

What you hear in the example is the audio through a commercial convolution reverb, using the IR I generated.


I was tempted by a different approach (is it?): avoid feedback and use "brute-force" computation.


Several "room modeling" raytraced systems already exist, but this one isn't. It is on the "algorithmic" side.

---

### Post #414 -- Page 14
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4741432&postcount=414>

Quote: > Originally Posted byquintosardo➡️I'm designing an algorithmic impulse response generator.Good idea, and it sounds great!



-Casey

---

### Post #415 -- Page 14
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4743690&postcount=415>

Thanks!


I'm wondering which features would be interesting to add.

I already have:


- early refls frequency dampening

- late refls attack and release time

- late refls frequency dampening

- statistical properties of the reflections (this software is statistically based instead of modeling or cascading and modulating)

- stereo width path (i.e. mono evolving to stereo)

- stereo echoes


I wonder if it is a common practice to let the stereo signal go in that "out-of +/-90deg" region, or "ultra-wide_non mono compatible"?

Mmmhhh...

---

### Post #416 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4803488&postcount=416>

It sure -looks- like a larc... Anyone know who's behind this?

![](https://static.gearspace.com/util/imgext.php?u=http%3A%2F%2Fplugindiscounts.com%2FNEWReverb.jpg&h=a62c6c9be781db9d78f954c260b07990)

---

### Post #417 -- Page 14
**User:** maky357
**Info:** Joined: Jul 2008Posts: 58🎧 15 years | Posts: 58
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4803690&postcount=417>

Quote: > Originally Posted byzmix➡️It sure -looks- like a larc... Anyone know who's behind this?Looks like Lexicon device

---

### Post #418 -- Page 14
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4805659&postcount=418>

Quote: > Originally Posted byquintosardo➡️I wonder if it is a common practice to let the stereo signal go in that "out-of +/-90deg" region, or "ultra-wide_non mono compatible"?Mmmhhh...Good question. From the algorithms I have seen and/or written, there are a few approaches:


- Use totally different output taps for left/right. This is the approach used by Lexicon and many others. For your algorithm, this would correspond to different random seeds for the left and right channels.


- Combine all of the output taps with different phase inversions for the left and right channels. A quick example, dating back to the Schroeder days: Let's say that you have a mono reverb with 3 series allpasses feeding 4 parallel combs. The combs can be combined for left and right outputs as follows:


outL = comb1+comb2-comb3-comb4

outR = comb1-comb2+comb3-comb4


This gives you a nice spatial spread, when listened to in stereo. However, if you sum things to mono, you get


outL+outR = 2*comb1 - 2*comb4


as comb2 and comb3 cancel out. 


The "ultra wide non mono compatible" approach comes from having inverted phases for the same signal in the left and right channels, which results in a "phantom rear" speaker. This is a nice effect for 3D imaging, but it will create problems if summed to mono anywhere after it is performed.


So, is it a common practice? I'm not sure. The big question is if having reverbs that sum poorly to mono will create problems in today's listening environments. Most DAWs will automatically instantiate stereo plugins when processing the output of another stereo plugin. I have a gut feeling that the "pseudo-stereo" techniques that rely on phase diffferences (as opposed to different left-right delays) might create problems with some compressed audio algorithms, but this is just a gut feeling. 


Any thoughts on this topic from the heavy lifters here?

---

### Post #419 -- Page 14
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4843963&postcount=419>

Thanks Sean, that's exactly the point.


Listening to some reverbs, I noticed that left-right behaviour.

It is the most stereo sound you can get without going into the red zone.


So I set the algorithm to get alternating "taps" (I don't have taps, but it is the same). This gives me that nice stereo spread. If I go even 1 degree further, I come into the red zone. This opens the reverb and surrounds the listener. But that single more degree will simply disappear in mono.


I've listened to several impulse responses sampled from great devices, but I cannot trust in phase details from those, of course.


Summing to mono doesn't degrade the signal, anyway. It just cancels out the surrounding part (like in your example). So, it is just matter of loosing some headroom? (the out of phase signal takes that very_small headroom in each channel).


Another thing I was investigating (most about early reflections):


- A highpass filter starts closed (only high freqs pass through) and opens fast (to allpass) with reverb attack. Low frequencies start appearing in reflections when delay is long enough to avoid canceling out by comb filtering.


I know this is a totally different view (from delays and allpasses) but I'm working from a "impulse response" point of view.


In the meanwhile I decided to make that reverb "realtime" (I really enjoy the idea of a IR generator, but I found an incredibly low interest by people in such a solution)

---

### Post #420 -- Page 14
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4844288&postcount=420>

Quote: > Originally Posted byseancostello➡️Good question. From the algorithms I have seen and/or written, there are a few approaches:- Use totally different output taps for left/right. This is the approach used by Lexicon and many others. For your algorithm, this would correspond to different random seeds for the left and right channels.- Combine all of the output taps with different phase inversions for the left and right channels. A quick example, dating back to the Schroeder days: Let's say that you have a mono reverb with 3 series allpasses feeding 4 parallel combs. The combs can be combined for left and right outputs as follows:outL = comb1+comb2-comb3-comb4outR = comb1-comb2+comb3-comb4This gives you a nice spatial spread, when listened to in stereo. However, if you sum things to mono, you getoutL+outR = 2*comb1 - 2*comb4as comb2 and comb3 cancel out.The "ultra wide non mono compatible" approach comes from having inverted phases for the same signal in the left and right channels, which results in a "phantom rear" speaker. This is a nice effect for 3D imaging, but it will create problems if summed to mono anywhere after it is performed.So, is it a common practice? I'm not sure. The big question is if having reverbs that sum poorly to mono will create problems in today's listening environments. Most DAWs will automatically instantiate stereo plugins when processing the output of another stereo plugin. I have a gut feeling that the "pseudo-stereo" techniques that rely on phase diffferences (as opposed to different left-right delays) might create problems with some compressed audio algorithms, but this is just a gut feeling.Any thoughts on this topic from the heavy lifters here?I think that antiphase output pairs are always a bad idea when simulating reverb.  They exist in the Schroeder theory only because they are computationally efficient, not because they sound good.


 One aspect that is not considered by this approach is that absolute antiphase of a complex signal simply does not exist in nature.  


If you are in an enclosed space  with a dimension of 4 meters between two of the walls and play the low "E" string on a guitar while standing in the center, the 82.4hz fundamental will be in antiphase *at that position* (also known as a 'null' in acoustical nomenclature).


Similarly, if you position two taps 6ms apart and pan one hard left and one hard right you will have a similar antiphase *at that frequency*.  


It's not important to concern yourself with musical note frequencies, and alternately, attaining a random distribution of nodes may be considered a theoretical ideal, but  there is a very good reason why reverb design is considered as much "art" as "science" and this is an example of where the former comes to the rescue of the latter. There are no shortcuts to creating a truly great reverb.


---

## Page 15

---

### Post #421 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4864692&postcount=421>

Below I have provided a screen shot showing the output each of the 4 reverb algorhythms of my 1980s era SONY DRE-2000,  fed by a single sample impulse and with the decay adjusted to 0.1s  (minimum is 0.0s but that produces no output..).  Note how diffuse algos B, C and D are..!

**EDIT:  The file lengths pictured below are exactly 233ms  from beginning to end.**

---

### Post #422 -- Page 15
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4864988&postcount=422>

Quote: > Originally Posted byShy➡️Can anyone explain what a "true stereo algorithm" even means?It means that the left and right inputs contribute uniquely to both of the left and right outputs. True stereo reverb requires four unique channels of reverb to do this.


The Lexicon reverb is a one channel reverb. It takes the pair of inputs and places them in a single delay loop, then outputs this mixed left/right signal at different times on the left and right outputs.



-Casey

---

### Post #423 -- Page 15
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865009&postcount=423>

Quote: > Originally Posted byCasey➡️It means that the left and right inputs contribute uniquely to both of the left and right outputs. True stereo reverb requires four unique channels of reverb to do this.The Lexicon reverb is a one channel reverb. It takes the pair of inputs and mixes them up then outputs this mix at different times on the left and right outputs.-CaseyWhat do you mean by "mixes them up"? And how is it a "one channel" reverb if when I input something panned hard left, the output I get has a distinct left bias? That's not stereo?

---

### Post #424 -- Page 15
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865034&postcount=424>

Quote: > Originally Posted byShy➡️What do you mean by "mixes them up"? And how is it a "one channel" reverb if when I input something panned hard left, the output I get has a distinct left bias? That's not stereo?That bias is related to the timing of the first few output taps. The bias you hear is based on the Haas effect which causes you to locate the sound at the first location you hear it at.


After this initial perception, a single channel reverb (even with stereo inputs) cannot be distinguished from a mono input reverb, so all of the left/right sound stage is lost during the remaining reverb time.



-Casey

---

### Post #425 -- Page 15
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865040&postcount=425>

Sorry, I have no idea what you mean, because the output definitely has a stereo sound stage. Hi-hat on the left, snare in the middle, guitar half to the right, and the output reflects that. It's nothing like a mono input reverb.

---

### Post #426 -- Page 15
**User:** audio ergo sum
**Info:** Joined: Oct 2008Posts: 3,644🎧 15 years | Posts: 3,644
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865061&postcount=426>

Quote: > Originally Posted byCasey➡️That bias is related to the timing of the first few output taps. The bias you hear is based on the Haas effect which causes you to locate the sound at the first location you hear it at.After this initial perception, a single channel reverb (even with stereo inputs) cannot be distinguished from a mono input reverb, so all of the left/right sound stage is lost during the remaining reverb time.-Caseytrying to understand: In real life it is the same, no? After the ER (Haas) you have the diffuse sound  field, and no discrete direction is perceptible anyway, except a general average energy distribution from a certain direction. (e.g. in a high church from top, which in a stereo reproduction will cause a tendency toward a mono tail)


AFAIK you would need true stereo processing the way you describe it only for simulating rooms that are very asymmetric, in shape and boundary layer material, no?

---

### Post #427 -- Page 15
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865098&postcount=427>

Quote: > Originally Posted byaudio ergo sum➡️In real life it is the same, no? After the ER (Haas) you have the diffuse sound  field, and no discrete direction is perceptible anyway.In very general terms you are correct. But there is a gradual shift from the left/right soundstage to a fully mixed room.


It does not happen instantly. If the reverb time of the room is less than the time it takes for the sound in the room to become fully mixed, the left/right soundstage remains intact throughout the reverb time.


Some critical listening will make this point very clearly. When adding reverb to spot mics for solo instruments within an orchestra, or simply augmenting the room mics, it is (as I believe you know) very important to match the mixing time of the added synthetic reverb to the natural acoustics.


Controlling this mixing time has only become possible using true stereo synthetic reverb. When the mixing time is too quick, as is often the case with other technologies, the added synthetic reverb can sound quite like a mono ball of soup sitting in the middle of the soundstage.


Try it out for yourself, I know you will hear this.



-Casey

---

### Post #428 -- Page 15
**User:** audio ergo sum
**Info:** Joined: Oct 2008Posts: 3,644🎧 15 years | Posts: 3,644
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865386&postcount=428>

Quote: > Originally Posted byCasey➡️In very general terms you are correct. But there is a gradual shift from the left/right soundstage to a fully mixed room.Interesting. I'm not sure I understand you fully. A "fully mixed room" you mean the room fully excited, energy evenly distributed?


Time wise we are talking about the first 100 ms here? Probably even shorter, for bass possibly longer?

Quote: > It does not happen instantly. If the reverb time of the room is less than the time it takes for the sound in the room to become fully mixed, the left/right soundstage remains intact throughout the reverb time.That would be the case for very small/dry rooms only? Rooms that basically never develop a diffuse sound field, since diffuse energy falls below relevant levels too quickly?

If the ER stage of a reverb algorithm is fully stereo that would be sufficient to take care of that?

Quote: > Some critical listening will make this point very clearly. When adding reverb to spot mics for solo instruments within an orchestra, or simply augmenting the room mics, it is (as I believe you know) very important to match the mixing time of the added synthetic reverb to the natural acoustics.Actually IME it is not that clear. Often the artificial reverb serves as an antagonist, filling in where the original acoustic lacks the desired ideal characteristics. Like when bringing up the gain of instruments in the rear, but keeping their perceived depth, woodwinds for example. I use less predelay for them, augmenting ER and simulating short distances between players and room boundaries even if they are not present for them in the real room.

Quote: > Controlling this mixing time has only become possible using true stereo synthetic reverb. When the mixing time is too quick, as is often the case with other technologies, the added synthetic reverb can sound quite like a mono ball of soup sitting in the middle of the soundstage.To me that often happens when the required effect is ambiance like, but a full reverb is mixed in.


That is IME the advantage of the heavily modulated tails. They are giving the lateral envelopment/side energy when existing room sound is mixed with artificial ones.


A lot of that heated discussion between the modulated vs more natural room evangelists and their favored devices comes down to comparing apples with oranges. (as in the factory presets :-)


You need different effects if you are either adding reverb to a mostly dry source (adding reverb to samples or dry small-studio recordings) or if you are enhancing a mix that already contains substantial room information.


Anyway, when it comes to music - sound for picture is a different beast - recreating real spaces is not what we need primarily, since real rooms are compromises all the time. The strength of artificial reverb is to add room sound that can not be created in reality, but supports the musical blend.


I remember David Griesinger gave a lecture where he talked about the 50-150ms time window obstructing clarity.  Difficult to impossible in a real room to attenuate reflections in that time window, but easy to do in an artificial reverb.

---

### Post #429 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4865707&postcount=429>

Quote: > Originally Posted byShy➡️What do you mean by "mixes them up"? And how is it a "one channel" reverb if when I input something panned hard left, the output I get has a distinct left bias? That's not stereo?Allow me to clarify.. in a typical Lexicon algo (for example, the concert hall), the left input goes through some input diffusion and some allpasses and along the way the signal is 'tapped' from this stream.  These taps are summed and output to the left channel (primarily). 


The right channel takes an identical route through it's own diffusion and allpasses and it's taps are output to the right channel (primarily).


Here is where the 'not true stereo' comment comes from.  In the lexicon, the output of the 'left' string of allpasses is fed into the right channel input and the output of the right channel allpasses is fed into the left channel input.  It's sort of a continuous loop, like a traffic roundabout.  Any signal injected into the left side will appear on the right side after one cycle.  It's simple and yet ingenius, and it cetainly does give a sense of 'stereo'... signals on the left appear on the left quickly and later on the right in a more diffuse and entirely reverberant way.


This brings up an interesting point about 'true stereo' reverb.  Most of the convolution based reverbs produce a "stereo" reverb as two panned mono reverbs, with no cross coupling effects.  It's pretty obvious why, but there are ways around this that involve creating a set of four mono in stereo out impulses.

---

### Post #430 -- Page 15
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866029&postcount=430>

Quote: > Originally Posted byzmix➡️Here is where the 'not true stereo' comment comes from.  In the lexicon, the output of the 'left' string of allpasses is fed into the right channel input and the output of the right channel allpasses is fed into the left channel input.  It's sort of a continuous loop, like a traffic roundabout.  Any signal injected into the left side will appear on the right side after one cycle.  It's simple and yet ingenius, and it cetainly does give a sense of 'stereo'... signals on the left appear on the left quickly and later on the right in a more diffuse and entirely reverberant way.Thanks for the explanation. But unless I'm completely mixing up something, Nobody Special's explanation completely contradicts yours and describes what you describe as "not true stereo" as what -is- "true stereo", and so what can I say.. what's "false" about it anyway? Is NS wrong?
Quote: > Originally Posted byNobody Special➡️Oh yes they have.  I'll reiterate that statement right here.  There are a few of the older products (PCM70, LXP-1) that aren't,  buteverythingin the last several years--even the inexpensive MX series--is true stereo.  In a stereo reverb, the earliest part of the reverb energy is located in the channel where the dry audio energy enters.  Over the next several tens of milliseconds, depending on the room size, that energy becomes evenly distributed among channels.I'll extend that statement to our surround reverbs.  Unlike a kludge in which a number of stereo reverbs are cobbled together, our surround reverbs follow the same pattern.  Early signal is in or near the location of the dry signal and then becomes evenly distributed over time.

---

### Post #431 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866225&postcount=431>

Quote: > Originally Posted byShy➡️Thanks for the explanation. But unless I'm completely mixing up something, Nobody Special's explanation completely contradicts yours and describes what you describe as "not true stereo" as what -is- "true stereo", and so what can I say.. what's "false" about it anyway? Is NS wrong?No, NS is correct and what we are describing is exactly the same thing.  The confusion here seems to stem from the dogmatic use of the term "true stereo". Remember, the menu is not the food...


 The Lexicon approach generally replicates the physics of what happens in a room.    I have several Sony reverbs that are also 'true stereo' and work in a different way than the Lexicon. Many ways to do it, all highly effective.

---

### Post #432 -- Page 15
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866508&postcount=432>

Quote: > Originally Posted byaudio ergo sum➡️Interesting. I'm not sure I understand you fully. A "fully mixed room" you mean the room fully excited, energy evenly distributed?Time wise we are talking about the first 100 ms here? Probably even shorter, for bass possibly longer?I completely agree with the points of view you have expressed. It is clearly based on years of hard won knowledge.


It is just this first concept that I am challenging. When matching a good room or hall by ear, the perceived stereo field persists in the reverberant energy for much longer than anticipated. Sound just does not homogenize as quickly as an energy distribution model would suggest. 


Having proper control over mixing times in a synthetic reverb allows synthetic reverb to better match existing acoustics, or in fact create more realistic spaces from dry material.


I agree with your point of view that this is not always the role of a reverb in an artistic process.


But I have spent the time to incorporate these observations into an available existence proof should anyone care to perform their own listening and form their own impressions as to whether or not they have merit.



-Casey

---

### Post #433 -- Page 15
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866584&postcount=433>

Quote: > Originally Posted byzmix➡️The confusion here seems to stem from the dogmatic use of the term "true stereo".I did not intend to use the words "true stereo" as it pertains to reverb in anything but their true meaning. Which is to say that the left and right inputs can affect both of the left and right outputs uniquely through the entirety of the reverb time. This is why I mentioned the need for four reverb channels to accomplish this in my earlier post.


You are simply questioning the need for this. Not it's meaning. As I mentioned above in my response to AES, I believe that there is a need for this when certain qualities are asked for in a reverb.



-Casey

---

### Post #434 -- Page 15
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866655&postcount=434>

Quote: > Originally Posted byzmix➡️Below I have provided a screen shot showing the output each of the 4 reverb algorhythms of my 1980s era SONY DRE-2000,  fed by a single sample impulse and with the decay adjusted to 0.1s  (minimum is 0.0s but that produces no output..).  Note how diffuse algos B, C and D are..!Very clear build from series allpasses in the attacks of the impulse responses. The more allpasses in series you use, the longer it takes for the signal to "fade in."

---

### Post #435 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866879&postcount=435>

Quote: > Originally Posted byseancostello➡️Very clear build from series allpasses in the attacks of the impulse responses. The more allpasses in series you use, the longer it takes for the signal to "fade in."I assume you mean "clearly built"... and yes, I agree.. these graphical examples represent only a few hundred ms, so you can see how the various algos use a collection of short allpasses.  When the reverb time is extended there are discernable patterns as well, remember that this was Sony's FIRST attempt at digital reverb, and was based on early 1980s technology, the allpass loops are quite short.  It is somewhat surprising how much diffusion they used (it is NOT user adjustable) in the B, C and D algos.

---

### Post #436 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4866901&postcount=436>

Quote: > Originally Posted byCasey➡️I did not intend to use the words "true stereo" as it pertains to reverb in anything but their true meaning. Which is to say that the left and right inputs can affect both of the left and right outputs uniquely through the entirety of the reverb time. This is why I mentioned the need for four reverb channels to accomplish this in my earlier post.You are simply questioning the need for this. Not it's meaning. As I mentioned above in my response to AES, I believe that there is a need for this when certain qualities are asked for in a reverb.-CaseyI completely understand your "four path" description,  and I'm certainly not questioning the need for that, and as I stated above I have several reverbs that are "true stereo" and have unique paths for the left and right inputs, and I have also recreated true stereo reverbs using IR plugins by making a set of four impulses and layering the results.


There are many ways to emulate the nature of sound from various source locations and listening positions.

---

### Post #437 -- Page 15
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4868583&postcount=437>

Quote: > Originally Posted byzmix➡️I assume you mean "clearly built"Nope, I meant "clearly build." The way that the impulses gradually build in energy is very indicative of the output of several series allpasses. The more allpasses, the longer it takes to build. This is why a reverb with allpasses in a loop, and a single tap at the end of a loop, sounds like it is "fading in." I think this is a good example of the Central Limit Theorem in action: convolve a whole bunch of impulse responses together, and the output resembles a Gaussian curve.

---

### Post #438 -- Page 15
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4868820&postcount=438>

Quote: > Originally Posted byseancostello➡️...I think this is a good example of the Central Limit Theorem in action: convolve a whole bunch of impulse responses together, and the output resembles a Gaussian curve.You mean in time domain, right?

It sounds ok, if you think of reverb IRs like "about-but-not-so-flat" very long EQs... putting lots of eqs in series should give something similar to a bandpass... with a bell-shaped IR.


About the IRs: while working on reverb, I'm looking for that "surrounding" effect. I think EQ has a great part in that effect, so I'm testing something like "those spikes in the IR are echoes, I equalize them with different EQs like they come from different directions". No HRTF, just different EQs.


I wonder if it is a trivial approach...


And I was wondering if any approach similar to "K-Stereo" by Bob Katz is commonly included in reverbs: Haas-time-range EQd delays with antiphase.

I experimented with some IRs I built to understand K-Stereo and they look effective, while I didn't try the real thing.


Any thought on this? EQ and Haas effect for more surrounding effect...

---

### Post #439 -- Page 15
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4868910&postcount=439>

Quote: > Originally Posted byseancostello➡️The way that the impulses gradually build in energy is very indicative of the output of several series allpasseswith coefficients in the range [-0.618; 0.618]. The more allpasseswith the coefficients in previous mentioned range, the longer it takes to build.Fixed for you.

---

### Post #440 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4869292&postcount=440>

Quote: > Originally Posted byseancostelloThe way that the impulses gradually build in energy is very indicative of the output of several series allpasseswith coefficients in the range [-0.618; 0.618].The more allpasseswith the coefficients in previous mentioned range,the longer it takes to build.Fixed for you.Quote:Originally Posted byWarp69➡️Fixed for you.Precisely.. Higher coefficients can actually result in faster build, and obviously lower ones will too.


I made an allpass which reached maximum density at around 0.6, but had the slowest attack at 0.33...  interesting.

---

### Post #441 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4869313&postcount=441>

Quote: > Originally Posted byseancostello➡️Nope, I meant "clearly build." The way that the impulses gradually build in energy is very indicative of the output of several series allpasses. The more allpasses, the longer it takes to build. This is why a reverb with allpasses in a loop, and a single tap at the end of a loop, sounds like it is "fading in." I think this is a good example of the Central Limit Theorem in action: convolve a whole bunch of impulse responses together, and the output resembles a Gaussian curve.

OK, I see what you were alluding to with that syntax...


In the case of the DRE-2000 the reverb 'tank' does not seem to contain any allpass elements in the feedback and therefor will not exhibit the response you mention.  I have been playing around with more constant density topologies and I think that within the context of music they are more useful than the increasing density variety.

---

### Post #442 -- Page 15
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4876729&postcount=442>

About that "EQ and surrounding" concept, this is what I got while trying to identify "magnitude" localization cues from the Head Related Transfer Functions I downloaded from the net:

![](https://static.gearspace.com/util/imgext.php?u=http%3A%2F%2Fwww.sknote.it%2Fimages%2FVerbera%2FVerbera_HRTF.jpg&h=050bb7ec09b428164233a16fc1cad5b4)


They are the responses, in frequency domain, referred to the "look forward" response, on a horizontal plane. That peak at about 8kHz must be an error in the files.

---

### Post #443 -- Page 15
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4877767&postcount=443>

I'm still around, just I've not had much time to play with reverbs - too busy at work doing engine testing and firmware development.


The series allpasses in a row can be interesting. Try the Eventide 'black hole' algorithm with different allpass gain settings. That reverb is literally just a lot of allpasses in series, but to me the fade-in and fade-out don't sound natural at all. Interesting, but not really natural.


I almost always think in the time domain in signal processing (or the angle domain in engine management - think about it for a minute), very rarely do I move to the frequency domain. Well, for filters, yes, but for allpasses of the lengths commonly found in reverbs, I always think of it as a delay time - and how an impulse 'bunches up' in time. That's equivalent, I guess, to frequency buildups.

---

### Post #444 -- Page 15
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4881069&postcount=444>

Quote: > Originally Posted bydale116dot7➡️The series allpasses in a row can be interesting. Try the Eventide 'black hole' algorithm with different allpass gain settings. That reverb is literally just a lot of allpasses in series, but to me the fade-in and fade-out don't sound natural at all. Interesting, but not really natural.There are some reverbs around like the Blackhole that are absolutely not natural, but very interesting to use. Because they add emotion and mood to a sound. Thats the main reason I like the effected reverbs so much.

---

### Post #445 -- Page 15
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4896798&postcount=445>

I finally got my reverb out! I have say thanks to a lot of people here, because I learned a lot from the people in this thread!

---

### Post #446 -- Page 15
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4897584&postcount=446>

Quote: > Originally Posted byFroombosch➡️I finally got my reverb out! I have say thanks to a lot of people here, because I learned a lot from the people in this thread!Congratulations! And we have learned a lot from you, as well!

---

### Post #447 -- Page 15
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4897655&postcount=447>

Quote: > Originally Posted byFroombosch➡️I finally got my reverb out! I have say thanks to a lot of people here, because I learned a lot from the people in this thread!I was following the discussion on another site. Congratulations! 



-Casey

---

### Post #448 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4903789&postcount=448>

Quote: > Originally Posted byFroombosch➡️I finally got my reverb out! I have say thanks to a lot of people here, because I learned a lot from the people in this thread! Nice one, Harrie!

---

### Post #449 -- Page 15
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4938672&postcount=449>

[BBC research paper on artificial reverberation](http://www.bbc.co.uk/rd/pubs/reports/1972-19.pdf).... from 1972.!!

---

### Post #450 -- Page 15
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4940195&postcount=450>

Quote: > Originally Posted byzmix➡️BBC research paper on artificial reverberation.... from 1972.!!WOW. This paper is all kinds of awesome. And all kinds of crazy. 


It is clear that many of these ideas were never tried, as they would have figured out that their "solutions" only led to more problems. For example, the idea of pitch shifting a sound up and down to feed it into a scale model of a room will quickly lead to the issue of trying to create a "glitchless" pitch shifter for polyphonic signals. Current technology is closer, but the rotating tape heads shown are pretty far from "glitchless." I also like the plate that has to work in a vacuum. And the optical convolution seems to neglect that convolution requires some way of delaying the signal. Multiplying the current amplitude of the input signal with the current amplitude of the impulse response results in amplitude modulation with no decay. 


The final algorithm in the paper, "Artificial reverberation using pseudo-random sequences"...OK, that is worth its weight in gold. This is some pretty formidable prior art.


Thanks for the link! BTW, there is also a 1974 BBC Publication by Axon [EDIT: I couldn't find it, so it probably isn't BBC, and may not be Axon], that apparently proposes a physical reverberator that seems very close to the Ursa Major Space Station. If the Ursa Major Space Station was made up of pipes and hoses, with different sections of the pipes moving around and outputs LITERALLY tapped out of the moving sections. I haven't seen the 1974 publication (just references to it), so it might be far saner than what I just described.


---

## Page 16

---

### Post #451 -- Page 16
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4940463&postcount=451>

Quote: > Originally Posted byseancostello➡️WOW. This paper is all kinds of awesome. And all kinds of crazy.It is clear that many of these ideas were never tried, as they would have figured out that their "solutions" only led to more problems. For example, the idea of pitch shifting a sound up and down to feed it into a scale model of a room will quickly lead to the issue of trying to create a "glitchless" pitch shifter for polyphonic signals. Current technology is closer, but the rotating tape heads shown are pretty far from "glitchless." I also like the plate that has to work in a vacuum. And the optical convolution seems to neglect that convolution requires some way of delaying the signal. Multiplying the current amplitude of the input signal with the current amplitude of the impulse response results in amplitude modulation with no decay.The final algorithm in the paper, "Artificial reverberation using pseudo-random sequences"...OK, that is worth its weight in gold. This is some pretty formidable prior art.Thanks for the link! BTW, there is also a 1974 BBC Publication by Axon [EDIT: I couldn't find it, so it probably isn't BBC, and may not be Axon], that apparently proposes a physical reverberator that seems very close to the Ursa Major Space Station. If the Ursa Major Space Station was made up of pipes and hoses, with different sections of the pipes moving around and outputs LITERALLY tapped out of the moving sections. I haven't seen the 1974 publication (just references to it), so it might be far saner than what I just described.I wouldn't be so quick to dismiss the ideas in this presentation, Sean..  The BBC did, in fact, produce a 'glitchless'  pitch shifter by using rotating *crossfaded* tape heads. I have heard that it was used by the BBC radio workshop for some effects in the Dr Who show.   It's not that different from the MXR, Eventide or AMS pitch shift algos except for the technology employed.  FFT / iFFT pitch shifting was still a ways off in the 1970s....


 As far as a plate reverb operating in a vacuum, it was only the ultra thin nickel foil plate that was so affected by atmospheric pressure. It's interesting to note that Dr. Kuhl was working on a 0.1 square meter plate of 0.02mm thickness, I would guess this became the EMT 240 'gold foil' plate...  (here is the [PATENT](http://www.wikipatents.com/3719905.html-1), granted in 1973).  


If you read through some of the ideas presented in the BBC archives, you'd think that the BBC operated in a vacuume..!

---

### Post #452 -- Page 16
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4940816&postcount=452>

Quote: > Originally Posted byzmix➡️I wouldn't be so quick to dismiss the ideas in this presentation, Sean..  The BBC did, in fact, produce a 'glitchless'  pitch shifter by using rotatingcrossfadedtape heads. I have heard that it was used by the BBC radio workshop for some effects in the Dr Who show.   It's not that different from the MXR, Eventide or AMS pitch shift algos except for the technology employed.  FFT / iFFT pitch shifting was still a ways off in the 1970s....The rotating tape heads have natural crossfading, due to the tape heads moving away from the tape, but they still sound glitchy as all get out to me. I would love to hear more early examples; the only ones I have in my collection are "Hymnen" by Stockhausen (got the vinyl for $1.00) and "She's Goin' Bald" by The Beach Boys off Smiley Smile. Smiley Smile, BTW, has some great "dry" tracks for testing reverbs.


Having said that, would the glitches be audible in the given example? My guess is that the glitches might be diffused, at least for the input fed into the room. The output...well, that's a different story.


I've read an AES paper from the 50's or 60's that proposed a similar "small" reverb chamber, but with the signal transposed to the higher ultra-audio range by frequency shifting. This seems like it might be a cleaner solution.

Quote: > As far as a plate reverb operating in a vacuum, it was only the ultra thin nickel foil plate that was so affected by atmospheric pressure. It's interesting to note that Dr. Kuhl was working on a 0.1 square meter plate of 0.02mm thickness, I would guess this became the EMT 240 'gold foil' plate...  (here is thePATENT, granted in 1973).The Kuhl idea is great, but it ain't a BBC idea. Have you heard the gold plates? How do they sound compared to the EMT140?

Quote: > If you read through some of the ideas presented in the BBC archives, you'd think that the BBC operated in a vacuume..!It seems like a classic engineering shop, where ideas designed in house are weighted higher than external ideas.

---

### Post #453 -- Page 16
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4947638&postcount=453>

It is incredible to see how much technology, left apart because of costs, is today available for new, cheap, use!


That pseudo-random algorithm sound great and works great!


It is the basis of what I did (before reading this paper now) and posted as audio examples in this thread!


They say "4000£ hardware only"!


Ah, the endless beauty of today's CPUs...

---

### Post #454 -- Page 16
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4947654&postcount=454>

Quote: > Originally Posted byseancostello➡️.And the optical convolution seems to neglect that convolution requires some way of delaying the signal. Multiplying the current amplitude of the input signal with the current amplitude of the impulse response results in amplitude modulation with no decay.They write about convolution... I think that the mask is something like a 1D transmittance path... maybe something like this:


- a series of led represent a window in the signal (-> slice in ram)

- the mask has a line of slots, each one represents its multiplication factor with its transmittance

- a series of elements sense the light from the signal through the mask and all elements are summed together.


A common (today) convolution when you  couldn't afford ram and cpu power...

---

### Post #455 -- Page 16
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4950841&postcount=455>

About that "scaled room" approach.

If I'd want to do it with a small model of a room and put inside speaker and mic, i.e.:


- 10x20x5m real room

- 1:20 scaled down model: 50x100x0.25cm

- scaled up frequencies: 20-20000Hz -> 400-400000Hz (!!!)


Even if I do it in analog (I was thinking about digital, but...), how could I manage those frequencies?


Did I miss something?


If I simply want to get a big sound from a small real room:


- 1x2x3m a closet

- **5x10x15** a virtual chamber (1:5 scale)

- scaled up frequencies: 20-20000Hz -> 100-100000Hz


- 3x4x3m a bedroom

- **15x20x15** a virtual chamber (1:5 scale)

- scaled up frequencies: 20-20000Hz -> 100-100000Hz


Maybe this could be easily tested in digital...


But there is an important problem I think.

I remember from my mechanics studies that, if you want to scale a mech model you have to scale the characteristics of the materials, too!


Shouldn't I scale the acoustical parameters of the materials, too???


i.e.: simulate a material reflective at 10000Hz in a 1:20 scale -> use a material reflective at 200000Hz... (???)


A simple test could be very interesting for special effects, anyway...

Should sound like converting the IR from a real room by slowing down the sampling rate (no stretching, slowing down like a record)

---

### Post #456 -- Page 16
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4952790&postcount=456>

Ok, this is something done starting from that "random" method in that paper as a starting point.

We can consider it a "modern" application of that starting point, then it was developed further, adding some statistical variations, localization cues, parameters envelopes and pitch modulation.


This is a series of audio tests I did with Verbera. There is a lot of reverb, of course, being it a test.


The first track is a dry stereo recording I did:


- a live played grand piano

- a pair of large diaphragm condenser mics in stereo pair

[Dry stereo piano (extreme dynamics, because untouched)](http://www.sknote.it/download/Verbera/Verbera_Piano_Dry.wav)

[75% dry + 100% effect, early reflections + 500ms reverb](http://www.sknote.it/download/Verbera/Verbera_Piano_500ms.wav)

[1000ms reverb](http://www.sknote.it/download/Verbera/Verbera_Piano_1000ms.wav)

[2500ms reverb](http://www.sknote.it/download/Verbera/Verbera_Piano_2500ms.wav)

[5000ms reverb](http://www.sknote.it/download/Verbera/Verbera_Piano_5000ms.wav)


Then a test about the reverb modulation. The pitch modulation is set to a very high level, so that the reverb sounds "detuned" to the piano:

[Detuned reverb](http://www.sknote.it/download/Verbera/Verbera_Piano_5000ms_mod.wav)


It sounds very natural,to me (not the detuned one, of course). I cannot hear the reverb anymore after a while (in the short example) without going back to the dry sound.


Feedback would be great

---

### Post #457 -- Page 16
**User:** quintosardo
**Info:** Joined: Mar 2009Posts: 8,642🎧 15 years | Posts: 8,642
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4953192&postcount=457>

Some terribly overdone stereo drums:


[Dry](http://www.sknote.it/download/Verbera/Verbera_Drums_Dry.wav)

[Effected_2000ms](http://www.sknote.it/download/Verbera/Verbera_Drums_2000ms.wav)

---

### Post #458 -- Page 16
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4953257&postcount=458>

Quote: > Originally Posted byzmix➡️The BBC did, in fact, produce a 'glitchless'  pitch shifter by using rotatingcrossfadedtape heads. I have heard that it was used by the BBC radio workshop for some effects in the Dr Who show.   It's not that different from the MXR, Eventide or AMS pitch shift algos except for the technology employed.I've got a couple H949's and I had an H910, and even though the two DAC outputs crossfade, there is a 'glitch' - you can hear it at the splice frequency. It's some kind of audible discontinuity, where for low pitch shifts, sounds just a bit disturbed. There's no audible click, but there's a detectable modulation pattern happening. If you set the ramp voltages to just 'flip' - making the integration capacitor on the H910 ramp generators almost zero - the glitch is an audible 'click' with lots of high frequency content. When you slow the ramp down, the 'click' goes away, yet there's something not right about the audio when it comes out of there. Without reverse-engineering the H949 firmware and reprogramming the PROM's, you can't easily do the ramp trick, since they are generated in the firmware via a multiplexed DAC.


At high pitch shifts (0.85 or lower, 1.15 or higher), I can hear the modulation at the splice frequency quite a lot. Even with the H949+lupine board (algorithm 3), there is that 'glitching'. It's better, but not perfect. In flange/chorus modes, all of the glitching goes away - because the splicing goes away. It sounds reasonable in that case. Except the 11-bit ADC/DAC system, which doesn't sound that good.


I've never been particularly happy with any pitch shifter except my Antares, and even then, only if it's correcting under about 40 or 50 cents.

---

### Post #459 -- Page 16
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4956284&postcount=459>

Quote: > Originally Posted byzmix➡️IOne aspect that is not considered by this approach is that absolute antiphase of a complex signal simply does not exist in nature.If you are in an enclosed space  with a dimension of 4 meters between two of the walls and play the low "E" string on a guitar while standing in the center, the 82.4hz fundamental will be in antiphaseat that position(also known as a 'null' in acoustical nomenclature).Similarly, if you position two taps 6ms apart and pan one hard left and one hard right you will have a similar antiphaseat that frequency.I was digesting this problem this morning, came to a similar solution, and went back and found this posting where you went back in time and figured out what I just figured out.  


You are totally right. Regardless of any problems that truly antiphase components will create in a reverb (and there are lots of these problems, especially when mixing to mono, or working with any audio compression or surround system that matrixes signals together), the fact remains that such a situation does not exist in the physical world.

---

### Post #460 -- Page 16
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4992239&postcount=460>

[Speculation on]


Regarding the UA announcement - I see that you have found good use of the rom readouts and reengineered code of the Lex 224.


[Speculation off]

---

### Post #461 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4992275&postcount=461>

Quote: > Originally Posted byWarp69➡️[Speculation on]Regarding the UA announcement - I see that you have found good use of the rom readouts and reengineered code of the Lex 224.[Speculation off]Yes, but David Griesinger already has the code. He has always been just a wee bit competitive with Barry Blesser. At the very least he has an introduction!


and Warp, back to work 


Edit: Oh yeah, me too!



-Casey

---

### Post #462 -- Page 16
**User:** thethrillfactor
**Info:** Joined: Jun 2002Posts: 20,0894 Reviews written🎧 20 years | Posts: 20,089
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=4998792&postcount=462>

Quote: > Originally Posted byseancostello➡️Do any of the people on this thread know what is currently going on with reverb pioneers like:- David Griesinger- Tony Agnello- Christopher MooreI know that Griesinger is no longer associated with Harman, but I don't know what he is doing right now (he could be happily retired for all I know). Agnello licensed one of the SP2016 algorithms for the XBox360 a few years back, and Moore had a reissue of the Space Station, but I haven't heard anything for a few years.I figure this thread would be as good a place as any to ask.On a similar note, are there any reverb people that haven't got much credit for their work, that anyone wants to call out? For example, I am a huge fan of Michael Gerzon's early 1970's work, that doesn't seem to get much acknowledgment.Tony Agnello is head of Princeton Digital designer of the latest hardware Reverb 2016 and the coding for the Eventide 2016 plug ins and Space Station SST-282 plug in.


Christopher Moore reissued his new version of the Space Station the SST-206 under the company Seven Woods audio Inc a couple of years ago.

---

### Post #463 -- Page 16
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5125496&postcount=463>

Quote: > Originally Posted bythethrillfactor➡️Tony Agnello is head of Princeton Digital designer of the latest hardware Reverb 2016 and the coding for the Eventide 2016 plug ins and Space Station SST-282 plug in.Christopher Moore reissued his new version of the Space Station the SST-206 under the company Seven Woods audio Inc a couple of years ago.This is true, but both of these events are several years old at this point. I think that the XBox 360 reverb was the last Princeton Digital announcement, and I think that was in 2005. The SST-206 no longer seems to be for sale.

---

### Post #464 -- Page 16
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5128001&postcount=464>

Life goes is different dirrection for a lot of people. Techniques and skills from reverb engineering can be used in other applications as well. It definetly shows that someone has really got good endurance and likes physics.

---

### Post #465 -- Page 16
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5130600&postcount=465>

Do we use audio samples that have appeared in this thread to show examples of stuff? And is it OK to just use whatever examples are around, or are there particular samples that are best to use?


I've had odd unserious Airwindows reverbs kicking around for a while, but largely thanks to this thread, I now have some serious ones and would like to post to the thread and talk shop 


I'm particularly wondering how people hunt down combinations of combs that lead to a 'hot' note on the verge of feedback. I can't get anywhere near a 'infinite' reverb through feedback, allpasses and combs alone (possibly I'm totally missing an obvious point and nobody does that). So I have a far-field reverb I quite like, but there are real limits to how 'live' I can make the room on certain sources. It's very nice but for those few hotspots- I do have to push the liveness rather extremely to get the feedbacking notes.


-chris

---

### Post #466 -- Page 16
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5131451&postcount=466>

On a loop style of reverb, infinite is pretty easy to get - set the loop gain to 1. To find hot-spots, I put loop diffusion to zero, inject some signal when in infinite mode, then slowly turn up diffusion until something starts to oscillate or ring. On single-loop reverbs, I find that at an infinite setting, allpass gains above about 0.6 or 0.7 tend to ring, and also the smaller the delay line length, the more likely you have ringing or even full-blown oscillation. It's helpful to have clickless (ramped) gain changes.

---

### Post #467 -- Page 16
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5180324&postcount=467>

Quote: > Originally Posted bychrisj➡️Do we use audio samples that have appeared in this thread to show examples of stuff? And is it OK to just use whatever examples are around, or are there particular samples that are best to use?-chrisIt depends on what the reverb is intended to do. I listen to pulses and snares to hear if the reverb is smooth enough. I also use some instruments to hear if depth, width, colour of the reverb is usable. On the version 2.0 of the EMpTy 250 I did a lot of tweaking listening to vocals, snares, guitars and pulses. 


As you see in this thread some people use spectum analysers, oscilators and other stuff to listen what is going on in other reverbs...

---

### Post #468 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5181270&postcount=468>

Quote: > Originally Posted bychrisj➡️I'm particularly wondering how people hunt down combinations of combs that lead to a 'hot' note on the verge of feedback. I can't get anywhere near a 'infinite' reverb through feedback, allpasses and combs alone (possibly I'm totally missing an obvious point and nobody does that).You should never have runaway feedback in a properly designed reverb.


Avoid comb filters in feedback paths. This is a basic no-no.


Even when modulated (depending on the type of modulation), NESTED allpasses can behave poorly as well. Smaller ones will show the problem more often because the taps are closer and the signal more coherent. Large tap spacing can reduce this to a negligible risk, but in the end they will always get you.


Some algorithms have this problem even though the taps are spaced fairly widely. With the right source, you can hear feedback build up, but then break up before it becomes runaway, as the modulation moves things around. 



-Casey

---

### Post #469 -- Page 16
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5182927&postcount=469>

Quote: > Originally Posted byCasey➡️Even when modulated (depending on the type of modulation), NESTED allpasses can behave poorly as well. Smaller ones will show the problem more often because the taps are closer and the signal more coherent. Large tap spacing can reduce this to a negligible risk, but in the end they will always get you.I need to do an analysis of the poles in nested allpasses someday. It seems like the delay in the innermost allpasses would result in poles that are much closer to the unit circle. Turn up the decay (i.e. global feedback) of the whole network, and the result is a metallic ring to the decay, as the innermost allpass will ring longer than any of the other delays. 


I've also run into situations where modulating allpasses can result in true instability (not just ringing, but the classic reverb blowup sound), as the modulation breaks the whole LTI property. However, this was for some pretty extreme modulation widths and speeds, and the pitch will start sounding way wobbly before the network starts to become unstable.

---

### Post #470 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5182953&postcount=470>

Quote: > Originally Posted byseancostello➡️the result is a metallic ring to the decay, as the innermost allpass will ring longer than any of the other delays.Hmmm, not sure I see what you mean.


An allpass filter does not have a metallic ring, it is allpass. Allpass filters can lead to a metallic sound because of their regular spectral smear. At the same gain, smaller allpass filters will have less spectral smear, and will cause less of a metallic residue in the tail.


Allpass funky sonics can be caused by beat patterns they set up, which is the sound of an allpass ringing out. But the much larger problem is their phase relationships with other elements in the structure.



-Casey

---

### Post #471 -- Page 16
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5185408&postcount=471>

But if you set the allpass coefficient to 1, do you not get an oscillator internally? If you use within-allpass output taps (and I know that structure exists in commercial offerings), wouldn't you'd hear it as a ringing?

---

### Post #472 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5185596&postcount=472>

Quote: > Originally Posted bydale116dot7➡️But if you set the allpass coefficient to 1, do you not get an oscillator internally? If you use within-allpass output taps (and I know that structure exists in commercial offerings), wouldn't you'd hear it as a ringing?If you take a tap from within the allpass. We are no longer talking about an allpass. This is like starting a discussion with, "if a square was a circle..."



-Casey

---

### Post #473 -- Page 16
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5186986&postcount=473>

Quote: > Originally Posted byCasey➡️You should never have runaway feedback in a properly designed reverb.Avoid comb filters in feedback paths. This is a basic no-no.Interesting! Is feedback just not as useful as I'd think it would be? I was playing with what I thought was an approach people sometimes did- the allpasses to blur out things, then loads of parallel combs in a reverb tank, then feedback from the output of that back to before the allpass, with other stuff like coloration and some motion on the delay taps. (I think I'm just modulating combs, and not the allpasses, which tend to be shorter)


I asked about the samples because I tweaked things like mad using your own dry signal sources- the guitar, the orchestra, the rimshot- and stuff like the rimshot was very tough to get to work. For the orchestra the hard part was getting lows to bloom nicely. The guitar just sounds nice in general 


I thought you could use feedback with combs in the loop- I sure didn't end up using a lot, I'll say that. I put in a feature where there's a darkness control that applies to lots of different parameters at once, and one was the global feedback. I don't think what I got works real well for incredibly long RT60, though it seems to get okay diffusion when damping is much less. (My first verb attempts were a lot sillier, but I try to learn from my mistakes...)

---

### Post #474 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187021&postcount=474>

Quote: > Originally Posted bychrisj➡️Interesting! Is feedback just not as useful as I'd think it would be? I was playing with what I thought was an approach people sometimes did- the allpasses to blur out things, then loads of parallel combs in a reverb tank, then feedback from the output of that back to before the allpass, with other stuff like coloration and some motion on the delay taps. (I think I'm just modulating combs, and not the allpasses, which tend to be shorter)I asked about the samples because I tweaked things like mad using your own dry signal sources- the guitar, the orchestra, the rimshot- and stuff like the rimshot was very tough to get to work. For the orchestra the hard part was getting lows to bloom nicely. The guitar just sounds nice in generalI thought you could use feedback with combs in the loop- I sure didn't end up using a lot, I'll say that. I put in a feature where there's a darkness control that applies to lots of different parameters at once, and one was the global feedback. I don't think what I got works real well for incredibly long RT60, though it seems to get okay diffusion when damping is much less. (My first verb attempts were a lot sillier, but I try to learn from my mistakes...)I should have been more specific; No tapped delay lines in the feedback loop.


It is clear how these will amplify certain frequencies yes? Deadly!



-Casey

---

### Post #475 -- Page 16
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187052&postcount=475>

Quote: > Originally Posted bychrisj➡️Is feedback just not as useful as I'd think it would be? I was playing with what I thought was an approach people sometimes did- the allpasses to blur out things, then loads of parallel combs in a reverb tank, then feedback from the output of that back to before the allpass, with other stuff like coloration and some motion on the delay taps. (I think I'm just modulating combs, and not the allpasses, which tend to be shorter)I believe most people use FDN which is loads of parallel delaylines with a feedback matrix (household, hadamard etc matrix)

---

### Post #476 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187079&postcount=476>

Quote: > Originally Posted byWarp69➡️I believe most people use FDN which is loads of parallel delaylines with a feedback matrix (household, hadamard etc matrix)Of course "loads of parallel delay lines" is topologically exactly the same as a tapped delay line. So whereas my admonition regarded a simple sum of taps, a fancypants feedback matrix must conserve power in the loop somehow!



-Casey

---

### Post #477 -- Page 16
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187133&postcount=477>

Quote: > Originally Posted byCasey➡️Of course "loads of parallel delay lines" is topologically exactly the same as a tapped delay line.Hang on- I'm not sure we're talking about the same thing, which probably means I explained it wrong. Maybe 'parallel' is the wrong word.


What I'm putting global feedback around is a big pile of separate delays each with their own regeneration that is local feedback- they're not sharing a buffer, each has their own buffer. I don't think that will reinforce in quite the same way as multiple taps on the same buffer, though I could be naive about that. I haven't thought much about multiple taps on the same buffer because it just seemed like it would give rise to more regular patterns...


It seems like if you have global feedback around a multitap delay you'd be guaranteed to have some real strong reinforcing peaks in the response? I don't think it would be anything like separate buffers each with local feedback. It seems like if you tried to get the same degree of feedback all globally from the output of a multitap it would just be impossible. (but then I'm not sure how you put in local feedback on a multitap, because I haven't coded any)

---

### Post #478 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187148&postcount=478>

You just need to be clear about what is in the feedback path.


It now sounds like you are saying that the tapped delays are not in the feedback path? This would be a good thing!


What is the source of your "global" feedback, and what does it feed?



-Casey

---

### Post #479 -- Page 16
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187267&postcount=479>

Quote: > Originally Posted byCasey➡️What is the source of your "global" feedback, and what does it feed?It goes allpass- tank (a bunch of delays with local feedback)- then after all that a small amount of the total output is fed back into the input again, in front of the allpass.


So each time through, there's one more allpass, and the same tank over again- it tends to bring out a resonant peak. I'm wondering if it's such a 'no-no' that nobody even does this?


*edit* Did some googling- it is a Schroeder model with global feedback over the entire thing in small amounts. It looks like a Householder arrangement but instead of -2/N combs, it's a very small positive feedback. I'm sorry, I'm posting too long again :(

---

### Post #480 -- Page 16
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187284&postcount=480>

Quote: > Originally Posted bychrisj➡️a small amount of the total output is fed back into the input againIf by "total output" you mean the reverb output, then yes, this is never done and is a big fat no-no given your topology as I understand it.



-Casey


---

## Page 17

---

### Post #481 -- Page 17
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187353&postcount=481>

OK, I just saw your additional note.


I thought you had multi tap delay lines feeding back. If you simply have multiple delays feeding back, then you view the topology as an FDN with a specific feedback matrix. The gains in this matrix must be arranged such that the power within the structure is conserved. (As you have noted!)



-Casey

---

### Post #482 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187378&postcount=482>

Quote: > Originally Posted bychrisj➡️*edit* Did some googling- it is a Schroeder model with global feedback over the entire thing in small amounts. It looks like a Householder arrangement but instead of -2/N combs, it's a very small positive feedback. I'm sorry, I'm posting too long again :(This will blowed up good! Blowed up REAL good! 

[YouTube - SCTV 4 Farm Film Report](https://www.youtube.com/watch?v=_dfoVqhQVyQ&feature=related)


In reverb terms, "blowed up" is used to refer to the instability that happens when you have a feedback gain of greater than 0 dB for some frequency. The amplitude of the output will keep increasing. With fixed point systems that use saturation, you can end up getting a stable oscillation. In floating point systems, it will eventually go outside of the floating point numerical range, and you will get NaNs, which are evil.


Read this whole chapter to learn how to work with feedback around parallel delay lines:

[Time shifts and delays](http://crca.ucsd.edu/%7Emsp/techniques/latest/book-html/node104.html)


Miller Puckette was one of the pioneers of feedback delay networks. Michael Gerzon developed the theory about 13 years before Puckette published his findings, but I don't know how many people actually read Gerzon's papers - they were in a journal that was very rare within the US.

---

### Post #483 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187411&postcount=483>

Quote: > Originally Posted byCasey➡️Hmmm, not sure I see what you mean.An allpass filter does not have a metallic ring, it is allpass. Allpass filters can lead to a metallic sound because of their regular spectral smear. At the same gain, smaller allpass filters will have less spectral smear, and will cause less of a metallic residue in the tail.Allpass is allpass, but this doesn't mean that all of the poles are the same distance from the unit circle. If you have a few poles that are closer to the unit circle than others, it seems like these will ring out longer than the others in the decay. Put feedback around these allpasses, and the poles will get even closer to the unit circle. 


As far as allpass filters not having a metallic ring, try creating an allpass delay nested 10 deep, with all the allpass coefficients at 0.7, and total delay at 20 msec, and run an impulse through it. This is an allpass system, but its decay is perceived as VERY metallic.


We may be arguing about semantics here. You say spectral smear, I say ringing poles. The point is that nested allpass filters are tricky to work with.

---

### Post #484 -- Page 17
**User:** j_j
**Info:** Joined: Jul 2009Posts: 802My Recordings/Credits🎧 15 years | Posts: 802My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187705&postcount=484>

I've had good luck working up a bit of an I/O framework (digital or analog) and then just using a netbook and gcc on linux. You'd be surprised what a dual-core atom will do 


And your hardware is already built.

---

### Post #485 -- Page 17
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5187892&postcount=485>

Quote: > Originally Posted byj_j➡️I've had good luck working up a bit of an I/O framework (digital or analog) and then just using a netbook and gcc on linux. You'd be surprised what a dual-core atom will doAnd your hardware is already built.A netbook is not a 1U high 19" rack like most pieces of outboard gear. I realize that may not be an issue for everybody, but for some people it is. Also, I rather enjoy designing the hardware... bring on the soldering iron.

---

### Post #486 -- Page 17
**User:** j_j
**Info:** Joined: Jul 2009Posts: 802My Recordings/Credits🎧 15 years | Posts: 802My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5188158&postcount=486>

Quote: > Originally Posted bydale116dot7➡️A netbook is not a 1U high 19" rack like most pieces of outboard gear. I realize that may not be an issue for everybody, but for some people it is. Also, I rather enjoy designing the hardware... bring on the soldering iron.Hm.


I could set this on on a 1U rack shelf. 


Seriously, it would work, but if you want to build, that's cool. I'm just tired of DSP's and the notoriously annoying compiler/assemblers that they come with. Been there, done that, and for way, way too (unblievably gross and offensive string of expletives) long.


First DSP I used kinda had a symbolic assembler. 4 tab fields, one for each stage of the pipeline. data moved from right (far tab) to left (near tab) as it got fetched, operated on once, added or not, and hten saved.


Branching was, well, possible.  Barely.

---

### Post #487 -- Page 17
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5188194&postcount=487>

Quote: > Originally Posted byj_j➡️I could set this on on a 1U rack shelf.Seriously, it would work, but if you want to build, that's cool. I'm just tired of DSP's and the notoriously annoying compiler/assemblers that they come with.Actually, an 'industrial' computer - something like a PC104 or something like that - with the same dual-core processor, also running Linux but in a 19" 1U box would be interesting. You could easily do your development on a netbook or whatever, and have two UI front-ends, one for a PC environment, the other for a little LCD and a few rotary encoders. Use a 'flash' hard drive in the 19" box to get rid of moving parts, that might work.


I don't mind working with the DSP56k family even in assembly code, it's relatively easy to write - almost as if I were programming on a PDP11 or 68k or some other CISC microprocessor. VLIW assembly code looks scary to me, though.

---

### Post #488 -- Page 17
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5188532&postcount=488>

Quote: > Originally Posted byseancostello➡️We may be arguing about semantics here. You say spectral smear, I say ringing poles. The point is that nested allpass filters are tricky to work with.Yes you are right, we are talking about the same thing. heh



-Casey

---

### Post #489 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5189024&postcount=489>

Quote: > Originally Posted byj_j➡️I've had good luck working up a bit of an I/O framework (digital or analog) and then just using a netbook and gcc on linux. You'd be surprised what a dual-core atom will doDo tell. What can it do? 


This is an interesting idea, especially if you are running Linux in a rack box (or smaller, if you use a mini-ITX, nano-ITX, or pico-ITX format). I haven't tried an Atom, though, so I don't know how they compare with the standard Core2Duo processors, or whatever they are called for PCs. Does the Atom have SSE instructions?


It probably wouldn't be that useful for stomp pedals, as I presume that an Atom is much less cost effective than something like the FV-1 or a Blackfin. However, I know that you can compile VST plugins for Linux. Hmmm.

---

### Post #490 -- Page 17
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5190894&postcount=490>

Quote: > Originally Posted byseancostello➡️It probably wouldn't be that useful for stomp pedals, as I presume that an Atom is much less cost effective than something like the FV-1 or a Blackfin. However, I know that you can compile VST plugins for Linux. Hmmm.That's almost always the case - for a stompbox, one other biggie is power consumption. A PC chipset of any kind sucks back the juice. It is true that a netbook takes less power from the wall than a 480L or 224, but a reverb based on something like the AL3201 in a stompbox (which will out-compute the 224) can be designed to take maybe 20mA from a battery using a linear regulator (10mA for the 3201, and about the same for the ADC-DAC), and if you spring for the cost of a switching power supply (all of three or four parts) you can get it down to probably about 7mA from a 9V battery - about 80 hours of use. On the other hand, my Aspire One netbook sucks about two amps out of its battery, and would attempt to drain a 9V stompbox battery in about ten minutes - if you could get the current out of a 9V battery fast enough.

---

### Post #491 -- Page 17
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5197583&postcount=491>

Maybe already been discussed:


Is the phaseresponse considered more important then the amplitude response within high order interpolators?



Harrie

---

### Post #492 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5198896&postcount=492>

Quote: > Originally Posted byFroombosch➡️Maybe already been discussed:Is the phaseresponse considered more important then the amplitude response within high order interpolators?Not for reverbs, IMO. Reverbs scramble phase anyway, so the phase response is not that important. The things I consider important are the amplitude response, and the SNR when the delay length changes by more than 1 sample:


- Linear interpolation has poor amplitude response versus frequency, but a nice SNR with wide modulation widths.

- Higher order FIR interpolation schemes have better amplitude responses, but the cost goes up with the order.

- Some allpass interpolation schemes can be very noisy when the modulation width is fairly high, so you have to be careful. This is due to the allpass coefficient getting too close to the unit circle, which results in a transient that takes a while to ring out.

- Using no interpolation results in a perfectly flat amplitude response, but crappy SNR.

- If your modulation is updated at a slower rate, this increases the SNR as well.

---

### Post #493 -- Page 17
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5198950&postcount=493>

I look for opportunities to combine linear interpolation when I have already upsampled significantly for other reasons. Sort of a freebie. heh


In some cases multiple high order interpolations are more expensive than just running your alg at a high sample rate all the time and using linear interpolation, watch for that.



-Casey

---

### Post #494 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5199067&postcount=494>

Quote: > Originally Posted byCasey➡️I look for opportunities to combine linear interpolation when I have already upsampled significantly for other reasons. Sort of a freebie. hehIn some cases multiple high order interpolations are more expensive than just running your alg at a high sample rate all the time and using linear interpolation, watch for that.You mentioned this earlier, but it is worth mentioning again. This has shaped plans of mine for a future algorithm...

---

### Post #495 -- Page 17
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5199609&postcount=495>

Quote: > Originally Posted byseancostello➡️This will blowed up good! Blowed up REAL good!Sure will  thanks, guys- I was able to do some tweaking. With your help I got it to this... I would still like to compare more directly to existing work. This is from Casey's guitar example which I like. Again, are there dry samples I should be using to post with?

---

### Post #496 -- Page 17
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5199754&postcount=496>

Quote: > Originally Posted bychrisj➡️Sure willthanks, guys- I was able to do some tweaking. With your help I got it to this...Very nice Chris. I particularly like the short example. The long example has a bit too much allpass going on though really, just try to settle them down.



-Casey

---

### Post #497 -- Page 17
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5199801&postcount=497>

You mean more in this direction? There's a damping slider, first example was 0.5 and 0.5 dry/wet on both. This one is damping to 1.0.


It's tricky because FarSpace is the one I wanted to be ridiculous infinite-space verb- NearSpace is more contained. I'd like to lean in the direction of the spaciousness and invisibility of your reverbs, and hopefully it's a tip of the hat- even though I'm not using any of your techniques that I know of- intentionally avoided similar verb structures. I'm trying to do my own thing, it just needs to have some similar qualities to the goodness of your verbs

---

### Post #498 -- Page 17
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5201257&postcount=498>

chris, 


I would rather try something different as a source to listen to a laaaaaarge reverb. 



Harrie

---

### Post #499 -- Page 17
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5201281&postcount=499>

I've been working on a revised hardware platform, I had too many blue jumper wires on the previous version, and after too much handling, it's starting to get a bit flakey. Also, a double-sided PC board isn't the best for a 100 MHz data bus - so a 4-layer it is. Along with fixing things that were obvious errors on the previous PC board, I've changed the DSP from a 100 MHz DSP56366 to a 200 MHz dual-core DSP56720. I'm thinking about using SDRAM, however, I'm a bit confused as to the best way to arrange data and move it to/from the SDRAM. It seems to me that SDRAM timing is pretty slow for hopping around in memory. For long delays, it's pretty obvious what to do (put the head and tail in internal SRAM and burst the middle into and out of the SDRAM) but for a high density multitap algorithm, the answer isn't quite so simple. Is this a case where certain algorithms just don't run as efficiently on different hardware? Is it best to try to keep large tap sizes in internal RAM if I can? Would I be better off with an untapped algorithm like an FDN? A single random SDRAM access takes about the same amount of time as almost 20 instructions (per core) - if in internal SRAM, I could do four allpasses (two per core) in the time it takes to just fetch a single sample from the SDRAM.

---

### Post #500 -- Page 17
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5203680&postcount=500>

Quote: > Originally Posted bydale116dot7➡️Is it best to try to keep large tap sizes in internal RAM if I can? Would I be better off with an untapped algorithm like an FDN?Is FDN an untapped algorithm?

---

### Post #501 -- Page 17
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5203770&postcount=501>

Each delay segment has a defined start and stop, without pseudo-randomly spaced taps in the middle like in the loop-style algorithms (Griesinger/Dattorro). The output comes from a summing matrix at the end of the delay lines. In this arrangement, you can easily move the middle section of each delay out into slow RAM, so long as you can write the head and and read the tail efficiently (fast RAM). That should be relatively cheap to do (in processor cycles), should be a relatively easy operation (you can probably program a DMA controller to do the memory moves), and also should handle resizing the delays quite easily. If a delay line is longer than about 100 samples, you can burst the data into and out of the SDRAM, and if it's shorter, you just turn off the SDRAM copy and leave the delay in SRAM.


Alternatively, if all of the audio for a reverb would fit in about 90k of SRAM, it could all sit in SRAM, and the SDRAM would only be used for bulk delays - predelay or slapback echo, that kind of thing. But if you upsample, then the 90k would disappear quickly - that would be under a second of audio at 96k.

---

### Post #502 -- Page 17
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5203820&postcount=502>

Quote: > Originally Posted bydale116dot7➡️Each delay segment has a defined start and stop, without pseudo-randomly spaced taps in the middle like in the loop-style algorithms (Griesinger/Dattorro). The output comes from a summing matrix at the end of the delay lines.You're correct, when we talk about a very basic implementation of FDN.


Btw. With the correct feedback matrix you can create 'loop-style algorithms' in FDN.

---

### Post #503 -- Page 17
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5203891&postcount=503>

Yes, it would be a sparse matrix. It may not be as 'efficient' to do it that way, but I'm looking at the hardware and trying to figure out the most efficient way of doing it - or deciding if I need to rework the processing hardware. The last thing you want to do is have a very beautiful PC board all put together, then find out the algorithms you want to run won't run efficiently on the hardware. An option I was thinking of was to put more than one DSP on there, but for a DIY project, multiprocessing seems a bit overkill.


What I found on the last design was:- The DSP was adequate to do very complex loop-based reverbs
- Long loop times were not accomodated particularly well (special effects and sampling, not reverbs) - and there was a barrier at 256k samples because of the address line arrangement of the DSP56366.
- The SRAM performed adequately but did add a wait state for every access. More on-chip RAM (zero wait state) would be better.
- I did not have digital audio I/O or USB capabilities, and I wanted to add them - espeically the digital I/O.
- The host processor (MCF51AC256) was not really fast enough to do modulation, and the DSP was busy enough processing audio that I didn't want to burden it.
- The I2C interface to the front panel was ok but added too many chips to the front panel PC boards.
- Though the SRAM was nice, it also cost $50 for a measly 512k of it.
- The linear regulators were ugly so I'm moving to a switcher for the main PSU. The PC board now has extra ferrite filters to get rid of the hash, plus separate analogue and digital 3.3V regulators.


So I upgraded the host processor to a MCF52259, ran parallel I/O off of it to the display panel, upgraded the DSP to a DSP56720, added AES digital I/O, a USB connector, and added a ton of SDRAM. The problem with SDRAM is its random access time is sucky, but it's cheap, and it bursts really quickly. Everything else is a significant step upwards, except for memory access time, which is about a factor of 10 worse (for the first access) - then its on-par. I'm just finishing up the PC board in my CAD package now. But I want to make sure that the algorithms can run efficiently before I get the new boards made up. I picked the same families of processors so I can reuse most of the code, and all of the development tools.

---

### Post #504 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5203965&postcount=504>

If you are working with SDRAM, you might want to switch to block-based processing, instead of sample-by-sample. My guess is that the set up and take down time of the SDRAM access is what takes the bulk of the cycles, and that once you have your setup done you can grab a block of samples rather quickly. From reading between the lines of what NS has posted, the PCM96 uses blocks of 32 samples. Back when I worked with ADI, I regularly used blocks of 16 or 32 samples to write reverbs, and it can work very well. You can do allpass loops this way, FDNs, whatever.

---

### Post #505 -- Page 17
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204051&postcount=505>

Quote: > Originally Posted byFroombosch➡️chris,I would rather try something different as a source to listen to a laaaaaarge reverb.HarrieYou mean like this? This is why I was asking if there were dry samples I could use. I feel okay posting it in this thread for feedback, but I don't feel I can show these clips outside the thread because they're Casey's samples.


It's not a huge deal, I do make demos available, but I wish there were great public domain audio clips as good as this.


I think the orchestral sample likes the laaaaaaarge reverb better- and you get more of a sense of the bass of the hall, which is kind of tricky to do without a separate LFE reverb. This is more of what the big one is for.

---

### Post #506 -- Page 17
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204282&postcount=506>

Sounds nice to me. I tend to use snare/ s***** kind of sounds, so I can hear how the tail moves/evolves. In crowded music it is more about the first 200 ms or so. The rest gets masked.

---

### Post #507 -- Page 17
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204292&postcount=507>

Quote: > Originally Posted byseancostello➡️Not for reverbs, IMO. Reverbs scramble phase anyway, so the phase response is not that important. The things I consider important are the amplitude response, and the SNR when the delay length changes by more than 1 sample:- Linear interpolation has poor amplitude response versus frequency, but a nice SNR with wide modulation widths.- Higher order FIR interpolation schemes have better amplitude responses, but the cost goes up with the order.- Some allpass interpolation schemes can be very noisy when the modulation width is fairly high, so you have to be careful. This is due to the allpass coefficient getting too close to the unit circle, which results in a transient that takes a while to ring out.- Using no interpolation results in a perfectly flat amplitude response, but crappy SNR.- If your modulation is updated at a slower rate, this increases the SNR as well.Thank you and Casey for your responces . Food for thought.

---

### Post #508 -- Page 17
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204308&postcount=508>

Quote: > Originally Posted bychrisj➡️because they're Casey's samples.I would have to look back, but I seem to recall that Rob King donated that sample.



-Casey

---

### Post #509 -- Page 17
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204324&postcount=509>

Quote: > Originally Posted byseancostello➡️If you are working with SDRAM, you might want to switch to block-based processing, instead of sample-by-sample.Of course you must still deal with samples on delay line input/output since any reverb would sound quite bad if limited to 16 or 32 sample boundaries.



-Casey

---

### Post #510 -- Page 17
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=5204386&postcount=510>

Quote: > Originally Posted byCasey➡️Of course you must still deal with samples on delay line input/output since any reverb would sound quite bad if limited to 16 or 32 sample boundaries.No problem - just make sure that you adjust your delay lengths to take into account the block delay in the feedback path. For example, if you want a 1000 sample comb filter, and your block size is 32 samples, you would use a delay of (1000-32)=968 samples.

