
---

## Page 23

---

### Post #661 -- Page 23
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6255664&postcount=661>

Mostly I'm just curious to see how they work; I suspect they may use unique (though not necessarily worthwhile) topologies. I'd probably build and enhance the algorithms in PD. I like the Ibanez a lot, but as for the Quadraverb I'm more interested in finding what causes that awful metallic ringing .  I do have other reverbs I'd rather analyze, but these allow enough control over density that it's actually possible.

---

### Post #662 -- Page 23
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6256309&postcount=662>

Quote: > Originally Posted byacreil➡️Mostly I'm just curious to see how they work; I suspect they may use unique (though not necessarily worthwhile) topologies. I'd probably build and enhance the algorithms in PD. I like the Ibanez a lot, but as for the Quadraverb I'm more interested in finding what causes that awful metallic ringing.  I do have other reverbs I'd rather analyze, but these allow enough control over density that it's actually possible.I'd be interested in seeing the topologies, delay settings, that sort of thing. Although if there is nasty ringing, the delay settings are probably far from ideal. Or the allpass coefficients are turned up too high.


From my emails with Keith Barr, I think that the Quadraverb algorithms would be parallel combs with embedded allpasses. Similar to the Quantec algorithm, but less combs, more allpasses. Output taps taken from within the comb - not necessarily from the end of the comb. Barr avoided taking output taps from within an allpass delay, to avoid the metallic sound that can result from that.

---

### Post #663 -- Page 23
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6256717&postcount=663>

Quote: > Originally Posted byseancostello➡️From my emails with Keith Barr, I think that the Quadraverb algorithms would be parallel combs with embedded allpasses. Similar to the Quantec algorithm, but less combs, more allpasses. Output taps taken from within the comb - not necessarily from the end of the comb. Barr avoided taking output taps from within an allpass delay, to avoid the metallic sound that can result from that.That's partly why I'm interested.  I've also somehow developed an allergy to the Quadraverb's gross reverb, so I kind of want to revisit it to see if it's the algorithm's fault or my own clueless misuse at 19-ish.  It's probably both.


Autechre were pretty big Quadraverb offenders too.

[YouTube - Autechre - Yeesland](https://www.youtube.com/watch?v=bPBBi4Vzk4Y&t=210)


There's your "metallic allpass coloration".  You'd think they were messing it up on purpose, but I have the exact same disaster on some of my old recordings.

---

### Post #664 -- Page 23
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6284708&postcount=664>

Quote: > Originally Posted byacreil➡️Quick hypothetical question: if I were to analyze the Alesis Quadraverb and Ibanez SDR-1000 algorithms in moderate  but not exacting detail, would that be of interest here or just a total waste of time?  This would include topology, delay lengths, parameter mappings (i.e. at least as much detail as the Dattorro algorithms) but not an exhaustive examination of loop filters or coefficients at specific decay times, etc.The Ibanez SDR 1000 is identical to the SONY MUR-201 and these share quite a lot of DNA with the famed SONY DRE2000.


I have several SDRs and a DRE2000 and these are capable of some incredibly well articulated reverb sounds.. unlike anything else I've heard (and I've heard / owned then all!)


The basic reverb structure in the MUR/SDR is a true stereo in / out and is based on the same "tapped ring" FDN topology as the Lexicon / Ensoniq / etc... but are constant density, like the AMS and EMT digital reverbs.

---

### Post #665 -- Page 23
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6287437&postcount=665>

That's why I wanted to try it. I'd noticed previously that an impulse into one channel will sort of pan back and forth between the outputs, like a Lexicon algorithm. But as you say it is constant density: with a long decay time and high "size" setting (diffusion), I can put in an impulse, then while it's decaying turn the size down and the tail will have the same low density as it would if the size parameter had been low to start with, indicating that the allpasses come after the main "tank" structure. This makes me think it won't be that difficult to analyze.


It seems like a unique and otherwise unknown topology, not that it's necessarily super useful today. I'd be interested to know how it differs from the DRE2000, also. I've heard (from you, probably) that it's the same basic algorithm, but is it significantly cut down or enhanced?


Obviously this isn't urgent, but I'll do it if I'm ever in the mood to do something that takes much longer than I expect.


Also, I didn't know AMS was constant density, I'm actually a little surprised.  Any more info on that?

---

### Post #666 -- Page 23
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6293126&postcount=666>

The SDR-1000 / MUR-201 differs from the DRE2000 in several important ways.

First of all he DRE2000 is a mono in / stereo out device.  It has 4 reverb algos and 2 delay and 2 Echo (with feedback) algos.


The DRE2000 reverb algos have no size or diffusion parameter, just HP, LP (4 choices of each), High and Low Rt multiplication (fixed frequency), decay time (0-9.9s) and two dry delays feeding the L and R outputs (except in the "A reverb" algo where the first delay is sent to the outputs centered and dry and the second feeds the input to the reverb and is called "sub reverb")


The 4 reverb algos vary in density (A is the loosest, D is very very fine grained..)

---

### Post #667 -- Page 23
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6293129&postcount=667>

See this post for more info:
[https://gearspace.com/board/4864692-post421.html](https://gearspace.com/board/4864692-post421.html)

![](https://gearspace.com/board/attachments/geekslutz-forum/147392d1260245146-reverb-subculture-cz-sony-dre-2000-0.1s-decay.jpg)

---

### Post #668 -- Page 23
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6300278&postcount=668>

Well it seems different enough that I shouldn't worry about emulating both at once, but it's nice to see what the algorithm descended from.

---

### Post #669 -- Page 23
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6368898&postcount=669>

I'm finding I'm able to get more soundstage depth by doing a thing sort of like companding- applying a saturation effect, doing the reverb and then trying to apply the inverse of the saturation effect again. On an actual sound, it goes thin and nasty, but does drop back in the sound picture. Applied to the reverb output it seems interesting 


mp3 versions and other links in this post- [https://gearspace.com/board/6368824-post85.html](https://gearspace.com/board/6368824-post85.html)

---

### Post #670 -- Page 23
**User:** theBackwardsman
**Info:** Joined: Feb 2007Posts: 741🎧 15 years | Posts: 741
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6410652&postcount=670>

Quote: > Originally Posted byzmix➡️Below I have provided a screen shot showing the output each of the 4 reverb algorhythms of my 1980s era SONY DRE-2000, fed by a single sample impulse and with the decay adjusted to 0.1s (minimum is 0.0s but that produces no output..). Note how diffuse algos B, C and D are..!EDIT: The file lengths pictured below are exactly 233ms from beginning to end.You wouldnt mind sharing the impulses?

---

### Post #671 -- Page 23
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=6456184&postcount=671>

Quote: > Originally Posted byacreil➡️Also, I didn't know AMS was constant density, I'm actually a little surprised.  Any more info on that?Maybe Warp69 should chime in

---

### Post #672 -- Page 23
**User:** FETHead
**Info:** Joined: Oct 2008Posts: 26🎧 15 years | Posts: 26
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=7173281&postcount=672>

This thread is way better than any technical reverb paper that I've ever read. You guys rock! 

In anyway - there is at least one Sony reverb algorithm that is at least partly laid out - and it's not in a reverb box - but in the Sony D7 delay - here is one of the pathes called Zoomverb:


Pre-Delay 1: CH1 41.44  CH2 52.25     100%

Pre-Delay 2: CH1 75.52  CH2 80.50     72.95%

Early Refl  1: CH1 24.02  CH2 27.67     50%

Early Refl  2: CH1 29.31  CH2 33.69     -50%

Early Refl  3: CH1 37.33  CH2 40.06     50%

Cross PreD : CH1 94.75  CH2 99.46     40.96%

Tap         1: CH1 0.208  CH2 3.021     97.67%

Tap         2: CH1 91.19  CH2 104.19    -73.24%

Tap         3: CH1 201.25 CH2 195.77   48.82%

Cross Tap 1: CH1 31.29  CH2 41.48     90.33%

Cross Tap 2: CH1 131.31 CH2 122.96   -47.36%

Cross Tap 3: CH1 229.85 CH2 241.19   29.44% 

Fdbk Time  : CH1 292.17  CH2 309.92  25% 

Cross Fdbk Time: CH1 317.85 CH2 342.50 10.84%

Fdbk Treble Shelf 6.3kHz -3dB


Overall EQ: LowShelf 250Hz -2.7dB ; Peak 1.25kHz +4.2dB  BW1.414


No time modulation is supported by the D7 btw.


I could take an IR  sometime if somebody is interisted. By the above - it's easy to realise that it is a true stereo verb - what makes it unique to me - is all the "Cross" delays as well as the feedback delay...


On a completely random note: does anybody have an example (or paper)

of the Gerzon vector allpass stucture/matrix?

---

### Post #673 -- Page 23
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8232001&postcount=673>

Quote: > Originally Posted byacreil➡️Here's the guitar example from a few pages back.I hate to bump an old thread but I just wracked my brain reading this entire thread post by post in search of the dry sample of this guitar and for the life of me I can't find it in this thread.  And I also have a huge headache now and my eyes feel crossed!


Can someone point me to the post where this dry sample is?  I want to test some of my reverb settings against examples in this thread.


Thanks,

Frank

---

### Post #674 -- Page 23
**User:** nickelironsteel
**Info:** Joined: Jul 2012Posts: 2,652🎧 10 years | Posts: 2,652
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8232840&postcount=674>

Quote: > Originally Posted bytheBackwardsman➡️You wouldnt mind sharing the impulses?no dice, they dont work, been there done that

---

### Post #675 -- Page 23
**User:** Melvin III
**Info:** Joined: Jan 2012Posts: 856My Studio🎧 10 years | Posts: 856My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8232864&postcount=675>

Wow its amazing I'm just now finding this thread after searching for something like this

---

### Post #676 -- Page 23
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8240659&postcount=676>

BUMP looking for the dry guitar sample. 


Thanks,

Frank

---

### Post #677 -- Page 23
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8247571&postcount=677>

Quote: > Originally Posted byionian➡️BUMP looking for the dry guitar sample.Thanks,FrankHere it is.

---

### Post #678 -- Page 23
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8247621&postcount=678>

Quote: > Originally Posted byacreil➡️Here it is.Thank you!  Very much appreciated!


Regards,

Frank

---

### Post #679 -- Page 23
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8247644&postcount=679>

I'm not sure how this ties into everything but I found this interesting none the less... Here's a letter from David Griesinger to Jon Dattoro (He created the algorithms for the Lexicon 2400 and later went to Esoniq where he wrote algorithms for the DP4) regarding the algorithms in the 224.

![](https://static.gearspace.com/util/imgext.php?u=http%3A%2F%2Fi109.photobucket.com%2Falbums%2Fn48%2Fionian2006%2FGriesingersm.jpg&h=3a8ab24bc40e63d2ef840081746328c3)



Here's the link for the full size scan of the letter (too big to post here directly)
[https://ccrma.stanford.edu/~dattorro/Griesinger.jpg](https://ccrma.stanford.edu/~dattorro/Griesinger.jpg)


Jon Dattoro's website, where I found the letter, as well as some other interesting things such as some of his AES papers:
[https://ccrma.stanford.edu/~dattorro/](https://ccrma.stanford.edu/~dattorro/)


Regards,

Frank

---

### Post #681 -- Page 23
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8422317&postcount=681>

Great.


A new photo of "reverberators"....... Although clean shaved.

---

### Post #682 -- Page 23
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8424408&postcount=682>

Quote: > Originally Posted byWarp69➡️Great.A new photo of "reverberators"....... Although clean shaved.You could draw beards in if you like.

---

### Post #683 -- Page 23
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8476739&postcount=683>

Quote: > Originally Posted byCasey➡️Attachment 316196A little waltzing bird told me that Michael is no longer to blame (i.e.working at) Lexicon...

---

### Post #684 -- Page 23
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8480068&postcount=684>

Quote: > Originally Posted byzmix➡️A little waltzing bird told me that Michael is no longer to blame (i.e.working at) Lexicon...No secret there.  Gone almost a year.

---

### Post #685 -- Page 23
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8480074&postcount=685>

Quote: > Originally Posted byDeleted Nobody Special ➡️No secret there.  Gone almost a year.News travels fast...erm..

---

### Post #686 -- Page 23
**User:** apprenticemart2
**Info:** Joined: Feb 2012Posts: 717🎧 10 years | Posts: 717
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8480620&postcount=686>

Quote: > Originally Posted byzmix➡️News travels fast...erm..This kind of news tends to reverberate......

---

### Post #687 -- Page 23
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8481285&postcount=687>

There's another blurb about the Dattorro/Griesinger thing in Barry Blesser's book *Spaces Speak, Are You Listening?*, from Chapter 6.

Quote: > To appreciate the influence of social context on reverberator design, consider the story of one particular design from the late 1980s, which originated as the flagship product of a world-renowned company specializing in reverberator technology. A start-up competitor, after failing to achieve a design of comparable quality, spent many months reverse engineering that product, legal, but perhaps unethical. In those days, with discrete electronics, reverse engineering was tractable. Shortly thereafter, the start-up company failed, but its reverberator design began to float around the industry. Even though details were still treated as a trade secret, the design eventually appeared in two articles (Gardner, 1998; Dattorro, 1997a). It was an old design, long obsolete in terms of acoustic quality, but it is still unique in that both the topology and a good set of working parameters are widely available.The Gardner citation is the "Reverberation Algorithms" chapter from the book *Applications of Digital Signal Processing to Audio and Acoustics*. The independently discovered algorithms that Griesinger mentions in his letter are also in Gardner's 1992 Master's thesis (The Virtual Acoustic Room) and article "A Realtime Multichannel Room Simulator". They include nested allpass filters, like the other Griesinger/Dattorro algorithm: [Dattorro Convex Optimization of a Reverberator - Wikimization](http://www.convexoptimization.com/wikimization/index.php/Dattorro_Convex_Optimization_of_a_Reverberator)


I don't even remember how much of this has already been covered in this thread. It's probably scattered over multiple pages, so I don't see the harm in rehashing.

---

### Post #688 -- Page 23
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8482494&postcount=688>

Quote: > Originally Posted byacreil➡️There's another blurb about the Dattorro/Griesinger thing in Barry Blesser's bookSpaces Speak, Are You Listening?, from Chapter 6.The Gardner citation is the "Reverberation Algorithms" chapter from the bookApplications of Digital Signal Processing to Audio and Acoustics. The independently discovered algorithms that Griesinger mentions in his letter are also in Gardner's 1992 Master's thesis (The Virtual Acoustic Room) and article "A Realtime Multichannel Room Simulator". They include nested allpass filters, like the other Griesinger/Dattorro algorithm:Dattorro Convex Optimization of a Reverberator - WikimizationI wonder if the Gardner stuff was truly "independently discovered." The Large Room (or whatever the biggest algorithm) in Gardner's thesis/article looks a lot like 1/2 of the Lexicon Concert Hall in the Convex Optimization algorithm. A bit more evidence that Gardner may have learned about the Lexicon architecture before writing his papers:


- One of the algorithms in Gardner's Reverb program for the AudioMedia cards is a "Stereo Hall," which consists of 2 nested allpass loop reverbs that are cross-coupled, similar to the Convex Optimization drawing. The algorithm isn't as complex as the Lexicon original, but odds are good that the cycles were limited on the AudioMedia cards.

- Gardner has the following paragraph in his article that is not in his thesis:

Quote: > It should be mentioned that these reverberator structures are not new, although there has been little written about them in the literature. The author’s first exposure to them occurred years ago when working in the electronic musical instrument industry. Without a doubt, there are many wonderful sounding commercially available reverberators, all based upon various efficient algorithms. It is unfortunate that the necessities of industrial competition have prevented the open discussion of such algorithms, because they are truly fascinating.My guess is that the Lexicon stuff has been reverse engineered on multiple occasions throughout the last 30+ years. Keith Barr mentioned that he figured out how to embed allpass delays within larger loops while messing with the controls of a 224 and watching how the impulse response changed.

---

### Post #689 -- Page 23
**User:** chet.d
**Info:** Joined: Oct 2007Posts: 2,254🎧 15 years | Posts: 2,254
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8489392&postcount=689>

I'm wondering about the different ursa major versions.


I've only heard about the stargate, and read your blog Sean where Chris Chimed in about it's tremolo type modulation. Curious.


I know little about the 8x32 and space station though.

Then there's the later sst-206 aes ver...


Appreciate any insights!

---

### Post #690 -- Page 23
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8489445&postcount=690>

Quote: > Originally Posted byseancostello➡️...Keith Barr mentioned that he figured out how to embed allpass delays within larger loops while messing with the controls of a 224 and watching how the impulse response changed.What would he have noticed?  Perhaps that the impulse became more diffuse as he increased the decay time? That would have been true of any reverb with allpass filters in the "tank".. but how would he have determined the presence of nested allpass filters?


---

## Page 24

---

### Post #691 -- Page 24
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8489726&postcount=691>

Quote: > Originally Posted byzmix➡️What would he have noticed?  Perhaps that the impulse became more diffuse as he increased the decay time? That would have been true of any reverb with allpass filters in the "tank".. but how would he have determined the presence of nested allpass filters?Barr probably DIDN'T determine that there were nested allpasses in the tank (i.e. allpasses inside of allpasses, embedded within a larger delay loop). The Alesis algorithms all seem to be single allpasses or series allpasses embedded within a loop, with 2AP+1 delay being a favorite structure of Keith's.

---

### Post #692 -- Page 24
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8489777&postcount=692>

Quote: > Originally Posted byseancostello➡️Barr probably DIDN'T determine that there were nested allpasses in the tank (i.e. allpasses inside of allpasses, embedded within a larger delay loop). The Alesis algorithms all seem to be single allpasses or series allpasses embedded within a loop, with 2AP+1 delay being a favorite structure of Keith's.Then why would he make such a claim?

---

### Post #693 -- Page 24
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8492902&postcount=693>

Quote: > Originally Posted byzmix➡️Then why would he make such a claim?He didn't. He just figured out the trick of embedding allpass delays inside of a larger loop. His quote:

Quote: > As for history, I once watched the impulse response of a 224 on a scope, moved a few sliders and realized what they were doing.

---

### Post #694 -- Page 24
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8492925&postcount=694>

Quote: > Originally Posted byseancostello➡️He didn't. He just figured out the trick of embedding allpass delays inside of a larger loop. His quote:"As for history, I once watched the impulse response of a 224 on a scope, moved a few sliders and realized what they were doing. "Sorry, (doh..!) That's more like it.  Pretty simple stuff to observe.  I misread your original statement and and instead of reading *embeded* was specifically wondering how he'd discern the presence of *nested* allpass in a loop..


loops..!

Quote: > Keith Barr mentioned that he figured out how to embed allpass delays within larger loops while messing with the controls of a 224 and watching how the impulse response changed.seancostello

---

### Post #695 -- Page 24
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8495279&postcount=695>

Quote: > Originally Posted bychet.d➡️I'm wondering about the different ursa major versions.I've only heard about the stargate, and read your blog Sean where Chris Chimed in about it's tremolo type modulation. Curious.The Stargate seems to fade out a delay line tap, move it to a different location, and fade it back in. The taps are all mixed and fed back to the input. I think the tap movements are periodic. It wouldn't be hard to get better results with more taps, controlled by some random process, but there's a limit to to the quality that you can get out of that sort of thing. It's inherently unstable, so you're trading off between a metallic howling feedback sound and an overly-modulated weird dissonant sound. If you want randomized reverb that's actually stable, there are better ways to do it. I've recently been working on ways to smoothly and stably move allpass or comb filters between discontinuous delay lengths, randomly couple different delays together, etc...

Quote: > I know little about the 8x32 and space station though.The 8x32 appears to be very similar to the J. A. Moorer "About This Reverberation Business" algorithm. Read the service manual. It would be easy to analyze if you had one to play with, but I don't really think it's worth bothering.


And the Space Station is more or less described in detail in two patents (4268717, 4303991) and the service manual. The delay times given in the patents may or may not correspond to the actual Space Station, but it's not hard to get a useful result by simply hand-tuning it. The patents don't describe the different "room" types either. Again the design is fundamentally pretty limited.


I'm more curious about the AKG ADR68K...

---

### Post #696 -- Page 24
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8497329&postcount=696>

The AKG ADR68K is based on the Lexicon design.

---

### Post #697 -- Page 24
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8497479&postcount=697>

Quote: > Originally Posted byWarp69➡️The AKG ADR68K is based on the Lexicon design.Although I never had a chance to play with that box, I believe it's built on the old Concert Hall.  It's not widely known, but in the very early '90s, Barry Blesser headed up a project at AKG (pre Harman), building a RAM-based audio editor for radio spots.  I've never asked Barry if his work with AKG predated that, but it *is* interesting.

---

### Post #698 -- Page 24
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8499571&postcount=698>

Quote: > Originally Posted byDeleted Nobody Special ➡️Although I never had a chance to play with that box, I believe it's built on the old Concert Hall.  It's not widely known, but in the very early '90s, Barry Blesser headed up a project at AKG (pre Harman), building a RAM-based audio editor for radio spots.  I've never asked Barry if his work with AKG predated that, but itisinteresting.Interesting. IIRC, Chris Moore designed some reverbs for Kurzweil as well. I also recall reading that Bill Gardner worked at Kurzweil at some point. Going back to Gardner's quote:

Quote: > It should be mentioned that these reverberator structures are not new, although there has been little written about them in the literature. The author’s first exposure to them occurred years ago when working in the electronic musical instrument industry. Without a doubt, there are many wonderful sounding commercially available reverberators, all based upon various efficient algorithms. It is unfortunate that the necessities of industrial competition have prevented the open discussion of such algorithms, because they are truly fascinating.If Chris Moore had figured out the 224-style reverbs for the AKG reverb, then it is possible that he introduced these structures to Kurzweil. I guess someone could ask him about this.

---

### Post #699 -- Page 24
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8500154&postcount=699>

Quote: > Originally Posted byseancostello➡️I also recall reading that Bill Gardner worked at Kurzweil at some pointBill also spent some time in the Lexicon building many years ago.  I don't remember him being an actual employee.  I think Dave G served as an advisor when Bill was going for his PhD.  I wasn't real clear on the details then and I'm afraid I'm less clear now.  But there was a period of several weeks when Bill was a regular sight around the place.

---

### Post #700 -- Page 24
**User:** chet.d
**Info:** Joined: Oct 2007Posts: 2,254🎧 15 years | Posts: 2,254
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8500231&postcount=700>

Interesting stuff. 

Who worked where when, algorithm recycling and industries protecting commerce.


Seeking a not so secret weapon box of richness, depth & lowish noise is tricky business.


Had my eye on the ursa's, master rooms, akg's, even curious about the yamaha rev1 ?


The potential for tricky repairs is a concern with all though unless you're fortunate enough to have an M7 in your budget.


I may reach out to Chris Moore re; his thoughts on the akg & kurzwell's.


Very cool & refreshing thread here.

---

### Post #701 -- Page 24
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8500962&postcount=701>

Quote: > Originally Posted bychet.d➡️Had my eye on the ursa's, master rooms, akg's, even curious about the yamaha rev1 ?Funny, I was just checking out the REV1 since I saw one on ebay.


Came across some neat reverb porn: [Yamaha REV1](https://picasaweb.google.com/111376222148597847123/YamahaRev1)


There seem to be 4 custom DSPs (YM5210, 48 pins, white CERDIP) total spread across 2 boards (APF and COM, hmm I wonder what those stand for...). Each have their own control store (MB8128, 2k x8) and RAM (3 have 64k x16 DRAM, one on the APF board has 16k x16 SRAM). Total audio memory is 208kwords. At a sample rate of 44.1 kHz, the total delay time is 4.83 seconds. Other ASICs are YM3541 (64 pins, 3 on the APF board, 2 on the COM board, 1 on the CPU board), and YM5211 (40 pins, white CERDIP, 1 on the CPU board). The CPU is a Z80. DACs and ADC are PCM53.


I think the early reflections (80 taps, 370 ms max) and pre-delay (2 separate delays, 600 ms each) account for one of the DSPs (since the total delay more or less fills one 64k RAM bank). So I might guess that each DSP can do about 80 instructions per sample. That leaves 240 instructions and 3.34 seconds of delay memory for the "tank".


For being made around 1984, it appears that Yamaha had everyone else outgunned, at least for a little while.


I'd be interested to see if any of these chips (perhaps a single YM5210) were used in the low end R1000 from around the same time.

---

### Post #702 -- Page 24
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8501429&postcount=702>

I had a nice visit today with Chris Moore. I asked him about the ADR-68k. He is very happy that so many folks are still interested in the older reverbs and the stories behind them.


The ADR originally stood for Aurora Digital Reverb. It was prototyped and demonstrated under the Ursa Major Brand for around three months.


At this time Chris had hired Barry Blesser as a consultant to run the strategy and human relations aspect of the company. I'm sure he must have added some technical asides, but this was not his main role.


He mentioned the other folks at Ursa at the time, Jeff Stanton, Charles Anderson and Mark Bruckner.


It was Jeff Stanton that did most of the work with a rented 224 and a logic analyzer, reverse engineering the concert hall algorithm. The results of this work went into the ADR-68K, along with other original work.


Chris had done some consulting with AKG earlier in his career. When money became very tight for Ursa Major, Chris travelled to Vienna. He ultimately sold Ursa Major to AKG. Now ADR stood for "All Digital Reverb" renaming it from the less gaudy "Aurora..."



-Casey

---

### Post #703 -- Page 24
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8505200&postcount=703>

Quote: > Originally Posted byCasey➡️I had a nice visit today with Chris Moore. I asked him about the ADR-68k. He is very happy that so many folks are still interested in the older reverbs and the stories behind them.The ADR originally stood for Aurora Digital Reverb. It was prototyped and demonstrated under the Ursa Major Brand for around three months.At this time Chris had hired Barry Blesser as a consultant to run the strategy and human relations aspect of the company. I'm sure he must have added some technical asides, but this was not his main role.He mentioned the other folks at Ursa at the time, Jeff Stanton, Charles Anderson and Mark Bruckner.It was Jeff Stanton that did most of the work with a rented 224 and a logic analyzer, reverse engineering the concert hall algorithm. The results of this work went into the ADR-68K, along with other original work.Chris had done some consulting with AKG earlier in his career. When money became very tight for Ursa Major, Chris travelled to Vienna. He ultimately sold Ursa Major to AKG. Now ADR stood for "All Digital Reverb" renaming it from the less gaudy "Aurora..."-CaseyThanks for the info, Casey! I love hearing about this sort of history.

---

### Post #704 -- Page 24
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8506748&postcount=704>

Thank you for the info, Casey - very appreciated.

---

### Post #705 -- Page 24
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8508794&postcount=705>

Quote: > Originally Posted byCasey➡️It was Jeff Stanton that did most of the work with a rented 224 and a logic analyzer, reverse engineering the concert hall algorithm.This is hilarious.  The Concert Hall algorithm that I put into some of the later Lex verbs came directly from Barry.  Barry probably just used Jeff's work as a basis, which of course came (with great labor on Jeff's part) from Dave's original box.  By the time it came to me, the original Lex sources were gone (at least as far as Dave was telling).


I can't help but think of the 'telephone' game where a phrase is whispered around a campfire to see how it mutates when it gets back to the original speaker.

---

### Post #706 -- Page 24
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8509369&postcount=706>

Someone else will need to complete this circle. I can add that when I last spoke with David on this topic, he predicted that the UAD knockoff would not get the chorusing right.


I a/b'd the 224 and UAD and David was spot on. This might have gone unoticed were it not for the fact that the chorusing of the 224 concert hall alg is arguably its most profound feature. 



-Casey

---

### Post #707 -- Page 24
**User:** Froombosch
**Info:** Joined: Jun 2004Posts: 1,190🎧 20 years | Posts: 1,190
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8509927&postcount=707>

Did he use the difficult way of producing chorus like he did in the 250?

---

### Post #708 -- Page 24
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8509972&postcount=708>

Quote: > Originally Posted byCasey➡️Someone else will need to complete this circle. I can add that when I last spoke with David on this topic, he predicted that the UAD knockoff would not get the chorusing right.I a/b'd the 224 and UAD and David was spot on. This might have gone unoticed were it not for the fact that the chorusing of the 224 concert hall alg is arguably its most profound feature.There're other differences between the 224 (my unit) and the UAD version besides the modulation.


The newer Lexicon models could change the algorithms betweeen OS versions - maybe this is the reason?

---

### Post #709 -- Page 24
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8524528&postcount=709>

Quote: > Originally Posted byseancostello➡️If Chris Moore had figured out the 224-style reverbs for the AKG reverb, then it is possible that he introduced these structures to Kurzweil. I guess someone could ask him about this.I visited with Chris this afternoon. He mentioned that he simply introduced the concepts and issues of FDN structures to Kurzweil. They then ran with it themselves. No 224 DNA was transmitted.



-Casey

---

### Post #710 -- Page 24
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8524750&postcount=710>

Quote: > Originally Posted byWarp69➡️There're other differences between the 224 (my unit) and the UAD version besides the modulation.The newer Lexicon models could change the algorithms betweeen OS versions - maybe this is the reason?What rev is the software in your 224?

---

### Post #711 -- Page 24
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8525683&postcount=711>

Quote: > Originally Posted byCasey➡️I visited with Chris this afternoon. He mentioned that he simply introduced the concepts and issues of FDN structures to Kurzweil. They then ran with it themselves. No 224 DNA was transmitted.Interesting, on a lot of levels. 


My copies of the Gerzon 1971 and 1972 papers were originally from Chris Moore. I didn't get them from him, but when I finally found someone with scans of the papers, they had "LIBRARY OF CHRISTOPHER MOORE - PLEASE RETURN" stamped on them. His annotations are an amazing illustration of the "aha!" moment when he "got" feedback delay networks, and cascaded unitary systems in general.


The Chris Moore reverb architectures I am aware of aren't cascaded unitary structures. The SST and Stargate are both multitap delay lines, with time variation of the feedback taps to allow for higher feedback gains before things go horribly unstable. The 8x32 is a multitap delay line feeding a Schroeder-style reverb, with lots of output taps. These are some pretty interesting structures by themselves, but if you then add FDNs, and Moore's understanding of the 224 algorithms, you've got a pretty amazing breadth of knowledge about reverb structures. 


This thread always makes me feel like a kid getting to eat Thanksgiving dinner at the grownup table for the first time.

---

### Post #712 -- Page 24
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8525821&postcount=712>

Quote: > Originally Posted byzmix➡️What rev is the software in your 224?It's version 4.3.


Most (every?) coefficients are very different if I compare the 4.3 to the UAD version.

[http://www.relab.dk/downloads/sound/UAD224.wav](http://www.relab.dk/downloads/sound/UAD224.wav)
[http://www.relab.dk/downloads/sound/LEX224.wav](http://www.relab.dk/downloads/sound/LEX224.wav)


The frequency response is also different - particular the low end.

[http://www.relab.dk/downloads/sound/UAD224_2.wav](http://www.relab.dk/downloads/sound/UAD224_2.wav)
[http://www.relab.dk/downloads/sound/LEX224_2.wav](http://www.relab.dk/downloads/sound/LEX224_2.wav)


Maybe it's a question about optimization? Or my unit is just different.

---

### Post #713 -- Page 24
**User:** saran42yu
**Info:** Joined: Oct 2012Posts: 25🎧 10 years | Posts: 25
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8525966&postcount=713>

DSP

---

### Post #714 -- Page 24
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8526504&postcount=714>

Quote: > Originally Posted byWarp69➡️It's version 4.3.Most (every?) coefficients are very different if I compare the 4.3 to the UAD version. The frequency response is also different - particular the low end.Maybe it's a question about optimization? Or my unit is just different.By  rev 4.3 the algos were final versions.


Perhaps you're hearing a difference because levels are not matched between your examples. The low end does sound thin in your 224,  so perhaps your analog board needs to me re-capped?  I've been able to null my 224 against the UAD (with Mode Enhancement and Decay Optimization set to off), on all of the algos.

---

### Post #715 -- Page 24
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8526537&postcount=715>

Quote: > Originally Posted byseancostello➡️Interesting, on a lot of levels.My copies of the Gerzon 1971 and 1972 papers were originally from Chris Moore. I didn't get them from him, but when I finally found someone with scans of the papers, they had "LIBRARY OF CHRISTOPHER MOORE - PLEASE RETURN" stamped on them. His annotations are an amazing illustration of the "aha!" moment when he "got" feedback delay networks, and cascaded unitary systems in general.The Chris Moore reverb architectures I am aware of aren't cascaded unitary structures. The SST and Stargate are both multitap delay lines, with time variation of the feedback taps to allow for higher feedback gains before things go horribly unstable. The 8x32 is a multitap delay line feeding a Schroeder-style reverb, with lots of output taps. These are some pretty interesting structures by themselves, but if you then add FDNs, and Moore's understanding of the 224 algorithms, you've got a pretty amazing breadth of knowledge about reverb structures.This thread always makes me feel like a kid getting to eat Thanksgiving dinner at the grownup table for the first time.Wow, that's a bit of history.. got scans of those docs?


The SST 282 Space Station and 323 / 626 Stargate topology are similar, they both have a mono FDN feeding a stationary multitap delay, which gives them a strange "pseudo-stereo" character. The feedback is prior to the output multitap matrix, and these output taps are not modulated.  The Stargate allows adjustment of the output taps proportionally ("size" ) and the Space station has preset tap spacings ("audition delay programs"). On the SST-282 each pair of output taps has it's own analog level control.

---

### Post #716 -- Page 24
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8526872&postcount=716>

Quote: > Originally Posted byzmix➡️Perhaps you're hearing a difference because levels are not matched between your examples. The low end does sound thin in your 224,  so perhaps your analog board needs to me re-capped?  I've been able to null my 224 against the UAD (with Mode Enhancement and Decay Optimization set to off), on all of the algos.


Hearing things? 


The level differences between the files are 0.06dB (RMS).


Anyway - there's clearly a difference between the UAD version and my V4.3. As posted before - every single coefficient is different between them - from delay lines values and feedback values to modulation.


Can you actually null your unit with the UAD version? That would indicate your unit sound like the UAD version - listen from 0:40 in the second test - is the UAD just like your unit in that regard?. Even the UA promotion videos show differences compare to the original. Which version did the UA video use?


First test is Program 1 and the second test is Program 3 - exact same settings on the UAD and the hardware.


Very interesting - I was completely unaware that OS versions could be that different.

---

### Post #717 -- Page 24
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8529423&postcount=717>

I have moved the hardware convolution discussion to this thread.

Quote: > Originally Posted byCasey➡️The Sony performs the convolution in the time domain. The plugins do it in the frequency domain.In theory these should be the same. In reality the Sony just sounds better. I saw where the Eastwest Spaces software used the Sony 777 for the IR capture of the IRs they sell. (It's also hard to miss the similarity of their GUI to the 777 as well.)I contacted the Eastwest guy that is here on GS and asked him about their software. He told me they use full double precision floats for their processing. I had thought that maybe a lack of precision was an issue.I would love if Eastwest could discuss this in the Reverb Subculture thread and perhaps post some A/Bs between what they captured on the Sony and what is played out of their convolution software.I am certainly willing to believe that the software can sound as good as the Sony 777 but have not heard that yet.-CaseyThis is a fast test - the exact same IR used on : 


Sony S777 24bit

Matlab for direct convolution (using the conv(x, y) command) 32bit(+)

Matlab for FFT (using the ifft(fft(x) .* fft(y)) command) 32bit(+)

Reverberate LE (using FFT Over Lap and Add - Intel) 32bit


Sony S777 : [http://www.relab.dk/downloads/sound/...ution/S777.wav](http://www.relab.dk/downloads/sound/convolution/S777.wav)

Matlab (Direct) : [http://www.relab.dk/downloads/sound/...ion/Matlab.wav](http://www.relab.dk/downloads/sound/convolution/Matlab.wav)

Matlab (FFT) : [http://www.relab.dk/downloads/sound/.../MatlabFFT.wav](http://www.relab.dk/downloads/sound/convolution/MatlabFFT.wav)

Reverberate LE : [http://www.relab.dk/downloads/sound/...erberateLE.wav](http://www.relab.dk/downloads/sound/convolution/ReverberateLE.wav)

---

### Post #718 -- Page 24
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8535792&postcount=718>

Quote: > Originally Posted byCasey➡️There were some interesting discussions earlier this week involving thoughts on pitch changes occurring within real life indoor venues.I had for many years assumed that folks knew that the whole discussion of pitch changes actually occurring in real spaces was just marketing spin designed to cover the need for modulation in artificial reverb.I was surprised to find that this assumption is not universally accepted to say the least. What is your take? Can we agree to debunk this myth?Bumping this due to a thought I just had:


Has anyone done any measurements in a concert hall to quantify (and maybe describe) the amount of sonic motion that occurs for steady state signals, if any?


The experiment could be simple: Set up a speaker on stage. Play a sine wave through it. At the back of the hall, set up a microphone or two. Record the signal.


If the hall is completely LTI, the sine wave should sound like a steady state sine wave at the back of the hall. If there is some sort of time invariance going on, it will manifest itself as time varying fluctuations in the amplitude of the sine wave. By playing back steady state sine waves at different frequencies, you could learn some interesting stuff. 


I'm not arguing that any observed variations would be due to pitch shifting, just that the above experiment could be used to show if there is a measurable amount of time variation in a hall.


Another experiment: Take several impulse responses over several minutes, using an identical signal for the impulse. Compute the cross-correlation of the impulse responses.

---

### Post #719 -- Page 24
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8535806&postcount=719>

Quote: > Originally Posted byseancostello➡️Bumping this due to a thought I just had:Has anyone done any measurements in a concert hall to quantify (and maybe describe) the amount of sonic motion that occurs for steady state signals, if any?The experiment could be simple: Set up a speaker on stage. Play a sine wave through it. At the back of the hall, set up a microphone or two. Record the signal.If the hall is completely LTI, the sine wave should sound like a steady state sine wave at the back of the hall. If there is some sort of time invariance going on, it will manifest itself as time varying fluctuations in the amplitude of the sine wave. By playing back steady state sine waves at different frequencies, you could learn some interesting stuff.I'm not arguing that any observed variations would be due to pitch shifting, just that the above experiment could be used to show if there is a measurable amount of time variation in a hall.Another experiment: Take several impulse responses over several minutes, using an identical signal for the impulse. Compute the cross-correlation of the impulse responses.I'm not sure that an impulse would tell you anything, Sean.  An impulse assumes an LTI system, and we're trying to prove it is -not- LTI, correct? 


I have only read Barry Blesser's AES paper where he talks about modulations

due to temperature fluxuation.   It's pretty obvious that the wind causes changes in the perceived point of origin when listening to a large PA system at an outdoor venue.

---

### Post #720 -- Page 24
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8535815&postcount=720>

Quote: > Originally Posted byseancostello➡️The experiment could be simple: Set up a speaker on stage. Play a sine wave through it. At the back of the hall, set up a microphone or two.Sean, this would be a very cool dream. Unfortunatly, it could never happen. There is no way that pitch can be affected in a natural space.


Please do the science and agree that pitch cannot be affected by any naturally occuring acuostic space.


This is an untruth propogated by David Griesinger and amplified by Lexicon.


Time of arrival may change, but pitch cannot be affected.


Thiis myth needs to be put to bed for good.



-Casey


---

## Page 25

---

### Post #721 -- Page 25
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8535835&postcount=721>

Quote: > Originally Posted byseancostello➡️I'm not arguing that any observed variations would be due to pitch shifting, just that the above experiment could be used to show if there is a measurable amount of time variation in a hall.Of course there is time variation in a hall. But the time of arrival, while it may vary, is never pitch shifted.



-Casey

---

### Post #722 -- Page 25
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8535906&postcount=722>

Quote: > Originally Posted byCasey➡️Sean, this would be a very cool dream. Unfortunatly, it could never happen. There is no way that pitch can be affected in a natural space.Please do the science and agree that pitch cannot be affected by any naturally occuring acuostic space.This is an untruth propogated by David Griesinger and amplified by Lexicon.Time of arrival may change, but pitch cannot be affected.Thiis myth needs to be put to bed for good.-CaseyI'm not talking about pitch (hence the "I'm not arguing that any observed variations would be due to pitch shifting" in my post). I just want to measure any *amplitude* fluctuations that do occur, and have the average rate & depth of the amplitude fluctuations measured for different sine frequencies.

---

### Post #723 -- Page 25
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8536181&postcount=723>

Quote: > Originally Posted byCasey➡️Time of arrival may change, but pitch cannot be affected....Unless you have an F16 flying around inside the hall.  I'd expect some substantial doppler shift, but then you'd probably have other things on your mind.

---

### Post #724 -- Page 25
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8537053&postcount=724>

Quote: > Originally Posted byseancostello➡️I'm not talking about pitch.I am sorry Sean, I misread your post. 


So yes, time of arrival and the phase of your signal will vary over time and direction. This is due to the variation in the speed of sound within the hall.


Michael what is an F16? Are you arguing that we can hear well above the highest note on a piano? 



-Casey

---

### Post #725 -- Page 25
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8537121&postcount=725>

Quote: > Originally Posted byCasey➡️Are you arguing that we can hear well above the highest note on a piano?Not after flying around in my F16

---

### Post #726 -- Page 25
**User:** Radardoug
**Info:** Joined: Oct 2009Posts: 2,048🎧 15 years | Posts: 2,048
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8537373&postcount=726>

If you take a tuned filter, and excite it with a frequency not quite on the resonant frequency of the filter, you will get output at the filter frequency.

There is a hall here in New Zealand (Michael Fowler Centre) that exhibits this phenomenom.

And my bathroom does it well.

Why don't good halls sound metallic?

---

### Post #727 -- Page 25
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8537922&postcount=727>

Quote: > Originally Posted byRadardoug➡️If you take a tuned filter, and excite it with a frequency not quite on the resonant frequency of the filter, you will get output at the filter frequency.There is a hall here in New Zealand (Michael Fowler Centre) that exhibits this phenomenom.And my bathroom does it well.Why don't good halls sound metallic?A good hall can be viewed as having a few BILLION of those resonant filters in parallel. The density (i.e. frequency distribution) of those filters increases as the square of frequency, if I remember my math correctly. A good hall is big enough that the lowest frequencies still have a couple of resonances per Hertz. A smaller hall, or a poorly designed/executed hall, one or more of the low resonances might be isolated enough that it causes audible pitch shifts.


If you have a good random distribution of these resonances, with consistent ring times for each of them, a given sine wave input will ring several resonances at once. This produces a signal that is best described as the input sine wave, decaying away, but with a very bumpy amplitude envelope. The denser the random distribution, the more random the bumpy amplitude envelope of the decaying signal will be.


A bad sounding reverb will display one or more of the following characteristics:


- Non-random distribution of resonance frequencies. If the frequencies are spaced at mathematically regular intervals, the result is a comb filter effect, with a very audible pitch.


- Not enough resonances. If the resonances are spaced too far apart, you can hear a beating effect as they decay away. A bit of subtle beating can be nice, but once this gets up beyond a few Hz it sounds REALLY bad. This can be audible in a small portion of the spectrum.


- Having one or more resonances decaying at a longer rate than the others. If there are a few of these close to each other, you will hear the beating between them.

---

### Post #728 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8539153&postcount=728>

Quote: > Originally Posted byseancostello➡️Bumping this due to a thought I just had:I think both experiments have been done in some form or another, though not exactly in the way that you proposed. 


Blesser's book describes sine tones transmitted through air over long distances (though not in a concert hall). In very still air with uniform temperature (i.e. underground), there is little variation in the received sine amplitude, but in outdoor environments there's a great deal of variation. He claims that over a distance of 300m, the propagation time varies by about 20 ms. So delay time variation of +/- 1% should be more or less in the ball park. But I dunno over what time scale this would be. Presumably it's some sort of 1/f variation.


I gave the book back to my boss, but I can steal it again if you want something more concrete than what's in my notes/memory.


The impulse response thing was described by Angelo Farina. He tried to average multiple concert hall impulse response recordings to improve the SNR, but found that it reduced high frequencies, indicating time variation.


Blesser claims that due to this time variation, *accurate* impulse response measurements can only be made for low frequencies, small spaces or early reflections. Of course impulse responses recordings that aren't restricted to these cases are still pretty useful for convolution plugins, but it limits the amount of useful data that you can extract, and you can't really legitimately claim that you've captured something authentic (though this doesn't seem to stop a lot of people).

---

### Post #729 -- Page 25
**User:** Ciozzi
**Info:** Joined: Mar 2007Posts: 1,540🎧 15 years | Posts: 1,540
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8542675&postcount=729>

Quote: > Originally Posted byCasey➡️Sean, this would be a very cool dream. Unfortunatly, it could never happen. There is no way that pitch can be affected in a natural space.Please do the science and agree that pitch cannot be affected by any naturally occuring acuostic space.This is an untruth propogated by David Griesinger and amplified by Lexicon.Time of arrival may change, but pitch cannot be affected.Thiis myth needs to be put to bed for good.-CaseyWell, it's a very remote possibility but pitch may be affected if something is moving inside the room. The doppler effect is very well documented and it can happen if either the source, the listener or any of the reflecting surfaces are changing their position in time.

---

### Post #730 -- Page 25
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8542793&postcount=730>

Quote: > Originally Posted byseancostello➡️A good hall can be viewed as having a few BILLION of those resonant filters in parallel.I read an article several years back (of *course* I can't remember where) that discussed theaters during the classical period of Greece.  Apparently large vases were placed around the theater to act as Helmholz resonators (an early version of LARES I guess).  It was probably quite an experience to be there (to watch Aristophanes take his curtain call), but it must have been bizarre acoustically.

---

### Post #731 -- Page 25
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8543203&postcount=731>

Quote: > Originally Posted byDeleted Nobody Special ➡️I read an article several years back (ofcourseI can't remember where) that discussed theaters during the classical period of Greece.  Apparently large vases were placed around the theater to act as Helmholz resonators (an early version of LARES I guess).  It was probably quite an experience to be there (to watch Aristophanes take his curtain call), but it must have been bizarre acoustically.There are many old Cathedrals into the walls of which were built Helmholtz resonators. It's a highly effective and proven method of controlling standing waves, actually makes the acoustics less bizarre..!

---

### Post #732 -- Page 25
**User:** undertone
**Info:** Joined: Jan 2007Posts: 1,2351 Review written🎧 15 years | Posts: 1,235
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8544329&postcount=732>

Quote: > Originally Posted byDeleted Nobody Special ➡️It was probably quite an experience to be there (to watch Aristophanes take his curtain call), but it must have been bizarre acoustically.It can still be. About 20 years ago I saw a performance of Shakespeare's Cymbeline at the [Epidaurus Theatre](https://en.wikipedia.org/wiki/Epidaurus) in Greece. It sits 15,000 and to this day dramatic performances are done un-amplified. I was amazed at the time by how intelligible speech was despite being 3/4 of the way up the center. I don't know if this theatre used resonators, but it definitely didn't sound un-natural.

---

### Post #733 -- Page 25
**User:** apprenticemart2
**Info:** Joined: Feb 2012Posts: 717🎧 10 years | Posts: 717
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8544519&postcount=733>

According to David Attenborough,if you are at the temple site of the city of Great Zimbabwe and speak in a normal voice you can be heard perfectly half a mile away in the valley below at the great enclosure. I'd love to know how that works. I think it's something to do with magic granite boulders oooooooh.

---

### Post #734 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8661297&postcount=734>

I've been working on something that I think is novel. I'm going to try to write up a paper for publication, but until then I'd like to see what you guys think about it.


The basic idea is simple; just a chain of 2x2 matrices and delays (as shown in the attached diagram). It's a feed-forward unitary network, with each successive stage doubling the number of echoes in the impulse response. This gets interesting when the delay lengths are powers of 2 (1, 2, 4, 8...) samples. The impulse response is a binary sequence (actually the [Rudin-Shapiro sequence](https://en.wikipedia.org/wiki/Rudin–Shapiro_sequence)) that's 2^(n+1) samples long for n stages. The impulse response is sort of maximally dense, since there's one echo per sample, and all echoes have uniform magnitude. This works because each echo in the impulse response corresponds to a unique path through the network.


It's a sort of burst of noise, like a multi-tap "gated reverb" algorithm, but much more dense. I can also get an exponential decay and high frequency damping, by inserting gains and filters inline with the delays, and also compensate the overall gain so that it's always unity. Reverse reverbs are possible this way as well, so long as care is taken to avoid numerical problems. Of course the decay always gets truncated at the end, but it's no problem to just make the sequence arbitrarily long. 20 stages is plenty. It can also easily be generalized to higher order matrices.


I think it's extremely promising for increasing echo density, as an alternative to things like allpasses. I'm not sure it's that useful for reverb, at least in the incarnation I've described. Since it's a binary sequence, each "echo" is either in phase or out of phase between the two outputs. The stereo image is kind of narrow. I'm looking into using sparse echo patterns, time variation, etc. to improve this.


Any thoughts/suggestions?

---

### Post #735 -- Page 25
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8663401&postcount=735>

Quote: > Originally Posted byacreil➡️IThe basic idea is simple; just a chain of 2x2 matrices and delays (as shown in the attached diagram).No diagram on this end - could you attach it again?

Quote: > It's a feed-forward unitary network, with each successive stage doubling the number of echoes in the impulse response. This gets interesting when the delay lengths are powers of 2 (1, 2, 4, 8...) samples. The impulse response is a binary sequence (actually theRudin-Shapiro sequence) that's 2^(n+1) samples long for n stages. The impulse response is sort of maximally dense, since there's one echo per sample, and all echoes have uniform magnitude. This works because each echo in the impulse response corresponds to a unique path through the network.This seems similar to a technique Miller Puckette has used in his reverbs, starting in the 1980s at IRCAM. I call the technique "cascaded unitary systems" but there might be a better name for it:

[Artificial reverberation](http://crca.ucsd.edu/~msp/techniques/latest/book-html/node111.html)


Your choice of delay lengths is certainly far different than the standard applications of this technique. Puckette's examples tends to use more standard "reverb delay lengths."

Quote: > It's a sort of burst of noise, like a multi-tap "gated reverb" algorithm, but much more dense. I can also get an exponential decay and high frequency damping, by inserting gains and filters inline with the delays, and also compensate the overall gain so that it's always unity. Reverse reverbs are possible this way as well, so long as care is taken to avoid numerical problems. Of course the decay always gets truncated at the end, but it's no problem to just make the sequence arbitrarily long. 20 stages is plenty. It can also easily be generalized to higher order matrices.I will be VERY interested to see how you control the decay shape. My experiments with the cascaded unitary systems always result in a Gaussian reverb envelope.


Don't forget that you can put feedback around a unitary system. In the example you describe, you would have 2 feedback paths.

Quote: > I think it's extremely promising for increasing echo density, as an alternative to things like allpasses. I'm not sure it's that useful for reverb, at least in the incarnation I've described. Since it's a binary sequence, each "echo" is either in phase or out of phase between the two outputs. The stereo image is kind of narrow. I'm looking into using sparse echo patterns, time variation, etc. to improve this.Any thoughts/suggestions?Run two of the cascaded systems in parallel, one for the left channel, one for the right. Vary the sign of theta in the rotation matrices between channels. In other words, if the angles of the cascaded rotation matrices are as follows in one channel:


45  45  45  45  45  45  45  45 


the other channel could have rotation matrices with these angles


45 -45  45 -45  45 -45  45 -45


You may wish to try something more random. Or, if you are using a cascade with the number of cascaded units as a power of 2, you could use the + and - signs of two rows in a Hadamard matrix to control the rotation angles.

---

### Post #736 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8664856&postcount=736>

Quote: > Originally Posted byseancostello➡️No diagram on this end - could you attach it again?er... I distinctly remember uploading it... and then after that I remember not bothering to check that it had actually been posted 

Quote: > This seems similar to a technique Miller Puckette has used in his reverbs, starting in the 1980s at IRCAM. I call the technique "cascaded unitary systems" but there might be a better name for it:Exactly. I asked him about it. He hadn't tried spacing the delays this way. And I haven't seen that structure anywhere else.

Quote: > Your choice of delay lengths is certainly far different than the standard applications of this technique. Puckette's examples tends to use more standard "reverb delay lengths."Right. It seemed weird to me at first, but for recirulating comb filters or whatever, you choose "incommensurate" delays so that the echoes don't coincide until (inevitably) the product of two of the delay lengths. But it doesn't work like that here.


The impulse response in this feed-forward structure is the superposition of every possible path through the network, i.e. the are echoes every additive combination of delay lengths. The echoes don't coincide as long as each delay is longer than the sum of all the shorter delays. Powers of two will fill every spot with no coinciding delays (since each delay is the sum of the shorter delays + 1). The impulse response is sort of a "boxcar" shape. If the delays are more widely spaced (sum + 2 or more), then not every spot is filled, so it's sparse. If they're more closely spaced, you get many coinciding echoes, and an overall Gaussian type shape.

Quote: > I will be VERY interested to see how you control the decay shape. My experiments with the cascaded unitary systems always result in a Gaussian reverb envelope.It's just the usual g = 10^-3t/RT60. This actually works for reverse reverb too. It's using the same equation, but with a negative RT60, which would normally be unstable. It doesn't work if the RT60 is very short compared to the total impulse response length, but it's fine for anything reasonable.

Quote: > Don't forget that you can put feedback around a unitary system. In the example you describe, you would have 2 feedback paths.I thought about it, but I can't really see the advantage here. For one thing, chaining them can sorta "undo" everything. h12(n) * h21(n) - h11(n) * h22(n) just turns it into a straight delay (* is convolution), though the sign depends on the number of stages. Anyway it's not going to get any more dense, and I've already got an exponential decay. I think it makes more sense to feed it into something else, to sort of smooth out the response like a moving average filter.

Quote: > Run two of the cascaded systems in parallel, one for the left channel, one for the right. Vary the sign of theta in the rotation matrices between channels. In other words, if the angles of the cascaded rotation matrices are as follows in one channel:The thing is that two binary sequences are at best going to be 50% correlated and 50% anticorrelated. I need to try more sparse delay patterns and see how that works, and maybe try delay time modulation.


One idea I had for time variation was to insert first order allpass filters (I mean phase shifters, not Schroeder allpasses) inline with the outputs of each stage. I'd been using them recently to sort of smoothly invert signals. I think that would cover your suggestion for different matrix angles. I haven't tried that yet either.

---

### Post #737 -- Page 25
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8669406&postcount=737>

Quote: > Originally Posted byacreil➡️Any thoughts/suggestions?In your diagram, I think that the add and subtract nodes should come AFTER the delay line. This will make it work better at the input of a network, when both "branches" are fed by the same signal. If the subtract happens before the delay, and the same signal is fed to both branches, the delay won't have any input.


I'd love to hear any sound examples of this in action!

---

### Post #738 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8671002&postcount=738>

I actually have another mixing stage at the end of the chain. That way both inputs and both outputs see the complete set of delays. Otherwise one is always delayed with respect to the other. You're right that there's cancellation when the inputs are correlated (or when the outputs are mixed). That's partly why I think this configuration is better used as a way to increase echo density, rather than a complete reverb. To avoid cancellation I think it might be best to use two separate chains that produce sparse responses, each with a different series of delay lengths to minimize coinciding echoes.


I'll post example impulse responses and sound samples when I get something a little more satisfactory, or at least better understand how to use it.

---

### Post #739 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8772636&postcount=739>

Small update...


The unitary network thing I'm working on doesn't work well with embedded damping filters unless progressively higher order filters are used. The reason is that it "switches over" from a signal that has passed through many filters (i.e. 2^(x)-1 samples of delay) to one that's passed through only one (2^x samples). At this point there's an audible discontinuity in the decay.


I don't think there's really much point in trying to use this as an all-inclusive reverberator, so I don't see it as a big issue. There are probably also ways to make it less noticeable.


On the other hand, I think a variation that would work well is to embed very short delays within the matrix of an FDN. The idea is to make a sort of crude model of diffuse reflections, without the problems associated with allpasses. I think on average the group delay ends up being flat, so it shouldn't contribute to increasing coloration over long decays. Also this doesn't have (to any significant degree) the "deconvolution" problem I mentioned earlier due to complementary sequences, as larger matrices have many more paths through them (n^2 for an n x n matrix). 


For a 4-delay FDN this would mean delays sandwiched between 4x4 Hadamard (or whatever) matrices. It's similar to the 2x2 case I describe above, but the delays would be 0, 1, 2, 3 samples for the first stage, then 0, 4, 8, 12, then 0, 16, 32, 48... This gives the same maximally dense (one echo per sample) result as the 2x2 case with power-of-two delay lengths.


This requires one matrix for each stage, so it gets a little expensive, but I think it would be good enough to sort of intersperse a small number of short delays at various points. I haven't tried this yet.

---

### Post #740 -- Page 25
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8774400&postcount=740>

Quote: > Originally Posted byacreil➡️Small update...The unitary network thing I'm working on doesn't work well with embedded damping filters unless progressively higher order filters are used. The reason is that it "switches over" from a signal that has passed through many filters (i.e. 2^(x)-1 samples of delay) to one that's passed through only one (2^x samples). At this point there's an audible discontinuity in the decay.I don't think there's really much point in trying to use this as an all-inclusive reverberator, so I don't see it as a big issue. There are probably also ways to make it less noticeable.On the other hand, I think a variation that would work well is to embed very short delays within the matrix of an FDN. The idea is to make a sort of crude model of diffuse reflections, without the problems associated with allpasses. I think on average the group delay ends up being flat, so it shouldn't contribute to increasing coloration over long decays. Also this doesn't have (to any significant degree) the "deconvolution" problem I mentioned earlier due to complementary sequences, as larger matrices have many more paths through them (n^2 for an n x n matrix).For a 4-delay FDN this would mean delays sandwiched between 4x4 Hadamard (or whatever) matrices. It's similar to the 2x2 case I describe above, but the delays would be 0, 1, 2, 3 samples for the first stage, then 0, 4, 8, 12, then 0, 16, 32, 48... This gives the same maximally dense (one echo per sample) result as the 2x2 case with power-of-two delay lengths.This requires one matrix for each stage, so it gets a little expensive, but I think it would be good enough to sort of intersperse a small number of short delays at various points. I haven't tried this yet.I'd be interested to hear the results.


One issue I have found with the sort of "cascaded feedforward unitary systems" you describe, is the tendency of the output of the cascade to have a Gaussian shaped impulse response. Are you are to avoid this by using a gain factor for each delay?

---

### Post #741 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8778958&postcount=741>

Quote: > Originally Posted byseancostello➡️One issue I have found with the sort of "cascaded feedforward unitary systems" you describe, is the tendency of the output of the cascade to have a Gaussian shaped impulse response. Are you are to avoid this by using a gain factor for each delay?It's the spacing of the delays that produces a Gaussian response (the length of delay x is smaller than or equal to the sum of all smaller delays). With power of 2 delay lengths, the impulse response has a "boxcar" shape without added gains.


I'm attaching basic impulse responses using power of two delays. You'll notice the timbre is weird. I don't notice this when it's put in series with other things. I've been trying to find other useful sequences. I think several different sequences could be combined to make it more "reverb-like".

---

### Post #742 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8785040&postcount=742>

I thought of a way to describe the impulse response shape that makes a little bit more sense... or maybe it will just be more confusing.


Consider an exponentially spaced sequence of delays with an arbitrary base of x. The kth delay is then dk = x^k samples. If x < 2, dk is less than the sum of all the delays d0 to dk-1 of the previous stages. If x = 2, dk is equal to the sum of delays d0 to dk-1 plus one sample. if x > 2, dk is greater than the sum of delays d0 to dk-1.


The impulse response of the kth stage is an impulse at 0 and an impulse at dk. The impulse response of the previous stages is convolved with this, so each stage basically adds a delayed copy of the result of the previous stages. If dk is shorter than the response of the previous stages (x < 2), the "original" and "delayed" copies will overlap, eventually resulting in a Gaussian-shaped response. 


If x = 2, the "delayed" copy will be appended to the end of original, resulting in a binary sequence with fractal properties that doubles in length with each added stage.


If x > 2, there will be a gap between the original and delayed sequences, producing an impulse response that sort of looks like the Cantor set.


I've attached some examples. x3,10.wav is x = 3, 10 stages. x1.5,25 is x = 1.5, 25 stages, and I'm sure you can deduce what the other one is. The "f" files have a fractal echo pattern, which just means that there's a constant gain of 0.5 inline with each delay. This tends to produce really bizarre results for x < 2, but I don't understand why.

---

### Post #743 -- Page 25
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=8788981&postcount=743>

Using a base of x = about sqrt(3) seems like an ok compromise between improved timbre and slightly sub-optimal impulse response shape. It doesn't have a long onset, but it's sort of lumpy (actually another weird fractal pattern). As a single network, this might be the most useful configuration.


Also series and parallel networks improve the sound, at some added computational expense.


I'm trying to think of some sort of FDN-like configuration that improves the existing shortcomings without introducing a bunch of new ones.

---

### Post #744 -- Page 25
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9486244&postcount=744>

For a thread on reverb this room is pretty dead.....!!!


Who's coming to the AES next week?

---

### Post #745 -- Page 25
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9486245&postcount=745>

For a thread on reverb this room is pretty dead.....!!!



Who's coming to the AES next week?

---

### Post #746 -- Page 25
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9486335&postcount=746>

Quote: > Originally Posted byzmix➡️Who's coming to the AES next week?Michael and I will both be speaking at a reverb discussion on Sunday morning. 



-Casey

---

### Post #747 -- Page 25
**User:** Avast!
**Info:** Joined: Oct 2010Posts: 373My Recordings/Credits🎧 15 years | Posts: 373My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9486339&postcount=747>

Valhalla hardware?

---

### Post #748 -- Page 25
**User:** ionian
**Info:** Joined: May 2010Posts: 7,477My Studio1 Review written🎧 15 years | Posts: 7,477My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9486720&postcount=748>

Quote: > Originally Posted byzmix➡️For a thread on reverb this room is pretty dead.....!!!Who's coming to the AES next week?Me!


Thanks,

Frank

---

### Post #749 -- Page 25
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9486997&postcount=749>

Quote: > Originally Posted byCasey➡️Michael and I will both be speaking at a reverb discussion on Sunday morning.I'm very much looking forward to it.  I hope a few of you will be able to come.

---

### Post #750 -- Page 25
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9488045&postcount=750>

Quote: > Originally Posted byAvast!➡️Valhalla hardware?No hardware yet. I'm working on cartridges for the TipTop Audio Z-DSP, which is a programmable DSP for Eurorack. So, my algorithms will be outside of the computer, but not in my own hardware boxes.


---

## Page 26

---

### Post #751 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9488235&postcount=751>

Quote: > Originally Posted byDeleted Nobody Special ➡️I'm very much looking forward to it.  I hope a few of you will be able to come.I won't be there, but I hope you and Casey wear some fake beards to get into the spirit of the event.

---

### Post #752 -- Page 26
**User:** kptainfilou
**Info:** Joined: Nov 2006Posts: 146🎧 15 years | Posts: 146
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9488549&postcount=752>

Quote: > Originally Posted byseancostello➡️No hardware yet. I'm working on cartridges for the TipTop Audio Z-DSP, which is a programmable DSP for Eurorack. So, my algorithms will be outside of the computer, but not in my own hardware boxes.Is that why there's still no update to AAX for any of your products ? heh

---

### Post #753 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9488671&postcount=753>

Quote: > Originally Posted bykptainfilou➡️Is that why there's still no update to AAX for any of your products ? hehThere's this **really cool** feature in modern businesses, where more than one task can be underway at a time!

---

### Post #754 -- Page 26
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9489104&postcount=754>

Quote: > Originally Posted byseancostello➡️I won't be there, but I hope you and Casey wear some fake beards to get into the spirit of the event.No, but we will be wearing our superhero capes.  Casey may have leotards on.

---

### Post #755 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9489208&postcount=755>

Quote: > Originally Posted byDeleted Nobody Special ➡️No, but we will be wearing our superhero capes.  Casey may have leotards on.Here's my million dollar idea: Come onstage as Mummenschanz. Black leotards, paper masks. Do some wacky, surrealistic mimes, then take off your paper masks, and - surprise, Mummenschanz is a couple of noted reverb developers! People would go crazy, I tell ya, CRAZY.

{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "@id": "https://youtube.com/v/3eazq_8jCOg",
  "name": "YouTube Video",
  "description": "Embedded YouTube video",
  "thumbnailUrl": "https://i.ytimg.com/vi/3eazq_8jCOg/hqdefault.jpg",
  "uploadDate": "2013-10-09T03:23:49+01:00",
  "contentUrl": "https://youtube.com/v/3eazq_8jCOg",
  "embedUrl": "https://youtube.com/embed/3eazq_8jCOg"
}

---

### Post #756 -- Page 26
**User:** kptainfilou
**Info:** Joined: Nov 2006Posts: 146🎧 15 years | Posts: 146
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9489856&postcount=756>

Quote: > Originally Posted byseancostello➡️There's thisreally coolfeature in modern businesses, where more than one task can be underway at a time!And there's this fantastic feature in the modern world called **"communication"** sometimes dubbed as **"news".**

---

### Post #757 -- Page 26
**User:** niklasni1
**Info:** Joined: Aug 2011Posts: 1,098🎧 10 years | Posts: 1,098
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9494657&postcount=757>

I want more reverb geekery. This thread is legend and a half, I'm just sad I've already read it all twice.


How are you finding the Z-DSP, Sean? It's built on that Spin Semi chip, right? I'm not into Eurorack (wallet issues), but I've been close to getting the development board a few times. I'm slowly moving towards an all-DIY hardware setup for electronic music (I call it the Glorious Five Year Plan), but there's a big reverb-shaped unknown in that equation. Lots going on in synth DIY, but less so for digital effects it seems.


The Spin Semi chip looks like a great architecture for effects, but I must say I find the limited number of controls a bit off-putting. I'd be keen to hear any thoughts on the platform.

---

### Post #758 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9497338&postcount=758>

Quote: > Originally Posted byniklasni1➡️I want more reverb geekery. This thread is legend and a half, I'm just sad I've already read it all twice.How are you finding the Z-DSP, Sean? It's built on that Spin Semi chip, right? I'm not into Eurorack (wallet issues), but I've been close to getting the development board a few times. I'm slowly moving towards an all-DIY hardware setup for electronic music (I call it the Glorious Five Year Plan), but there's a big reverb-shaped unknown in that equation. Lots going on in synth DIY, but less so for digital effects it seems.The Spin Semi chip looks like a great architecture for effects, but I must say I find the limited number of controls a bit off-putting. I'd be keen to hear any thoughts on the platform.First of all, the development board is plenty easy to work with, so I'd recommend picking one up. For small-scale DIY projects, you may want to look at the SKRM-C8 daughter boards, which will integrate into your own circuits without having to solder surface mount:

[SKRM-C8-XXX | Experimental Noize](http://www.experimentalnoize.com/components/skrm-c8-xxx-reverb-effects-module/)


The FV-1 is really limited. Sometimes these limits are inspiring. For reverbs, you have JUST ENOUGH cycles to make things work, and coming up with different things that work is a lot of fun (for me). Having to cut the complexity of an algorithm in half, while trying to retain the sound, is helping me get better at reverb design. 


Sometimes these limits kinda suck. The pitch shifter is good for mild detuning, but for larger pitch shift amounts it is VERY metallic, and I am finding it difficult to get rid of this metallic sound. I need to remove the "metal" in order to have decent Shimmer algorithms in there.  Generating triangle waves takes a lot of cycles. Random numbers are near impossible to generate and use.


The limited number of controls is actually pretty great. It turns out that a 3 knob reverb can be very powerful and also easy to use. Lots of stomp boxes used 3 knobs or less, and are still much loved. You can always use analog circuitry for wet/dry mix, tone controls, feedback processing, etc.


The headroom of the FV-1 is limited, compared to floating point processing. This gives the FV-1 a "sound." I like this sound. It reminds me of the older fixed point reverb hardware. The 224XL I was working with this week also has a "sound," with quantization noise, quantized modulation, and lots of other "schmuck" that probably comes from rounding errors and saturation within the algorithms.

---

### Post #759 -- Page 26
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9508616&postcount=759>

I just picked up a 224, moved the sliders to the middle, fed in some tracks, and 'wow'. I thought my PCM91 sounded good - it is a better reverb than most of my others. But the 224 sounds, oh I don't know, different, and in a very good way. There's something about the sound that isn't just in the algorithms, maybe the phase shift of the antialiasing filters or the EQ network or something, but it's different.

---

### Post #760 -- Page 26
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9508651&postcount=760>

Quote: > Originally Posted byCasey➡️Michael and I will both be speaking at a reverb discussion on Sunday morning.-Casey

I scoured most of the schedule, what's the title of the event?



I'll be mentoring for SPARS Friday-Sunday..


...see you there!

---

### Post #761 -- Page 26
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9508656&postcount=761>

Quote: > Originally Posted bydale116dot7➡️I just picked up a 224, moved the sliders to the middle, fed in some tracks, and 'wow'. I thought my PCM91 sounded good - it is a better reverb than most of my others. But the 224 sounds, oh I don't know, different, and in a very good way. There's something about the sound that isn't just in the algorithms, maybe the phase shift of the antialiasing filters or the EQ network or something, but it's different. I don't know if it's the gain staged converters, the fact that they're Successive Approximation, or maybe it's the enormous output transformers and very nice input transformers, but that hardware is remarkable.. I use mine all the time, nothing in a plugin can touch it.

---

### Post #762 -- Page 26
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9508694&postcount=762>

Quote: > Originally Posted byCasey➡️Of course there is time variation in a hall. But the time of arrival, while it may vary, is never pitch shifted.-CaseyI was at a cabin on a lake a few months ago, and there was a large bonfire going.  I placed a portable radio on a chair and  sat across the bonfire from it.  The pitch shifting was plainly audible in the form of a through zero flanging  / Leslie speaker effects.  Quite incredible...  Thermal currents affect  sound wave propagation, so I think the possibility of pitch variations occurring in nature should be considered.

---

### Post #763 -- Page 26
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9508724&postcount=763>

It's been quite a long time since I've worked on reverb algorithms. I usually use my DIY hardware as straight ahead digital delay lines. I was thinking of 'finishing up' a bunch of algorithms on my DSBP56366 box. Although the 56366 isn't a current IC any more I do have a bunch of them and PC boards are relatively inexpensive so I can get new ones made up with my hardware fixes. I'd change the design out to a 4-layer to clean up the memory signals.


One thing I am a bit curious about is what the EMT-250 sounds like. I've never heard one (at least not up close and personal) but the hardware design seems quite interesting.

---

### Post #764 -- Page 26
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9509243&postcount=764>

Quote: > Originally Posted byzmix➡️I scoured most of the schedule, what's the title of the event?...see you there!Thanks for asking.  Here it is:
[Workshop](http://www.aes.org/events/135/workshops/?ID=3722)

---

### Post #765 -- Page 26
**User:** niklasni1
**Info:** Joined: Aug 2011Posts: 1,098🎧 10 years | Posts: 1,098
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9512838&postcount=765>

Quote: > Originally Posted byseancostello➡️The FV-1 is really limited. Sometimes these limits are inspiring. For reverbs, you have JUST ENOUGH cycles to make things work, and coming up with different things that work is a lot of fun (for me). Having to cut the complexity of an algorithm in half, while trying to retain the sound, is helping me get better at reverb design.But for a regular programmer (with some assembly experience on various processors), do you think the instruction set serves as a good introduction to DSP?

Quote: > The limited number of controls is actually pretty great. It turns out that a 3 knob reverb can be very powerful and also easy to use. Lots of stomp boxes used 3 knobs or less, and are still much loved. You can always use analog circuitry for wet/dry mix, tone controls, feedback processing, etc.Right, I appreciate that... but you still have to worry about which controls to bring out, and what ranges to give them.. especially while you're developing an algorithm. Maybe I'm just too structured as a programmer for this type of work  but I'd prefer to have the parameters of a programme clearly separate from the interface, and that seems like it'd be somewhat manual and tedious (and maybe a little expensive) in the FV1 assembly language..

---

### Post #766 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9514754&postcount=766>

Quote: > Originally Posted byniklasni1➡️But for a regular programmer (with some assembly experience on various processors), do you think the instruction set serves as a good introduction to DSP?Compiling a GUI-less VST would be a much better way of learning DSP for a regular programmer. You can use C/C++.

---

### Post #767 -- Page 26
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9520548&postcount=767>

I posted a sample of a new-ish Pure Data reverb algorithm on some other thread, but it got deleted for whatever reason. It was a spinoff of [this one](https://gearspace.com/board/electronic-music-instruments-electronic-music-production/850256-reverb-alesis-wedge-action.html) (which is where the dry recording came from).


It's a new design, but you may be able to infer where some of the inspiration came from. It's entirely randomized, based on time-varying multiap delays, allpass chains (which I think may be a significant invention) and multitap modulated delays. It also includes the unitary network thing that I described previously.


edit: cropped the screen shot of the patch so that it doesn't get auto-resized.


The patch is available if anyone's interested. It's not the most usable thing in the world, but the sound is better than anything else I've made or used.

---

### Post #768 -- Page 26
**User:** niklasni1
**Info:** Joined: Aug 2011Posts: 1,098🎧 10 years | Posts: 1,098
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9522964&postcount=768>

That does sound very nice. I'd like the patch if you're sharing

---

### Post #769 -- Page 26
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9527588&postcount=769>

Quote: > Originally Posted byniklasni1➡️I'd like the patch if you're sharingThis should work in Pd-extended.

---

### Post #770 -- Page 26
**User:** niklasni1
**Info:** Joined: Aug 2011Posts: 1,098🎧 10 years | Posts: 1,098
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9528319&postcount=770>

Thank you.

---

### Post #771 -- Page 26
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9534420&postcount=771>

{Post AES bump}

---

### Post #772 -- Page 26
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9580226&postcount=772>

AES : W26 FX Design Panel - Reverb.


Some talk about :


The motivation behind the current products.

What makes a great sounding reverb.

Hardware vs software development.

Convolution vs algorithmic.

Lexicon tool box (allpass loops, modulation etc.).

---

### Post #773 -- Page 26
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9581015&postcount=773>

Quote: > Originally Posted byzmix➡️I was at a cabin on a lake a few months ago, and there was a large bonfire going.  I placed a portable radio on a chair and  sat across the bonfire from it.  The pitch shifting was plainly audible in the form of a through zero flanging  / Leslie speaker effects.  Quite incredible...  Thermal currents affect  sound wave propagation, so I think the possibility of pitch variations occurring in nature should be considered.Nope. What you heard was simple multi-path. This causes flanging of course, but no (pitch aspect of the) Leslie effect.


The source signal was split into multiple audible paths on the way to your ear. Some went through rapidly varying heated air, some did not. This causes delay/phase variation between the multiple paths. This is exactly what phase shift/flange is.


A phase shift between one or more identical signals can resemble pitch shift as different frequencies are amplified and attenuated over time.


Nothing in the environment you describe could have caused a pitch shift though.


Pitch is affected by movement in the environment; Of you or the source or anything in between. Pitch can also be affected by sympathetic vibrations/resonances of physical elements which are off pitch.


In nature you could have moving leaves, lightening "cracks" that move rapidly from the ground to the sky or the flapping wings of flying monkeys or the bird on your shoulder.



-Casey

---

### Post #774 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9661037&postcount=774>

I am trying to wrap my head around how resonance density balances out with maximum echo density in digital reverbs. Here's the hypothetical situation:


You have an LTI digital reverb with 50 seconds of delay time, spaced between a huge number of parallel combs in a feedback delay network (we've got ourselves a fast computer here). Several hundred to a few thousand or so parallel delay lines. The delay lines are perfectly tuned, so the resonance and echo density is smooth as butter. The 50 seconds of delay time gives you 50 resonances per Hertz. 


Set this hypothetical reverb for a 2 second delay time.


Now take an impulse response of the reverb. To get past any frequency domain convolution issues, the impulse response will be realized with a direct form FIR filter. Again, we've got ourselves a fast hypothetical computer.


According to convolution theory, the impulse response should perfectly capture the sound of the LTI system. Let's assume that we have a "true stereo" impulse of the huge FDN, with separate impulses for L->L, L->R, R->R, R->L. This would take 8 seconds of delay memory for the FIR filter. Pretty sizable memory savings.


DOES the impulse response really capture the sound of the reverb? What happened to the 50 resonances per hertz? The FIR has 0 resonances per hertz. Can you really hear those 50 resonances per hertz in a 2 second decay? Assuming that the raw number crunching issues aren't important, are we wasting the 50 seconds of delay memory in our FDN, if we could get by with 8 seconds using a direct form realization?


I'm really confused by the above ideas. Obviously, they relate to capturing the real modal density of a concert hall (which will have billions of discrete resonances, as opposed to the 100*sampling rate resonances of our hypothetical example). It also relates to the general idea of series versus parallel reverberator algorithms, and whether there is an upper limit to the amount of delay memory that can be effectively utilized in an artificial reverberator.

---

### Post #775 -- Page 26
**User:** feck
**Info:** Joined: Aug 2006Posts: 4,489My Recordings/Credits🎧 15 years | Posts: 4,489My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9661041&postcount=775>

Sean, Casey, Martin...I LOVE that there are people like you out there who ponder these intricacies so that the rest of us can benefit from your findings. And this as I am bouncing a mix right now with an M7, a bunch of Valhalla verbs and several LX480's on it.

---

### Post #776 -- Page 26
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9661461&postcount=776>

Quote: > Originally Posted byseancostello➡️50 seconds of delay time, spaced between a huge number of parallel combs in a feedback delay network.You say parallel combs in an FDN. Don't you mean serial combs then? I want to understand this first before continuing.



-Casey

---

### Post #777 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9661848&postcount=777>

Quote: > Originally Posted byCasey➡️You say parallel combs in an FDN. Don't you mean serial combs then? I want to understand this first before continuing.-CaseyParallel delays in an FDN.

---

### Post #778 -- Page 26
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9662710&postcount=778>

Hi everybody!


This thread has been very interesting to read... 

Quote: > Originally Posted byseancostello➡️DOES the impulse response really capture the sound of the reverb?IMO, only if you take the dynamic range of the system into account. If you use RT60 as a measurement for the reverberation time and you have a dynamic range of 60 dB, it would at least be true...

Quote: > Originally Posted byseancostello➡️What happened to the 50 resonances per hertz? The FIR has 0 resonances per hertz. Can you really hear those 50 resonances per hertz in a 2 second decay? Assuming that the raw number crunching issues aren't important, are we wasting the 50 seconds of delay memory in our FDN, if we could get by with 8 seconds using a direct form realization?Yes, the convolution would be the most sufficient implementation in terms of memory in this case. The 50 resonances per second cannot be observed due to the limited frequency resolution with an observation window of only two seconds (=> 1/2 Hz frequency bins).


Stian

---

### Post #779 -- Page 26
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9662834&postcount=779>

Quote: > Originally Posted byseancostello➡️I am trying to wrap my head around how resonance density balances out with maximum echo density in digital reverbs. Here's the hypothetical situation:Assuming all delays are short enough that they recirculate a number of times before the reverb decays, think about how they will be tuned. There will be so many that you can't put all the delays to good use. For a really crude calculation, say that 50 seconds of delay is distributed over 500 delay lines tuned between, say, 60 and 120 ms, or 2880 and 5760 samples at a sample rate of 48 kHz. Well, there are only 340 prime numbers between 2880 and 5760 (and I know they only have to be coprime, but that doesn't get you that many more). You could, of course, use a higher sample rate and/or subsample interpolation, but they're already tuned very closely together. Delays tuned to 3331 and 3343 samples (just adjacent primes I picked arbitrarily; these are actually spaced further apart than most) have resonances differing by only 0.0517 Hz (this is assuming parallel comb filters rather than an FDN). The beating period is 19.33 seconds, which is far longer than the decay time. I don't think these are going to be audibly distinct. Having this many delays will be pretty redundant.


This leads to an a different conception... Given a very dense cluster of sine tones (i.e. resonances), what's the shortest signal duration that can adequately resolve them? If they're tuned so closely together that the beating periods between adjacent resonances are much longer than the signal duration, you can sensibly say that they can't be resolved, right? So there's a sort of upper limit to useful modal density for a given decay time. If it's 50 resonances per Hz, certainly you'd need more than a 2 second decay time. And I suppose you could also consider a corresponding "echo density of white noise" that you also can't exceed.... 


I don't remember the best way to resolve different frequencies in the frequency domain, but I know of one that's pretty good. PARSHL (i.e. what Julius O. Smith III was doing in the mid 80s) estimates frequency by taking a rectangular windowed portion of the signal, zero padding it, FFT, then searching for peaks in the interpolated spectrum. And there's another way that involves using some other window function and then searching for a resulting window function "kernel". I forgot how those are supposed to compare, but at any rate the resolution is much better than just the bin size, and might give a rough idea of a theoretical upper limit of modal density. But certainly this would be better than what the human ear can resolve...


So there are surely limits to how far things can be pushed before any further improvement is irrelevant. But in practice, since low CPU usage is still a priority, the goal is still generally to take limited resources and make something that sucks as little as possible.

---

### Post #780 -- Page 26
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663530&postcount=780>

Quote: > Originally Posted bysaagedal➡️Hi everybody!Hi!

Quote: > If you use RT60 as a measurement for the reverberation time and you have a dynamic range of 60 dB, it would at least be true...We're talking a purely hypothetical system here. So it has REALLY good dynamic range. 

Quote: > Yes, the convolution would be the most sufficient implementation in terms of memory in this case. The 50 resonances per second cannot be observed due to the limited frequency resolution with an observation window of only two seconds (=> 1/2 Hz frequency bins).This makes sense. RT60 is essentially our observation window in this case.


---

## Page 27

---

### Post #781 -- Page 27
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663577&postcount=781>

Quote: > Originally Posted byacreil➡️Assuming all delays are short enough that they recirculate a number of times before the reverb decays, think about how they will be tuned. There will be so many that you can't put all the delays to good use. For a really crude calculation, say that 50 seconds of delay is distributed over 500 delay lines tuned between, say, 60 and 120 ms, or 2880 and 5760 samples at a sample rate of 48 kHz. Well, there are only 340 prime numbers between 2880 and 5760 (and I know they only have to be coprime, but that doesn't get you that many more). You could, of course, use a higher sample rate and/or subsample interpolation, but they're already tuned very closely together.Again, this is a hypothetical example. Although the recent Quantec Yardsticks seem to use a similar structure (parallel "resonantors" with >50 seconds of total delay memory). 


A real physical concert hall would have far more modal density than our hypothetical 50 second FDN reverb. The mean free path of Boston Symphony Hall is 53 feet (47 msec), so having a few hundred to a few thousand parallel delays in the 30 msec to 60 msec range seems about right, although I would probably extend the max delay range to 120 msec as you suggest.

Quote: > This leads to an a different conception... Given a very dense cluster of sine tones (i.e. resonances), what's the shortest signal duration that can adequately resolve them? If they're tuned so closely together that the beating periods between adjacent resonances are much longer than the signal duration, you can sensibly say that they can't be resolved, right? So there's a sort of upper limit to useful modal density for a given decay time. If it's 50 resonances per Hz, certainly you'd need more than a 2 second decay time. And I suppose you could also consider a corresponding "echo density of white noise" that you also can't exceed....This makes sense. 

Quote: > I don't remember the best way to resolve different frequencies in the frequency domain, but I know of one that's pretty good. PARSHL (i.e. what Julius O. Smith III was doing in the mid 80s) estimates frequency by taking a rectangular windowed portion of the signal, zero padding it, FFT, then searching for peaks in the interpolated spectrum.That's weird. I mentioned PARSHL in a tweet the other day. Tim Stilson used to use this at my old job, to take noisy loops (for engine noise) and resample them so they would loop at 64 sample boundaries. This was necessary for the PS2 sound system.

Quote: > So there are surely limits to how far things can be pushed before any further improvement is irrelevant. But in practice, since low CPU usage is still a priority, the goal is still generally to take limited resources and make something that sucks as little as possible.It's been a while since I've worked on an embedded processor, and I never had full reign of the SHARCs & Blackfins I used. It would be interesting to see what algorithm architectures would work on a platform with a modern DSP or ARM, that was dedicated to reverb processing. Having a huge amount of delay memory would certainly be convenient, but there is no point wasting the delay memory on things that can't be heard.

---

### Post #782 -- Page 27
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663651&postcount=782>

Quote: > Originally Posted byseancostello➡️Parallel delays in an FDN.Ok, well I am going to assume that you have a non-trivial mixing matrix. I think of that as serial combs, but no matter.


Except that an FDN is not a collection of parallel combs. It is a collection of long loops with very low gain through each entire loop.


50 secs is a long time. Your frequency peaks and valleys are going to be very shallow (because of the very low gain through any entire loop) and won't contribute much to the frequency response of the FDN.


As far as an FIR capturing the frequency response of the FDN, yes of course it will.


The reason to have an FDN is to increase time density. So your FDN is just a means to an end. Creating the dense pulse trains and frequency response that you capture in your FIR.



-Casey

---

### Post #783 -- Page 27
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663729&postcount=783>

Quote: > Originally Posted byseancostello➡️You have an LTI digital reverb with 50 seconds of delay time, spaced between a huge number of parallel combs in a feedback delay network.Quote: > Originally Posted byacreil➡️Assuming all delays are short enough that they recirculate a number of times before the reverb decays, think about how they will be tuned.Quote: > Originally Posted byseancostello➡️so having a few hundred to a few thousand parallel delays in the 30 msec to 60 msec range seems about right.Again, not sure what we are talking about here. An FDN of a few hundred combs coupled in an FDN by a non-trivial mixing matrix will have a near infinite number of loops. Why are we talking about peaks in individual combs?


Why the prime numbers? They have no use/meaning in this context.


-Casey

---

### Post #784 -- Page 27
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663767&postcount=784>

Quote: > Originally Posted byCasey➡️Again, not sure what we are talking about here. An FDN of a few hundred combs coupled in an FDN by a non-trivial mixing matrix will have a near infinite number of loops. Why are we talking about peaks in individual combs?I'm talking about peaks/valleys in the entire system. Let's assume a maximally diffuse scattering matrix. 512/1024 order Hadamard matrix, if that works for you.


"Parallel combs" was used as a shorthand for parallel delay lines in an FDN, versus a feedforward unitary system. Obviously, the more coupling there is between the delay lines, the further away things get from parallel comb filters.

---

### Post #785 -- Page 27
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663791&postcount=785>

Quote: > Originally Posted byCasey➡️Ok, well I am going to assume that you have a non-trivial mixing matrix. I think of that as serial combs, but no matter.Why do you think of this as serial combs? That is an intriguing viewpoint, but I don't claim to understand it.

---

### Post #786 -- Page 27
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663860&postcount=786>

Quote: > Originally Posted byseancostello➡️Why do you think of this as serial combs? That is an intriguing viewpoint, but I don't claim to understand it.Because there is no such thing as a parallel comb in an FDN with a non-trivial mixing matrix.


That is why I am wondering about the discussion of prime numbers and the frequency response of the individual combs (delay lines). That has no meaning in the context of such an FDN.


The variety of paths and hence delay lengths is infinite in the case of a hundred combs. They all couple serially, with very low gain. So because of the low gain over any entire loop, you end up with very shallow peaks, and the number of peaks becomes countless.


Which is all good! You really want flat response unless you don't. Like a small space or some type of Foley matching.


-Casey

---

### Post #787 -- Page 27
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9663903&postcount=787>

Another thing to consider in this regard and this really blows the whole "mode thing" away (if not your mind) is that in an FDN all of the inputs to the combs are also combs.


But... when you prove this, by doing the transform, you notice that all of the peaks have been replaced by valleys and all the valleys by peaks!


So if you have a hundred combs and hence a hundred inputs to those combs, the inputs themselves are, as a whole, a comb as well, but in a feed-forward topology, thereby flipping the peaks and valleys. 


If you really care about adding all these things up (which I don't) you have to account for all of that as well.


Root cause for a good sound can be a bitch to figure and is sometimes best ignored.


-Casey

---

### Post #788 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9664045&postcount=788>

Quote: > Originally Posted byseancostello➡️We're talking a purely hypothetical system here. So it has REALLY good dynamic range.Well, in that case the FDN and the FIR filter won't be identical due to the infinite impulse response of the FDN. For all practical reasons, however, and when you take the limited dynamic range of the human auditory system into account, they will be perceived as identical... ;-)


Stian

---

### Post #789 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9664071&postcount=789>

Quote: > Originally Posted byCasey➡️The variety of paths and hence delay lengths is infinite in the case of a hundred combs. They all couple serially, with very low gain. So because of the low gain over any entire loop, you end up with very shallow peaks, and the number of peaks becomes countless.That made me wonder - does the scattering matrix really increase the density of the resonances? In other words, will you have a larger number of resonances with lets say a Hadamard feedback matrix than with the identity matrix? Intuitively, I would say no, but I might be wrong...


Stian

---

### Post #790 -- Page 27
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9665235&postcount=790>

Quote: > Originally Posted bysaagedal➡️That made me wonder - does the scattering matrix really increase the density of the resonances? In other words, will you have a larger number of resonances with lets say a Hadamard feedback matrix than with the identity matrix? Intuitively, I would say no, but I might be wrong...StianThe scattering matrix won't increase the number of resonances, but it will change the distribution. In general, a good FDN will have a more "randomized" spacing of resonances. The resonance density will be constant for your typical delay based FDN running at a single sampling rate, but the distance between adjacent resonances should be random, in order to avoid the distinctive comb filtering sound.

---

### Post #791 -- Page 27
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9665255&postcount=791>

Quote: > Originally Posted bysaagedal➡️That made me wonder - does the scattering matrix really increase the density of the resonances? In other words, will you have a larger number of resonances with lets say a Hadamard feedback matrix than with the identity matrix? Intuitively, I would say no, but I might be wrong...StianYour intuition is correct. The total number of peaks is limited by the overall delay time in the entire FDN. No magic there. On the other hand, the low frequency response of the system is improved by maximum mixing. So that is sort of magical.


The magnitudes of the peaks will change with additional mixing due to the variety of paths that this enables. Some paths will not have any peaks if they are much longer than RT60. So it becomes impossible to count peaks in something like the proposed 50 second model.



-Casey

---

### Post #792 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9665814&postcount=792>

Quote: > Originally Posted byCasey➡️Your intuition is correct. The total number of peaks is limited by the overall delay time in the entire FDN. No magic there.Thanks for clarifying (also to you, Sean), I misinterpreted your previous post. It's good to hear that my intuition isn't all that off... 


Stian

---

### Post #793 -- Page 27
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9667042&postcount=793>

Quote: > Originally Posted byacreil➡️And I suppose you could also consider a corresponding "echo density of white noise" that you also can't exceed....White noise does not necessarily imply maximum echo density.

---

### Post #794 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9667247&postcount=794>

Quote: > Originally Posted byWarp69➡️White noise does not necessarily imply maximum echo density.Why not? Could you please elaborate? 


Stian

---

### Post #795 -- Page 27
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9668215&postcount=795>

RASI, RTSI and similar noise generators etc. - RTSI also have flatter temporal envelopments (4000+), so they appear more 'smooth' compared to something like Gaussian white noise. Since they are sparse you can heavily optimize your algorithms compared to standard convolution with Gaussian white noise.

---

### Post #796 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9670107&postcount=796>

Quote: > Originally Posted byWarp69➡️RASI, RTSI and similar noise generators etc. - RTSI also have flatter temporal envelopments (4000+), so they appear more 'smooth' compared to something like Gaussian white noise. Since they are sparse you can heavily optimize your algorithms compared to standard convolution with Gaussian white noise.I'm afraid I couldn't quite follow you there. How can you achieve a higher density than white noise? Anyway, thanks for intending to explain... 


Stian

---

### Post #797 -- Page 27
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9670243&postcount=797>

Quote: > Originally Posted bysaagedal➡️How can you achieve a higher density than white noise?There exist algorithms which achieve flat spectral power before they reach maximum echo density - they are sparse but they're still white noise.

[www.relab.dk/downloads/sound/Noise.wav](http://www.relab.dk/downloads/sound/Noise.wav)


First part RTSI noise (7000) and the second part probably what you would call traditional noise based on Gaussian. Both white noise, but the first part appear more 'smooth' than the second part as stated earlier. We can therefor have white noise without maximum echo density.


This leads us to an interesting question : How many impulses/sec are necessary before humans perceive 'maximum' density? Recent studies suggests 4000.

---

### Post #798 -- Page 27
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9670334&postcount=798>

Quote: > Originally Posted byWarp69➡️This leads us to an interesting question : How many impulses/sec are necessary before humans perceive 'maximum' density? Recent studies suggests 4000.If that many.  In the typical case I'd bet it's in the hundreds.  That's mainly why I'v stayed out of this conversation.  I really think that pursuing maximum density is a trip down the rathole, because that's not the way our hearing system works.  We do a pretty decent job of decoding early reflections.  Given the dangers that awaited our distant ancestors, there was a lot of evolutionary pressure to make sure we could tell where sounds were coming from.  But once we reach the point where there's no vector information in the sound--and that comes very quickly--a different part of our auditory cortex takes over.  Just like the visual cortex, the auditory cortex is very good at data reduction.  In the many things necessary to keep an organism alive (and the energy budget required to do so), it's simply not worth trying to decode all that information.  So what do we get out of all those reflections?  We get frequency, loudness and momentary inter-aural differences.  The number of reflections required to create that effect is incidental and I think that information is thrown away (if it's even there) early in the hearing process.

---

### Post #799 -- Page 27
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9670514&postcount=799>

Quote: > Originally Posted byDeleted Nobody Special ➡️If that many.  In the typical case I'd bet it's in the hundreds.The number was for broadband - as an example, it's 1/5 (800+) for lowpass filtered (1.5KHz).

---

### Post #800 -- Page 27
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9670785&postcount=800>

Quote: > Originally Posted bysaagedal➡️I'm afraid I couldn't quite follow you there. How can you achieve a higher density than white noise? Anyway, thanks for intending to explain...Not the ACTUAL echo density, but the PERCEIVED echo density. Or, to be more accurate, the smoothness of the decay with a given echo density.


Google "velvet noise" for more details.

---

### Post #801 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9671354&postcount=801>

Quote: > Originally Posted byseancostello➡️Not the ACTUAL echo density, but the PERCEIVED echo density. Or, to be more accurate, the smoothness of the decay with a given echo density.Google "velvet noise" for more details.That makes sense. The effect is quite interesting. I like the smoothness in the example from Warp69.


Stian

---

### Post #802 -- Page 27
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9705708&postcount=802>

Quote: > Originally Posted byDeleted Nobody Special ➡️If that many.  In the typical case I'd bet it's in the hundreds.  That's mainly why I'v stayed out of this conversation.  I really think that pursuing maximum density is a trip down the rathole, because that's not the way our hearing system works.  We do a pretty decent job of decoding early reflections.  Given the dangers that awaited our distant ancestors, there was a lot of evolutionary pressure to make sure we could tell where sounds were coming from.  But once we reach the point where there's no vector information in the sound--and that comes very quickly--a different part of our auditory cortex takes over.  Just like the visual cortex, the auditory cortex is very good at data reduction.  In the many things necessary to keep an organism alive (and the energy budget required to do so), it's simply not worth trying to decode all that information.  So what do we get out of all those reflections?  We get frequency, loudness and momentary inter-aural differences.  The number of reflections required to create that effect is incidental and I think that information is thrown away (if it's even there) early in the hearing process.As perhaps one of the few contributors to this thread who  makes his primary living by mixing records, I'd like to add that I seldom use reverb in a mix unless I cannot achieve my goals any other way.  My first choice for "ambience" is usually one or two short delays, always with subtle modulation.  The number of times this is referred to as "reverb" by the producer or artist would astonish you.   When I do use reverb it's always my Sony DRE-2000, Lexicon 224 (non x non xl), AMS RMX, or my Ursa Major Space Station.  I find that "modern" reverbs are far too dense to be useful in  any context other than in isolation, particularly the plugin reverbs available today.   As is happens I've done quite a bit of reverb preset programming over the past several decades and it's always been nice to get feedback from real professionals who've used my presets and commented that they were the only useful settings in the box. ( I remember Chuck Ainley saying this to me in the 1990s when, after talking about his Ensoniq DP/2,  I mentioned those were my presets).  


To sum up: Discussing maximum theoretical density is as Deleted Nobody Special  says above, "a trip down the rathole".   The best advice I can offer is to make sure that there are no obvious "tells" in the reverb itself, and above all use your ears (or better yet, enlist a professional to help you to understand obstacles to practical application of your algo and craft it with you).

---

### Post #803 -- Page 27
**User:** Radardoug
**Info:** Joined: Oct 2009Posts: 2,048🎧 15 years | Posts: 2,048
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9707962&postcount=803>

Quote: > Originally Posted byMichael Carnes➡️Unfortunately, the original 224 and PCM70 code was lost long, long ago.N.S.The code is not lost while there is still a machine available. What you mean is the notes to the code. A good programmer with time on his hands could re-create it, but its a fair few hours of work.

I dragged out my 224 last week, sorted the E43 error, and used it on vocals and drums. Ahhhhh.......

Those boys were way clever in their time!

---

### Post #804 -- Page 27
**User:** Deleted Nobody Special Posts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9708621&postcount=804>

Quote: > Originally Posted byRadardoug➡️The code is not lost while there is still a machine available. What you mean is the notes to the code. A good programmer with time on his hands could re-create it, but its a fair few hours of work.I have my doubts about that.  All of that logic, from Lexichips on back, had bugs and all sorts of strange workarounds. I never programmed the 224, but I worked with nearly everything after that. There were operations that were required by a host processor (usually a mighty Z80) that depended on wait-states being fed by the DSP, followed by cycle-counting. There were instruction words that were meaningless and words that didn't do what the microcode would indicate.  There were issues with impedance and tolerance buildups and all sorts of nightmarish situations.  There were never more than 2 or 3 people for a given processor who knew all of the ins and outs.  These things weren't general-purpose processors.  They were devices with serious blemishes that usually took months to characterize.  To say I don't miss them would be an understatement.


A programmer good enough to figure out all of that from a box would have any number of better things to do.

---

### Post #805 -- Page 27
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9709107&postcount=805>

BREAKING NEWS:


Here is is..!!


The August 1979 issue of Recording Engineer - Producer magazine:"Special Emphasis: Reverberation"

[http://www.americanradiohistory.com/...ng-1979-08.pdf](http://www.americanradiohistory.com/Archive-Recording-Engineer/70s/Recording-1979-08.pdf) 


Includes  a great article by David Griesinger starting on page 92.


On page 94 he states:  "Contrary to popular opinion, high diffusion is not always desirable, at least for the first 200ms or so after an impulsive input."

---

### Post #806 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9709374&postcount=806>

Quote: > Originally Posted byzmix➡️On page 94 he states:  "Contrary to popular opinion, high diffusion is not always desirable, at least for the first 200ms or so after an impulsive input."I do think the developers on this thread are aware of this and this is why we have the distinction between early reflections and the late reverberation. In my view it is desirable to have a smooth exponentially decaying dense reverberation tail without any perceivable distinct echoes after the first 100 to 200 ms our auditory system uses to determine the acoustical surroundings. Even for the early reflections, diffusion is desirable to avoid comb filtering effects, and if you look at the impulse response measurement from the real hall in the article, you'll notice that the early reflections are quite diffuse.


I think it is also important to keep in mind that reverberation is a very subjective matter and producers will have different needs depending on musical style and personal gusto. Personally, I'm pursuing a reverberation that is as realistic as possible, and real acoustical spaces tend to be very dense after a short build-up time. If realism is desirable in a specific mix is another question.


Stian

---

### Post #807 -- Page 27
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9709662&postcount=807>

Quote: > Originally Posted byMichael Carnes➡️I have my doubts about that.  All of that logic, from Lexichips on back, had bugs and all sorts of strange workarounds. I never programmed the 224, but I worked with nearly everything after that. There were operations that were required by a host processor (usually a mighty Z80) that depended on wait-states being fed by the DSP, followed by cycle-counting. There were instruction words that were meaningless and words that didn't do what the microcode would indicate.  There were issues with impedance and tolerance buildups and all sorts of nightmarish situations.  There were never more than 2 or 3 people for a given processor who knew all of the ins and outs.  These things weren't general-purpose processors.  They were devices with serious blemishes that usually took months to characterize.  To say I don't miss them would be an understatement.A programmer good enough to figure out all of that from a box would have any number of better things to do.For a while I didn't have better things to do, or probably more likely I wanted to understand how things work. The Lexichips are weird, yes. The 224 processor seemed pretty straightforward, though, and I do have disassembled code (both 8080 and DSP) for the 224, and a pretty decent disassembly of the DSP algorithms for the PCM70, PCM91, and 480L. But don't ask, I can't share those due to lawyers and my conscience. I'm not going to go giving away David's and Michaels' (and others') work. I just wanted to know how it worked. I found the Lexichip (PCM91) a bit more confusing and if I really wanted a good understanding I'd hook up a logic analyzer and a shadow microcode memory to see the fetch in parallel (the fetched microcode bus is not available on a Lexichip). The PCM70, 224, and 480L are pretty straightforward to understand since the microcode sequencer is right in the open for all to see although the interprocessor communication on the 480L is a bit confusing since I don't have a 480L to hook my logic analyzer to it. I do have a PCM70, 91, and 224 so getting those were no big deal. However understanding the algorithm from a reverse engineering aspect is much different than being able to write and test a new algorithm although I'm pretty sure I could figure it out and get it to work. However Michael's estimate is probably right - I would have to spend several months playing with the chip to understand its quirks, and I've got a bit of an advantage over many in that I write embedded code (automotive engine control) for a living so dealing with cycle-counted timings and things like that are already no problem. Most programmers these days have no clue how to do that stuff, but then again, I have no idea how to program a VST plug-in.


But the next question is what do you want to do with that information? Make a plug-in? Clone it? Write new algorithms for ancient hardware? Implement a 224 in an FPGA? You definitely have the timing margins for it now in today's FPGA's.

---

### Post #808 -- Page 27
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9710278&postcount=808>

Quote: > Originally Posted bysaagedal➡️I do think the developers on this thread are aware of this and this is why we have the distinction between early reflections and the late reverberation. In my view it is desirable to have a smooth exponentially decaying dense reverberation tail without any perceivable distinct echoes after the first 100 to 200 ms our auditory system uses to determine the acoustical surroundings. Even for the early reflections, diffusion is desirable to avoid comb filtering effects, and if you look at the impulse response measurement from the real hall in the article, you'll notice that the early reflections are quite diffuse.I think it is also important to keep in mind that reverberation is a very subjective matter and producers will have different needs depending on musical style and personal gusto. Personally, I'm pursuing a reverberation that is as realistic as possible, and real acoustical spaces tend to be very dense after a short build-up time. If realism is desirable in a specific mix is another question.StianSubjective indeed.  One of my favorite comments on the subject of design came from a conversations I had with Casey Dowdell a few years ago when he referred to one of his designs as "an opinion".  Very astute and wise observation.


"Early Reflections" is a semantic construct used in the 1970s to provide a simplified description of the acoustic behavior of an enclosed space, later employed in digital reverberators to allow some control over the proximity of the source and listener, but it's an "engineering driven" pursuit rather than an actual physically distinct phenomenon.   Even David Griesinger  later refuted this model, and as you've pointed out in your message (above) the "ER" components of a room will exhibit diffuse qualities (though technically not the "earliest" reflections).    I would  have hoped that the developers on this thread would have long surpassed the platitudes of theoretical design objectives and branched into more exploratory territory.  In my own reverb designs I've employed none of the standard FDN / Diffusor-delay loops, and yet managed to create an illusion of an interesting space.   Back in the 1990s we used to joke about the various semi-pro reverb algos as "A space you wouldn't want to live in", though it's clear in retrospect that they were largely trying to emulate and what's worse "improve" existing digital reverb topologies.


On the subject of "realism".... I have recorded in (or mixed tracks recorded in) some of the most meticulously constructed acoustical environments know to man, and I will state categorically that comb filtering, lumpy resonances, uneven buildup, uneven decay, distinct echoes and other "undesirable" anomalies are present in every single one.  It's simply a tacit assumption that as an engineer you'll make sense of the space and produce a pleasant or at least useful sound.

---

### Post #809 -- Page 27
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9712226&postcount=809>

Quote: > Originally Posted bysaagedal➡️Personally, I'm pursuing a reverberation that is as realistic as possible, and real acoustical spaces tend to be very dense after a short build-up time.Which characteristics have you found/or believe improve realism in synthetic reverberation? I find this very discussion about realism in reverberation very interesting.

---

### Post #810 -- Page 27
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9719635&postcount=810>

Quote: > Originally Posted byzmix➡️Subjective indeed.  One of my favorite comments on the subject of design came from a conversations I had with Casey Dowdell a few years ago when he referred to one of his designs as "an opinion".  Very astute and wise observation.Yes, definitely a very wise and humble point of view, especially considering how acclaimed his "opinions" are. The M7 is a remarkable unit in my opinion.

Quote: > Originally Posted byzmix➡️"Early Reflections" is a semantic construct used in the 1970s to provide a simplified description of the acoustic behavior of an enclosed space, later employed in digital reverberators to allow some control over the proximity of the source and listener, but it's an "engineering driven" pursuit rather than an actual physically distinct phenomenon. Even David Griesinger  later refuted this model, and as you've pointed out in your message (above) the "ER" components of a room will exhibit diffuse qualities (though technically not the "earliest" reflections).What I tried to say is that the distinction makes sense due to properties of the human auditory system. I never said that it is a physically distinct phenomenon.

Quote: > Originally Posted byzmix➡️I would  have hoped that the developers on this thread would have long surpassed the platitudes of theoretical design objectives and branched into more exploratory territory.  In my own reverb designs I've employed none of the standard FDN / Diffusor-delay loops, and yet managed to create an illusion of an interesting space.Interesting, are these meant for a commercial product or are the ideas behind them something you would want to share?


Stian

