
---

## Page 28

---

### Post #811 -- Page 28
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9719685&postcount=811>

Quote: > Originally Posted byWarp69➡️Which characteristics have you found/or believe improve realism in synthetic reverberation? I find this very discussion about realism in reverberation very interesting.It is indeed a very interesting topic. Personally, I do think density up to the point of "perceived maximum density" is important in the decay phase. I also think the early reflections are important for the illusion of space, but a realistic simulation should also include their diffuse quality in order to reduce comb filter effects.


Stian

---

### Post #812 -- Page 28
**User:** Oden
**Info:** Joined: Apr 2010Posts: 1,141🎧 15 years | Posts: 1,141
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9947180&postcount=812>

Insightful thread, bumping it up once more!


Quote: > Originally Posted byseancostello➡️I am trying to wrap my head around how resonance density balances out with maximum echo density in digital reverbs. Here's the hypothetical situation:You have an LTI digital reverb with 50 seconds of delay time, spaced between a huge number of parallel combs in a feedback delay network (we've got ourselves a fast computer here). Several hundred to a few thousand or so parallel delay lines. The delay lines are perfectly tuned, so the resonance and echo density is smooth as butter. The 50 seconds of delay time gives you 50 resonances per Hertz.Set this hypothetical reverb for a 2 second delay time.Now take an impulse response of the reverb. To get past any frequency domain convolution issues, the impulse response will be realized with a direct form FIR filter. Again, we've got ourselves a fast hypothetical computer.According to convolution theory, the impulse response should perfectly capture the sound of the LTI system. Let's assume that we have a "true stereo" impulse of the huge FDN, with separate impulses for L->L, L->R, R->R, R->L. This would take 8 seconds of delay memory for the FIR filter. Pretty sizable memory savings.DOES the impulse response really capture the sound of the reverb? What happened to the 50 resonances per hertz? The FIR has 0 resonances per hertz. Can you really hear those 50 resonances per hertz in a 2 second decay? Assuming that the raw number crunching issues aren't important, are we wasting the 50 seconds of delay memory in our FDN, if we could get by with 8 seconds using a direct form realization?I'm really confused by the above ideas. Obviously, they relate to capturing the real modal density of a concert hall (which will have billions of discrete resonances, as opposed to the 100*sampling rate resonances of our hypothetical example). It also relates to the general idea of series versus parallel reverberator algorithms, and whether there is an upper limit to the amount of delay memory that can be effectively utilized in an artificial reverberator.I think this was an interesting read and question. I don't think it was ever answered.


My (poor) attempt of an answer, possibly I am missing something :


Yes the IR does capture the resonances perfectly, because obviously 2 second reverb can not ever have 50 resonances per herz, as only frequencies of 0.5hz and it's multiples exist in such signal. In other words, those resonances and frequencies don't exist and are gone the second you shorten the reverb time. Just like the impulse response is drastically shortened.


The IR captures the 2 second reverb perfectly just like it captures the impulse response perfectly. The other frequencies come into play only once you lengthen the time, in which case(if you loop the impulse response), you probably won't get the original 50 second reverb back. Unless it's impulse was the same as the 2 second reverb looped (unlikely).


Which brings us to the answer, in a limited time signal, of course there must be a point where adding more delays does nothing new. Because there are only a limited amount of possible impulse responses! It's kind of like, why use 50 second samples, if there is only 2 seconds of playback in them? By making the frequency domain denser you expand the time domain and vice versa...


Logically thinking about this, the point where nothing new can be added by adding more delay lines is when you have one delay line for each sample in the impulse response. So for 2 seconds worth of reverb that would be 48000*2 for mono signal.... fairly high amount.

---

### Post #813 -- Page 28
**User:** chet.d
**Info:** Joined: Oct 2007Posts: 2,254🎧 15 years | Posts: 2,254
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=9947390&postcount=813>

Had an eye out for a Stargate  for years. Patience paid off a few weeks ago.

I rejoice

---

### Post #814 -- Page 28
**User:** sirhans
**Info:** Joined: May 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10112261&postcount=814>

Hi, I'm looking for information about how to tune delay line lengths to smooth out the frequency response of the reverb tail for an FDN reverb.  I'm just tuning them by ear right now but wondering if there's an automated method or a trick that would offer some guidance to guide the manual tuning in the right direction.


Has anyone read any papers on the subject or do you have any hints to share?


thanks in advance.

---

### Post #815 -- Page 28
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10114253&postcount=815>

Quote: > Originally Posted bysirhans➡️Hi, I'm looking for information about how to tune delay line lengths to smooth out the frequency response of the reverb tail for an FDN reverb.Hi. I think the idea of "tuning the frequency response of the reverb tail" is too vague. I know what you mean. Since that frequency response actually depends on delay interactions, and a similar frequency response (good or bad) can be achieved with configurations that are completely different from each other, it's actually a case where you can't make up rules or directions for achieving a certain (especially a "flat") frequency response unless you don't mind restricting people's options of how they can structure their own delay/feedback network.


For getting a "smooth" (flat) response, I'd say there are basically several ways: 1. ensuring as much difference / spacing between the overall delays as possible throughout the entire process, avoiding harmonic interactions, etc. 2. balancing several (or ideally many) groups of closely spaced delays in such a way that together, they form a smooth response, 3. additionally using filters within the loop, although this is most likely a bad idea since you'd get a weird sound even if the response itself is just right.


It's very complicated and gets exponentially more complicated with bigger and more complex networks. Tweaking only by ear is likely to not even be feasible with a complex design, so you'd have to use some calculations that personally I don't know about. How to actually decide about delay line lengths (for a smooth response) is complicated and individual to your specific case, and I suppose serious designers build their own tools to help them with it, which are specific to their own design/s. Maybe some people have specific values for this, but then you'd have to depend on someone else's structure.

---

### Post #816 -- Page 28
**User:** Oden
**Info:** Joined: Apr 2010Posts: 1,141🎧 15 years | Posts: 1,141
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10115735&postcount=816>

Quote: > Originally Posted byShy➡️Hi. I think the idea of "tuning the frequency response of the reverb tail" is too vague. I know what you mean. Since that frequency response actually depends on delay interactions, and a similar frequency response (good or bad) can be achieved with configurations that are completely different from each other, it's actually a case where you can't make up rules or directions for achieving a certain (especially a "flat") frequency response unless you don't mind restricting people's options of how they can structure their own delay/feedback network.For getting a "smooth" (flat) response, I'd say there are basically several ways: 1. ensuring as much difference / spacing between the overall delays as possible throughout the entire process, avoiding harmonic interactions, etc. 2. balancing several (or ideally many) groups of closely spaced delays in such a way that together, they form a smooth response, 3. additionally using filters within the loop, although this is most likely a bad idea since you'd get a weird sound even if the response itself is just right.It's very complicated and gets exponentially more complicated with bigger and more complex networks. Tweaking only by ear is likely to not even be feasible with a complex design, so you'd have to use some calculations that personally I don't know about. How to actually decide about delay line lengths (for a smooth response) is complicated and individual to your specific case, and I suppose serious designers build their own tools to help them with it, which are specific to their own design/s. Maybe some people have specific values for this, but then you'd have to depend on someone else's structure.

Isn't getting flat frequency response technically really simple though? Just take time period, such as two seconds. And then rise all the FFT bins equally. Now you have a perfectly flat frequency response impulse.


The problems start when you want to convolve the impulse with a signal though. To perform the multiplication you need to add enough zeroes to the signals to be equal length. And then you need to add some more zeroes to not have circular convolution... All that zero padding of course alters the frequency response (and number of FFT bins) significantly.


So I believe only way to have a flat frequency response is to do linear convolution and have a longer impulse than the source material is (thus no more zeroes need to be added to the impulse, but rather the signal, to make then equal length and thus have equal amount of FFT bins to do the multiplication).


This would be a terrible sounding reverb... Or make no sound at all (now that I think about it, I think perfectly flat frequency response impulse is equal to dirac delta, but also white noise with different phase...hmm...).

---

### Post #817 -- Page 28
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10116056&postcount=817>

Quote: > Originally Posted bysirhans➡️Hi, I'm looking for information about how to tune delay line lengths to smooth out the frequency response of the reverb tail for an FDN reverb.You do not mention your choice of mixing matrix. I will assume it is a typical one with maximum mixing.


There are no secrets, just listening and measuring. You need to approximate a flat frequency response by selecting delays which will give you the best modal density when their individual frequency responses are all overlapped.


A simple way to do this is to use prime numbers of samples in your delay lengths. This avoids having repeated modal peaks across your length selections.


Since longer delay lines will have lower modal peaks it is best to keep the ratio of the shortest to longest under 2 to 1.


The range of lengths should be under 120 msecs to assure sufficient echo density. Longer sets (say 60 to 120 msecs) give you a larger range of primes to pick from allowing larger numbers of delay elements. This allows for more modal density but will require the use of a post network allpass or two per channel to enhance the echo density.


Allpasses should be in series only. When using more than one in series I use a length ratio of around 2.85. Tell me where that ratio comes from for a prize.



-Casey

---

### Post #818 -- Page 28
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10116153&postcount=818>

That's some very nice advice but I have to say that regarding the usage of prime numbers, if I restrict my delays according to that, it's apparently impossible to get the kind of spatial image I want. How is it possible to work around this? The ratio of shortest to longest under 2 to 1, I kind of intuitively never considered a larger ratio because it seems crazy , but who knows, maybe something useful is still possible despite seemingly crazy ratios.

---

### Post #819 -- Page 28
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10116329&postcount=819>

Quote: > Originally Posted byShy➡️How is it possible to work around this?Feed Forward architectures combined with very low gain feedback paths.


Feed Forward inverts the modal peaks into modal valleys and low feedback gain minimizes the normal feedback peaks. Instant flatness booster.


Since your frequency peaks are now nice and round instead of pointy it makes little difference if you have some repeated modes in your delay elements.


This comes down to your choice of mixing matrix. Make good choices there, then move on to delay selection.


-Casey

---

### Post #820 -- Page 28
**User:** Shy
**Info:** Joined: Aug 2009Posts: 2,090🎧 15 years | Posts: 2,090
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10116490&postcount=820>

That's a nice idea but the problem with this "instant flatness booster" is that although you can "mask" "peaks" in that way, the overall character of the sound ends up being pretty far from the result you really want and forces you to change the way you mix everything and create more and more indistinct parts to form a distinct and desirable enough result, which really just ends up being insufficient. At least that's how it is for me. Maybe with a complex enough setup, and countless headaches, something good could come out of it, but that's far beyond my capabilities.

---

### Post #821 -- Page 28
**User:** sirhans
**Info:** Joined: May 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10125189&postcount=821>

Thanks Casey, Shy, that information helps.


I'm just using a Hadamard matrix for mixing the feedback.

Quote: > Originally Posted byCasey➡️A simple way to do this is to use prime numbers of samples in your delay lengths. This avoids having repeated modal peaks across your length selections.Using prime numbers seems intuitively reasonable, and the i've got limited very limited processing power so the FDN won't be large enough to prevent me from setting the lengths just by guessing, listening, and measuring.  But it bothers me that there isn't a more automated way to do it.  What happens when the FDN has 32 delays?  Perhaps when the network is really huge, the tuning doesn't have to be so perfect?


I wrote a matlab function that measures the extent to which a set of delays are sharing resonances.  The result is not surprising:

[2-delay plot](http://bluemangoo.com/~hans/coincidentResonances.png)


The plot shows the degree to which resonant modes coincide for a pair of delays, d1 and d2, where d1 is fixed and d2 varies from 1*d1 to 3*d1.  Not surprisingly, it has large peaks where d2=d1, d2=2*d1, and d2=3*d1.  Smaller peaks correspond to d2=1.5*d1, d2=2.5*d1 and so on.  When used for only two delays, there's nothing surprising here; we could easily calculate this information by hand.


It's slightly more interesting when there are two delays d1 and d2, are there with fixed lengths and we vary the length of a third delay d3:

[3-delay plot](http://bluemangoo.com/~hans/coincidentResonances2.png)


With a larger number of delays in the network the peaks get more dense and less easy to predict by hand.  I'm hoping to avoid bad combinations of delay lengths by doing a randomized search for combinations that avoid peaks in the graph.  


I'll try it in my reverb code this week and see how it goes.

---

### Post #822 -- Page 28
**User:** sirhans
**Info:** Joined: May 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10127377&postcount=822>

Quote: > Originally Posted byCasey➡️Allpasses should be in series only. When using more than one in series I use a length ratio of around 2.85. Tell me where that ratio comes from for a prize.Still thinking about this.  


Shroeder's paper suggested prime numbered lengths near a common ratio of 3.  But since there are some pairs of primes that are within 1 sample of a perfect 1:3 ratio, it would be better to avoid using integer ratios entirely.  2.85 is near 3 but even nearer to 20/7, which does a better job of avoiding common factors between the delay lengths.


I suspect the answer you have in mind is still more clever than that though.

---

### Post #823 -- Page 28
**User:** sirhans
**Info:** Joined: May 2014Posts: 4🎧 10 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10127483&postcount=823>

Thanks Casey, Shy, for the info.  That's helpful.

Quote: > Originally Posted byCasey➡️You do not mention your choice of mixing matrix. I will assume it is a typical one with maximum mixing.Yes, i'm just using a Hadamard matrix.

Quote: > Originally Posted byCasey➡️There are no secrets, just listening and measuring. You need to approximate a flat frequency response by selecting delays which will give you the best modal density when their individual frequency responses are all overlapped.A simple way to do this is to use prime numbers of samples in your delay lengths. This avoids having repeated modal peaks across your length selections.It seems that just using primes wouldn't completely avoid problems with modal peaks coinciding.  4441 and 6661, for example, are prime but since 4441*1.5 is nearly equal to 6661 I'd still expect those two numbers to be bad choices. I'm wondering if this kind of intuition can't be automated some how into an algorithm that automatically finds good sets of delay times.


I wrote something in matlab that measures the distances between the modes of resonance of a set of delay lines and automatically searches for a set of delay times that keep the modes spread apart.  I don't like the results yet.  I'll keep working on it and if it's not better than what I get by just listening, I'll take your advice and just do it by ear.

---

### Post #824 -- Page 28
**User:** jngpng
**Info:** Joined: Aug 2009Posts: 11🎧 15 years | Posts: 11
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10378308&postcount=824>

Thanks for this thread guys. A lot of interesting material here. Thought I'd finally chime in because Casey's question caught my interest.

Quote: > Originally Posted byCasey➡️Allpasses should be in series only. When using more than one in series I use a length ratio of around 2.85. Tell me where that ratio comes from for a prize.-CaseyMy best guess is that you choose this ratio because it's equivalent to tuning the ringing frequencies of the allpasses to an interval of 1 octave + a tritone. Not a bad choice if you want to maximise the perceived dissonance/noisyiness of the response...

---

### Post #825 -- Page 28
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=10388169&postcount=825>

Has anyone ever heard one?

![](https://static.gearspace.com/util/imgext.php?u=http%3A%2F%2Fwww.electricalaudio.com%2Fitem.php%3Fpage%3D258%26amp%3Bpic%3Dpictures%2F258-0.jpg&h=0dac91d979fe5b70784c448bf705a806)

---

### Post #826 -- Page 28
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11072202&postcount=826>

I have a question about convolution that I was hoping one of the more interested parties here could explain.  


When I perform a swept sine wave convolution to a spring reverb, there is an additional initial "spike" in the resulting convolved impulse, though there is no direct path in the device, the output is taken directly from the tank's output transducer. (see below).


If I use a single sample pulse to excite the reverb, there is no such initial spike.


What could be causing the swept sine convolution process to generate this initial spike?

---

### Post #827 -- Page 28
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11126754&postcount=827>

Quote: > Originally Posted byzmix➡️What could be causing the swept sine convolution process to generate this initial spike?Depending on how you're doing the sine sweep, it could be a result of distortion. IIRC a rising exponential sine sweep can give individual pre-echoes for each harmonic produced by the distortion.  


It's in some paper by Angelo Farina, but I don't feel like finding it.

---

### Post #828 -- Page 28
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11126858&postcount=828>

Quote: > Originally Posted byacreil➡️Depending on how you're doing the sine sweep, it could be a result of distortion. IIRC a rising exponential sine sweep can give individual pre-echoes for each harmonic produced by the distortion.It's in some paper by Angelo Farina, but I don't feel like finding it.Thank you so much, I think I've found it:

[http://pcfarina.eng.unipr.it/Public/...226-AES122.pdf](http://pcfarina.eng.unipr.it/Public/Papers/226-AES122.pdf)


"Quote: > it was recognized the need of further perfecting the measurement technique for dealing with some problems.- pre-ringing at low frequency before the arrival of the direct sound pulse- sensitivity to abrupt pulsive noises during the measurement- skewing of the measured impulse response when the playback and recording digital clocks were mismatched- cancellation of the high frequencies in the late part of the tail when performing synchronous averaging- time-smearing of the impulse response when amplitude-based pre-equalization of the test signal was employed"

---

### Post #829 -- Page 28
**User:** wschira
**Info:** Joined: Nov 2015Posts: 5🎧 10 years | Posts: 5
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11515468&postcount=829>

Hello all,


I' m new in the forum. I have introduced myself already on the top level, but as I'm mostly interested in the reverb forum, I will it do here again.

My name is Wolfgang Schira, I'm electronic engineer with special background FPGA- and ASIC design. I' m German, located in France near the German border.


I have also some question to the forum (hope it's not to fast, but live is short. I'm searching for the structure (and more) of the EMT250, as I want to build a feasibility study to rebuild it as stand alone hardware version. I found on the eventide forum @
[Froombosch](https://gearspace.com/board/member.php?u=4593)
 and contacted him as he started a few years ago to put some information about the subject in this forum. He introduced himself as Harrie Munnik. He was very kind, but he wouldn' t ( or better said couldn't) reveal a lot, as he wants to protect his IP (which was also build with the help of this forum and Dr. Blesser as he told to me.) I can understand this. Neverthless he gave me the contact to gearslutz and some hints which let me come to the conclusion, that the EMT250 is somewhat (or quite) different from that what was documented in the patent 4,181,820.

I also contacted Dr. Blesser without hope to get some help as I know, he's consulted UAD to build there EMT250 plugin. And so arrived it, he clammed up.

All information and help from the forum is very appreciated. I'm mostly interested in structure diagrams like these into the patent, but showing the structure of the real 250.

I will also screen the forum as I think there is already some information.

---

### Post #830 -- Page 28
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11515494&postcount=830>

Welcome to the forum and this exciting topic.


I'm unsure if any of us can help you very much at this point, but I believe there's a promotional video from UA that actually have the structure displayed. The various coefficients was not present, I think, so you would have to get hold of them somehow.


Maybe someone is able to answer specific questions.

---

### Post #831 -- Page 28
**User:** wschira
**Info:** Joined: Nov 2015Posts: 5🎧 10 years | Posts: 5
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11518760&postcount=831>

I heard from this promo video, Harrie Munnik spoke about. But I didn't find it anywhere. I mean I had read in the forum that it is removed from the UAD site.

---

### Post #832 -- Page 28
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11518827&postcount=832>

Quote: > Originally Posted bywschira➡️I heard from this promo video, Harrie Munnik spoke about. But I didn't find it anywhere. I mean I had read in the forum that it is removed from the UAD site.[https://youtu.be/KgaSwmE9AnY?t=151](https://youtu.be/KgaSwmE9AnY?t=151)

---

### Post #833 -- Page 28
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11518994&postcount=833>

You'll will get very close by just setting up 3 loops with 3 taps each. Of the 9 taps, split them 4 and 5 across left / right, then sum them for final l and r output paths.


The feedback stays in each loop and has a one pole hp and one pole lp as well as attenuation. Each loop should be a different size. Try sizes of between 150 and 300 milliseconds of delay. Note there is no allpass in the feedback path.


Put a pair of allpasses on each of the left and right final output paths. The allpass sizes of each pair should be one small and one large in a ratio of around 2.7. They should be small then large on the left and large then small on the right. You can make them 2 or 3% different in size left vs right. The overall size of the allpasses should be such that they "fill in" the space between the main taps (consider their nominal static locations for this.) The allpass gains will be between 0.5 and 0.75. All slightly different.


Dynamically randomize the location of the 9 taps by raising and lowering them in different locations. To assure constant power, use a sin function when raising and lowering the taps. A tap should go from full on to full off to full on again in 500 to 600 milliseconds. Of course move the tap when it is fully off and within a total range of 5 to 15 milliseconds of delay. 


Coordinate the raising and lowering of the taps such that the 4 taps going left are 22.5 degrees in respective phase and the 5 taps going right are at 18, when considering the sin function running in a 90 degree range.


Get the UAD version and just play around and dial in the sound. You can measure any early reflections, as they would be static. Note that they may go through the allpasses, not sure.


Others have said there is more to it than that but this is my rough understanding of it.


Good luck!


-Casey

---

### Post #834 -- Page 28
**User:** wschira
**Info:** Joined: Nov 2015Posts: 5🎧 10 years | Posts: 5
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11528249&postcount=834>

Hi Casey,


Thank you for your suggestions. I have also collected some others and the puzzle get clearer and clearer.


Have a good time!

---

### Post #835 -- Page 28
**User:** wschira
**Info:** Joined: Nov 2015Posts: 5🎧 10 years | Posts: 5
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11528253&postcount=835>

Hallo Sean


many thanks for the link.


greetings

Wolfgang

---

### Post #836 -- Page 28
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11588334&postcount=836>

Here's a great idea for tuning a new reverb algo, let the public do all your listening tests for you and submit their favorite settings:

[Protoverb 1.0](https://www.u-he.com/cms/179-protoverb)


Quote: > u-he.comProtoverb 1.0Michael PettitDetailsCreated on Tuesday, 15 December 2015 10:37ProtoverbProtoverb is an experimental reverb based on the idea of a "room simulator". Most algorithmic reverbs try to avoid resonances or model the reflections of sound from a rooms walls. Protoverb does the opposite. It builds up as many room resonances as possible, modeling the body of air in the room. It therefore does not need to modulate or colour the signal. The result is a very natural sounding reverbration with some interesting features: Long standing frequencies resonate louder, as if the air takes some time to get excited. Multiple instruments don't mash into a diffuse mud, they stay distinct. If you play a short melody, the room seems to repeat a ghost echo of that melody. Those properties are indeed found in churches and large halls, but they're rarely found in conventional algorithmic reverbs.However...To achieve this kind of stuff, Protoverb works with loads and loads of parallel, serial and networked delays. By all means, there is no mathematical formula that makes such a structure sound "just right". As with all delay based reverbs, it's down to trial and error, and maybe a lot of luck with random values. Therefore we designed Protoverb to present you with delay lines of random lengths and a random assembly of networking and feedback strategies. Which, if you're lucky and you come across a great setting, you can submit to our website, along with a few detailsPush buttons to randomize!To be precise, the small text box at the bottom contains two random entries. The first part depicts the network structure, strategies for a spatial layout and distribution of delay taps, strategies for finding useful delay lengths and so on. The second part is a seed for a pseudo-random number generator which is used to find various parameters, such as average delay length, which prime number to chose (if any) and so on. This text can either be edited by double click, or both parts can be independently randomized with the two random buttons below.Get Protoverb - it's free!In other words: Protoverb is a data mining concept. Instead of spending a few months ourselves, we hope that our community will come up with great settings. As a reward, this plug-in is free, people are encouraged to share their settings and thoughts on the internet, and at some point we'll draw some prizes (details to be announced in January 2016) from the submissions (we'll always draw the first entry of equal submissions, so you can share without fear!)Download Protoverb 1.0 Mac (AAX, AU & VST2)Download Protoverb 1.0 Win (AAX & VST2)Download Protoverb 1.0 Linux (VST2)Enjoy, Happy Holidays and have a great start into 2016- Urs & teamNewsletterGet all the u-he news, updates and goodies when you join the u-he newsletter. Just enter your email address below and hit the button!

---

### Post #837 -- Page 28
**User:** johnbruner
**Info:** Joined: Feb 2015Posts: 530🎧 10 years | Posts: 530
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11665404&postcount=837>

Quote: > Originally Posted byseancostello➡️Quote:Originally Posted byRadardoug➡️If you take a tuned filter, and excite it with a frequency not quite on the resonant frequency of the filter, you will get output at the filter frequency.There is a hall here in New Zealand (Michael Fowler Centre) that exhibits this phenomenom.And my bathroom does it well....A good hall can be viewed as having a few BILLION of those resonant filters in parallel.... A smaller hall, or a poorly designed/executed hall, one or more of the low resonances might be isolated enough that it causes audible pitch shifts.If you have a good random distribution of these resonances, with consistent ring times for each of them, a given sine wave input will ring several resonances at once. This produces a signal that is best described as the input sine wave, decaying away, but with a very bumpy amplitude envelope.....How would an LTI system shift any energy from an input-frequency to a different frequency at output? Isn't that something LTI systems never do? Are you talking about non-LTI filters here?

---

### Post #838 -- Page 28
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11675456&postcount=838>

Quote: > Originally Posted byjohnbruner➡️How would an LTI system shift any energy from an input-frequency to a different frequency at output? Isn't that something LTI systems never do? Are you talking about non-LTI filters here?A sine tone only contains at one exact frequency if its duration is infinite. A transient or tone burst will always have components at a variety of frequencies. An LTI reverb fed a sine tone, *during steady state conditions*, will have only a single sinusoidal component at its output, but a tone burst will excite a number of different resonant modes which will beat against each other. If there's not adequate modal density, and the frequency of the tone doesn't coincide with one of the resonant modes, it will seem to change the pitch.


It's like a poorly designed speaker or a small, poorly treated room having a boomy, "one note" quality to the bass, or a comb filter with a lot of feedback. There doesn't have to be any non-LTI behavior for this to happen.

---

### Post #839 -- Page 28
**User:** johnbruner
**Info:** Joined: Feb 2015Posts: 530🎧 10 years | Posts: 530
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11675489&postcount=839>

Quote: > Originally Posted byacreil➡️A sine tone only contains at one exact frequency if its duration is infinite. A transient or tone burst will always have components at a variety of frequencies. An LTI reverb fed a sine tone,during steady state conditions, will have only a single sinusoidal component at its output, but a tone burst will excite a number of different resonant modes which will beat against each other. If there's not adequate modal density, and the frequency of the tone doesn't coincide with one of the resonant modes, it will seem to change the pitch.It's like a poorly designed speaker or a small, poorly treated room having a boomy, "one note" quality to the bass, or a comb filter with a lot of feedback. There doesn't have to be any non-LTI behavior for this to happen.Thanks. Can you recommend a source(s) where I can read more about this math? I have:


- Bracewell, The Fourier Transform & Its Applications

- Oppenheim and Willsky, Signals and Systems

- Oppenheim and Schafer, Discrete-Time Signal Processing


but I haven't mastered their contents by any stretch. If this is covered in those texts, I haven't gotten to that part yet.

---

### Post #840 -- Page 28
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11677034&postcount=840>

Quote: > Originally Posted byjohnbruner➡️Thanks. Can you recommend a source(s) where I can read more about this math? I have:- Bracewell, The Fourier Transform & Its Applications- Oppenheim and Willsky, Signals and Systems- Oppenheim and Schafer, Discrete-Time Signal Processingbut I haven't mastered their contents by any stretch. If this is covered in those texts, I haven't gotten to that part yet.I don't think anything I said is beyond the scope of those books. Basically, multiplication in time domain is equivalent to convolution in frequency domain. So every time you use an envelope to control an oscillator's amplitude, this introduces things that aren't in the oscillator's spectrum.


---

## Page 29

---

### Post #841 -- Page 29
**User:** johnbruner
**Info:** Joined: Feb 2015Posts: 530🎧 10 years | Posts: 530
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=11677168&postcount=841>

Quote: > Originally Posted byacreil➡️I don't think anything I said is beyond the scope of those books. Basically, multiplication in time domain is equivalent to convolution in frequency domain. So every time you use an envelope to control an oscillator's amplitude, this introduces things that aren't in the oscillator's spectrum.Thanks again.

---

### Post #842 -- Page 29
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12050199&postcount=842>

Quote: > Originally Posted byShy➡️That's a nice idea but the problem with this "instant flatness booster" is that although you can "mask" "peaks" in that way,That and that you can use the resulting valleys to eliminate your in-loop allpass ringing.



-Casey

---

### Post #843 -- Page 29
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12108217&postcount=843>

Here is an interesting paper about creating a "modal" artificial reverb using tuned resonant  filters....

[https://www.academia.edu/27559433/Mo...newheel_Organs](https://www.academia.edu/27559433/Modal_Processor_Effects_Inspired_by_Hammond_Tonewheel_Organs)

Quote: > Since each mode of the modal reverberator is a narrow bandpass ﬁlter, a sufﬁcient frequencydensity of modes is required to support typical wideband musical signals. In particular, unless eachfrequency component of the input is sufﬁciently close to a mode center, it may not contribute audibly tothe output.Audio examples here:

[https://ccrma.stanford.edu/~kwerner/...mmondizer.html](https://ccrma.stanford.edu/~kwerner/appliedsciences/hammondizer.html)

---

### Post #844 -- Page 29
**User:** miscend
**Info:** Joined: Jul 2009Posts: 4,289My Studio🎧 15 years | Posts: 4,289My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12338385&postcount=844>

Quote: > Originally Posted byzmix➡️Here is an interesting paper about creating a "modal" artificial reverb using tuned resonant  filters....https://www.academia.edu/27559433/Mo...newheel_OrgansAudio examples here:https://ccrma.stanford.edu/~kwerner/...mmondizer.html

Does it sound better than the Bricasti?

---

### Post #845 -- Page 29
**User:** jupiter8
**Info:** Joined: Feb 2006Posts: 2,192🎧 20 years | Posts: 2,192
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12340848&postcount=845>

Quote: > Originally Posted byzmix➡️Here is an interesting paper about creating a "modal" artificial reverb using tuned resonant  filters....https://www.academia.edu/27559433/Mo...newheel_OrgansAudio examples here:https://ccrma.stanford.edu/~kwerner/...mmondizer.htmlIsn't that kinda how the Zynaptiq Adaptiverb works ?

---

### Post #846 -- Page 29
**User:** Stolle
**Info:** Joined: Sep 2009Posts: 230🎧 15 years | Posts: 230
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12529725&postcount=846>

The Exponential audio R4, hall2 algorithm has density modulation. Is that a first or has that appeared in any other reverbs?

---

### Post #847 -- Page 29
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12530582&postcount=847>

Not that I am aware of. 


I can imagine modulating the gain of allpass filters outside of the feedback path or adjusting tap density coming out of the feedback path. This would presume a constant density design that sets a base line density and then modulates it. 


Alternatively, I can imagine modulating the gain of allpass filters inside the feedback path or modulating the feedback in an FDN design to reduce/increase mixing in non constant density designs. 


My first thought was that modulating a normally constant density design with a fixed density baseline might be more interesting than doing the same in a design that has exponentially increasing density. But in this latter case you would be modulating density growth which also seems interesting on reflection. 


-Casey

---

### Post #848 -- Page 29
**User:** Warp69
**Info:** Joined: Sep 2004Posts: 714🎧 20 years | Posts: 714
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12530623&postcount=848>

Quote: > Originally Posted byCasey➡️modulating the gain of allpass filters inside the feedback pathThis is how some of the algorithms (Plate etc.) works in the Lexicon PCM91 - which is also done by Michael.

---

### Post #849 -- Page 29
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12531555&postcount=849>

Quote: > Originally Posted byCasey➡️Not that I am aware of.I can imagine modulating the gain of allpass filters outside of the feedback path or adjusting tap density coming out of the feedback path. This would presume a constant density design that sets a base line density and then modulates it.Alternatively, I can imagine modulating the gain of allpass filters inside the feedback path or modulating the feedback in an FDN design to reduce/increase mixing in non constant density designs.My first thought was that modulating a normally constant density design with a fixed density baseline might be more interesting than doing the same in a design that has exponentially increasing density. But in this latter case you would be modulating density growth which also seems interesting on reflection.-CaseyModulating allpass filter gains, or modulating FDN matrices in a unitary manner, has certainly been done before (I know that Casey knows this, but just quoting his post for the sake of the thread):

[http://ant-s4.unibw-hamburg.de/dafx/...pers/lokki.pdf](http://ant-s4.unibw-hamburg.de/dafx/paper-archive/2001/papers/lokki.pdf) (modulating allpass coefficients)

[https://www.audiolabs-erlangen.de/co...hlecht2015.pdf](https://www.audiolabs-erlangen.de/content/05-fau/professor/00-habets/03-publications/Schlecht2015.pdf) (modulating feedback matrices)

[https://www.google.com/patents/US7062337](https://www.google.com/patents/US7062337) (modulating feedback matrices)


Similar techniques have also been used in the industry for several decades now.


In the versions that I know of, the AP gains or FDN matrix coefficients are usually changed in a "balanced" manner. In other words, while one part of the network has increasing gains / scattering coefficients, another part has decreasing gains / scattering coefficients. This results in a constant-ish rate of increasing echo density throughout the network as a whole, while individual parts of the network might have lower or higher densities at a given snapshot in time.

---

### Post #850 -- Page 29
**User:** uCjr
**Info:** Joined: Aug 2012Posts: 22🎧 10 years | Posts: 22
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12543510&postcount=850>

This thread is incredibly informative. I would like to thank everyone who has contributed to it so far. Some of the posts are years old, however, so I did want to ask about the state of things right this second. 


I'm looking to get into some audio programming to support a friend who makes pedals. Where should I start? Is it still worthwhile to study DSP chips like the Blackfins, or are general processors getting fast enough? I know you can get small DIP ARM chips now. Also, does DSP chip learning transfer to other things or is there a lot of specific knowledge. I've done some assembly coding and I do not fear it. 


Thanks in advance for any responses.

---

### Post #851 -- Page 29
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12543648&postcount=851>

As you have seen in this thread, algorithms can be executed with very few cycles if need be. I would use the DSP that fit the cost, power and cooling budget of the pedal being developed. 


If an ARM chip fits best that will work just fine as well. 


You can develop in C or C++ for the most part and then use language intrinsics or assembly in the most performance critical sections. 


Look for good DMA functionality as much as anything. This will allow you to move data towards the CPU while your code is crunching numbers. That saves time waiting on slower external memory. All DSPs will have this. 


Coding is coding. If your next project is writing in Swift for iOS you will still be gaining knowledge working on pedals. 



-Casey

---

### Post #852 -- Page 29
**User:** AleLab
**Info:** Joined: Jun 2016Posts: 125My Studio🎧 5 years | Posts: 125My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12674636&postcount=852>

Quote: > Originally Posted byDeleted ab87343➡️If that many.  In the typical case I'd bet it's in the hundreds.  That's mainly why I'v stayed out of this conversation.  I really think that pursuing maximum density is a trip down the rathole, because that's not the way our hearing system works.  We do a pretty decent job of decoding early reflections.  Given the dangers that awaited our distant ancestors, there was a lot of evolutionary pressure to make sure we could tell where sounds were coming from.  But once we reach the point where there's no vector information in the sound--and that comes very quickly--a different part of our auditory cortex takes over.  Just like the visual cortex, the auditory cortex is very good at data reduction.  In the many things necessary to keep an organism alive (and the energy budget required to do so), it's simply not worth trying to decode all that information.  So what do we get out of all those reflections?  We get frequency, loudness and momentary inter-aural differences.  The number of reflections required to create that effect is incidental and I think that information is thrown away (if it's even there) early in the hearing process.I've been reading the entire thread. To me that is very important information. Have you some resources behind that affirmation?

---

### Post #853 -- Page 29
**User:** FETHead
**Info:** Joined: Oct 2008Posts: 26🎧 15 years | Posts: 26
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12776046&postcount=853>

Quote: > Originally Posted byseancostello➡️Hi all,Dropping some reverb science about allpass filters and the ubiquitous Diffusion control:Reverbs: Diffusion, allpass delays, and metallic artifacts « The Halls of ValhallaDig your blog! And would just like to add that Yamaha was modulating allpass coefficients(not delay) already way back in 1982 (US4472993). It won't cure the metallic nature, but could in theory improve the periodicity thereof. 


Currently trying to wrap my head around constant density types...there doesn't seem to be many options available beyond modified-Schroeder's parallel loops(ignoring input/output modifiers), all the classic 'tricks' increase density with time. If you could have enough distributed taps via brute-force tapped-FIR, lets say 1000 taps over time x, like 2 seconds, the problem becomes damping. Let's say you have damping every 100 taps, the damping would sound steppy, especially when it crosses the 5kHz to 3kHz region. And don't think the old DSPs had enough juice to pull that off in any way. Any ideas?


*Edit: It seems the Yamaha allpass has only a 1 sample delay, so it's akin to placing a 100% wet phaser before the reverb...

---

### Post #854 -- Page 29
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12776870&postcount=854>

Quote: > Originally Posted byFETHead➡️Dig your blog! And would just like to add that Yamaha was modulating allpass coefficients(not delay) already way back in 1982 (US4472993). It won't cure the metallic nature, but could in theory improve the periodicity thereof.I wouldn't necessarily draw any conclusions from that. Yamaha patented an enormous number of things that were never commercialized. And while some of the synthesis patents obviously describe specific products in considerable detail, the reverb/effect patents are generally vague and don't seem to reveal anything particularly informative. 


I think the only early Yamaha reverbs that use modulation are the REV1 and REV5. The REV5 seems to apply periodic modulation to the output taps.

Quote: > Currently trying to wrap my head around constant density types...there doesn't seem to be many options available beyond modified-Schroeder's parallel loops(ignoring input/output modifiers), all the classic 'tricks' increase density with time.It's basically different combinations of comb filters, allpasses and multitap delays. A lot of the better ones make good use of early reflections. Some do relatively unorthodox things, like putting comb filters and multitap delays in series. This makes the frequency response more uneven, but it also increases echo density a lot.

---

### Post #855 -- Page 29
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12827726&postcount=855>

Interesting approach to physical modeling and avoiding “numerical dispersion” artifacts, which I had never heard of until reading this..


[NESS - Next Generation Sound Synthesis](http://www.ness.music.ed.ac.uk/archives/systems/virtual-room-acoustics)


The result of this research has been implemented in this "Dynamic Plate" reverb plugin, it's not bad:

[https://physicalaudio.co.uk/PA1.html](https://physicalaudio.co.uk/PA1.html)


And here is a description of a "Switched Convolution" reverb (I believe this is now used in a commercial product):

[https://ccrma.stanford.edu/~keunsup/screverb.html](https://ccrma.stanford.edu/~keunsup/screverb.html)


More details about implementation:

[https://ccrma.stanford.edu/~keunsup/approx_reverb.html](https://ccrma.stanford.edu/~keunsup/approx_reverb.html)

---

### Post #856 -- Page 29
**User:** miscend
**Info:** Joined: Jul 2009Posts: 4,289My Studio🎧 15 years | Posts: 4,289My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12828103&postcount=856>

That's an interesting plate reverb. I hope they develop it into a series of algorithms.

---

### Post #857 -- Page 29
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12845003&postcount=857>

Hello gentlemen..


Oddball question for you.. somewhat reverb related...!


I need some MIDI / Sysex help.. I think I've reduced question to the simplest form possible, so if you know  anyone who might have any insights I'd appreciate the advice:


I’m trying to learn how to send a Sysex string to my Lexicon PCM-70 properly.


I have two different apps here that can transmit Sysex via faders and buttons, I just need to understand the syntax to type in the string of Hex numbers.


This is the description of the Sysex format in the Lexicon PCM-70 manual on page 6-4 section B: “Parameter Data”


(hex)


F0 Sysex ID

06 Lexicon

00 PCM 70


(bin)


oo1o nnnn n=MIDI chaneels 0-15 (0=channel 1)

oggg gggg g=parameter number # 0-89 (table 1)*


*[note: Table 1 states that for Parameter number has a range of 0 to 59, this number corresponds to (10* row) + column. 

The PCM 70 has 10 buttons on the front panel, labeled 0 through 9 and using the up and down arrows selects a row from 0 to 5. The “mix” parameter is in row 0, column 0]


oooo ovvv v=parameter value - 10 bits; MSB sent first (see table for parameter limits)

ovvv vvvv


(hex)


F7 end of Sysex


In the concert hall algo, the mix parameter is described as:


Row number 0, 

Byte 47, 48

Parameter number 0

Minimum Value 462

Maximum value 562

and a display value from 0-100%


2 byte words are in the following form:


Byte

0 dddd dddd Low 8 Bits

1 0000 00dd High 2bits


My question is:


How do I format those numbers to send that as a string of sysex, and allow the value to be changed by a fader object?

---

### Post #858 -- Page 29
**User:** oldgearguy
**Info:** Joined: Sep 2002Posts: 5,007🎧 20 years | Posts: 5,007
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12845940&postcount=858>

First, try to get a static string to change the value.


(all number below in hex.  If you're using MIDI-Ox or similar to send the test data, you may need to preface each byte with 0x -- not in front of my music computers to check this at the moment).


F0 06 00 20 00 03 4E F7  (sets the Mix to 0% on MIDI channel 1)

F0 06 00 20 00 04 32 F7 (sets the Mix to 100% on MIDI channel 1)


The 4th byte (in the above = 20) sets the MIDI channel using the bottom 4 bits.

So in binary:  0 0 1 0 x x x x  (0010 = 2 and the 0000 through 1111 for MIDI channel number-1)


The next byte is the parameter number (in the above 00).  This is the Mix parameter (#0) in Table 7 for Concert Hall data.  This is a straight translation of the parameter # from decimal to hex.  No magic required.


The difficulty comes with the next 2 bytes.  Parameter data is up to 10 bits of information.  MIDI only lets you use 7 bits per byte for regular data (the 8th - high bit is used to indicate special things).


So, for a mix setting of 0%, according to the table you need to send the decimal number 462.

[Square brackets indicate a byte of data]


462 decimal = 01CE hex.

01CE hex = [0000 0001] [1100 1110] binary.  I grouped this in the traditional way for the first step.


Lexicon only uses the lower 10 bits, and remember, MIDI only lets you have 7 bits per byte, so the binary is now grouped like this:


[0000 0011]  [x100 1110]  (where x is the high bit and must always be 0 for data bytes).


We have to send the high bits first then the low bits, so that translates into


03

4E


Hope that helps.  Feel free to ask any questions.


Getting the values to change via a slider will involve mapping the 0-127 (or whatever the slider normally generates) into 462->562 and then converting before sending it out.  That will be a follow-up post later today/tomorrow if needed.


(back in the late 80's/early 90's I wrote a DOS-based editor for the LXP-5)

---

### Post #859 -- Page 29
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12846306&postcount=859>

Quote: > Originally Posted byoldgearguy➡️--//--snip--//--Hope that helps.  Feel free to ask any questions.---//snip--//--(back in the late 80's/early 90's I wrote a DOS-based editor for the LXP-5)

Thank you so much, this is exactly what I needed to see.. I managed to get all 28 parameters mapped to sysex controls, value ranges and all, now I need to figure out how to switch algos (and repeat this for each one), display parameter names and scaled values, all the icing on the cake, but so happy to have been able to get this to work.. thanks so much.


PS: I had an LXP-5 in the early 90s, nice box, I think there were 2 8080 (or Z80?) processors in there.. plagued by encoder issues, though.. and once an encoder was moved (by a puff of wind, for example) the unit would reset..


LXP-15 had better encoders but the parameter scaling was from hell, you would need to rotate the encoder 7200˚ to change a parameter by 1 ms (slight exaggeration, but not much)

---

### Post #860 -- Page 29
**User:** oldgearguy
**Info:** Joined: Sep 2002Posts: 5,007🎧 20 years | Posts: 5,007
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12846507&postcount=860>

Quote: > Originally Posted byzmix➡️Thank you so much, this is exactly what I needed to see.. I managed to get all 28 parameters mapped to sysex controls, value ranges and all, now I need to figure out how to switch algos (and repeat this for each one), display parameter names and scaled values, all the icing on the cake, but so happy to have been able to get this to work.. thanks so much.PS: I had an LXP-5 in the early 90s, nice box, I think there were 2 8080 (or Z80?) processors in there.. plagued by encoder issues, though.. and once an encoder was moved (by a puff of wind, for example) the unit would reset..LXP-15 had better encoders but the parameter scaling was from hell, you would need to rotate the encoder 7200˚ to change a parameter by 1 ms (slight exaggeration, but not much)Excellent - glad I was able to help.  I spend far too much time looking at MIDI hex dumps versus actually using the gear around me.


I stepped up from the LXP-5 to a used 224 that was going fairly cheaply in the early 90's.  The UI was much better.

---

### Post #861 -- Page 29
**User:** gordbort
**Info:** Joined: Feb 2012Posts: 11🎧 10 years | Posts: 11
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12862724&postcount=861>

Quote: > Originally Posted byCasey➡️Let's build a simple little reverb from scratch,...Hi, I'm an ECE student currently in a computer design class working with FPGAs. The final project is to design a CPU and assembly instruction set, and run some sort of program on it. I'd like to do a reverb. I've skimmed over this thread and there is a ton of terrific info in it. But from a processing core perspective, what sort of assembly instructions would be desirable for a reverb developer? EG. If I can get the core to do X in minimal clock cycles, what sort of things would X be? Sine function? Log function? Random number generator? Really try to get my multiplier fast? Huge memory read? 


Right now I'm less concerned with the reverb implementation and more concerned with the implementation of cpu instructions that will facilitate the reverb implementation. So for those of you who have worked with various DSPs, are there instructions that you wish you had when developing reverbs?


For the curious, we're working with these boards: [Nexys 3 Spartan-6 FPGA Trainer Board (LIMITED TIME) - Digilent](http://store.digilentinc.com/nexys-3-spartan-6-fpga-trainer-board-limited-time-see-nexys4-ddr/)

---

### Post #862 -- Page 29
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12862811&postcount=862>

Quote: > Originally Posted bygordbort➡️Hi, I'm an ECE student currently in a computer design class working with FPGAs. The final project is to design a CPU and assembly instruction set, and run some sort of program on it. I'd like to do a reverb. I've skimmed over this thread and there is a ton of terrific info in it. But from a processing core perspective, what sort of assembly instructions would be desirable for a reverb developer? EG. If I can get the core to do X in minimal clock cycles, what sort of things would X be? Sine function? Log function? Random number generator? Really try to get my multiplier fast? Huge memory read?Like any DSP it's mainly multiply and accumulate instructions that are most important. These are needed for scaling delay taps, filtering, interpolation, etc. Ideally this should take one clock. Automatically generating memory addresses would be a good idea too.


If you look up the service manual for the Yamaha SPX90 there's a nice block diagram (attached) depicting the YM3804 DSP and YM3807 MOD ICs. The reverb isn't very good because there's only about 524 ms total delay time (16k / 31.25 kHz) and only 32 total memory reads or writes per sample. I'd say you should at the very least double both of those for a bare minimum decent quality reverb. But the nice thing here is the YM3807 MOD IC. This is basically a 16 channel oscillator with an independent rate and 4k x 32 bit waveform per channel. It's obvious from the diagram that these oscillators add offsets to the memory read addresses and amplitude coefficients, thus enabling modulation effects. The advantage here is that there are 16 channels of modulation with no CPU overhead; similar effect processors at the time used a microprocessor to generate the modulation signals by continuously writing to the DSP instruction memory. This is okay but limited by the speed of the microprocessor. If you do it in hardware like this you can modulate more things at once.


The Klark Teknik DN 780 service manual is a nice reference too.

---

### Post #863 -- Page 29
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12862998&postcount=863>

Quote: > Originally Posted bygordbort➡️Hi, I'm an ECE student currently in a computer design class working with FPGAs. The final project is to design a CPU and assembly instruction set, and run some sort of program on it. I'd like to do a reverb. I've skimmed over this thread and there is a ton of terrific info in it. But from a processing core perspective, what sort of assembly instructions would be desirable for a reverb developer? EG. If I can get the core to do X in minimal clock cycles, what sort of things would X be? Sine function? Log function? Random number generator? Really try to get my multiplier fast? Huge memory read?Right now I'm less concerned with the reverb implementation and more concerned with the implementation of cpu instructions that will facilitate the reverb implementation. So for those of you who have worked with various DSPs, are there instructions that you wish you had when developing reverbs?For the curious, we're working with these boards:Nexys 3 Spartan-6 FPGA Trainer Board (LIMITED TIME) - DigilentI would see if you could get your university to purchase this book for your department or library:

[https://www.amazon.com/ASIC-Design-S.../dp/0071481613](https://www.amazon.com/ASIC-Design-Silicon-Sandbox-Mixed-Signal/dp/0071481613)


This was written by the late Keith Barr, who designed or codesigned a bunch of reverb specific ASICs in his career. 


In conjunction with this, take a look at the main documents for the Spin Semiconductor FV-1:

[Spin Semiconductor - Products](http://www.spinsemi.com/products.html)


The FV-1 is a dedicated audio processing DSP. It has a fairly small instruction set, with most of the instructions dedicated to reverb applications. There is also a TON of great reverb examples for the FV-1, both on the main FV-1 page and in the Spin Semiconductor forum. 


It might be worth getting a subset of the FV-1 instructions running in an FPGA, so you could directly run an FV-1 example algorithm. This way, you don't have to focus on reverb algorithm development, but rather on getting your FPGA realization up and running.

---

### Post #864 -- Page 29
**User:** gordbort
**Info:** Joined: Feb 2012Posts: 11🎧 10 years | Posts: 11
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=12864722&postcount=864>

That's excellent info acreil and seancostello, thank you!

---

### Post #865 -- Page 29
**User:** Rumi
**Info:** Joined: Oct 2003Posts: 1,758My Studio1 Review written🎧 20 years | Posts: 1,758My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13039994&postcount=865>

If you're moved, I would be interested in hearing anything about 


- Melda MTurboReverb

- u-he Protoverb


from you experts.


These two implement interesting new concepts, in different ways.


I am not asking for anything particular. Except: Can you tell us something about the structure and concept of the Protoverb? This is the most solid and 3D sounding reverb plugin I know, and it would be great to know more about where that comes from. 

Interestingly enough, Urs Heckmann from u-he wrote somewhere that he hasn't come to any conclusions in relation to what sounds good in Protoverb and what doesn't.

---

### Post #866 -- Page 29
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13040393&postcount=866>

Quote: > Originally Posted byRumi➡️If you're moved, I would be interested in hearing anything about- Melda MTurboReverb- u-he Protoverbfrom you experts.These two implement interesting new concepts, in different ways.I am not asking for anything particular. Except: Can you tell us something about the structure and concept of the Protoverb? This is the most solid and 3D sounding reverb plugin I know, and it would be great to know more about where that comes from.Interestingly enough, Urs Heckmann from u-he wrote somewhere that he hasn't come to any conclusions in relation to what sounds good in Protoverb and what doesn't.Protoverb was mentioned earlier in this thread, not much initial interest, but I like the "crowd sourcing" of the reverb listening and tuning:

[Reverb Subculture](https://gearspace.com/board/11588334-post0.html)

---

### Post #867 -- Page 29
**User:** miscend
**Info:** Joined: Jul 2009Posts: 4,289My Studio🎧 15 years | Posts: 4,289My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13041071&postcount=867>

Softube Tsar1 is a very good reverb. Apparently it uses four parallel engines to create the stereo reverb.

---

### Post #868 -- Page 29
**User:** Stolle
**Info:** Joined: Sep 2009Posts: 230🎧 15 years | Posts: 230
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13041223&postcount=868>

Quote: > Originally Posted bymiscend➡️Softube Tsar1 is a very good reverb. Apparently it uses four parallel engines to create the stereo reverb.So does just about everyone else.

---

### Post #869 -- Page 29
**User:** Rumi
**Info:** Joined: Oct 2003Posts: 1,758My Studio1 Review written🎧 20 years | Posts: 1,758My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13159230&postcount=869>

Quote: > Originally Posted byzmix➡️Protoverb was mentioned earlier in this thread, not much initial interest, but I like the "crowd sourcing" of the reverb listening and tuning:Reverb SubcultureThank you!


For whatever reason, gearslutz no longer sends me post reply and PM notifications, so I didn't notice that there was a reply until now.


If anyone could post some information (that is understandable for a non-expert, like for example block diagram descriptions) about how the Protoverb realises its reverbs, so that I can re-build them in MTurboReverb, and experiment with them, that would be a great help.


I find the sound of the Protoverb very promising, more so than that of most reverb plugins currently available, but the lack of functionality makes it hard to handle.

---

### Post #870 -- Page 29
**User:** Rumi
**Info:** Joined: Oct 2003Posts: 1,758My Studio1 Review written🎧 20 years | Posts: 1,758My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13159233&postcount=870>

BTW, the "crowd funding" of Protoverb apparently led to nothing, unfortunately - Urs wrote that the gathered data didn't show any repeatable characteristics, so it seems that Protoverb won't be turned into a full-featured reverb plugin. Which is a real pity, since it sounds more solid and spatial than most other reverb plugins.


---

## Page 30

---

### Post #871 -- Page 30
**User:** meloco_go
**Info:** Joined: Nov 2008Posts: 394🎧 15 years | Posts: 394
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13175302&postcount=871>

The fact that no patterns and preferences were found raises a very interesting point for psychoacoustics of reverb perception. Although it might also be an artifact of the procedure.

---

### Post #872 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13175628&postcount=872>

Quote: > Originally Posted bymeloco_go➡️The fact that no patterns and preferences were found raises a very interesting point for psychoacoustics of reverb perception. Although it might also be an artifact of the procedure.

 I am not sure that we can conclude from Urs' statement that he's not pursuing this reverb (by the way I cannot find any source for that claim so if someone has a link please post it) because no patterns or preferences were found, I think lack of participation is more likely. I'd like to know more, perhaps I'll write to him.


The Protoverb doesn't change it's basic structure, just the lengths of the delays and location of the taps, and it is possible to find some very good combinations within that structure, and that structure is one of millions of possible structures that might be used..


As interesting as "crowd sourcing" the tuning of a reverb algo may be in theory, reverb design is about taste and preferences as much as anything else,  and doesn't particularly lend itself to any form of automation -- including crowd sourcing.  


I think I can speak for all reverb designers when I say that we start with some theory about some aspect of reverberation that we want to explore and examine, and delve into it with innumerable "prototypes" until we prove or disprove our theories. 


However, there is seldom correlation between what a reverb designer intends and how an end-user ultimately "hears" as this is completely context dependent.


As an example, I recently mixed a record and used my 1977 Dynacord VRS-23 "Vertical Reverberation System" on the lead vocal. This is not a 'reverb" by any definition you'd hear from a reverb designer, it's simply 2 BBD lines at a specific ratio to each other with a single global feedback control (though it is comprised of 10 BBD chips and would be possible to modify in very interesting ways). I had this device returning to the mixer at a level of -20dB, and the producer in his notes was referring to this as "reverb on the vocal", which it certainly functions as, but it's really only 2 delays.


-CZ

---

### Post #873 -- Page 30
**User:** jupiter8
**Info:** Joined: Feb 2006Posts: 2,192🎧 20 years | Posts: 2,192
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13196879&postcount=873>

[YouTube](https://www.youtube.com/watch?v=o9eMmpuhz1M&index=4&list=PLeDzk3D8LGAnBLegmUTS1PPRKY9BYwZD1)


Here's a really interesting series about reverb design.

---

### Post #874 -- Page 30
**User:** eugtone
**Info:** Joined: Oct 2016Posts: 389My Studio🎧 5 years | Posts: 389My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13432611&postcount=874>

Quote: > Originally Posted byzmix➡️As an added bonus, here are exactly the same tests as above, but using a 100hz square wave oscillator as a signal source:The modulation incorporated in the PCM96 algorhythms sounds to me like several allpass filters tuned to the lower audible end of the spectrum. The effect is not unlike a Bode frequency shifter,  or a Phase shifter with the dry path muted (listening to the swept allpass outputs only) or an FM synthesizer.  It imparts a disturbing ''wowowowow" to the 'running' reverb and makes the tail jump around unnaturally.

It is interesting that if I take your Ursa major SS file and deconvolve the verb channel with the dry I can clearly find the spacing of the first 8 taps.  Are the initial 8 taps not heavily modulated in the algorithm?  (the rest of the signal certainly seems to be).

---

### Post #875 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13432897&postcount=875>

Quote: > Originally Posted byeugtone➡️It is interesting that if I take your Ursa major SS file and deconvolve the verb channel with the dry I can clearly find the spacing of the first 8 taps.  Are the initial 8 taps not heavily modulated in the algorithm?  (the rest of the signal certainly seems to be).

The output taps in the Ursa Major Space Station are not modulated at all.


The 16 programs on the front panel select between various fixed preset tap spacings. The amplitude of the taps are controlled in stereo pairs by the four level controls on the front panel.  


The "reverb"  is a heavily modulated FDN with an analog feedback path, no interpolation. This mono signal feeds the 8 taps.

---

### Post #876 -- Page 30
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434123&postcount=876>

Quote: > Originally Posted byStolle➡️So does just about everyone else.I think that you would find on closer inspection that this is not generally the case. 


While on this topic I have long wanted to give Zmix a tip of the hat for creating some very nice presets for this Reverb. His are the more creative ones beyond the standard hall and room spaces. 


You have a great ear my friend!



-Casey

---

### Post #877 -- Page 30
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434145&postcount=877>

So Barry’s patent on reduced ringing allpasses must be close to expiring. I remember hearing about it 15 years ago. 


Anyone have an exact date on it? Anyone interested in discussing it?



-Casey

---

### Post #878 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434168&postcount=878>

Quote: > Originally Posted byCasey➡️I think that you would find on closer inspection that this is not generally the case.While on this topic I have long wanted to give Zmix a tip of the hat for creating some very nice presets for this Reverb. His are the more creative ones beyond the standard hall and room spaces.You have a great ear my friend!-CaseyWow, I'm honored and flattered, thank yo for the kind words my friend..!!! 


 The architect of that algorithm told me he had no idea it was capable of those sounds.  

As we all know,  reverb design can get a bit "focused" as an idea gets refined and refined and refined, it's easy to miss the forest for the trees.  

I think they made some good compromises when reducing the user interface to those 5 basic controls, it's very hard for a beginner to make a "bad" sound, and given the wealth of choices available, people tend to move on quickly if something frustrates them, hence the current trend toward "one sound" reverbs, Plates, Chambers and Springs, which basically offer the user two choices, either "this works" or "this doesn't work".

---

### Post #879 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434173&postcount=879>

Quote: > Originally Posted byCasey➡️So Barry’s patent on reduced ringing allpasses must be close to expiring. I remember hearing about it 15 years ago.Anyone have an exact date on it? Anyone interested in discussing it?-CaseyThis one? 


Patent was awarded in 2006...

---

### Post #880 -- Page 30
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434222&postcount=880>

Quote: > Originally Posted byzmix➡️This one?That’s the one yes.


The minimalist Reverb he implented utilizing the two main tenets of this patent was considered inside Lex as a low cost product candidate a year or so earlier.


I guess the patent process can be very slow.



-Casey

---

### Post #881 -- Page 30
**User:** italo de angelis
**Info:** Joined: Oct 2010Posts: 2,069🎧 15 years | Posts: 2,069
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434373&postcount=881>

Quote: > Originally Posted byCasey➡️That’s the one yes.The minimalist Reverb he implented utilizing the two main tenets of this patent was considered inside Lex as a low cost product candidate a year or so earlier.I guess the patent process can be very slow.-Casey

Isn't that PCM8x/9x reverb work?

---

### Post #882 -- Page 30
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13434737&postcount=882>

Quote: > Originally Posted byitalo de angelis➡️Isn't that PCM8x/9x reverb work?No, this work was never released to my knowledge. 



-Casey

---

### Post #883 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13436709&postcount=883>

Quote: > Originally Posted byCasey➡️No, this work was never released to my knowledge.-Casey

Has anyone implemented the idea to evaluate the sound?

---

### Post #884 -- Page 30
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13436754&postcount=884>

Quote: > Originally Posted byzmix➡️Has anyone implemented the idea to evaluate the sound?The very simple proof of concept delivered on the promise but was too simple to be of commercial value to Lexicon. 


The basic tenets of his patent are great ideas which I am sure have general applicability and would be useful in a more complex arrangement that would sound improved. 


The one possible issue is that with very long loops the coloration of the improved allpass(s) would likely be heard in the initial onset of Reverb at the benefit of a tail that did not get worse over time. 


-Casey

---

### Post #885 -- Page 30
**User:** oldgearguy
**Info:** Joined: Sep 2002Posts: 5,007🎧 20 years | Posts: 5,007
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13436760&postcount=885>

Quote: > Originally Posted byCasey➡️The very simple proof of concept delivered on the promise but was too simple to be of commercial value to Lexicon.The basic tenets of his patent are great ideas which I am sure have general applicability and would be useful in a more complex arrangement that would sound improved.The one possible issue is that with very long loops the coloration of the improved allpass(s) would likely be heard in the initial onset of Reverb at the benefit of a tail that did not get worse over time.-CaseyYes, but would that necessarily be a bad thing?  I mean, if you're looking for a pure/natural reverb sound only then yes I can see the coloration would be a negative, but with so many 'effected' reverbs available and often desired, that coloration might be a worthwhile addition/tradeoff.  Heck, if you're a good marketer, you'd call it a feature.

---

### Post #886 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13440162&postcount=886>

Quote: > Originally Posted byCasey➡️The very simple proof of concept delivered on the promise but was too simple to be of commercial value to Lexicon.The basic tenets of his patent are great ideas which I am sure have general applicability and would be useful in a more complex arrangement that would sound improved.The one possible issue is that with very long loops the coloration of the improved allpass(s) would likely be heard in the initial onset of Reverb at the benefit of a tail that did not get worse over time.-Casey


Quote: > Originally Posted byoldgearguy➡️Yes, but would that necessarily be a bad thing?  I mean, if you're looking for a pure/natural reverb sound only then yes I can see the coloration would be a negative, but with so many 'effected' reverbs available and often desired, that coloration might be a worthwhile addition/tradeoff.  Heck, if you're a good marketer, you'd call it a feature.What Casey is alluding to in his post is the potential to have a basic reverb framework that doesn't suffer from the typical coloration and artifacts of current allpass networks, and the question is whether Barry Blesser's patented method does actually "improve" the result.  So called "natural" reverb is colored in ways that are largely unexplained, and while a allpass network can simulate the effect (as can many other methods), there aren't physical allpass filtering mechanisms in nature per se so we can theorize that the artifacts in the current allpass  implementation might be responsible for this deviation from so called "nature".  


Coloration is easy.

---

### Post #887 -- Page 30
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13441061&postcount=887>

Quote: > Originally Posted byzmix➡️What Casey is alluding to in his post is the potential to have a basic reverb framework that doesn't suffer from the typical coloration and artifacts of current allpass networks, and the question is whether Barry Blesser's patented method does actually "improve" the result.  So called "natural" reverb is colored in ways that are largely unexplained, and while a allpass network can simulate the effect (as can many other methods), there aren't physical allpass filtering mechanisms in nature per se so we can theorize that the artifacts in the current allpass  implementation might be responsible for this deviation from so called "nature".Coloration is easy.Well most parts of reverb algorithms don't have anything to do with "nature" anyway, unless you're using a 3D waveguide mesh, or conversely, you're modeling an acoustic space that consists of long, interconnected tubes. The point of the Blesser patent is to achieve even modal decay in topolgies that don't want to have even modal decay. This is assumed to be generally desirable, although it's not a natural phenomenon.


But I think in 2018 it's a solution to a problem that may not really exist anymore. It might have been helpful in the Lexicon PCM60 or whatever, but in most modern implementations you can pretty much have all the delay time you want, and if not an unlimited number of delay taps, at least a great deal more than in the 80s. So it's not necessary anymore for the signal to circulate through the same allpasses a large number of times, becoming progressively more metallic. You'd only see a significant benefit at proportionally longer decay times. Is it that important to ensure that the decay is uncolored after circulating through a small room algorithm for 30 seconds? If you really want even modal decay, why not use an FDN in the first place? I could see it being useful in embedded applications or games or something, but maybe not a commercial reverb. I mean it's mathematically brilliant but maybe a little too late.

---

### Post #888 -- Page 30
**User:** italo de angelis
**Info:** Joined: Oct 2010Posts: 2,069🎧 15 years | Posts: 2,069
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13441451&postcount=888>

Quote: > Originally Posted byzmix➡️What Casey is alluding to in his post is the potential to have a basic reverb framework that doesn't suffer from the typical coloration and artifacts of current allpass networks, and the question is whether Barry Blesser's patented method does actually "improve" the result.  So called "natural" reverb is colored in ways that are largely unexplained, and while a allpass network can simulate the effect (as can many other methods), there aren't physical allpass filtering mechanisms in nature per se so we can theorize that the artifacts in the current allpass  implementation might be responsible for this deviation from so called "nature".Coloration is easy.

Coloration is part of every natural reverb... check any place open or closed, small to very large... and coloration is there. There is no such concept of "pure" or "uncolored" reverb. We all know that. The problem is more about other artifacts or to make the reverb musical. Some claimed natural digital reverbs sound very musically limited, even poor at times...

---

### Post #889 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13441786&postcount=889>

Yes, we all seem to agree that coloration is a part of natural reverb.


The finer, and perhaps less obvious, point I am making here is that the coloration of the current allpass based reverb models may have no analog in "nature" and that by reducing (or eliminating) their characteristic coloration we may (or may not) have a chance to hear beyond our current paradigms.

---

### Post #890 -- Page 30
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13443660&postcount=890>

Quote: > Originally Posted byzmix➡️The finer, and perhaps less obvious, point I am making here is that the coloration of the current allpass based reverb models may have no analog in "nature" and that by reducing (or eliminating) their characteristic coloration we may (or may not) have a chance to hear beyond our current paradigms.I don't think the coloration is something that can be completely eliminated. The whole idea of an allpass is to spread certain frequencies over time. That's inherently unnatural. Ensuring even modal decay when they're used in a feedback loop doesn't make them them any more natural.


But I'd say a bigger problem with allpasses is their time domain response. This is a major reason why many reverb topologies completely suck for very short decay times. But while allpasses were important for making a decent sounding reverb with 128 or so instructions, you don't have to use them now.

---

### Post #891 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13444740&postcount=891>

Quote: > Originally Posted byzmix➡️Yes, we all seem to agree that coloration is a part of natural reverb.The finer, and perhaps less obvious, point I am making here is that the coloration of the current allpass based reverb models may have no analog in "nature" and that by reducing (or eliminating) their characteristic coloration we may (or may not) have a chance to hear beyond our current paradigms.
Quote: > Originally Posted byacreil➡️I don't think the coloration is something that can be completely eliminated. The whole idea of an allpass is to spread certain frequencies over time. That's inherently unnatural. Ensuring even modal decay when they're used in a feedback loop doesn't make them them any more natural.But I'd say a bigger problem with allpasses is their time domain response. This is a major reason why many reverb topologies completely suck for very short decay times. But while allpasses were important for making a decent sounding reverb with 128 or so instructions, you don't have to use them now.Certainly whenever you have more than one signal path offset in time there is inherent coloration regardless of topology, I think we all agree about that, the question I'm raising is what coloration was unique to  the standard allpass configuration and would we "miss" it if it's gone?  I have several reverbs I've created using parallel combs rather than allpass filters, they have a very useful coloration that is quite different from an allpass ring / FDN reverb..

---

### Post #892 -- Page 30
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13445912&postcount=892>

Quote: > Originally Posted byzmix➡️Certainly whenever you have more than one signal path offset in time there is inherent coloration regardless of topology, I think we all agree about that, the question I'm raising is what coloration was unique to  the standard allpass configuration and would we "miss" it if it's gone?  I have several reverbs I've created using parallel combs rather than allpass filters, they have a very useful coloration that is quite different from an allpass ring / FDN reverb..I think there are two things here that you're conflating.


The problem with the allpass loop topology is that some of the resonant modes decay more slowly than the others. The patent ensures that they decay evenly, so that all resonant modes have the same reverb time (assuming no high frequency damping). You can intentionally design a reverb to not have even modal decay if you want to. It's as simple as layering two reverbs with different decay times. Or if you're using parallel combs, just set the feedback coefficients poorly.


From a frequency domain perspective, an FDN and parallel combs aren't so different except that the modal frequencies are shifted. I don't think this patent would affect the modal frequencies, all else being equal. If that's your "coloration", it shouldn't be any different.


Also this patent isn't applicable to series allpasses, so the coloration that results from input diffusion networks won't be changed.

---

### Post #893 -- Page 30
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13445939&postcount=893>

Quote: > Originally Posted byacreil➡️I think there are two things here that you're conflating.The problem with the allpass loop topology is that some of the resonant modes decay more slowly than the others. The patent ensures that they decay evenly, so that all resonant modes have the same reverb time (assuming no high frequency damping). You can intentionally design a reverb to not have even modal decay if you want to. It's as simple as layering two reverbs with different decay times. Or if you're using parallel combs, just set the feedback coefficients poorly.From a frequency domain perspective, an FDN and parallel combs aren't so different except that the modal frequencies are shifted. I don't think this patent would affect the modal frequencies, all else being equal. If that's your "coloration", it shouldn't be any different.Also this patent isn't applicable to series allpasses, so the coloration that results from input diffusion networks won't be changed.I'm sorry if I wasn't clear, I was hoping I was distinguishing these two things rather than conflating them..  My point was simply that all reverb topologies have "coloration" and as we've had at least 3 responses sort of hammering away on the subject I just wanted to put that aside as a general idea and focus on the *difference* in color that Dr. Blesser's patent may have...

---

### Post #894 -- Page 30
**User:** eugtone
**Info:** Joined: Oct 2016Posts: 389My Studio🎧 5 years | Posts: 389My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13448401&postcount=894>

I was playing around with modelling the frequency damping due to travel through air, and computed some mean phase transform IRs that I sometimes drop in delay plugins so that my echos are attenuated based on the distance of flight required to get a certain delay (ignoring loss due to whatever it needed to reflect off of to return).  I found a rough model for the falloff on some website and shared some IRs for people.
[air attenuation IRs](https://gearspace.com/board/music-computers/1204487-free-ir-pack-naturally-filtering-delays-based-distance.html)


I'm only using MPT because I like that for guitar cabinet IRs.  Would a linear phase EQ be the most accurate form of what I'm attempting here?  Do you guys consider this when designing reverbs?

---

### Post #895 -- Page 30
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13835626&postcount=895>

Quote: > Originally Posted byeugtone➡️I was playing around with modelling the frequency damping due to travel through air, and computed some mean phase transform IRs that I sometimes drop in delay plugins so that my echos are attenuated based on the distance of flight required to get a certain delay (ignoring loss due to whatever it needed to reflect off of to return).  I found a rough model for the falloff on some website and shared some IRs for people.air attenuation IRsI'm only using MPT because I like that for guitar cabinet IRs.  Would a linear phase EQ be the most accurate form of what I'm attempting here?  Do you guys consider this when designing reverbs?I realize that my answer comes very late, but I would definitely go for minimum phase. Linear phase with it's pre-ringing doesn't really occur in natural acoustic surroundings. I believe the propagation loss should be considered minimum phase, although interference will most probably make rooms mixed phase.


Best,

Stian

---

### Post #896 -- Page 30
**User:** Acon Digital - Stian
**Info:** Joined: Apr 2013Posts: 882🎧 10 years | Posts: 882
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=13835638&postcount=896>

Hi everybody!


Is anybody here aware of scientific articles covering time invariance / variance in real halls or other large acoustical spaces? E.g. in a large hall, how similar will two consecutive impulse response measurements be? I assume that there will be an increasing difference towards the end of the reverb tail since time differences due to air currents, etc. will accumulate over time.


Best,

Stian

---

### Post #897 -- Page 30
**User:** ad8e
**Info:** Joined: Jan 2021Posts: 2🎧 5 years | Posts: 2
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15267129&postcount=897>

I recently did a lot of math on reverbs, and am planning on writing a treatise. Are there reverb designers who publish research, or does everyone keep their findings private? Griesinger and Lokki have been doing good work from the perceptual side. But if it's just these two, I'll probably tailor my writing toward a mathematical/academic audience, instead of making it accessible to an average programmer. I tried searching through JAES and JASA with the "reverb" keyword, but the articles found were not of general interest. JAES's search functionality doesn't seem to sort by relevance. I had better results trawling through Griesinger and Lokki's publications.

---

### Post #898 -- Page 30
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15267466&postcount=898>

Definitely sort out Blessers Notch Pass design. It is clever, and will become a staple when it comes off its patent protection. 



-Casey

---

### Post #899 -- Page 30
**User:** ad8e
**Info:** Joined: Jan 2021Posts: 2🎧 5 years | Posts: 2
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15268296&postcount=899>

This is the link: [https://patents.google.com/patent/US20060116781](https://patents.google.com/patent/US20060116781)


I checked it out after your recommendation; I had seen the previous mentions but didn't pay attention at the time. It looks like a tool for people constructing reverb topology by manual experimentation of topologies and hand-tweaking filter lengths. One can notchpass any poles that approach the unit circle, have too high a residue, or group too closely together.


Meh, my first inclination as a mathematician is to be upset by people taking patents on simple math, but my further consideration is that this is actually appropriate for a patent. It's not a canonical construction, and someone deriving theory from scratch won't encounter it. Rather, it is a specific property of his particular implementation. And seeing the enthusiastic response from other reverb designers, it does not appear to be so simple that it would be discussed without his contribution. If it were optimal in math, I would be more upset, since it is a specific and obvious example of a more general construction which is actually canonical.


I can describe that more general construction. In an FDN, delay lengths are either uncorrelated or correlated, no in-between. Then, you can "allpassify" any subfilter by taking all the poles and turning them into paired zeros across the unit circle, basically flipping feedbacks into feedforwards. This is the case when delay lengths are correlated.


Doing this for a single feedback delay line is an error; it should be done for a larger subfilter. And I'm glad Blesser's patent doesn't spot this, or I would be pissed, since it's not ok to patent math. The feedforward and feedback can either be in series, parallel, or other topology, and the feedforward can instead be a feedback with different gain. (Basically, instead of pairing a pole and zero, a pole is paired with an offset pole, "shadowing" the first pole.) What's important is not the strength distribution of the echoes, but the paired locations, and the fact that the paired filter is in opposition to the original filter. This technique (including Blesser's) doesn't seem of general interest anyway, since the effect of the pairing is:


1. it distorts the attack region of the complex plane.

2. it reduces the energy of the echo, which makes it a wash in terms of tail energy/distortion efficiency, and disadvantageous in terms of CPU usage. Its main purpose is to hand-tweak your frequency graph.


I can't be too confident of my assertion that 1. is bad, because my own reverb faces unexpectedly huge variance in the Fourier spectrum at low RT60. And if you pair poles instead of zeroes, then at least there are no zeros in the attack region. Distortion in the attack region may be a worthy tradeoff for better steady state behavior.


If you want to experiment with the specific filter in his patent before it expires, I recommend pairing poles with offset poles. This construction should be superior to Blesser's, ignoring CPU and memory considerations, because it doesn't insert zeroes in inappropriate places, and better controls group profile. If the group profile isn't what you want, you can change the residue of the offset poles. I'm not patenting anything, so there's no patents to worry about. However, I don't recommend this construction anyway, unless you really are tweaking your coefficients and filter lengths by hand.


Thanks for the recommendation. It helped me form an impression of the state of public reverb design.

---

### Post #900 -- Page 30
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15694979&postcount=900>

Anyone want to guess what this is? I think there are enough clues.


---

## Page 31

---

### Post #901 -- Page 31
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15695417&postcount=901>

Quote: > Originally Posted byacreil➡️Anyone want to guess what this is? I think there are enough clues.An Alesis? 


Are you sure this is drawing is correct. I wonder about the 4 bit attenuation “.9375” in the loop. Seems like it should be before the third pair of output taps. As it is, it is just combined with the master attenuation “.75”. 


Maybe to avoid left/right balance issues. Still I would have placed it after the third AP in series with the master if that were the case. 


-Casey

---

### Post #902 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15695882&postcount=902>

Quote: > Originally Posted byCasey➡️An Alesis?No prize without the exact model 

Quote: > Are you sure this is drawing is correct. I wonder about the 4 bit attenuation “.9375” in the loop. Seems like it should be before the third pair of output taps. As it is, it is just combined with the master attenuation “.75”.I haven't tested it yet, but I think any errors would be miscalculated gains or delay lengths rather than the topology. Anyway the 0.75 is part of the lowpass filter.

Quote: > Maybe to avoid left/right balance issues. Still I would have placed it after the third AP in series with the master if that were the case.The balance and stereo image in this model don't seem to be particularly high priorities. 


Here's the impulse response (from a simulation with no anti-aliasing/reconstruction filter modeling, resampled to 44.1 kHz).

---

### Post #903 -- Page 31
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15695891&postcount=903>

Quote: > Originally Posted byacreil➡️No prize without the exact modelI'd guess Microverb or XT:C based on the sample rate..

---

### Post #904 -- Page 31
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15696015&postcount=904>

Quote: > Originally Posted byzmix➡️I'd guess Microverb or XT:C based on the sample rate..Or the Nanoverb.


I still think the attenuation elements should be slid back so they happen before the 2nd and 3rd output tap pairs respectively. It will lessen that recirculation bump. 


I see what you did there. Not even stoned yet, and I see your cops night stick is beating in time with the recirculation stepping!


And why the random insertion of 21 samples of forced predelay?


-Casey

---

### Post #905 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15696153&postcount=905>

Quote: > Originally Posted byzmix➡️I'd guess Microverb or XT:C based on the sample rate..I believe the sample rate in the XT:c is 39062.5 Hz. The original Microverb's sample rate is 23437.5 Hz, but I don't have that one. But there's one other one that uses that sample rate...

Quote: > Originally Posted byCasey➡️Or the Nanoverb.I'm no stranger to wasting my life on stuff that no one else cares about, but even I wouldn't bother with that one. I'm pretty sure it's just a boring rehash of the Midiverb 4 (which I think is just a crappier, less capable version of the Quadraverb 2). I've got an endless queue of worthier time sinks.

Quote: > I still think the attenuation elements should be slid back so they happen before the 2nd and 3rd output tap pairs respectively. It will lessen that recirculation bump.I see what you did there. Not even stoned yet, and I see your cops night stick is beating in time with the recirculation stepping!Should "recirculation stepping" be the official name for that? i.e. where there's only one attenuator or filter in the loop and you can distinctly hear each pass? I think it's actually sometimes useful if you're not aiming for realism. It's kind of like a gated reverb, where you can get a big sound without the decay getting too messy when the input signal is busy. We need consistent terminology for these things.

Quote: > And why the random insertion of 21 samples of forced predelay?22 if you count the single sample delay on the input that's there for no discernible reason (this might actually be a vestigial remnant of a lowpass filter from a related algorithm). Well there's no other pre-delay, so I don't think it's a bad thing. There are much weirder and more inexplicable things lurking in the other algorithms. Which I will of course share for your head-scratching pleasure.

---

### Post #906 -- Page 31
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15696213&postcount=906>

Quote: > Originally Posted byacreil➡️I believe the sample rate in the XT:c is 39062.5 Hz. The original Microverb's sample rate is 23437.5 Hz, but I don't have that one. But there's one other one that uses that sample rate...Gonna guess MIDIverb. But I don't have that one - just MIDIverb II, IV, Quadraverb, and Wedge.

Quote: > I'm no stranger to wasting my life on stuff that no one else cares about, but even I wouldn't bother with that one. I'm pretty sure it's just a boring rehash of the Midiverb 4 (which I think is just a crappier, less capable version of the Quadraverb 2). I've got an endless queue of worthier time sinks.I think the Midiverb 4 sounds pretty good. But it's been years since I've plugged any of that stuff in.

Quote: > Should "recirculation stepping" be the official name for that? i.e. where there's only one attenuator or filter in the loop and you can distinctly hear each pass? I think it's actually sometimes useful if you're not aiming for realism. It's kind of like a gated reverb, where you can get a big sound without the decay getting too messy when the input signal is busy. We need consistent terminology for these things.A single attenuator in the loop can be fine, if you have enough allpasses with the right coefficient. But that's not what your impulse is showing.

Quote: > 22 if you count the single sample delay on the input that's there for no discernible reason (this might actually be a vestigial remnant of a lowpass filter from a related algorithm). Well there's no other pre-delay, so I don't think it's a bad thing. There are much weirder and more inexplicable things lurking in the other algorithms. Which I will of course share for your head-scratching pleasure.We're gonna see a lot of allpasses with 0.5 and -0.5 coefficients.

---

### Post #907 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15696732&postcount=907>

Quote: > Originally Posted byseancostello➡️Gonna guess MIDIverb. But I don't have that one - just MIDIverb II, IV, Quadraverb, and Wedge.I knew you'd get it <3<3<3 although I think you had something of an unfair advantage since I told you previously that I had one and was messing with it. It's preset 49, "18 Sec. EX. LARGE BRIGHT" from the Midiverb. 

Quote: > I think the Midiverb 4 sounds pretty good. But it's been years since I've plugged any of that stuff in.I think the Quadraverb 2 is the one to get though, or the Wedge. But I feel like Alesis were kind of stagnating in the 90s. Ensoniq, Roland, Sony and Digitech were doing better mid-priced effects at that point. The Quadraverb 2 wasn't that much of an advancement (still just 128 instructions per sample), then they just coasted forever.

Quote: > A single attenuator in the loop can be fine, if you have enough allpasses with the right coefficient. But that's not what your impulse is showing.Yeah these are kind of special. In practice though it mostly sounds pretty good. Except there's an *enormous* amount of clipping on some of the longer reverbs (including the one I posted earlier). The dynamic range completely sucks. I kind of like that, though. It gives it that crap "20 year old Rephlex Records artist in a bedroom studio at mom's house" quality.

Quote: > We're gonna see a lot of allpasses with 0.5 and -0.5 coefficients.I got your allpasses right here. 21 of them. Some of it is rearranged a bit for the sake of clarity (the gains in the feedback path were weird). Don't ask me why the input filter output is taken after the delay and the feedback filter output is taken before the delay. Maybe it was more convenient. But why are there even two filters in the first place when they're both the same?

---

### Post #908 -- Page 31
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15696907&postcount=908>

Quote: > Originally Posted byacreil➡️I think the Quadraverb 2 is the one to get though, or the Wedge. But I feel like Alesis were kind of stagnating in the 90s. Ensoniq, Roland, Sony and Digitech were doing better mid-priced effects at that point. The Quadraverb 2 wasn't that much of an advancement (still just 128 instructions per sample), then they just coasted forever.I wonder how long the Alesis reverb DSPs stuck with 128 instructions. The AL3201 had 128 instructions as well. Same with the Spin Semi FV-1, although that chip didn't require the memory refreshing instructions of the AL3201, so you could do a bit more. The FV-1 sounds good, but I could make use of 2-4X the memory and 2X the instructions.

Quote: > I got your allpasses right here. 21 of them. Some of it is rearranged a bit for the sake of clarity (the gains in the feedback path were weird). Don't ask me why the input filter output is taken after the delay and the feedback filter output is taken before the delay. Maybe it was more convenient. But why are there even two filters in the first place when they're both the same?Agreed - I would use the same filter for input and feedback signal. 


I'm a bit more disturbed that the feedback path has no "straight" delay in there. When you take series allpasses and route their output back to the input, the feedforward signal will be routed as well - i.e. the dry input signal, scaled by the feedforward coefficients of the allpasses in series. If the number of allpasses is low and/or the coefficients are closer to |1.0|, you can get some nasty resonance in there, unless you delay the feedback path. In this case, the "dry" gain is -90 dB, so probably not much of a problem. Any coloration would be masked by, well, all the cruft that the Midiverb is gonna have in there.


It's interesting to see the Bloom algorithm drawn out like that. Kinda like a stripped down Blackhole algorithm, but with fewer stereo output allpasses, and no modulation. It looks a lot like an expanded version of a reverb algorithm in Hal Chamberlin's book, that had 3 mono series allpasses for the main reverb, and two sets of 2 shorter series allpasses following that in parallel to make things stereo.

---

### Post #909 -- Page 31
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15697381&postcount=909>

Quote: > Originally Posted byseancostello➡️I wonder how long the Alesis reverb DSPs stuck with 128 instructions. The AL3201 had 128 instructions as well. Same with the Spin Semi FV-1, although that chip didn't require the memory refreshing instructions of the AL3201, so you could do a bit more. The FV-1 sounds good, but I could make use of 2-4X the memory and 2X the instructions.Agreed - I would use the same filter for input and feedback signal.I'm a bit more disturbed that the feedback path has no "straight" delay in there. When you take series allpasses and route their output back to the input, the feedforward signal will be routed as well - i.e. the dry input signal, scaled by the feedforward coefficients of the allpasses in series. If the number of allpasses is low and/or the coefficients are closer to |1.0|, you can get some nasty resonance in there, unless you delay the feedback path. In this case, the "dry" gain is -90 dB, so probably not much of a problem. Any coloration would be masked by, well, all the cruft that the Midiverb is gonna have in there.It's interesting to see the Bloom algorithm drawn out like that. Kinda like a stripped down Blackhole algorithm, but with fewer stereo output allpasses, and no modulation. It looks a lot like an expanded version of a reverb algorithm in Hal Chamberlin's book, that had 3 mono series allpasses for the main reverb, and two sets of 2 shorter series allpasses following that in parallel to make things stereo.Designs like this make BB’s notchpass seem so overdue. And so brilliant. A closed form for calculating the AP coefs to damp the metal. 


You (@acreil) mention some weird AP coefs. Perhaps some hand calculations/trial and error to do the same?


-Casey

---

### Post #910 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15698342&postcount=910>

Quote: > Originally Posted byseancostello➡️I wonder how long the Alesis reverb DSPs stuck with 128 instructions. The AL3201 had 128 instructions as well. Same with the Spin Semi FV-1, although that chip didn't require the memory refreshing instructions of the AL3201, so you could do a bit more. The FV-1 sounds good, but I could make use of 2-4X the memory and 2X the instructions.As far as I know the early ones were 128 instruction, the DASP-8 IC in the Midiverb 3 and Microverb 3 are 64 (this looks to me like the DASP-16 IC in the Midiverb 2 with a 16x8 multiplier tacked on), the ZAK 24 IC in the Quadraverb is 96, the DSP1 IC in the Quadraverb 2/Wedge is 128, and the M4/M4C IC in the Midiverb 4 is 64. But obviously the capabilities of the IC and what it's accomplishing per instruction vary a lot. It takes 4 instructions here to do an allpass with a 0.5 coefficient, 3 instructions for a first order lowpass with a 0.5 coefficient.


I think the same basic Midiverb design originated in the MXR 01. ART continued to use it (or at least closely related designs) in the DR1, DR2, ProVerb, Multiverb, FXR, and all the different ugly variants and rehashes. They actually implemented modulation effects before Alesis, and later even a (terrible) pitch shifter. Eventually the ART processors used 64k x 20 RAM and a custom IC. I don't know if there were other improvements (there are no schematics available, plus the part numbers are sanded off of the early ones), but they seemed to still use horrible sounding Schroeder reverbs. I messed around with a Multiverb once and thought it was awful, much worse than the Quadraverb. Trying to do programmable multi-effects with such a limited processor is kind of a bad fit. I'm impressed that they were able to do it at all, but it makes more sense to do weird-ish preset effects where strange behavior and lack of flexibility aren't a problem.

Quote: > It's interesting to see the Bloom algorithm drawn out like that. Kinda like a stripped down Blackhole algorithm, but with fewer stereo output allpasses, and no modulation. It looks a lot like an expanded version of a reverb algorithm in Hal Chamberlin's book, that had 3 mono series allpasses for the main reverb, and two sets of 2 shorter series allpasses following that in parallel to make things stereo.This predates Eventide's implementation, doesn't it? Unless it first appeared in the SP2016. I expect there are some algorithms in the Midifex that would be closer to the Chamberlin algorithm. 

Quote: > Originally Posted byCasey➡️Designs like this make BB’s notchpass seem so overdue. And so brilliant. A closed form for calculating the AP coefs to damp the metal.There are definitely a lot of metallic reverb tails in the Midiverb. Generally the onsets are metallic due to series allpasses (sounds horrible when listening to the impulse response but generally okay in practice), the mid portion is fairly smooth and neutral, then it becomes metallic as it decays. But the signal has decayed to a pretty low level by that point, so it's not that noticeable. If I had to complain about the algorithms, the stereo separation/balance is really bad (or at least weird) in some of them. But on the whole it sounds pretty good, and there's not really much that jumps out and sounds like garbage. There's no struggle to get a usable sound like there is with a lot of lower end reverbs.


I think it sounds better than the Quadraverb, definitely better than the SPX90 or REV7, and mostly better than the Roland SRV-2000 (which has an impressively powerful processor, but not enough memory). And honestly I'd probably prefer the Midiverb and Midiverb 2 over an AMS RMX16 and Lexicon PCM60. I think it wins the 16k x 16/time invariant weight class.

Quote: > You (@acreil) mention some weird AP coefs. Perhaps some hand calculations/trial and error to do the same?So far the allpasses have all been the same topology/coefficient. The weird coefficient thing I noticed was the filter/gain coefficients in the bloom algorithm. The gains in the actual algorithm are -0.25 and 1.5, which I rewrote as 0.5 and -0.75 for the sake of clarity. The gains are often done strangely because the only multiplication is a hardwired arithmetic right shift. I assume Keith Barr had written out a table of all the possible gains and the sequences of instructions used to obtain them (it's actually more flexible in this respect than I would have expected), but trying to reverse engineer it is not particularly intuitive.

---

### Post #911 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15699330&postcount=911>

I've been digging through the Midiverb/Midifex algorithms looking for different reverb topologies. There seem to be two main ones, which I guess could be called "hall" (represented by Midiverb preset 49, which I posted before) and "room" (Midiverb preset 7, attached). But I notice that the ones I picked aren't necessarily the best examples. Most of the hall variants seem to have 6 allpasses on the input and a smoother overall sound (and correspondingly a distinct "bloom" effect on the onset). And Midiverb preset 7 appears to contain a bug. Maybe the problem is on my end (I'm really just fumbling my way through this), but I repeatedly worked through the extremely convoluted gain calculations and kept coming up with the same result. The issue is that this algorithm uses a different allpass variant on the input (the recirculating portion uses the same allpass as the others with a 0.5 coefficient). The coefficient is 0.625 and it takes 8 instructions rather than 4 (I would have thought 0.75 would be simpler, but who knows). The problem is that the feed forward gain on the third one appears to be 0.75 rather than 0.625, hence it's not really an allpass. The same thing appears in some other algorithms, but not all of them. I also find it a little odd that there are two separate recirculating loops here rather than one. Casey will be pleased that the feedback gains are evenly distributed.

---

### Post #912 -- Page 31
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15699589&postcount=912>

Quote: > Originally Posted byacreil➡️preset 7 appears to contain a bug.Maybe they needed to save cycles? The benefit of the larger feed forward is less bloom. Maybe it was just the thing they needed to get to a room sound? A little extra feed forward outside the loop probably isn’t going to add much color with so much feed back going on. 


I hear you on the two loops. That seems like more of a bug. No obvious reason for not having one loop. 



-Casey

---

### Post #913 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15699691&postcount=913>

Quote: > Originally Posted byCasey➡️Maybe they needed to save cycles? The benefit of the larger feed forward is less bloom. Maybe it was just the thing they needed to get to a room sound? A little extra feed forward outside the loop probably isn’t going to add much color with so much feed back going on.It would have been simpler to do it "correctly". The way it looks to me is there's an extra instruction that doesn't need to be there. It's got the correct gains, then it accumulates a temporary address and messes one of them up. There are some other variants that accumulate a different address there instead. I'll have to see what those are doing.


It could well be intentional. One thing that makes the Midiverb and Midiverb 2 so useful is that they get the small space sound right in a way that most reverbs don't. Usually (as I'm sure you're well aware) you set the decay time to 0.2 seconds or whatever and just hear the input allpasses and nothing else, and it sounds horrible. Quantec and Roland could do it well. The Ibanez SDR-1000 does alright, although it often sounds weird with impulsive inputs. The Quadraverb and SPX90 sound cheap and awful. The Midiverb always mixes well and doesn't sound like garbage. With the right wet/dry balance it's one of those "you forget it's there until you mute it" kind of things. Cheap stuff never manages to do that. If it does something weird to help accomplish that, I wouldn't be all that surprised. 

Quote: > I hear you on the two loops. That seems like more of a bug. No obvious reason for not having one loop.I could see maybe doing that if it was stereo input or something. I guess. It might make more sense in context if compared against the XT, XT:c and Midiverb 2. I feel like this was sort of an intermediate step in the way things were evolving.

---

### Post #914 -- Page 31
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15700376&postcount=914>

Have you seen this email from Keith that Shawn posted?

[https://valhalladsp.com/2010/08/25/rip-keith-barr/](https://valhalladsp.com/2010/08/25/rip-keith-barr/)

---

### Post #915 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15700576&postcount=915>

Quote: > Originally Posted byTomás Mulcahy➡️Have you seen this email from Keith that Shawn posted?https://valhalladsp.com/2010/08/25/rip-keith-barr/I've seen it, although I haven't looked at it recently. I tried to use it as a reference when working on the script I wrote to simulate the Midiverb, but the details aren't completely accurate. I ended up ignoring all that and just using the schematic and an oscilloscope. But it turned out that there's an omission in the schematic too...


At this point I have a simulator and a disassembler. I should write a couple other things to make the process simpler, then also write an assembler and start writing my own algorithms. At that point I will reach the zenith of nerdiness. 


Anyway here's the 600ms gate algorithm (#59). The allpass network to make stereo outputs is similar to the bloom algorithm, and just as crappy. But 91 taps is impressive. The other gate algorithms just use fewer taps. They sound alright, but I would prefer if they'd been biased more toward shorter gate times.

---

### Post #916 -- Page 31
**User:** Antti H
**Info:** Joined: Sep 2010Posts: 408My Studio🎧 15 years | Posts: 408My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15700896&postcount=916>

Quote: > Originally Posted byacreil➡️Anyway here's the 600ms gate algorithm (#59). The allpass network to make stereo outputs is similar to the bloom algorithm, and just as crappy.Funnily enough, I used the exact same idea to make a mono reverb (4-line Schroeder with global negative feedback, IOW the simplest possible FDN) into "stereo" for the VS10xx mp3 / gmidi ICs back in 2005. In my case it was due to never having had access to any remotely decent reverb unit to play with coupled with extreme ram constraints (IIRC the reverb runs at 14.7 / 16 kHz and uses 300 - 400 ms of delay, so around 10 kB of ram total) and the fact that I did the whole design in about three weeks from scratch, including all the research and finding what papers I could.


It's the usual tragedy of the throw-it-in bad designs ending up selling more than proper stuff (AFAIK, those chips have been sold by the millions during the last 15 years).

---

### Post #917 -- Page 31
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15701276&postcount=917>

Quote: > Originally Posted byacreil➡️I've seen it, although I haven't looked at it recently. I tried to use it as a reference when working on the script I wrote to simulate the Midiverb, but the details aren't completely accurate. I ended up ignoring all that and just using the schematic and an oscilloscope. But it turned out that there's an omission in the schematic too...At this point I have a simulator and a disassembler. I should write a couple other things to make the process simpler, then also write an assembler and start writing my own algorithms. At that point I will reach the zenith of nerdiness.Anyway here's the 600ms gate algorithm (#59). The allpass network to make stereo outputs is similar to the bloom algorithm, and just as crappy. But 91 taps is impressive. The other gate algorithms just use fewer taps. They sound alright, but I would prefer if they'd been biased more toward shorter gate times.I love my Midiverbs. Are these from some resource that has all these algorithms available this way? I'd love to see what the super-long verbs like 49 and 50 are like. I particularly like that we can identify 'tropes' out of these, like the 'two allpasses and a delay' module, or the 0.5 allpasses I already knew about.

---

### Post #918 -- Page 31
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15702455&postcount=918>

Quote: > Originally Posted byCasey➡️I hear you on the two loops. That seems like more of a bug. No obvious reason for not having one loop.From a 2008 email exchange with Keith Barr:


"I’ve forgotten about the Quadraverb. I think it was a 64 instruction engine, may have been 128. Frank would know, he did the chip as I recall. For algorithms, I was the guru at the time, and I was just coming around to putting APs in delays loops and recognizing the need for extensive loop filtering. My guess is that the Quadraverb used 4 parallel loops of 2 X AP +1 delay, outputs from delay taps as the basic structure. I doubt there were any single large loops like I use now."


So, probably not a bug, so much as a different design approach that changed over time.


Some more info from Keith's posts at the Spin Semiconductor forum:


"“The first reference to all passes I recall was an AES issue that detailed Schroeder’s work, a terrible sounding algorythm as described. The tinny sound of the MXR reverb (my work) suffered from this problem. Other early reverbs also suffered from this limited structure (Nichols). Including all pass filters within the comb loops came next (in my work), which definately improved density build, but I was having coding difficulties in the early years with multiple APs in a loop.


It only makes sense though, that the inclusion of multiple APs in a delay loop will improve density, which in my case, was finally worked out with my Midiverb, and other later Alesis products. Finally, the summation of multiple regenerated delays, with APs included, leads to excessive peaking at certain frequencies… Making the reverb a single loop solves the problem.


I’ve found that once you’re in the single loop, multiple AP arena, you can make just about anything that has a good tail, reletively flat response, and as much final density as you like. Everything I write today is single loop, with modifications as to input signal injection and output tap selection. “"

---

### Post #919 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15702563&postcount=919>

Quote: > Originally Posted byAntti H➡️Funnily enough, I used the exact same idea to make a mono reverb (4-line Schroeder with  global negative feedback, iow the simplest possible FDN) into "stereo" for the VS10xx mp3 / gmidi ICs back in 2005. In my case it was due to never having had access to any remotely decent reverb unit to play with, extreme ram constraints (IIRC the reverb runs at 14.7 / 16 kHz) and the fact that I did the whole design in about three weeks from scratch, including all the research and finding what papers I could.Wow, that must have sounded really... not good. I don't think allpass chains are necessarily a completely horrible idea for making a signal stereo, but the stereo width on the bloom algorithm is noticeably not as good as the other reverbs. 


I wish I could find all the worst reverb algorithms lurking in cheap keyboards and home stereos and karaoke machines and whatever. There must be some real gems out there. Thank you for your contribution.


I always like comparing different gated reverb algorithms because many of them aren't just straightforward multitap delays, but it's not necessarily clear what else they're doing. The Roland DEP-5 seems to switch between several different configurations depending on the length. Twiddling the knobs while playing through it gives some very strange effects.

Quote: > Originally Posted bychrisj➡️I love my Midiverbs. Are these from some resource that has all these algorithms available this way?I am the resource. I did 49 on the previous page.

Quote: > Originally Posted byseancostello➡️From a 2008 email exchange with Keith Barr:"I’ve forgotten about the Quadraverb. I think it was a 64 instruction engine, may have been 128. Frank would know, he did the chip as I recall. For algorithms, I was the guru at the time, and I was just coming around to putting APs in delays loops and recognizing the need for extensive loop filtering. My guess is that the Quadraverb used 4 parallel loops of 2 X AP +1 delay, outputs from delay taps as the basic structure. I doubt there were any single large loops like I use now."I would think it would be relatively easy to figure out the Quadraverb's basic topology from impulse responses, since you can set all the allpass coefficients to zero. A single loop would just result in a repeating echo pattern, and that's clearly not what's happening. IIRC one of them (chamber or hall or something) seems to have a different topology.


I also got distracted today thinking about the SPX90. I think it's a Schroeder reverb with two early reflection taps, a couple series allpasses and maybe 6 combs with two output taps each. All 4 algorithms (plate, room, hall, vocal) use the same topology.

---

### Post #920 -- Page 31
**User:** seancostello
**Info:** Joined: Feb 2009Posts: 4,769🎧 15 years | Posts: 4,769
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15702577&postcount=920>

Quote: > Originally Posted byacreil➡️I would think it would be relatively easy to figure out the Quadraverb's basic topology from impulse responses, since you can set all the allpass coefficients to zero. A single loop would just result in a repeating echo pattern, and that's clearly not what's happening. IIRC one of them (chamber or hall or something) seems to have a different topology.I would need to find a power supply for my Quadraverb to hear what is going on. It has sat on a shelf for many years.

Quote: > I also got distracted today thinking about the SPX90. I think it's a Schroeder reverb with two early reflection taps, a couple series allpasses and maybe 6 combs with two output taps each. All 4 algorithms (plate, room, hall, vocal) use the same topology.I know Yamaha has some patents that show "crossover Schroeder" reverbs. Like, 3 bands of Schroeder reverb, with a different structure for low, medium & high frequencies. Then again, Yamaha has a LOT of patents, and it is hard to know what actually made it into a product.

---

### Post #921 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15703570&postcount=921>

Quote: > Originally Posted byseancostello➡️I would need to find a power supply for my Quadraverb to hear what is going on. It has sat on a shelf for many years.The last time I dug mine out it sounded better than I remembered. It used to have this obnoxious sound that permeated everything. But probably I just sucked at using the high frequency decay parameter and didn't realize that the input mix and predelay mix parameters can introduce horrific comb filtering. 

Quote: > I know Yamaha has some patents that show "crossover Schroeder" reverbs. Like, 3 bands of Schroeder reverb, with a different structure for low, medium & high frequencies. Then again, Yamaha has a LOT of patents, and it is hard to know what actually made it into a product.I think a lot of their patents are just spitballing. Some describe specific products in a lot of detail, but a lot of them are apparently just ideas that weren't even seriously considered. The crossover reverb thing doesn't seem like an especially good idea anyway. Kind of just a waste of memory and processing power. Maybe if you were using a critically sampled filter bank...


The SPX90 is really underpowered. 64 instructions but only 32 memory reads/writes. *But* it has 16 channel hardware-based modulation that's better than what everyone else was doing. Hence the symphonic and dual pitch shift algorithms. 


Yamaha kind of disappoint me in the effect processor department. The REV1 was the most powerful thing around until maybe the Lexicon 480L or Roland R880. The SPX90 and REV7 kind of suck (other than the symphonic effect). The REV5 sounds pretty good, but there's nothing exciting about it. For the most part they were well behind the competition and just rehashed the same stuff for years. I'll be even more disappointed if everything just turns out to be Schroeder reverbs.


The R1000 is a real oddball though. Mono in/out and 37 parallel comb filters, apparently. First custom IC for reverb too. I almost want one.

---

### Post #922 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15709467&postcount=922>

Two more multitap variants. Multitap delays can be implemented very efficiently (one instruction per tap), plus filters and gains can be fairly easily added to specific groups of delay taps. But I don't see any early reflection taps in the reverb algorithms.


I'll have a couple more reverb variants when I can redraw them more cleanly. Those will be more interesting.

---

### Post #923 -- Page 31
**User:** Reverb Foundry
**Info:** Joined: Aug 2021Posts: 33 | Posts: 33
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15709896&postcount=923>

Quote: > Originally Posted byCasey➡️I hear you on the two loops. That seems like more of a bug. No obvious reason for not having one loop.Pretty easy to get a bug like that in some of these old architectures, it's simple to swap the dual-loop architecture of HD Cart's reverb algorithm for a single-loop variant. This inspired the 'recirculation' control which does just that and turns it from a dual loop reverb to a much longer single loop design. Sounds much better in single loop mode imho.


Matt

---

### Post #924 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721056&postcount=924>

I still haven't written a Midiverb assembler yet (putting it off because parsing stuff from strings is boring), but I'm prototyping some new algorithms. It's easier than I expected, and actually a rather fun form of recreational programming. Beats sudoku or whatever.


If anyone's curious, you can get about 10 comb filters with decent filtering and attenuation and two output taps. With no filtering, a 0.75 feedback coefficient and two output taps, you can get 20. With no filter, 0.5 feedback and one output tap, 30. Or you can get 24 allpasses (0.5 coefficient) with two loop filters/attenuators. 


Basically, the Midiverb design is great at doing delay taps, allpass or lowpass filters with a 0.5 coefficient. And it's pretty crap at everything else. Trying to make a programmable reverb with a Schroeder topology is really an uphill battle. So it's no surprise that the MXR 01 sucked (also don't ever buy one because there's an inter-board connector that's terribly designed). I wouldn't expect a lot from the Alesis XT or XT:c either (far too little delay memory for the recirculating portion when factoring in the pre-delay, input allpasses and relatively high sample rate). The Midiverb/Midifex/Midiverb II are pretty much as good as it gets. At least until I program some better algorithms. 


I figured out how to do allpasses with a -0.25 or 0.75 coefficient, nested allpasses, plus some other stuff. I don't think an FDN is really in the cards. Maybe a very basic one, but it won't be very good.


Currently I've got a 27C256 EPROM installed in mine with both the Midiverb and Midifex algorithms and a switch to select between them. But a 27C512 will fit too. I could easily program another 20 or 30 algorithms, plus "infinite reverb" variants of some of the existing algorithms. And I can modify the "bypass" algorithm so that it doesn't clear the delay memory when changing algorithms.

---

### Post #925 -- Page 31
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721133&postcount=925>

Quote: > Originally Posted byacreil➡️Currently I've got a 27C256 EPROM installed in mine with both the Midiverb and Midifex algorithms and a switch to select between them.Very cool!

---

### Post #926 -- Page 31
**User:** niklasni1
**Info:** Joined: Aug 2011Posts: 1,098🎧 10 years | Posts: 1,098
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721237&postcount=926>

I'm really curious about what the instruction set for something like this looks like. Does it have branching/looping at all? Or is it all straight ahead for N samples and then back to the beginning?

---

### Post #927 -- Page 31
**User:** pulsar modular
**Info:** Joined: Sep 2004Posts: 954My Studio🎧 20 years | Posts: 954My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721241&postcount=927>

A few years ago I implemented the plate reverb described in a  white paper by Jon Dattorro. It sounds very good to me. I found it somewhat surprising as I got into it, that the type of schematic presented (some also in this thread) was more than a block diagram, in fact a very complete description of the algorithm. Do tools exist that configures usable code from such schematics, so you can test it directly? Seems quite possible and very useful. Is it perhaps too esoteric and pros build their own tools?

---

### Post #928 -- Page 31
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721786&postcount=928>

Quote: > Originally Posted byniklasni1➡️I'm really curious about what the instruction set for something like this looks like. Does it have branching/looping at all? Or is it all straight ahead for N samples and then back to the beginning?For the Midiverb there are 4 instructions:- Read from current memory address, scale by 0.5 and add to accumulator.
- Clear accumulator, read from current memory address, scale by 0.5 and store to accumulator.
- Write from accumulator to current memory address, scale accumulator contents by 1.5.
- Scale by -1 and write from accumulator to current memory address, scale accumulator contents by -0.5.
Plus there are special instruction cycles for input (write the input from the ADC latch to the current memory address) and output (read from the current memory address and store in the left or right DAC latch).


That's it. No conditionals or anything; it just runs through the same 128 instructions for every sample. You don't really need anything more for reverb. 

Quote: > Originally Posted bypulsar modular➡️A few years ago I implemented the plate reverb described in a  white paper by Jon Dattorro. It sounds very good to me. I found it somewhat surprising as I got into it, that the type of schematic presented (some also in this thread) was more than a block diagram, in fact a very complete description of the algorithm. Do tools exist that configures usable code from such schematics, so you can test it directly? Seems quite possible and very useful. Is it perhaps too esoteric and pros build their own tools?Usually it's quickest to prototype it in something like Pure Data, Max/MSP or Reaktor. That way it can be tweaked in real time.

---

### Post #929 -- Page 31
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721850&postcount=929>

Quote: > Originally Posted byacreil➡️Basically, the Midiverb design is great at doing delay taps, allpass or lowpass filters with a 0.5 coefficient. And it's pretty crap at everything else. Trying to make a programmable reverb with a Schroeder topology is really an uphill battle. So it's no surprise that the MXR 01 sucked (also don't ever buy one because there's an inter-board connector that's terribly designed). I wouldn't expect a lot from the Alesis XT or XT:c either (far too little delay memory for the recirculating portion when factoring in the pre-delay, input allpasses and relatively high sample rate). The Midiverb/Midifex/Midiverb II are pretty much as good as it gets. At least until I program some better algorithms.I figured out how to do allpasses with a -0.25 or 0.75 coefficient, nested allpasses, plus some other stuff. I don't think an FDN is really in the cards. Maybe a very basic one, but it won't be very good.Currently I've got a 27C256 EPROM installed in mine with both the Midiverb and Midifex algorithms and a switch to select between them. But a 27C512 will fit too. I could easily program another 20 or 30 algorithms, plus "infinite reverb" variants of some of the existing algorithms. And I can modify the "bypass" algorithm so that it doesn't clear the delay memory when changing algorithms.Have you got 50? I've done a lot of stuff with my Midiverbs (yes, multiple) on 50. Or in some cases one on 49 driving one on 50. If you don't mind sharing, I would be hot to know what exactly makes 50 tick. I'm looking over 49 with great interest.


And I love allpasses with a 0.5 coefficient. It translates to native floating point numbers with a striking efficiency. It sounds a lot like employing lowpasses also with 0.5 multiplies is key to the technique? And not present in the brighter Midiverbs, though the 0.5 allpasses clearly are?

---

### Post #930 -- Page 31
**User:** toitoy
**Info:** Joined: Jul 2013Posts: 355My Studio🎧 10 years | Posts: 355My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721869&postcount=930>

Is anybody in to Melda's Turboreverb? I'd love to repeat these alogos there but I'm not to smart to do it on my own.


---

## Page 32

---

### Post #931 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15721912&postcount=931>

Quote: > Originally Posted bychrisj➡️Have you got 50? I've done a lot of stuff with my Midiverbs (yes, multiple) on 50. Or in some cases one on 49 driving one on 50. If you don't mind sharing, I would be hot to know what exactly makes 50 tick. I'm looking over 49 with great interest.I haven't drawn it out, but I think it's very similar to 49. I figured out that most of the algorithms that use the "hall" algorithm (these are 12 and 19-50; the ones that have a noticeable "buildup" in the reverb onset) use 6 allpasses on the input, but 49 and 50 only use 4. Apparently this is to dedicate more delay memory to the recirculating portion. Surprisingly, they're not complicated algorithms at all. They only use about 70 instructions. 

Quote: > It sounds a lot like employing lowpasses also with 0.5 multiplies is key to the technique? And not present in the brighter Midiverbs, though the 0.5 allpasses clearly are?It's just the easiest way to make it darker sounding. A variety of different filters are used, but the 0.5 coefficient lowpass is the most common. The models that depart from this would be the Midiverb III (which probably isn't worth bothering with), Microverb III (which should actually be pretty cool), Quadraverb, Midiverb 4, etc.

---

### Post #932 -- Page 32
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15722013&postcount=932>

Had a Microverb III and then a Quadraverb+. The latter I thought sounded smoother. The former often had ringing even on the mid-length decays, but not as much as an SPX90 does. Midiverb 4 sounds really lush.

---

### Post #933 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15722701&postcount=933>

Quote: > Originally Posted byDeleted 4768d8b➡️Had a Microverb III and then a Quadraverb+. The latter I thought sounded smoother. The former often had ringing even on the mid-length decays, but not as much as an SPX90 does. Midiverb 4 sounds really lush.Comparing something with 16Kwords of memory to anything with more is kind of inherently unfair. But the Microverb III has some more bloom algorithms and things.

---

### Post #934 -- Page 32
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15722787&postcount=934>

Quote: > Originally Posted byacreil➡️16kwords of memoryThat the Microverb III or the SPX90?

---

### Post #935 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15722845&postcount=935>

Quote: > Originally Posted byDeleted 4768d8b➡️That the Microverb III or the SPX90?Both. The Microverb III does a better job with it though.

---

### Post #936 -- Page 32
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15722869&postcount=936>

Quote: > Originally Posted byacreil➡️Both. The Microverb III does a better job with it though.Agreed. I did like the DMP7D (two SPX90 on board) I used to run one into the other.

---

### Post #937 -- Page 32
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15754791&postcount=937>

Wow this thread is still going. Haven’t been on here for a while, I kind of got burned out helping people repair stuff and disappeared for a bit, but I thought about this thread as I dug out one of my DSP projects to work on (Freescale DSP56366, which when I based a design on it back in 2008 it was quite new, and now is obsolete). Digging into the Alesis ‘verbs is quite neat, the giveaway to me was the 0.5 allpass coefficient.

---

### Post #938 -- Page 32
**User:** krabbencutter
**Info:** Joined: Dec 2015Posts: 213My Studio🎧 10 years | Posts: 213My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15763225&postcount=938>

Hey everyone,


two years ago I was fortunate enough to pick up an Ursa Major Stargate 323 in excellent condition for an incredible price. Fast forward to today and I've managed to recreate a low-level emulation for NI Reaktor:
[https://www.native-instruments.com/d...ry/show/14155/](https://www.native-instruments.com/de/reaktor-community/reaktor-user-library/entry/show/14155/)

It's available for free and also works in Reaktor Player with a 30min time limit. I'm also working on an open source VST plugin, but since C++ & JUCE are much more complex than Reaktor, it will probably be a couple of months before I'll have anything to show.


The Stargate 323 is a mono-to-stereo Reverb with a 32kHz sampling rate and 16 bit resolution. Compared to something like a Lexicon 480 the hardware design is pretty simplistic; which is great because otherwise this would have been an impossible task for me :D The Stargate 323 is all "discrete" logic clocked by a single 8MHz oscillator. By "discrete" I mean that there's no dedicated CPU and it's all just 74series ICs. But even with those limitations, there's an impressive amount of parallel computation going on. The circuit also has lots of quirks where the designers had to work around the limitations of specific components, most likely because it was cheaper to use stock they already had from the SST-282 than to source different parts. One example of this are the rotary switches for the reverb parameters. They are 4-bit gray code switches, which is a different encoding scheme than binary. And while there are 16 available settings for Pre-Delay, there are only 8 Reverb Programs and 8 Decay Times. So the designers used XOR-Gates to ensure the counting of bits 1-3 prefectly repeats after 8 rotations.


tl;dr: I've spent 18 months analysing all the eeprom data and the role of every single IC and transferred what I learned into code. While there's still some room for improvement the result sounds already very close to my hardware. And by "room for improvement" i mean "the tremolo sound of the last 5% of a 10s reverb tail at -40dB still needs some tuning" 

{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "@id": "https://youtube.com/v/ATupf1pVfAY",
  "name": "YouTube Video",
  "description": "Embedded YouTube video",
  "thumbnailUrl": "https://i.ytimg.com/vi/ATupf1pVfAY/hqdefault.jpg",
  "uploadDate": "2021-12-13T17:15:41+00:00",
  "contentUrl": "https://youtube.com/v/ATupf1pVfAY",
  "embedUrl": "https://youtube.com/embed/ATupf1pVfAY"
}

---

### Post #939 -- Page 32
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15763453&postcount=939>

Quote: > Originally Posted bykrabbencutter➡️Hey everyone,two years ago I was fortunate enough to pick up an Ursa Major Stargate 323 in excellent condition for an incredible price. Fast forward to today and I've managed to recreate a low-level emulation for NI Reaktor:https://www.native-instruments.com/d...ry/show/14155/It's available for free and also works in Reaktor Player with a 30min time limit. I'm also working on an open source VST plugin, but since C++ & JUCE are much more complex than Reaktor, it will probably be a couple of months before I'll have anything to show.The Stargate 323 is a mono-to-stereo Reverb with a 32kHz sampling rate and 16 bit resolution. Compared to something like a Lexicon 480 the hardware design is pretty simplistic; which is great because otherwise this would have been an impossible task for me :D The Stargate 323 is all "discrete" logic clocked by a single 8MHz oscillator. By "discrete" I mean that there's no dedicated CPU and it's all just 74series ICs. But even with those limitations, there's an impressive amount of parallel computation going on. The circuit also has lots of quirks where the designers had to work around the limitations of specific components, most likely because it was cheaper to use stock they already had from the SST-282 than to source different parts. One example of this are the rotary switches for the reverb parameters. They are 4-bit gray code switches, which is a different encoding scheme than binary. And while there are 16 available settings for Pre-Delay, there are only 8 Reverb Programs and 8 Decay Times. So the designers used XOR-Gates to ensure the counting of bits 1-3 prefectly repeats after 8 rotations.tl;dr: I've spent 18 months analysing all the eeprom data and the role of every single IC and transferred what I learned into code. While there's still some room for improvement the result sounds already very close to my hardware. And by "room for improvement" i mean "the tremolo sound of the last 5% of a 10s reverb tail at -40dB still needs some tuning"Very nice work...!


I have had a fair amount of experience with the Stargate 323 and 626, and have owned a SST-282 Space Station for decades.

One thing these devices seem to have in common is a topology of a reverb "tank"  feeding discrete output taps.  In the case of the SST-282 the tank is mono and uses modulated, non-interpolated delays and an analog feedback path to control the reverb length.

One of the characteristics of the 323 (and 626) is that the reverb produced can sound a little "phasey" and stagnant due to the timing of the output taps.


What did you discover in your analysis?

---

### Post #940 -- Page 32
**User:** krabbencutter
**Info:** Joined: Dec 2015Posts: 213My Studio🎧 10 years | Posts: 213My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15763655&postcount=940>

Quote: > Originally Posted byzmix➡️One of the characteristics of the 323 (and 626) is that the reverb produced can sound a little "phasey" and stagnant due to the timing of the output taps.Yeah, the 323 definitely has its own sound and imperfections, but at the same time it sounds like nothing else out there, which is why I love it so much 

Quote: > Originally Posted byzmix➡️What did you discover in your analysis?My analysis has been in complete ignorance of the actual algorithm. Because the 323 is all single-function logic ICs & eeproms I decided to rebuild the whole circuit logic in code. My assumption was that if I can accurately reproduce all the address & gain calculations for each incoming sample and subsequent delay taps, I should also get the exact same output.

---

### Post #941 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15779868&postcount=941>

Quote: > Originally Posted bykrabbencutter➡️two years ago I was fortunate enough to pick up an Ursa Major Stargate 323 in excellent condition for an incredible price. Fast forward to today and I've managed to recreate a low-level emulation for NI Reaktor:Great work. I had considered something similar at one point, but quickly abandoned it. The Space Station and Stargate models are based on a fundamentally very weird idea: a bunch of delay taps are summed together with global feedback. While this is simple and convenient (using a single analog feedback path and no digital multiplier), normally it's inherently unstable. So the Space Station modulates the delay taps, and the Stargate crossfades between the delay taps in a pretermined, periodic pattern. 


I didn't have the ROM dumps at the time, so I attempted to do it by randomly crossfading delay taps. It sounded *really* not promising, so I gave up after like an hour or two of messing around. Chris Moore must have been amazingly persistent. But I found that if you both modulate *and* crossfade the delay taps, it actually sounds great (and not all weird and semi-broken like the Ursa Major ones). I was completely surprised, since that's not really a sane way to do reverb. I was just doing it for giggles. 


The Ursa Major 8x32 also uses analog feedback and no DSP, but it's a more conventional Schroeder reverb with early reflection taps and no modulation, very similar to James A. Moorer's "About This Reverberation Business" paper. 


Other than Ursa Major, the only other digital reverb I know of that uses analog feedback is the Dynacord DRS78. But it apparently uses a more standard allpass loop topology, and as far as I can tell the design is kind of broken. As far as I remember, it should implement about 7 allpass filters in series. But it apparently uses the Schroeder 3 multiply topology, which uses gains g, -g and 1-g^2. It can multiply by 0.75, -0.75 and 0.5. If g is 0.75, 1-g^2 should be 0.4375, but it seems to use 0.5 instead. So they're not really allpass, and especially with feedback it sounds *really* metallic. But that's just my semi-informed analysis without owning one or having ROM dumps.

---

### Post #942 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15779873&postcount=942>

I'm still working on the Midiverb stuff. I've documented the first 40 or so algorithms. I wrote some stuff to find all the delay lengths automatically, so anymore it just takes a few minutes for each algorithm. 


They're mostly variants of the ones I posted earlier, but with a few surprises. Some of them take the outputs from the delay lines in the allpasses, and one (Midiverb algorithm 19) is completely broken. There's no feedback in the recirculating portion because something is written to (apparently) the wrong address. So there's an allpass that never makes it to the output and a lowpass filter that processes nothing. Overall there are two main topologies, but a lot of different variations to each. 


I tried the Microverb and Midiverb II as well (I don't have a ROM dump for the Microverb II), but this is considerably more difficult. I think I can see the instructions correctly (it's kinda different compared to the Midiverb), but the address increments seem to be somehow encrypted. As in they're exclusive-ored with a changing bit pattern. So that's going to be fun to figure out. My initial impression is that the algorithms appear to be modified versions of the Midiverb algorithms, with the ones in the Midiverb II being fancier and having more output taps.

---

### Post #943 -- Page 32
**User:** chrisj
**Info:** Joined: Aug 2004Posts: 5,680🎧 20 years | Posts: 5,680
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15780053&postcount=943>

Quote: > Originally Posted byacreil➡️I'm still working on the Midiverb stuff. I've documented the first 40 or so algorithms. I wrote some stuff to find all the delay lengths automatically, so anymore it just takes a few minutes for each algorithm.They're mostly variants of the ones I posted earlier, but with a few surprises. Some of them take the outputs from the delay lines in the allpasses, and one (Midiverb algorithm 19) is completely broken. There's no feedback in the recirculating portion because something is written to (apparently) the wrong address. So there's an allpass that never makes it to the output and a lowpass filter that processes nothing. Overall there are two main topologies, but a lot of different variations to each.I tried the Microverb and Midiverb II as well (I don't have a ROM dump for the Microverb II), but this is considerably more difficult. I think I can see the instructions correctly (it's kinda different compared to the Midiverb), but the address increments seem to be somehow encrypted. As in they're exclusive-ored with a changing bit pattern. So that's going to be fun to figure out. My initial impression is that the algorithms appear to be modified versions of the Midiverb algorithms, with the ones in the Midiverb II being fancier and having more output taps.I'd love to see more of this. I have no intention on 'doing' a Midiverb plugin, but I'd like to do isolated algorithms I enjoyed (like 50) and try to get 'em to sound correct ITB at modern sampling rates etc. It'd be like how I did 'Mackity': first get an algorithm, presumably with some sort of undersampling, then get the output stage sounding right (which can have some interesting quirks to it).


The sufficiently diligent open source user would be able to build on my work to 'do' a Midiverb plugin with everything, provided it honored the MIT license

---

### Post #944 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15786775&postcount=944>

Quote: > Originally Posted bychrisj➡️I'd love to see more of this. I have no intention on 'doing' a Midiverb plugin, but I'd like to do isolated algorithms I enjoyed (like 50) and try to get 'em to sound correct ITB at modern sampling rates etc. It'd be like how I did 'Mackity': first get an algorithm, presumably with some sort of undersampling, then get the output stage sounding right (which can have some interesting quirks to it).The sufficiently diligent open source user would be able to build on my work to 'do' a Midiverb plugin with everything, provided it honored the MIT licenseI think there are two ways to approach it. The first would use different "prototype" algorithms that are generalizations of Midiverb/Midifex algorithms. All the presets would just be these with different delay lengths, coefficients and output taps (I suppose I need to organize these in a spreadsheet). And all the parameters could be made available to the user for editing, including arbitrary coefficients and longer delays than what's possible in the Midiverb. I'm going to do this in Pure Data (since there aren't a lot of decent reverbs available in Pd, other than the ones I've made). But making a decent user interface will be difficult. I can't really see a good way to make that level of editing user friendly. For this approach I think it would be more or less sufficient to just do resampling, anti-aliasing and reconstruction filtering, with optional ADC/DAC clipping.


The second option would be an exact emulation that's numerically accurate and runs the exact same algorithms (including new algorithms and whatever can be adapted from other models). In some ways I think that would be simpler to do, but it would be much less efficient. Probably for copyright reasons it would be best to load external ROM files like a game console emulator. This opens the door to all sorts of promising low-level glitchy weirdness, like new algorithms that have intentional clipping, quantization distortion or unstable feedback, instantaneous switching between effects without clearing the delay memory (I want to modify the CPU ROM in mine to do this), "infinite" algorithms that repeat the delay memory contents in various (erroneous) ways, and storage of multiple delay memory banks that can be switched in a manner analogous to a sampler. And it would be the definitive "perfect" emulation. It won't be easily editable, but new algorithms could be created with an assembler. 


It's numerically weird, so there are definite advantages to emulating it exactly. The ADC is 12 bit (connecting to data bus bits D12 to D1) and the DAC is 13 bit (D12 to D0). This should seem strange to you, because typically there are extra LSBs used as guard bits to avoid audible limit cycles. Here it's got extra MSBs instead. The problem is that there's no saturation arithmetic. The DAC saturates (highly audible on the longer reverb algorithms), but the DSP portion just overflows, so the extra bits are used to get a little more headroom. Limit cycles are prevented by rounding toward zero, which contributes some distortion. Also, since it only uses a hardwired binary shift, each gain coefficient may lose up to 2-3 bits of precision, depending on how it's implemented. For example, the Midiverb gets -0.84375 by doing 0.5 * -0.5 * 1.5 * 1.5 * 1.5. Just multiplying and quantizing to 16 bits won't be equivalent. There are a few places where this introduces considerable distortion. 


It crossed my mind to do a plugin, but I don't want to spend the rest of my life working on this. When I'm done I'll probably just clean up the code and documentation and GPL everything. I wanted to figure out the Microverb and Midiverb II (and the Microverb II if I can get a ROM dump) as well, because they have at least some similar algorithms. It would be nice to have a single set of data that covers all of them, but figuring those out is more involved than I expected. And the modulation effects in the Midiverb II are another issue entirely. I should probably just finish all the Midiverb/Midifex stuff first. I expect the Alesis XT/XT:c can be similarly reverse engineered, but I doubt the reverbs are very good. I'll do it if someone sends them to me for free. I'm not paying ebay money for that junk.


I also made some nice new algorithms that I'd like to run on the hardware. The goal was to use all the delay memory for the recirculating part, in order to minimize any metallic quality. I found that nested allpasses are great for this. I got pretty much my ideal reverb sound (at least for hall style reverbs): a few sparse initial echoes and a quick buildup of density. And I came up with a clever way to tune it with only a few parameters, constraining the delay lengths so that they don't exceed the maximum (about 699 ms).

---

### Post #945 -- Page 32
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15787391&postcount=945>

Quote: > Originally Posted byacreil➡️I think there are two ways to approach it. The first would use different "prototype" algorithms that are generalizations of Midiverb/Midifex algorithms. All the presets would just be these with different delay lengths, coefficients and output taps (I suppose I need to organize these in a spreadsheet).…..I also made some nice new algorithms that I'd like to run on the hardware. The goal was to use all the delay memory for the recirculating part, in order to minimize any metallic quality. I found that nested allpasses are great for this. I got pretty much my ideal reverb sound (at least for hall style reverbs): a few sparse initial echoes and a quick buildup of density. And I came up with a clever way to tune it with only a few parameters, constraining the delay lengths so that they don't exceed the maximum (about 699 ms).I built two hardware reverbs, one using the Alesis AL3202 reverb IC, the other using an NXP DSP (56366/56367). What I ended up doing when I got to the NXP system was write some generic DSP routines for a two tap summer, a multi tap summer, and a two multiply allpass, all using the same ‘z-1’ memory structure. Then I wrote a simple RTOS, a sort of generic effect setting editor via the front panel LCD that used two rotary encoders, and a few push buttons. In the middle is where I made it generic, but I never did write a user friendly way of making different algorithms. basically they are implemented as arrays of structures where you arrange taps and gains, and can add size scalars (from the setting editor) to the tap locations, amplitude scalars (same thing), and a limited number of chorus taps. Anyways, it was abstracted in such a way that the DSP code hardly ever needed changing. In theory I could make an effect with a knob for every tap or filter location and amplitude, and I do that for development sometimes, but usually I distill it down to 5-15 user adjusted parameters per effect. The host software and about 10 reverb and delay algorithms take up about 150k on a Coldfire V1, the DSP code is probably less than 1000 24-bit instructions. I was thinking of writing up a graphical editor on the PC similar to the Eventide package but I’m not the best at PC GUI programming. I don’t know if this gives you any ideas but I thought I’d share the general architecture of what I did. I implemented this in parallel with the steps at the start of this thread, I think that was 12 or 15 years ago.


The other hardware I built was the same host processor (Coldfire V1) plus the AL3202 DRE. It looked like the Midiverb hardware was an inspiration. It’s a nice bit of hardware and quite easy to use.


I also like nested all pass filters, I find it easier to get a good echo density without really high coefficients, often I set them in the 0.25 to 0.6 area, and they don’t sound metallic down there.

---

### Post #946 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15789183&postcount=946>

Quote: > Originally Posted bydale116dot7➡️I built two hardware reverbs, one using the Alesis AL3202 reverb IC, the other using an NXP DSP (56366/56367). What I ended up doing when I got to the NXP system was write some generic DSP routines for a two tap summer, a multi tap summer, and a two multiply allpass, all using the same ‘z-1’ memory structure. Then I wrote a simple RTOS, a sort of generic effect setting editor via the front panel LCD that used two rotary encoders, and a few push buttons. In the middle is where I made it generic, but I never did write a user friendly way of making different algorithms. basically they are implemented as arrays of structures where you arrange taps and gains, and can add size scalars (from the setting editor) to the tap locations, amplitude scalars (same thing), and a limited number of chorus taps. Anyways, it was abstracted in such a way that the DSP code hardly ever needed changing. In theory I could make an effect with a knob for every tap or filter location and amplitude, and I do that for development sometimes, but usually I distill it down to 5-15 user adjusted parameters per effect. The host software and about 10 reverb and delay algorithms take up about 150k on a Coldfire V1, the DSP code is probably less than 1000 24-bit instructions. I was thinking of writing up a graphical editor on the PC similar to the Eventide package but I’m not the best at PC GUI programming. I don’t know if this gives you any ideas but I thought I’d share the general architecture of what I did. I implemented this in parallel with the steps at the start of this thread, I think that was 12 or 15 years ago.I'm prototyping it in Pure Data (and meanwhile also making fancy versions of the same basic algorithms), so it's easy to modify and tune it. I wrote out some stuff on paper, like nested allpasses and different gains, so I know more or less what's feasible in the hardware. I've yet to finish the assembler, but it's going to load .txt files and spit out both impulse responses and a binary file that I can burn to an EPROM. I'm doing this is Octave/Matlab. I'm sure Python would have been a better choice, but I'm more familiar with Matlab. The only really tricky thing here is that if I try to do anything really weird, it won't be reflected in the impulse response. So that will be more trial and error. The goal is to get maybe 256 total effects, and switch between them instantaneously without clearing the delay memory. Then they can be sequenced over MIDI. I got the idea partly from the Dynacord DRS78, which can use a trigger pulse to toggle between reverb and delay modes, as well as different delay times. This doesn't clear the memory, and it even changes the sample rate for extra weirdness. 


I got good high level controls with the nested allpass algorithm. Currently there are 4 nested allpasses (I'll make a fancier version with an arbitrary number). The relevant parameters are total delay time, spread (the delay times for each allpass are logarithmically distributed over this range), and then 3 parameters to proportionally scale the relative lengths of the inner allpass delay, the outer allpass delay, and the delay after each allpass. Changing any of those parameters actually changes all the delay times simultaneously, and they always sum to the same total delay time. The only low level manual twiddling is the delay times for the output taps, and those are set as a percentage of the delay after each allpass. It's not totally intuitive, and it takes some careful adjustment to get a good sound. But it's fairly quick and simple, and it ends up being very flexible. It's a nice balance between having minimal controls that don't permit fine tuning, and full manual control where it's too easy to go off into the weeds. 


The problem with trying to edit the existing Midiverb algorithms is that generally the different loop gains are all wonky and mismatched. There can be high level controls that set them all uniformly, globally scale the delay times, etc., but that won't be able to get the same sound as manually adjusting everything. Many of the Midifex algorithms would be neat if they were editable, but they're kind of useless as just preset delay/filter/allpass chain effects.

---

### Post #947 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15789184&postcount=947>

This is how I partied for new year's. It's also my cat's birthday, so I had to party extra hard.

---

### Post #948 -- Page 32
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15789409&postcount=948>

These are great! Thank you for sharing

---

### Post #949 -- Page 32
**User:** sergio_frias_23
**Info:** Joined: Jan 2012Posts: 62🎧 10 years | Posts: 62
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15789432&postcount=949>

[https://www.youtube.com/watch?v=5DYbirWuBaU](https://www.youtube.com/watch?v=5DYbirWuBaU)


more on reverse enginering the midiverb

---

### Post #950 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15790414&postcount=950>

Quote: > Originally Posted bysergio_frias_23➡️https://www.youtube.com/watch?v=5DYbirWuBaUmore on reverse enginering the midiverbI'm gonna do better than that. "There's no schematic." lol what's this then?

---

### Post #951 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15790429&postcount=951>

part 2

---

### Post #952 -- Page 32
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15796436&postcount=952>

Quote: > Originally Posted byacreil➡️I'm gonna do better than that. "There's no schematic." lol what's this then?

He does have a schematic, apparently..


{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "@id": "https://youtube.com/v/JNPpU08YZjk",
  "name": "YouTube Video",
  "description": "Embedded YouTube video",
  "thumbnailUrl": "https://i.ytimg.com/vi/JNPpU08YZjk/hqdefault.jpg",
  "uploadDate": "2022-01-07T02:59:41+00:00",
  "contentUrl": "https://youtube.com/v/JNPpU08YZjk",
  "embedUrl": "https://youtube.com/embed/JNPpU08YZjk"
}

---

### Post #953 -- Page 32
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15796505&postcount=953>

This one looks like he or someone else drew it up from a PC board. I think Keith said he used a drafting table and tape for the original, not CAD. This was a nice video. The hardware design here is pretty clever.

---

### Post #954 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15796592&postcount=954>

Quote: > Originally Posted byzmix➡️He does have a schematic, apparently..Yeah but they had to draw the whole thing. I never would have bothered. Having the official schematic gave me some nightmares though because it doesn't show the arithmetic right shift. I had to find that with a multimeter.


Credit goes to Robin Whittle for the Midiverb schematic and the Midifex ROM dump, by the way.


I have to give them credit for noticing a couple things I didn't (mainly that the lower 5 DAC bits are left floating when it saturates), but I also noticed a few errors and omissions and overall found the whole thing a bit confusing and overcomplicated. It's nice to check my work against someone else's. I thought I'd screwed up the filter modeling because of the high frequency peak; surprisingly it's actually supposed to do that.

---

### Post #955 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15797500&postcount=955>

Here's the last installment for now. I skipped some because they're reverb or multitap algorithms that are best described elsewhere. Some of them are confusing as hell. The filters are already a pain to figure out, but sometimes there's no consistency regarding the way they're implemented, and occasionally there are complicated filters implemented that aren't even used. So I'm making a lot of mistakes. It would be interesting to see what kind of development environment Keith Barr had cooked up; I'm sure it didn't resemble what I'm looking at. Overall my conclusion is that the Midifex likely has the weirdest collection of algorithms of any commercial product. For the most part they're not particularly useful, but they're certainly inventive.

---

### Post #956 -- Page 32
**User:** CEM3310
**Info:** Joined: Mar 2017Posts: 189🎧 5 years | Posts: 189
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15797646&postcount=956>

Great work! Unfortunately the diagrams seem very pixelated so it's very hard to see much of the detail.


UPDATE: Actually forget that, it was just me being a bit stupid, can now see the details much better. Again, great work and many thanks for sharing with us.

---

### Post #957 -- Page 32
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15797678&postcount=957>

Quote: > Originally Posted byCEM3310➡️Great work! Unfortunately the diagrams seem very pixelated so it's very hard to see much of the detail.UPDATE: Actually forget that, it was just me being a bit stupid, can now see the details much better. Again, great work and many thanks for sharing with us.All images get automatically resized by the forum software. They're not great but they should be at least sorta legible. I'll make .pdf files eventually.

---

### Post #958 -- Page 32
**User:** FETHead
**Info:** Joined: Oct 2008Posts: 26🎧 15 years | Posts: 26
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15799676&postcount=958>

Quote: > Originally Posted byacreil➡️The SPX90 is really underpowered. 64 instructions but only 32 memory reads/writes.Butit has 16 channel hardware-based modulation that's better than what everyone else was doing. Hence the symphonic and dual pitch shift algorithms.Yamaha kind of disappoint me in the effect processor department. The REV1 was the most powerful thing around until maybe the Lexicon 480L or Roland R880. The SPX90 and REV7 kind of suck (other than the symphonic effect). The REV5 sounds pretty good, but there's nothing exciting about it. For the most part they were well behind the competition and just rehashed the same stuff for years. I'll be even more disappointed if everything just turns out to be Schroeder reverbs.Always wondered why 16 modulators, it's seems like a lot, as far as I can tell not all is used in the symphonic, which leaves the pitch change programs, but 8 modulators a side seems too much me.  The best Yamaha I heard was the ProR3, plates weren't great but the halls were nice.

---

### Post #959 -- Page 32
**User:** FETHead
**Info:** Joined: Oct 2008Posts: 26🎧 15 years | Posts: 26
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15799717&postcount=959>

Quote: > Originally Posted bykrabbencutter➡️tl;dr: I've spent 18 months analysing all the eeprom data and the role of every single IC and transferred what I learned into code. While there's still some room for improvement the result sounds already very close to my hardware. And by "room for improvement" i mean "the tremolo sound of the last 5% of a 10s reverb tail at -40dB still needs some tuning"Maybe tweak and measure that obscure "Rate Level to ADS", as mentioned in the service manual, your unit might have drifted over time. It's by far the strangest thing I've seen in a reverb, and not totally sure I understand what it does, think it controls the tap-fade rate based on the input that is bandpassed.

---

### Post #960 -- Page 32
**User:** dale116dot7🎙️
**Info:** Joined: Dec 2003Posts: 1,142My Studio🎧 20 years | Posts: 1,142My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15800281&postcount=960>

It’s interesting how different units do the LFOs, and on Lexicons, how long the Z80 lived in that spot. Yes, 64 instructions seems a bit low. I liked the AL3201, but I kind of wished it had double the RAM. But with the 8 bit multiplier, you could do a lot with the 128 instructions. The other thing that I would have liked is two ADC/DAC ports. You could have cascaded two or more of the ICs in creative ways with that arrangement. Has anyone studied the DN780 much? It used a ADSP1010 MAC chip.

