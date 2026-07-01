
---

## Page 33

---

### Post #961 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15802416&postcount=961>

Quote: > Originally Posted byFETHead➡️Always wondered why 16 modulators, it's seems like a lot, as far as I can tell not all is used in the symphonic, which leaves the pitch change programs, but 8 modulators a side seems too much me.  The best Yamaha I heard was the ProR3, plates weren't great but the halls were nice.I think the YM3807 modulator IC was initially designed to be a hardware LFO in the HX series Electones, and then later it was also used to smooth control data in the DMP7. Yamaha were really careful in their high end models to use smooth, hardware-based modulation for everything. But stuff like the DX7 wasn't fancy enough for that, so it's only got software generated pitch modulation. The SPX90 probably never uses more than 8 modulators at a time, but it wasn't made for the SPX90.


From comparing the user manuals, the ProR3 looks very similar to the REV5. I find it totally usable but unexciting. The SPX90 and REV7 reverbs sound kind of awful, but they have their uses too.

Quote: > Originally Posted byFETHead➡️Maybe tweak and measure that obscure "Rate Level to ADS", as mentioned in the service manual, your unit might have drifted over time. It's by far the strangest thing I've seen in a reverb, and not totally sure I understand what it does, think it controls the tap-fade rate based on the input that is bandpassed.My best guess is that it was intended to increase the rate of modulation when an input signal is present (to make it more stable?), and then slow it when there's no input signal (to make the tails smoother?). I haven't looked at it in years but I remember getting the impression that it wasn't used anymore after some ROM revisions. 

Quote: > Originally Posted bydale116dot7➡️The other thing that I would have liked is two ADC/DAC ports. You could have cascaded two or more of the ICs in creative ways with that arrangement.Yamaha did that too in the REV7 and REV5. Each of the YM3804 ICs has 4 input channels and 4 output channels. I'd love to reverse engineer that hardware since it covers a huge number of different implementations, but I don't think I'm ready for that headache at the moment. 

Quote: > Originally Posted bydale116dot7➡️Has anyone studied the DN780 much? It used a ADSP1010 MAC chip.I looked at it a little. If I remember right, it looks like 128 instruction, 32Kx16 memory, no modulation. It's a nice reference design but not anything super special.

---

### Post #962 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15815520&postcount=962>

Guess what this is. You won't get it right, but guess anyway.

---

### Post #963 -- Page 33
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15815551&postcount=963>

Quote: > Originally Posted byacreil➡️Guess what this is. You won't get it right, but guess anyway.All those parallel combs and diffusion on the outputs... I feel like the separate ER delay should be a giveaway...  It's something with MIDI based on the clock rate..  is it even a reverb?

---

### Post #964 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15815571&postcount=964>

Quote: > Originally Posted byzmix➡️All those parallel combs and diffusion on the outputs... I feel like the separate ER delay should be a giveaway...  It's something with MIDI based on the clock rate..  is it even a reverb?Yeah it's a reverb. You might have one. Someone here does, I don't remember if it's you.


The notable thing is the way the combs are tuned. The delay times are very close. This seems like a horrible idea, but the multiple output taps on each one ensure that the echoes are pretty evenly distributed. I was thinking recently that one of the main problems with parallel comb filters is that the echoes inevitably bunch up somewhere, and other times leave a gap as long as the shortest delay length. This seems to solve that problem without any metallic resonances (other than the allpasses, which make short decay times sound very metallic).


This also isn't the complete algorithm. There's another part that I haven't looked at yet. But you'll get just this if the parameters are set a certain way.

---

### Post #965 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15821025&postcount=965>

Check this shit out. Allpass chain? No problem. 


Hmm, what am I messing with this time (while I should be doing something else)?

---

### Post #966 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15823814&postcount=966>

{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "@id": "https://youtube.com/v/h9o5_W6hn9k",
  "name": "YouTube Video",
  "description": "Embedded YouTube video",
  "thumbnailUrl": "https://i.ytimg.com/vi/h9o5_W6hn9k/hqdefault.jpg",
  "uploadDate": "2022-01-23T23:20:10+00:00",
  "contentUrl": "https://youtube.com/v/h9o5_W6hn9k",
  "embedUrl": "https://youtube.com/embed/h9o5_W6hn9k"
}

---

### Post #967 -- Page 33
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15823845&postcount=967>

Dumb question: Are the feedback loops really independent (not summed at the input or in series)?

---

### Post #968 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15823878&postcount=968>

Quote: > Originally Posted byzmix➡️Dumb question: Are the feedback loops really independent (not summed at the input or in series)?Correct. I'm 100% certain of the delay times and topology. I implemented it in Pure Data for troubleshooting purposes and I completely nailed it (see pic). 


The thing I'm less confident about is the loop filters. I'm not sure if they're shelf filters or not. It's hard to tell from the test recordings I made. Not that it's really that important.

---

### Post #969 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15827818&postcount=969>

Here's one from a very popular effect processor (actually a later related model with a different sample rate). I'm not sure about the gains, and I left out the highpass/lowpass filtering on the input.


It's really... not good. Worse than I expected.

---

### Post #970 -- Page 33
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15828865&postcount=970>

Yamaha?

---

### Post #971 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15829084&postcount=971>

Quote: > Originally Posted byDeleted 4768d8b➡️Yamaha?Yeah. It's the vocal algorithm from the FX900, which is a rehash of the SPX90. Same thing in the FX500, etc. I should do a more thorough job of it later, but I think it's basically the right idea. 


I'd really hoped for better. I know the processor is extremely underpowered, but this just seems brain damaged. They could have dropped the early reflection taps and given all the combs the same number of output taps. This kind of doesn't bode well for the other Yamaha reverbs, and I can't imagine the crappiness of the TG77/TG33/V50, etc. reverbs, which sound much worse.


Anyway I'm only dipping my toes into this stuff so far, but it's easier than I expected. It's not trivial, but not impossibly difficult either. So I'm gonna reverse engineer and disclose every commercial reverb algorithm ever. And maybe I'll manage to kill the stupid myth that vintage hardware reverbs have a "super magic 3D sound" or "superior processing power" that VSTs can't possibly match. It seems to me that most of the classic stuff isn't all that great.

---

### Post #972 -- Page 33
**User:** oldgearguy
**Info:** Joined: Sep 2002Posts: 5,007🎧 20 years | Posts: 5,007
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15829094&postcount=972>

This has been an excellent thread and I very much appreciate the deep dive you're doing across the vintage hardware landscape.  Having owned a lot of it over the years, I certainly kept my favorites, but it's cool to see 'under the covers' so to speak.


My only comment is that yeah - maybe they weren't so great, but in context a lot of the older gear worked well, whether it was because the results were getting additionally processed by going through a console+tape or because the weird frequency peaks and such fit with the other instrumentation around it, or maybe just very good engineers squeezing out the maximum possibilities from what they had.


For older people looking back, the sound of this gear has been imprinted in our memories from hearing it so much on so many records over the years that it's hard to separate the harsh reality from the cloud of nostalgia.

---

### Post #973 -- Page 33
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15829189&postcount=973>

Quote: > Originally Posted byacreil➡️It seems to me that most of the classic stuff isn't all that great.Agreed. Totally subjective, but I admired the H3000 and Sony DPS V77 more than any Yamaha (rev 7 or SPX90) and even, heretically, the Lexicon 224XL (that was quite underwhelming when I used one around 2000).  That Sony had genuinely beautiful reverbs. Maybe you'll bust that to a myth too 


SPX2000 was quite OK as are whatever they put in the PM5D.


Those are the only machines I spent a lot of time with excluding all the cheap Alesis. I kept the Quadraverb for the longest time.

---

### Post #974 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15829543&postcount=974>

Quote: > Originally Posted byoldgearguy➡️This has been an excellent thread and I very much appreciate the deep dive you're doing across the vintage hardware landscape.  Having owned a lot of it over the years, I certainly kept my favorites, but it's cool to see 'under the covers' so to speak.My only comment is that yeah - maybe they weren't so great, but in context a lot of the older gear worked well, whether it was because the results were getting additionally processed by going through a console+tape or because the weird frequency peaks and such fit with the other instrumentation around it, or maybe just very good engineers squeezing out the maximum possibilities from what they had.For older people looking back, the sound of this gear has been imprinted in our memories from hearing it so much on so many records over the years that it's hard to separate the harsh reality from the cloud of nostalgia.The thing that got to me was watching a Yamaha REV7 demo video on youtube. Through the whole thing I found myself thinking, "God, I'm glad I never bought one of those." And all the comments are saying, "VSTs can't touch this sound!" Meanwhile it sounds about as good as I'd expect from a free VST from 20 years ago.


I think a lot of it is just that certain stuff set the standard. The EMT 250 and AMS RMX16 did their thing in a distinctive way that made an impact on the way people recorded. But it doesn't mean they're unsurpassed. If you could go back to 1980 and give producers some crap Digitech that no one cares about, that would have been used all over everything too. 

Quote: > Originally Posted byTomás Mulcahy➡️Agreed. Totally subjective, but I admired the H3000 and Sony DPS V77 more than any Yamaha (rev 7 or SPX90) and even, heretically, the Lexicon 224XL (that was quite underwhelming when I used one around 2000).  That Sony had genuinely beautiful reverbs. Maybe you'll bust that to a myth tooSPX2000 was quite OK as are whatever they put in the PM5D.Those are the only machines I spent a lot of time with excluding all the cheap Alesis. I kept the Quadraverb for the longest time.The Lexicon 224 models are a lot more impressive once you realize that the hardware isn't very capable. They really got as much as possible out of barely adequate resources. There's probably more ingenuity there than anywhere else. 


As for Sony, maybe I'm working on that already

---

### Post #975 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15833216&postcount=975>

Here's one that I like. It's not perfect, but it sounds pretty good. It's not the same model as the other 32 kHz reverb I posted previously. 12 early reflection taps, 4 allpasses, 6 combs with 2 taps each. 


This one gave me some trouble. The issue is that the comb output taps come both at the end and exactly in the middle of the delay. This would seem like a really not smart thing to do; if the feedback is positive, it would be (almost) exactly the same as a comb filter with half the delay length, thus wasting both delay taps and memory. But here the feedback is negative, so the resulting echoes are a repeating pattern of positive, positive, negative, negative, which is different from what you'd get with half the delay length. I'm not convinced that this is really a good idea, but it doesn't reduce modal density compared to a more irregular tap spacing, so it doesn't just waste the memory. 


I'm getting the impression that most commercial reverbs were Schroeder variants, at least in the 80s and 90s.

---

### Post #976 -- Page 33
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15833248&postcount=976>

Quote: > Originally Posted byacreil➡️...some crap Digitech that no one cares about...Yes! Their reverbs were always *awful*. They have a good rep for pitch shifting though. I am still using a Digitech Vocalist II. Nothing else sounds quite like it. I hope some day it becomes a plugin. Anyone know who IVL Technologies were/ are? That's what it says when it boots up.

---

### Post #977 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15833988&postcount=977>

Quote: > Originally Posted byDeleted 4768d8b➡️Yes! Their reverbs were alwaysawful. They have a good rep for pitch shifting though. I am still using a Digitech Vocalist II. Nothing else sounds quite like it. I hope some day it becomes a plugin. Anyone know who IVL Technologies were/ are? That's what it says when it boots up.I don't think the Digitech stuff was bad; at least the later S-DISC processors were pretty advanced. Although I got a Digitech RP200 for free; that thing is completely useless. IVL initially made pitch-to-MIDI boxes for various instruments, and they had a lot of patents for pitch tracking algorithms and PSOLA pitch shifters (if I remember right). But I don't think the IVL products sold very well on their own. They designed an IC that was licensed by Digitech and used in the Whammy, IPS33, etc. And these were eventually developed into vocal harmony processors. These weren't the first PSOLA pitch shifters; the Korg DVP-1 came out before that in 1986. But Korg seemed to miss their opportunity to market it effectively, and they never followed up on it. 


The stupid thing is that the other Digitech effects didn't use the IVL IC. So lots of products made by a company known for very good pitch shifting actually had crappy constant splice rate pitch shifters, including the RP series guitar processors. They have the foot pedal and the "Whammy" effect, but they sound horrible.

---

### Post #978 -- Page 33
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15834050&postcount=978>

Forgot about the S-Disc processors. But ya prior to that I never heard a good reverb from them. Never heard the S-Disc either. I thought the Whammy pedal was really good though!


So it's a chip? I must pop open the Vocalist and take a look.

[http://www.muzines.co.uk/articles/perfect-pitch/7227](http://www.muzines.co.uk/articles/perfect-pitch/7227)
[http://www.muzines.co.uk/articles/ivl-steelrider/807](http://www.muzines.co.uk/articles/ivl-steelrider/807)

---

### Post #979 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15834099&postcount=979>

Quote: > Originally Posted byDeleted 4768d8b➡️Forgot about the S-Disc processors. But ya prior to that I never heard a good reverb from them. Never heard the S-Disc either. I thought the Whammy pedal was really good though!Before S-DISC they used the HISC chip, which was not really great but not terrible either. And before that the RDS 6400 and 6500, which may have used something different. I'm vaguely curious about those, but not enough to actually buy one. 

Quote: > So it's a chip? I must pop open the Vocalist and take a look.It was a custom chip initially, I think the later ones used general purpose DSPs.

---

### Post #980 -- Page 33
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15834273&postcount=980>

Actually it was ART reverbs I was thinking of not Digitech. Oops! I used two or three different models in the nineties and they were dreadful. I can't remember which ones. Lots of pink paint on the front. 1U.

---

### Post #981 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15834370&postcount=981>

Quote: > Originally Posted byDeleted 4768d8b➡️Actually it was ART reverbs I was thinking of not Digitech. Oops! I used two or three different models in the nineties and they were dreadful. I can't remember which ones. Lots of pink paint on the front. 1U.Oh yeah those are really, *really* bad. Maybe there's a worse reverb out there somewhere built into a crappy practice amp, but if there is, I haven't heard it. The later ART DMV-Pro seems alright though.

---

### Post #982 -- Page 33
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,229🎧 20 years | Posts: 5,229
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15835823&postcount=982>

Quote: > Originally Posted byacreil➡️But I found that if you both modulateandcrossfade the delay taps, it actually sounds great (and not all weird and semi-broken like the Ursa Major ones). I was completely surprised, since that's not really a sane way to do reverb. I was just doing it for giggles.

I'd love to hear that. Is it sufficiently different from anything already existing to make it into a product (plugin)?

---

### Post #983 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15836065&postcount=983>

Quote: > Originally Posted byliving sounds➡️I'd love to hear that. Is it sufficiently different from anything already existing to make it into a product (plugin)?It's available if you can tolerate using Pure Data, but it's not user friendly. It's definitely different, but might be too weird and complicated for a product. I've used it as my main reverb for years.

---

### Post #984 -- Page 33
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,229🎧 20 years | Posts: 5,229
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15836286&postcount=984>

Quote: > Originally Posted byacreil➡️It's available if you can tolerate using Pure Data, but it's not user friendly. It's definitely different, but might be too weird and complicated for a product. I've used it as my main reverb for years.How do you integrate Pure Data into your setup? Can you compile a VST-plugin? I'd definitely like to try. :-)

---

### Post #985 -- Page 33
**User:** toitoy
**Info:** Joined: Jul 2013Posts: 355My Studio🎧 10 years | Posts: 355My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15836484&postcount=985>

Quote: > Originally Posted byliving sounds➡️How do you integrate Pure Data into your setup? Can you compile a VST-plugin? I'd definitely like to try. :-)[https://github.com/logsol/Pd-Pulp](https://github.com/logsol/Pd-Pulp)

This is an audio plugin that enables you to run pd patches inside your DAW. You can use the automation feature of your DAW to control up to 10 parameters of the loaded pd patch.

---

### Post #986 -- Page 33
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,229🎧 20 years | Posts: 5,229
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15836500&postcount=986>

Quote: > Originally Posted bytoitoy➡️https://github.com/logsol/Pd-PulpThis is an audio plugin that enables you to run pd patches inside your DAW. You can use the automation feature of your DAW to control up to 10 parameters of the loaded pd patch.Great, thanks!


 @
[acreil](https://gearspace.com/board/member.php?u=143351)
: Is there a place where I can download your algorithm? Thanks!

---

### Post #987 -- Page 33
**User:** Avast!
**Info:** Joined: Oct 2010Posts: 373My Recordings/Credits🎧 15 years | Posts: 373My Recordings/Credits
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15837484&postcount=987>

I'm just a piker in this discussion, but have been following it for ages.


I have -good- reverbs now, but one old one i liked was the Sony/Ibanez SDR1000. Acreil or anyone have commentary or analysis of it? 


I loved the reverbs when and only when I dialed the HF recirculation down to 1% or maybe a few percent, leaving a dark shell of a room, which i could use TONS of.

---

### Post #988 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15838717&postcount=988>

Quote: > Originally Posted byliving sounds➡️Great, thanks!@acreil: Is there a place where I can download your algorithm? Thanks!It's in pretty much all the PD patches I've uploaded (reverb727~). [Like this one](https://acreil.wordpress.com/2020/01/13/pure-data-frequency-domain-filtering-patch/). I'd like to make a video explaining it in detail, but it's complicated. I'm working on some more conventional reverbs (and some less conventional ones). Hopefully those will be more usable. 

Quote: > Originally Posted byliving sounds➡️How do you integrate Pure Data into your setup? Can you compile a VST-plugin? I'd definitely like to try. :-)I don't have to integrate anything because I either do everything in PD or do everything with hardware. 

Quote: > Originally Posted byAvast!➡️I'm just a piker in this discussion, but have been following it for ages.I have -good- reverbs now, but one old one i liked was the Sony/Ibanez SDR1000. Acreil or anyone have commentary or analysis of it?I loved the reverbs when and only when I dialed the HF recirculation down to 1% or maybe a few percent, leaving a dark shell of a room, which i could use TONS of.I like the SDR1000 a lot (although I wish I had the SDR1000+ ROM in mine). It's got a nice low sample rate (26 kHz), lots of delay memory (64K x 16), real stereo in/stereo out (I think it's the first mid-priced model to offer this). And it can sound very strange on percussive sounds if misused, so it has an interesting character that more advanced processors often lack. Analysis will come soon-ish.

---

### Post #989 -- Page 33
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,229🎧 20 years | Posts: 5,229
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15840162&postcount=989>

Quote: > Originally Posted bytoitoy➡️https://github.com/logsol/Pd-PulpThis is an audio plugin that enables you to run pd patches inside your DAW. You can use the automation feature of your DAW to control up to 10 parameters of the loaded pd patch.This doesn't run on Windows or MacOS, does it? 


Is there a way to try out the reverb without installing Linux or learning to program a RasPi first?

---

### Post #990 -- Page 33
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15842403&postcount=990>

Here's another one; it's fairly elaborate so I had to break it up a little. It's surprisingly smooth sounding (at least with sensible parameters). It's certainly the best Schroeder topology reverb I've heard yet, although maybe somewhat lacking in character. And of course it still sucks for short decay times.


It's odd that the density parameter (variable from 1 to 4) switches the allpasses in and out of the signal path rather than varying the coefficients. 


Another strange thing here is the diffusion parameter, which actually controls the stereo width by changing the left and right delay taps. This shows diffusion = 10 (the maximum). When diffusion is 0 it's close to mono.  I don't know why you'd want to use anything but 10. Unsurprisingly, the way it's described in the user manual is not remotely helpful. 


There's also modulation, which I haven't shown here. The modulation is simple (a fixed rate sinusoidal LFO with complementary modulation in the left and right channels, not inside a feedback loop). But I don't know where it is in the signal path, except that it doesn't affect the early reflection taps.


---

## Page 34

---

### Post #991 -- Page 34
**User:** Antti H
**Info:** Joined: Sep 2010Posts: 408My Studio🎧 15 years | Posts: 408My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15842451&postcount=991>

Quote: > Originally Posted byacreil➡️It's odd that the density parameter (variable from 1 to 4) switches the allpasses in and out of the signal path rather than varying the coefficients.Another strange thing here is the diffusion parameter, which actually controls the stereo width by changing the left and right delay taps. This shows diffusion = 10 (the maximum).Yamaha SPX900 and any builtin reverbs derived from that.

---

### Post #992 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15842493&postcount=992>

Quote: > Originally Posted byAntti H➡️Yamaha SPX900 and any builtin reverbs derived from that.Not quite, it's the REV5 large hall algorithm. I expect the SPX900 is close but simpler.

---

### Post #993 -- Page 34
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15842960&postcount=993>

I guessed it was Yamaha but the differences to the last algo threw me off.


Well, that explains why hardly anyone knows what the diffusion parameter is for

---

### Post #994 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15843952&postcount=994>

Quote: > Originally Posted byDeleted 4768d8b➡️Well, that explains why hardly anyone knows what the diffusion parameter is forYeah it's dumb, I don't know what the idea was there. Alesis used "density" for the input allpass coefficients and "diffusion" for the loop allpass coefficients. That actually makes sense. 


I looked at the REV5 symphonic algorithm too. It uses 3 modulated delay taps, panned left, right and center. I don't really know what the hell the modulation is doing though 


I should check it other models to see if they do the same thing.

---

### Post #995 -- Page 34
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15844137&postcount=995>

Oh wow. That's unique. What's the input signal there?


 It does sound nice. I used to really like it until accurate Roland Dimension D emulations came along. That's even better IMO. A friend keeps an SPX2000 hooked up via AES/EBU just for Symphonic.

---

### Post #996 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15844173&postcount=996>

Quote: > Originally Posted byDeleted 4768d8b➡️Oh wow. That's unique. What's the input signal there?It's a 20 kHz sine tone. Lower frequencies won't show anything useful on a spectrogram. I think the best way to see what's going on would be an impulse train at about 100 Hz going into the input of the REV5 and triggering the sweep of an analog oscilloscope. Basically, the taps are moving for a little bit and then stopping, then moving again, but it's hard to visualize clearly. Actually, I could probably show it with a Pure Data patch, but the oscilloscope would be more fun.

Quote: > It does sound nice. I used to really like it until accurate Roland Dimension D emulations came along.I don't know what the fixation is with the Dimension D. It's not doing anything complicated. It uses a clever crossover circuit so that it doesn't detune low frequencies, but the modulation isn't fancy. The Roland RS-09/RS-505/VP-330 chorus is where it's at.

---

### Post #997 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15844532&postcount=997>

Here's the improved version of [this reverb](https://gearspace.com/board/showpost.php?p=15815520&postcount=962) from a later software revision. The main difference is that there's an additional allpass stage (with inexplicably strange delay lengths), plus the early reflection taps are panned left and right rather than mono. It sounds much better. 


I'm more confident this time that I got it right. Previously I wasn't sure what the sub-reverb did, where the highpass/lowpass filters were in the signal path, or where the start point was. 


I'm sad no one guessed it tho.

Do you like this song?
{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "@id": "https://youtube.com/v/_CL6n0FJZpk",
  "name": "YouTube Video",
  "description": "Embedded YouTube video",
  "thumbnailUrl": "https://i.ytimg.com/vi/_CL6n0FJZpk/hqdefault.jpg",
  "uploadDate": "2022-02-05T06:30:07+00:00",
  "contentUrl": "https://youtube.com/v/_CL6n0FJZpk",
  "embedUrl": "https://youtube.com/embed/_CL6n0FJZpk"
}

---

### Post #998 -- Page 34
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15844589&postcount=998>

Quote: > Originally Posted byacreil➡️I don't know what the fixation is with the Dimension D. It's not doing anything complicated.Yea that's exactly it. It doesn't sound like chorus. It's perfect for getting BVs to sit behind the lead, same for pads. I didn't know about the LF filter. Maybe that's why I think it sounds better than detune algos like Yamaha's Symphonic.


I know what you mean about fixation though- the hardware is way too expensive. There are quite a few emulation plugins and they're all perfectly good at it. I chose the Arturia because I got a discount from already owning their other plugins.

---

### Post #999 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15845097&postcount=999>

Quote: > Originally Posted byTomás Mulcahy➡️Yea that's exactly it. It doesn't sound like chorus. It's perfect for getting BVs to sit behind the lead, same for pads. I didn't know about the LF filter. Maybe that's why I think it sounds better than detune algos like Yamaha's Symphonic.I know what you mean about fixation though- the hardware is way too expensive. There are quite a few emulation plugins and they're all perfectly good at it. I chose the Arturia because I got a discount from already owning their other plugins.Other than the crossover though, it's pretty much the same as almost every Roland chorus since the Jupiter 4, and plenty of other things besides. It's 2 BBDs with complementary triangle wave modulation. It's the bare minimum for a decent stereo chorus.

---

### Post #1000 -- Page 34
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15845149&postcount=1000>

Quote: > Originally Posted byacreil➡️Other than the crossover though, it's pretty much the same as almost every Roland chorus since the Jupiter 4, and plenty of other things besides. It's 2 BBDs with complementary triangle wave modulation. It's the bare minimum for a decent stereo chorus.Isn't there a compander as well though? I don't think all the Roland chorus implementations have a compander. Plus the levels are preset with a bias towards width instead of depth like a regular chorus  To be fair, it's a very good UI.


It explains why the Arturia bundle is so cheap, and they gave away the Juno chorus for free

---

### Post #1001 -- Page 34
**User:** Antti H
**Info:** Joined: Sep 2010Posts: 408My Studio🎧 15 years | Posts: 408My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15845334&postcount=1001>

Quote: > Originally Posted byacreil➡️Other than the crossover though, it's pretty much the same as almost every Roland chorus since the Jupiter 4, and plenty of other things besides. It's 2 BBDs with complementary triangle wave modulation. It's the bare minimum for a decent stereo chorus.Yet it sounds much more useful than a regular chorus for all the occasions when you want to add width, movement and to make the sound "better" without making it sound obviously chorused or "unfocused". It may be simple to implement, but it works really well.

---

### Post #1002 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15845861&postcount=1002>

Quote: > Originally Posted byDeleted 4768d8b➡️Isn't there a compander as well though? I don't think all the Roland chorus implementations have a compander. Plus the levels are preset with a bias towards width instead of depth like a regular chorusTo be fair, it's a very good UI.Companders improve dynamic range, but shouldn't affect the sound all that much. Roland were pretty thoughtful about about implementing controls. In the DEP-5, the chorus delay excursion varies as a function of the modulation rate and detune depth. So you're not varying it directly, as you are in most designs; the result is that the amount of detuning is constant as you change the modulation rate; slower rates increase the excursion depth. It's not difficult to do this (at least in a digital effect), but most manufacturers didn't bother. And this chorus is the same standard Roland chorus effect, just digital. 


Anyway most digital stereo chorus algorithms seem to do pretty much the same thing; the analog chorus circuits that don't do this are usually the crappy single BBD pseudo-stereo variety.

---

### Post #1003 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15845867&postcount=1003>

Here's reverb B, supposed to be a "medium-sized concert hall". Sounds alright, smoother than reverb A.


This is a classic album 
![](https://m.media-amazon.com/images/I/51FUauZ5NEL._SX425_.jpg)

---

### Post #1004 -- Page 34
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,229🎧 20 years | Posts: 5,229
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15846443&postcount=1004>

Quote: > Originally Posted byacreil➡️Here's reverb B, supposed to be a "medium-sized concert hall". Sounds alright, smoother than reverb A.This is a classic albumSPX-1000?

---

### Post #1005 -- Page 34
**User:** cowudders
**Info:** Joined: Jan 2006Posts: 1,021🎧 20 years | Posts: 1,021
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15846526&postcount=1005>

Quote: > Originally Posted byacreil➡️Here's reverb B, supposed to be a "medium-sized concert hall". Sounds alright, smoother than reverb A.This is a classic albumi really enjoy this thread, being a reverb fan&freak for ages now, i'm learning a ton and feel totally entertained! thank you. it's obviously a sony, though

---

### Post #1006 -- Page 34
**User:** cowudders
**Info:** Joined: Jan 2006Posts: 1,021🎧 20 years | Posts: 1,021
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15846536&postcount=1006>

Quote: > Originally Posted byacreil➡️I looked at the REV5 symphonic algorithm too. It uses 3 modulated delay taps, panned left, right and center. I don't really know what the hell the modulation is doing thoughI should check it other models to see if they do the same thing.very strange   i think overloud tries to model the spx symphonic (and a stringmachine chorus) with their 'modula' plug-in. i wonder if they got this right.

---

### Post #1007 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15846719&postcount=1007>

Quote: > Originally Posted bycowudders➡️it's obviously a sony, thoughYeah, I was trying to make it as obvious as possible

---

### Post #1008 -- Page 34
**User:** sergio_frias_23
**Info:** Joined: Jan 2012Posts: 62🎧 10 years | Posts: 62
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15847008&postcount=1008>

Sony DRE 2000

---

### Post #1009 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15847320&postcount=1009>

Quote: > Originally Posted bysergio_frias_23➡️Sony DRE 2000Right. I don't really care much about Dr. Dre.


I shall post the other two algorithms soon-ish. I thought they were going to be difficult, but I just managed to confuse myself.

---

### Post #1010 -- Page 34
**User:** sergio_frias_23
**Info:** Joined: Jan 2012Posts: 62🎧 10 years | Posts: 62
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15847720&postcount=1010>

hello acreil, i have a question about your midiverb 59 algorithm, you draw a series of numbers representing taps,and i got a little confused, is the delay taps using this topology(see below) or another one? (like output taps from a  circulating feedback delay).


![](https://lh3.googleusercontent.com/vyDInaBYfkt9mkkaSiL5N0tEL_Uys_m6fh0YPXbucdppmPdudE8h28lB_EVLbjiPNAURGc9msqnkRmzRcCmE9Xfvm3vSFcdHtUZ3Xks7gMjh61w4xAolUPxt7_UZsieAslYPN6DhqSXSwVNb6hwTBvxevp2KSH2FHzi4KV90q0MbCEPoB4ZB5nSs4YlypYEptfxAWsW2R7thpnZGJHJc4MvKgVSai42_mjeICU3AW95TnQCJkjv-yukNp1rUiBVa3AW98BDTdvwTVgMzDGreMsMWxbiIGL_dhtIy17qFbdrR4gsX7djMFt8h0Z5xvHH3k8UlyD-Seb7hLgKBI9EVwxc_MEXZ1iA6T1OnFvf1fR9x2yMW2A9PkZKXWXK8VcwYFD42VNQ5U0psDM7EVNyurvur2quTug9nklQ7_ZlAB3vlqA2kLjk5ddS_YpKtspBtYynZdy73eezNzhgTgnrztLP71qx0ZK8gQMLMH1dia6AQDysGT9Zbd9uoxqXNbYw0xM5TxOGEm8ZQaXqKUqkrS0z4bIgl71dvy2uUwWT1hgCVepQLMnIrHs4KnJUjw93epujGFMm8W8EMgBvRRhsB3QMx3NZHGJa6LFYvXRgnLziJFWkshD4muHNSFKcUkaGaxqP5u3zhnbILSxmJSFUxv_LNcA3Co8H6batZ8iPECWU_JVdupc-2Z8FYFOLRv1eAX5NUxpJtQhR5uxt7Ft3y_fbE=w519-h346-no?authuser=0)

---

### Post #1011 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15848092&postcount=1011>

Quote: > Originally Posted bysergio_frias_23➡️hello acreil, i have a question about your midiverb 59 algorithm, you draw a series of numbers representing taps,and i got a little confused, is the delay taps using this topology(see below) or another one? (like output taps from a  circulating feedback delay).I can't see the image. They're just completely straightforward delay line taps.

---

### Post #1012 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15850503&postcount=1012>

Here are the remaining two DRE 2000 algorithms, both described as plates. It's a different topology with stereo comb taps. Both of them use two allpasses with the same delay length, which made it difficult to figure out. I have no idea why that was done. I think the other two algorithms sound better.


This will probably be all for a while; I have other stuff I need to do.

---

### Post #1013 -- Page 34
**User:** sergio_frias_23
**Info:** Joined: Jan 2012Posts: 62🎧 10 years | Posts: 62
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15854862&postcount=1013>

Quote: > Originally Posted byacreil➡️Here are the remaining two DRE 2000 algorithms, both described as plates. It's a different topology with stereo comb taps. Both of them use two allpasses with the same delay length, which made it difficult to figure out. I have no idea why that was done. I think the other two algorithms sound better.This will probably be all for a while; I have other stuff I need to do.very interesting, one question,what means h(z) in the feedback delay ? is it a 1 sample delay?

---

### Post #1014 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15854978&postcount=1014>

Quote: > Originally Posted bysergio_frias_23➡️very interesting, one question,what means h(z) in the feedback delay ? is it a 1 sample delay?Loop filter. Shorthand for "I dunno, some kind of highpass/lowpass/whatever filtering". You can just use some standard filter and it will work well enough.

---

### Post #1015 -- Page 34
**User:** damien
**Info:** Joined: Nov 2006Posts: 416🎧 15 years | Posts: 416
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15856809&postcount=1015>

If you guys are looking for eeproms there's plenty of them here:
[https://dbwbp.com/index.php/9-misc/37-synth-eprom-dumps](https://dbwbp.com/index.php/9-misc/37-synth-eprom-dumps)


Quadraverbs, sony, ensoniq you name it, even the sony dps v-77 is there. (it's in my top 3 RVB)


I tried to disassemble an ensoniq dp pro eprom to get the "never-documented" sysex instructions, but I never succeed. The 90s fx unit are almost always working around M68k mpu, or hitachi H8/3002 processors, the sony dps line has them.


A tutorial about how to turn a bin file from an eeprom dump to a "readable" file containing instructions would be awesome! Everytime I ran a .bin in disassembler.io I had nothing usable.


Hope it helps for eeprom dumps

---

### Post #1016 -- Page 34
**User:** sergio_frias_23
**Info:** Joined: Jan 2012Posts: 62🎧 10 years | Posts: 62
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15875223&postcount=1016>

heelo acreil,about the midiverb shorter reverbs,(program 1 for ex.) they seem instant ,no buildup,but i can be wrong,are they the same algorithm like program 7 you posted or some kind of taps followed by a series of all pass?, thank you.

---

### Post #1017 -- Page 34
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15875255&postcount=1017>

Quote: > Originally Posted byacreil➡️Here are the remaining two DRE 2000 algorithms, both described as plates. It's a different topology with stereo comb taps. Both of them use two allpasses with the same delay length, which made it difficult to figure out. I have no idea why that was done. I think the other two algorithms sound better.This will probably be all for a while; I have other stuff I need to do.Wow... I've been away from this thread for a few weeks and just look at what you've been up to...!!


I feared this was what you were up to when I saw the "sub reverb" in your earlier depiction.  In Sony-speak the "sub reverb" is really only an additional delay path feeding the main reverb, though in  the stereo devices (such as the MUR-201 / SDR-1000) they have additional paths through some mono and stereo ER clusters.  All very novel and somewhat innovative, but very few of their end users (besides me) bothered to program them... the R7 suffered from a terrible Encoder interface that adjusted delay parameters in µs  - nearly - it took a week to change the settings , maybe worse than how Lexicon implemented the encoder on the LXP-15.


I actually own a DRE-2000 and several of the Sony/Ibanez SDR-1000 


The DRE-200 program "D" is a stunning and unequaled reverb,  based on your comment I wonder if you got it right, or if you are using the earlier version of the DRE (where they had "spring" reverb algos - discarded for rev2)?


In some other thread here I have demonstrated that the first two algos in the DRE are present in the SDR/MUR, and the last 2 are in the Sony R7.


It's a remarkably useful reverb, in spite of it's unusual topology.


The SDR / MUR "Hall" is a based on an Allpass "ring" ala Lexicon and suffers from the crazy stereo panning effects when driven from one channel.


I have the schematics and EPROMS for my DRE, how are you deriving these algos?

---

### Post #1018 -- Page 34
**User:** Deleted 4768d8bPosts: n/aMy Studio
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15875269&postcount=1018>

Interesting about the encoders. I worked in a studio with a Sony DPS V-77, and I owned a Lexicon LXP15ii for years. Got pretty deep into the Sony (even tried the vocoder and digital i/o) but way deeper into the Lexicon. For those who don't know: the DPS V-77 was like a "best of" all of the previous units. Filters, delays, reverbs, pitch mod etc. As far as I know it was just as extensively editable as well.


Admittedly they are slightly different units to the ones you mention- but both were a joy to programme IME. Never had issues with the encoders on those particular models. I added a 1U rack strip with 4 pots for the VR (?) sockets on the Lexicon. It was a lovely machine for on the fly tweaking, especially if you fed it back on itself.

---

### Post #1019 -- Page 34
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15875290&postcount=1019>

Quote: > Originally Posted bydamien➡️I tried to disassemble an ensoniq dp pro eprom to get the "never-documented" sysex instructions, but I never succeed. The 90s fx unit are almost always working around M68k mpu, or hitachi H8/3002 processors, the sony dps line has them.That would be difficult, ensoniq developed their own proprietary DSP in house.  I was involved in the DP/4+, DP/2 and DP/Pro development. The DP/Pro should have been much more successful than it was, but I think things like the "Expert Verb" algo were too molecular for most end-users (you could adjust every delay and allpass in the algo and there were 2 different topologies).

---

### Post #1020 -- Page 34
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15876108&postcount=1020>

Quote: > Originally Posted bysergio_frias_23➡️heelo acreil,about the midiverb shorter reverbs,(program 1 for ex.) they seem instant ,no buildup,but i can be wrong,are they the same algorithm like program 7 you posted or some kind of taps followed by a series of all pass?, thank you.It's the same basic topology, but some of them take outputs from the delays inside the allpasses (both the input allpass chain and the loop allpasses). So they have a very rapid onset, but sometimes a metallic sound.

Quote: > Originally Posted byzmix➡️I feared this was what you were up to when I saw the "sub reverb" in your earlier depiction.  In Sony-speak the "sub reverb" is really only an additional delay path feeding the main reverb, though in  the stereo devices (such as the MUR-201 / SDR-1000) they have additional paths through some mono and stereo ER clusters.Yeah, this caused me some confusion. I have the SDR 1000 and it's fairly obvious that the sub-reverb is a separate mono in/mono out reverb. Plus on the REV5 it's an independent reverb. I was expecting something fancier. 


You wouldn't happen to have the SDR 1000+ or MU-R201 ROM dump, would you? Mine's the original model.

Quote: > the R7 suffered from a terrible Encoder interface that adjusted delay parameters in µs  - nearly - it took a week to change the settings , maybe worse than how Lexicon implemented the encoder on the LXP-15.The REV5 is a pain in the ass too. 1500ms of delay and only increment/decrement buttons . You can watch your fingernails grow while holding the button down. It makes the Quadraverb's pressure sensitive buttons seem totally brilliant. And that's just a piezo transducer attached to the back of the PCB. Was everyone else too stupid to just copy that? 

Quote: > The DRE-200 program "D" is a stunning and unequaled reverb,  based on your comment I wonder if you got it right, or if you are using the earlier version of the DRE (where they had "spring" reverb algos - discarded for rev2)?That's just my reaction to hearing the impulse response. Impulse responses are a great way evaluate at least some aspects of a reverb, but they also kind of provide too much information. It's really unflattering, like watching porn in 4K. An impulse response might sound nasty with a bunch of allpass ringing, but you probably won't hear it on a musical signal. And anyway I'm overly picky, at least when it comes to things that are supposed to be high end. The Midiverb gets a pass, but I'm gonna criticize everything else to death.


I think version 1 just uses one algorithm, which is basically A but with 2 allpasses per output channel rather than 3. It's not as good, and you're not missing anything if you don't have it.

Quote: > The SDR / MUR "Hall" is a based on an Allpass "ring" ala Lexicon and suffers from the crazy stereo panning effects when driven from one channel.I noted the panning thing, but I think it's still constant echo density. I would have dug into mine already, but I want to poke around in the hardware first. I need to find the exact sample rate, the number of instructions per sample, etc. And clean the pots and maybe modify it a little.


It's crossed my mind also to acquire a DPS V77. Normally I rule out buying "fancy" gear or spending more than like $100, because I can design stuff that's better (maybe not so much with very good pitch shifters or highly nonlinear VCFs, but almost everything else). But things like the Sony DPS V77, Alesis Quadraverb 2, Roland SRV 330, Dynacord DRP 15, Korg A1 and Behringer V Verb do tempt me, at least if they're cheap enough.

Quote: > I have the schematics and EPROMS for my DRE, how are you deriving these algos?Impulse responses. The guy who wrote [this article](https://www.amazona.de/zeitmaschine-sony-dre-2000-digital-reverberator-halleffekt/) (Georg Müller) posted some impulse responses from version 1. I opened them in Audacity and figured it would be relatively easy to reverse engineer since the echo density is quite low. I asked him if he'd be willing to make a couple test recordings. He agreed to do it, but his unit had since been upgraded to version 2. I messed around with Audacity and a couple Matlab scripts, figured out version 1 (minus the initial delay since there's no dry impulse for reference), analyzed some of my own gear, then figured out version 2. 


Turns out it's actually pretty easy for most designs, regardless of echo density. There are certainly things that I wouldn't be able to analyze easily, but in practice I haven't encountered them. At this point I expect that most commercial reverbs use variants of Schroeder topologies (other than Lexicon, Quantec, Alesis, Dynacord, Ensoniq, Ursa Major and Eventide). Allpass loops are harder, but doable if the allpass coefficients can be set to 0. I don't have a good way to analyze modulation. Delay lengths are estimated (this mostly depends on how closely the actual sample rate matches the nominal sample rate). Gains are rough approximations. I can determine where filtering happens in the feedback loop, but not really the specifics. That's far from sufficient to make a totally accurate plugin, for example, but it's enough to play with the algorithm, make variations on it, compare different models, etc.


So if you'd like to make me some test recordings...

Quote: > Originally Posted byzmix➡️That would be difficult, ensoniq developed their own proprietary DSP in house.The right way to do it would be to use a logic analyzer to read the data sent to the DSP, then try to deduce the instruction set as you fiddle with delay times, feedback, filtering, etc. And maybe also see what the RAM addresses are doing, send the DSP different instructions to see what happens, etc. The instruction sets aren't generally going to be very complicated because it's mostly just MAC instructions. But it's still a huge headache. And then there's also mapping the user parameters to the DSP program, etc.


It wasn't that hard with the Midiverb since it's all discrete logic and the instruction set is near trivial. I just needed the schematic, ROM dumps and an oscilloscope. It wouldn't be a big deal to do the same with the Alesis XT and XT:c. But that's not the case for most reverbs.


---

## Page 35

---

### Post #1021 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15876154&postcount=1021>

Quote: > Originally Posted byacreil➡️It's the same basic topology, but some of them take outputs from the delays inside the allpasses (both the input allpass chain and the loop allpasses). So they have a very rapid onset, but sometimes a metallic sound.Yeah, this caused me some confusion. I have the SDR 1000 and it's fairly obvious that the sub-reverb is a separate mono in/mono out reverb. Plus on the REV5 it's an independent reverb. I was expecting something fancier.You wouldn't happen to have the SDR 1000+ or MU-R201 ROM dump, would you? Mine's the original model.The REV5 is a pain in the ass too. 1500ms of delay and only increment/decrement buttons. You can watch your fingernails grow while holding the button down. It makes the Quadraverb's pressure sensitive buttons seem totally brilliant. And that's just a piezo transducer attached to the back of the PCB. Was everyone else too stupid to just copy that?That's just my reaction to hearing the impulse response. Impulse responses are a great way evaluate at least some aspects of a reverb, but they also kind of provide too much information. It's really unflattering, like watching porn in 4K. An impulse response might sound nasty with a bunch of allpass ringing, but you probably won't hear it on a musical signal. And anyway I'm overly picky, at least when it comes to things that are supposed to be high end. The Midiverb gets a pass, but I'm gonna criticize everything else to death.I think version 1 just uses one algorithm, which is basically A but with 2 allpasses per output channel rather than 3. It's not as good, and you're not missing anything if you don't have it.I noted the panning thing, but I think it's still constant echo density. I would have dug into mine already, but I want to poke around in the hardware first. I need to find the exact sample rate, the number of instructions per sample, etc. And clean the pots and maybe modify it a little.It's crossed my mind also to acquire a DPS V77. Normally I rule out buying "fancy" gear or spending more than like $100, because I can design stuff that's better (maybe not so much with very good pitch shifters or highly nonlinear VCFs, but almost everything else). But things like the Sony DPS V77, Alesis Quadraverb 2, Roland SRV 330, Dynacord DRP 15, Korg A1 and Behringer V Verb do tempt me, at least if they're cheap enough.Impulse responses. The guy who wrotethis article(Georg Müller) posted some impulse responses from version 1. I opened them in Audacity and figured it would be relatively easy to reverse engineer since the echo density is quite low. I asked him if he'd be willing to make a couple test recordings. He agreed to do it, but his unit had since been upgraded to version 2. I messed around with Audacity and a couple Matlab scripts, figured out version 1 (minus the initial delay since there's no dry impulse for reference), analyzed some of my own gear, then figured out version 2.Turns out it's actually pretty easy for most designs, regardless of echo density. There are certainly things that I wouldn't be able to analyze easily, but in practice I haven't encountered them. At this point I expect that most commercial reverbs use variants of Schroeder topologies (other than Lexicon, Quantec, Alesis, Dynacord, Ensoniq, Ursa Major and Eventide). Allpass loops are harder, but doable if the allpass coefficients can be set to 0. I don't have a good way to analyze modulation. Delay lengths are estimated (this mostly depends on how closely the actual sample rate matches the nominal sample rate). Gains are rough approximations. I can determine where filtering happens in the feedback loop, but not really the specifics. That's far from sufficient to make a totally accurate plugin, for example, but it's enough to play with the algorithm, make variations on it, compare different models, etc.So if you'd like to make me some test recordings...The right way to do it would be to use a logic analyzer to read the data sent to the DSP, then try to deduce the instruction set as you fiddle with delay times, feedback, filtering, etc. And maybe also see what the RAM addresses are doing, send the DSP different instructions to see what happens, etc. The instruction sets aren't generally going to be very complicated because it's mostly just MAC instructions. But it's still a huge headache. And then there's also mapping the user parameters to the DSP program, etc.It wasn't that hard with the Midiverb since it's all discrete logic and the instruction set is near trivial. I just needed the schematic, ROM dumps and an oscilloscope. It wouldn't be a big deal to do the same with the Alesis XT and XT:c. But that's not the case for most reverbs....maybe take another look at your algo diagrams now that you know that the "Sub reverb"  just a straight delay into the reverb itself.


Ha..! I sent Georg the Rev 2 Eproms..!


Also back in the early 1990s I had a friend try to copy the eprom from my MUR-201 (aka SDR-1000+) so I could update my SDR to a "plus" he said that the eproms were encrypted and he couldn't get them to dump...

---

### Post #1022 -- Page 35
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15876305&postcount=1022>

Quote: > Originally Posted byzmix➡️...maybe take another look at your algo diagrams now that you know that the "Sub reverb"  just a straight delay into the reverb itself.I accounted for that already. I was just confused when I was doing the version 1 diagram. I assumed I was leaving out something important.

Quote: > Ha..! I sent Georg the Rev 2 Eproms..!Yeah that figures. I know Sean sent him the AES paper. The algorithm described in the paper isn't really related to the DRE 2000 design.

Quote: > Also back in the early 1990s I had a friend try to copy the eprom from my MUR-201 (aka SDR-1000+) so I could update my SDR to a "plus" he said that the eproms were encrypted and he couldn't get them to dump...I've only run into weird things like that when dumping mask ROMs, usually because the chip enable pin is active high rather than active low (this allows two ICs to use the same chip enable signal without an inverter). But at least from the service manual it just looks like a standard 27C256. I don't think those can be encrypted. I'll have to add dumping the ROM to the list of things to do as well, since I don't think anyone's done it.


What I can say so far about the SDR 1000 hardware is that the CXD1079Q DSP was also used in some surround processors (SDP-505ES, SDP-777ES), a weird CD player (CDZ-1) and a mastering limiter (DAT-1000). The overall hardware design is pretty simple, but the DSP seems fairly sophisticated. It looks like it's either 96, 128 or 192 instructions per sample. The EQ is analog. Some of the later Sony effect processor ICs were also used in consumer gear.

---

### Post #1023 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=15914647&postcount=1023>

Came across this one, our "very own" Sean Costello..!


Very nice, Sean..!

{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "@id": "https://youtube.com/v/jbLDP6WZDeY",
  "name": "YouTube Video",
  "description": "Embedded YouTube video",
  "thumbnailUrl": "https://i.ytimg.com/vi/jbLDP6WZDeY/hqdefault.jpg",
  "uploadDate": "2022-03-23T12:11:36+00:00",
  "contentUrl": "https://youtube.com/v/jbLDP6WZDeY",
  "embedUrl": "https://youtube.com/embed/jbLDP6WZDeY"
}

---

### Post #1024 -- Page 35
**User:** MarcoZ
**Info:** Joined: Jul 2022Posts: 6 | Posts: 6
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16067721&postcount=1024>

Hi Everyone - I´m new here....


This I will ask acreil...
[https://gearspace.com/board/attachme...re-scan-45.jpg](https://gearspace.com/board/attachments/geekzone/986885d1635401059-reverb-subculture-scan-45.jpg)

What are the numbers in black, and what does it mean in red ?


post 997:

What does the numbers mean in the boxes in the diagram ? are this the sample adress from the FDN ? or is it the bufferlength of one allpass ?

(APF 224,227 etc. ?)


What is the H(z) box ? Also delay ?


How did you came to this diagram ? only by hearing the algorithm ?


Thank you.

---

### Post #1025 -- Page 35
**User:** MarcoZ
**Info:** Joined: Jul 2022Posts: 6 | Posts: 6
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16067723&postcount=1025>

sean was writing that its difficult to do a triangle LFO or an random generator on Fv-1.

My idea would be to use Pot3 as LFO / Random source if you take an attiny with DAC (R2R) for modulating input. As I read in the beginning of this monstertread its because you need it for a concert hall algorithm (0.4hz triangle with random).


Maybe I don´t understand this because triangle and random on top (mixed) or either triangle or random as mod source ?

---

### Post #1026 -- Page 35
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16068155&postcount=1026>

Quote: > Originally Posted byMarcoZ➡️sean was writing that its difficult to do a triangle LFO or an random generator on Fv-1.My idea would be to use Pot3 as LFO / Random source if you take an attiny with DAC (R2R) for modulating input. As I read in the beginning of this monstertread its because you need it for a concert hall algorithm (0.4hz triangle with random).Maybe I don´t understand this because triangle and random on top (mixed) or either triangle or random as mod source ?Concert hall would need several unrelated LFOs. 


Have we discussed the specific LFO characteristics used in that algorithm? If not let’s. 



-Casey

---

### Post #1027 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16068240&postcount=1027>

Quote: > Originally Posted byCasey➡️Concert hall would need several unrelated LFOs.Have we discussed the specific LFO characteristics used in that algorithm? If not let’s.-CaseyLexicon only use one LFO in their concert hall..

---

### Post #1028 -- Page 35
**User:** Casey
**Info:** Joined: May 2003Posts: 1,796🎧 20 years | Posts: 1,796
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16068290&postcount=1028>

Quote: > Originally Posted byzmix➡️Lexicon only use one LFO in their concert hall..I know you have looked at that carefully. So one LFO used in multiple cases, presumably with every other one in opposition? That makes sense given that the microprocessor creating the LFO randomly missed some delay updates I believe because it could not quite keep up at times.

---

### Post #1029 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16068314&postcount=1029>

Quote: > Originally Posted byCasey➡️I know you have looked at that carefully. So one LFO used in multiple cases, presumably with every other one in opposition? That makes sense given that the microprocessor creating the LFO randomly missed some delay updates I believe because it could not quite keep up at times.

Single random LFO is injected in a (very) few places, yes..  in another algo a simple triangle only injected once in one side of the loop,and what is surprising is that you don't hear it as such.

---

### Post #1030 -- Page 35
**User:** oldgearguy
**Info:** Joined: Sep 2002Posts: 5,007🎧 20 years | Posts: 5,007
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16068397&postcount=1030>

What about in their HD cart algorithm?

---

### Post #1031 -- Page 35
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16068786&postcount=1031>

Quote: > Originally Posted byMarcoZ➡️What are the numbers in blackDelay lengths in samples.
Quote: > and what does it mean in red ?Memory address offsets; at the time I was calculating everything manually, so I used that to keep track of the different delay lines. I wrote a script later that would list all the memory read and write addresses and their corresponding delays.

Quote: > post 997:What does the numbers mean in the boxes in the diagram ? are this the sample adress from the FDN ? or is it the bufferlength of one allpass ?(APF 224,227 etc. ?)Again, delay length in samples, -0.7 is the allpass coefficient.

Quote: > What is the H(z) box ? Also delay ?Loop filter, either a lowpass/highpass or shelf filters. Probably shelf filters, but it's hard to tell the way I'm doing it.

Quote: > How did you came to this diagram ? only by hearing the algorithm ?For the Midiverb it was reverse engineering the algorithms on the EPROM. The others were analyzed from impulse responses.

---

### Post #1032 -- Page 35
**User:** living sounds
**Info:** Joined: Aug 2004Posts: 5,229🎧 20 years | Posts: 5,229
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16071416&postcount=1032>

Quote: > Originally Posted byrobobob➡️Casey or any other Bricasti user who knows...Love my M7The presets and the sound quality A+My density is saving edit changes to a user preset in the register bank.The user manual is a bit terse for my taste for this critical UI of editing and saving edit changesI took Tiled room and saved it to R0 as ShowerTiledThen edited parameters to make it react more like a small showerTried Store, then Reg then StoreAfter several iterations I got one parameter change to saveBut,was the sequence:EditRegStore???Recall the named user preset using Reg (do I have to hit Enter to tell the M7 that this is the current loaded preset?)Editchange paramsGo to Reg, but NO asterisk to reassure me that the machine knows it is in Edit mode!Back to Edit and try againRepeat until cussing commencesJust NOT getting the UI metaphor for editing user presets in the Reg banksAny condescension welcome IF it makes this necessary feature usable for me!TIAOff topic.

---

### Post #1033 -- Page 35
**User:** MarcoZ
**Info:** Joined: Jul 2022Posts: 6 | Posts: 6
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16072435&postcount=1033>

Quote: > Originally Posted byacreil➡️Delay lengths in samples.Memory address offsets; at the time I was calculating everything manually, so I used that to keep track of the different delay lines. I wrote a script later that would list all the memory read and write addresses and their corresponding delays.Again, delay length in samples, -0.7 is the allpass coefficient.Loop filter, either a lowpass/highpass or shelf filters. Probably shelf filters, but it's hard to tell the way I'm doing it.For the Midiverb it was reverse engineering the algorithms on the EPROM. The others were analyzed from impulse responses.Wow thank you !

So every AP has a private delay memoryline ?

and a main delayline for the tank ?


So you load the Eprom of the midiverb to an 8051 simulator to find the tables of 45 / 49 (bloom1 +2 ) ?


are the dasp8 opcodes the same of the fv-1(also by keith barr) ? 


Impulse response IR Files : so you can see the allpasses inside the spectral answer ?

---

### Post #1034 -- Page 35
**User:** MarcoZ
**Info:** Joined: Jul 2022Posts: 6 | Posts: 6
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16072436&postcount=1034>

Quote: > Originally Posted byzmix➡️Single random LFO is injected in a (very) few places, yes..  in another algo a simple triangle only injected once in one side of the loop,and what is surprising is that you don't hear it as such.So I could try to use pot3 as an random noise source for an fv-1 algorithm ?

---

### Post #1035 -- Page 35
**User:** MarcoZ
**Info:** Joined: Jul 2022Posts: 6 | Posts: 6
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16072443&postcount=1035>

Quote: > Originally Posted byMarcoZ➡️Wow thank you !So every AP has a private delay memoryline ?and a main delayline for the tank ?So you load the Eprom of the midiverb to an 8051 simulator to find the tables of 45 / 49 (bloom1 +2 ) ?are the dasp8 opcodes the same of the fv-1(also by keith barr) ?Impulse response IR Files : so you can see the allpasses inside the spectral answer ?Btw. I got an defective Midiverb2 and repair it a few days afo. I read the eprom too. But my I8031 ASM knowledge is poor at the moment. After disassembling with  d52v336 I get a source file to try with the edsim51.jar but get stuck with an Unknown label "int0". I didn´t find out which port pin this should be since I have no schematic for the MV2.

---------

X00c8:	mov	a,[#0ffh](https://gearspace.com/board/usertag.php?do=list&action=hash&hash=0ffh) 		; 00c8   74 ff      t.

X00ca:	movx	@r0,a		; 00ca   f2         r

	jnb	int0,X00d9	; 00cb   30 b2 0b   02.

	mov	a,22h		; 00ce   e5 22      e"

	setb	acc.1		; 00d0   d2 e1      Ra

	mov	22h,a		; 00d2   f5 22      u"

	pop	psw		; 00d4   d0 d0      PP

	pop	acc		; 00d6   d0 e0      P`

	reti			; 00d8   32         2

------

---

### Post #1036 -- Page 35
**User:** MarcoZ
**Info:** Joined: Jul 2022Posts: 6 | Posts: 6
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16075008&postcount=1036>

[http://freeverb3vst.osdn.jp/doc/Progenitor.jpg](http://freeverb3vst.osdn.jp/doc/Progenitor.jpg) 


Found this diagram of the concert hall algorithm. Where should this one random lfo injected ?

---

### Post #1037 -- Page 35
**User:** acreil
**Info:** Joined: May 2010Posts: 3,375🎧 15 years | Posts: 3,375
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16076043&postcount=1037>

Quote: > Originally Posted byMarcoZ➡️Wow thank you !So every AP has a private delay memoryline ?and a main delayline for the tank ?No, the addresses are the read/write points for one sample. It cycles through all the addresses like any standard design. The difference is that Alesis used address *increments* rather than offsets added to a base address from a circular buffer. It ends up performing the same function but saves a few 74xx ICs.

Quote: > So you load the Eprom of the midiverb to an 8051 simulator to find the tables of 45 / 49 (bloom1 +2 ) ?The microprocessor in the Midiverb only handles the MIDI and user interface. The algorithms are stored on a separate EPROM. I wrote a simulator and disassembler to generate impulse responses and readable code from the algorithm ROM. 

Quote: > are the dasp8 opcodes the same of the fv-1(also by keith barr) ?I don't know. They're probably not related at all. 

Quote: > Impulse response IR Files : so you can see the allpasses inside the spectral answer ?There's no spectral analysis. First I remove the series allpasses by processing the recorded impulse response in reverse through allpasses with estimated delays and coefficients. Then I can identify the number and length of the comb filters using something like autocorrelation, then identify which delay tap comes from which comb. 


It's harder for allpass loop reverbs, but I can fumble my way through those too. In practice, most of the ones I've looked at have been Schroeder reverbs. I'm getting the impression that the allpass loop topology was totally unknown to Japanese manufacturers. 

Quote: > Originally Posted byMarcoZ➡️Btw. I got an defective Midiverb2 and repair it a few days afo. I read the eprom too. But my I8031 ASM knowledge is poor at the moment. After disassembling with  d52v336 I get a source file to try with the edsim51.jar but get stuck with an Unknown label "int0". I didn´t find out which port pin this should be since I have no schematic for the MV2.I haven't tried disassembling it, but I think the non-modulated algorithms are copied straight off of the EPROM to the instruction memory. The service manual for the Midiverb 3 is available, and although they're different products with a different custom IC, the designs seem very similar. So maybe that's useful as a reference.

---

### Post #1038 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16078198&postcount=1038>

Quote: > Originally Posted byMarcoZ➡️http://freeverb3vst.osdn.jp/doc/Progenitor.jpgFound this diagram of the concert hall algorithm. Where should this one random lfo injected ?That is not the Concert Hall Algorithm, that is Jon Dattorro's representation of what such an algo might look like, it's similar to the reverb he created for the Ensoniq DP/4.


You can see in the diagram that there is one modulated allpass in the loop, labeled "chorus":

![](https://gearspace.com/board/attachment.php?attachmentid=1024891&stc=1&d=1657541120)

---

### Post #1039 -- Page 35
**User:** rafa1981
**Info:** Joined: Jan 2021Posts: 15🎧 5 years | Posts: 15
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16132738&postcount=1039>

Midiverb EMU available! Seems that the dev participated here.
[UBERVERB ( reproduction of a classic reverb from 1986)](https://gearspace.com/board/music-computers/1386803-uberverb-reproduction-classic-reverb-1986-a.html)

---

### Post #1040 -- Page 35
**User:** manecolooper
**Info:** Joined: Dec 2016Posts: 4🎧 5 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16209610&postcount=1040>

Quote: > Originally Posted byacreil➡️I knew you'd get it <3<3<3 although I think you had something of an unfair advantage since I told you previously that I had one and was messing with it. It's preset 49, "18 Sec. EX. LARGE BRIGHT" from the Midiverb.I think the Quadraverb 2 is the one to get though, or the Wedge. But I feel like Alesis were kind of stagnating in the 90s. Ensoniq, Roland, Sony and Digitech were doing better mid-priced effects at that point. The Quadraverb 2 wasn't that much of an advancement (still just 128 instructions per sample), then they just coasted forever.Yeah these are kind of special. In practice though it mostly sounds pretty good. Except there's anenormousamount of clipping on some of the longer reverbs (including the one I posted earlier). The dynamic range completely sucks. I kind of like that, though. It gives it that crap "20 year old Rephlex Records artist in a bedroom studio at mom's house" quality.I got your allpasses right here. 21 of them. Some of it is rearranged a bit for the sake of clarity (the gains in the feedback path were weird). Don't ask me why the input filter output is taken after the delay and the feedback filter output is taken before the delay. Maybe it was more convenient. But why are there even two filters in the first place when they're both the same?your posts are a treasure...thanks so much!!!

---

### Post #1041 -- Page 35
**User:** manecolooper
**Info:** Joined: Dec 2016Posts: 4🎧 5 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16221224&postcount=1041>

Quote: > Originally Posted byacreil➡️Here's the last installment for now. I skipped some because they're reverb or multitap algorithms that are best described elsewhere. Some of them are confusing as hell. The filters are already a pain to figure out, but sometimes there's no consistency regarding the way they're implemented, and occasionally there are complicated filters implemented that aren't even used. So I'm making a lot of mistakes. It would be interesting to see what kind of development environment Keith Barr had cooked up; I'm sure it didn't resemble what I'm looking at. Overall my conclusion is that the Midifex likely has the weirdest collection of algorithms of any commercial product. For the most part they're not particularly useful, but they're certainly inventive.Do you have 53 to 57 ? thanks so much!

---

### Post #1042 -- Page 35
**User:** Antti H
**Info:** Joined: Sep 2010Posts: 408My Studio🎧 15 years | Posts: 408My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16263783&postcount=1042>

Quote: > Originally Posted byzmix➡️That is not the Concert Hall Algorithm, that is Jon Dattorro's representation of what such an algo might look like, it's similar to the reverb he created for the Ensoniq DP/4.You can see in the diagram that there is one modulated allpass in the loop, labeled "chorus":That image does match actual 224 concert hall IRs up to the three recursive allpass filters part at least (barring minor differences in delay lengths), at which point I didn't bother digging further back when I did the analysis. Considering that and a few pecularities of the image, I choose to believe Jon Dattorro's interpretation.

---

### Post #1043 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16264184&postcount=1043>

Quote: > Originally Posted byAntti H➡️That image does match actual 224 concert hall IRs up to the three recursive allpass filters part at least (barring minor differences in delay lengths), at which point I didn't bother digging further back when I did the analysis. Considering that and a few pecularities of the image, I choose to believe Jon Dattorro's interpretation.Similar, yes, most reverb designers were (are?) chasing the 224 Concert Hall,  in this case a simple test is to listen to the DP/4 Hall and compare it to the Lexicon 224.

---

### Post #1044 -- Page 35
**User:** mu:zines
**Info:** Joined: Mar 2014Posts: 5,579🎧 10 years | Posts: 5,579
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16423181&postcount=1044>

I just put up a relatively rare interview with Keith Barr, from Home & Studio Recording (UK) magazine (1986), for those interested:

![](https://static.gearspace.com/util/imgext.php?u=http%3A%2F%2Fwww.muzines.co.uk%2Fimages_mag%2Farticles%2Fhsr%2FHSR_86_09_the_alesis_f_large.jpg&h=a892b77c49d7f566d448ae197be852e7)


"The Alesis File" - HSR Sep '86
[http://www.muzines.co.uk/articles/the-alesis-file/12861](http://www.muzines.co.uk/articles/the-alesis-file/12861)

---

### Post #1045 -- Page 35
**User:** manecolooper
**Info:** Joined: Dec 2016Posts: 4🎧 5 years | Posts: 4
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16483427&postcount=1045>

Great interview!

---

### Post #1046 -- Page 35
**User:** rafa1981
**Info:** Joined: Jan 2021Posts: 15🎧 5 years | Posts: 15
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16572946&postcount=1046>

I will probably releasing some open source reverb in plugin format containing some of the algorithms posted in this thread with minor mods. 

 @
[acreil](https://gearspace.com/board/member.php?u=143351)
 How should they be credited?

---

### Post #1047 -- Page 35
**User:** acreil
**Info:** Posts: n/aMy Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16575430&postcount=1047>

Wonderful! I don't think @
[acreil](https://gearspace.com/board/member.php?u=143351)
 comes here any more. You could try [his blog](https://acreil.wordpress.com/) maybe?

---

### Post #1048 -- Page 35
**User:** rafa1981
**Info:** Joined: Jan 2021Posts: 15🎧 5 years | Posts: 15
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16588734&postcount=1048>

There you go. I submitted to the KVR developer contest.
[https://www.kvraudio.com/product/turbo-paco-by-artv](https://www.kvraudio.com/product/turbo-paco-by-artv)


Sources here:
[https://github.com/RafaGago/artv-audio](https://github.com/RafaGago/artv-audio)


This has been a learning project, as a reverb rookie criticisms are very welcome. Adding algorithms based on the same old stuff should be pretty easy (for me).

---

### Post #1049 -- Page 35
**User:** saintjules
**Info:** Joined: Jul 2023Posts: 2 | Posts: 2
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16589675&postcount=1049>

Quote: > Originally Posted byrafa1981➡️There you go. I submitted to the KVR developer contest.https://www.kvraudio.com/product/turbo-paco-by-artvSources here:https://github.com/RafaGago/artv-audioThis has been a learning project, as a reverb rookie criticisms are very welcome. Adding algorithms based on the same old stuff should be pretty easy (for me).hi, thank you for the awesome plugin, sounds great from my first tests!

I have a few issues though. I'm on Linux and Ardour/Mixbus crash as soon as I load the plugin. All's good in Reaper. Any idea in how to troubleshoot this?

---

### Post #1050 -- Page 35
**User:** zmix
**Info:** Joined: Jan 2005Posts: 931🎧 20 years | Posts: 931
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16589695&postcount=1050>

Quote: > Originally Posted byrafa1981➡️There you go. I submitted to the KVR developer contest.https://www.kvraudio.com/product/turbo-paco-by-artvSources here:https://github.com/RafaGago/artv-audioThis has been a learning project, as a reverb rookie criticisms are very welcome. Adding algorithms based on the same old stuff should be pretty easy (for me).I'd love to hear is Rafa, any chance you can compile an Audio Units version?


---

## Page 36

---

### Post #1051 -- Page 36
**User:** rafa1981
**Info:** Joined: Jan 2021Posts: 15🎧 5 years | Posts: 15
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16589759&postcount=1051>

Sorry about that. I'm a Reaper user myself and I don't any other DAW.


If you are a dev, I package the debug symbols of the executable as a build artifact (below), so if you have a core dump it can be loaded with a debugger and get the stack trace.

[https://github.com/RafaGago/artv-aud...rbopaco-v1.0.0](https://github.com/RafaGago/artv-audio/releases/tag/turbopaco-v1.0.0)


I'm trying to compile and run Ardour, as it seems there are no binaries of it anymore...


EDIT: Don't bother with stack traces, I already found the error. I was misreporting the allowed IO configurations on a base class and Ardour was sending a mono input, which I don't support.


EDIT2: New build [available](https://github.com/RafaGago/artv-audio/releases/tag/turbopaco-v1.0.1).

---

### Post #1052 -- Page 36
**User:** rafa1981
**Info:** Joined: Jan 2021Posts: 15🎧 5 years | Posts: 15
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16589772&postcount=1052>

Quote: > Originally Posted byzmix➡️I'd love to hear is Rafa, any chance you can compile an Audio Units version?I unfortunately don't know much about Mac development other than it seems to require payment for signing binaries, etc. I don't have access to a Mac. I myself use Linux for personal computing and developing and Windows only for audio.


The project is vanilla JUCE using CMake and all SIMD code (if any) is using Clang's vector types; there is no architecture specific code. My educated guess is that compiling for Mac shouldn't be hard for someone that knows how to do it.

---

### Post #1053 -- Page 36
**User:** saintjules
**Info:** Joined: Jul 2023Posts: 2 | Posts: 2
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16590688&postcount=1053>

Quote: > Originally Posted byrafa1981➡️Sorry about that. I'm a Reaper user myself and I don't any other DAW.If you are a dev, I package the debug symbols of the executable as a build artifact (below), so if you have a core dump it can be loaded with a debugger and get the stack trace.https://github.com/RafaGago/artv-aud...rbopaco-v1.0.0I'm trying to compile and run Ardour, as it seems there are no binaries of it anymore...EDIT: Don't bother with stack traces, I already found the error. I was misreporting the allowed IO configurations on a base class and Ardour was sending a mono input, which I don't support.EDIT2: New buildavailable.Wow, that was fast. Thank you much! Works like a charm now.

---

### Post #1054 -- Page 36
**User:** Urs
**Info:** Joined: Oct 2003Posts: 652My Studio🎧 20 years | Posts: 652My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16610059&postcount=1054>

Quote: > Originally Posted byRumi➡️BTW, the "crowd funding" of Protoverb apparently led to nothing, unfortunately - Urs wrote that the gathered data didn't show any repeatable characteristics, so it seems that Protoverb won't be turned into a full-featured reverb plugin. Which is a real pity, since it sounds more solid and spatial than most other reverb plugins.Sorry for the super late reply... in the meantime we've had a student intern who applied machine learning to the submissions. While 5% more here or there seemed inconclusive to us a humans, the machine has indeed spotted patterns! We kind of have a tool now that can do the listening tests and place the result on a map, where certain clusters correspond to certain characteristics. Fun stuff, albeit is beyond my field of expertise.


Also, in recent years we have been sent settings that sounded surprisingly good. If we ever find the time we'll probably try to apply the knowledge and these fab settings, and add some more sound shaping control. Not sure in which kind of scope.

---

### Post #1055 -- Page 36
**User:** Rumi
**Info:** Joined: Oct 2003Posts: 1,758My Studio1 Review written🎧 20 years | Posts: 1,758My Studio
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16610414&postcount=1055>

Quote: > Originally Posted byUrs➡️Sorry for the super late reply... in the meantime we've had a student intern who applied machine learning to the submissions. While 5% more here or there seemed inconclusive to us a humans, the machine has indeed spotted patterns! We kind of have a tool now that can do the listening tests and place the result on a map, where certain clusters correspond to certain characteristics. Fun stuff, albeit is beyond my field of expertise.Also, in recent years we have been sent settings that sounded surprisingly good. If we ever find the time we'll probably try to apply the knowledge and these fab settings, and add some more sound shaping control. Not sure in which kind of scope.Na das sind ja gute Neuigkeiten! 


Thank you for taking this further!

---

### Post #1056 -- Page 36
**User:** gentleclockdivid
**Info:** Joined: Mar 2009Posts: 6,373🎧 15 years | Posts: 6,373
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16966575&postcount=1056>

Anyone familiar with reaktor ?

I've read about a series of nested allpasses inside an alpass delay .

This is how I basically done it but not verry  sure where to put the Allpass series (only used 3 ) inside the master allpass loop 
![](https://i.imgur.com/j9FGgN1.jpeg)


And the position inside the master allpassdelay 
![](https://i.imgur.com/OPW4wPc.jpeg)

Which I think is correct , when looking at this picture ( from vallhalla dsp )website 
![](https://i.imgur.com/2aPn7Xd.jpeg)


Pure data has the cyclone allpass~ but since this is a closed external , it's not possible to put allpass series inside of it .

One could make an allpas~ with the block~ 1 and tabsend/receive~ for 1 unit sample feedback but things get messy pretty fast .

---

### Post #1057 -- Page 36
**User:** gentleclockdivid
**Info:** Joined: Mar 2009Posts: 6,373🎧 15 years | Posts: 6,373
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=16971422&postcount=1057>

O.K back to nested allpas because I simpy don't know if it's correct or not .


Some people say that just a feedforward-feedback gain structure around an allpas is already considered nested .


So this is a schroeder alpass in reaktor core  , and the macro below it 
![](https://i.imgur.com/z4JKqwB.jpeg)


Would the picture below  be considered a nested allpas , by inserting an allpas in the feedback structure of an allpass
![](https://i.imgur.com/4uCizUR.jpeg)


Or is  building a feedforward-feedback around an allpass already considered a nested allpas ?
![](https://i.imgur.com/RrVjZuq.jpeg)

---

### Post #1058 -- Page 36
**User:** amberience
**Info:** Joined: Mar 2007Posts: 503🎧 15 years | Posts: 503
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17567273&postcount=1058>

Mild bump, but I love this thread!


I recently prototyped a 4x4 Hadamard FDN reverb, with modulation:
[https://youtu.be/1kMHloRQLcM](https://youtu.be/1kMHloRQLcM)


I was trying to go for a Boss RV-5 'Modulate' kind of thing.

---

### Post #1059 -- Page 36
**User:** amberience
**Info:** Joined: Mar 2007Posts: 503🎧 15 years | Posts: 503
**Date:** Unknown
**Link:** <https://gearspace.com/board/showpost.php?p=17577067&postcount=1059>

Hoping Sean and acreil are still around?? Any tips on how best to analyse reverbs to figure out the internals?


Here's as much as I can figure out:


- Cepstrum analysis can reveal delay time patterns. For example:

![](https://thegearforum.com/attachments/1758915591523-png.52479/)


This is a Cepstrum of an IR of program from the Midiverb II, with the graph gain boosted to raise peaks.


Y-axis (up/down) == frequency

X-axis (left/right) == time


Those red bars are essentially delay times.


Delay Time (ms) = 1000 / Frequency.


So that very top one, at 77hz. Delay time is 12.98ms. Or at a 48kHz sample-rate, 623 samples.



But I don't really have much of a clue about how I'd isolate that to a particular set of APF's at the input as a diffusion network, or how to establish how many APF's might exist. I get that I should look for patterns later on in the IR, for things to do with late reflections. But similar issues there, hard to predict/estimate what the structure might be.


I know you can extrapolate modulation depth and time by running solid sine tones through. I also know that you can extrapolate whether the underlying delay buffers support smooth interpolation or not, by changing room size amounts and such things.


Apart from this thread, are there any good resources on reverse engineering reverbs (and delays tbh!) in order to figure out what was done??


I'm mostly interested in creating some "inspired by" models. But my ADHD is kicking in and I'm really keen to know the innards of my RV-5, Midiverb II, and others!!

