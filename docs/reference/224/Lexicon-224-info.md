## Background



When a client enquired whether I would take a look at some faulty Lexicon reverb units, I immediately visualised a few 1U rack boxes with power supply issues. The reality was very different, and I was introduced to the mighty Lexicon 224 in the form of a gigantic cardboard box and three addled-looking 4U rack units. Thus began a fascinating experience with these groundbreaking and still revered effects units.



## Technology



The Lexicon 224 was among the first digital effects processors. It was designed in the late 1970s using the best technology available, which at the time was the 8080 microprocessor, 12-bit converters and bucketloads of 74S/LS-series logic.



Several improvements were made over the lifetime of the model, leading to a variety of different versions. All are based around an 8-slot cardframe using a now long-obsolete card standard called Multibus I (Multibus II is different). To begin with, only seven cards were fitted to the 224:



## AIN and AOUT (Analogue In and Out)



These two cards contain the input buffer/gain trimming circuitry, anti-aliasing filters (using RC4558 dual opamps) and 12-bit audio converters. Transformer balancing is used, with the two input transformers (the 224 is a stereo unit) mounted directly on the AIN card and the four larger output transformers (allowing two effects or quad operation) located on the rear panel.



The audio converters are 12-bit and both use a single DAC80 DAC IC. Sample-and-hold circuits multiplex the two/four audio channels. The ADC is a successive-approximation type using a DAC and comparator.



Here is the first technical "gotcha" - the two DAC80s are NOT the same. The AOUT card uses a voltage-output device that is still fairly readily available, while the AIN card uses a much-rarer current-output part. Beware! They are not interchangeable.



Although the converters themselves are 12-bit, a clever scaling circuit gives an extra 24dB of headroom by actively shifting the input gain. This gives a 16-bit conversion range overall, though precision is still only 12-bit.



## FPC (Floating Point Converter)



This card converts the 12-bit floating-point data of the AIN and AOUT cards to and from 16-bit fixed-point data for the DSP circuitry.



## ALU (Arithmetic Logic Unit)



In conjunction with the DMEM and T&C cards, the ALU is a 16-bit, fixed-point Digital Signal Processor constructed predominantly from 74-series logic ICs - an amazing achievement. Sample rate is 20kHz and the "DSP" executes 100 operations per sample period, i.e. a 2MHz instruction rate. The ALU card contains the multiplier/accumulator sections of the DSP.



## DMEM



The DMEM card contains the working memory for the discrete DSP. There is 16Kwords of 16-bit wide storage implemented using 4116 DRAMs. These devices require three supply voltages and are known to be a bit temperamental.



## T&C (Timing and Control)



The T&C card provides all clock and control signals for the discrete DSP. A bank of 6810 static RAM devices store the program to be executed; this is decoded into low-level command signals by a further pool of small-scale logic.



## BLC/SBC (Board Level/Single Board Computer)



This is an off-the-shelf single-board computer card manufactured by either Intel or National Semiconductor. It holds an 8080 microprocessor and associated peripheral ICs including parallel ports (used to communicate with the remote control head), serial ports, a small amount of RAM and a bank of four 2716 EPROMs for program storage.



The SBC card manages the unit, handling the user interface and loading the DSP with the selected effect algorithm.



With a 20kHz sampling rate, the audio bandwidth of the original 224 was around 8kHz.



The EPROM firmware for this configuration was revised up to version 4.3. At this point, an eighth card was added to the unit - the NVS (Non Volatile Storage). This contained a block of battery-backed (three AAA NiCds) static RAM and sockets for a greatly enlarged amount of EPROM program storage. User patches could now be stored in non-volatile memory and a larger number of factory patches were included; the firmware for this configuration was version 4.4.



An earlier unit can be upgraded to this specification if an NVS card is available, but it may require a small modification to the cardframe to route an extra signal to the NVS.



## The 224X



The 224X was a major enhancement to the basic design which doubled the audio bandwidth to 16kHz. The essential structure stayed the same but completely new DMEM and T&C cards were required to sustain the doubling of speed. In particular, the 224X DMEM card carries twice the amount of RAM (32Kwords).



Additionally, the analogue filtering on the AIN and AOUT cards was revised to raise the cutoff frequency.



The most recent firmware version for this configuration is version 8.1 (NOT v8.1A).



Unless the replacement DMEM and T&C cards are available, it is not possible to upgrade a standard 224 to 224X specification. Theoretically it would be possible to modify the AIN and AOUT cards rather than replacing them, but this would be a lengthy and expensive process.



## The 224XL



All units to this point had used a basic remote-control "head" allowing limited communication with the user. The enhanced firmware functionality of the 224X pushed this user interface rather harder than it could really handle and it was not long before it was replaced by the LARC (Lexicon Alphanumeric Remote Control) with more buttons,alphanumeric LED displays and a tape interface for saving patches. As an aside, the schematics indicate that this was known for a while as the LURCH...I'm no marketing genius, but even I can see why that got changed :-)



This was known as the 224XL. Firmware started with version 8.1A and proceeded up to 8.2.1.



The LARC is not interchangeable with the earlier remote head - it uses a serial interface rather than the parallel connection of the earlier unit and requires a new header board to be fitted to the chassis.