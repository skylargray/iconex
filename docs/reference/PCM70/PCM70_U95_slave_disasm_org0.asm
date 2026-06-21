; z80dasm 1.1.6
; command line: z80dasm --origin=0 --address --labels --source Lexicon_PCM-70-V2_0-U95.BIN

	org	00000h

l0000h:
	jr l0060h		;0000	18 5e 	. ^ 
l0002h:
	ld a,l			;0002	7d 	} 
l0003h:
	jr z,l0048h		;0003	28 43 	( C 
l0005h:
	add hl,hl			;0005	29 	) 
l0006h:
	jr nz,l004bh		;0006	20 43 	  C 
	ld c,a			;0008	4f 	O 
	ld d,b			;0009	50 	P 
	ld e,c			;000a	59 	Y 
l000bh:
	ld d,d			;000b	52 	R 
l000ch:
	ld c,c			;000c	49 	I 
	ld b,a			;000d	47 	G 
	ld c,b			;000e	48 	H 
	ld d,h			;000f	54 	T 
l0010h:
	jr nz,l005eh		;0010	20 4c 	  L 
	ld b,l			;0012	45 	E 
	ld e,b			;0013	58 	X 
	ld c,c			;0014	49 	I 
	ld b,e			;0015	43 	C 
	ld c,a			;0016	4f 	O 
	ld c,(hl)			;0017	4e 	N 
	inc l			;0018	2c 	, 
	jr nz,$+75		;0019	20 49 	  I 
	ld c,(hl)			;001b	4e 	N 
	ld b,e			;001c	43 	C 
	ld l,020h		;001d	2e 20 	.   
	ld sp,l3839h		;001f	31 39 38 	1 9 8 
	dec (hl)			;0022	35 	5 
	nop			;0023	00 	. 
	nop			;0024	00 	. 
	nop			;0025	00 	. 
	nop			;0026	00 	. 
	nop			;0027	00 	. 
	nop			;0028	00 	. 
	nop			;0029	00 	. 
	nop			;002a	00 	. 
	nop			;002b	00 	. 
	nop			;002c	00 	. 
	nop			;002d	00 	. 
	nop			;002e	00 	. 
	nop			;002f	00 	. 
l0030h:
	nop			;0030	00 	. 
	nop			;0031	00 	. 
l0032h:
	nop			;0032	00 	. 
	nop			;0033	00 	. 
	nop			;0034	00 	. 
	nop			;0035	00 	. 
	nop			;0036	00 	. 
	nop			;0037	00 	. 
	jp l02d3h		;0038	c3 d3 02 	. . . 
	nop			;003b	00 	. 
	nop			;003c	00 	. 
	nop			;003d	00 	. 
	nop			;003e	00 	. 
	nop			;003f	00 	. 
l0040h:
	ld d,b			;0040	50 	P 
	ld b,e			;0041	43 	C 
	ld c,l			;0042	4d 	M 
	scf			;0043	37 	7 
	jr nc,l0066h		;0044	30 20 	0   
	ld d,e			;0046	53 	S 
	ld c,h			;0047	4c 	L 
l0048h:
	ld b,c			;0048	41 	A 
	ld d,(hl)			;0049	56 	V 
	ld b,l			;004a	45 	E 
l004bh:
	jr nz,l008eh		;004b	20 41 	  A 
	ld c,(hl)			;004d	4e 	N 
	ld b,h			;004e	44 	D 
	jr nz,$+85		;004f	20 53 	  S 
l0051h:
	ld d,b			;0051	50 	P 
	ld b,c			;0052	41 	A 
	ld b,e			;0053	43 	C 
	ld b,l			;0054	45 	E 
	ld d,a			;0055	57 	W 
	ld b,c			;0056	41 	A 
	ld d,d			;0057	52 	R 
	ld b,l			;0058	45 	E 
	jr nz,l00b1h		;0059	20 56 	  V 
	ld sp,l322eh		;005b	31 2e 32 	1 . 2 
l005eh:
	jr nc,l0080h		;005e	30 20 	0   
l0060h:
	ld sp,047ffh		;0060	31 ff 47 	1 . G 
	im 1		;0063	ed 56 	. V 
	di			;0065	f3 	. 
l0066h:
	exx			;0066	d9 	. 
	ld b,000h		;0067	06 00 	. . 
	ld c,001h		;0069	0e 01 	. . 
	ld de,04342h		;006b	11 42 43 	. B C 
	exx			;006e	d9 	. 
	ld a,069h		;006f	3e 69 	> i 
	out (030h),a		;0071	d3 30 	. 0 
	ld hl,04000h		;0073	21 00 40 	! . @ 
	ld de,04001h		;0076	11 01 40 	. . @ 
	ld bc,007f5h		;0079	01 f5 07 	. . . 
l007ch:
	xor a			;007c	af 	. 
	ld (hl),a			;007d	77 	w 
	ldir		;007e	ed b0 	. . 
l0080h:
	call sub_0251h		;0080	cd 51 02 	. Q . 
l0083h:
	in a,(050h)		;0083	db 50 	. P 
	bit 0,a		;0085	cb 47 	. G 
	call nz,sub_00fah		;0087	c4 fa 00 	. . . 
	ld a,(04345h)		;008a	3a 45 43 	: E C 
	or a			;008d	b7 	. 
l008eh:
	jp z,l009bh		;008e	ca 9b 00 	. . . 
	call sub_0215h		;0091	cd 15 02 	. . . 
	call sub_01b7h		;0094	cd b7 01 	. . . 
	xor a			;0097	af 	. 
	ld (04345h),a		;0098	32 45 43 	2 E C 
l009bh:
	ld a,(04346h)		;009b	3a 46 43 	: F C 
	or a			;009e	b7 	. 
	jp z,l00a9h		;009f	ca a9 00 	. . . 
	call sub_0281h		;00a2	cd 81 02 	. . . 
l00a5h:
	xor a			;00a5	af 	. 
l00a6h:
	ld (04346h),a		;00a6	32 46 43 	2 F C 
l00a9h:
	ld a,(04348h)		;00a9	3a 48 43 	: H C 
	or a			;00ac	b7 	. 
	jp z,l00b7h		;00ad	ca b7 00 	. . . 
	xor a			;00b0	af 	. 
l00b1h:
	ld (04348h),a		;00b1	32 48 43 	2 H C 
	call sub_0198h		;00b4	cd 98 01 	. . . 
l00b7h:
	xor a			;00b7	af 	. 
	ld b,a			;00b8	47 	G 
	di			;00b9	f3 	. 
	ld hl,04343h		;00ba	21 43 43 	! C C 
	ld a,(hl)			;00bd	7e 	~ 
	or a			;00be	b7 	. 
	jr z,l00c7h		;00bf	28 06 	( . 
	ld (hl),b			;00c1	70 	p 
	call sub_15e3h		;00c2	cd e3 15 	. . . 
	jr l00d0h		;00c5	18 09 	. . 
l00c7h:
	inc hl			;00c7	23 	# 
	ld a,(hl)			;00c8	7e 	~ 
	or a			;00c9	b7 	. 
	jr z,l00d0h		;00ca	28 04 	( . 
	ld (hl),b			;00cc	70 	p 
	call sub_169ah		;00cd	cd 9a 16 	. . . 
l00d0h:
	ei			;00d0	fb 	. 
	ld a,(04353h)		;00d1	3a 53 43 	: S C 
	or a			;00d4	b7 	. 
	call nz,sub_01edh		;00d5	c4 ed 01 	. . . 
	ld a,(04347h)		;00d8	3a 47 43 	: G C 
	or a			;00db	b7 	. 
	jp z,l00ebh		;00dc	ca eb 00 	. . . 
	xor a			;00df	af 	. 
	ld (04347h),a		;00e0	32 47 43 	2 G C 
	call sub_02f9h		;00e3	cd f9 02 	. . . 
	nop			;00e6	00 	. 
	call sub_0883h		;00e7	cd 83 08 	. . . 
	nop			;00ea	00 	. 
l00ebh:
	call sub_0883h		;00eb	cd 83 08 	. . . 
	nop			;00ee	00 	. 
	call sub_0ad2h		;00ef	cd d2 0a 	. . . 
	nop			;00f2	00 	. 
	call sub_0274h		;00f3	cd 74 02 	. t . 
	nop			;00f6	00 	. 
	jp l0083h		;00f7	c3 83 00 	. . . 
sub_00fah:
	in a,(020h)		;00fa	db 20 	.   
	cp 0ffh		;00fc	fe ff 	. . 
	jp z,l0105h		;00fe	ca 05 01 	. . . 
	ld (041c6h),a		;0101	32 c6 41 	2 . A 
	ret			;0104	c9 	. 
l0105h:
	call sub_018eh		;0105	cd 8e 01 	. . . 
	cp 080h		;0108	fe 80 	. . 
l010ah:
	jp c,l013dh		;010a	da 3d 01 	. = . 
	jr z,l0121h		;010d	28 12 	( . 
	cp 081h		;010f	fe 81 	. . 
l0111h:
	jp z,l0178h		;0111	ca 78 01 	. x . 
	cp 083h		;0114	fe 83 	. . 
	jr z,l0127h		;0116	28 0f 	( . 
l0118h:
	ld b,a			;0118	47 	G 
	and 0f0h		;0119	e6 f0 	. . 
	cp 090h		;011b	fe 90 	. . 
l011dh:
	ld a,b			;011d	78 	x 
l011eh:
	jr z,l0139h		;011e	28 19 	( . 
	ret			;0120	c9 	. 
l0121h:
	ld a,001h		;0121	3e 01 	> . 
l0123h:
	ld (04345h),a		;0123	32 45 43 	2 E C 
	ret			;0126	c9 	. 
l0127h:
	call sub_018eh		;0127	cd 8e 01 	. . . 
l012ah:
	ld (04349h),a		;012a	32 49 43 	2 I C 
	call sub_018eh		;012d	cd 8e 01 	. . . 
l0130h:
	ld (0434ah),a		;0130	32 4a 43 	2 J C 
l0133h:
	ld a,001h		;0133	3e 01 	> . 
	ld (04348h),a		;0135	32 48 43 	2 H C 
l0138h:
	ret			;0138	c9 	. 
l0139h:
	ld (04346h),a		;0139	32 46 43 	2 F C 
	ret			;013c	c9 	. 
l013dh:
	ld d,000h		;013d	16 00 	. . 
l013fh:
	ld e,a			;013f	5f 	_ 
l0140h:
	ld hl,04000h		;0140	21 00 40 	! . @ 
	add hl,de			;0143	19 	. 
	call sub_018eh		;0144	cd 8e 01 	. . . 
l0147h:
	ld (hl),a			;0147	77 	w 
	ld a,e			;0148	7b 	{ 
	or a			;0149	b7 	. 
	jr z,l0161h		;014a	28 15 	( . 
	cp 003h		;014c	fe 03 	. . 
	jr nc,l015bh		;014e	30 0b 	0 . 
	ld hl,(04001h)		;0150	2a 01 40 	* . @ 
l0153h:
	ld (041c8h),hl		;0153	22 c8 41 	" . A 
	ld a,0c0h		;0156	3e c0 	> . 
	ld (041c7h),a		;0158	32 c7 41 	2 . A 
l015bh:
	ld a,001h		;015b	3e 01 	> . 
	ld (04347h),a		;015d	32 47 43 	2 G C 
l0160h:
	ret			;0160	c9 	. 
l0161h:
	ld b,(hl)			;0161	46 	F 
	ld a,(04040h)		;0162	3a 40 40 	: @ @ 
	cp b			;0165	b8 	. 
	jr z,l015bh		;0166	28 f3 	( . 
	inc hl			;0168	23 	# 
	xor a			;0169	af 	. 
	ld (hl),a			;016a	77 	w 
l016bh:
	ld d,h			;016b	54 	T 
	ld e,l			;016c	5d 	] 
	inc de			;016d	13 	. 
l016eh:
	ld b,a			;016e	47 	G 
l016fh:
	ld c,02eh		;016f	0e 2e 	. . 
l0171h:
	ldir		;0171	ed b0 	. . 
	inc a			;0173	3c 	< 
	ld (04347h),a		;0174	32 47 43 	2 G C 
l0177h:
	ret			;0177	c9 	. 
l0178h:
	call sub_018eh		;0178	cd 8e 01 	. . . 
l017bh:
	cp 0ffh		;017b	fe ff 	. . 
	jr nz,l0178h		;017d	20 f9 	  . 
	call z,sub_018eh		;017f	cc 8e 01 	. . . 
	cp 082h		;0182	fe 82 	. . 
	jp z,l018dh		;0184	ca 8d 01 	. . . 
	call l013dh		;0187	cd 3d 01 	. = . 
	jp l0178h		;018a	c3 78 01 	. x . 
l018dh:
	ret			;018d	c9 	. 
sub_018eh:
	in a,(050h)		;018e	db 50 	. P 
	bit 0,a		;0190	cb 47 	. G 
	jp z,sub_018eh		;0192	ca 8e 01 	. . . 
	in a,(020h)		;0195	db 20 	.   
	ret			;0197	c9 	. 
sub_0198h:
	ld d,a			;0198	57 	W 
	ld a,(04349h)		;0199	3a 49 43 	: I C 
	add a,a			;019c	87 	. 
	ld e,a			;019d	5f 	_ 
	ld hl,l1902h		;019e	21 02 19 	! . . 
	add hl,de			;01a1	19 	. 
	ld e,(hl)			;01a2	5e 	^ 
	inc hl			;01a3	23 	# 
	ld d,(hl)			;01a4	56 	V 
	ld hl,0434ah		;01a5	21 4a 43 	! J C 
	ld b,(hl)			;01a8	46 	F 
	ex de,hl			;01a9	eb 	. 
	ld c,030h		;01aa	0e 30 	. 0 
l01ach:
	in a,(050h)		;01ac	db 50 	. P 
	bit 1,a		;01ae	cb 4f 	. O 
	jr nz,l01ach		;01b0	20 fa 	  . 
	outi		;01b2	ed a3 	. . 
	jr nz,l01ach		;01b4	20 f6 	  . 
	ret			;01b6	c9 	. 
sub_01b7h:
	ld c,a			;01b7	4f 	O 
	ld a,(04353h)		;01b8	3a 53 43 	: S C 
	or a			;01bb	b7 	. 
	jp nz,l01d4h		;01bc	c2 d4 01 	. . . 
	in a,(050h)		;01bf	db 50 	. P 
	bit 1,a		;01c1	cb 4f 	. O 
	jp z,l01e9h		;01c3	ca e9 01 	. . . 
	ld a,001h		;01c6	3e 01 	> . 
	ld (04353h),a		;01c8	32 53 43 	2 S C 
	ld hl,0434bh		;01cb	21 4b 43 	! K C 
	ld (04354h),hl		;01ce	22 54 43 	" T C 
	ld (04356h),hl		;01d1	22 56 43 	" V C 
l01d4h:
	ld hl,(04354h)		;01d4	2a 54 43 	* T C 
	ld (hl),c			;01d7	71 	q 
	inc hl			;01d8	23 	# 
	ld a,l			;01d9	7d 	} 
	ld (04354h),hl		;01da	22 54 43 	" T C 
	ld hl,04353h		;01dd	21 53 43 	! S C 
	cp l			;01e0	bd 	. 
	ret nc			;01e1	d0 	. 
	ld hl,0434bh		;01e2	21 4b 43 	! K C 
	ld (04354h),hl		;01e5	22 54 43 	" T C 
	ret			;01e8	c9 	. 
l01e9h:
	ld a,c			;01e9	79 	y 
	out (030h),a		;01ea	d3 30 	. 0 
	ret			;01ec	c9 	. 
sub_01edh:
	in a,(050h)		;01ed	db 50 	. P 
	bit 0,a		;01ef	cb 47 	. G 
	ret nz			;01f1	c0 	. 
	ld hl,(04356h)		;01f2	2a 56 43 	* V C 
	ld a,(hl)			;01f5	7e 	~ 
	out (030h),a		;01f6	d3 30 	. 0 
	inc hl			;01f8	23 	# 
	ex de,hl			;01f9	eb 	. 
	ld a,e			;01fa	7b 	{ 
	ld hl,04353h		;01fb	21 53 43 	! S C 
	cp l			;01fe	bd 	. 
	jp nc,l0206h		;01ff	d2 06 02 	. . . 
	ld hl,0434bh		;0202	21 4b 43 	! K C 
	ex de,hl			;0205	eb 	. 
l0206h:
	ld hl,(04354h)		;0206	2a 54 43 	* T C 
	ex de,hl			;0209	eb 	. 
	ld (04356h),hl		;020a	22 56 43 	" V C 
	ld a,l			;020d	7d 	} 
	cp e			;020e	bb 	. 
	ret c			;020f	d8 	. 
	xor a			;0210	af 	. 
	ld (04353h),a		;0211	32 53 43 	2 S C 
	ret			;0214	c9 	. 
sub_0215h:
	call sub_021ch		;0215	cd 1c 02 	. . . 
	call z,sub_023ah		;0218	cc 3a 02 	. : . 
	ret			;021b	c9 	. 
sub_021ch:
	ld a,069h		;021c	3e 69 	> i 
	ld hl,0c000h		;021e	21 00 c0 	! . . 
	add hl,sp			;0221	39 	9 
	ld b,l			;0222	45 	E 
	ld c,h			;0223	4c 	L 
	ld hl,0ffffh		;0224	21 ff ff 	! . . 
	add hl,sp			;0227	39 	9 
l0228h:
	ld d,(hl)			;0228	56 	V 
	ld (hl),a			;0229	77 	w 
	cp (hl)			;022a	be 	. 
	ld (hl),d			;022b	72 	r 
	jr nz,l0237h		;022c	20 09 	  . 
	dec hl			;022e	2b 	+ 
	djnz l0228h		;022f	10 f7 	. . 
	dec c			;0231	0d 	. 
	jp p,l0228h		;0232	f2 28 02 	. ( . 
l0235h:
	xor a			;0235	af 	. 
	ret			;0236	c9 	. 
l0237h:
	ld a,001h		;0237	3e 01 	> . 
	ret			;0239	c9 	. 
sub_023ah:
	ld hl,l3fffh		;023a	21 ff 3f 	! . ? 
	inc l			;023d	2c 	, 
	xor a			;023e	af 	. 
l023fh:
	add a,(hl)			;023f	86 	. 
	dec l			;0240	2d 	- 
	jr nz,l023fh		;0241	20 fc 	  . 
	dec h			;0243	25 	% 
	jp p,l023fh		;0244	f2 3f 02 	. ? . 
	nop			;0247	00 	. 
	ret z			;0248	c8 	. 
	ld a,(l0002h)		;0249	3a 02 00 	: . . 
	or a			;024c	b7 	. 
	ret z			;024d	c8 	. 
	ld a,002h		;024e	3e 02 	> . 
	ret			;0250	c9 	. 
sub_0251h:
	xor a			;0251	af 	. 
	ld hl,04040h		;0252	21 40 40 	! @ @ 
	ld de,04000h		;0255	11 00 40 	. . @ 
	ld (de),a			;0258	12 	. 
	out (000h),a		;0259	d3 00 	. . 
	set 0,a		;025b	cb c7 	. . 
	ld (hl),a			;025d	77 	w 
	out (000h),a		;025e	d3 00 	. . 
	res 0,a		;0260	cb 87 	. . 
	out (000h),a		;0262	d3 00 	. . 
	call sub_0527h		;0264	cd 27 05 	. ' . 
	xor a			;0267	af 	. 
sub_0268h:
	add a,a			;0268	87 	. 
	inc a			;0269	3c 	< 
l026ah:
	out (000h),a		;026a	d3 00 	. . 
	ld b,010h		;026c	06 10 	. . 
l026eh:
	djnz l026eh		;026e	10 fe 	. . 
	xor a			;0270	af 	. 
	out (000h),a		;0271	d3 00 	. . 
	ret			;0273	c9 	. 
sub_0274h:
	ld a,000h		;0274	3e 00 	> . 
	dec a			;0276	3d 	= 
	jp z,l027dh		;0277	ca 7d 02 	. } . 
	ld a,(04040h)		;027a	3a 40 40 	: @ @ 
l027dh:
	call sub_0268h		;027d	cd 68 02 	. h . 
	ret			;0280	c9 	. 
sub_0281h:
	ld de,0fefeh		;0281	11 fe fe 	. . . 
	ld c,090h		;0284	0e 90 	. . 
	cp c			;0286	b9 	. 
	jp z,l029bh		;0287	ca 9b 02 	. . . 
	inc c			;028a	0c 	. 
	cp c			;028b	b9 	. 
	jp z,l0299h		;028c	ca 99 02 	. . . 
	inc c			;028f	0c 	. 
	cp c			;0290	b9 	. 
	jp z,l0295h		;0291	ca 95 02 	. . . 
	ret			;0294	c9 	. 
l0295h:
	ld e,000h		;0295	1e 00 	. . 
	jr l029bh		;0297	18 02 	. . 
l0299h:
	ld d,000h		;0299	16 00 	. . 
l029bh:
	ld c,0feh		;029b	0e fe 	. . 
	xor a			;029d	af 	. 
	ld hl,0403fh		;029e	21 3f 40 	! ? @ 
	ld b,03ch		;02a1	06 3c 	. < 
l02a3h:
	ld (hl),a			;02a3	77 	w 
	dec hl			;02a4	2b 	+ 
	djnz l02a3h		;02a5	10 fc 	. . 
	ld (hl),d			;02a7	72 	r 
	dec hl			;02a8	2b 	+ 
	ld (hl),e			;02a9	73 	s 
	dec hl			;02aa	2b 	+ 
l02abh:
	ld (hl),c			;02ab	71 	q 
	dec hl			;02ac	2b 	+ 
	ld (hl),a			;02ad	77 	w 
	call sub_01b7h		;02ae	cd b7 01 	. . . 
	inc a			;02b1	3c 	< 
	ld (04347h),a		;02b2	32 47 43 	2 G C 
	ret			;02b5	c9 	. 
sub_02b6h:
	ld hl,l2c4ch		;02b6	21 4c 2c 	! L , 
	ld de,0837fh		;02b9	11 7f 83 	.  . 
	ld bc,l0080h		;02bc	01 80 00 	. . . 
	lddr		;02bf	ed b8 	. . 
	ld bc,l0080h		;02c1	01 80 00 	. . . 
	ld de,081ffh		;02c4	11 ff 81 	. . . 
	lddr		;02c7	ed b8 	. . 
	ld bc,l0080h		;02c9	01 80 00 	. . . 
	ld de,082ffh		;02cc	11 ff 82 	. . . 
	lddr		;02cf	ed b8 	. . 
	xor a			;02d1	af 	. 
	ret			;02d2	c9 	. 
l02d3h:
	ex af,af'			;02d3	08 	. 
	dec a			;02d4	3d 	= 
	jr z,l02dbh		;02d5	28 04 	( . 
	ex af,af'			;02d7	08 	. 
	ei			;02d8	fb 	. 
	reti		;02d9	ed 4d 	. M 
l02dbh:
	exx			;02db	d9 	. 
	ex de,hl			;02dc	eb 	. 
	dec (hl)			;02dd	35 	5 
	ex de,hl			;02de	eb 	. 
	dec b			;02df	05 	. 
	jr z,l02eeh		;02e0	28 0c 	( . 
	ld hl,l0000h+1		;02e2	21 01 00 	! . . 
	add hl,de			;02e5	19 	. 
	ld (hl),c			;02e6	71 	q 
l02e7h:
	exx			;02e7	d9 	. 
	ld a,008h		;02e8	3e 08 	> . 
	ex af,af'			;02ea	08 	. 
	ei			;02eb	fb 	. 
	reti		;02ec	ed 4d 	. M 
l02eeh:
	ld b,008h		;02ee	06 08 	. . 
	ld hl,l0002h		;02f0	21 02 00 	! . . 
	add hl,de			;02f3	19 	. 
	ld (hl),c			;02f4	71 	q 
	jr l02e7h		;02f5	18 f0 	. . 
sub_02f7h:
	jr l030bh		;02f7	18 12 	. . 
sub_02f9h:
	ld de,04000h		;02f9	11 00 40 	. . @ 
	ld hl,04040h		;02fc	21 40 40 	! @ @ 
	call sub_0527h		;02ff	cd 27 05 	. ' . 
sub_0302h:
	call l030bh		;0302	cd 0b 03 	. . . 
	jp c,l03beh		;0305	da be 03 	. . . 
	jp l03c5h		;0308	c3 c5 03 	. . . 
l030bh:
	ld a,001h		;030b	3e 01 	> . 
	ld (042e3h),a		;030d	32 e3 42 	2 . B 
l0310h:
	ld hl,(042e6h)		;0310	2a e6 42 	* . B 
	ld a,h			;0313	7c 	| 
l0314h:
	and 008h		;0314	e6 08 	. . 
	jp nz,l031dh		;0316	c2 1d 03 	. . . 
	ld a,h			;0319	7c 	| 
	and 0fbh		;031a	e6 fb 	. . 
	ld h,a			;031c	67 	g 
l031dh:
	add hl,hl			;031d	29 	) 
	ld (042e4h),hl		;031e	22 e4 42 	" . B 
	ld hl,04001h		;0321	21 01 40 	! . @ 
	ld de,l045eh		;0324	11 5e 04 	. ^ . 
	ld bc,041e8h		;0327	01 e8 41 	. . A 
	ret c			;032a	d8 	. 
	inc hl			;032b	23 	# 
	ld a,(041c9h)		;032c	3a c9 41 	: . A 
	call sub_0453h		;032f	cd 53 04 	. S . 
	dec hl			;0332	2b 	+ 
l0333h:
	jp z,l033eh		;0333	ca 3e 03 	. > . 
	ld a,0ffh		;0336	3e ff 	> . 
	ld (04041h),a		;0338	32 41 40 	2 A @ 
	ld (04042h),a		;033b	32 42 40 	2 B @ 
l033eh:
	ld a,(041c8h)		;033e	3a c8 41 	: . A 
l0341h:
	ld (042eah),a		;0341	32 ea 42 	2 . B 
	push hl			;0344	e5 	. 
	ld hl,(04001h)		;0345	2a 01 40 	* . @ 
	ld (042e8h),hl		;0348	22 e8 42 	" . B 
	ld hl,(041c8h)		;034b	2a c8 41 	* . A 
	ld (04001h),hl		;034e	22 01 40 	" . @ 
	pop hl			;0351	e1 	. 
	ld a,007h		;0352	3e 07 	> . 
	ld (042e1h),a		;0354	32 e1 42 	2 . B 
	call sub_039dh		;0357	cd 9d 03 	. . . 
	push hl			;035a	e5 	. 
	ld hl,(042e8h)		;035b	2a e8 42 	* . B 
	ld (04001h),hl		;035e	22 01 40 	" . @ 
	ld hl,04042h		;0361	21 42 40 	! B @ 
	call sub_042fh		;0364	cd 2f 04 	. / . 
	ld (0432ch),a		;0367	32 2c 43 	2 , C 
	ld (042f7h),hl		;036a	22 f7 42 	" . B 
	push de			;036d	d5 	. 
	push bc			;036e	c5 	. 
	ld a,(041a1h)		;036f	3a a1 41 	: . A 
	ld l,a			;0372	6f 	o 
	ld h,000h		;0373	26 00 	& . 
	ld a,(04188h)		;0375	3a 88 41 	: . A 
	cp 020h		;0378	fe 20 	.   
	jp nz,l037fh		;037a	c2 7f 03 	.  . 
	add hl,hl			;037d	29 	) 
	add hl,hl			;037e	29 	) 
l037fh:
	ex de,hl			;037f	eb 	. 
	ld a,(041d5h)		;0380	3a d5 41 	: . A 
	call sub_10e3h		;0383	cd e3 10 	. . . 
	or a			;0386	b7 	. 
	jp z,l038ch		;0387	ca 8c 03 	. . . 
	ld h,0ffh		;038a	26 ff 	& . 
l038ch:
	ld a,h			;038c	7c 	| 
	or a			;038d	b7 	. 
	jp nz,l0392h		;038e	c2 92 03 	. . . 
	inc a			;0391	3c 	< 
l0392h:
	ld (041d6h),a		;0392	32 d6 41 	2 . A 
	ld (04302h),a		;0395	32 02 43 	2 . C 
	pop bc			;0398	c1 	. 
	pop de			;0399	d1 	. 
	pop hl			;039a	e1 	. 
	or a			;039b	b7 	. 
	ret			;039c	c9 	. 
sub_039dh:
	ld a,(042e1h)		;039d	3a e1 42 	: . B 
	dec a			;03a0	3d 	= 
	ld (042e1h),a		;03a1	32 e1 42 	2 . B 
	ret z			;03a4	c8 	. 
	call sub_0452h		;03a5	cd 52 04 	. R . 
	push hl			;03a8	e5 	. 
	push de			;03a9	d5 	. 
	call sub_03b5h		;03aa	cd b5 03 	. . . 
	pop de			;03ad	d1 	. 
	inc de			;03ae	13 	. 
	inc de			;03af	13 	. 
	pop hl			;03b0	e1 	. 
	inc hl			;03b1	23 	# 
	jp sub_039dh		;03b2	c3 9d 03 	. . . 
sub_03b5h:
	push hl			;03b5	e5 	. 
	ex de,hl			;03b6	eb 	. 
	ld e,(hl)			;03b7	5e 	^ 
	inc hl			;03b8	23 	# 
	ld d,(hl)			;03b9	56 	V 
	inc hl			;03ba	23 	# 
	ex de,hl			;03bb	eb 	. 
	pop de			;03bc	d1 	. 
	jp (hl)			;03bd	e9 	. 
l03beh:
	push hl			;03be	e5 	. 
	ld hl,l000ch		;03bf	21 0c 00 	! . . 
	add hl,de			;03c2	19 	. 
	ex de,hl			;03c3	eb 	. 
	pop hl			;03c4	e1 	. 
l03c5h:
	ld a,(042e3h)		;03c5	3a e3 42 	: . B 
	inc a			;03c8	3c 	< 
	ld (042e3h),a		;03c9	32 e3 42 	2 . B 
	cp 00dh		;03cc	fe 0d 	. . 
	jp z,l03edh		;03ce	ca ed 03 	. . . 
	push hl			;03d1	e5 	. 
	ld hl,(042e4h)		;03d2	2a e4 42 	* . B 
	add hl,hl			;03d5	29 	) 
	ld (042e4h),hl		;03d6	22 e4 42 	" . B 
	pop hl			;03d9	e1 	. 
	jp c,l03beh		;03da	da be 03 	. . . 
	cp 002h		;03dd	fe 02 	. . 
	jp z,l0403h		;03df	ca 03 04 	. . . 
	ld a,007h		;03e2	3e 07 	> . 
	ld (042e1h),a		;03e4	32 e1 42 	2 . B 
	call sub_039dh		;03e7	cd 9d 03 	. . . 
	jp l03c5h		;03ea	c3 c5 03 	. . . 
l03edh:
	ld hl,0402bh		;03ed	21 2b 40 	! + @ 
	call sub_0452h		;03f0	cd 52 04 	. R . 
	inc hl			;03f3	23 	# 
	call sub_0452h		;03f4	cd 52 04 	. R . 
	inc hl			;03f7	23 	# 
	call sub_0452h		;03f8	cd 52 04 	. R . 
	inc hl			;03fb	23 	# 
	call sub_0452h		;03fc	cd 52 04 	. R . 
	inc hl			;03ff	23 	# 
	jp sub_0452h		;0400	c3 52 04 	. R . 
l0403h:
	inc hl			;0403	23 	# 
	call sub_0452h		;0404	cd 52 04 	. R . 
	dec hl			;0407	2b 	+ 
	jp z,l0413h		;0408	ca 13 04 	. . . 
	ld a,0ffh		;040b	3e ff 	> . 
	ld (04047h),a		;040d	32 47 40 	2 G @ 
l0410h:
	ld (04048h),a		;0410	32 48 40 	2 H @ 
l0413h:
	ld a,(04007h)		;0413	3a 07 40 	: . @ 
	ld (042eah),a		;0416	32 ea 42 	2 . B 
	ld a,007h		;0419	3e 07 	> . 
	ld (042e1h),a		;041b	32 e1 42 	2 . B 
	call sub_039dh		;041e	cd 9d 03 	. . . 
	push hl			;0421	e5 	. 
	ld hl,04048h		;0422	21 48 40 	! H @ 
	call sub_042fh		;0425	cd 2f 04 	. / . 
	ld (0432dh),a		;0428	32 2d 43 	2 - C 
	pop hl			;042b	e1 	. 
	jp l03c5h		;042c	c3 c5 03 	. . . 
sub_042fh:
	ld a,001h		;042f	3e 01 	> . 
	ld (04300h),a		;0431	32 00 43 	2 . C 
	push de			;0434	d5 	. 
	push bc			;0435	c5 	. 
	ld a,(hl)			;0436	7e 	~ 
	call sub_0f5ch		;0437	cd 5c 0f 	. \ . 
	push af			;043a	f5 	. 
	call sub_0cfah		;043b	cd fa 0c 	. . . 
	pop af			;043e	f1 	. 
	push hl			;043f	e5 	. 
	ld d,a			;0440	57 	W 
	ld a,(042f4h)		;0441	3a f4 42 	: . B 
	or a			;0444	b7 	. 
	jp z,l044dh		;0445	ca 4d 04 	. M . 
	dec a			;0448	3d 	= 
	cp d			;0449	ba 	. 
	jp c,l044eh		;044a	da 4e 04 	. N . 
l044dh:
	ld a,d			;044d	7a 	z 
l044eh:
	pop hl			;044e	e1 	. 
	pop bc			;044f	c1 	. 
	pop de			;0450	d1 	. 
	ret			;0451	c9 	. 
sub_0452h:
	ld a,(hl)			;0452	7e 	~ 
sub_0453h:
	push hl			;0453	e5 	. 
	push de			;0454	d5 	. 
	ld de,l0040h		;0455	11 40 00 	. @ . 
	add hl,de			;0458	19 	. 
	cp (hl)			;0459	be 	. 
	ld (hl),a			;045a	77 	w 
	pop de			;045b	d1 	. 
l045ch:
	pop hl			;045c	e1 	. 
	ret			;045d	c9 	. 
l045eh:
	and e			;045e	a3 	. 
	dec c			;045f	0d 	. 
	ld l,e			;0460	6b 	k 
	rrca			;0461	0f 	. 
	rst 30h			;0462	f7 	. 
	djnz l045ch		;0463	10 f7 	. . 
	djnz l046ah		;0465	10 03 	. . 
	ld (de),a			;0467	12 	. 
l0468h:
	and a			;0468	a7 	. 
	inc de			;0469	13 	. 
l046ah:
	and e			;046a	a3 	. 
	dec c			;046b	0d 	. 
	ld h,d			;046c	62 	b 
	rrca			;046d	0f 	. 
	rst 30h			;046e	f7 	. 
l046fh:
	djnz l0468h		;046f	10 f7 	. . 
	djnz l0476h		;0471	10 03 	. . 
	ld (de),a			;0473	12 	. 
	ld d,h			;0474	54 	T 
	dec d			;0475	15 	. 
l0476h:
	pop af			;0476	f1 	. 
	inc d			;0477	14 	. 
	ret m			;0478	f8 	. 
	ld de,l04efh		;0479	11 ef 04 	. . . 
	rst 30h			;047c	f7 	. 
	djnz l046fh		;047d	10 f0 	. . 
	ld (de),a			;047f	12 	. 
	call nz,0f112h		;0480	c4 12 f1 	. . . 
	inc d			;0483	14 	. 
	pop af			;0484	f1 	. 
	inc d			;0485	14 	. 
	pop af			;0486	f1 	. 
	inc d			;0487	14 	. 
	pop af			;0488	f1 	. 
	inc d			;0489	14 	. 
	pop af			;048a	f1 	. 
	inc d			;048b	14 	. 
	pop af			;048c	f1 	. 
	inc d			;048d	14 	. 
	djnz $+23		;048e	10 15 	. . 
	djnz l04a7h		;0490	10 15 	. . 
	djnz l04a9h		;0492	10 15 	. . 
	djnz l04abh		;0494	10 15 	. . 
	djnz l04adh		;0496	10 15 	. . 
	djnz l04afh		;0498	10 15 	. . 
	xor 004h		;049a	ee 04 	. . 
	xor 004h		;049c	ee 04 	. . 
	xor 004h		;049e	ee 04 	. . 
	xor 004h		;04a0	ee 04 	. . 
	xor 004h		;04a2	ee 04 	. . 
	xor 004h		;04a4	ee 04 	. . 
	cp c			;04a6	b9 	. 
l04a7h:
	dec d			;04a7	15 	. 
	cp c			;04a8	b9 	. 
l04a9h:
	dec d			;04a9	15 	. 
	cp c			;04aa	b9 	. 
l04abh:
	dec d			;04ab	15 	. 
l04ach:
	cp c			;04ac	b9 	. 
l04adh:
	dec d			;04ad	15 	. 
l04aeh:
	cp c			;04ae	b9 	. 
l04afh:
	dec d			;04af	15 	. 
l04b0h:
	cp c			;04b0	b9 	. 
	dec d			;04b1	15 	. 
l04b2h:
	rst 30h			;04b2	f7 	. 
	djnz l04ach		;04b3	10 f7 	. . 
	djnz l04aeh		;04b5	10 f7 	. . 
	djnz l04b0h		;04b7	10 f7 	. . 
	djnz l04b2h		;04b9	10 f7 	. . 
	djnz $-7		;04bb	10 f7 	. . 
	djnz $-7		;04bd	10 f7 	. . 
	djnz $-7		;04bf	10 f7 	. . 
	djnz $-7		;04c1	10 f7 	. . 
	djnz $-7		;04c3	10 f7 	. . 
	djnz $-7		;04c5	10 f7 	. . 
	djnz $-7		;04c7	10 f7 	. . 
	djnz $-114		;04c9	10 8c 	. . 
	dec d			;04cb	15 	. 
	adc a,h			;04cc	8c 	. 
	dec d			;04cd	15 	. 
	adc a,h			;04ce	8c 	. 
	dec d			;04cf	15 	. 
	adc a,h			;04d0	8c 	. 
	dec d			;04d1	15 	. 
	adc a,h			;04d2	8c 	. 
	dec d			;04d3	15 	. 
	adc a,h			;04d4	8c 	. 
	dec d			;04d5	15 	. 
	sbc a,(hl)			;04d6	9e 	. 
	ld de,l119eh		;04d7	11 9e 11 	. . . 
	sbc a,(hl)			;04da	9e 	. 
l04dbh:
	ld de,l119eh		;04db	11 9e 11 	. . . 
	sbc a,(hl)			;04de	9e 	. 
	ld de,l119eh		;04df	11 9e 11 	. . . 
	sbc a,(hl)			;04e2	9e 	. 
	ld de,l119eh		;04e3	11 9e 11 	. . . 
	rst 30h			;04e6	f7 	. 
	djnz $-7		;04e7	10 f7 	. . 
	djnz l04dbh		;04e9	10 f0 	. . 
	ld (de),a			;04eb	12 	. 
	pop af			;04ec	f1 	. 
	inc d			;04ed	14 	. 
	ret			;04ee	c9 	. 
l04efh:
	and 0f8h		;04ef	e6 f8 	. . 
	cp 000h		;04f1	fe 00 	. . 
	push af			;04f3	f5 	. 
	ld a,(0402bh)		;04f4	3a 2b 40 	: + @ 
	jr nz,l04fdh		;04f7	20 04 	  . 
	and 0bfh		;04f9	e6 bf 	. . 
	jr l04ffh		;04fb	18 02 	. . 
l04fdh:
	or 040h		;04fd	f6 40 	. @ 
l04ffh:
	ld (0402bh),a		;04ff	32 2b 40 	2 + @ 
	pop af			;0502	f1 	. 
	rrca			;0503	0f 	. 
	rrca			;0504	0f 	. 
	rrca			;0505	0f 	. 
	cp 010h		;0506	fe 10 	. . 
	jr nc,l051ah		;0508	30 10 	0 . 
	sub 010h		;050a	d6 10 	. . 
	cpl			;050c	2f 	/ 
	inc a			;050d	3c 	< 
	inc a			;050e	3c 	< 
	ld (0418bh),a		;050f	32 8b 41 	2 . A 
	ld a,001h		;0512	3e 01 	> . 
	ld (0418dh),a		;0514	32 8d 41 	2 . A 
	jp l11f8h		;0517	c3 f8 11 	. . . 
l051ah:
	sub 00fh		;051a	d6 0f 	. . 
	ld (0418dh),a		;051c	32 8d 41 	2 . A 
	ld a,001h		;051f	3e 01 	> . 
	ld (0418bh),a		;0521	32 8b 41 	2 . A 
	jp l11f8h		;0524	c3 f8 11 	. . . 
sub_0527h:
	ld a,(de)			;0527	1a 	. 
	cp (hl)			;0528	be 	. 
	jp nz,l0546h		;0529	c2 46 05 	. F . 
l052ch:
	ld hl,0402ch		;052c	21 2c 40 	! , @ 
	ld de,0406ch		;052f	11 6c 40 	. l @ 
	ld a,(de)			;0532	1a 	. 
	cp (hl)			;0533	be 	. 
	jr nz,l053ch		;0534	20 06 	  . 
	push af			;0536	f5 	. 
	xor a			;0537	af 	. 
	out (030h),a		;0538	d3 30 	. 0 
	pop af			;053a	f1 	. 
	ret z			;053b	c8 	. 
l053ch:
	ld (de),a			;053c	12 	. 
	ld (0432bh),a		;053d	32 2b 43 	2 + C 
	ld a,(04040h)		;0540	3a 40 40 	: @ @ 
	ld (04184h),a		;0543	32 84 41 	2 . A 
l0546h:
	di			;0546	f3 	. 
	push af			;0547	f5 	. 
	call sub_071dh		;0548	cd 1d 07 	. . . 
	call sub_02b6h		;054b	cd b6 02 	. . . 
	ld a,001h		;054e	3e 01 	> . 
	out (040h),a		;0550	d3 40 	. @ 
	out (000h),a		;0552	d3 00 	. . 
	out (040h),a		;0554	d3 40 	. @ 
	ld b,010h		;0556	06 10 	. . 
l0558h:
	djnz l0558h		;0558	10 fe 	. . 
	xor a			;055a	af 	. 
	out (000h),a		;055b	d3 00 	. . 
	out (030h),a		;055d	d3 30 	. 0 
	out (040h),a		;055f	d3 40 	. @ 
	ld hl,041e2h		;0561	21 e2 41 	! . A 
	ld b,0ffh		;0564	06 ff 	. . 
	ld a,000h		;0566	3e 00 	> . 
	ld (04340h),a		;0568	32 40 43 	2 @ C 
l056bh:
	ld (hl),a			;056b	77 	w 
	inc hl			;056c	23 	# 
	dec b			;056d	05 	. 
	jp nz,l056bh		;056e	c2 6b 05 	. k . 
	ld a,001h		;0571	3e 01 	> . 
	ld hl,04333h		;0573	21 33 43 	! 3 C 
	ld (hl),a			;0576	77 	w 
	inc hl			;0577	23 	# 
	ld (hl),a			;0578	77 	w 
	xor a			;0579	af 	. 
	ld (040d3h),a		;057a	32 d3 40 	2 . @ 
	pop af			;057d	f1 	. 
	push af			;057e	f5 	. 
	add a,a			;057f	87 	. 
	inc a			;0580	3c 	< 
	ld (04187h),a		;0581	32 87 41 	2 . A 
	pop af			;0584	f1 	. 
	call sub_0ab3h		;0585	cd b3 0a 	. . . 
	cp 0ffh		;0588	fe ff 	. . 
	ret z			;058a	c8 	. 
	push hl			;058b	e5 	. 
	ld (04185h),hl		;058c	22 85 41 	" . A 
	inc hl			;058f	23 	# 
l0590h:
	ld e,(hl)			;0590	5e 	^ 
	inc hl			;0591	23 	# 
	ld d,(hl)			;0592	56 	V 
	ex de,hl			;0593	eb 	. 
	ld (042e6h),hl		;0594	22 e6 42 	" . B 
	ld hl,l0032h		;0597	21 32 00 	! 2 . 
	add hl,de			;059a	19 	. 
	ld a,(hl)			;059b	7e 	~ 
	ld (041d5h),a		;059c	32 d5 41 	2 . A 
	ld de,0001ah		;059f	11 1a 00 	. . . 
	add hl,de			;05a2	19 	. 
	ld de,0418ch		;05a3	11 8c 41 	. . A 
	ld bc,l0003h		;05a6	01 03 00 	. . . 
	ldir		;05a9	ed b0 	. . 
	ld hl,(04185h)		;05ab	2a 85 41 	* . A 
	ld de,l0051h		;05ae	11 51 00 	. Q . 
	add hl,de			;05b1	19 	. 
	ld de,0418fh		;05b2	11 8f 41 	. . A 
	ld bc,l000bh		;05b5	01 0b 00 	. . . 
	ldir		;05b8	ed b0 	. . 
	ld hl,(04185h)		;05ba	2a 85 41 	* . A 
	ld de,08133h		;05bd	11 33 81 	. 3 . 
	add hl,de			;05c0	19 	. 
	ld (042ech),hl		;05c1	22 ec 42 	" . B 
	ld hl,(04185h)		;05c4	2a 85 41 	* . A 
	ld de,07f33h		;05c7	11 33 7f 	. 3  
	add hl,de			;05ca	19 	. 
	ld (042eeh),hl		;05cb	22 ee 42 	" . B 
	ld hl,04041h		;05ce	21 41 40 	! A @ 
	ld b,02fh		;05d1	06 2f 	. / 
	ld a,0ffh		;05d3	3e ff 	> . 
l05d5h:
	ld (hl),a			;05d5	77 	w 
	inc hl			;05d6	23 	# 
	dec b			;05d7	05 	. 
	jp nz,l05d5h		;05d8	c2 d5 05 	. . . 
	pop hl			;05db	e1 	. 
	push hl			;05dc	e5 	. 
	ld de,0005dh		;05dd	11 5d 00 	. ] . 
	add hl,de			;05e0	19 	. 
	ex de,hl			;05e1	eb 	. 
	ld hl,04358h		;05e2	21 58 43 	! X C 
	ld bc,041e2h		;05e5	01 e2 41 	. . A 
l05e8h:
	ld a,(de)			;05e8	1a 	. 
	inc a			;05e9	3c 	< 
	jp z,l06a0h		;05ea	ca a0 06 	. . . 
	ld a,l			;05ed	7d 	} 
	ld (bc),a			;05ee	02 	. 
	inc bc			;05ef	03 	. 
	ld a,h			;05f0	7c 	| 
	ld (bc),a			;05f1	02 	. 
	inc bc			;05f2	03 	. 
	ld a,(de)			;05f3	1a 	. 
	ld (bc),a			;05f4	02 	. 
	inc bc			;05f5	03 	. 
	and 00fh		;05f6	e6 0f 	. . 
	jp z,l0612h		;05f8	ca 12 06 	. . . 
	ld a,(de)			;05fb	1a 	. 
	and 030h		;05fc	e6 30 	. 0 
	cp 000h		;05fe	fe 00 	. . 
l0600h:
	call z,sub_068dh		;0600	cc 8d 06 	. . . 
	cp 010h		;0603	fe 10 	. . 
	call z,sub_0631h		;0605	cc 31 06 	. 1 . 
	cp 020h		;0608	fe 20 	.   
	call z,sub_0616h		;060a	cc 16 06 	. . . 
	cp 030h		;060d	fe 30 	. 0 
	jp nz,l05e8h		;060f	c2 e8 05 	. . . 
l0612h:
	inc de			;0612	13 	. 
	jp l05e8h		;0613	c3 e8 05 	. . . 
sub_0616h:
	push af			;0616	f5 	. 
	push bc			;0617	c5 	. 
	ld a,(de)			;0618	1a 	. 
	inc de			;0619	13 	. 
	and 00fh		;061a	e6 0f 	. . 
	ld b,a			;061c	47 	G 
l061dh:
	call sub_0655h		;061d	cd 55 06 	. U . 
	ld (hl),a			;0620	77 	w 
	inc hl			;0621	23 	# 
	ld a,(de)			;0622	1a 	. 
	inc de			;0623	13 	. 
	ld (hl),a			;0624	77 	w 
	inc hl			;0625	23 	# 
	ld a,(de)			;0626	1a 	. 
	inc de			;0627	13 	. 
	ld (hl),a			;0628	77 	w 
	inc hl			;0629	23 	# 
	dec b			;062a	05 	. 
	jp nz,l061dh		;062b	c2 1d 06 	. . . 
	pop bc			;062e	c1 	. 
	pop af			;062f	f1 	. 
	ret			;0630	c9 	. 
sub_0631h:
	push af			;0631	f5 	. 
	push bc			;0632	c5 	. 
	ld a,(de)			;0633	1a 	. 
	inc de			;0634	13 	. 
	and 00fh		;0635	e6 0f 	. . 
	ld b,a			;0637	47 	G 
l0638h:
	call sub_0655h		;0638	cd 55 06 	. U . 
	dec de			;063b	1b 	. 
	ld a,(de)			;063c	1a 	. 
	inc de			;063d	13 	. 
	and 080h		;063e	e6 80 	. . 
	jp z,l064ah		;0640	ca 4a 06 	. J . 
	ld a,(de)			;0643	1a 	. 
	ld (hl),a			;0644	77 	w 
	inc hl			;0645	23 	# 
	inc de			;0646	13 	. 
	call sub_0655h		;0647	cd 55 06 	. U . 
l064ah:
	ld a,(de)			;064a	1a 	. 
	ld (hl),a			;064b	77 	w 
	inc hl			;064c	23 	# 
	inc de			;064d	13 	. 
	dec b			;064e	05 	. 
	jp nz,l0638h		;064f	c2 38 06 	. 8 . 
	pop bc			;0652	c1 	. 
	pop af			;0653	f1 	. 
	ret			;0654	c9 	. 
sub_0655h:
	ld a,(de)			;0655	1a 	. 
	and 07fh		;0656	e6 7f 	.  
	push de			;0658	d5 	. 
	push hl			;0659	e5 	. 
	ld l,a			;065a	6f 	o 
	ld h,000h		;065b	26 00 	& . 
	ld de,08300h		;065d	11 00 83 	. . . 
	add hl,de			;0660	19 	. 
	ex de,hl			;0661	eb 	. 
	pop hl			;0662	e1 	. 
	ld (hl),e			;0663	73 	s 
	inc hl			;0664	23 	# 
	ld (hl),d			;0665	72 	r 
	inc hl			;0666	23 	# 
	call sub_0e51h		;0667	cd 51 0e 	. Q . 
	cpl			;066a	2f 	/ 
	bit 4,a		;066b	cb 67 	. g 
	jp z,l0686h		;066d	ca 86 06 	. . . 
	push bc			;0670	c5 	. 
	and 00fh		;0671	e6 0f 	. . 
	ld b,a			;0673	47 	G 
	inc de			;0674	13 	. 
	call sub_0e51h		;0675	cd 51 0e 	. Q . 
	cpl			;0678	2f 	/ 
	and 001h		;0679	e6 01 	. . 
	rla			;067b	17 	. 
	rla			;067c	17 	. 
	rla			;067d	17 	. 
	rla			;067e	17 	. 
	or b			;067f	b0 	. 
	set 7,a		;0680	cb ff 	. . 
	pop bc			;0682	c1 	. 
	jp l068ah		;0683	c3 8a 06 	. . . 
l0686h:
	and 007h		;0686	e6 07 	. . 
	rla			;0688	17 	. 
	rla			;0689	17 	. 
l068ah:
	pop de			;068a	d1 	. 
	inc de			;068b	13 	. 
	ret			;068c	c9 	. 
sub_068dh:
	push af			;068d	f5 	. 
	push bc			;068e	c5 	. 
	ld a,(de)			;068f	1a 	. 
	inc de			;0690	13 	. 
	and 00fh		;0691	e6 0f 	. . 
	ld b,a			;0693	47 	G 
l0694h:
	call sub_0655h		;0694	cd 55 06 	. U . 
	ld (hl),a			;0697	77 	w 
	inc hl			;0698	23 	# 
	dec b			;0699	05 	. 
	jp nz,l0694h		;069a	c2 94 06 	. . . 
	pop bc			;069d	c1 	. 
	pop af			;069e	f1 	. 
	ret			;069f	c9 	. 
l06a0h:
	ld hl,l0010h		;06a0	21 10 00 	! . . 
	ld (04335h),hl		;06a3	22 35 43 	" 5 C 
	ld a,(04187h)		;06a6	3a 87 41 	: . A 
	res 0,a		;06a9	cb 87 	. . 
	ld (04187h),a		;06ab	32 87 41 	2 . A 
	call sub_0953h		;06ae	cd 53 09 	. S . 
	pop hl			;06b1	e1 	. 
	ld hl,(04185h)		;06b2	2a 85 41 	* . A 
	ld de,00233h		;06b5	11 33 02 	. 3 . 
	add hl,de			;06b8	19 	. 
	ld de,08300h		;06b9	11 00 83 	. . . 
	ld bc,l0080h		;06bc	01 80 00 	. . . 
	ldir		;06bf	ed b0 	. . 
	ld a,000h		;06c1	3e 00 	> . 
	or a			;06c3	b7 	. 
	jp z,l06d8h		;06c4	ca d8 06 	. . . 
	ld a,(l0003h+1)		;06c7	3a 04 00 	: . . 
	ld (0c080h),a		;06ca	32 80 c0 	2 . . 
	ld bc,l0080h		;06cd	01 80 00 	. . . 
	ld de,0c080h		;06d0	11 80 c0 	. . . 
	ldir		;06d3	ed b0 	. . 
	ld a,(0c000h)		;06d5	3a 00 c0 	: . . 
l06d8h:
	ld hl,(04185h)		;06d8	2a 85 41 	* . A 
	ld de,00233h		;06db	11 33 02 	. 3 . 
	add hl,de			;06de	19 	. 
	ld de,04100h		;06df	11 00 41 	. . A 
	ld bc,l0080h		;06e2	01 80 00 	. . . 
	ldir		;06e5	ed b0 	. . 
	ld hl,l0000h		;06e7	21 00 00 	! . . 
	ld (04330h),hl		;06ea	22 30 43 	" 0 C 
	ld a,(042f0h)		;06ed	3a f0 42 	: . B 
	and 040h		;06f0	e6 40 	. @ 
	or 001h		;06f2	f6 01 	. . 
	ld (042f0h),a		;06f4	32 f0 42 	2 . B 
l06f7h:
	ld a,(042f0h)		;06f7	3a f0 42 	: . B 
	or a			;06fa	b7 	. 
	jp m,l0709h		;06fb	fa 09 07 	. . . 
	and 001h		;06fe	e6 01 	. . 
	jp z,l0709h		;0700	ca 09 07 	. . . 
	call sub_0883h		;0703	cd 83 08 	. . . 
	jp l06f7h		;0706	c3 f7 06 	. . . 
l0709h:
	ld de,04000h		;0709	11 00 40 	. . @ 
	ld hl,04040h		;070c	21 40 40 	! @ @ 
	ld a,(de)			;070f	1a 	. 
	ld (hl),a			;0710	77 	w 
	call sub_0805h		;0711	cd 05 08 	. . . 
	ld a,(04040h)		;0714	3a 40 40 	: @ @ 
	cp 004h		;0717	fe 04 	. . 
	jr c,l071ch		;0719	38 01 	8 . 
	ei			;071b	fb 	. 
l071ch:
	ret			;071c	c9 	. 
sub_071dh:
	ld a,(042e7h)		;071d	3a e7 42 	: . B 
	and 080h		;0720	e6 80 	. . 
	jp nz,l0779h		;0722	c2 79 07 	. y . 
l0725h:
	ld hl,(041fah)		;0725	2a fa 41 	* . A 
	ld a,(041fch)		;0728	3a fc 41 	: . A 
	and 00fh		;072b	e6 0f 	. . 
	ld c,a			;072d	4f 	O 
	ld a,(041ffh)		;072e	3a ff 41 	: . A 
	add a,c			;0731	81 	. 
	ld c,a			;0732	4f 	O 
	ld a,(04202h)		;0733	3a 02 42 	: . B 
	add a,c			;0736	81 	. 
	ld c,a			;0737	4f 	O 
	ld a,(04205h)		;0738	3a 05 42 	: . B 
	add a,c			;073b	81 	. 
	ld c,a			;073c	4f 	O 
	ret z			;073d	c8 	. 
	ld b,001h		;073e	06 01 	. . 
l0740h:
	ld e,(hl)			;0740	5e 	^ 
	inc hl			;0741	23 	# 
	ld d,(hl)			;0742	56 	V 
	inc hl			;0743	23 	# 
	ld a,(hl)			;0744	7e 	~ 
	bit 7,a		;0745	cb 7f 	.  
	jp nz,l0759h		;0747	c2 59 07 	. Y . 
	sub 004h		;074a	d6 04 	. . 
	jp c,l0769h		;074c	da 69 07 	. i . 
	ld (hl),a			;074f	77 	w 
	ld b,a			;0750	47 	G 
	call sub_0ecch		;0751	cd cc 0e 	. . . 
	ld b,000h		;0754	06 00 	. . 
	jp l0769h		;0756	c3 69 07 	. i . 
l0759h:
	res 7,a		;0759	cb bf 	. . 
	sub 001h		;075b	d6 01 	. . 
	jp c,l0769h		;075d	da 69 07 	. i . 
	set 7,a		;0760	cb ff 	. . 
	ld (hl),a			;0762	77 	w 
	ld b,a			;0763	47 	G 
	call sub_0ecch		;0764	cd cc 0e 	. . . 
	ld b,000h		;0767	06 00 	. . 
l0769h:
	inc hl			;0769	23 	# 
	dec c			;076a	0d 	. 
	jp nz,l0740h		;076b	c2 40 07 	. @ . 
	ld a,b			;076e	78 	x 
	or a			;076f	b7 	. 
	jp nz,l0779h		;0770	c2 79 07 	. y . 
	call sub_14dch		;0773	cd dc 14 	. . . 
	jp l0725h		;0776	c3 25 07 	. % . 
l0779h:
	ld hl,04000h		;0779	21 00 40 	! . @ 
	ld de,04080h		;077c	11 80 40 	. . @ 
	ld bc,l0030h		;077f	01 30 00 	. 0 . 
	ldir		;0782	ed b0 	. . 
	ld hl,04040h		;0784	21 40 40 	! @ @ 
	ld de,04000h		;0787	11 00 40 	. . @ 
	ld bc,l0030h		;078a	01 30 00 	. 0 . 
	ldir		;078d	ed b0 	. . 
	ld a,(042e7h)		;078f	3a e7 42 	: . B 
	and 020h		;0792	e6 20 	.   
	jp nz,l07b3h		;0794	c2 b3 07 	. . . 
	ld a,(042e7h)		;0797	3a e7 42 	: . B 
	ld b,004h		;079a	06 04 	. . 
	ld hl,l3ffeh		;079c	21 fe 3f 	! . ? 
	ld de,l0006h		;079f	11 06 00 	. . . 
l07a2h:
	dec b			;07a2	05 	. 
	jp z,l07aeh		;07a3	ca ae 07 	. . . 
	rla			;07a6	17 	. 
	jp c,l07a2h		;07a7	da a2 07 	. . . 
	add hl,de			;07aa	19 	. 
	jp l07a2h		;07ab	c3 a2 07 	. . . 
l07aeh:
	ld a,0ffh		;07ae	3e ff 	> . 
	ld (hl),a			;07b0	77 	w 
	ld b,000h		;07b1	06 00 	. . 
l07b3h:
	ld a,(042e7h)		;07b3	3a e7 42 	: . B 
	and 010h		;07b6	e6 10 	. . 
	jp nz,l07ebh		;07b8	c2 eb 07 	. . . 
	ld a,(042e7h)		;07bb	3a e7 42 	: . B 
	ld b,005h		;07be	06 05 	. . 
	ld hl,l3ffbh		;07c0	21 fb 3f 	! . ? 
	ld de,l0006h		;07c3	11 06 00 	. . . 
l07c6h:
	dec b			;07c6	05 	. 
	jp z,l07d2h		;07c7	ca d2 07 	. . . 
	rla			;07ca	17 	. 
	jp c,l07c6h		;07cb	da c6 07 	. . . 
	add hl,de			;07ce	19 	. 
	jp l07c6h		;07cf	c3 c6 07 	. . . 
l07d2h:
	push hl			;07d2	e5 	. 
	ld c,006h		;07d3	0e 06 	. . 
	ld b,000h		;07d5	06 00 	. . 
l07d7h:
	ld a,(hl)			;07d7	7e 	~ 
	sub 008h		;07d8	d6 08 	. . 
	ld (hl),a			;07da	77 	w 
	jp nc,l07e3h		;07db	d2 e3 07 	. . . 
	ld (hl),000h		;07de	36 00 	6 . 
	jp l07e5h		;07e0	c3 e5 07 	. . . 
l07e3h:
	ld b,001h		;07e3	06 01 	. . 
l07e5h:
	inc hl			;07e5	23 	# 
	dec c			;07e6	0d 	. 
	jp nz,l07d7h		;07e7	c2 d7 07 	. . . 
	pop hl			;07ea	e1 	. 
l07ebh:
	push hl			;07eb	e5 	. 
	push bc			;07ec	c5 	. 
	call sub_0302h		;07ed	cd 02 03 	. . . 
	pop bc			;07f0	c1 	. 
	pop hl			;07f1	e1 	. 
	ld a,b			;07f2	78 	x 
	or a			;07f3	b7 	. 
	jp nz,l07d2h		;07f4	c2 d2 07 	. . . 
	out (040h),a		;07f7	d3 40 	. @ 
l07f9h:
	ld hl,04080h		;07f9	21 80 40 	! . @ 
	ld de,04000h		;07fc	11 00 40 	. . @ 
	ld bc,l0030h		;07ff	01 30 00 	. 0 . 
	ldir		;0802	ed b0 	. . 
	ret			;0804	c9 	. 
sub_0805h:
	ld a,(042e7h)		;0805	3a e7 42 	: . B 
	and 010h		;0808	e6 10 	. . 
	jp nz,l0877h		;080a	c2 77 08 	. w . 
	ld a,(042e7h)		;080d	3a e7 42 	: . B 
	ld b,005h		;0810	06 05 	. . 
	ld hl,l3ffbh		;0812	21 fb 3f 	! . ? 
	ld de,l0006h		;0815	11 06 00 	. . . 
l0818h:
	dec b			;0818	05 	. 
	jp z,l0824h		;0819	ca 24 08 	. $ . 
	rla			;081c	17 	. 
	jp c,l0818h		;081d	da 18 08 	. . . 
	add hl,de			;0820	19 	. 
	jp l0818h		;0821	c3 18 08 	. . . 
l0824h:
	push hl			;0824	e5 	. 
	ld de,04081h		;0825	11 81 40 	. . @ 
	ld bc,l0006h		;0828	01 06 00 	. . . 
	ldir		;082b	ed b0 	. . 
	pop hl			;082d	e1 	. 
	push hl			;082e	e5 	. 
	ld d,h			;082f	54 	T 
	ld e,l			;0830	5d 	] 
	inc e			;0831	1c 	. 
	ld bc,l0005h		;0832	01 05 00 	. . . 
	xor a			;0835	af 	. 
	ld (hl),a			;0836	77 	w 
	ldir		;0837	ed b0 	. . 
	out (040h),a		;0839	d3 40 	. @ 
	call sub_0302h		;083b	cd 02 03 	. . . 
	ld a,(04187h)		;083e	3a 87 41 	: . A 
	set 0,a		;0841	cb c7 	. . 
	ld (04187h),a		;0843	32 87 41 	2 . A 
	ld hl,04081h		;0846	21 81 40 	! . @ 
	ld c,006h		;0849	0e 06 	. . 
	ld b,000h		;084b	06 00 	. . 
	pop de			;084d	d1 	. 
l084eh:
	push de			;084e	d5 	. 
	ld b,000h		;084f	06 00 	. . 
l0851h:
	ld a,(de)			;0851	1a 	. 
	add a,008h		;0852	c6 08 	. . 
	jr c,l0859h		;0854	38 03 	8 . 
	cp (hl)			;0856	be 	. 
	jr c,l085ch		;0857	38 03 	8 . 
l0859h:
	ld a,(hl)			;0859	7e 	~ 
	jr l085eh		;085a	18 02 	. . 
l085ch:
	ld b,001h		;085c	06 01 	. . 
l085eh:
	ld (de),a			;085e	12 	. 
	inc de			;085f	13 	. 
	inc hl			;0860	23 	# 
	dec c			;0861	0d 	. 
	jr nz,l0851h		;0862	20 ed 	  . 
	push bc			;0864	c5 	. 
	out (040h),a		;0865	d3 40 	. @ 
	call sub_0302h		;0867	cd 02 03 	. . . 
	pop bc			;086a	c1 	. 
	pop de			;086b	d1 	. 
	ld hl,04081h		;086c	21 81 40 	! . @ 
	ld a,b			;086f	78 	x 
	or a			;0870	b7 	. 
	ld c,006h		;0871	0e 06 	. . 
	jp nz,l084eh		;0873	c2 4e 08 	. N . 
	ret			;0876	c9 	. 
l0877h:
	ld a,(04187h)		;0877	3a 87 41 	: . A 
	set 0,a		;087a	cb c7 	. . 
	ld (04187h),a		;087c	32 87 41 	2 . A 
	call sub_0302h		;087f	cd 02 03 	. . . 
	ret			;0882	c9 	. 
sub_0883h:
	ld a,(042f0h)		;0883	3a f0 42 	: . B 
	bit 0,a		;0886	cb 47 	. G 
	ret z			;0888	c8 	. 
	ld b,a			;0889	47 	G 
	ld a,(042e7h)		;088a	3a e7 42 	: . B 
	and 080h		;088d	e6 80 	. . 
	jp nz,l091dh		;088f	c2 1d 09 	. . . 
	ld hl,(04206h)		;0892	2a 06 42 	* . B 
	ld a,(04208h)		;0895	3a 08 42 	: . B 
	and 00fh		;0898	e6 0f 	. . 
	jp z,l091dh		;089a	ca 1d 09 	. . . 
	ld c,a			;089d	4f 	O 
	ld a,b			;089e	78 	x 
	or a			;089f	b7 	. 
	ld a,c			;08a0	79 	y 
	ld c,000h		;08a1	0e 00 	. . 
	jp m,l08ddh		;08a3	fa dd 08 	. . . 
l08a6h:
	push af			;08a6	f5 	. 
	ld e,(hl)			;08a7	5e 	^ 
	inc hl			;08a8	23 	# 
	ld d,(hl)			;08a9	56 	V 
	inc hl			;08aa	23 	# 
	ld a,(hl)			;08ab	7e 	~ 
	and 01fh		;08ac	e6 1f 	. . 
	jp z,l08b9h		;08ae	ca b9 08 	. . . 
	dec a			;08b1	3d 	= 
	ld (hl),a			;08b2	77 	w 
	ld b,a			;08b3	47 	G 
	call sub_0ecch		;08b4	cd cc 0e 	. . . 
	ld c,001h		;08b7	0e 01 	. . 
l08b9h:
	inc hl			;08b9	23 	# 
	inc hl			;08ba	23 	# 
	inc hl			;08bb	23 	# 
	pop af			;08bc	f1 	. 
	dec a			;08bd	3d 	= 
	jp nz,l08a6h		;08be	c2 a6 08 	. . . 
	dec c			;08c1	0d 	. 
	ret z			;08c2	c8 	. 
	ld hl,(0432eh)		;08c3	2a 2e 43 	* . C 
	call sub_0922h		;08c6	cd 22 09 	. " . 
	ld a,(042f0h)		;08c9	3a f0 42 	: . B 
	and 040h		;08cc	e6 40 	. @ 
	jp z,l08d7h		;08ce	ca d7 08 	. . . 
	ld a,040h		;08d1	3e 40 	> @ 
	ld (042f0h),a		;08d3	32 f0 42 	2 . B 
	ret			;08d6	c9 	. 
l08d7h:
	ld a,081h		;08d7	3e 81 	> . 
	ld (042f0h),a		;08d9	32 f0 42 	2 . B 
	ret			;08dc	c9 	. 
l08ddh:
	push af			;08dd	f5 	. 
	ld e,(hl)			;08de	5e 	^ 
	inc hl			;08df	23 	# 
	ld d,(hl)			;08e0	56 	V 
	inc hl			;08e1	23 	# 
	ld a,(hl)			;08e2	7e 	~ 
	and 01fh		;08e3	e6 1f 	. . 
	ld b,a			;08e5	47 	G 
	call sub_0e51h		;08e6	cd 51 0e 	. Q . 
	cpl			;08e9	2f 	/ 
	bit 4,a		;08ea	cb 67 	. g 
	jp z,l0904h		;08ec	ca 04 09 	. . . 
	push bc			;08ef	c5 	. 
	and 00fh		;08f0	e6 0f 	. . 
	ld b,a			;08f2	47 	G 
	inc de			;08f3	13 	. 
	call sub_0e51h		;08f4	cd 51 0e 	. Q . 
	dec de			;08f7	1b 	. 
	cpl			;08f8	2f 	/ 
	and 001h		;08f9	e6 01 	. . 
	rla			;08fb	17 	. 
	rla			;08fc	17 	. 
	rla			;08fd	17 	. 
	rla			;08fe	17 	. 
	or b			;08ff	b0 	. 
	pop bc			;0900	c1 	. 
	jp l0908h		;0901	c3 08 09 	. . . 
l0904h:
	and 007h		;0904	e6 07 	. . 
	rla			;0906	17 	. 
	rla			;0907	17 	. 
l0908h:
	cp b			;0908	b8 	. 
	jp z,l0913h		;0909	ca 13 09 	. . . 
	inc b			;090c	04 	. 
	ld (hl),b			;090d	70 	p 
	call sub_0ecch		;090e	cd cc 0e 	. . . 
	ld c,001h		;0911	0e 01 	. . 
l0913h:
	inc hl			;0913	23 	# 
	inc hl			;0914	23 	# 
	inc hl			;0915	23 	# 
	pop af			;0916	f1 	. 
	dec a			;0917	3d 	= 
	jp nz,l08ddh		;0918	c2 dd 08 	. . . 
	dec c			;091b	0d 	. 
	ret z			;091c	c8 	. 
l091dh:
	xor a			;091d	af 	. 
	ld (042f0h),a		;091e	32 f0 42 	2 . B 
	ret			;0921	c9 	. 
sub_0922h:
	ld (04330h),hl		;0922	22 30 43 	" 0 C 
	ld c,l			;0925	4d 	M 
	ld b,h			;0926	44 	D 
	ld hl,(04206h)		;0927	2a 06 42 	* . B 
	ld a,(04208h)		;092a	3a 08 42 	: . B 
l092dh:
	and 00fh		;092d	e6 0f 	. . 
	ret z			;092f	c8 	. 
	push bc			;0930	c5 	. 
	ld e,(hl)			;0931	5e 	^ 
	inc hl			;0932	23 	# 
	ld d,(hl)			;0933	56 	V 
	inc hl			;0934	23 	# 
	inc hl			;0935	23 	# 
	ld c,(hl)			;0936	4e 	N 
	inc hl			;0937	23 	# 
	ld b,(hl)			;0938	46 	F 
	inc hl			;0939	23 	# 
	ex (sp),hl			;093a	e3 	. 
	push af			;093b	f5 	. 
	push hl			;093c	e5 	. 
	push de			;093d	d5 	. 
	call sub_0a4ah		;093e	cd 4a 0a 	. J . 
	ld e,c			;0941	59 	Y 
	nop			;0942	00 	. 
	nop			;0943	00 	. 
	ld d,b			;0944	50 	P 
	nop			;0945	00 	. 
	nop			;0946	00 	. 
	pop hl			;0947	e1 	. 
	pop bc			;0948	c1 	. 
	call sub_13cbh		;0949	cd cb 13 	. . . 
	pop af			;094c	f1 	. 
	pop hl			;094d	e1 	. 
	dec a			;094e	3d 	= 
	jp nz,l092dh		;094f	c2 2d 09 	. - . 
	ret			;0952	c9 	. 
sub_0953h:
	ld a,(04198h)		;0953	3a 98 41 	: . A 
	ld c,a			;0956	4f 	O 
	ld a,(04198h)		;0957	3a 98 41 	: . A 
	ld b,a			;095a	47 	G 
	ld a,(0402ch)		;095b	3a 2c 40 	: , @ 
	add a,c			;095e	81 	. 
	ld c,a			;095f	4f 	O 
	ld a,(04199h)		;0960	3a 99 41 	: . A 
	cp c			;0963	b9 	. 
	jp c,l0968h		;0964	da 68 09 	. h . 
	ld a,c			;0967	79 	y 
l0968h:
	ld l,a			;0968	6f 	o 
	ld h,000h		;0969	26 00 	& . 
	ld c,h			;096b	4c 	L 
	call sub_0cc9h		;096c	cd c9 0c 	. . . 
	ex de,hl			;096f	eb 	. 
	add hl,hl			;0970	29 	) 
	add hl,hl			;0971	29 	) 
	add hl,hl			;0972	29 	) 
	add hl,hl			;0973	29 	) 
	ld a,h			;0974	7c 	| 
	ld (041a1h),a		;0975	32 a1 41 	2 . A 
	ld hl,(04191h)		;0978	2a 91 41 	* . A 
	ld bc,(0418fh)		;097b	ed 4b 8f 41 	. K . A 
	ld a,(041a1h)		;097f	3a a1 41 	: . A 
	call sub_0a9ch		;0982	cd 9c 0a 	. . . 
	inc bc			;0985	03 	. 
	ld (0419dh),bc		;0986	ed 43 9d 41 	. C . A 
	ld hl,08000h		;098a	21 00 80 	! . . 
	or a			;098d	b7 	. 
	sbc hl,bc		;098e	ed 42 	. B 
	ld (041a3h),hl		;0990	22 a3 41 	" . A 
	ld hl,08280h		;0993	21 80 82 	! . . 
	ld (0433ch),hl		;0996	22 3c 43 	" < C 
	ld hl,08180h		;0999	21 80 81 	! . . 
	ld (0433eh),hl		;099c	22 3e 43 	" > C 
	ld a,(041a1h)		;099f	3a a1 41 	: . A 
	sub 010h		;09a2	d6 10 	. . 
	ld e,a			;09a4	5f 	_ 
	ld d,000h		;09a5	16 00 	. . 
	ld a,(04197h)		;09a7	3a 97 41 	: . A 
	call sub_10d3h		;09aa	cd d3 10 	. . . 
	add hl,hl			;09ad	29 	) 
	add hl,hl			;09ae	29 	) 
	ld a,h			;09af	7c 	| 
	add a,010h		;09b0	c6 10 	. . 
	ld (041a2h),a		;09b2	32 a2 41 	2 . A 
	ld bc,(04193h)		;09b5	ed 4b 93 41 	. K . A 
	ld hl,(0418fh)		;09b9	2a 8f 41 	* . A 
	or a			;09bc	b7 	. 
	sbc hl,bc		;09bd	ed 42 	. B 
	push hl			;09bf	e5 	. 
	ld hl,(04195h)		;09c0	2a 95 41 	* . A 
	or a			;09c3	b7 	. 
	sbc hl,bc		;09c4	ed 42 	. B 
	add hl,hl			;09c6	29 	) 
	add hl,hl			;09c7	29 	) 
	ld b,h			;09c8	44 	D 
	ld c,l			;09c9	4d 	M 
	pop de			;09ca	d1 	. 
	call 00d61h		;09cb	cd 61 0d 	. a . 
	call 00d61h		;09ce	cd 61 0d 	. a . 
	ex de,hl			;09d1	eb 	. 
	call sub_0cc9h		;09d2	cd c9 0c 	. . . 
	ld a,(041a2h)		;09d5	3a a2 41 	: . A 
	cp d			;09d8	ba 	. 
	jp c,l09e0h		;09d9	da e0 09 	. . . 
	ld a,d			;09dc	7a 	z 
	ld (041a2h),a		;09dd	32 a2 41 	2 . A 
l09e0h:
	ld a,(04000h)		;09e0	3a 00 40 	: . @ 
	call sub_0ab3h		;09e3	cd b3 0a 	. . . 
	push hl			;09e6	e5 	. 
	ld de,l0030h		;09e7	11 30 00 	. 0 . 
	add hl,de			;09ea	19 	. 
	ld a,(hl)			;09eb	7e 	~ 
	inc a			;09ec	3c 	< 
	pop hl			;09ed	e1 	. 
	ld (04341h),a		;09ee	32 41 43 	2 A C 
	jp z,l0a2dh		;09f1	ca 2d 0a 	. - . 
	ld de,l0133h		;09f4	11 33 01 	. 3 . 
	add hl,de			;09f7	19 	. 
	ld d,h			;09f8	54 	T 
	ld e,l			;09f9	5d 	] 
	ld bc,l0080h		;09fa	01 80 00 	. . . 
	add hl,bc			;09fd	09 	. 
l09feh:
	ld a,(de)			;09fe	1a 	. 
	cpl			;09ff	2f 	/ 
l0a00h:
	ld c,a			;0a00	4f 	O 
	ld a,(hl)			;0a01	7e 	~ 
l0a02h:
	cpl			;0a02	2f 	/ 
	ld b,a			;0a03	47 	G 
	inc de			;0a04	13 	. 
	inc hl			;0a05	23 	# 
	push hl			;0a06	e5 	. 
	call sub_0a4ah		;0a07	cd 4a 0a 	. J . 
	push de			;0a0a	d5 	. 
	ld hl,(0433eh)		;0a0b	2a 3e 43 	* > C 
	ld de,(0433ch)		;0a0e	ed 5b 3c 43 	. [ < C 
	ld a,b			;0a12	78 	x 
	cpl			;0a13	2f 	/ 
	ld (hl),a			;0a14	77 	w 
	ld a,c			;0a15	79 	y 
	cpl			;0a16	2f 	/ 
	ld (de),a			;0a17	12 	. 
	inc de			;0a18	13 	. 
	inc hl			;0a19	23 	# 
	ld (0433eh),hl		;0a1a	22 3e 43 	" > C 
	ld (0433ch),de		;0a1d	ed 53 3c 43 	. S < C 
	ld de,08200h		;0a21	11 00 82 	. . . 
	or a			;0a24	b7 	. 
	sbc hl,de		;0a25	ed 52 	. R 
	pop de			;0a27	d1 	. 
	pop hl			;0a28	e1 	. 
	ret z			;0a29	c8 	. 
	jp l09feh		;0a2a	c3 fe 09 	. . . 
l0a2dh:
	ld de,l0133h		;0a2d	11 33 01 	. 3 . 
	add hl,de			;0a30	19 	. 
	ld de,(0433ch)		;0a31	ed 5b 3c 43 	. [ < C 
	ld bc,l0080h		;0a35	01 80 00 	. . . 
	ldir		;0a38	ed b0 	. . 
	ld de,(0433eh)		;0a3a	ed 5b 3e 43 	. [ > C 
	ld bc,l0080h		;0a3e	01 80 00 	. . . 
	ldir		;0a41	ed b0 	. . 
	ld hl,0ffffh		;0a43	21 ff ff 	! . . 
	ld (04193h),hl		;0a46	22 93 41 	" . A 
	ret			;0a49	c9 	. 
sub_0a4ah:
	push hl			;0a4a	e5 	. 
	push de			;0a4b	d5 	. 
	call sub_0a52h		;0a4c	cd 52 0a 	. R . 
	pop de			;0a4f	d1 	. 
	pop hl			;0a50	e1 	. 
	ret			;0a51	c9 	. 
sub_0a52h:
	ld hl,(04193h)		;0a52	2a 93 41 	* . A 
	or a			;0a55	b7 	. 
	sbc hl,bc		;0a56	ed 42 	. B 
	ret nc			;0a58	d0 	. 
	ld hl,(0418fh)		;0a59	2a 8f 41 	* . A 
	dec hl			;0a5c	2b 	+ 
	or a			;0a5d	b7 	. 
	sbc hl,bc		;0a5e	ed 42 	. B 
	jp nc,l0a7ah		;0a60	d2 7a 0a 	. z . 
	ld hl,(04191h)		;0a63	2a 91 41 	* . A 
	or a			;0a66	b7 	. 
	sbc hl,bc		;0a67	ed 42 	. B 
	jp c,l0a88h		;0a69	da 88 0a 	. . . 
	ld hl,(0418fh)		;0a6c	2a 8f 41 	* . A 
	push hl			;0a6f	e5 	. 
	ld h,b			;0a70	60 	` 
	ld l,c			;0a71	69 	i 
	pop bc			;0a72	c1 	. 
	ld a,(041a1h)		;0a73	3a a1 41 	: . A 
	call sub_0a9ch		;0a76	cd 9c 0a 	. . . 
	ret			;0a79	c9 	. 
l0a7ah:
	ld hl,(04193h)		;0a7a	2a 93 41 	* . A 
	push hl			;0a7d	e5 	. 
	ld h,b			;0a7e	60 	` 
	ld l,c			;0a7f	69 	i 
	pop bc			;0a80	c1 	. 
	ld a,(041a2h)		;0a81	3a a2 41 	: . A 
	call sub_0a9ch		;0a84	cd 9c 0a 	. . . 
	ret			;0a87	c9 	. 
l0a88h:
	ld hl,(04191h)		;0a88	2a 91 41 	* . A 
	ex de,hl			;0a8b	eb 	. 
	ld h,b			;0a8c	60 	` 
	ld l,c			;0a8d	69 	i 
	or a			;0a8e	b7 	. 
	sbc hl,de		;0a8f	ed 52 	. R 
	push hl			;0a91	e5 	. 
	ld hl,(0419dh)		;0a92	2a 9d 41 	* . A 
	ld b,h			;0a95	44 	D 
	ld c,l			;0a96	4d 	M 
	pop hl			;0a97	e1 	. 
	add hl,bc			;0a98	09 	. 
	ld b,h			;0a99	44 	D 
	ld c,l			;0a9a	4d 	M 
	ret			;0a9b	c9 	. 
sub_0a9ch:
	push bc			;0a9c	c5 	. 
	or a			;0a9d	b7 	. 
	sbc hl,bc		;0a9e	ed 42 	. B 
	ex de,hl			;0aa0	eb 	. 
	call sub_10e3h		;0aa1	cd e3 10 	. . . 
	ld b,004h		;0aa4	06 04 	. . 
l0aa6h:
	add hl,hl			;0aa6	29 	) 
	rla			;0aa7	17 	. 
	dec b			;0aa8	05 	. 
	jp nz,l0aa6h		;0aa9	c2 a6 0a 	. . . 
	ld b,a			;0aac	47 	G 
	ld c,h			;0aad	4c 	L 
	pop hl			;0aae	e1 	. 
	add hl,bc			;0aaf	09 	. 
	ld b,h			;0ab0	44 	D 
	ld c,l			;0ab1	4d 	M 
	ret			;0ab2	c9 	. 
sub_0ab3h:
	push bc			;0ab3	c5 	. 
	push de			;0ab4	d5 	. 
	ld c,a			;0ab5	4f 	O 
	ld hl,l299ah		;0ab6	21 9a 29 	! . ) 
	ld de,l0333h		;0ab9	11 33 03 	. 3 . 
	ld b,007h		;0abc	06 07 	. . 
l0abeh:
	ld a,(hl)			;0abe	7e 	~ 
	cp c			;0abf	b9 	. 
	jr z,l0aceh		;0ac0	28 0c 	( . 
	add hl,de			;0ac2	19 	. 
	ld a,03fh		;0ac3	3e 3f 	> ? 
	cp h			;0ac5	bc 	. 
	jr c,l0acah		;0ac6	38 02 	8 . 
	djnz l0abeh		;0ac8	10 f4 	. . 
l0acah:
	ld a,0ffh		;0aca	3e ff 	> . 
	jr l0acfh		;0acc	18 01 	. . 
l0aceh:
	ld a,c			;0ace	79 	y 
l0acfh:
	pop de			;0acf	d1 	. 
	pop bc			;0ad0	c1 	. 
	ret			;0ad1	c9 	. 
sub_0ad2h:
	ld a,(0418ah)		;0ad2	3a 8a 41 	: . A 
	or a			;0ad5	b7 	. 
	jp m,l0b81h		;0ad6	fa 81 0b 	. . . 
	ld a,(0402bh)		;0ad9	3a 2b 40 	: + @ 
	and 040h		;0adc	e6 40 	. @ 
	jp z,l0b81h		;0ade	ca 81 0b 	. . . 
	ld hl,040b0h		;0ae1	21 b0 40 	! . @ 
	ld (040d0h),hl		;0ae4	22 d0 40 	" . @ 
	ld hl,04333h		;0ae7	21 33 43 	! 3 C 
	ld de,0418ch		;0aea	11 8c 41 	. . A 
	dec (hl)			;0aed	35 	5 
	jp nz,l0b7ah		;0aee	c2 7a 0b 	. z . 
	ld (hl),040h		;0af1	36 40 	6 @ 
	push hl			;0af3	e5 	. 
	ld a,(041e4h)		;0af4	3a e4 41 	: . A 
	and 00fh		;0af7	e6 0f 	. . 
	ld h,a			;0af9	67 	g 
	ld a,(0402dh)		;0afa	3a 2d 40 	: - @ 
	and 00fh		;0afd	e6 0f 	. . 
	cp h			;0aff	bc 	. 
	jp c,l0b04h		;0b00	da 04 0b 	. . . 
	ld a,h			;0b03	7c 	| 
l0b04h:
	ld h,a			;0b04	67 	g 
	ld a,(041e4h)		;0b05	3a e4 41 	: . A 
	and 0f0h		;0b08	e6 f0 	. . 
	or h			;0b0a	b4 	. 
	ld (040d3h),a		;0b0b	32 d3 40 	2 . @ 
	ld a,h			;0b0e	7c 	| 
	pop hl			;0b0f	e1 	. 
	or a			;0b10	b7 	. 
	ret z			;0b11	c8 	. 
	push hl			;0b12	e5 	. 
	ld hl,(041e2h)		;0b13	2a e2 41 	* . A 
	ld de,040b0h		;0b16	11 b0 40 	. . @ 
	ld b,a			;0b19	47 	G 
	ld a,(0402dh)		;0b1a	3a 2d 40 	: - @ 
	or a			;0b1d	b7 	. 
	ld a,b			;0b1e	78 	x 
	jp m,l0b50h		;0b1f	fa 50 0b 	. P . 
l0b22h:
	push af			;0b22	f5 	. 
	inc hl			;0b23	23 	# 
	inc hl			;0b24	23 	# 
	inc hl			;0b25	23 	# 
	ld a,(hl)			;0b26	7e 	~ 
	inc hl			;0b27	23 	# 
	inc hl			;0b28	23 	# 
	push hl			;0b29	e5 	. 
	push de			;0b2a	d5 	. 
	or a			;0b2b	b7 	. 
	jp p,l0b30h		;0b2c	f2 30 0b 	. 0 . 
	cpl			;0b2f	2f 	/ 
l0b30h:
	rra			;0b30	1f 	. 
	add a,040h		;0b31	c6 40 	. @ 
	ld e,a			;0b33	5f 	_ 
	ld d,000h		;0b34	16 00 	. . 
	ld a,(0418dh)		;0b36	3a 8d 41 	: . A 
	call sub_10d3h		;0b39	cd d3 10 	. . . 
	add hl,hl			;0b3c	29 	) 
	inc h			;0b3d	24 	$ 
	pop de			;0b3e	d1 	. 
	ld a,h			;0b3f	7c 	| 
	ld (de),a			;0b40	12 	. 
	inc de			;0b41	13 	. 
	ld a,(0418eh)		;0b42	3a 8e 41 	: . A 
	ld (de),a			;0b45	12 	. 
	inc de			;0b46	13 	. 
	pop hl			;0b47	e1 	. 
	pop af			;0b48	f1 	. 
	dec a			;0b49	3d 	= 
	jp nz,l0b22h		;0b4a	c2 22 0b 	. " . 
	jp l0b60h		;0b4d	c3 60 0b 	. ` . 
l0b50h:
	ex de,hl			;0b50	eb 	. 
	ld a,(0418dh)		;0b51	3a 8d 41 	: . A 
	ld c,a			;0b54	4f 	O 
	ld a,(0418eh)		;0b55	3a 8e 41 	: . A 
l0b58h:
	ld (hl),c			;0b58	71 	q 
	inc hl			;0b59	23 	# 
	ld (hl),a			;0b5a	77 	w 
	inc hl			;0b5b	23 	# 
	dec b			;0b5c	05 	. 
	jp nz,l0b58h		;0b5d	c2 58 0b 	. X . 
l0b60h:
	pop hl			;0b60	e1 	. 
	inc hl			;0b61	23 	# 
	ld de,0418ch		;0b62	11 8c 41 	. . A 
	dec (hl)			;0b65	35 	5 
	jp nz,l0b7ah		;0b66	c2 7a 0b 	. z . 
	ld a,(de)			;0b69	1a 	. 
	ld (hl),a			;0b6a	77 	w 
	ld hl,(04335h)		;0b6b	2a 35 43 	* 5 C 
	inc hl			;0b6e	23 	# 
	ld a,h			;0b6f	7c 	| 
	and 007h		;0b70	e6 07 	. . 
	ld h,a			;0b72	67 	g 
	ld (04335h),hl		;0b73	22 35 43 	" 5 C 
	ld a,(hl)			;0b76	7e 	~ 
	ld (04337h),a		;0b77	32 37 43 	2 7 C 
l0b7ah:
	ld hl,04332h		;0b7a	21 32 43 	! 2 C 
	dec (hl)			;0b7d	35 	5 
	jp z,l0b88h		;0b7e	ca 88 0b 	. . . 
l0b81h:
	ld a,030h		;0b81	3e 30 	> 0 
l0b83h:
	dec a			;0b83	3d 	= 
	jp nz,l0b83h		;0b84	c2 83 0b 	. . . 
	ret			;0b87	c9 	. 
l0b88h:
	dec de			;0b88	1b 	. 
	ld a,(de)			;0b89	1a 	. 
	ld (hl),a			;0b8a	77 	w 
	ld a,(040d3h)		;0b8b	3a d3 40 	: . @ 
	ld b,a			;0b8e	47 	G 
	and 00fh		;0b8f	e6 0f 	. . 
	ret z			;0b91	c8 	. 
	ld a,(04337h)		;0b92	3a 37 43 	: 7 C 
	ld (040d2h),a		;0b95	32 d2 40 	2 . @ 
	ld a,b			;0b98	78 	x 
	ld hl,(041e2h)		;0b99	2a e2 41 	* . A 
l0b9ch:
	push af			;0b9c	f5 	. 
	ld e,(hl)			;0b9d	5e 	^ 
	inc hl			;0b9e	23 	# 
	ld d,(hl)			;0b9f	56 	V 
	inc hl			;0ba0	23 	# 
	inc hl			;0ba1	23 	# 
	ld b,(hl)			;0ba2	46 	F 
	inc hl			;0ba3	23 	# 
	ld a,(040d2h)		;0ba4	3a d2 40 	: . @ 
	ld c,a			;0ba7	4f 	O 
	pop af			;0ba8	f1 	. 
	push af			;0ba9	f5 	. 
	or a			;0baa	b7 	. 
	jp p,l0bb9h		;0bab	f2 b9 0b 	. . . 
	rrca			;0bae	0f 	. 
	jp nc,l0bb9h		;0baf	d2 b9 0b 	. . . 
	ld a,c			;0bb2	79 	y 
	xor 001h		;0bb3	ee 01 	. . 
	ld c,a			;0bb5	4f 	O 
	jp l0bc2h		;0bb6	c3 c2 0b 	. . . 
l0bb9h:
	pop af			;0bb9	f1 	. 
	push af			;0bba	f5 	. 
	and 040h		;0bbb	e6 40 	. @ 
	ld a,c			;0bbd	79 	y 
	jp nz,l0bc2h		;0bbe	c2 c2 0b 	. . . 
	rrca			;0bc1	0f 	. 
l0bc2h:
	ld (040d2h),a		;0bc2	32 d2 40 	2 . @ 
l0bc5h:
	xor a			;0bc5	af 	. 
	out (000h),a		;0bc6	d3 00 	. . 
	ld a,(040d2h)		;0bc8	3a d2 40 	: . @ 
	and 001h		;0bcb	e6 01 	. . 
	push hl			;0bcd	e5 	. 
	ld a,(hl)			;0bce	7e 	~ 
	ld hl,(040d0h)		;0bcf	2a d0 40 	* . @ 
	jp z,l0c31h		;0bd2	ca 31 0c 	. 1 . 
	rla			;0bd5	17 	. 
	jp c,l0c1dh		;0bd6	da 1d 0c 	. . . 
	rra			;0bd9	1f 	. 
	or a			;0bda	b7 	. 
	jp z,l0be7h		;0bdb	ca e7 0b 	. . . 
	sub (hl)			;0bde	96 	. 
	jp nc,l0c81h		;0bdf	d2 81 0c 	. . . 
	ld a,000h		;0be2	3e 00 	> . 
	jp l0c81h		;0be4	c3 81 0c 	. . . 
l0be7h:
	ld a,b			;0be7	78 	x 
	add a,002h		;0be8	c6 02 	. . 
	call sub_0bf4h		;0bea	cd f4 0b 	. . . 
	pop hl			;0bed	e1 	. 
	call sub_0c5bh		;0bee	cd 5b 0c 	. [ . 
	jp l0bc5h		;0bf1	c3 c5 0b 	. . . 
sub_0bf4h:
	push af			;0bf4	f5 	. 
	jp c,l0c00h		;0bf5	da 00 0c 	. . . 
	xor b			;0bf8	a8 	. 
	inc hl			;0bf9	23 	# 
	and (hl)			;0bfa	a6 	. 
	jp nz,l0c00h		;0bfb	c2 00 0c 	. . . 
	pop af			;0bfe	f1 	. 
	ret			;0bff	c9 	. 
l0c00h:
	pop af			;0c00	f1 	. 
	pop hl			;0c01	e1 	. 
	pop hl			;0c02	e1 	. 
l0c03h:
	pop af			;0c03	f1 	. 
	push af			;0c04	f5 	. 
	push hl			;0c05	e5 	. 
	ld l,a			;0c06	6f 	o 
	ld a,(040d3h)		;0c07	3a d3 40 	: . @ 
	sub l			;0c0a	95 	. 
	ld l,a			;0c0b	6f 	o 
	ld a,001h		;0c0c	3e 01 	> . 
	inc l			;0c0e	2c 	, 
l0c0fh:
	rlca			;0c0f	07 	. 
	dec l			;0c10	2d 	- 
	jp nz,l0c0fh		;0c11	c2 0f 0c 	. . . 
	ld hl,04337h		;0c14	21 37 43 	! 7 C 
	xor (hl)			;0c17	ae 	. 
	ld (hl),a			;0c18	77 	w 
	pop hl			;0c19	e1 	. 
	jp l0ca8h		;0c1a	c3 a8 0c 	. . . 
l0c1dh:
	rra			;0c1d	1f 	. 
	add a,(hl)			;0c1e	86 	. 
	cp 0a1h		;0c1f	fe a1 	. . 
	jp c,l0c81h		;0c21	da 81 0c 	. . . 
	ld a,b			;0c24	78 	x 
	add a,001h		;0c25	c6 01 	. . 
	call sub_0bf4h		;0c27	cd f4 0b 	. . . 
	pop hl			;0c2a	e1 	. 
	call sub_0c79h		;0c2b	cd 79 0c 	. y . 
	jp l0bc5h		;0c2e	c3 c5 0b 	. . . 
l0c31h:
	rla			;0c31	17 	. 
	jp nc,l0c47h		;0c32	d2 47 0c 	. G . 
	rra			;0c35	1f 	. 
	sub (hl)			;0c36	96 	. 
	jp m,l0c81h		;0c37	fa 81 0c 	. . . 
	ld a,b			;0c3a	78 	x 
	sub 002h		;0c3b	d6 02 	. . 
	call sub_0bf4h		;0c3d	cd f4 0b 	. . . 
	pop hl			;0c40	e1 	. 
	call sub_0c5bh		;0c41	cd 5b 0c 	. [ . 
	jp l0bc5h		;0c44	c3 c5 0b 	. . . 
l0c47h:
	rra			;0c47	1f 	. 
	add a,(hl)			;0c48	86 	. 
	cp 021h		;0c49	fe 21 	. ! 
	jp c,l0c81h		;0c4b	da 81 0c 	. . . 
	ld a,b			;0c4e	78 	x 
	sub 001h		;0c4f	d6 01 	. . 
	call sub_0bf4h		;0c51	cd f4 0b 	. . . 
	pop hl			;0c54	e1 	. 
	call sub_0c79h		;0c55	cd 79 0c 	. y . 
	jp l0bc5h		;0c58	c3 c5 0b 	. . . 
sub_0c5bh:
	dec hl			;0c5b	2b 	+ 
	ld (hl),a			;0c5c	77 	w 
	inc hl			;0c5d	23 	# 
	ld b,a			;0c5e	47 	G 
	push de			;0c5f	d5 	. 
	push hl			;0c60	e5 	. 
	ld hl,0ff7dh		;0c61	21 7d ff 	! } . 
l0c64h:
	add hl,de			;0c64	19 	. 
	cpl			;0c65	2f 	/ 
	ld (hl),a			;0c66	77 	w 
	pop hl			;0c67	e1 	. 
	pop de			;0c68	d1 	. 
	ld a,080h		;0c69	3e 80 	> . 
	xor (hl)			;0c6b	ae 	. 
	ld (hl),a			;0c6c	77 	w 
	ld a,(04187h)		;0c6d	3a 87 41 	: . A 
	out (000h),a		;0c70	d3 00 	. . 
	ld a,00ah		;0c72	3e 0a 	> . 
l0c74h:
	dec a			;0c74	3d 	= 
	jp nz,l0c74h		;0c75	c2 74 0c 	. t . 
	ret			;0c78	c9 	. 
sub_0c79h:
	push de			;0c79	d5 	. 
	push hl			;0c7a	e5 	. 
	ld hl,0ff7ch		;0c7b	21 7c ff 	! | . 
	jp l0c64h		;0c7e	c3 64 0c 	. d . 
l0c81h:
	pop hl			;0c81	e1 	. 
	ld (hl),a			;0c82	77 	w 
	and 03fh		;0c83	e6 3f 	. ? 
	cp 020h		;0c85	fe 20 	.   
	jp z,l0cc2h		;0c87	ca c2 0c 	. . . 
	cp 000h		;0c8a	fe 00 	. . 
	ld b,059h		;0c8c	06 59 	. Y 
	jp z,l0c98h		;0c8e	ca 98 0c 	. . . 
	cp 010h		;0c91	fe 10 	. . 
	jp z,l0c98h		;0c93	ca 98 0c 	. . . 
	set 2,b		;0c96	cb d0 	. . 
l0c98h:
	bit 4,a		;0c98	cb 67 	. g 
	jp z,l0c9eh		;0c9a	ca 9e 0c 	. . . 
	dec b			;0c9d	05 	. 
l0c9eh:
	cpl			;0c9e	2f 	/ 
	res 4,a		;0c9f	cb a7 	. . 
l0ca1h:
	push hl			;0ca1	e5 	. 
	ld h,d			;0ca2	62 	b 
	ld l,e			;0ca3	6b 	k 
	inc hl			;0ca4	23 	# 
	ld (hl),b			;0ca5	70 	p 
	ld (de),a			;0ca6	12 	. 
	pop hl			;0ca7	e1 	. 
l0ca8h:
	push hl			;0ca8	e5 	. 
	ld hl,(040d0h)		;0ca9	2a d0 40 	* . @ 
	inc hl			;0cac	23 	# 
	inc hl			;0cad	23 	# 
	ld (040d0h),hl		;0cae	22 d0 40 	" . @ 
	pop hl			;0cb1	e1 	. 
	ld a,(04187h)		;0cb2	3a 87 41 	: . A 
	out (000h),a		;0cb5	d3 00 	. . 
	pop af			;0cb7	f1 	. 
	inc hl			;0cb8	23 	# 
	dec a			;0cb9	3d 	= 
	ld c,a			;0cba	4f 	O 
	and 00fh		;0cbb	e6 0f 	. . 
	ld a,c			;0cbd	79 	y 
	jp nz,l0b9ch		;0cbe	c2 9c 0b 	. . . 
	ret			;0cc1	c9 	. 
l0cc2h:
	ld b,019h		;0cc2	06 19 	. . 
	ld a,0efh		;0cc4	3e ef 	> . 
	jp l0ca1h		;0cc6	c3 a1 0c 	. . . 
sub_0cc9h:
	ld a,010h		;0cc9	3e 10 	> . 
	ld (0432ah),a		;0ccb	32 2a 43 	2 * C 
l0cceh:
	ex de,hl			;0cce	eb 	. 
	add hl,hl			;0ccf	29 	) 
	ex de,hl			;0cd0	eb 	. 
	add hl,hl			;0cd1	29 	) 
	jp c,l0cf0h		;0cd2	da f0 0c 	. . . 
	ld a,l			;0cd5	7d 	} 
	sub c			;0cd6	91 	. 
	ld (0432bh),a		;0cd7	32 2b 43 	2 + C 
	ld a,h			;0cda	7c 	| 
	sbc a,b			;0cdb	98 	. 
	jp c,l0ce5h		;0cdc	da e5 0c 	. . . 
l0cdfh:
	ld h,a			;0cdf	67 	g 
	ld a,(0432bh)		;0ce0	3a 2b 43 	: + C 
	ld l,a			;0ce3	6f 	o 
	inc e			;0ce4	1c 	. 
l0ce5h:
	ld a,(0432ah)		;0ce5	3a 2a 43 	: * C 
	dec a			;0ce8	3d 	= 
	ld (0432ah),a		;0ce9	32 2a 43 	2 * C 
	jp nz,l0cceh		;0cec	c2 ce 0c 	. . . 
	ret			;0cef	c9 	. 
l0cf0h:
	ld a,l			;0cf0	7d 	} 
	sub c			;0cf1	91 	. 
	ld (0432bh),a		;0cf2	32 2b 43 	2 + C 
	ld a,h			;0cf5	7c 	| 
	sbc a,b			;0cf6	98 	. 
	jp l0cdfh		;0cf7	c3 df 0c 	. . . 
sub_0cfah:
	push de			;0cfa	d5 	. 
	push bc			;0cfb	c5 	. 
	ld l,a			;0cfc	6f 	o 
	ld h,000h		;0cfd	26 00 	& . 
	ld de,l0d3fh		;0cff	11 3f 0d 	. ? . 
	add hl,de			;0d02	19 	. 
	ld e,(hl)			;0d03	5e 	^ 
	ld d,000h		;0d04	16 00 	. . 
	cp 01eh		;0d06	fe 1e 	. . 
	jp c,l0d0eh		;0d08	da 0e 0d 	. . . 
	inc hl			;0d0b	23 	# 
	inc hl			;0d0c	23 	# 
	ld d,(hl)			;0d0d	56 	V 
l0d0eh:
	ex de,hl			;0d0e	eb 	. 
	add hl,hl			;0d0f	29 	) 
	ex de,hl			;0d10	eb 	. 
	push de			;0d11	d5 	. 
	ld a,(04000h)		;0d12	3a 00 40 	: . @ 
	call sub_0ab3h		;0d15	cd b3 0a 	. . . 
	ld de,l0003h+1		;0d18	11 04 00 	. . . 
	add hl,de			;0d1b	19 	. 
	ld e,(hl)			;0d1c	5e 	^ 
	ld d,000h		;0d1d	16 00 	. . 
	ld a,(041a1h)		;0d1f	3a a1 41 	: . A 
	call sub_10d3h		;0d22	cd d3 10 	. . . 
	add hl,hl			;0d25	29 	) 
	add hl,hl			;0d26	29 	) 
	add hl,hl			;0d27	29 	) 
	add hl,hl			;0d28	29 	) 
	ld a,h			;0d29	7c 	| 
	jp nc,l0d2fh		;0d2a	d2 2f 0d 	. / . 
	ld a,0ffh		;0d2d	3e ff 	> . 
l0d2fh:
	pop de			;0d2f	d1 	. 
	call sub_10e3h		;0d30	cd e3 10 	. . . 
	ld b,l			;0d33	45 	E 
	ld l,h			;0d34	6c 	l 
	ld h,a			;0d35	67 	g 
	ld a,b			;0d36	78 	x 
	or a			;0d37	b7 	. 
	jp p,l0d3ch		;0d38	f2 3c 0d 	. < . 
	inc hl			;0d3b	23 	# 
l0d3ch:
	pop bc			;0d3c	c1 	. 
	pop de			;0d3d	d1 	. 
	ret			;0d3e	c9 	. 
l0d3fh:
	ld b,006h		;0d3f	06 06 	. . 
	ex af,af'			;0d41	08 	. 
	add hl,bc			;0d42	09 	. 
	dec bc			;0d43	0b 	. 
	inc c			;0d44	0c 	. 
	dec c			;0d45	0d 	. 
	ld c,00fh		;0d46	0e 0f 	. . 
	ld de,l1412h		;0d48	11 12 14 	. . . 
	ld d,018h		;0d4b	16 18 	. . 
	ld a,(de)			;0d4d	1a 	. 
	inc e			;0d4e	1c 	. 
	ld e,022h		;0d4f	1e 22 	. " 
	ld h,02ah		;0d51	26 2a 	& * 
	ld l,034h		;0d53	2e 34 	. 4 
	add hl,sp			;0d55	39 	9 
	ld b,c			;0d56	41 	A 
	ld c,e			;0d57	4b 	K 
	ld d,l			;0d58	55 	U 
	ld h,h			;0d59	64 	d 
	ld a,b			;0d5a	78 	x 
	and b			;0d5b	a0 	. 
	call c,0bc5eh		;0d5c	dc 5e bc 	. ^ . 
	ld bc,07a02h		;0d5f	01 02 7a 	. . z 
	or a			;0d62	b7 	. 
	rra			;0d63	1f 	. 
	ld d,a			;0d64	57 	W 
	ld a,e			;0d65	7b 	{ 
	rra			;0d66	1f 	. 
	ld e,a			;0d67	5f 	_ 
	ret			;0d68	c9 	. 
	ld a,000h		;0d69	3e 00 	> . 
l0d6bh:
	ex (sp),hl			;0d6b	e3 	. 
	ex (sp),hl			;0d6c	e3 	. 
	push hl			;0d6d	e5 	. 
	pop hl			;0d6e	e1 	. 
	dec a			;0d6f	3d 	= 
	jp nz,l0d6bh		;0d70	c2 6b 0d 	. k . 
	ret			;0d73	c9 	. 
	ld l,a			;0d74	6f 	o 
	ld h,000h		;0d75	26 00 	& . 
	sub 032h		;0d77	d6 32 	. 2 
	ret c			;0d79	d8 	. 
	ld l,a			;0d7a	6f 	o 
	sub 032h		;0d7b	d6 32 	. 2 
	jp nc,l0d88h		;0d7d	d2 88 0d 	. . . 
	push de			;0d80	d5 	. 
	add hl,hl			;0d81	29 	) 
	ld de,l0032h		;0d82	11 32 00 	. 2 . 
	add hl,de			;0d85	19 	. 
	pop de			;0d86	d1 	. 
	ret			;0d87	c9 	. 
l0d88h:
	ld l,a			;0d88	6f 	o 
	sub 032h		;0d89	d6 32 	. 2 
	jp nc,l0d97h		;0d8b	d2 97 0d 	. . . 
	push de			;0d8e	d5 	. 
	add hl,hl			;0d8f	29 	) 
	add hl,hl			;0d90	29 	) 
	ld de,00096h		;0d91	11 96 00 	. . . 
	add hl,de			;0d94	19 	. 
	pop de			;0d95	d1 	. 
	ret			;0d96	c9 	. 
l0d97h:
	ld l,a			;0d97	6f 	o 
	push de			;0d98	d5 	. 
	add hl,hl			;0d99	29 	) 
	add hl,hl			;0d9a	29 	) 
	add hl,hl			;0d9b	29 	) 
	ld de,0015eh		;0d9c	11 5e 01 	. ^ . 
	add hl,de			;0d9f	19 	. 
	pop de			;0da0	d1 	. 
	ret			;0da1	c9 	. 
	nop			;0da2	00 	. 
	jp z,l11f8h		;0da3	ca f8 11 	. . . 
	push bc			;0da6	c5 	. 
	ex de,hl			;0da7	eb 	. 
	call sub_0f5ch		;0da8	cd 5c 0f 	. \ . 
	ld b,a			;0dab	47 	G 
	inc hl			;0dac	23 	# 
	ld a,(hl)			;0dad	7e 	~ 
	push hl			;0dae	e5 	. 
	call sub_0f5ch		;0daf	cd 5c 0f 	. \ . 
	ld c,a			;0db2	4f 	O 
	ld a,b			;0db3	78 	x 
	sub c			;0db4	91 	. 
	call sub_0febh		;0db5	cd eb 0f 	. . . 
	ld a,(041eah)		;0db8	3a ea 41 	: . A 
	and 00fh		;0dbb	e6 0f 	. . 
	jp z,l0e26h		;0dbd	ca 26 0e 	. & . 
	ld hl,(041e8h)		;0dc0	2a e8 41 	* . A 
	inc hl			;0dc3	23 	# 
	inc hl			;0dc4	23 	# 
	ld a,(hl)			;0dc5	7e 	~ 
	or a			;0dc6	b7 	. 
	jp z,l0e26h		;0dc7	ca 26 0e 	. & . 
	push bc			;0dca	c5 	. 
	ld a,(041edh)		;0dcb	3a ed 41 	: . A 
	and 00fh		;0dce	e6 0f 	. . 
	ld l,a			;0dd0	6f 	o 
	ld h,000h		;0dd1	26 00 	& . 
	ld a,(041eah)		;0dd3	3a ea 41 	: . A 
	and 00fh		;0dd6	e6 0f 	. . 
	ld b,a			;0dd8	47 	G 
	ld c,h			;0dd9	4c 	L 
	call sub_0cc9h		;0dda	cd c9 0c 	. . . 
	pop bc			;0ddd	c1 	. 
	ld a,d			;0dde	7a 	z 
	cp 002h		;0ddf	fe 02 	. . 
	jp c,l0e26h		;0de1	da 26 0e 	. & . 
	push bc			;0de4	c5 	. 
	ld a,c			;0de5	79 	y 
	or a			;0de6	b7 	. 
	rla			;0de7	17 	. 
	rla			;0de8	17 	. 
	rla			;0de9	17 	. 
	dec d			;0dea	15 	. 
	dec d			;0deb	15 	. 
	jp z,l0e03h		;0dec	ca 03 0e 	. . . 
	ld e,a			;0def	5f 	_ 
	ld c,d			;0df0	4a 	J 
	ld d,000h		;0df1	16 00 	. . 
	call sub_10d3h		;0df3	cd d3 10 	. . . 
	ld a,h			;0df6	7c 	| 
	dec c			;0df7	0d 	. 
	jp z,l0e03h		;0df8	ca 03 0e 	. . . 
l0dfbh:
	call sub_10d3h		;0dfb	cd d3 10 	. . . 
	ld a,h			;0dfe	7c 	| 
	dec c			;0dff	0d 	. 
	jp nz,l0dfbh		;0e00	c2 fb 0d 	. . . 
l0e03h:
	pop bc			;0e03	c1 	. 
	push bc			;0e04	c5 	. 
	cp 040h		;0e05	fe 40 	. @ 
	jp nc,l0e0ch		;0e07	d2 0c 0e 	. . . 
	ld a,040h		;0e0a	3e 40 	> @ 
l0e0ch:
	ld c,a			;0e0c	4f 	O 
	ld a,b			;0e0d	78 	x 
	and 03fh		;0e0e	e6 3f 	. ? 
	ld b,000h		;0e10	06 00 	. . 
	ld h,b			;0e12	60 	` 
	ld l,a			;0e13	6f 	o 
	call sub_0cc9h		;0e14	cd c9 0c 	. . . 
	pop bc			;0e17	c1 	. 
	ld a,b			;0e18	78 	x 
	and 080h		;0e19	e6 80 	. . 
	ld b,a			;0e1b	47 	G 
	ld a,d			;0e1c	7a 	z 
	cp 020h		;0e1d	fe 20 	.   
	jp c,l0e24h		;0e1f	da 24 0e 	. $ . 
	ld a,01fh		;0e22	3e 1f 	> . 
l0e24h:
	or b			;0e24	b0 	. 
	ld b,a			;0e25	47 	G 
l0e26h:
	ld a,b			;0e26	78 	x 
	ld (0432bh),a		;0e27	32 2b 43 	2 + C 
	pop hl			;0e2a	e1 	. 
	pop bc			;0e2b	c1 	. 
	push hl			;0e2c	e5 	. 
	call sub_11e6h		;0e2d	cd e6 11 	. . . 
	pop de			;0e30	d1 	. 
	jp nz,l0e3dh		;0e31	c2 3d 0e 	. = . 
	push hl			;0e34	e5 	. 
	ld hl,0ffd0h		;0e35	21 d0 ff 	! . . 
	add hl,de			;0e38	19 	. 
	ld (hl),0ffh		;0e39	36 ff 	6 . 
	pop hl			;0e3b	e1 	. 
	ret			;0e3c	c9 	. 
l0e3dh:
	push bc			;0e3d	c5 	. 
	ld c,a			;0e3e	4f 	O 
	ld a,(0432bh)		;0e3f	3a 2b 43 	: + C 
	ld b,a			;0e42	47 	G 
l0e43h:
	ld e,(hl)			;0e43	5e 	^ 
	inc hl			;0e44	23 	# 
	ld d,(hl)			;0e45	56 	V 
	inc hl			;0e46	23 	# 
	inc hl			;0e47	23 	# 
	call sub_0e59h		;0e48	cd 59 0e 	. Y . 
	dec c			;0e4b	0d 	. 
	jp nz,l0e43h		;0e4c	c2 43 0e 	. C . 
	pop bc			;0e4f	c1 	. 
	ret			;0e50	c9 	. 
sub_0e51h:
	push hl			;0e51	e5 	. 
	ld hl,(042eeh)		;0e52	2a ee 42 	* . B 
	add hl,de			;0e55	19 	. 
	ld a,(hl)			;0e56	7e 	~ 
	pop hl			;0e57	e1 	. 
	ret			;0e58	c9 	. 
sub_0e59h:
	push bc			;0e59	c5 	. 
	xor a			;0e5a	af 	. 
	out (000h),a		;0e5b	d3 00 	. . 
	call sub_0e51h		;0e5d	cd 51 0e 	. Q . 
	bit 4,a		;0e60	cb 67 	. g 
	jp z,l0e84h		;0e62	ca 84 0e 	. . . 
	and 0f0h		;0e65	e6 f0 	. . 
	ld c,a			;0e67	4f 	O 
	ld a,b			;0e68	78 	x 
	rra			;0e69	1f 	. 
	rra			;0e6a	1f 	. 
	cpl			;0e6b	2f 	/ 
	and 007h		;0e6c	e6 07 	. . 
	or c			;0e6e	b1 	. 
	bit 7,b		;0e6f	cb 78 	. x 
	jp nz,l0e76h		;0e71	c2 76 0e 	. v . 
	set 3,a		;0e74	cb df 	. . 
l0e76h:
	ld (de),a			;0e76	12 	. 
	push hl			;0e77	e5 	. 
	ld hl,0be00h		;0e78	21 00 be 	! . . 
	add hl,de			;0e7b	19 	. 
	ld (hl),a			;0e7c	77 	w 
	pop hl			;0e7d	e1 	. 
	ld a,b			;0e7e	78 	x 
	and 01fh		;0e7f	e6 1f 	. . 
	jp l0ebch		;0e81	c3 bc 0e 	. . . 
l0e84h:
	push hl			;0e84	e5 	. 
	and 0f0h		;0e85	e6 f0 	. . 
	ld c,a			;0e87	4f 	O 
	ld a,b			;0e88	78 	x 
	cpl			;0e89	2f 	/ 
	and 00fh		;0e8a	e6 0f 	. . 
	or c			;0e8c	b1 	. 
	ld h,a			;0e8d	67 	g 
	inc de			;0e8e	13 	. 
	call sub_0e51h		;0e8f	cd 51 0e 	. Q . 
	and 0f2h		;0e92	e6 f2 	. . 
	ld c,a			;0e94	4f 	O 
	ld a,b			;0e95	78 	x 
	and 00fh		;0e96	e6 0f 	. . 
	jp z,l0e9dh		;0e98	ca 9d 0e 	. . . 
	set 2,c		;0e9b	cb d1 	. . 
l0e9dh:
	bit 4,b		;0e9d	cb 60 	. ` 
	jp nz,l0ea4h		;0e9f	c2 a4 0e 	. . . 
	set 0,c		;0ea2	cb c1 	. . 
l0ea4h:
	bit 7,b		;0ea4	cb 78 	. x 
	jp nz,l0eabh		;0ea6	c2 ab 0e 	. . . 
	set 3,c		;0ea9	cb d9 	. . 
l0eabh:
	ld a,h			;0eab	7c 	| 
	ld h,d			;0eac	62 	b 
	ld l,e			;0ead	6b 	k 
	dec de			;0eae	1b 	. 
	ld (de),a			;0eaf	12 	. 
	ld (hl),c			;0eb0	71 	q 
	ld hl,0be00h		;0eb1	21 00 be 	! . . 
	add hl,de			;0eb4	19 	. 
	ld (hl),a			;0eb5	77 	w 
	inc hl			;0eb6	23 	# 
	ld (hl),c			;0eb7	71 	q 
	pop hl			;0eb8	e1 	. 
	ld a,b			;0eb9	78 	x 
	set 7,a		;0eba	cb ff 	. . 
l0ebch:
	push af			;0ebc	f5 	. 
	ld a,(04187h)		;0ebd	3a 87 41 	: . A 
	out (000h),a		;0ec0	d3 00 	. . 
	ld b,008h		;0ec2	06 08 	. . 
l0ec4h:
	djnz l0ec4h		;0ec4	10 fe 	. . 
	xor a			;0ec6	af 	. 
	out (000h),a		;0ec7	d3 00 	. . 
	pop af			;0ec9	f1 	. 
	pop bc			;0eca	c1 	. 
	ret			;0ecb	c9 	. 
sub_0ecch:
	push bc			;0ecc	c5 	. 
	xor a			;0ecd	af 	. 
	out (000h),a		;0ece	d3 00 	. . 
	call sub_0e51h		;0ed0	cd 51 0e 	. Q . 
	bit 4,a		;0ed3	cb 67 	. g 
	jp z,l0ef6h		;0ed5	ca f6 0e 	. . . 
	and 0f8h		;0ed8	e6 f8 	. . 
	ld c,a			;0eda	4f 	O 
	ld a,b			;0edb	78 	x 
	cp 020h		;0edc	fe 20 	.   
	jp nz,l0ee2h		;0ede	c2 e2 0e 	. . . 
	dec a			;0ee1	3d 	= 
l0ee2h:
	rra			;0ee2	1f 	. 
	rra			;0ee3	1f 	. 
	cpl			;0ee4	2f 	/ 
	and 007h		;0ee5	e6 07 	. . 
	or c			;0ee7	b1 	. 
	ld (de),a			;0ee8	12 	. 
	push hl			;0ee9	e5 	. 
	ld hl,0be00h		;0eea	21 00 be 	! . . 
	add hl,de			;0eed	19 	. 
	ld (hl),a			;0eee	77 	w 
	pop hl			;0eef	e1 	. 
	ld a,b			;0ef0	78 	x 
	and 03fh		;0ef1	e6 3f 	. ? 
	jp l0f2ch		;0ef3	c3 2c 0f 	. , . 
l0ef6h:
	push hl			;0ef6	e5 	. 
	and 0f0h		;0ef7	e6 f0 	. . 
	ld c,a			;0ef9	4f 	O 
	ld a,b			;0efa	78 	x 
	cp 020h		;0efb	fe 20 	.   
	jp z,l0f3ch		;0efd	ca 3c 0f 	. < . 
	cpl			;0f00	2f 	/ 
	and 00fh		;0f01	e6 0f 	. . 
	or c			;0f03	b1 	. 
	ld h,a			;0f04	67 	g 
l0f05h:
	inc de			;0f05	13 	. 
	call sub_0e51h		;0f06	cd 51 0e 	. Q . 
	and 0fah		;0f09	e6 fa 	. . 
	ld c,a			;0f0b	4f 	O 
	ld a,b			;0f0c	78 	x 
	and 00fh		;0f0d	e6 0f 	. . 
	jp z,l0f14h		;0f0f	ca 14 0f 	. . . 
	set 2,c		;0f12	cb d1 	. . 
l0f14h:
	bit 4,b		;0f14	cb 60 	. ` 
	jp nz,l0f1bh		;0f16	c2 1b 0f 	. . . 
	set 0,c		;0f19	cb c1 	. . 
l0f1bh:
	ld a,h			;0f1b	7c 	| 
	ld h,d			;0f1c	62 	b 
	ld l,e			;0f1d	6b 	k 
	dec de			;0f1e	1b 	. 
	ld (de),a			;0f1f	12 	. 
	ld (hl),c			;0f20	71 	q 
	ld hl,0be00h		;0f21	21 00 be 	! . . 
	add hl,de			;0f24	19 	. 
	ld (hl),a			;0f25	77 	w 
	inc hl			;0f26	23 	# 
	ld (hl),c			;0f27	71 	q 
	pop hl			;0f28	e1 	. 
	ld a,b			;0f29	78 	x 
	set 7,a		;0f2a	cb ff 	. . 
l0f2ch:
	push af			;0f2c	f5 	. 
	ld a,(04187h)		;0f2d	3a 87 41 	: . A 
	out (000h),a		;0f30	d3 00 	. . 
	ld b,008h		;0f32	06 08 	. . 
l0f34h:
	djnz l0f34h		;0f34	10 fe 	. . 
	xor a			;0f36	af 	. 
	out (000h),a		;0f37	d3 00 	. . 
	pop af			;0f39	f1 	. 
	pop bc			;0f3a	c1 	. 
l0f3bh:
	ret			;0f3b	c9 	. 
l0f3ch:
	ld a,c			;0f3c	79 	y 
	or 00fh		;0f3d	f6 0f 	. . 
	ld h,a			;0f3f	67 	g 
	inc de			;0f40	13 	. 
	and 020h		;0f41	e6 20 	.   
	jp nz,l0f51h		;0f43	c2 51 0f 	. Q . 
	call sub_0e51h		;0f46	cd 51 0e 	. Q . 
	and 0d9h		;0f49	e6 d9 	. . 
	or 001h		;0f4b	f6 01 	. . 
	ld c,a			;0f4d	4f 	O 
	jp l0f1bh		;0f4e	c3 1b 0f 	. . . 
l0f51h:
	call sub_0e51h		;0f51	cd 51 0e 	. Q . 
	and 0f9h		;0f54	e6 f9 	. . 
	or 001h		;0f56	f6 01 	. . 
	ld c,a			;0f58	4f 	O 
	jp l0f1bh		;0f59	c3 1b 0f 	. . . 
sub_0f5ch:
	and 0f8h		;0f5c	e6 f8 	. . 
	rrca			;0f5e	0f 	. 
	rrca			;0f5f	0f 	. 
	rrca			;0f60	0f 	. 
	ret			;0f61	c9 	. 
	jp z,l11f8h		;0f62	ca f8 11 	. . . 
	call sub_0f5ch		;0f65	cd 5c 0f 	. \ . 
	jp l0f97h		;0f68	c3 97 0f 	. . . 
	jp z,l11f8h		;0f6b	ca f8 11 	. . . 
	cp 0fdh		;0f6e	fe fd 	. . 
	jp c,l0f7dh		;0f70	da 7d 0f 	. } . 
	ld a,041h		;0f73	3e 41 	> A 
	ld (042f0h),a		;0f75	32 f0 42 	2 . B 
	ld a,020h		;0f78	3e 20 	>   
	jp l0f97h		;0f7a	c3 97 0f 	. . . 
l0f7dh:
	push af			;0f7d	f5 	. 
	ld a,(042f0h)		;0f7e	3a f0 42 	: . B 
	and 040h		;0f81	e6 40 	. @ 
	jp z,l0f93h		;0f83	ca 93 0f 	. . . 
	ld a,(04188h)		;0f86	3a 88 41 	: . A 
	cp 020h		;0f89	fe 20 	.   
	jp nz,l0f93h		;0f8b	c2 93 0f 	. . . 
	ld a,081h		;0f8e	3e 81 	> . 
	ld (042f0h),a		;0f90	32 f0 42 	2 . B 
l0f93h:
	pop af			;0f93	f1 	. 
	call sub_0f5ch		;0f94	cd 5c 0f 	. \ . 
l0f97h:
	ld (04188h),a		;0f97	32 88 41 	2 . A 
	call sub_11e6h		;0f9a	cd e6 11 	. . . 
	ret z			;0f9d	c8 	. 
	push bc			;0f9e	c5 	. 
	ld c,a			;0f9f	4f 	O 
	ld a,(04188h)		;0fa0	3a 88 41 	: . A 
	ld b,a			;0fa3	47 	G 
l0fa4h:
	push bc			;0fa4	c5 	. 
	ld e,(hl)			;0fa5	5e 	^ 
	inc hl			;0fa6	23 	# 
	ld d,(hl)			;0fa7	56 	V 
	inc hl			;0fa8	23 	# 
	ld a,(hl)			;0fa9	7e 	~ 
	or a			;0faa	b7 	. 
	jp z,l0fe0h		;0fab	ca e0 0f 	. . . 
	dec a			;0fae	3d 	= 
	and 00fh		;0faf	e6 0f 	. . 
	call sub_107bh		;0fb1	cd 7b 10 	. { . 
	ld b,a			;0fb4	47 	G 
	ld a,(hl)			;0fb5	7e 	~ 
	and 040h		;0fb6	e6 40 	. @ 
	jp z,l0fe0h		;0fb8	ca e0 0f 	. . . 
	inc hl			;0fbb	23 	# 
	call sub_0ecch		;0fbc	cd cc 0e 	. . . 
	ld e,(hl)			;0fbf	5e 	^ 
	inc hl			;0fc0	23 	# 
	ld d,(hl)			;0fc1	56 	V 
	inc hl			;0fc2	23 	# 
	ld a,b			;0fc3	78 	x 
	pop bc			;0fc4	c1 	. 
	push bc			;0fc5	c5 	. 
	ld c,a			;0fc6	4f 	O 
	push bc			;0fc7	c5 	. 
	ld a,(042eah)		;0fc8	3a ea 42 	: . B 
	call sub_0f5ch		;0fcb	cd 5c 0f 	. \ . 
	ld b,a			;0fce	47 	G 
	ld a,(hl)			;0fcf	7e 	~ 
	dec a			;0fd0	3d 	= 
	call sub_107bh		;0fd1	cd 7b 10 	. { . 
	pop bc			;0fd4	c1 	. 
	sub c			;0fd5	91 	. 
	call sub_0febh		;0fd6	cd eb 0f 	. . . 
	call sub_0e59h		;0fd9	cd 59 0e 	. Y . 
	inc hl			;0fdc	23 	# 
	jp l0fe4h		;0fdd	c3 e4 0f 	. . . 
l0fe0h:
	inc hl			;0fe0	23 	# 
	call sub_0ecch		;0fe1	cd cc 0e 	. . . 
l0fe4h:
	pop bc			;0fe4	c1 	. 
	dec c			;0fe5	0d 	. 
	jp nz,l0fa4h		;0fe6	c2 a4 0f 	. . . 
	pop bc			;0fe9	c1 	. 
	ret			;0fea	c9 	. 
sub_0febh:
	or a			;0feb	b7 	. 
	jp p,l0ff3h		;0fec	f2 f3 0f 	. . . 
	cpl			;0fef	2f 	/ 
	inc a			;0ff0	3c 	< 
	or 080h		;0ff1	f6 80 	. . 
l0ff3h:
	ld b,a			;0ff3	47 	G 
	ret			;0ff4	c9 	. 
sub_0ff5h:
	ld a,(041e7h)		;0ff5	3a e7 41 	: . A 
	and 00fh		;0ff8	e6 0f 	. . 
	ret z			;0ffa	c8 	. 
	ld c,a			;0ffb	4f 	O 
	ld a,(0432ch)		;0ffc	3a 2c 43 	: , C 
	ld hl,(041e5h)		;0fff	2a e5 41 	* . A 
sub_1002h:
	add a,a			;1002	87 	. 
	ld b,a			;1003	47 	G 
	ld a,080h		;1004	3e 80 	> . 
	ld (04323h),a		;1006	32 23 43 	2 # C 
l1009h:
	push bc			;1009	c5 	. 
	ld e,(hl)			;100a	5e 	^ 
	inc hl			;100b	23 	# 
	ld d,(hl)			;100c	56 	V 
	inc hl			;100d	23 	# 
	ld a,(04323h)		;100e	3a 23 43 	: # C 
	cp (hl)			;1011	be 	. 
	jp z,l1049h		;1012	ca 49 10 	. I . 
	ld a,(hl)			;1015	7e 	~ 
	ld (04323h),a		;1016	32 23 43 	2 # C 
	push hl			;1019	e5 	. 
	push de			;101a	d5 	. 
	ld e,b			;101b	58 	X 
	ld d,000h		;101c	16 00 	. . 
	and 0e0h		;101e	e6 e0 	. . 
	call sub_10d3h		;1020	cd d3 10 	. . . 
	ld b,h			;1023	44 	D 
	pop de			;1024	d1 	. 
	pop hl			;1025	e1 	. 
	ld a,(042f3h)		;1026	3a f3 42 	: . B 
	or a			;1029	b7 	. 
	jp z,l1030h		;102a	ca 30 10 	. 0 . 
	ld a,b			;102d	78 	x 
	rra			;102e	1f 	. 
	ld b,a			;102f	47 	G 
l1030h:
	ld a,(hl)			;1030	7e 	~ 
	and 01fh		;1031	e6 1f 	. . 
	cp b			;1033	b8 	. 
	jp c,l1038h		;1034	da 38 10 	. 8 . 
	ld a,b			;1037	78 	x 
l1038h:
	push af			;1038	f5 	. 
	ld a,(04300h)		;1039	3a 00 43 	: . C 
	ld b,a			;103c	47 	G 
	pop af			;103d	f1 	. 
	sub b			;103e	90 	. 
	cp 000h		;103f	fe 00 	. . 
	jp p,l1046h		;1041	f2 46 10 	. F . 
	ld a,000h		;1044	3e 00 	> . 
l1046h:
	ld (04324h),a		;1046	32 24 43 	2 $ C 
l1049h:
	ld a,(04324h)		;1049	3a 24 43 	: $ C 
	ld b,a			;104c	47 	G 
	inc hl			;104d	23 	# 
	call sub_0ecch		;104e	cd cc 0e 	. . . 
	inc de			;1051	13 	. 
	inc de			;1052	13 	. 
	call sub_0ecch		;1053	cd cc 0e 	. . . 
	pop bc			;1056	c1 	. 
	ld a,(042e7h)		;1057	3a e7 42 	: . B 
	and 040h		;105a	e6 40 	. @ 
	jp nz,l1076h		;105c	c2 76 10 	. v . 
	ld a,(042f3h)		;105f	3a f3 42 	: . B 
	or a			;1062	b7 	. 
	jp nz,l1076h		;1063	c2 76 10 	. v . 
	ld a,003h		;1066	3e 03 	> . 
	cp c			;1068	b9 	. 
	jp c,l1076h		;1069	da 76 10 	. v . 
	ld a,(0432dh)		;106c	3a 2d 43 	: - C 
	add a,a			;106f	87 	. 
	ld b,a			;1070	47 	G 
	ld a,080h		;1071	3e 80 	> . 
	ld (04323h),a		;1073	32 23 43 	2 # C 
l1076h:
	dec c			;1076	0d 	. 
	jp nz,l1009h		;1077	c2 09 10 	. . . 
	ret			;107a	c9 	. 
sub_107bh:
	push hl			;107b	e5 	. 
	push de			;107c	d5 	. 
	and 00fh		;107d	e6 0f 	. . 
	ld e,a			;107f	5f 	_ 
	add a,a			;1080	87 	. 
	add a,a			;1081	87 	. 
	add a,e			;1082	83 	. 
	ld e,a			;1083	5f 	_ 
	ld d,000h		;1084	16 00 	. . 
	ld h,d			;1086	62 	b 
	ld l,b			;1087	68 	h 
	ld b,d			;1088	42 	B 
	add hl,hl			;1089	29 	) 
	add hl,hl			;108a	29 	) 
	add hl,hl			;108b	29 	) 
	add hl,hl			;108c	29 	) 
	add hl,hl			;108d	29 	) 
	push hl			;108e	e5 	. 
	ld c,h			;108f	4c 	L 
	ld hl,l10a6h		;1090	21 a6 10 	! . . 
	add hl,de			;1093	19 	. 
	add hl,bc			;1094	09 	. 
	pop de			;1095	d1 	. 
	call sub_1266h		;1096	cd 66 12 	. f . 
	and 0feh		;1099	e6 fe 	. . 
	rra			;109b	1f 	. 
	cp 01fh		;109c	fe 1f 	. . 
	jp c,l10a3h		;109e	da a3 10 	. . . 
	ld a,01fh		;10a1	3e 1f 	> . 
l10a3h:
	pop de			;10a3	d1 	. 
	pop hl			;10a4	e1 	. 
	ret			;10a5	c9 	. 
l10a6h:
	ld h,030h		;10a6	26 30 	& 0 
	ld a,(0413eh)		;10a8	3a 3e 41 	: > A 
	ld e,031h		;10ab	1e 31 	. 1 
	add hl,sp			;10ad	39 	9 
	dec a			;10ae	3d 	= 
	ld b,c			;10af	41 	A 
	inc e			;10b0	1c 	. 
	dec l			;10b1	2d 	- 
	scf			;10b2	37 	7 
	inc a			;10b3	3c 	< 
	ld b,c			;10b4	41 	A 
	ld d,029h		;10b5	16 29 	. ) 
	inc (hl)			;10b7	34 	4 
	dec sp			;10b8	3b 	; 
	ld b,b			;10b9	40 	@ 
	dec l			;10ba	2d 	- 
	jr c,$+62		;10bb	38 3c 	8 < 
	ld a,042h		;10bd	3e 42 	> B 
	jr $+45		;10bf	18 2b 	. + 
	dec (hl)			;10c1	35 	5 
	dec sp			;10c2	3b 	; 
	ccf			;10c3	3f 	? 
	dec d			;10c4	15 	. 
	add hl,hl			;10c5	29 	) 
	inc sp			;10c6	33 	3 
	ld a,(0123fh)		;10c7	3a 3f 12 	: ? . 
	daa			;10ca	27 	' 
	ld (l3f3ah),a		;10cb	32 3a 3f 	2 : ? 
	inc c			;10ce	0c 	. 
	ld hl,l382eh		;10cf	21 2e 38 	! . 8 
	ccf			;10d2	3f 	? 
sub_10d3h:
	ld hl,l0000h		;10d3	21 00 00 	! . . 
	ld b,008h		;10d6	06 08 	. . 
l10d8h:
	add hl,hl			;10d8	29 	) 
	rla			;10d9	17 	. 
	jp nc,l10deh		;10da	d2 de 10 	. . . 
	add hl,de			;10dd	19 	. 
l10deh:
	dec b			;10de	05 	. 
	jp nz,l10d8h		;10df	c2 d8 10 	. . . 
	ret			;10e2	c9 	. 
sub_10e3h:
	ld hl,l0000h		;10e3	21 00 00 	! . . 
	ld b,008h		;10e6	06 08 	. . 
l10e8h:
	add hl,hl			;10e8	29 	) 
	rla			;10e9	17 	. 
	jp nc,l10eeh		;10ea	d2 ee 10 	. . . 
	add hl,de			;10ed	19 	. 
l10eeh:
	jp nc,l10f2h		;10ee	d2 f2 10 	. . . 
	inc a			;10f1	3c 	< 
l10f2h:
	dec b			;10f2	05 	. 
	jp nz,l10e8h		;10f3	c2 e8 10 	. . . 
	ret			;10f6	c9 	. 
	jp z,l11f1h		;10f7	ca f1 11 	. . . 
	cp 0ffh		;10fa	fe ff 	. . 
	jp z,l1157h		;10fc	ca 57 11 	. W . 
	cp 0fdh		;10ff	fe fd 	. . 
	jp c,l1109h		;1101	da 09 11 	. . . 
	ld a,020h		;1104	3e 20 	>   
	jp l110ch		;1106	c3 0c 11 	. . . 
l1109h:
	call sub_0f5ch		;1109	cd 5c 0f 	. \ . 
l110ch:
	ld (0432bh),a		;110c	32 2b 43 	2 + C 
	call sub_11e6h		;110f	cd e6 11 	. . . 
	push af			;1112	f5 	. 
	push hl			;1113	e5 	. 
	ld e,(hl)			;1114	5e 	^ 
	inc hl			;1115	23 	# 
	ld d,(hl)			;1116	56 	V 
	call sub_0e51h		;1117	cd 51 0e 	. Q . 
	and 010h		;111a	e6 10 	. . 
	jp z,l112dh		;111c	ca 2d 11 	. - . 
	ld a,(hl)			;111f	7e 	~ 
	and 003h		;1120	e6 03 	. . 
	jp nz,l112dh		;1122	c2 2d 11 	. - . 
	ld a,(0432bh)		;1125	3a 2b 43 	: + C 
	and 0fch		;1128	e6 fc 	. . 
	ld (0432bh),a		;112a	32 2b 43 	2 + C 
l112dh:
	pop hl			;112d	e1 	. 
	pop af			;112e	f1 	. 
	jp z,l113ch		;112f	ca 3c 11 	. < . 
	push bc			;1132	c5 	. 
	ld c,a			;1133	4f 	O 
	ld a,(0432bh)		;1134	3a 2b 43 	: + C 
	ld b,a			;1137	47 	G 
	call sub_11d8h		;1138	cd d8 11 	. . . 
	pop bc			;113b	c1 	. 
l113ch:
	push bc			;113c	c5 	. 
	ld a,(0432bh)		;113d	3a 2b 43 	: + C 
	ld b,a			;1140	47 	G 
	ld a,020h		;1141	3e 20 	>   
	sub b			;1143	90 	. 
	ld (0432bh),a		;1144	32 2b 43 	2 + C 
	pop bc			;1147	c1 	. 
	call sub_11e6h		;1148	cd e6 11 	. . . 
	ret z			;114b	c8 	. 
	push bc			;114c	c5 	. 
	ld c,a			;114d	4f 	O 
	ld a,(0432bh)		;114e	3a 2b 43 	: + C 
	ld b,a			;1151	47 	G 
	call sub_11d8h		;1152	cd d8 11 	. . . 
	pop bc			;1155	c1 	. 
	ret			;1156	c9 	. 
l1157h:
	call sub_11e6h		;1157	cd e6 11 	. . . 
	jp z,l117bh		;115a	ca 7b 11 	. { . 
	push bc			;115d	c5 	. 
l115eh:
	push hl			;115e	e5 	. 
	push af			;115f	f5 	. 
	ld c,a			;1160	4f 	O 
	push hl			;1161	e5 	. 
	inc hl			;1162	23 	# 
	inc hl			;1163	23 	# 
	ld a,(hl)			;1164	7e 	~ 
	pop hl			;1165	e1 	. 
	and 03fh		;1166	e6 3f 	. ? 
	jp z,l1178h		;1168	ca 78 11 	. x . 
	dec a			;116b	3d 	= 
	ld b,a			;116c	47 	G 
	call sub_11d8h		;116d	cd d8 11 	. . . 
	call sub_14dch		;1170	cd dc 14 	. . . 
	pop af			;1173	f1 	. 
	pop hl			;1174	e1 	. 
	jp l115eh		;1175	c3 5e 11 	. ^ . 
l1178h:
	pop af			;1178	f1 	. 
	pop hl			;1179	e1 	. 
	pop bc			;117a	c1 	. 
l117bh:
	call sub_11e6h		;117b	cd e6 11 	. . . 
	ret z			;117e	c8 	. 
	push bc			;117f	c5 	. 
l1180h:
	push hl			;1180	e5 	. 
	push af			;1181	f5 	. 
	ld c,a			;1182	4f 	O 
	push hl			;1183	e5 	. 
	inc hl			;1184	23 	# 
	inc hl			;1185	23 	# 
	ld a,(hl)			;1186	7e 	~ 
	pop hl			;1187	e1 	. 
	and 03fh		;1188	e6 3f 	. ? 
	jp z,l119ah		;118a	ca 9a 11 	. . . 
	dec a			;118d	3d 	= 
	ld b,a			;118e	47 	G 
	call sub_11d8h		;118f	cd d8 11 	. . . 
	call sub_14dch		;1192	cd dc 14 	. . . 
	pop af			;1195	f1 	. 
	pop hl			;1196	e1 	. 
	jp l1180h		;1197	c3 80 11 	. . . 
l119ah:
	pop af			;119a	f1 	. 
	pop hl			;119b	e1 	. 
	pop bc			;119c	c1 	. 
	ret			;119d	c9 	. 
l119eh:
	jp z,l11f1h		;119e	ca f1 11 	. . . 
	call sub_0f5ch		;11a1	cd 5c 0f 	. \ . 
	ld (0432bh),a		;11a4	32 2b 43 	2 + C 
	call sub_11e6h		;11a7	cd e6 11 	. . . 
	jp z,l11b7h		;11aa	ca b7 11 	. . . 
	push bc			;11ad	c5 	. 
	ld c,a			;11ae	4f 	O 
	ld a,(0432bh)		;11af	3a 2b 43 	: + C 
	ld b,a			;11b2	47 	G 
	call sub_11d8h		;11b3	cd d8 11 	. . . 
	pop bc			;11b6	c1 	. 
l11b7h:
	push bc			;11b7	c5 	. 
	ld a,(0432bh)		;11b8	3a 2b 43 	: + C 
	ld b,a			;11bb	47 	G 
	or a			;11bc	b7 	. 
	ld a,01fh		;11bd	3e 1f 	> . 
	jp z,l11c5h		;11bf	ca c5 11 	. . . 
	ld a,020h		;11c2	3e 20 	>   
	sub b			;11c4	90 	. 
l11c5h:
	ld (0432bh),a		;11c5	32 2b 43 	2 + C 
	pop bc			;11c8	c1 	. 
	call sub_11e6h		;11c9	cd e6 11 	. . . 
	ret z			;11cc	c8 	. 
	push bc			;11cd	c5 	. 
	ld c,a			;11ce	4f 	O 
	ld a,(0432bh)		;11cf	3a 2b 43 	: + C 
	ld b,a			;11d2	47 	G 
	call sub_11d8h		;11d3	cd d8 11 	. . . 
	pop bc			;11d6	c1 	. 
	ret			;11d7	c9 	. 
sub_11d8h:
	ld e,(hl)			;11d8	5e 	^ 
	inc hl			;11d9	23 	# 
	ld d,(hl)			;11da	56 	V 
	inc hl			;11db	23 	# 
	call sub_0ecch		;11dc	cd cc 0e 	. . . 
	ld (hl),a			;11df	77 	w 
	inc hl			;11e0	23 	# 
	dec c			;11e1	0d 	. 
	jp nz,sub_11d8h		;11e2	c2 d8 11 	. . . 
	ret			;11e5	c9 	. 
sub_11e6h:
	ld a,(bc)			;11e6	0a 	. 
	inc bc			;11e7	03 	. 
	ld l,a			;11e8	6f 	o 
	ld a,(bc)			;11e9	0a 	. 
	inc bc			;11ea	03 	. 
	ld h,a			;11eb	67 	g 
	ld a,(bc)			;11ec	0a 	. 
	inc bc			;11ed	03 	. 
	and 00fh		;11ee	e6 0f 	. . 
	ret			;11f0	c9 	. 
l11f1h:
	ld hl,l0006h		;11f1	21 06 00 	! . . 
	add hl,bc			;11f4	09 	. 
	ld c,l			;11f5	4d 	M 
	ld b,h			;11f6	44 	D 
	ret			;11f7	c9 	. 
l11f8h:
	inc bc			;11f8	03 	. 
	inc bc			;11f9	03 	. 
	inc bc			;11fa	03 	. 
	ret			;11fb	c9 	. 
l11fch:
	ld hl,l000ch		;11fc	21 0c 00 	! . . 
	add hl,bc			;11ff	09 	. 
	ld c,l			;1200	4d 	M 
	ld b,h			;1201	44 	D 
	ret			;1202	c9 	. 
	jp z,l11fch		;1203	ca fc 11 	. . . 
	push bc			;1206	c5 	. 
	ld l,a			;1207	6f 	o 
	ld h,000h		;1208	26 00 	& . 
	ld e,l			;120a	5d 	] 
	ld d,h			;120b	54 	T 
	add hl,hl			;120c	29 	) 
	add hl,de			;120d	19 	. 
	push hl			;120e	e5 	. 
	call sub_11e6h		;120f	cd e6 11 	. . . 
	dec bc			;1212	0b 	. 
	ld a,(bc)			;1213	0a 	. 
	pop de			;1214	d1 	. 
	ld hl,l12a4h		;1215	21 a4 12 	! . . 
	rla			;1218	17 	. 
	jp c,l1226h		;1219	da 26 12 	. & . 
	ld hl,l12b4h		;121c	21 b4 12 	! . . 
	rla			;121f	17 	. 
	jp c,l1226h		;1220	da 26 12 	. & . 
	ld hl,l1294h		;1223	21 94 12 	! . . 
l1226h:
	ld b,000h		;1226	06 00 	. . 
	ld c,d			;1228	4a 	J 
	add hl,bc			;1229	09 	. 
	ld bc,041cfh		;122a	01 cf 41 	. . A 
	ld d,004h		;122d	16 04 	. . 
l122fh:
	push de			;122f	d5 	. 
	call sub_1266h		;1230	cd 66 12 	. f . 
	pop de			;1233	d1 	. 
	inc hl			;1234	23 	# 
	inc hl			;1235	23 	# 
	inc hl			;1236	23 	# 
	inc hl			;1237	23 	# 
	ld (bc),a			;1238	02 	. 
	inc bc			;1239	03 	. 
	dec d			;123a	15 	. 
	jp nz,l122fh		;123b	c2 2f 12 	. / . 
	ld hl,041cfh		;123e	21 cf 41 	! . A 
	ld a,005h		;1241	3e 05 	> . 
	ld (041aeh),a		;1243	32 ae 41 	2 . A 
	pop bc			;1246	c1 	. 
l1247h:
	ld a,(041aeh)		;1247	3a ae 41 	: . A 
	dec a			;124a	3d 	= 
	ld (041aeh),a		;124b	32 ae 41 	2 . A 
	ret z			;124e	c8 	. 
	ld a,(hl)			;124f	7e 	~ 
	ld (0432bh),a		;1250	32 2b 43 	2 + C 
	inc hl			;1253	23 	# 
	push hl			;1254	e5 	. 
	call sub_11e6h		;1255	cd e6 11 	. . . 
	push bc			;1258	c5 	. 
	ld c,a			;1259	4f 	O 
	ld a,(0432bh)		;125a	3a 2b 43 	: + C 
	ld b,a			;125d	47 	G 
	call nz,sub_11d8h		;125e	c4 d8 11 	. . . 
	pop bc			;1261	c1 	. 
	pop hl			;1262	e1 	. 
	jp l1247h		;1263	c3 47 12 	. G . 
sub_1266h:
	push bc			;1266	c5 	. 
	ld c,(hl)			;1267	4e 	N 
	push hl			;1268	e5 	. 
	inc hl			;1269	23 	# 
	ld a,(hl)			;126a	7e 	~ 
	sub c			;126b	91 	. 
	push af			;126c	f5 	. 
	jp nc,l1272h		;126d	d2 72 12 	. r . 
	cpl			;1270	2f 	/ 
	inc a			;1271	3c 	< 
l1272h:
	ld d,000h		;1272	16 00 	. . 
	call sub_10d3h		;1274	cd d3 10 	. . . 
	pop af			;1277	f1 	. 
	jp nc,l1282h		;1278	d2 82 12 	. . . 
	ld a,l			;127b	7d 	} 
	cpl			;127c	2f 	/ 
	ld l,a			;127d	6f 	o 
	ld a,h			;127e	7c 	| 
	cpl			;127f	2f 	/ 
	ld h,a			;1280	67 	g 
	inc hl			;1281	23 	# 
l1282h:
	ex de,hl			;1282	eb 	. 
	pop hl			;1283	e1 	. 
	ld b,(hl)			;1284	46 	F 
	ld c,000h		;1285	0e 00 	. . 
	ex de,hl			;1287	eb 	. 
	add hl,bc			;1288	09 	. 
	ex de,hl			;1289	eb 	. 
	ld a,07fh		;128a	3e 7f 	>  
	cp e			;128c	bb 	. 
	ld a,d			;128d	7a 	z 
	jp nc,l1292h		;128e	d2 92 12 	. . . 
	inc a			;1291	3c 	< 
l1292h:
	pop bc			;1292	c1 	. 
	ret			;1293	c9 	. 
l1294h:
	rra			;1294	1f 	. 
	dec e			;1295	1d 	. 
	ld (de),a			;1296	12 	. 
	nop			;1297	00 	. 
	ld a,(bc)			;1298	0a 	. 
	rrca			;1299	0f 	. 
	inc d			;129a	14 	. 
	nop			;129b	00 	. 
	ld (bc),a			;129c	02 	. 
	ld a,(bc)			;129d	0a 	. 
	inc c			;129e	0c 	. 
	nop			;129f	00 	. 
	ld bc,l0f05h		;12a0	01 05 0f 	. . . 
	rra			;12a3	1f 	. 
l12a4h:
	rra			;12a4	1f 	. 
	inc e			;12a5	1c 	. 
	inc d			;12a6	14 	. 
	nop			;12a7	00 	. 
	rrca			;12a8	0f 	. 
	inc d			;12a9	14 	. 
l12aah:
	add hl,de			;12aa	19 	. 
	ld (bc),a			;12ab	02 	. 
	dec b			;12ac	05 	. 
	ld a,(bc)			;12ad	0a 	. 
	ld de,0001eh		;12ae	11 1e 00 	. . . 
	inc d			;12b1	14 	. 
	inc e			;12b2	1c 	. 
	rra			;12b3	1f 	. 
l12b4h:
	rra			;12b4	1f 	. 
	inc e			;12b5	1c 	. 
	djnz l12c0h		;12b6	10 08 	. . 
	djnz l12cah		;12b8	10 10 	. . 
	djnz $+12		;12ba	10 0a 	. . 
	djnz $+18		;12bc	10 10 	. . 
	djnz $+18		;12be	10 10 	. . 
l12c0h:
	ex af,af'			;12c0	08 	. 
	djnz $+30		;12c1	10 1c 	. . 
	rra			;12c3	1f 	. 
	jp z,l11f8h		;12c4	ca f8 11 	. . . 
	cpl			;12c7	2f 	/ 
	and 0fch		;12c8	e6 fc 	. . 
l12cah:
	rra			;12ca	1f 	. 
	rra			;12cb	1f 	. 
	ld (0432bh),a		;12cc	32 2b 43 	2 + C 
	and 03eh		;12cf	e6 3e 	. > 
	rra			;12d1	1f 	. 
	inc a			;12d2	3c 	< 
	ld (042f4h),a		;12d3	32 f4 42 	2 . B 
	push bc			;12d6	c5 	. 
	ld hl,04047h		;12d7	21 47 40 	! G @ 
	call sub_042fh		;12da	cd 2f 04 	. / . 
	ld (0432dh),a		;12dd	32 2d 43 	2 - C 
	ld hl,04041h		;12e0	21 41 40 	! A @ 
	call sub_042fh		;12e3	cd 2f 04 	. / . 
	ld (0432ch),a		;12e6	32 2c 43 	2 , C 
	call sub_0ff5h		;12e9	cd f5 0f 	. . . 
	pop bc			;12ec	c1 	. 
	jp l1377h		;12ed	c3 77 13 	. w . 
	jp z,l11f8h		;12f0	ca f8 11 	. . . 
	push af			;12f3	f5 	. 
	ld a,(04187h)		;12f4	3a 87 41 	: . A 
	res 0,a		;12f7	cb 87 	. . 
	cp 006h		;12f9	fe 06 	. . 
	jr z,l1303h		;12fb	28 06 	( . 
	cp 002h		;12fd	fe 02 	. . 
	jr z,l1330h		;12ff	28 2f 	( / 
	jr l136fh		;1301	18 6c 	. l 
l1303h:
	pop af			;1303	f1 	. 
	cp 000h		;1304	fe 00 	. . 
	jp nz,l1319h		;1306	c2 19 13 	. . . 
	push af			;1309	f5 	. 
	ld a,0fbh		;130a	3e fb 	> . 
	ld (08187h),a		;130c	32 87 81 	2 . . 
	ld a,0feh		;130f	3e fe 	> . 
	ld (08287h),a		;1311	32 87 82 	2 . . 
	ld (04340h),a		;1314	32 40 43 	2 @ C 
	jr l136fh		;1317	18 56 	. V 
l1319h:
	push af			;1319	f5 	. 
	ld a,(04340h)		;131a	3a 40 43 	: @ C 
	or a			;131d	b7 	. 
	jr z,l136fh		;131e	28 4f 	( O 
	ld a,0ffh		;1320	3e ff 	> . 
	ld (08187h),a		;1322	32 87 81 	2 . . 
	ld a,0feh		;1325	3e fe 	> . 
	ld (08287h),a		;1327	32 87 82 	2 . . 
	xor a			;132a	af 	. 
	ld (04340h),a		;132b	32 40 43 	2 @ C 
	jr l136fh		;132e	18 3f 	. ? 
l1330h:
	pop af			;1330	f1 	. 
	cp 000h		;1331	fe 00 	. . 
	jp nz,l1350h		;1333	c2 50 13 	. P . 
	push af			;1336	f5 	. 
	ld a,0ffh		;1337	3e ff 	> . 
	ld (08181h),a		;1339	32 81 81 	2 . . 
	ld a,0feh		;133c	3e fe 	> . 
	ld (08281h),a		;133e	32 81 82 	2 . . 
	ld a,0ffh		;1341	3e ff 	> . 
	ld (081d4h),a		;1343	32 d4 81 	2 . . 
	ld a,0ffh		;1346	3e ff 	> . 
	ld (082d4h),a		;1348	32 d4 82 	2 . . 
	ld (04340h),a		;134b	32 40 43 	2 @ C 
	jr l136fh		;134e	18 1f 	. . 
l1350h:
	push af			;1350	f5 	. 
	ld a,(04340h)		;1351	3a 40 43 	: @ C 
	or a			;1354	b7 	. 
	jr z,l136fh		;1355	28 18 	( . 
	ld a,0fdh		;1357	3e fd 	> . 
	ld (08181h),a		;1359	32 81 81 	2 . . 
	ld a,00ch		;135c	3e 0c 	> . 
	ld (08281h),a		;135e	32 81 82 	2 . . 
	ld a,0fah		;1361	3e fa 	> . 
	ld (081d4h),a		;1363	32 d4 81 	2 . . 
	ld a,09ch		;1366	3e 9c 	> . 
	ld (082d4h),a		;1368	32 d4 82 	2 . . 
	xor a			;136b	af 	. 
	ld (04340h),a		;136c	32 40 43 	2 @ C 
l136fh:
	pop af			;136f	f1 	. 
	and 0fch		;1370	e6 fc 	. . 
	rra			;1372	1f 	. 
	rra			;1373	1f 	. 
	ld (0432bh),a		;1374	32 2b 43 	2 + C 
l1377h:
	call sub_11e6h		;1377	cd e6 11 	. . . 
	ret z			;137a	c8 	. 
	push bc			;137b	c5 	. 
	ld c,a			;137c	4f 	O 
	ld a,(0432bh)		;137d	3a 2b 43 	: + C 
	ld b,a			;1380	47 	G 
	ld a,(0432dh)		;1381	3a 2d 43 	: - C 
	push af			;1384	f5 	. 
	ld a,(04300h)		;1385	3a 00 43 	: . C 
	push af			;1388	f5 	. 
	xor a			;1389	af 	. 
	ld (04300h),a		;138a	32 00 43 	2 . C 
	ld a,001h		;138d	3e 01 	> . 
	ld (042f3h),a		;138f	32 f3 42 	2 . B 
	ld a,b			;1392	78 	x 
	ld (0432dh),a		;1393	32 2d 43 	2 - C 
	call sub_1002h		;1396	cd 02 10 	. . . 
	xor a			;1399	af 	. 
	ld (042f3h),a		;139a	32 f3 42 	2 . B 
	pop af			;139d	f1 	. 
	ld (04300h),a		;139e	32 00 43 	2 . C 
	pop af			;13a1	f1 	. 
	ld (0432dh),a		;13a2	32 2d 43 	2 - C 
	pop bc			;13a5	c1 	. 
	ret			;13a6	c9 	. 
	jp z,l11f8h		;13a7	ca f8 11 	. . . 
	call sub_11e6h		;13aa	cd e6 11 	. . . 
	ret z			;13ad	c8 	. 
	push bc			;13ae	c5 	. 
	call sub_1564h		;13af	cd 64 15 	. d . 
	ld h,b			;13b2	60 	` 
	ld l,c			;13b3	69 	i 
	ld (0432eh),hl		;13b4	22 2e 43 	" . C 
	ex de,hl			;13b7	eb 	. 
	ld hl,(04330h)		;13b8	2a 30 43 	* 0 C 
	or a			;13bb	b7 	. 
	sbc hl,de		;13bc	ed 52 	. R 
	pop bc			;13be	c1 	. 
	ret z			;13bf	c8 	. 
	ld a,(042f0h)		;13c0	3a f0 42 	: . B 
	and 040h		;13c3	e6 40 	. @ 
	or 001h		;13c5	f6 01 	. . 
	ld (042f0h),a		;13c7	32 f0 42 	2 . B 
	ret			;13ca	c9 	. 
sub_13cbh:
	push de			;13cb	d5 	. 
	push bc			;13cc	c5 	. 
	ex de,hl			;13cd	eb 	. 
	add hl,bc			;13ce	09 	. 
	ex de,hl			;13cf	eb 	. 
	ld a,e			;13d0	7b 	{ 
	cpl			;13d1	2f 	/ 
	ld e,a			;13d2	5f 	_ 
	ld a,d			;13d3	7a 	z 
	cpl			;13d4	2f 	/ 
	ld d,a			;13d5	57 	W 
	push de			;13d6	d5 	. 
	push hl			;13d7	e5 	. 
	ld de,0be00h		;13d8	11 00 be 	. . . 
	add hl,de			;13db	19 	. 
	ld e,(hl)			;13dc	5e 	^ 
	inc hl			;13dd	23 	# 
	ld d,(hl)			;13de	56 	V 
	pop hl			;13df	e1 	. 
	bit 4,e		;13e0	cb 63 	. c 
	ld a,e			;13e2	7b 	{ 
	cpl			;13e3	2f 	/ 
	jr z,l13f1h		;13e4	28 0b 	( . 
	and 007h		;13e6	e6 07 	. . 
	ld c,a			;13e8	4f 	O 
	jr z,l1456h		;13e9	28 6b 	( k 
	ld b,a			;13eb	47 	G 
	call sub_144bh		;13ec	cd 4b 14 	. K . 
	jr l1456h		;13ef	18 65 	. e 
l13f1h:
	and 00fh		;13f1	e6 0f 	. . 
	ld c,a			;13f3	4f 	O 
	set 7,c		;13f4	cb f9 	. . 
	jr z,l1402h		;13f6	28 0a 	( . 
	ld b,a			;13f8	47 	G 
	call sub_144bh		;13f9	cd 4b 14 	. K . 
	bit 0,d		;13fc	cb 42 	. B 
	jr nz,l1456h		;13fe	20 56 	  V 
	jr l1406h		;1400	18 04 	. . 
l1402h:
	bit 0,d		;1402	cb 42 	. B 
	jr nz,l141ch		;1404	20 16 	  . 
l1406h:
	ld a,c			;1406	79 	y 
	add a,010h		;1407	c6 10 	. . 
	ld c,a			;1409	4f 	O 
	inc d			;140a	14 	. 
	inc hl			;140b	23 	# 
	ld (hl),d			;140c	72 	r 
	dec hl			;140d	2b 	+ 
	ld a,e			;140e	7b 	{ 
	and 0f0h		;140f	e6 f0 	. . 
	ld e,a			;1411	5f 	_ 
l1412h:
	call sub_14cah		;1412	cd ca 14 	. . . 
	ld b,00fh		;1415	06 0f 	. . 
	call sub_144bh		;1417	cd 4b 14 	. K . 
	jr l1456h		;141a	18 3a 	. : 
l141ch:
	bit 1,d		;141c	cb 4a 	. J 
	jr nz,l1454h		;141e	20 34 	  4 
	ld a,d			;1420	7a 	z 
	xor e			;1421	ab 	. 
	bit 5,a		;1422	cb 6f 	. o 
	jr nz,l1454h		;1424	20 2e 	  . 
	ld (04180h),de		;1426	ed 53 80 41 	. S . A 
	bit 5,d		;142a	cb 6a 	. j 
	jr nz,l1432h		;142c	20 04 	  . 
	and 0c0h		;142e	e6 c0 	. . 
	jr nz,l1454h		;1430	20 22 	  " 
l1432h:
	ld a,e			;1432	7b 	{ 
	and 0f0h		;1433	e6 f0 	. . 
	ld e,a			;1435	5f 	_ 
	ld a,d			;1436	7a 	z 
	or 036h		;1437	f6 36 	. 6 
	and 0feh		;1439	e6 fe 	. . 
	ld d,a			;143b	57 	W 
	inc hl			;143c	23 	# 
	ld (hl),d			;143d	72 	r 
	dec hl			;143e	2b 	+ 
	call sub_14cah		;143f	cd ca 14 	. . . 
	ld c,090h		;1442	0e 90 	. . 
	ld b,00fh		;1444	06 0f 	. . 
	call sub_144bh		;1446	cd 4b 14 	. K . 
	jr l1406h		;1449	18 bb 	. . 
sub_144bh:
	push bc			;144b	c5 	. 
	inc e			;144c	1c 	. 
	call sub_14cah		;144d	cd ca 14 	. . . 
	pop bc			;1450	c1 	. 
	djnz sub_144bh		;1451	10 f8 	. . 
	ret			;1453	c9 	. 
l1454h:
	ld c,000h		;1454	0e 00 	. . 
l1456h:
	ld (04182h),de		;1456	ed 53 82 41 	. S . A 
	pop de			;145a	d1 	. 
	push bc			;145b	c5 	. 
	push hl			;145c	e5 	. 
	ld bc,0ff80h		;145d	01 80 ff 	. . . 
	add hl,bc			;1460	09 	. 
	push hl			;1461	e5 	. 
	add hl,bc			;1462	09 	. 
	add hl,bc			;1463	09 	. 
	pop bc			;1464	c1 	. 
	ld a,e			;1465	7b 	{ 
	ld (hl),d			;1466	72 	r 
	ld (bc),a			;1467	02 	. 
	pop hl			;1468	e1 	. 
	pop bc			;1469	c1 	. 
	ld de,(04182h)		;146a	ed 5b 82 41 	. [ . A 
	ld a,c			;146e	79 	y 
	cp 000h		;146f	fe 00 	. . 
	jr z,l14c7h		;1471	28 54 	( T 
	bit 7,a		;1473	cb 7f 	.  
	jr nz,l147dh		;1475	20 06 	  . 
	ld b,c			;1477	41 	A 
	call sub_14beh		;1478	cd be 14 	. . . 
	jr l14c7h		;147b	18 4a 	. J 
l147dh:
	inc hl			;147d	23 	# 
	ld (hl),d			;147e	72 	r 
	dec hl			;147f	2b 	+ 
	and 07fh		;1480	e6 7f 	.  
	ld c,a			;1482	4f 	O 
	sub 010h		;1483	d6 10 	. . 
	jr nc,l148dh		;1485	30 06 	0 . 
	ld b,c			;1487	41 	A 
	call sub_14beh		;1488	cd be 14 	. . . 
	jr l14c7h		;148b	18 3a 	. : 
l148dh:
	ld c,a			;148d	4f 	O 
	ld b,00fh		;148e	06 0f 	. . 
	call sub_14beh		;1490	cd be 14 	. . . 
	res 0,d		;1493	cb 82 	. . 
	inc hl			;1495	23 	# 
	ld (hl),d			;1496	72 	r 
	dec hl			;1497	2b 	+ 
	ld a,e			;1498	7b 	{ 
	or 00fh		;1499	f6 0f 	. . 
	ld e,a			;149b	5f 	_ 
	call sub_14cah		;149c	cd ca 14 	. . . 
	ld a,c			;149f	79 	y 
	or a			;14a0	b7 	. 
	jr z,l14c7h		;14a1	28 24 	( $ 
	sub 010h		;14a3	d6 10 	. . 
	jr z,l14adh		;14a5	28 06 	( . 
	ld b,c			;14a7	41 	A 
	call sub_14beh		;14a8	cd be 14 	. . . 
	jr l14c7h		;14ab	18 1a 	. . 
l14adh:
	ld b,00fh		;14ad	06 0f 	. . 
	call sub_14beh		;14af	cd be 14 	. . . 
	ld de,(04180h)		;14b2	ed 5b 80 41 	. [ . A 
	ld (hl),e			;14b6	73 	s 
	inc hl			;14b7	23 	# 
	ld (hl),d			;14b8	72 	r 
	call sub_14cbh		;14b9	cd cb 14 	. . . 
	jr l14c7h		;14bc	18 09 	. . 
sub_14beh:
	push bc			;14be	c5 	. 
	dec e			;14bf	1d 	. 
	call sub_14cah		;14c0	cd ca 14 	. . . 
	pop bc			;14c3	c1 	. 
	djnz sub_14beh		;14c4	10 f8 	. . 
	ret			;14c6	c9 	. 
l14c7h:
	pop bc			;14c7	c1 	. 
	pop de			;14c8	d1 	. 
	ret			;14c9	c9 	. 
sub_14cah:
	ld (hl),e			;14ca	73 	s 
sub_14cbh:
	ld a,(04187h)		;14cb	3a 87 41 	: . A 
	out (000h),a		;14ce	d3 00 	. . 
	call sub_14d7h		;14d0	cd d7 14 	. . . 
	xor a			;14d3	af 	. 
	out (000h),a		;14d4	d3 00 	. . 
	ret			;14d6	c9 	. 
sub_14d7h:
	ld b,004h		;14d7	06 04 	. . 
l14d9h:
	djnz l14d9h		;14d9	10 fe 	. . 
	ret			;14db	c9 	. 
sub_14dch:
	push bc			;14dc	c5 	. 
	ld b,005h		;14dd	06 05 	. . 
l14dfh:
	dec b			;14df	05 	. 
	jp nz,l14dfh		;14e0	c2 df 14 	. . . 
	pop bc			;14e3	c1 	. 
	ret			;14e4	c9 	. 
	and 00fh		;14e5	e6 0f 	. . 
sub_14e7h:
	ret z			;14e7	c8 	. 
	ld c,a			;14e8	4f 	O 
	jp sub_11d8h		;14e9	c3 d8 11 	. . . 
	and 0fch		;14ec	e6 fc 	. . 
	rrca			;14ee	0f 	. 
	rrca			;14ef	0f 	. 
	ret			;14f0	c9 	. 
	jp z,l11f8h		;14f1	ca f8 11 	. . . 
	cp 0fdh		;14f4	fe fd 	. . 
	jr c,l14fch		;14f6	38 04 	8 . 
	ld a,020h		;14f8	3e 20 	>   
	jr l14ffh		;14fa	18 03 	. . 
l14fch:
	call sub_0f5ch		;14fc	cd 5c 0f 	. \ . 
l14ffh:
	ld (0432bh),a		;14ff	32 2b 43 	2 + C 
	call sub_11e6h		;1502	cd e6 11 	. . . 
	push bc			;1505	c5 	. 
	ld c,a			;1506	4f 	O 
	ld a,(0432bh)		;1507	3a 2b 43 	: + C 
	ld b,a			;150a	47 	G 
	call nz,sub_11d8h		;150b	c4 d8 11 	. . . 
	pop bc			;150e	c1 	. 
	ret			;150f	c9 	. 
	jp nz,l151dh		;1510	c2 1d 15 	. . . 
	ld hl,l0006h		;1513	21 06 00 	! . . 
	add hl,de			;1516	19 	. 
	call sub_0452h		;1517	cd 52 04 	. R . 
	jp z,l11f8h		;151a	ca f8 11 	. . . 
l151dh:
	call sub_11e6h		;151d	cd e6 11 	. . . 
	ret z			;1520	c8 	. 
	push bc			;1521	c5 	. 
	push hl			;1522	e5 	. 
	push af			;1523	f5 	. 
	ld a,(de)			;1524	1a 	. 
	ld hl,l0006h		;1525	21 06 00 	! . . 
	add hl,de			;1528	19 	. 
	ld c,(hl)			;1529	4e 	N 
	ld b,a			;152a	47 	G 
	ld a,(04341h)		;152b	3a 41 43 	: A C 
	or a			;152e	b7 	. 
	jr z,l153fh		;152f	28 0e 	( . 
	ld hl,(041a3h)		;1531	2a a3 41 	* . A 
	or a			;1534	b7 	. 
	sbc hl,bc		;1535	ed 42 	. B 
	jr nc,l154dh		;1537	30 14 	0 . 
	ld bc,(041a3h)		;1539	ed 4b a3 41 	. K . A 
	jr l154dh		;153d	18 0e 	. . 
l153fh:
	ld hl,(042ech)		;153f	2a ec 42 	* . B 
	add hl,de			;1542	19 	. 
	ld de,03ed1h		;1543	11 d1 3e 	. . > 
	add hl,de			;1546	19 	. 
	ld a,(hl)			;1547	7e 	~ 
	cp b			;1548	b8 	. 
	jr nc,l154dh		;1549	30 02 	0 . 
	ld b,a			;154b	47 	G 
	ld c,b			;154c	48 	H 
l154dh:
	pop af			;154d	f1 	. 
	pop hl			;154e	e1 	. 
	call l092dh		;154f	cd 2d 09 	. - . 
	pop bc			;1552	c1 	. 
	ret			;1553	c9 	. 
	jp z,l11f8h		;1554	ca f8 11 	. . . 
	call sub_11e6h		;1557	cd e6 11 	. . . 
	ret z			;155a	c8 	. 
	push bc			;155b	c5 	. 
	call sub_1564h		;155c	cd 64 15 	. d . 
	call l092dh		;155f	cd 2d 09 	. - . 
	pop bc			;1562	c1 	. 
	ret			;1563	c9 	. 
sub_1564h:
	push hl			;1564	e5 	. 
	push af			;1565	f5 	. 
	ld a,(de)			;1566	1a 	. 
	ld hl,l0006h		;1567	21 06 00 	! . . 
	add hl,de			;156a	19 	. 
	ld e,000h		;156b	1e 00 	. . 
	ld d,a			;156d	57 	W 
	ld a,044h		;156e	3e 44 	> D 
	call sub_10e3h		;1570	cd e3 10 	. . . 
	ld de,l0080h		;1573	11 80 00 	. . . 
	add hl,de			;1576	19 	. 
	jp nc,l157bh		;1577	d2 7b 15 	. { . 
	inc a			;157a	3c 	< 
l157bh:
	ld b,a			;157b	47 	G 
	ld c,h			;157c	4c 	L 
	ld hl,(041a3h)		;157d	2a a3 41 	* . A 
	or a			;1580	b7 	. 
	sbc hl,bc		;1581	ed 42 	. B 
	jr nc,l1589h		;1583	30 04 	0 . 
	ld bc,(041a3h)		;1585	ed 4b a3 41 	. K . A 
l1589h:
	pop af			;1589	f1 	. 
	pop hl			;158a	e1 	. 
	ret			;158b	c9 	. 
	jp z,l11f8h		;158c	ca f8 11 	. . . 
	call sub_11e6h		;158f	cd e6 11 	. . . 
	ret z			;1592	c8 	. 
	push bc			;1593	c5 	. 
	call sub_159ch		;1594	cd 9c 15 	. . . 
	call l092dh		;1597	cd 2d 09 	. - . 
	pop bc			;159a	c1 	. 
	ret			;159b	c9 	. 
sub_159ch:
	push hl			;159c	e5 	. 
	push af			;159d	f5 	. 
	ld a,(de)			;159e	1a 	. 
	ld hl,(042ech)		;159f	2a ec 42 	* . B 
	add hl,de			;15a2	19 	. 
	ld de,03ed1h		;15a3	11 d1 3e 	. . > 
	add hl,de			;15a6	19 	. 
	ld b,(hl)			;15a7	46 	F 
l15a8h:
	cp b			;15a8	b8 	. 
	jr c,l15ach		;15a9	38 01 	8 . 
	ld a,b			;15ab	78 	x 
l15ach:
	rra			;15ac	1f 	. 
	ld b,a			;15ad	47 	G 
	jr c,l15b4h		;15ae	38 04 	8 . 
	ld c,000h		;15b0	0e 00 	. . 
	jr l15b6h		;15b2	18 02 	. . 
l15b4h:
	ld c,080h		;15b4	0e 80 	. . 
l15b6h:
	pop af			;15b6	f1 	. 
	pop hl			;15b7	e1 	. 
	ret			;15b8	c9 	. 
	jp z,l11f8h		;15b9	ca f8 11 	. . . 
	and 0fch		;15bc	e6 fc 	. . 
	rra			;15be	1f 	. 
	rra			;15bf	1f 	. 
	or a			;15c0	b7 	. 
	jp nz,l15c5h		;15c1	c2 c5 15 	. . . 
	inc a			;15c4	3c 	< 
l15c5h:
	sub 020h		;15c5	d6 20 	.   
	ld (0432bh),a		;15c7	32 2b 43 	2 + C 
	call sub_11e6h		;15ca	cd e6 11 	. . . 
	ret z			;15cd	c8 	. 
	push bc			;15ce	c5 	. 
	ld c,a			;15cf	4f 	O 
	ld a,(0432bh)		;15d0	3a 2b 43 	: + C 
	call sub_0febh		;15d3	cd eb 0f 	. . . 
l15d6h:
	ld e,(hl)			;15d6	5e 	^ 
	inc hl			;15d7	23 	# 
	ld d,(hl)			;15d8	56 	V 
	inc hl			;15d9	23 	# 
	call sub_0e59h		;15da	cd 59 0e 	. Y . 
	dec c			;15dd	0d 	. 
	jp nz,l15d6h		;15de	c2 d6 15 	. . . 
	pop bc			;15e1	c1 	. 
	ret			;15e2	c9 	. 
sub_15e3h:
	ld a,(042f0h)		;15e3	3a f0 42 	: . B 
	and 040h		;15e6	e6 40 	. @ 
	ret nz			;15e8	c0 	. 
	push bc			;15e9	c5 	. 
	ld a,(041cdh)		;15ea	3a cd 41 	: . A 
	ld b,a			;15ed	47 	G 
	ld a,(041c6h)		;15ee	3a c6 41 	: . A 
	cp b			;15f1	b8 	. 
	jp c,l15f8h		;15f2	da f8 15 	. . . 
	ld (041cdh),a		;15f5	32 cd 41 	2 . A 
l15f8h:
	ld a,(04300h)		;15f8	3a 00 43 	: . C 
	ld c,a			;15fb	4f 	O 
	ld a,(041c7h)		;15fc	3a c7 41 	: . A 
	or c			;15ff	b1 	. 
	jp nz,l1605h		;1600	c2 05 16 	. . . 
	pop bc			;1603	c1 	. 
	ret			;1604	c9 	. 
l1605h:
	push hl			;1605	e5 	. 
	push de			;1606	d5 	. 
	ld a,(041c6h)		;1607	3a c6 41 	: . A 
	ld b,a			;160a	47 	G 
	ld hl,041cch		;160b	21 cc 41 	! . A 
	cp (hl)			;160e	be 	. 
	jp c,l1613h		;160f	da 13 16 	. . . 
	ld (hl),a			;1612	77 	w 
l1613h:
	dec hl			;1613	2b 	+ 
	ld a,(hl)			;1614	7e 	~ 
	cp b			;1615	b8 	. 
	ld a,b			;1616	78 	x 
	ld (hl),a			;1617	77 	w 
	jp nc,l1696h		;1618	d2 96 16 	. . . 
	ld h,a			;161b	67 	g 
	ld a,(042feh)		;161c	3a fe 42 	: . B 
	ld c,a			;161f	4f 	O 
	call sub_185fh		;1620	cd 5f 18 	. _ . 
	ld b,a			;1623	47 	G 
	push af			;1624	f5 	. 
	ld a,(04300h)		;1625	3a 00 43 	: . C 
	or a			;1628	b7 	. 
	jp z,l1656h		;1629	ca 56 16 	. V . 
	ld a,b			;162c	78 	x 
	sub c			;162d	91 	. 
	jp c,l1656h		;162e	da 56 16 	. V . 
	ld hl,042fdh		;1631	21 fd 42 	! . B 
	ld (hl),000h		;1634	36 00 	6 . 
	inc hl			;1636	23 	# 
	ld (hl),a			;1637	77 	w 
	ld b,a			;1638	47 	G 
	inc hl			;1639	23 	# 
	ld (hl),000h		;163a	36 00 	6 . 
	inc hl			;163c	23 	# 
	ld a,(041d6h)		;163d	3a d6 41 	: . A 
	ld (04302h),a		;1640	32 02 43 	2 . C 
l1643h:
	ld hl,04300h		;1643	21 00 43 	! . C 
	ld a,(hl)			;1646	7e 	~ 
	or a			;1647	b7 	. 
	jp z,l1656h		;1648	ca 56 16 	. V . 
	dec (hl)			;164b	35 	5 
	jp z,l1650h		;164c	ca 50 16 	. P . 
	dec (hl)			;164f	35 	5 
l1650h:
	call sub_0ff5h		;1650	cd f5 0f 	. . . 
	jp l1643h		;1653	c3 43 16 	. C . 
l1656h:
	pop hl			;1656	e1 	. 
	ld a,(041c7h)		;1657	3a c7 41 	: . A 
	or a			;165a	b7 	. 
	jp z,l1696h		;165b	ca 96 16 	. . . 
	ld b,h			;165e	44 	D 
	ld a,(041c5h)		;165f	3a c5 41 	: . A 
	ld h,a			;1662	67 	g 
	ld a,b			;1663	78 	x 
	sub h			;1664	94 	. 
	ld l,a			;1665	6f 	o 
	jp c,l1696h		;1666	da 96 16 	. . . 
	ld a,0c8h		;1669	3e c8 	> . 
	cp b			;166b	b8 	. 
	jp c,l1675h		;166c	da 75 16 	. u . 
	ld a,l			;166f	7d 	} 
	cp 027h		;1670	fe 27 	. ' 
	jp c,l1696h		;1672	da 96 16 	. . . 
l1675h:
	ld a,b			;1675	78 	x 
	ld (041cah),a		;1676	32 ca 41 	2 . A 
l1679h:
	ld a,(0402eh)		;1679	3a 2e 40 	: . @ 
	ld (042f5h),a		;167c	32 f5 42 	2 . B 
	ld hl,(04001h)		;167f	2a 01 40 	* . @ 
	ld a,(041c9h)		;1682	3a c9 41 	: . A 
	cp h			;1685	bc 	. 
	jp nc,l1696h		;1686	d2 96 16 	. . . 
	ld (041c8h),hl		;1689	22 c8 41 	" . A 
	call sub_02f7h		;168c	cd f7 02 	. . . 
	xor a			;168f	af 	. 
	ld (041c7h),a		;1690	32 c7 41 	2 . A 
	jp l1696h		;1693	c3 96 16 	. . . 
l1696h:
	pop de			;1696	d1 	. 
	pop hl			;1697	e1 	. 
	pop bc			;1698	c1 	. 
	ret			;1699	c9 	. 
sub_169ah:
	ld a,(041cch)		;169a	3a cc 41 	: . A 
	ld b,a			;169d	47 	G 
	ld a,(041c6h)		;169e	3a c6 41 	: . A 
	cp b			;16a1	b8 	. 
	jp c,l16a6h		;16a2	da a6 16 	. . . 
	ld b,a			;16a5	47 	G 
l16a6h:
	xor a			;16a6	af 	. 
	ld (041cch),a		;16a7	32 cc 41 	2 . A 
	ld h,b			;16aa	60 	` 
	ld l,a			;16ab	6f 	o 
	call sub_185fh		;16ac	cd 5f 18 	. _ . 
	ld b,a			;16af	47 	G 
	ld a,b			;16b0	78 	x 
	ld (0432bh),a		;16b1	32 2b 43 	2 + C 
	ld a,(042f0h)		;16b4	3a f0 42 	: . B 
	and 040h		;16b7	e6 40 	. @ 
	jp z,l16beh		;16b9	ca be 16 	. . . 
	ld b,010h		;16bc	06 10 	. . 
l16beh:
	ld a,(042feh)		;16be	3a fe 42 	: . B 
	ld c,a			;16c1	4f 	O 
	ld a,b			;16c2	78 	x 
	sub c			;16c3	91 	. 
	jp c,l16f3h		;16c4	da f3 16 	. . . 
	ld hl,042fdh		;16c7	21 fd 42 	! . B 
	ld (hl),000h		;16ca	36 00 	6 . 
	inc hl			;16cc	23 	# 
	ld (hl),b			;16cd	70 	p 
	ld c,b			;16ce	48 	H 
	inc hl			;16cf	23 	# 
	ld (hl),000h		;16d0	36 00 	6 . 
	inc hl			;16d2	23 	# 
	ld a,(hl)			;16d3	7e 	~ 
	or a			;16d4	b7 	. 
	jp z,l16f3h		;16d5	ca f3 16 	. . . 
	ld a,(041d6h)		;16d8	3a d6 41 	: . A 
	ld (04302h),a		;16db	32 02 43 	2 . C 
	push bc			;16de	c5 	. 
l16dfh:
	ld hl,04300h		;16df	21 00 43 	! . C 
	ld a,(hl)			;16e2	7e 	~ 
	or a			;16e3	b7 	. 
	jp z,l16f2h		;16e4	ca f2 16 	. . . 
	dec (hl)			;16e7	35 	5 
	jp z,l16ech		;16e8	ca ec 16 	. . . 
	dec (hl)			;16eb	35 	5 
l16ech:
	call sub_0ff5h		;16ec	cd f5 0f 	. . . 
	jp l16dfh		;16ef	c3 df 16 	. . . 
l16f2h:
	pop bc			;16f2	c1 	. 
l16f3h:
	ld a,(0432bh)		;16f3	3a 2b 43 	: + C 
	and 0f8h		;16f6	e6 f8 	. . 
	rra			;16f8	1f 	. 
	rra			;16f9	1f 	. 
	rra			;16fa	1f 	. 
	ld h,a			;16fb	67 	g 
	ld a,(041c5h)		;16fc	3a c5 41 	: . A 
	ld l,a			;16ff	6f 	o 
	and 0f8h		;1700	e6 f8 	. . 
	rra			;1702	1f 	. 
	rra			;1703	1f 	. 
	rra			;1704	1f 	. 
	sub l			;1705	95 	. 
	cpl			;1706	2f 	/ 
	inc a			;1707	3c 	< 
	add a,h			;1708	84 	. 
	ld (041c5h),a		;1709	32 c5 41 	2 . A 
	ld h,a			;170c	67 	g 
	ld a,(0432bh)		;170d	3a 2b 43 	: + C 
	push bc			;1710	c5 	. 
	ld b,a			;1711	47 	G 
	sub h			;1712	94 	. 
	ld l,a			;1713	6f 	o 
	jp c,l173dh		;1714	da 3d 17 	. = . 
	ld a,0c8h		;1717	3e c8 	> . 
	cp b			;1719	b8 	. 
	jp c,l1723h		;171a	da 23 17 	. # . 
	ld a,l			;171d	7d 	} 
	cp 027h		;171e	fe 27 	. ' 
	jp c,l173dh		;1720	da 3d 17 	. = . 
l1723h:
	ld a,b			;1723	78 	x 
	ld (041cah),a		;1724	32 ca 41 	2 . A 
	ld a,(041c7h)		;1727	3a c7 41 	: . A 
	and 001h		;172a	e6 01 	. . 
	jp z,l176ah		;172c	ca 6a 17 	. j . 
	ld a,0c0h		;172f	3e c0 	> . 
	ld (041c7h),a		;1731	32 c7 41 	2 . A 
	ld a,(0402eh)		;1734	3a 2e 40 	: . @ 
	ld (042f5h),a		;1737	32 f5 42 	2 . B 
	jp l176ah		;173a	c3 6a 17 	. j . 
l173dh:
	ld a,(041cah)		;173d	3a ca 41 	: . A 
	ld c,a			;1740	4f 	O 
	cp b			;1741	b8 	. 
	jp nc,l174ch		;1742	d2 4c 17 	. L . 
	ld a,(0432bh)		;1745	3a 2b 43 	: + C 
	ld c,a			;1748	4f 	O 
	ld (041cah),a		;1749	32 ca 41 	2 . A 
l174ch:
	ld a,005h		;174c	3e 05 	> . 
	ld l,a			;174e	6f 	o 
	ld a,c			;174f	79 	y 
	sub b			;1750	90 	. 
	cp l			;1751	bd 	. 
	jp c,l176ah		;1752	da 6a 17 	. j . 
	ld a,(0402bh)		;1755	3a 2b 40 	: + @ 
	and 001h		;1758	e6 01 	. . 
	jp z,l176ah		;175a	ca 6a 17 	. j . 
	ld a,(041c7h)		;175d	3a c7 41 	: . A 
	and 001h		;1760	e6 01 	. . 
	jp nz,l176ah		;1762	c2 6a 17 	. j . 
	ld a,0c1h		;1765	3e c1 	> . 
	ld (041c7h),a		;1767	32 c7 41 	2 . A 
l176ah:
	pop bc			;176a	c1 	. 
	ld hl,042feh		;176b	21 fe 42 	! . B 
	ld c,(hl)			;176e	4e 	N 
	ld a,c			;176f	79 	y 
	sub b			;1770	90 	. 
	ld b,a			;1771	47 	G 
	ld a,(0402bh)		;1772	3a 2b 40 	: + @ 
	and 080h		;1775	e6 80 	. . 
	jp z,l17a9h		;1777	ca a9 17 	. . . 
	ld a,b			;177a	78 	x 
	cp 016h		;177b	fe 16 	. . 
	inc hl			;177d	23 	# 
	jp c,l1799h		;177e	da 99 17 	. . . 
	ld a,(hl)			;1781	7e 	~ 
	or a			;1782	b7 	. 
	jp nz,l1799h		;1783	c2 99 17 	. . . 
	ld (hl),001h		;1786	36 01 	6 . 
	ld hl,04303h		;1788	21 03 43 	! . C 
	ld b,(hl)			;178b	46 	F 
	ld a,c			;178c	79 	y 
	sub b			;178d	90 	. 
	jp c,l1799h		;178e	da 99 17 	. . . 
	cp 018h		;1791	fe 18 	. . 
	jp c,l1799h		;1793	da 99 17 	. . . 
	dec hl			;1796	2b 	+ 
	ld (hl),00fh		;1797	36 0f 	6 . 
l1799h:
	ld de,04303h		;1799	11 03 43 	. . C 
	ld hl,04304h		;179c	21 04 43 	! . C 
	push bc			;179f	c5 	. 
	ld c,00ah		;17a0	0e 0a 	. . 
	ld b,000h		;17a2	06 00 	. . 
	ldir		;17a4	ed b0 	. . 
	pop bc			;17a6	c1 	. 
	ld a,c			;17a7	79 	y 
	ld (de),a			;17a8	12 	. 
l17a9h:
	ld a,(041c7h)		;17a9	3a c7 41 	: . A 
	ld b,a			;17ac	47 	G 
	and 0c0h		;17ad	e6 c0 	. . 
	jp z,l1870h		;17af	ca 70 18 	. p . 
	and 080h		;17b2	e6 80 	. . 
	jp z,l17f0h		;17b4	ca f0 17 	. . . 
	ld a,(041c9h)		;17b7	3a c9 41 	: . A 
	and 0f8h		;17ba	e6 f8 	. . 
	ld d,a			;17bc	57 	W 
	ld a,b			;17bd	78 	x 
	rra			;17be	1f 	. 
	jp nc,l17dfh		;17bf	d2 df 17 	. . . 
	ld hl,042f5h		;17c2	21 f5 42 	! . B 
	ld a,(hl)			;17c5	7e 	~ 
	or a			;17c6	b7 	. 
	jp z,l17ceh		;17c7	ca ce 17 	. . . 
	dec (hl)			;17ca	35 	5 
	jp l1870h		;17cb	c3 70 18 	. p . 
l17ceh:
	ld a,(042e7h)		;17ce	3a e7 42 	: . B 
	and 040h		;17d1	e6 40 	. @ 
	ld hl,04008h		;17d3	21 08 40 	! . @ 
	jp nz,l17e2h		;17d6	c2 e2 17 	. . . 
	ld hl,0400eh		;17d9	21 0e 40 	! . @ 
	jp l17e2h		;17dc	c3 e2 17 	. . . 
l17dfh:
	ld hl,04002h		;17df	21 02 40 	! . @ 
l17e2h:
	call sub_1840h		;17e2	cd 40 18 	. @ . 
	ld a,d			;17e5	7a 	z 
	ld (041c9h),a		;17e6	32 c9 41 	2 . A 
	ld a,b			;17e9	78 	x 
	jp nz,l17f0h		;17ea	c2 f0 17 	. . . 
	and 07fh		;17ed	e6 7f 	.  
	ld b,a			;17ef	47 	G 
l17f0h:
	ld a,b			;17f0	78 	x 
	and 040h		;17f1	e6 40 	. @ 
	ld a,b			;17f3	78 	x 
	jp z,l182fh		;17f4	ca 2f 18 	. / . 
	ld a,(041c8h)		;17f7	3a c8 41 	: . A 
	and 0f8h		;17fa	e6 f8 	. . 
	ld d,a			;17fc	57 	W 
	ld a,b			;17fd	78 	x 
	rra			;17fe	1f 	. 
	jp nc,l181fh		;17ff	d2 1f 18 	. . . 
	ld hl,042f5h		;1802	21 f5 42 	! . B 
	ld a,(hl)			;1805	7e 	~ 
	or a			;1806	b7 	. 
	jp z,l180eh		;1807	ca 0e 18 	. . . 
	dec (hl)			;180a	35 	5 
	jp l1870h		;180b	c3 70 18 	. p . 
l180eh:
	ld hl,04007h		;180e	21 07 40 	! . @ 
	ld a,(042e7h)		;1811	3a e7 42 	: . B 
	and 040h		;1814	e6 40 	. @ 
	jp nz,l1822h		;1816	c2 22 18 	. " . 
	ld hl,0400dh		;1819	21 0d 40 	! . @ 
	jp l1822h		;181c	c3 22 18 	. " . 
l181fh:
	ld hl,04001h		;181f	21 01 40 	! . @ 
l1822h:
	call sub_1840h		;1822	cd 40 18 	. @ . 
	ld a,d			;1825	7a 	z 
	ld (041c8h),a		;1826	32 c8 41 	2 . A 
	ld a,b			;1829	78 	x 
	jp nz,l182fh		;182a	c2 2f 18 	. / . 
	and 0bfh		;182d	e6 bf 	. . 
l182fh:
	ld (041c7h),a		;182f	32 c7 41 	2 . A 
	call sub_02f7h		;1832	cd f7 02 	. . . 
	ld a,(041c7h)		;1835	3a c7 41 	: . A 
	and 0c0h		;1838	e6 c0 	. . 
	jp nz,l17a9h		;183a	c2 a9 17 	. . . 
	jp l1870h		;183d	c3 70 18 	. p . 
sub_1840h:
	ld a,(hl)			;1840	7e 	~ 
	cp d			;1841	ba 	. 
	jp c,l1848h		;1842	da 48 18 	. H . 
	ld d,(hl)			;1845	56 	V 
	xor a			;1846	af 	. 
	ret			;1847	c9 	. 
l1848h:
	ld a,(hl)			;1848	7e 	~ 
	sub d			;1849	92 	. 
	jp nc,l1853h		;184a	d2 53 18 	. S . 
	ld a,d			;184d	7a 	z 
	sub 008h		;184e	d6 08 	. . 
	jp l1859h		;1850	c3 59 18 	. Y . 
l1853h:
	and 0f8h		;1853	e6 f8 	. . 
	ret z			;1855	c8 	. 
	ld a,d			;1856	7a 	z 
	add a,008h		;1857	c6 08 	. . 
l1859h:
	ld d,a			;1859	57 	W 
	ld a,(hl)			;185a	7e 	~ 
	sub d			;185b	92 	. 
	and 0f8h		;185c	e6 f8 	. . 
	ret			;185e	c9 	. 
sub_185fh:
	ld a,l			;185f	7d 	} 
	or 002h		;1860	f6 02 	. . 
	ld l,a			;1862	6f 	o 
	ld a,007h		;1863	3e 07 	> . 
l1865h:
	sub 010h		;1865	d6 10 	. . 
	add hl,hl			;1867	29 	) 
	jp nc,l1865h		;1868	d2 65 18 	. e . 
	add hl,hl			;186b	29 	) 
	ret nc			;186c	d0 	. 
	add a,008h		;186d	c6 08 	. . 
	ret			;186f	c9 	. 
l1870h:
	ld hl,04302h		;1870	21 02 43 	! . C 
	ld a,(04188h)		;1873	3a 88 41 	: . A 
	cp 020h		;1876	fe 20 	.   
	jp z,l188ch		;1878	ca 8c 18 	. . . 
	ld a,(042f8h)		;187b	3a f8 42 	: . B 
	or a			;187e	b7 	. 
	jp nz,l188ah		;187f	c2 8a 18 	. . . 
	ld a,(042f7h)		;1882	3a f7 42 	: . B 
	cp 078h		;1885	fe 78 	. x 
	jp c,l188ch		;1887	da 8c 18 	. . . 
l188ah:
	ld (hl),014h		;188a	36 14 	6 . 
l188ch:
	ld a,(hl)			;188c	7e 	~ 
	dec hl			;188d	2b 	+ 
	dec (hl)			;188e	35 	5 
	jp nz,l18c0h		;188f	c2 c0 18 	. . . 
	ld (hl),a			;1892	77 	w 
	ld hl,042ffh		;1893	21 ff 42 	! . B 
	ld a,(hl)			;1896	7e 	~ 
	inc hl			;1897	23 	# 
	or a			;1898	b7 	. 
	jp nz,l18a8h		;1899	c2 a8 18 	. . . 
	ld a,(hl)			;189c	7e 	~ 
	or a			;189d	b7 	. 
	jp z,l18c0h		;189e	ca c0 18 	. . . 
	dec (hl)			;18a1	35 	5 
	call sub_0ff5h		;18a2	cd f5 0f 	. . . 
	jp l18c0h		;18a5	c3 c0 18 	. . . 
l18a8h:
	ld a,(04188h)		;18a8	3a 88 41 	: . A 
	cp 020h		;18ab	fe 20 	.   
	ld a,(hl)			;18ad	7e 	~ 
	jp z,l18b6h		;18ae	ca b6 18 	. . . 
	cp 00ch		;18b1	fe 0c 	. . 
	jp nc,l18c0h		;18b3	d2 c0 18 	. . . 
l18b6h:
	cp 014h		;18b6	fe 14 	. . 
	jp nc,l18c0h		;18b8	d2 c0 18 	. . . 
	inc a			;18bb	3c 	< 
	ld (hl),a			;18bc	77 	w 
	call sub_0ff5h		;18bd	cd f5 0f 	. . . 
l18c0h:
	ld hl,041ceh		;18c0	21 ce 41 	! . A 
	dec (hl)			;18c3	35 	5 
	jp nz,l18fbh		;18c4	c2 fb 18 	. . . 
	ld (hl),008h		;18c7	36 08 	6 . 
	ld a,(04188h)		;18c9	3a 88 41 	: . A 
	cp 020h		;18cc	fe 20 	.   
	jp z,l18fbh		;18ce	ca fb 18 	. . . 
	ld hl,(042f7h)		;18d1	2a f7 42 	* . B 
	add hl,hl			;18d4	29 	) 
	add hl,hl			;18d5	29 	) 
	add hl,hl			;18d6	29 	) 
	add hl,hl			;18d7	29 	) 
	ld b,h			;18d8	44 	D 
	ld c,l			;18d9	4d 	M 
	ld hl,l0010h		;18da	21 10 00 	! . . 
	call sub_0cc9h		;18dd	cd c9 0c 	. . . 
	ld hl,(042fdh)		;18e0	2a fd 42 	* . B 
	or a			;18e3	b7 	. 
	sbc hl,de		;18e4	ed 52 	. R 
	jp nc,l18ech		;18e6	d2 ec 18 	. . . 
	ld hl,l0000h		;18e9	21 00 00 	! . . 
l18ech:
	ld (042fdh),hl		;18ec	22 fd 42 	" . B 
	ld hl,041cah		;18ef	21 ca 41 	! . A 
	ld a,(hl)			;18f2	7e 	~ 
	sub 003h		;18f3	d6 03 	. . 
	jp nc,l18fah		;18f5	d2 fa 18 	. . . 
	ld a,000h		;18f8	3e 00 	> . 
l18fah:
	ld (hl),a			;18fa	77 	w 
l18fbh:
	ret			;18fb	c9 	. 
	ld d,b			;18fc	50 	P 
	ld d,d			;18fd	52 	R 
	ld b,l			;18fe	45 	E 
	ld d,h			;18ff	54 	T 
	ld b,c			;1900	41 	A 
	ld b,d			;1901	42 	B 
l1902h:
	ld d,(hl)			;1902	56 	V 
	add hl,de			;1903	19 	. 
	adc a,019h		;1904	ce 19 	. . 
	ld b,(hl)			;1906	46 	F 
	ld a,(de)			;1907	1a 	. 
	cp (hl)			;1908	be 	. 
	ld a,(de)			;1909	1a 	. 
	ld (hl),01bh		;190a	36 1b 	6 . 
	xor (hl)			;190c	ae 	. 
	dec de			;190d	1b 	. 
	ld h,01ch		;190e	26 1c 	& . 
	sbc a,(hl)			;1910	9e 	. 
	inc e			;1911	1c 	. 
	ld d,01dh		;1912	16 1d 	. . 
	adc a,(hl)			;1914	8e 	. 
	dec e			;1915	1d 	. 
	ld bc,0791eh		;1916	01 1e 79 	. . y 
	ld e,0f1h		;1919	1e f1 	. . 
	ld e,069h		;191b	1e 69 	. i 
	rra			;191d	1f 	. 
	pop hl			;191e	e1 	. 
	rra			;191f	1f 	. 
	ld e,c			;1920	59 	Y 
	jr nz,$-45		;1921	20 d1 	  . 
	jr nz,l196eh		;1923	20 49 	  I 
	ld hl,l21c1h		;1925	21 c1 21 	! . ! 
	add hl,sp			;1928	39 	9 
	ld (l22b1h),hl		;1929	22 b1 22 	" . " 
	add hl,hl			;192c	29 	) 
	inc hl			;192d	23 	# 
	and c			;192e	a1 	. 
	inc hl			;192f	23 	# 
	add hl,de			;1930	19 	. 
	inc h			;1931	24 	$ 
	sub c			;1932	91 	. 
	inc h			;1933	24 	$ 
	add hl,bc			;1934	09 	. 
	dec h			;1935	25 	% 
	add a,c			;1936	81 	. 
	dec h			;1937	25 	% 
	ld sp,hl			;1938	f9 	. 
	dec h			;1939	25 	% 
	ld (hl),c			;193a	71 	q 
	ld h,0e9h		;193b	26 e9 	& . 
	ld h,061h		;193d	26 61 	& a 
	daa			;193f	27 	' 
	ld (hl),c			;1940	71 	q 
	daa			;1941	27 	' 
	add a,c			;1942	81 	. 
	daa			;1943	27 	' 
	sub c			;1944	91 	. 
	daa			;1945	27 	' 
	and c			;1946	a1 	. 
	daa			;1947	27 	' 
	ld c,l			;1948	4d 	M 
	inc l			;1949	2c 	, 
	sbc a,d			;194a	9a 	. 
	dec l			;194b	2d 	- 
	or e			;194c	b3 	. 
	ld (l35e6h),a		;194d	32 e6 35 	2 . 5 
	add hl,de			;1950	19 	. 
	add hl,sp			;1951	39 	9 
	ld c,h			;1952	4c 	L 
	inc a			;1953	3c 	< 
	ld a,a			;1954	7f 	 
	ccf			;1955	3f 	? 
	inc b			;1956	04 	. 
	ld b,e			;1957	43 	C 
	ld c,b			;1958	48 	H 
	ld c,a			;1959	4f 	O 
	ld d,d			;195a	52 	R 
	ld d,l			;195b	55 	U 
	ld d,e			;195c	53 	S 
	jr nz,l197fh		;195d	20 20 	    
	jr nz,l1981h		;195f	20 20 	    
	jr nz,l1983h		;1961	20 20 	    
	jr nz,l1965h		;1963	20 00 	  . 
l1965h:
	nop			;1965	00 	. 
	nop			;1966	00 	. 
	nop			;1967	00 	. 
	nop			;1968	00 	. 
	nop			;1969	00 	. 
	nop			;196a	00 	. 
	nop			;196b	00 	. 
	nop			;196c	00 	. 
	nop			;196d	00 	. 
l196eh:
	nop			;196e	00 	. 
	nop			;196f	00 	. 
	nop			;1970	00 	. 
	nop			;1971	00 	. 
	nop			;1972	00 	. 
	nop			;1973	00 	. 
	nop			;1974	00 	. 
	nop			;1975	00 	. 
	nop			;1976	00 	. 
	nop			;1977	00 	. 
	nop			;1978	00 	. 
	nop			;1979	00 	. 
	nop			;197a	00 	. 
	nop			;197b	00 	. 
	nop			;197c	00 	. 
	nop			;197d	00 	. 
	nop			;197e	00 	. 
l197fh:
	nop			;197f	00 	. 
	nop			;1980	00 	. 
l1981h:
	nop			;1981	00 	. 
	nop			;1982	00 	. 
l1983h:
	ld (0c025h),a		;1983	32 25 c0 	2 % . 
	ld c,09ah		;1986	0e 9a 	. . 
	rrca			;1988	0f 	. 
	adc a,003h		;1989	ce 03 	. . 
	nop			;198b	00 	. 
	and (hl)			;198c	a6 	. 
	nop			;198d	00 	. 
	nop			;198e	00 	. 
	nop			;198f	00 	. 
	ld (de),a			;1990	12 	. 
	xor d			;1991	aa 	. 
	ld (de),a			;1992	12 	. 
	ld (de),a			;1993	12 	. 
	ld (de),a			;1994	12 	. 
	ld (de),a			;1995	12 	. 
	xor d			;1996	aa 	. 
	ld (de),a			;1997	12 	. 
	nop			;1998	00 	. 
	jp nz,05ac8h		;1999	c2 c8 5a 	. . Z 
	adc a,0b5h		;199c	ce b5 	. . 
	cp e			;199e	bb 	. 
	cp a			;199f	bf 	. 
	ld d,l			;19a0	55 	U 
	nop			;19a1	00 	. 
	dec b			;19a2	05 	. 
	ei			;19a3	fb 	. 
	ld a,(bc)			;19a4	0a 	. 
l19a5h:
	sbc a,d			;19a5	9a 	. 
	or 008h		;19a6	f6 08 	. . 
	ret m			;19a8	f8 	. 
	nop			;19a9	00 	. 
	sbc a,c			;19aa	99 	. 
	adc a,032h		;19ab	ce 32 	. 2 
	ret c			;19ad	d8 	. 
	ld (0ce99h),a		;19ae	32 99 ce 	2 . . 
	jr z,l19b3h		;19b1	28 00 	( . 
l19b3h:
	nop			;19b3	00 	. 
	xor c			;19b4	a9 	. 
	nop			;19b5	00 	. 
	nop			;19b6	00 	. 
	nop			;19b7	00 	. 
	nop			;19b8	00 	. 
	xor d			;19b9	aa 	. 
	nop			;19ba	00 	. 
	nop			;19bb	00 	. 
	nop			;19bc	00 	. 
	nop			;19bd	00 	. 
	xor d			;19be	aa 	. 
	nop			;19bf	00 	. 
	nop			;19c0	00 	. 
	nop			;19c1	00 	. 
	nop			;19c2	00 	. 
	xor d			;19c3	aa 	. 
	nop			;19c4	00 	. 
	nop			;19c5	00 	. 
	nop			;19c6	00 	. 
	nop			;19c7	00 	. 
l19c8h:
	xor d			;19c8	aa 	. 
	nop			;19c9	00 	. 
	nop			;19ca	00 	. 
	nop			;19cb	00 	. 
	nop			;19cc	00 	. 
	xor d			;19cd	aa 	. 
	inc b			;19ce	04 	. 
	ld b,e			;19cf	43 	C 
	ld c,b			;19d0	48 	H 
	ld c,a			;19d1	4f 	O 
	ld d,d			;19d2	52 	R 
	ld d,l			;19d3	55 	U 
	ld d,e			;19d4	53 	S 
	jr nz,l1a1ch		;19d5	20 45 	  E 
	ld b,e			;19d7	43 	C 
	ld c,b			;19d8	48 	H 
	ld c,a			;19d9	4f 	O 
	ld b,l			;19da	45 	E 
	ld d,e			;19db	53 	S 
	nop			;19dc	00 	. 
	nop			;19dd	00 	. 
	nop			;19de	00 	. 
	nop			;19df	00 	. 
	nop			;19e0	00 	. 
	nop			;19e1	00 	. 
	nop			;19e2	00 	. 
	nop			;19e3	00 	. 
	nop			;19e4	00 	. 
	nop			;19e5	00 	. 
	nop			;19e6	00 	. 
	nop			;19e7	00 	. 
	nop			;19e8	00 	. 
	nop			;19e9	00 	. 
	nop			;19ea	00 	. 
	nop			;19eb	00 	. 
	nop			;19ec	00 	. 
	nop			;19ed	00 	. 
	nop			;19ee	00 	. 
	nop			;19ef	00 	. 
	nop			;19f0	00 	. 
	nop			;19f1	00 	. 
	nop			;19f2	00 	. 
	nop			;19f3	00 	. 
	nop			;19f4	00 	. 
	nop			;19f5	00 	. 
	nop			;19f6	00 	. 
	nop			;19f7	00 	. 
	nop			;19f8	00 	. 
	nop			;19f9	00 	. 
	nop			;19fa	00 	. 
	ld (0c025h),a		;19fb	32 25 c0 	2 % . 
	nop			;19fe	00 	. 
	sbc a,d			;19ff	9a 	. 
	rrca			;1a00	0f 	. 
	dec d			;1a01	15 	. 
	ld b,000h		;1a02	06 00 	. . 
	xor d			;1a04	aa 	. 
	nop			;1a05	00 	. 
	nop			;1a06	00 	. 
	nop			;1a07	00 	. 
	ld (de),a			;1a08	12 	. 
	xor d			;1a09	aa 	. 
	ld (de),a			;1a0a	12 	. 
	call m,012fch		;1a0b	fc fc 12 	. . . 
	sub (hl)			;1a0e	96 	. 
	ld (de),a			;1a0f	12 	. 
	nop			;1a10	00 	. 
	ret z			;1a11	c8 	. 
	pop de			;1a12	d1 	. 
	ld e,d			;1a13	5a 	Z 
	ld a,(hl)			;1a14	7e 	~ 
	ld a,(hl)			;1a15	7e 	~ 
	cp d			;1a16	ba 	. 
	cp (hl)			;1a17	be 	. 
	ld e,d			;1a18	5a 	Z 
	nop			;1a19	00 	. 
	nop			;1a1a	00 	. 
	nop			;1a1b	00 	. 
l1a1ch:
	jr nc,l19c8h		;1a1c	30 aa 	0 . 
	out (000h),a		;1a1e	d3 00 	. . 
	nop			;1a20	00 	. 
	nop			;1a21	00 	. 
	xor c			;1a22	a9 	. 
	adc a,0ceh		;1a23	ce ce 	. . 
	adc a,032h		;1a25	ce 32 	. 2 
	sub l			;1a27	95 	. 
	ld (l0032h),a		;1a28	32 32 00 	2 2 . 
	nop			;1a2b	00 	. 
	xor d			;1a2c	aa 	. 
	nop			;1a2d	00 	. 
	nop			;1a2e	00 	. 
	nop			;1a2f	00 	. 
	nop			;1a30	00 	. 
	xor d			;1a31	aa 	. 
	nop			;1a32	00 	. 
	nop			;1a33	00 	. 
	nop			;1a34	00 	. 
	nop			;1a35	00 	. 
	xor d			;1a36	aa 	. 
	nop			;1a37	00 	. 
	nop			;1a38	00 	. 
	nop			;1a39	00 	. 
	nop			;1a3a	00 	. 
	xor d			;1a3b	aa 	. 
	nop			;1a3c	00 	. 
	nop			;1a3d	00 	. 
	nop			;1a3e	00 	. 
	nop			;1a3f	00 	. 
	xor d			;1a40	aa 	. 
	nop			;1a41	00 	. 
	nop			;1a42	00 	. 
	nop			;1a43	00 	. 
	nop			;1a44	00 	. 
	xor d			;1a45	aa 	. 
	inc b			;1a46	04 	. 
	ld b,l			;1a47	45 	E 
	ld b,e			;1a48	43 	C 
	ld c,b			;1a49	48 	H 
	ld c,a			;1a4a	4f 	O 
	jr nz,$+72		;1a4b	20 46 	  F 
	ld c,h			;1a4d	4c 	L 
	ld b,c			;1a4e	41 	A 
	ld c,(hl)			;1a4f	4e 	N 
	ld b,a			;1a50	47 	G 
	ld b,l			;1a51	45 	E 
	jr nz,$+34		;1a52	20 20 	    
	nop			;1a54	00 	. 
	nop			;1a55	00 	. 
	nop			;1a56	00 	. 
	nop			;1a57	00 	. 
	nop			;1a58	00 	. 
	nop			;1a59	00 	. 
	nop			;1a5a	00 	. 
	nop			;1a5b	00 	. 
	nop			;1a5c	00 	. 
	nop			;1a5d	00 	. 
	nop			;1a5e	00 	. 
	nop			;1a5f	00 	. 
	nop			;1a60	00 	. 
	nop			;1a61	00 	. 
	nop			;1a62	00 	. 
	nop			;1a63	00 	. 
	nop			;1a64	00 	. 
	nop			;1a65	00 	. 
	nop			;1a66	00 	. 
	nop			;1a67	00 	. 
	nop			;1a68	00 	. 
	nop			;1a69	00 	. 
	nop			;1a6a	00 	. 
	nop			;1a6b	00 	. 
	nop			;1a6c	00 	. 
	nop			;1a6d	00 	. 
	nop			;1a6e	00 	. 
	nop			;1a6f	00 	. 
	nop			;1a70	00 	. 
	nop			;1a71	00 	. 
	nop			;1a72	00 	. 
	ld (0c027h),a		;1a73	32 27 c0 	2 ' . 
	defb 0fdh,05ah,00fh	;illegal sequence		;1a76	fd 5a 0f 	. Z . 
	jp pe,l0000h		;1a79	ea 00 00 	. . . 
	and (hl)			;1a7c	a6 	. 
	nop			;1a7d	00 	. 
	nop			;1a7e	00 	. 
	nop			;1a7f	00 	. 
	ld (bc),a			;1a80	02 	. 
	xor d			;1a81	aa 	. 
	ld (bc),a			;1a82	02 	. 
	dec c			;1a83	0d 	. 
	dec c			;1a84	0d 	. 
	ld (de),a			;1a85	12 	. 
	xor d			;1a86	aa 	. 
	ld (de),a			;1a87	12 	. 
	nop			;1a88	00 	. 
	ld h,055h		;1a89	26 55 	& U 
	xor d			;1a8b	aa 	. 
	ld (hl),b			;1a8c	70 	p 
	ld a,(hl)			;1a8d	7e 	~ 
	ld a,(hl)			;1a8e	7e 	~ 
	ld a,(hl)			;1a8f	7e 	~ 
	xor d			;1a90	aa 	. 
	nop			;1a91	00 	. 
	ld e,00ah		;1a92	1e 0a 	. . 
	inc d			;1a94	14 	. 
	xor d			;1a95	aa 	. 
	add hl,de			;1a96	19 	. 
	rrca			;1a97	0f 	. 
	inc de			;1a98	13 	. 
	nop			;1a99	00 	. 
	xor d			;1a9a	aa 	. 
	adc a,032h		;1a9b	ce 32 	. 2 
	rst 20h			;1a9d	e7 	. 
	add hl,de			;1a9e	19 	. 
	sbc a,c			;1a9f	99 	. 
	or 00ah		;1aa0	f6 0a 	. . 
	nop			;1aa2	00 	. 
	nop			;1aa3	00 	. 
	xor c			;1aa4	a9 	. 
	nop			;1aa5	00 	. 
	nop			;1aa6	00 	. 
	nop			;1aa7	00 	. 
	nop			;1aa8	00 	. 
	xor d			;1aa9	aa 	. 
	nop			;1aaa	00 	. 
	nop			;1aab	00 	. 
	nop			;1aac	00 	. 
	nop			;1aad	00 	. 
	xor d			;1aae	aa 	. 
	nop			;1aaf	00 	. 
	nop			;1ab0	00 	. 
	nop			;1ab1	00 	. 
	nop			;1ab2	00 	. 
	xor d			;1ab3	aa 	. 
	nop			;1ab4	00 	. 
	nop			;1ab5	00 	. 
	nop			;1ab6	00 	. 
	nop			;1ab7	00 	. 
	xor d			;1ab8	aa 	. 
	nop			;1ab9	00 	. 
	nop			;1aba	00 	. 
	nop			;1abb	00 	. 
	nop			;1abc	00 	. 
	xor d			;1abd	aa 	. 
	inc b			;1abe	04 	. 
	ld d,e			;1abf	53 	S 
	ld d,h			;1ac0	54 	T 
	ld b,l			;1ac1	45 	E 
	ld d,d			;1ac2	52 	R 
	ld b,l			;1ac3	45 	E 
	ld c,a			;1ac4	4f 	O 
	jr nz,l1b0dh		;1ac5	20 46 	  F 
	ld c,h			;1ac7	4c 	L 
	ld b,c			;1ac8	41 	A 
	ld c,(hl)			;1ac9	4e 	N 
	ld b,a			;1aca	47 	G 
	ld b,l			;1acb	45 	E 
	nop			;1acc	00 	. 
	nop			;1acd	00 	. 
	nop			;1ace	00 	. 
	nop			;1acf	00 	. 
	nop			;1ad0	00 	. 
	nop			;1ad1	00 	. 
	nop			;1ad2	00 	. 
	nop			;1ad3	00 	. 
	nop			;1ad4	00 	. 
	nop			;1ad5	00 	. 
	nop			;1ad6	00 	. 
	nop			;1ad7	00 	. 
	nop			;1ad8	00 	. 
	nop			;1ad9	00 	. 
	nop			;1ada	00 	. 
	nop			;1adb	00 	. 
	nop			;1adc	00 	. 
	nop			;1add	00 	. 
	nop			;1ade	00 	. 
	nop			;1adf	00 	. 
	nop			;1ae0	00 	. 
	nop			;1ae1	00 	. 
	nop			;1ae2	00 	. 
	nop			;1ae3	00 	. 
	nop			;1ae4	00 	. 
	nop			;1ae5	00 	. 
	nop			;1ae6	00 	. 
	nop			;1ae7	00 	. 
	nop			;1ae8	00 	. 
	nop			;1ae9	00 	. 
	nop			;1aea	00 	. 
	ld (0c025h),a		;1aeb	32 25 c0 	2 % . 
	inc c			;1aee	0c 	. 
	sbc a,d			;1aef	9a 	. 
	rrca			;1af0	0f 	. 
	adc a,004h		;1af1	ce 04 	. . 
	nop			;1af3	00 	. 
	and (hl)			;1af4	a6 	. 
	nop			;1af5	00 	. 
	nop			;1af6	00 	. 
	nop			;1af7	00 	. 
	ld (de),a			;1af8	12 	. 
	xor d			;1af9	aa 	. 
	ld (de),a			;1afa	12 	. 
	ld (de),a			;1afb	12 	. 
	ld (de),a			;1afc	12 	. 
	rst 28h			;1afd	ef 	. 
	ld l,d			;1afe	6a 	j 
	rst 28h			;1aff	ef 	. 
	nop			;1b00	00 	. 
	sub h			;1b01	94 	. 
l1b02h:
	sub l			;1b02	95 	. 
	ld e,c			;1b03	59 	Y 
	sub e			;1b04	93 	. 
	sbc a,b			;1b05	98 	. 
	add a,d			;1b06	82 	. 
	add a,d			;1b07	82 	. 
	ld d,l			;1b08	55 	U 
	nop			;1b09	00 	. 
	add hl,de			;1b0a	19 	. 
	rst 20h			;1b0b	e7 	. 
	add hl,de			;1b0c	19 	. 
l1b0dh:
	sbc a,d			;1b0d	9a 	. 
	rst 20h			;1b0e	e7 	. 
	dec bc			;1b0f	0b 	. 
	push af			;1b10	f5 	. 
	nop			;1b11	00 	. 
	sbc a,c			;1b12	99 	. 
	adc a,0ceh		;1b13	ce ce 	. . 
	ld (0a532h),a		;1b15	32 32 a5 	2 2 . 
	rst 28h			;1b18	ef 	. 
	ld de,l0000h		;1b19	11 00 00 	. . . 
	xor c			;1b1c	a9 	. 
	nop			;1b1d	00 	. 
	nop			;1b1e	00 	. 
	nop			;1b1f	00 	. 
	nop			;1b20	00 	. 
	xor d			;1b21	aa 	. 
	nop			;1b22	00 	. 
	nop			;1b23	00 	. 
	nop			;1b24	00 	. 
	nop			;1b25	00 	. 
	xor d			;1b26	aa 	. 
	nop			;1b27	00 	. 
	nop			;1b28	00 	. 
	nop			;1b29	00 	. 
	nop			;1b2a	00 	. 
	xor d			;1b2b	aa 	. 
	nop			;1b2c	00 	. 
	nop			;1b2d	00 	. 
	nop			;1b2e	00 	. 
	nop			;1b2f	00 	. 
	xor d			;1b30	aa 	. 
	nop			;1b31	00 	. 
	nop			;1b32	00 	. 
	nop			;1b33	00 	. 
	nop			;1b34	00 	. 
	xor d			;1b35	aa 	. 
	inc b			;1b36	04 	. 
	ld b,h			;1b37	44 	D 
	ld c,a			;1b38	4f 	O 
	ld d,l			;1b39	55 	U 
	ld b,d			;1b3a	42 	B 
	ld c,h			;1b3b	4c 	L 
	ld b,l			;1b3c	45 	E 
	jr nz,l1b92h		;1b3d	20 53 	  S 
	ld c,h			;1b3f	4c 	L 
	ld b,c			;1b40	41 	A 
	ld d,b			;1b41	50 	P 
	jr nz,$+34		;1b42	20 20 	    
	nop			;1b44	00 	. 
	nop			;1b45	00 	. 
	nop			;1b46	00 	. 
	nop			;1b47	00 	. 
	nop			;1b48	00 	. 
	nop			;1b49	00 	. 
	nop			;1b4a	00 	. 
	nop			;1b4b	00 	. 
	nop			;1b4c	00 	. 
	nop			;1b4d	00 	. 
	nop			;1b4e	00 	. 
	nop			;1b4f	00 	. 
	nop			;1b50	00 	. 
	nop			;1b51	00 	. 
	nop			;1b52	00 	. 
	nop			;1b53	00 	. 
	nop			;1b54	00 	. 
	nop			;1b55	00 	. 
	nop			;1b56	00 	. 
	nop			;1b57	00 	. 
	nop			;1b58	00 	. 
	nop			;1b59	00 	. 
	nop			;1b5a	00 	. 
	nop			;1b5b	00 	. 
	nop			;1b5c	00 	. 
	nop			;1b5d	00 	. 
	nop			;1b5e	00 	. 
	nop			;1b5f	00 	. 
	nop			;1b60	00 	. 
	nop			;1b61	00 	. 
	nop			;1b62	00 	. 
	ld (0c026h),a		;1b63	32 26 c0 	2 & . 
	dec b			;1b66	05 	. 
	sbc a,d			;1b67	9a 	. 
l1b68h:
	rrca			;1b68	0f 	. 
	call pe,l0000h		;1b69	ec 00 00 	. . . 
	and (hl)			;1b6c	a6 	. 
	nop			;1b6d	00 	. 
	nop			;1b6e	00 	. 
	nop			;1b6f	00 	. 
	ld (de),a			;1b70	12 	. 
	xor d			;1b71	aa 	. 
	ld (de),a			;1b72	12 	. 
	rst 28h			;1b73	ef 	. 
	ld (de),a			;1b74	12 	. 
	ld (de),a			;1b75	12 	. 
	and (hl)			;1b76	a6 	. 
	rst 28h			;1b77	ef 	. 
	nop			;1b78	00 	. 
	dec de			;1b79	1b 	. 
	and 069h		;1b7a	e6 69 	. i 
	add a,d			;1b7c	82 	. 
	jr l1b68h		;1b7d	18 e9 	. . 
	add a,d			;1b7f	82 	. 
	ld e,c			;1b80	59 	Y 
	nop			;1b81	00 	. 
	rla			;1b82	17 	. 
	nop			;1b83	00 	. 
	nop			;1b84	00 	. 
	xor d			;1b85	aa 	. 
	rla			;1b86	17 	. 
	nop			;1b87	00 	. 
	nop			;1b88	00 	. 
	nop			;1b89	00 	. 
	xor d			;1b8a	aa 	. 
	adc a,0e7h		;1b8b	ce e7 	. . 
	nop			;1b8d	00 	. 
	ld (l19a5h),a		;1b8e	32 a5 19 	2 . . 
	nop			;1b91	00 	. 
l1b92h:
	nop			;1b92	00 	. 
	nop			;1b93	00 	. 
	xor d			;1b94	aa 	. 
	nop			;1b95	00 	. 
	nop			;1b96	00 	. 
	nop			;1b97	00 	. 
l1b98h:
	nop			;1b98	00 	. 
	xor d			;1b99	aa 	. 
	nop			;1b9a	00 	. 
	nop			;1b9b	00 	. 
	nop			;1b9c	00 	. 
	nop			;1b9d	00 	. 
	xor d			;1b9e	aa 	. 
	nop			;1b9f	00 	. 
	nop			;1ba0	00 	. 
	nop			;1ba1	00 	. 
	nop			;1ba2	00 	. 
	xor d			;1ba3	aa 	. 
	nop			;1ba4	00 	. 
	nop			;1ba5	00 	. 
	nop			;1ba6	00 	. 
	nop			;1ba7	00 	. 
	xor d			;1ba8	aa 	. 
	nop			;1ba9	00 	. 
	nop			;1baa	00 	. 
	nop			;1bab	00 	. 
	nop			;1bac	00 	. 
	xor d			;1bad	aa 	. 
	inc b			;1bae	04 	. 
	ld d,e			;1baf	53 	S 
	ld d,b			;1bb0	50 	P 
	ld c,c			;1bb1	49 	I 
	ld c,l			;1bb2	4d 	M 
	jr nz,l1bfah		;1bb3	20 45 	  E 
	ld b,e			;1bb5	43 	C 
	ld c,b			;1bb6	48 	H 
	ld c,a			;1bb7	4f 	O 
	ld b,l			;1bb8	45 	E 
	ld d,e			;1bb9	53 	S 
	jr nz,$+34		;1bba	20 20 	    
	nop			;1bbc	00 	. 
	nop			;1bbd	00 	. 
	nop			;1bbe	00 	. 
	nop			;1bbf	00 	. 
	nop			;1bc0	00 	. 
	nop			;1bc1	00 	. 
	nop			;1bc2	00 	. 
	nop			;1bc3	00 	. 
	nop			;1bc4	00 	. 
	nop			;1bc5	00 	. 
	nop			;1bc6	00 	. 
	nop			;1bc7	00 	. 
	nop			;1bc8	00 	. 
	nop			;1bc9	00 	. 
	nop			;1bca	00 	. 
	nop			;1bcb	00 	. 
	nop			;1bcc	00 	. 
	nop			;1bcd	00 	. 
	nop			;1bce	00 	. 
	nop			;1bcf	00 	. 
	nop			;1bd0	00 	. 
	nop			;1bd1	00 	. 
	nop			;1bd2	00 	. 
	nop			;1bd3	00 	. 
	nop			;1bd4	00 	. 
	nop			;1bd5	00 	. 
	nop			;1bd6	00 	. 
	nop			;1bd7	00 	. 
	nop			;1bd8	00 	. 
	nop			;1bd9	00 	. 
	nop			;1bda	00 	. 
	ld (0c027h),a		;1bdb	32 27 c0 	2 ' . 
	ex af,af'			;1bde	08 	. 
	sbc a,d			;1bdf	9a 	. 
	rrca			;1be0	0f 	. 
	call pe,l0000h		;1be1	ec 00 00 	. . . 
	and (hl)			;1be4	a6 	. 
	nop			;1be5	00 	. 
	nop			;1be6	00 	. 
	nop			;1be7	00 	. 
l1be8h:
	ld (de),a			;1be8	12 	. 
	xor d			;1be9	aa 	. 
	ld (de),a			;1bea	12 	. 
	ld (de),a			;1beb	12 	. 
	rst 28h			;1bec	ef 	. 
	rst 28h			;1bed	ef 	. 
	ld e,d			;1bee	5a 	Z 
	rst 28h			;1bef	ef 	. 
	nop			;1bf0	00 	. 
	ld a,(hl)			;1bf1	7e 	~ 
	dec hl			;1bf2	2b 	+ 
	xor c			;1bf3	a9 	. 
	ld a,(hl)			;1bf4	7e 	~ 
	inc (hl)			;1bf5	34 	4 
	ld a,(bc)			;1bf6	0a 	. 
	inc c			;1bf7	0c 	. 
	xor d			;1bf8	aa 	. 
	nop			;1bf9	00 	. 
l1bfah:
	jr z,l1be8h		;1bfa	28 ec 	( . 
	jr l1b98h		;1bfc	18 9a 	. . 
	inc c			;1bfe	0c 	. 
	dec c			;1bff	0d 	. 
	call p,09a00h		;1c00	f4 00 9a 	. . . 
	adc a,000h		;1c03	ce 00 	. . 
	ld (0a932h),a		;1c05	32 32 a9 	2 2 . 
	jp po,0001eh		;1c08	e2 1e 00 	. . . 
	nop			;1c0b	00 	. 
	xor c			;1c0c	a9 	. 
	nop			;1c0d	00 	. 
	nop			;1c0e	00 	. 
	nop			;1c0f	00 	. 
	nop			;1c10	00 	. 
	xor d			;1c11	aa 	. 
	nop			;1c12	00 	. 
	nop			;1c13	00 	. 
	nop			;1c14	00 	. 
	nop			;1c15	00 	. 
	xor d			;1c16	aa 	. 
	nop			;1c17	00 	. 
	nop			;1c18	00 	. 
	nop			;1c19	00 	. 
	nop			;1c1a	00 	. 
	xor d			;1c1b	aa 	. 
	nop			;1c1c	00 	. 
	nop			;1c1d	00 	. 
	nop			;1c1e	00 	. 
	nop			;1c1f	00 	. 
	xor d			;1c20	aa 	. 
	nop			;1c21	00 	. 
	nop			;1c22	00 	. 
	nop			;1c23	00 	. 
	nop			;1c24	00 	. 
	xor d			;1c25	aa 	. 
	inc b			;1c26	04 	. 
	ld d,e			;1c27	53 	S 
	ld d,a			;1c28	57 	W 
	ld b,c			;1c29	41 	A 
	ld d,d			;1c2a	52 	R 
	ld b,d			;1c2b	42 	B 
	ld c,h			;1c2c	4c 	L 
	ld b,l			;1c2d	45 	E 
	jr nz,l1c50h		;1c2e	20 20 	    
	jr nz,l1c52h		;1c30	20 20 	    
	jr nz,$+34		;1c32	20 20 	    
	nop			;1c34	00 	. 
	nop			;1c35	00 	. 
	nop			;1c36	00 	. 
	nop			;1c37	00 	. 
	nop			;1c38	00 	. 
	nop			;1c39	00 	. 
	nop			;1c3a	00 	. 
	nop			;1c3b	00 	. 
	nop			;1c3c	00 	. 
	nop			;1c3d	00 	. 
	nop			;1c3e	00 	. 
	nop			;1c3f	00 	. 
	nop			;1c40	00 	. 
	nop			;1c41	00 	. 
	nop			;1c42	00 	. 
	nop			;1c43	00 	. 
	nop			;1c44	00 	. 
	nop			;1c45	00 	. 
	nop			;1c46	00 	. 
	nop			;1c47	00 	. 
	nop			;1c48	00 	. 
	nop			;1c49	00 	. 
	nop			;1c4a	00 	. 
	nop			;1c4b	00 	. 
	nop			;1c4c	00 	. 
	nop			;1c4d	00 	. 
	nop			;1c4e	00 	. 
	nop			;1c4f	00 	. 
l1c50h:
	nop			;1c50	00 	. 
	nop			;1c51	00 	. 
l1c52h:
	nop			;1c52	00 	. 
	ld (0c025h),a		;1c53	32 25 c0 	2 % . 
	ex af,af'			;1c56	08 	. 
	sbc a,d			;1c57	9a 	. 
	rrca			;1c58	0f 	. 
	inc d			;1c59	14 	. 
	nop			;1c5a	00 	. 
	nop			;1c5b	00 	. 
	xor d			;1c5c	aa 	. 
	nop			;1c5d	00 	. 
	nop			;1c5e	00 	. 
	nop			;1c5f	00 	. 
	ld (de),a			;1c60	12 	. 
	xor d			;1c61	aa 	. 
	ld (de),a			;1c62	12 	. 
	djnz l1c74h		;1c63	10 0f 	. . 
l1c65h:
	ld de,l12aah		;1c65	11 aa 12 	. . . 
	nop			;1c68	00 	. 
	jr nz,l1c65h		;1c69	20 fa 	  . 
	ld l,d			;1c6b	6a 	j 
	and e			;1c6c	a3 	. 
	sbc a,e			;1c6d	9b 	. 
	sub h			;1c6e	94 	. 
	ld (00095h),a		;1c6f	32 95 00 	2 . . 
	add hl,de			;1c72	19 	. 
	inc hl			;1c73	23 	# 
l1c74h:
	inc bc			;1c74	03 	. 
	xor d			;1c75	aa 	. 
	rst 10h			;1c76	d7 	. 
	jp c,00021h		;1c77	da 21 00 	. ! . 
	and l			;1c7a	a5 	. 
	push hl			;1c7b	e5 	. 
	ld hl,l32ceh		;1c7c	21 ce 32 	! . 2 
	sbc a,c			;1c7f	99 	. 
	nop			;1c80	00 	. 
	nop			;1c81	00 	. 
	nop			;1c82	00 	. 
	nop			;1c83	00 	. 
	xor d			;1c84	aa 	. 
	nop			;1c85	00 	. 
	nop			;1c86	00 	. 
	nop			;1c87	00 	. 
	nop			;1c88	00 	. 
	xor d			;1c89	aa 	. 
	nop			;1c8a	00 	. 
	nop			;1c8b	00 	. 
	nop			;1c8c	00 	. 
	nop			;1c8d	00 	. 
	xor d			;1c8e	aa 	. 
	nop			;1c8f	00 	. 
	nop			;1c90	00 	. 
	nop			;1c91	00 	. 
	nop			;1c92	00 	. 
	xor d			;1c93	aa 	. 
	nop			;1c94	00 	. 
	nop			;1c95	00 	. 
	nop			;1c96	00 	. 
	nop			;1c97	00 	. 
	xor d			;1c98	aa 	. 
	nop			;1c99	00 	. 
	nop			;1c9a	00 	. 
	nop			;1c9b	00 	. 
	nop			;1c9c	00 	. 
	xor d			;1c9d	aa 	. 
	inc b			;1c9e	04 	. 
	ld d,b			;1c9f	50 	P 
	ld d,e			;1ca0	53 	S 
	ld e,c			;1ca1	59 	Y 
	ld b,e			;1ca2	43 	C 
	ld c,b			;1ca3	48 	H 
	ld c,a			;1ca4	4f 	O 
	jr nz,l1cech		;1ca5	20 45 	  E 
	ld b,e			;1ca7	43 	C 
	ld c,b			;1ca8	48 	H 
	ld c,a			;1ca9	4f 	O 
	ld b,l			;1caa	45 	E 
	ld d,e			;1cab	53 	S 
	nop			;1cac	00 	. 
	nop			;1cad	00 	. 
	nop			;1cae	00 	. 
	nop			;1caf	00 	. 
	nop			;1cb0	00 	. 
	nop			;1cb1	00 	. 
	nop			;1cb2	00 	. 
	nop			;1cb3	00 	. 
	nop			;1cb4	00 	. 
	nop			;1cb5	00 	. 
	nop			;1cb6	00 	. 
	nop			;1cb7	00 	. 
	nop			;1cb8	00 	. 
	nop			;1cb9	00 	. 
	nop			;1cba	00 	. 
	nop			;1cbb	00 	. 
	nop			;1cbc	00 	. 
	nop			;1cbd	00 	. 
	nop			;1cbe	00 	. 
	nop			;1cbf	00 	. 
	nop			;1cc0	00 	. 
	nop			;1cc1	00 	. 
	nop			;1cc2	00 	. 
	nop			;1cc3	00 	. 
	nop			;1cc4	00 	. 
	nop			;1cc5	00 	. 
	nop			;1cc6	00 	. 
	nop			;1cc7	00 	. 
	nop			;1cc8	00 	. 
	nop			;1cc9	00 	. 
	nop			;1cca	00 	. 
	ld (0c021h),a		;1ccb	32 21 c0 	2 ! . 
	inc c			;1cce	0c 	. 
	sbc a,d			;1ccf	9a 	. 
	rrca			;1cd0	0f 	. 
	jr z,l1cd9h		;1cd1	28 06 	( . 
	nop			;1cd3	00 	. 
	xor d			;1cd4	aa 	. 
	nop			;1cd5	00 	. 
	nop			;1cd6	00 	. 
	nop			;1cd7	00 	. 
	ld (de),a			;1cd8	12 	. 
l1cd9h:
	xor d			;1cd9	aa 	. 
	ld (de),a			;1cda	12 	. 
	ld (de),a			;1cdb	12 	. 
	ld (de),a			;1cdc	12 	. 
	ld (de),a			;1cdd	12 	. 
	xor d			;1cde	aa 	. 
	ld (de),a			;1cdf	12 	. 
	nop			;1ce0	00 	. 
	ld a,e			;1ce1	7b 	{ 
	ld a,b			;1ce2	78 	x 
	xor d			;1ce3	aa 	. 
	ld a,e			;1ce4	7b 	{ 
	ld a,h			;1ce5	7c 	| 
	ld a,h			;1ce6	7c 	| 
sub_1ce7h:
	ld a,(hl)			;1ce7	7e 	~ 
	xor d			;1ce8	aa 	. 
	nop			;1ce9	00 	. 
sub_1ceah:
	and d			;1cea	a2 	. 
	nop			;1ceb	00 	. 
l1cech:
	rrca			;1cec	0f 	. 
	and (hl)			;1ced	a6 	. 
	xor b			;1cee	a8 	. 
	nop			;1cef	00 	. 
	ld (de),a			;1cf0	12 	. 
	nop			;1cf1	00 	. 
	xor c			;1cf2	a9 	. 
	push hl			;1cf3	e5 	. 
	ld hl,l32ceh		;1cf4	21 ce 32 	! . 2 
	sbc a,c			;1cf7	99 	. 
	nop			;1cf8	00 	. 
	nop			;1cf9	00 	. 
	nop			;1cfa	00 	. 
	nop			;1cfb	00 	. 
	xor d			;1cfc	aa 	. 
	nop			;1cfd	00 	. 
	nop			;1cfe	00 	. 
	nop			;1cff	00 	. 
	nop			;1d00	00 	. 
	xor d			;1d01	aa 	. 
	nop			;1d02	00 	. 
	nop			;1d03	00 	. 
	nop			;1d04	00 	. 
	nop			;1d05	00 	. 
	xor d			;1d06	aa 	. 
	nop			;1d07	00 	. 
	nop			;1d08	00 	. 
	nop			;1d09	00 	. 
	nop			;1d0a	00 	. 
	xor d			;1d0b	aa 	. 
	nop			;1d0c	00 	. 
	nop			;1d0d	00 	. 
	nop			;1d0e	00 	. 
	nop			;1d0f	00 	. 
	xor d			;1d10	aa 	. 
	nop			;1d11	00 	. 
	nop			;1d12	00 	. 
	nop			;1d13	00 	. 
	nop			;1d14	00 	. 
	xor d			;1d15	aa 	. 
	dec b			;1d16	05 	. 
	ld d,e			;1d17	53 	S 
	ld c,c			;1d18	49 	I 
	ld c,(hl)			;1d19	4e 	N 
	ld b,a			;1d1a	47 	G 
	ld c,h			;1d1b	4c 	L 
	ld b,l			;1d1c	45 	E 
	jr nz,l1d63h		;1d1d	20 44 	  D 
	ld b,l			;1d1f	45 	E 
	ld c,h			;1d20	4c 	L 
	ld b,c			;1d21	41 	A 
	ld e,c			;1d22	59 	Y 
	jr nz,l1d25h		;1d23	20 00 	  . 
l1d25h:
	nop			;1d25	00 	. 
	nop			;1d26	00 	. 
	nop			;1d27	00 	. 
	nop			;1d28	00 	. 
	nop			;1d29	00 	. 
	nop			;1d2a	00 	. 
	nop			;1d2b	00 	. 
	nop			;1d2c	00 	. 
	nop			;1d2d	00 	. 
	nop			;1d2e	00 	. 
	nop			;1d2f	00 	. 
	nop			;1d30	00 	. 
	nop			;1d31	00 	. 
	nop			;1d32	00 	. 
	nop			;1d33	00 	. 
	nop			;1d34	00 	. 
	nop			;1d35	00 	. 
	nop			;1d36	00 	. 
	nop			;1d37	00 	. 
	nop			;1d38	00 	. 
	nop			;1d39	00 	. 
	nop			;1d3a	00 	. 
	nop			;1d3b	00 	. 
	nop			;1d3c	00 	. 
	nop			;1d3d	00 	. 
	nop			;1d3e	00 	. 
	nop			;1d3f	00 	. 
	nop			;1d40	00 	. 
	nop			;1d41	00 	. 
	nop			;1d42	00 	. 
	ld (0c027h),a		;1d43	32 27 c0 	2 ' . 
	adc a,05ah		;1d46	ce 5a 	. Z 
	ex de,hl			;1d48	eb 	. 
	ret pe			;1d49	e8 	. 
	nop			;1d4a	00 	. 
	nop			;1d4b	00 	. 
	and l			;1d4c	a5 	. 
	nop			;1d4d	00 	. 
	nop			;1d4e	00 	. 
	nop			;1d4f	00 	. 
	ld (de),a			;1d50	12 	. 
	xor d			;1d51	aa 	. 
	ld (de),a			;1d52	12 	. 
	rst 28h			;1d53	ef 	. 
	rst 28h			;1d54	ef 	. 
	rst 28h			;1d55	ef 	. 
	ld d,(hl)			;1d56	56 	V 
	rst 28h			;1d57	ef 	. 
	nop			;1d58	00 	. 
	ld l,h			;1d59	6c 	l 
	ld l,h			;1d5a	6c 	l 
	xor c			;1d5b	a9 	. 
	ld h,e			;1d5c	63 	c 
	ld h,e			;1d5d	63 	c 
	ld h,e			;1d5e	63 	c 
	ld h,e			;1d5f	63 	c 
	ld d,l			;1d60	55 	U 
	nop			;1d61	00 	. 
	pop af			;1d62	f1 	. 
l1d63h:
	pop af			;1d63	f1 	. 
	pop af			;1d64	f1 	. 
	ld d,(hl)			;1d65	56 	V 
	pop af			;1d66	f1 	. 
	pop af			;1d67	f1 	. 
	pop af			;1d68	f1 	. 
	nop			;1d69	00 	. 
	sub l			;1d6a	95 	. 
	ld a,(bc)			;1d6b	0a 	. 
	ld a,(bc)			;1d6c	0a 	. 
	ld a,(bc)			;1d6d	0a 	. 
	ld a,(bc)			;1d6e	0a 	. 
	xor d			;1d6f	aa 	. 
	ld a,(bc)			;1d70	0a 	. 
	ld a,(bc)			;1d71	0a 	. 
	nop			;1d72	00 	. 
	nop			;1d73	00 	. 
	xor d			;1d74	aa 	. 
	nop			;1d75	00 	. 
	nop			;1d76	00 	. 
	nop			;1d77	00 	. 
	nop			;1d78	00 	. 
	xor d			;1d79	aa 	. 
	nop			;1d7a	00 	. 
	nop			;1d7b	00 	. 
	nop			;1d7c	00 	. 
	nop			;1d7d	00 	. 
	xor d			;1d7e	aa 	. 
	nop			;1d7f	00 	. 
	nop			;1d80	00 	. 
	nop			;1d81	00 	. 
	nop			;1d82	00 	. 
	xor d			;1d83	aa 	. 
	nop			;1d84	00 	. 
	nop			;1d85	00 	. 
	nop			;1d86	00 	. 
	nop			;1d87	00 	. 
	xor d			;1d88	aa 	. 
	nop			;1d89	00 	. 
	nop			;1d8a	00 	. 
	nop			;1d8b	00 	. 
	nop			;1d8c	00 	. 
	xor d			;1d8d	aa 	. 
	dec b			;1d8e	05 	. 
	ld b,h			;1d8f	44 	D 
	ld c,a			;1d90	4f 	O 
	ld d,l			;1d91	55 	U 
	ld b,d			;1d92	42 	B 
	ld c,h			;1d93	4c 	L 
	ld b,l			;1d94	45 	E 
	jr nz,l1ddbh		;1d95	20 44 	  D 
	ld b,l			;1d97	45 	E 
	ld c,h			;1d98	4c 	L 
	ld b,c			;1d99	41 	A 
	ld e,c			;1d9a	59 	Y 
	jr nz,l1d9dh		;1d9b	20 00 	  . 
l1d9dh:
	nop			;1d9d	00 	. 
	nop			;1d9e	00 	. 
	nop			;1d9f	00 	. 
	nop			;1da0	00 	. 
	nop			;1da1	00 	. 
	nop			;1da2	00 	. 
	nop			;1da3	00 	. 
	nop			;1da4	00 	. 
	nop			;1da5	00 	. 
	nop			;1da6	00 	. 
	nop			;1da7	00 	. 
	nop			;1da8	00 	. 
	nop			;1da9	00 	. 
	nop			;1daa	00 	. 
	nop			;1dab	00 	. 
	nop			;1dac	00 	. 
	nop			;1dad	00 	. 
	nop			;1dae	00 	. 
	nop			;1daf	00 	. 
	nop			;1db0	00 	. 
	nop			;1db1	00 	. 
	nop			;1db2	00 	. 
	nop			;1db3	00 	. 
	nop			;1db4	00 	. 
	nop			;1db5	00 	. 
	nop			;1db6	00 	. 
	nop			;1db7	00 	. 
	nop			;1db8	00 	. 
	nop			;1db9	00 	. 
	nop			;1dba	00 	. 
	ld (0c025h),a		;1dbb	32 25 c0 	2 % . 
	adc a,05ah		;1dbe	ce 5a 	. Z 
	jp po,000e2h		;1dc0	e2 e2 00 	. . . 
	nop			;1dc3	00 	. 
	and l			;1dc4	a5 	. 
	nop			;1dc5	00 	. 
	nop			;1dc6	00 	. 
	nop			;1dc7	00 	. 
	ld (de),a			;1dc8	12 	. 
	xor d			;1dc9	aa 	. 
	ld (de),a			;1dca	12 	. 
	ld a,(bc)			;1dcb	0a 	. 
	rst 28h			;1dcc	ef 	. 
	rst 28h			;1dcd	ef 	. 
	ld e,d			;1dce	5a 	Z 
	rst 28h			;1dcf	ef 	. 
	nop			;1dd0	00 	. 
	inc bc			;1dd1	03 	. 
	dec (hl)			;1dd2	35 	5 
	xor c			;1dd3	a9 	. 
	ld h,e			;1dd4	63 	c 
	ld h,e			;1dd5	63 	c 
	ld h,e			;1dd6	63 	c 
	ld h,e			;1dd7	63 	c 
	ld d,l			;1dd8	55 	U 
	nop			;1dd9	00 	. 
	pop af			;1dda	f1 	. 
l1ddbh:
	pop af			;1ddb	f1 	. 
	pop af			;1ddc	f1 	. 
	ld d,(hl)			;1ddd	56 	V 
	pop af			;1dde	f1 	. 
	pop af			;1ddf	f1 	. 
	pop af			;1de0	f1 	. 
	nop			;1de1	00 	. 
	sub l			;1de2	95 	. 
	dec bc			;1de3	0b 	. 
	dec bc			;1de4	0b 	. 
	dec bc			;1de5	0b 	. 
	dec bc			;1de6	0b 	. 
	xor d			;1de7	aa 	. 
	dec bc			;1de8	0b 	. 
	rrca			;1de9	0f 	. 
	nop			;1dea	00 	. 
	adc a,06ah		;1deb	ce 6a 	. j 
	ld (l0000h),a		;1ded	32 00 00 	2 . . 
	nop			;1df0	00 	. 
	xor d			;1df1	aa 	. 
	nop			;1df2	00 	. 
	nop			;1df3	00 	. 
	nop			;1df4	00 	. 
	nop			;1df5	00 	. 
	xor d			;1df6	aa 	. 
	nop			;1df7	00 	. 
	nop			;1df8	00 	. 
	nop			;1df9	00 	. 
	nop			;1dfa	00 	. 
	xor d			;1dfb	aa 	. 
	nop			;1dfc	00 	. 
	nop			;1dfd	00 	. 
	nop			;1dfe	00 	. 
	nop			;1dff	00 	. 
	xor d			;1e00	aa 	. 
	dec b			;1e01	05 	. 
	ld d,b			;1e02	50 	P 
	ld b,c			;1e03	41 	A 
	ld c,(hl)			;1e04	4e 	N 
	jr nz,l1e4bh		;1e05	20 44 	  D 
	ld b,l			;1e07	45 	E 
	ld c,h			;1e08	4c 	L 
	ld b,c			;1e09	41 	A 
	ld e,c			;1e0a	59 	Y 
	ld d,e			;1e0b	53 	S 
	jr nz,l1e2eh		;1e0c	20 20 	    
	jr nz,l1e10h		;1e0e	20 00 	  . 
l1e10h:
	nop			;1e10	00 	. 
	nop			;1e11	00 	. 
	nop			;1e12	00 	. 
	nop			;1e13	00 	. 
	nop			;1e14	00 	. 
	nop			;1e15	00 	. 
	nop			;1e16	00 	. 
	nop			;1e17	00 	. 
	nop			;1e18	00 	. 
	nop			;1e19	00 	. 
	nop			;1e1a	00 	. 
	nop			;1e1b	00 	. 
	nop			;1e1c	00 	. 
	nop			;1e1d	00 	. 
	nop			;1e1e	00 	. 
	nop			;1e1f	00 	. 
	nop			;1e20	00 	. 
	nop			;1e21	00 	. 
	nop			;1e22	00 	. 
	nop			;1e23	00 	. 
	nop			;1e24	00 	. 
	nop			;1e25	00 	. 
	nop			;1e26	00 	. 
	nop			;1e27	00 	. 
	nop			;1e28	00 	. 
	nop			;1e29	00 	. 
	nop			;1e2a	00 	. 
	nop			;1e2b	00 	. 
	nop			;1e2c	00 	. 
	nop			;1e2d	00 	. 
l1e2eh:
	ld (0c027h),a		;1e2e	32 27 c0 	2 ' . 
	adc a,05ah		;1e31	ce 5a 	. Z 
	defb 0edh;next byte illegal after ed		;1e33	ed 	. 
	adc a,000h		;1e34	ce 00 	. . 
	nop			;1e36	00 	. 
	and l			;1e37	a5 	. 
	nop			;1e38	00 	. 
	nop			;1e39	00 	. 
	nop			;1e3a	00 	. 
	ld (de),a			;1e3b	12 	. 
	xor d			;1e3c	aa 	. 
	ld (de),a			;1e3d	12 	. 
	rst 28h			;1e3e	ef 	. 
	rst 28h			;1e3f	ef 	. 
	rst 28h			;1e40	ef 	. 
	ld d,(hl)			;1e41	56 	V 
	rst 28h			;1e42	ef 	. 
	nop			;1e43	00 	. 
	adc a,c			;1e44	89 	. 
	ld d,l			;1e45	55 	U 
	xor c			;1e46	a9 	. 
	ld h,e			;1e47	63 	c 
	ld h,e			;1e48	63 	c 
	ld h,e			;1e49	63 	c 
	ld h,e			;1e4a	63 	c 
l1e4bh:
	ld d,l			;1e4b	55 	U 
	nop			;1e4c	00 	. 
	pop af			;1e4d	f1 	. 
	pop af			;1e4e	f1 	. 
	pop af			;1e4f	f1 	. 
	ld d,(hl)			;1e50	56 	V 
	pop af			;1e51	f1 	. 
	pop af			;1e52	f1 	. 
	pop af			;1e53	f1 	. 
	nop			;1e54	00 	. 
	sub l			;1e55	95 	. 
	rrca			;1e56	0f 	. 
	rrca			;1e57	0f 	. 
	rrca			;1e58	0f 	. 
	rrca			;1e59	0f 	. 
	xor d			;1e5a	aa 	. 
	rrca			;1e5b	0f 	. 
	rrca			;1e5c	0f 	. 
	nop			;1e5d	00 	. 
	adc a,06ah		;1e5e	ce 6a 	. j 
	ld (l0000h),a		;1e60	32 00 00 	2 . . 
	nop			;1e63	00 	. 
	xor d			;1e64	aa 	. 
	nop			;1e65	00 	. 
	nop			;1e66	00 	. 
	nop			;1e67	00 	. 
	nop			;1e68	00 	. 
	xor d			;1e69	aa 	. 
	nop			;1e6a	00 	. 
	nop			;1e6b	00 	. 
	nop			;1e6c	00 	. 
	nop			;1e6d	00 	. 
	xor d			;1e6e	aa 	. 
	nop			;1e6f	00 	. 
	nop			;1e70	00 	. 
	nop			;1e71	00 	. 
	nop			;1e72	00 	. 
	xor d			;1e73	aa 	. 
	nop			;1e74	00 	. 
	nop			;1e75	00 	. 
	nop			;1e76	00 	. 
	nop			;1e77	00 	. 
	xor d			;1e78	aa 	. 
	dec b			;1e79	05 	. 
	ld b,e			;1e7a	43 	C 
	ld c,c			;1e7b	49 	I 
	ld d,d			;1e7c	52 	R 
	ld b,e			;1e7d	43 	C 
	ld d,l			;1e7e	55 	U 
	ld c,h			;1e7f	4c 	L 
	ld b,c			;1e80	41 	A 
	ld d,d			;1e81	52 	R 
	jr nz,l1ec8h		;1e82	20 44 	  D 
	ld c,h			;1e84	4c 	L 
	ld e,c			;1e85	59 	Y 
	ld d,e			;1e86	53 	S 
	nop			;1e87	00 	. 
	nop			;1e88	00 	. 
	nop			;1e89	00 	. 
	nop			;1e8a	00 	. 
	nop			;1e8b	00 	. 
	nop			;1e8c	00 	. 
	nop			;1e8d	00 	. 
	nop			;1e8e	00 	. 
	nop			;1e8f	00 	. 
	nop			;1e90	00 	. 
	nop			;1e91	00 	. 
	nop			;1e92	00 	. 
	nop			;1e93	00 	. 
	nop			;1e94	00 	. 
	nop			;1e95	00 	. 
	nop			;1e96	00 	. 
	nop			;1e97	00 	. 
	nop			;1e98	00 	. 
	nop			;1e99	00 	. 
	nop			;1e9a	00 	. 
	nop			;1e9b	00 	. 
	nop			;1e9c	00 	. 
	nop			;1e9d	00 	. 
	nop			;1e9e	00 	. 
	nop			;1e9f	00 	. 
	nop			;1ea0	00 	. 
	nop			;1ea1	00 	. 
	nop			;1ea2	00 	. 
	nop			;1ea3	00 	. 
	nop			;1ea4	00 	. 
	nop			;1ea5	00 	. 
	ld (0c027h),a		;1ea6	32 27 c0 	2 ' . 
	ret m			;1ea9	f8 	. 
	ld e,d			;1eaa	5a 	Z 
	call pe,000ceh		;1eab	ec ce 00 	. . . 
	nop			;1eae	00 	. 
	and l			;1eaf	a5 	. 
l1eb0h:
	nop			;1eb0	00 	. 
	nop			;1eb1	00 	. 
	nop			;1eb2	00 	. 
	ld (de),a			;1eb3	12 	. 
	xor d			;1eb4	aa 	. 
	ld (de),a			;1eb5	12 	. 
	inc c			;1eb6	0c 	. 
	rst 28h			;1eb7	ef 	. 
	rst 28h			;1eb8	ef 	. 
	ld e,d			;1eb9	5a 	Z 
	rst 28h			;1eba	ef 	. 
	nop			;1ebb	00 	. 
	sbc a,b			;1ebc	98 	. 
	ld (hl),d			;1ebd	72 	r 
	xor c			;1ebe	a9 	. 
	ld b,b			;1ebf	40 	@ 
	ld h,e			;1ec0	63 	c 
	ld h,e			;1ec1	63 	c 
	ld h,e			;1ec2	63 	c 
	ld d,(hl)			;1ec3	56 	V 
	nop			;1ec4	00 	. 
	pop af			;1ec5	f1 	. 
	pop af			;1ec6	f1 	. 
	pop af			;1ec7	f1 	. 
l1ec8h:
	ld d,(hl)			;1ec8	56 	V 
	pop af			;1ec9	f1 	. 
	pop af			;1eca	f1 	. 
	pop af			;1ecb	f1 	. 
	nop			;1ecc	00 	. 
	sub l			;1ecd	95 	. 
	rrca			;1ece	0f 	. 
	rrca			;1ecf	0f 	. 
	rrca			;1ed0	0f 	. 
	rrca			;1ed1	0f 	. 
	xor d			;1ed2	aa 	. 
	rrca			;1ed3	0f 	. 
	rrca			;1ed4	0f 	. 
	nop			;1ed5	00 	. 
	nop			;1ed6	00 	. 
	xor d			;1ed7	aa 	. 
	ld (000ceh),a		;1ed8	32 ce 00 	2 . . 
	nop			;1edb	00 	. 
	and (hl)			;1edc	a6 	. 
	nop			;1edd	00 	. 
	nop			;1ede	00 	. 
	nop			;1edf	00 	. 
	nop			;1ee0	00 	. 
	xor d			;1ee1	aa 	. 
	nop			;1ee2	00 	. 
	nop			;1ee3	00 	. 
	nop			;1ee4	00 	. 
	nop			;1ee5	00 	. 
	xor d			;1ee6	aa 	. 
	nop			;1ee7	00 	. 
	nop			;1ee8	00 	. 
	nop			;1ee9	00 	. 
	nop			;1eea	00 	. 
	xor d			;1eeb	aa 	. 
	nop			;1eec	00 	. 
	nop			;1eed	00 	. 
	nop			;1eee	00 	. 
	nop			;1eef	00 	. 
	xor d			;1ef0	aa 	. 
	dec b			;1ef1	05 	. 
	inc (hl)			;1ef2	34 	4 
	jr nz,l1f4bh		;1ef3	20 56 	  V 
	ld c,a			;1ef5	4f 	O 
	ld c,c			;1ef6	49 	I 
	ld b,e			;1ef7	43 	C 
	ld b,l			;1ef8	45 	E 
	jr nz,l1f3fh		;1ef9	20 44 	  D 
	ld b,l			;1efb	45 	E 
	ld c,h			;1efc	4c 	L 
	ld b,c			;1efd	41 	A 
	ld e,c			;1efe	59 	Y 
	nop			;1eff	00 	. 
	nop			;1f00	00 	. 
	nop			;1f01	00 	. 
	nop			;1f02	00 	. 
	nop			;1f03	00 	. 
	nop			;1f04	00 	. 
	nop			;1f05	00 	. 
	nop			;1f06	00 	. 
	nop			;1f07	00 	. 
	nop			;1f08	00 	. 
	nop			;1f09	00 	. 
	nop			;1f0a	00 	. 
	nop			;1f0b	00 	. 
	nop			;1f0c	00 	. 
	nop			;1f0d	00 	. 
	nop			;1f0e	00 	. 
	nop			;1f0f	00 	. 
	nop			;1f10	00 	. 
	nop			;1f11	00 	. 
	nop			;1f12	00 	. 
	nop			;1f13	00 	. 
	nop			;1f14	00 	. 
	nop			;1f15	00 	. 
	nop			;1f16	00 	. 
	nop			;1f17	00 	. 
	nop			;1f18	00 	. 
	nop			;1f19	00 	. 
	nop			;1f1a	00 	. 
	nop			;1f1b	00 	. 
	nop			;1f1c	00 	. 
	nop			;1f1d	00 	. 
	ld (0c026h),a		;1f1e	32 26 c0 	2 & . 
	ret c			;1f21	d8 	. 
	ld e,d			;1f22	5a 	Z 
	rst 28h			;1f23	ef 	. 
	adc a,000h		;1f24	ce 00 	. . 
	nop			;1f26	00 	. 
	and l			;1f27	a5 	. 
	nop			;1f28	00 	. 
	nop			;1f29	00 	. 
	nop			;1f2a	00 	. 
	ld (de),a			;1f2b	12 	. 
	xor d			;1f2c	aa 	. 
	ld (de),a			;1f2d	12 	. 
	ld (de),a			;1f2e	12 	. 
	ld (de),a			;1f2f	12 	. 
	rst 28h			;1f30	ef 	. 
	ld l,d			;1f31	6a 	j 
	rst 28h			;1f32	ef 	. 
	nop			;1f33	00 	. 
	sub d			;1f34	92 	. 
	inc a			;1f35	3c 	< 
	xor c			;1f36	a9 	. 
	ld e,(hl)			;1f37	5e 	^ 
	ld l,l			;1f38	6d 	m 
	ld h,e			;1f39	63 	c 
	ld h,e			;1f3a	63 	c 
	ld e,d			;1f3b	5a 	Z 
	nop			;1f3c	00 	. 
	pop af			;1f3d	f1 	. 
	pop af			;1f3e	f1 	. 
l1f3fh:
	pop af			;1f3f	f1 	. 
	ld d,(hl)			;1f40	56 	V 
	pop af			;1f41	f1 	. 
	pop af			;1f42	f1 	. 
	pop af			;1f43	f1 	. 
	nop			;1f44	00 	. 
	sub l			;1f45	95 	. 
	rrca			;1f46	0f 	. 
	rrca			;1f47	0f 	. 
	rrca			;1f48	0f 	. 
	rrca			;1f49	0f 	. 
	xor d			;1f4a	aa 	. 
l1f4bh:
	rrca			;1f4b	0f 	. 
	rrca			;1f4c	0f 	. 
	nop			;1f4d	00 	. 
	ld (l32aah),a		;1f4e	32 aa 32 	2 . 2 
	adc a,0ceh		;1f51	ce ce 	. . 
	nop			;1f53	00 	. 
	sub (hl)			;1f54	96 	. 
	nop			;1f55	00 	. 
	nop			;1f56	00 	. 
	nop			;1f57	00 	. 
	nop			;1f58	00 	. 
	xor d			;1f59	aa 	. 
	nop			;1f5a	00 	. 
	nop			;1f5b	00 	. 
	nop			;1f5c	00 	. 
	nop			;1f5d	00 	. 
	xor d			;1f5e	aa 	. 
	nop			;1f5f	00 	. 
	nop			;1f60	00 	. 
	nop			;1f61	00 	. 
	nop			;1f62	00 	. 
	xor d			;1f63	aa 	. 
	nop			;1f64	00 	. 
	nop			;1f65	00 	. 
	nop			;1f66	00 	. 
	nop			;1f67	00 	. 
	xor d			;1f68	aa 	. 
	dec b			;1f69	05 	. 
	ld d,c			;1f6a	51 	Q 
	ld d,l			;1f6b	55 	U 
	ld b,c			;1f6c	41 	A 
	ld d,h			;1f6d	54 	T 
	ld d,d			;1f6e	52 	R 
	ld c,a			;1f6f	4f 	O 
	jr nz,l1fb6h		;1f70	20 44 	  D 
	ld b,l			;1f72	45 	E 
	ld c,h			;1f73	4c 	L 
	ld b,c			;1f74	41 	A 
	ld e,c			;1f75	59 	Y 
	ld d,e			;1f76	53 	S 
	nop			;1f77	00 	. 
	nop			;1f78	00 	. 
	nop			;1f79	00 	. 
	nop			;1f7a	00 	. 
	nop			;1f7b	00 	. 
	nop			;1f7c	00 	. 
	nop			;1f7d	00 	. 
	nop			;1f7e	00 	. 
	nop			;1f7f	00 	. 
	nop			;1f80	00 	. 
	nop			;1f81	00 	. 
	nop			;1f82	00 	. 
	nop			;1f83	00 	. 
	nop			;1f84	00 	. 
	nop			;1f85	00 	. 
	nop			;1f86	00 	. 
	nop			;1f87	00 	. 
	nop			;1f88	00 	. 
	nop			;1f89	00 	. 
	nop			;1f8a	00 	. 
	nop			;1f8b	00 	. 
	nop			;1f8c	00 	. 
	nop			;1f8d	00 	. 
	nop			;1f8e	00 	. 
	nop			;1f8f	00 	. 
	nop			;1f90	00 	. 
	nop			;1f91	00 	. 
	nop			;1f92	00 	. 
	nop			;1f93	00 	. 
	nop			;1f94	00 	. 
	nop			;1f95	00 	. 
	ld (0c02ah),a		;1f96	32 2a c0 	2 * . 
	defb 0ddh,05ah,0e4h	;illegal sequence		;1f99	dd 5a e4 	. Z . 
	push de			;1f9c	d5 	. 
	nop			;1f9d	00 	. 
	nop			;1f9e	00 	. 
	and l			;1f9f	a5 	. 
	nop			;1fa0	00 	. 
	nop			;1fa1	00 	. 
	nop			;1fa2	00 	. 
	ld (bc),a			;1fa3	02 	. 
	xor d			;1fa4	aa 	. 
	ld (bc),a			;1fa5	02 	. 
	ld (de),a			;1fa6	12 	. 
	ld (de),a			;1fa7	12 	. 
	rst 28h			;1fa8	ef 	. 
	ld l,d			;1fa9	6a 	j 
	rst 28h			;1faa	ef 	. 
	nop			;1fab	00 	. 
	sub d			;1fac	92 	. 
	sub b			;1fad	90 	. 
	xor c			;1fae	a9 	. 
	ld e,(hl)			;1faf	5e 	^ 
	ld e,l			;1fb0	5d 	] 
	ld h,e			;1fb1	63 	c 
	ld h,e			;1fb2	63 	c 
	ld e,d			;1fb3	5a 	Z 
	nop			;1fb4	00 	. 
	pop af			;1fb5	f1 	. 
l1fb6h:
	pop af			;1fb6	f1 	. 
	pop af			;1fb7	f1 	. 
	ld d,(hl)			;1fb8	56 	V 
	pop af			;1fb9	f1 	. 
	pop af			;1fba	f1 	. 
	pop af			;1fbb	f1 	. 
	nop			;1fbc	00 	. 
	sub l			;1fbd	95 	. 
	rrca			;1fbe	0f 	. 
	rrca			;1fbf	0f 	. 
	rrca			;1fc0	0f 	. 
	rrca			;1fc1	0f 	. 
	xor d			;1fc2	aa 	. 
	rrca			;1fc3	0f 	. 
	rrca			;1fc4	0f 	. 
	nop			;1fc5	00 	. 
	adc a,06ah		;1fc6	ce 6a 	. j 
	ld (00cf4h),a		;1fc8	32 f4 0c 	2 . . 
	nop			;1fcb	00 	. 
	and (hl)			;1fcc	a6 	. 
	nop			;1fcd	00 	. 
	nop			;1fce	00 	. 
	nop			;1fcf	00 	. 
	nop			;1fd0	00 	. 
	xor d			;1fd1	aa 	. 
	nop			;1fd2	00 	. 
	nop			;1fd3	00 	. 
	nop			;1fd4	00 	. 
	nop			;1fd5	00 	. 
	xor d			;1fd6	aa 	. 
	nop			;1fd7	00 	. 
	nop			;1fd8	00 	. 
	nop			;1fd9	00 	. 
	nop			;1fda	00 	. 
	xor d			;1fdb	aa 	. 
	nop			;1fdc	00 	. 
	nop			;1fdd	00 	. 
	nop			;1fde	00 	. 
	nop			;1fdf	00 	. 
	xor d			;1fe0	aa 	. 
	dec b			;1fe1	05 	. 
	ld b,(hl)			;1fe2	46 	F 
	ld c,c			;1fe3	49 	I 
	ld c,h			;1fe4	4c 	L 
	ld d,h			;1fe5	54 	T 
	ld b,l			;1fe6	45 	E 
	ld d,d			;1fe7	52 	R 
	ld b,l			;1fe8	45 	E 
	ld b,h			;1fe9	44 	D 
	jr nz,$+70		;1fea	20 44 	  D 
	ld c,h			;1fec	4c 	L 
	ld e,c			;1fed	59 	Y 
	ld d,e			;1fee	53 	S 
	nop			;1fef	00 	. 
	nop			;1ff0	00 	. 
	nop			;1ff1	00 	. 
	nop			;1ff2	00 	. 
	nop			;1ff3	00 	. 
	nop			;1ff4	00 	. 
	nop			;1ff5	00 	. 
	nop			;1ff6	00 	. 
	nop			;1ff7	00 	. 
	nop			;1ff8	00 	. 
	nop			;1ff9	00 	. 
	nop			;1ffa	00 	. 
	nop			;1ffb	00 	. 
	nop			;1ffc	00 	. 
	nop			;1ffd	00 	. 
	nop			;1ffe	00 	. 
	nop			;1fff	00 	. 
	nop			;2000	00 	. 
	nop			;2001	00 	. 
	nop			;2002	00 	. 
	nop			;2003	00 	. 
	nop			;2004	00 	. 
	nop			;2005	00 	. 
	nop			;2006	00 	. 
	nop			;2007	00 	. 
	nop			;2008	00 	. 
	nop			;2009	00 	. 
	nop			;200a	00 	. 
	nop			;200b	00 	. 
	nop			;200c	00 	. 
	nop			;200d	00 	. 
	ld (0c033h),a		;200e	32 33 c0 	2 3 . 
	jp po,0ce5ah		;2011	e2 5a ce 	. Z . 
	adc a,000h		;2014	ce 00 	. . 
	nop			;2016	00 	. 
	and l			;2017	a5 	. 
	nop			;2018	00 	. 
	nop			;2019	00 	. 
	nop			;201a	00 	. 
	add hl,bc			;201b	09 	. 
	xor d			;201c	aa 	. 
	inc c			;201d	0c 	. 
	rrca			;201e	0f 	. 
	ld (de),a			;201f	12 	. 
	ld (de),a			;2020	12 	. 
	xor d			;2021	aa 	. 
	ld (de),a			;2022	12 	. 
	nop			;2023	00 	. 
	dec (hl)			;2024	35 	5 
	ld d,e			;2025	53 	S 
	xor d			;2026	aa 	. 
	ld h,a			;2027	67 	g 
	ld (hl),a			;2028	77 	w 
	add a,a			;2029	87 	. 
	sub a			;202a	97 	. 
	xor d			;202b	aa 	. 
	nop			;202c	00 	. 
	pop af			;202d	f1 	. 
	call p,056f8h		;202e	f4 f8 56 	. . V 
	rst 38h			;2031	ff 	. 
	dec b			;2032	05 	. 
	rrca			;2033	0f 	. 
	nop			;2034	00 	. 
	xor c			;2035	a9 	. 
	jp p,0f9f4h		;2036	f2 f4 f9 	. . . 
	rst 38h			;2039	ff 	. 
	ld d,l			;203a	55 	U 
	ld b,00fh		;203b	06 0f 	. . 
	nop			;203d	00 	. 
	adc a,06ah		;203e	ce 6a 	. j 
	jp po,l07f9h		;2040	e2 f9 07 	. . . 
	ld e,0a5h		;2043	1e a5 	. . 
	ld (l0000h),a		;2045	32 00 00 	2 . . 
	nop			;2048	00 	. 
	xor d			;2049	aa 	. 
	nop			;204a	00 	. 
	nop			;204b	00 	. 
	nop			;204c	00 	. 
	nop			;204d	00 	. 
	xor d			;204e	aa 	. 
	nop			;204f	00 	. 
	nop			;2050	00 	. 
	nop			;2051	00 	. 
	nop			;2052	00 	. 
	xor d			;2053	aa 	. 
	nop			;2054	00 	. 
	nop			;2055	00 	. 
	nop			;2056	00 	. 
	nop			;2057	00 	. 
	xor d			;2058	aa 	. 
	ld b,04dh		;2059	06 4d 	. M 
	ld b,c			;205b	41 	A 
	ld c,d			;205c	4a 	J 
	ld c,a			;205d	4f 	O 
	ld d,d			;205e	52 	R 
	jr nz,l20a4h		;205f	20 43 	  C 
	ld c,b			;2061	48 	H 
	ld c,a			;2062	4f 	O 
	ld d,d			;2063	52 	R 
	ld b,h			;2064	44 	D 
	jr nz,$+34		;2065	20 20 	    
	nop			;2067	00 	. 
	nop			;2068	00 	. 
	nop			;2069	00 	. 
	nop			;206a	00 	. 
	nop			;206b	00 	. 
	nop			;206c	00 	. 
	nop			;206d	00 	. 
	nop			;206e	00 	. 
	nop			;206f	00 	. 
	nop			;2070	00 	. 
	nop			;2071	00 	. 
	nop			;2072	00 	. 
	nop			;2073	00 	. 
	nop			;2074	00 	. 
	nop			;2075	00 	. 
	nop			;2076	00 	. 
	nop			;2077	00 	. 
	nop			;2078	00 	. 
	nop			;2079	00 	. 
	nop			;207a	00 	. 
	nop			;207b	00 	. 
	nop			;207c	00 	. 
	nop			;207d	00 	. 
	nop			;207e	00 	. 
	nop			;207f	00 	. 
	nop			;2080	00 	. 
	nop			;2081	00 	. 
	nop			;2082	00 	. 
	nop			;2083	00 	. 
	nop			;2084	00 	. 
	nop			;2085	00 	. 
	ld (0c027h),a		;2086	32 27 c0 	2 ' . 
	adc a,05ah		;2089	ce 5a 	. Z 
	adc a,00bh		;208b	ce 0b 	. . 
	dec bc			;208d	0b 	. 
	nop			;208e	00 	. 
	xor c			;208f	a9 	. 
	nop			;2090	00 	. 
	nop			;2091	00 	. 
	nop			;2092	00 	. 
	ld a,(bc)			;2093	0a 	. 
	xor d			;2094	aa 	. 
	inc c			;2095	0c 	. 
	inc c			;2096	0c 	. 
	ld (de),a			;2097	12 	. 
	ld c,0aah		;2098	0e aa 	. . 
	ld b,000h		;209a	06 00 	. . 
	rst 18h			;209c	df 	. 
	and 05ah		;209d	e6 5a 	. Z 
	ex de,hl			;209f	eb 	. 
	rst 28h			;20a0	ef 	. 
	jp p,055f7h		;20a1	f2 f7 55 	. . U 
l20a4h:
	nop			;20a4	00 	. 
	ld e,e			;20a5	5b 	[ 
	ld e,(hl)			;20a6	5e 	^ 
	ld h,c			;20a7	61 	a 
	xor d			;20a8	aa 	. 
	ld h,c			;20a9	61 	a 
	ld h,c			;20aa	61 	a 
	ld h,c			;20ab	61 	a 
	nop			;20ac	00 	. 
	xor d			;20ad	aa 	. 
	sbc a,d			;20ae	9a 	. 
	cp e			;20af	bb 	. 
	jp c,055fah		;20b0	da fa 55 	. . U 
	ld a,(de)			;20b3	1a 	. 
	add hl,sp			;20b4	39 	9 
	nop			;20b5	00 	. 
	adc a,06ah		;20b6	ce 6a 	. j 
	jp po,l07f9h		;20b8	e2 f9 07 	. . . 
	ld e,0a5h		;20bb	1e a5 	. . 
	ld (l0000h),a		;20bd	32 00 00 	2 . . 
	nop			;20c0	00 	. 
	xor d			;20c1	aa 	. 
	nop			;20c2	00 	. 
	nop			;20c3	00 	. 
	nop			;20c4	00 	. 
	nop			;20c5	00 	. 
	xor d			;20c6	aa 	. 
	nop			;20c7	00 	. 
	nop			;20c8	00 	. 
	nop			;20c9	00 	. 
	nop			;20ca	00 	. 
	xor d			;20cb	aa 	. 
	nop			;20cc	00 	. 
	nop			;20cd	00 	. 
	nop			;20ce	00 	. 
	nop			;20cf	00 	. 
	xor d			;20d0	aa 	. 
	ld b,04dh		;20d1	06 4d 	. M 
	ld c,c			;20d3	49 	I 
	ld c,(hl)			;20d4	4e 	N 
	ld c,a			;20d5	4f 	O 
	ld d,d			;20d6	52 	R 
	jr nz,l211ch		;20d7	20 43 	  C 
	ld c,b			;20d9	48 	H 
	ld c,a			;20da	4f 	O 
	ld d,d			;20db	52 	R 
	ld b,h			;20dc	44 	D 
	jr nz,$+34		;20dd	20 20 	    
	nop			;20df	00 	. 
	nop			;20e0	00 	. 
	nop			;20e1	00 	. 
	nop			;20e2	00 	. 
	nop			;20e3	00 	. 
	nop			;20e4	00 	. 
	nop			;20e5	00 	. 
	nop			;20e6	00 	. 
	nop			;20e7	00 	. 
	nop			;20e8	00 	. 
	nop			;20e9	00 	. 
	nop			;20ea	00 	. 
	nop			;20eb	00 	. 
	nop			;20ec	00 	. 
	nop			;20ed	00 	. 
	nop			;20ee	00 	. 
	nop			;20ef	00 	. 
	nop			;20f0	00 	. 
	nop			;20f1	00 	. 
	nop			;20f2	00 	. 
	nop			;20f3	00 	. 
	nop			;20f4	00 	. 
	nop			;20f5	00 	. 
	nop			;20f6	00 	. 
	nop			;20f7	00 	. 
	nop			;20f8	00 	. 
	nop			;20f9	00 	. 
	nop			;20fa	00 	. 
	nop			;20fb	00 	. 
	nop			;20fc	00 	. 
	nop			;20fd	00 	. 
	ld (0c027h),a		;20fe	32 27 c0 	2 ' . 
	adc a,05ah		;2101	ce 5a 	. Z 
	adc a,00bh		;2103	ce 0b 	. . 
	dec bc			;2105	0b 	. 
	nop			;2106	00 	. 
	xor c			;2107	a9 	. 
	nop			;2108	00 	. 
	nop			;2109	00 	. 
	nop			;210a	00 	. 
	ld a,(bc)			;210b	0a 	. 
	xor d			;210c	aa 	. 
	inc c			;210d	0c 	. 
	inc c			;210e	0c 	. 
	ld (de),a			;210f	12 	. 
	ld c,0aah		;2110	0e aa 	. . 
	ld b,000h		;2112	06 00 	. . 
	rst 18h			;2114	df 	. 
	and 05ah		;2115	e6 5a 	. Z 
	ex de,hl			;2117	eb 	. 
	xor 0f2h		;2118	ee f2 	. . 
	rst 30h			;211a	f7 	. 
	ld d,l			;211b	55 	U 
l211ch:
	nop			;211c	00 	. 
	ld e,e			;211d	5b 	[ 
	ld e,(hl)			;211e	5e 	^ 
	ld h,c			;211f	61 	a 
	xor d			;2120	aa 	. 
	ld h,c			;2121	61 	a 
	ld h,c			;2122	61 	a 
	ld h,c			;2123	61 	a 
	nop			;2124	00 	. 
	xor d			;2125	aa 	. 
	sbc a,d			;2126	9a 	. 
	cp e			;2127	bb 	. 
	jp c,055fah		;2128	da fa 55 	. . U 
	ld a,(de)			;212b	1a 	. 
	add hl,sp			;212c	39 	9 
	nop			;212d	00 	. 
	adc a,06ah		;212e	ce 6a 	. j 
	jp po,l07f9h		;2130	e2 f9 07 	. . . 
	ld e,0a5h		;2133	1e a5 	. . 
	ld (l0000h),a		;2135	32 00 00 	2 . . 
	nop			;2138	00 	. 
	xor d			;2139	aa 	. 
	nop			;213a	00 	. 
	nop			;213b	00 	. 
	nop			;213c	00 	. 
	nop			;213d	00 	. 
	xor d			;213e	aa 	. 
	nop			;213f	00 	. 
	nop			;2140	00 	. 
	nop			;2141	00 	. 
	nop			;2142	00 	. 
	xor d			;2143	aa 	. 
	nop			;2144	00 	. 
	nop			;2145	00 	. 
	nop			;2146	00 	. 
	nop			;2147	00 	. 
	xor d			;2148	aa 	. 
	ld b,037h		;2149	06 37 	. 7 
	ld d,h			;214b	54 	T 
	ld c,b			;214c	48 	H 
	jr nz,$+85		;214d	20 53 	  S 
	ld c,b			;214f	48 	H 
	ld b,c			;2150	41 	A 
	ld d,d			;2151	52 	R 
	ld d,b			;2152	50 	P 
	jr nz,l2186h		;2153	20 31 	  1 
	ld sp,00020h		;2155	31 20 00 	1   . 
	nop			;2158	00 	. 
	nop			;2159	00 	. 
	nop			;215a	00 	. 
	nop			;215b	00 	. 
	nop			;215c	00 	. 
	nop			;215d	00 	. 
	nop			;215e	00 	. 
	nop			;215f	00 	. 
	nop			;2160	00 	. 
	nop			;2161	00 	. 
	nop			;2162	00 	. 
	nop			;2163	00 	. 
	nop			;2164	00 	. 
	nop			;2165	00 	. 
	nop			;2166	00 	. 
	nop			;2167	00 	. 
	nop			;2168	00 	. 
	nop			;2169	00 	. 
	nop			;216a	00 	. 
	nop			;216b	00 	. 
	nop			;216c	00 	. 
	nop			;216d	00 	. 
	nop			;216e	00 	. 
	nop			;216f	00 	. 
	nop			;2170	00 	. 
	nop			;2171	00 	. 
	nop			;2172	00 	. 
l2173h:
	nop			;2173	00 	. 
	nop			;2174	00 	. 
	nop			;2175	00 	. 
	ld (0c027h),a		;2176	32 27 c0 	2 ' . 
	adc a,05ah		;2179	ce 5a 	. Z 
	adc a,00bh		;217b	ce 0b 	. . 
	dec bc			;217d	0b 	. 
	nop			;217e	00 	. 
	xor c			;217f	a9 	. 
	nop			;2180	00 	. 
	nop			;2181	00 	. 
	nop			;2182	00 	. 
	inc b			;2183	04 	. 
	xor d			;2184	aa 	. 
	inc c			;2185	0c 	. 
l2186h:
	inc c			;2186	0c 	. 
	djnz l2196h		;2187	10 0d 	. . 
	xor d			;2189	aa 	. 
	ld a,(bc)			;218a	0a 	. 
	nop			;218b	00 	. 
	ex (sp),hl			;218c	e3 	. 
	rst 28h			;218d	ef 	. 
	ld e,d			;218e	5a 	Z 
	di			;218f	f3 	. 
	ld sp,hl			;2190	f9 	. 
	defb 0fdh,001h,095h	;illegal sequence		;2191	fd 01 95 	. . . 
	nop			;2194	00 	. 
	ld e,l			;2195	5d 	] 
l2196h:
	ld h,c			;2196	61 	a 
	ld h,c			;2197	61 	a 
	xor d			;2198	aa 	. 
	ld h,c			;2199	61 	a 
	ld h,c			;219a	61 	a 
	ld h,c			;219b	61 	a 
	nop			;219c	00 	. 
	xor d			;219d	aa 	. 
	sbc a,d			;219e	9a 	. 
	cp e			;219f	bb 	. 
	jp c,055fah		;21a0	da fa 55 	. . U 
	ld a,(de)			;21a3	1a 	. 
	add hl,sp			;21a4	39 	9 
	nop			;21a5	00 	. 
	nop			;21a6	00 	. 
	xor d			;21a7	aa 	. 
	adc a,0e7h		;21a8	ce e7 	. . 
	rlca			;21aa	07 	. 
	add hl,de			;21ab	19 	. 
	and l			;21ac	a5 	. 
	ld (l0000h),a		;21ad	32 00 00 	2 . . 
	nop			;21b0	00 	. 
	xor d			;21b1	aa 	. 
	nop			;21b2	00 	. 
	nop			;21b3	00 	. 
	nop			;21b4	00 	. 
	nop			;21b5	00 	. 
	xor d			;21b6	aa 	. 
	nop			;21b7	00 	. 
	nop			;21b8	00 	. 
	nop			;21b9	00 	. 
	nop			;21ba	00 	. 
	xor d			;21bb	aa 	. 
	nop			;21bc	00 	. 
	nop			;21bd	00 	. 
	nop			;21be	00 	. 
	nop			;21bf	00 	. 
	xor d			;21c0	aa 	. 
l21c1h:
	ld b,044h		;21c1	06 44 	. D 
	ld c,a			;21c3	4f 	O 
	ld c,l			;21c4	4d 	M 
	jr nz,l21f8h		;21c5	20 31 	  1 
	inc sp			;21c7	33 	3 
	ld d,h			;21c8	54 	T 
	ld c,b			;21c9	48 	H 
	jr nz,l21ech		;21ca	20 20 	    
	jr nz,l21eeh		;21cc	20 20 	    
	jr nz,l21d0h		;21ce	20 00 	  . 
l21d0h:
	nop			;21d0	00 	. 
	nop			;21d1	00 	. 
	ld b,c			;21d2	41 	A 
	nop			;21d3	00 	. 
	ld b,c			;21d4	41 	A 
	ld b,c			;21d5	41 	A 
	nop			;21d6	00 	. 
	nop			;21d7	00 	. 
	nop			;21d8	00 	. 
	nop			;21d9	00 	. 
	nop			;21da	00 	. 
	nop			;21db	00 	. 
	ld d,000h		;21dc	16 00 	. . 
	jr l21f9h		;21de	18 19 	. . 
	nop			;21e0	00 	. 
	nop			;21e1	00 	. 
	nop			;21e2	00 	. 
	nop			;21e3	00 	. 
	nop			;21e4	00 	. 
	nop			;21e5	00 	. 
	call m,00100h		;21e6	fc 00 01 	. . . 
	inc bc			;21e9	03 	. 
	nop			;21ea	00 	. 
	nop			;21eb	00 	. 
l21ech:
	nop			;21ec	00 	. 
	nop			;21ed	00 	. 
l21eeh:
	ld (0c027h),a		;21ee	32 27 c0 	2 ' . 
	adc a,05ah		;21f1	ce 5a 	. Z 
	adc a,00bh		;21f3	ce 0b 	. . 
	dec bc			;21f5	0b 	. 
	nop			;21f6	00 	. 
	xor c			;21f7	a9 	. 
l21f8h:
	nop			;21f8	00 	. 
l21f9h:
	nop			;21f9	00 	. 
	nop			;21fa	00 	. 
	rrca			;21fb	0f 	. 
	xor d			;21fc	aa 	. 
	dec c			;21fd	0d 	. 
	ld de,l0410h		;21fe	11 10 04 	. . . 
	xor d			;2201	aa 	. 
	rlca			;2202	07 	. 
	nop			;2203	00 	. 
	rst 18h			;2204	df 	. 
	ex de,hl			;2205	eb 	. 
	ld e,d			;2206	5a 	Z 
	push af			;2207	f5 	. 
	ei			;2208	fb 	. 
	call p,09503h		;2209	f4 03 95 	. . . 
	nop			;220c	00 	. 
	ld e,e			;220d	5b 	[ 
	ld e,(hl)			;220e	5e 	^ 
	ld e,(hl)			;220f	5e 	^ 
	xor d			;2210	aa 	. 
	ld h,c			;2211	61 	a 
	ld h,c			;2212	61 	a 
	ld h,c			;2213	61 	a 
	nop			;2214	00 	. 
	xor d			;2215	aa 	. 
	sbc a,d			;2216	9a 	. 
	xor a			;2217	af 	. 
	push bc			;2218	c5 	. 
	jp c,0ef55h		;2219	da 55 ef 	. U . 
	di			;221c	f3 	. 
	nop			;221d	00 	. 
	in a,(065h)		;221e	db 65 	. e 
	ld h,0efh		;2220	26 ef 	& . 
	ld de,066fbh		;2222	11 fb 66 	. . f 
	dec b			;2225	05 	. 
	nop			;2226	00 	. 
	nop			;2227	00 	. 
	nop			;2228	00 	. 
	xor d			;2229	aa 	. 
	nop			;222a	00 	. 
	nop			;222b	00 	. 
	nop			;222c	00 	. 
	nop			;222d	00 	. 
	xor d			;222e	aa 	. 
	nop			;222f	00 	. 
	nop			;2230	00 	. 
	nop			;2231	00 	. 
	nop			;2232	00 	. 
	xor d			;2233	aa 	. 
	nop			;2234	00 	. 
	nop			;2235	00 	. 
	nop			;2236	00 	. 
	nop			;2237	00 	. 
	xor d			;2238	aa 	. 
	rlca			;2239	07 	. 
	ld b,e			;223a	43 	C 
	ld c,a			;223b	4f 	O 
	ld c,(hl)			;223c	4e 	N 
	ld b,e			;223d	43 	C 
	ld b,l			;223e	45 	E 
	ld d,d			;223f	52 	R 
	ld d,h			;2240	54 	T 
	jr nz,l228bh		;2241	20 48 	  H 
	ld b,c			;2243	41 	A 
	ld c,h			;2244	4c 	L 
	ld c,h			;2245	4c 	L 
	jr nz,l2248h		;2246	20 00 	  . 
l2248h:
	nop			;2248	00 	. 
	nop			;2249	00 	. 
	nop			;224a	00 	. 
	nop			;224b	00 	. 
	nop			;224c	00 	. 
	nop			;224d	00 	. 
	nop			;224e	00 	. 
	nop			;224f	00 	. 
	nop			;2250	00 	. 
	nop			;2251	00 	. 
	nop			;2252	00 	. 
	nop			;2253	00 	. 
	nop			;2254	00 	. 
	nop			;2255	00 	. 
	nop			;2256	00 	. 
	nop			;2257	00 	. 
	nop			;2258	00 	. 
	nop			;2259	00 	. 
	nop			;225a	00 	. 
	nop			;225b	00 	. 
	nop			;225c	00 	. 
	nop			;225d	00 	. 
	nop			;225e	00 	. 
	nop			;225f	00 	. 
	nop			;2260	00 	. 
	nop			;2261	00 	. 
	nop			;2262	00 	. 
	nop			;2263	00 	. 
	nop			;2264	00 	. 
	nop			;2265	00 	. 
	ld (0c02dh),a		;2266	32 2d c0 	2 - . 
	ld d,09ah		;2269	16 9a 	. . 
	ld a,a			;226b	7f 	 
	adc a,l			;226c	8d 	. 
	dec c			;226d	0d 	. 
	nop			;226e	00 	. 
	and (hl)			;226f	a6 	. 
	ld bc,00800h		;2270	01 00 08 	. . . 
	nop			;2273	00 	. 
	xor d			;2274	aa 	. 
	jp p,0f006h		;2275	f2 06 f0 	. . . 
	ret p			;2278	f0 	. 
	ld e,c			;2279	59 	Y 
	ld a,(bc)			;227a	0a 	. 
	pop af			;227b	f1 	. 
	or 000h		;227c	f6 00 	. . 
	sub (hl)			;227e	96 	. 
	rst 28h			;227f	ef 	. 
	rst 28h			;2280	ef 	. 
	rst 28h			;2281	ef 	. 
	rst 28h			;2282	ef 	. 
	ld d,l			;2283	55 	U 
	nop			;2284	00 	. 
	sub b			;2285	90 	. 
	sub b			;2286	90 	. 
	sub b			;2287	90 	. 
	ld d,(hl)			;2288	56 	V 
	sub b			;2289	90 	. 
	nop			;228a	00 	. 
l228bh:
	nop			;228b	00 	. 
	nop			;228c	00 	. 
	xor c			;228d	a9 	. 
	nop			;228e	00 	. 
	nop			;228f	00 	. 
	nop			;2290	00 	. 
	nop			;2291	00 	. 
	xor d			;2292	aa 	. 
	nop			;2293	00 	. 
	nop			;2294	00 	. 
	nop			;2295	00 	. 
	nop			;2296	00 	. 
	xor d			;2297	aa 	. 
	nop			;2298	00 	. 
	nop			;2299	00 	. 
	nop			;229a	00 	. 
	nop			;229b	00 	. 
	xor d			;229c	aa 	. 
	nop			;229d	00 	. 
	nop			;229e	00 	. 
	nop			;229f	00 	. 
	nop			;22a0	00 	. 
	xor d			;22a1	aa 	. 
	nop			;22a2	00 	. 
	nop			;22a3	00 	. 
	nop			;22a4	00 	. 
	nop			;22a5	00 	. 
	xor d			;22a6	aa 	. 
	nop			;22a7	00 	. 
	nop			;22a8	00 	. 
	nop			;22a9	00 	. 
	nop			;22aa	00 	. 
	xor d			;22ab	aa 	. 
	nop			;22ac	00 	. 
	nop			;22ad	00 	. 
	nop			;22ae	00 	. 
	nop			;22af	00 	. 
	xor d			;22b0	aa 	. 
l22b1h:
	rlca			;22b1	07 	. 
	ld c,h			;22b2	4c 	L 
	ld c,a			;22b3	4f 	O 
	ld c,(hl)			;22b4	4e 	N 
	ld b,a			;22b5	47 	G 
	jr nz,l2300h		;22b6	20 48 	  H 
	ld b,c			;22b8	41 	A 
	ld c,h			;22b9	4c 	L 
	ld c,h			;22ba	4c 	L 
	jr nz,l22ddh		;22bb	20 20 	    
	jr nz,$+34		;22bd	20 20 	    
	nop			;22bf	00 	. 
	nop			;22c0	00 	. 
	nop			;22c1	00 	. 
	nop			;22c2	00 	. 
	nop			;22c3	00 	. 
	nop			;22c4	00 	. 
	nop			;22c5	00 	. 
	nop			;22c6	00 	. 
	nop			;22c7	00 	. 
	nop			;22c8	00 	. 
	nop			;22c9	00 	. 
	nop			;22ca	00 	. 
	nop			;22cb	00 	. 
	nop			;22cc	00 	. 
	nop			;22cd	00 	. 
	nop			;22ce	00 	. 
	nop			;22cf	00 	. 
	nop			;22d0	00 	. 
	nop			;22d1	00 	. 
	nop			;22d2	00 	. 
	nop			;22d3	00 	. 
	nop			;22d4	00 	. 
	nop			;22d5	00 	. 
	nop			;22d6	00 	. 
	nop			;22d7	00 	. 
	nop			;22d8	00 	. 
	nop			;22d9	00 	. 
	nop			;22da	00 	. 
	nop			;22db	00 	. 
	nop			;22dc	00 	. 
l22ddh:
	nop			;22dd	00 	. 
	ld (0c02ch),a		;22de	32 2c c0 	2 , . 
	add hl,de			;22e1	19 	. 
	sbc a,d			;22e2	9a 	. 
	ld a,a			;22e3	7f 	 
	adc a,c			;22e4	89 	. 
	inc bc			;22e5	03 	. 
	nop			;22e6	00 	. 
	and (hl)			;22e7	a6 	. 
	ld bc,l0a00h		;22e8	01 00 0a 	. . . 
	ld b,0aah		;22eb	06 aa 	. . 
	jp m,0ff08h		;22ed	fa 08 ff 	. . . 
	rst 38h			;22f0	ff 	. 
	ld e,c			;22f1	59 	Y 
	ei			;22f2	fb 	. 
	call pe,000e1h		;22f3	ec e1 00 	. . . 
	sub l			;22f6	95 	. 
	rst 28h			;22f7	ef 	. 
	rst 28h			;22f8	ef 	. 
	rst 28h			;22f9	ef 	. 
	rst 28h			;22fa	ef 	. 
	ld d,l			;22fb	55 	U 
	nop			;22fc	00 	. 
	sub b			;22fd	90 	. 
	sub b			;22fe	90 	. 
	sub b			;22ff	90 	. 
l2300h:
	ld d,(hl)			;2300	56 	V 
	sub b			;2301	90 	. 
	nop			;2302	00 	. 
	nop			;2303	00 	. 
	nop			;2304	00 	. 
	xor c			;2305	a9 	. 
	nop			;2306	00 	. 
	nop			;2307	00 	. 
	nop			;2308	00 	. 
	nop			;2309	00 	. 
	xor d			;230a	aa 	. 
	nop			;230b	00 	. 
	nop			;230c	00 	. 
	nop			;230d	00 	. 
	nop			;230e	00 	. 
	xor d			;230f	aa 	. 
	nop			;2310	00 	. 
	nop			;2311	00 	. 
	nop			;2312	00 	. 
	nop			;2313	00 	. 
	xor d			;2314	aa 	. 
	nop			;2315	00 	. 
	nop			;2316	00 	. 
	nop			;2317	00 	. 
	nop			;2318	00 	. 
	xor d			;2319	aa 	. 
	nop			;231a	00 	. 
	nop			;231b	00 	. 
	nop			;231c	00 	. 
	nop			;231d	00 	. 
	xor d			;231e	aa 	. 
	nop			;231f	00 	. 
	nop			;2320	00 	. 
	nop			;2321	00 	. 
	nop			;2322	00 	. 
	xor d			;2323	aa 	. 
	nop			;2324	00 	. 
	nop			;2325	00 	. 
	nop			;2326	00 	. 
	nop			;2327	00 	. 
	xor d			;2328	aa 	. 
	rlca			;2329	07 	. 
	ld b,a			;232a	47 	G 
	ld e,c			;232b	59 	Y 
	ld c,l			;232c	4d 	M 
	ld c,(hl)			;232d	4e 	N 
	ld b,c			;232e	41 	A 
	ld d,e			;232f	53 	S 
	ld c,c			;2330	49 	I 
	ld d,l			;2331	55 	U 
	ld c,l			;2332	4d 	M 
	jr nz,l2355h		;2333	20 20 	    
	jr nz,$+34		;2335	20 20 	    
	nop			;2337	00 	. 
	nop			;2338	00 	. 
	nop			;2339	00 	. 
	nop			;233a	00 	. 
	nop			;233b	00 	. 
	nop			;233c	00 	. 
	nop			;233d	00 	. 
	nop			;233e	00 	. 
	nop			;233f	00 	. 
	nop			;2340	00 	. 
	nop			;2341	00 	. 
	nop			;2342	00 	. 
	nop			;2343	00 	. 
	nop			;2344	00 	. 
	nop			;2345	00 	. 
	nop			;2346	00 	. 
	nop			;2347	00 	. 
	nop			;2348	00 	. 
	nop			;2349	00 	. 
	nop			;234a	00 	. 
	nop			;234b	00 	. 
	nop			;234c	00 	. 
	nop			;234d	00 	. 
	nop			;234e	00 	. 
	nop			;234f	00 	. 
	nop			;2350	00 	. 
	nop			;2351	00 	. 
	nop			;2352	00 	. 
	nop			;2353	00 	. 
	nop			;2354	00 	. 
l2355h:
	nop			;2355	00 	. 
	ld (0c02dh),a		;2356	32 2d c0 	2 - . 
	inc bc			;2359	03 	. 
	sbc a,d			;235a	9a 	. 
	ld a,a			;235b	7f 	 
	xor e			;235c	ab 	. 
	rst 38h			;235d	ff 	. 
	ld b,096h		;235e	06 96 	. . 
	ld bc,l0600h		;2360	01 00 06 	. . . 
	inc c			;2363	0c 	. 
	xor d			;2364	aa 	. 
	or 000h		;2365	f6 00 	. . 
	rst 38h			;2367	ff 	. 
	rst 38h			;2368	ff 	. 
	ld e,c			;2369	59 	Y 
	cp 008h		;236a	fe 08 	. . 
	daa			;236c	27 	' 
	nop			;236d	00 	. 
	xor c			;236e	a9 	. 
	rlca			;236f	07 	. 
	rst 28h			;2370	ef 	. 
	rlca			;2371	07 	. 
	rst 28h			;2372	ef 	. 
	ld h,(hl)			;2373	66 	f 
	nop			;2374	00 	. 
	jp po,0e990h		;2375	e2 90 e9 	. . . 
	ld d,(hl)			;2378	56 	V 
	sub b			;2379	90 	. 
	nop			;237a	00 	. 
	nop			;237b	00 	. 
	nop			;237c	00 	. 
	xor c			;237d	a9 	. 
	nop			;237e	00 	. 
	nop			;237f	00 	. 
	nop			;2380	00 	. 
	nop			;2381	00 	. 
	xor d			;2382	aa 	. 
	nop			;2383	00 	. 
	nop			;2384	00 	. 
	nop			;2385	00 	. 
	nop			;2386	00 	. 
	xor d			;2387	aa 	. 
	nop			;2388	00 	. 
	nop			;2389	00 	. 
	nop			;238a	00 	. 
	nop			;238b	00 	. 
	xor d			;238c	aa 	. 
	nop			;238d	00 	. 
	nop			;238e	00 	. 
	nop			;238f	00 	. 
	nop			;2390	00 	. 
	xor d			;2391	aa 	. 
	nop			;2392	00 	. 
	nop			;2393	00 	. 
	nop			;2394	00 	. 
	nop			;2395	00 	. 
	xor d			;2396	aa 	. 
	nop			;2397	00 	. 
	nop			;2398	00 	. 
	nop			;2399	00 	. 
	nop			;239a	00 	. 
	xor d			;239b	aa 	. 
	nop			;239c	00 	. 
	nop			;239d	00 	. 
	nop			;239e	00 	. 
	nop			;239f	00 	. 
	xor d			;23a0	aa 	. 
	ex af,af'			;23a1	08 	. 
	ld d,d			;23a2	52 	R 
	ld c,c			;23a3	49 	I 
	ld b,e			;23a4	43 	C 
	ld c,b			;23a5	48 	H 
	jr nz,l23ebh		;23a6	20 43 	  C 
	ld c,b			;23a8	48 	H 
	ld b,c			;23a9	41 	A 
	ld c,l			;23aa	4d 	M 
	ld b,d			;23ab	42 	B 
	ld b,l			;23ac	45 	E 
	ld d,d			;23ad	52 	R 
	jr nz,l23b0h		;23ae	20 00 	  . 
l23b0h:
	nop			;23b0	00 	. 
	nop			;23b1	00 	. 
	nop			;23b2	00 	. 
	nop			;23b3	00 	. 
	nop			;23b4	00 	. 
	nop			;23b5	00 	. 
	nop			;23b6	00 	. 
	nop			;23b7	00 	. 
	nop			;23b8	00 	. 
	nop			;23b9	00 	. 
	nop			;23ba	00 	. 
	nop			;23bb	00 	. 
	nop			;23bc	00 	. 
	nop			;23bd	00 	. 
	nop			;23be	00 	. 
	nop			;23bf	00 	. 
	nop			;23c0	00 	. 
	nop			;23c1	00 	. 
	nop			;23c2	00 	. 
	nop			;23c3	00 	. 
	nop			;23c4	00 	. 
	nop			;23c5	00 	. 
	nop			;23c6	00 	. 
	nop			;23c7	00 	. 
	nop			;23c8	00 	. 
	nop			;23c9	00 	. 
	nop			;23ca	00 	. 
	nop			;23cb	00 	. 
	nop			;23cc	00 	. 
	nop			;23cd	00 	. 
	ld (0c028h),a		;23ce	32 28 c0 	2 ( . 
	cp 05ah		;23d1	fe 5a 	. Z 
	ld a,a			;23d3	7f 	 
	add a,c			;23d4	81 	. 
	nop			;23d5	00 	. 
	ld bc,l00a6h		;23d6	01 a6 00 	. . . 
	nop			;23d9	00 	. 
	dec c			;23da	0d 	. 
	rlca			;23db	07 	. 
	xor d			;23dc	aa 	. 
	ret m			;23dd	f8 	. 
	dec b			;23de	05 	. 
	ld b,006h		;23df	06 06 	. . 
	xor c			;23e1	a9 	. 
	rst 38h			;23e2	ff 	. 
	nop			;23e3	00 	. 
	nop			;23e4	00 	. 
	nop			;23e5	00 	. 
	xor c			;23e6	a9 	. 
	rst 28h			;23e7	ef 	. 
	rst 28h			;23e8	ef 	. 
	rst 28h			;23e9	ef 	. 
	rst 28h			;23ea	ef 	. 
l23ebh:
	ld d,l			;23eb	55 	U 
	rst 28h			;23ec	ef 	. 
	rst 28h			;23ed	ef 	. 
	nop			;23ee	00 	. 
	sub b			;23ef	90 	. 
	ld h,l			;23f0	65 	e 
	sub b			;23f1	90 	. 
	sub b			;23f2	90 	. 
	sub b			;23f3	90 	. 
	sub b			;23f4	90 	. 
	ld d,l			;23f5	55 	U 
	sub b			;23f6	90 	. 
	nop			;23f7	00 	. 
	nop			;23f8	00 	. 
	nop			;23f9	00 	. 
	xor c			;23fa	a9 	. 
	nop			;23fb	00 	. 
	nop			;23fc	00 	. 
	nop			;23fd	00 	. 
	nop			;23fe	00 	. 
	xor d			;23ff	aa 	. 
	nop			;2400	00 	. 
	nop			;2401	00 	. 
	nop			;2402	00 	. 
	nop			;2403	00 	. 
	xor d			;2404	aa 	. 
	nop			;2405	00 	. 
	nop			;2406	00 	. 
	nop			;2407	00 	. 
	nop			;2408	00 	. 
	xor d			;2409	aa 	. 
	nop			;240a	00 	. 
	nop			;240b	00 	. 
	nop			;240c	00 	. 
	nop			;240d	00 	. 
	xor d			;240e	aa 	. 
	nop			;240f	00 	. 
	nop			;2410	00 	. 
	nop			;2411	00 	. 
	nop			;2412	00 	. 
	xor d			;2413	aa 	. 
	nop			;2414	00 	. 
	nop			;2415	00 	. 
	nop			;2416	00 	. 
	nop			;2417	00 	. 
	xor d			;2418	aa 	. 
	ex af,af'			;2419	08 	. 
	ld d,e			;241a	53 	S 
	ld c,l			;241b	4d 	M 
	ld b,c			;241c	41 	A 
	ld c,h			;241d	4c 	L 
	ld c,h			;241e	4c 	L 
	jr nz,l2473h		;241f	20 52 	  R 
	ld c,a			;2421	4f 	O 
	ld c,a			;2422	4f 	O 
	ld c,l			;2423	4d 	M 
	jr nz,l2446h		;2424	20 20 	    
	jr nz,l2428h		;2426	20 00 	  . 
l2428h:
	nop			;2428	00 	. 
	nop			;2429	00 	. 
	nop			;242a	00 	. 
	nop			;242b	00 	. 
	nop			;242c	00 	. 
	nop			;242d	00 	. 
	nop			;242e	00 	. 
	nop			;242f	00 	. 
	nop			;2430	00 	. 
	nop			;2431	00 	. 
	nop			;2432	00 	. 
	nop			;2433	00 	. 
	nop			;2434	00 	. 
	nop			;2435	00 	. 
	nop			;2436	00 	. 
	nop			;2437	00 	. 
	nop			;2438	00 	. 
	nop			;2439	00 	. 
	nop			;243a	00 	. 
	nop			;243b	00 	. 
	nop			;243c	00 	. 
	nop			;243d	00 	. 
	nop			;243e	00 	. 
	nop			;243f	00 	. 
	nop			;2440	00 	. 
	nop			;2441	00 	. 
	nop			;2442	00 	. 
	nop			;2443	00 	. 
	nop			;2444	00 	. 
	nop			;2445	00 	. 
l2446h:
	ld (0c027h),a		;2446	32 27 c0 	2 ' . 
	or 05ah		;2449	f6 5a 	. Z 
	ld a,a			;244b	7f 	 
	add a,a			;244c	87 	. 
	rlca			;244d	07 	. 
	ld bc,l00a6h		;244e	01 a6 00 	. . . 
	nop			;2451	00 	. 
	inc b			;2452	04 	. 
	ld (bc),a			;2453	02 	. 
	xor d			;2454	aa 	. 
	or 008h		;2455	f6 08 	. . 
	ld b,006h		;2457	06 06 	. . 
	xor c			;2459	a9 	. 
	ld a,(bc)			;245a	0a 	. 
	ret m			;245b	f8 	. 
	call pe,09600h		;245c	ec 00 96 	. . . 
	rst 28h			;245f	ef 	. 
	rst 28h			;2460	ef 	. 
	rst 28h			;2461	ef 	. 
	rst 28h			;2462	ef 	. 
	ld d,l			;2463	55 	U 
	rst 28h			;2464	ef 	. 
	rst 28h			;2465	ef 	. 
	nop			;2466	00 	. 
	sub b			;2467	90 	. 
	ld h,l			;2468	65 	e 
	sub b			;2469	90 	. 
	sub b			;246a	90 	. 
	sub b			;246b	90 	. 
	sub b			;246c	90 	. 
	ld d,l			;246d	55 	U 
	sub b			;246e	90 	. 
	nop			;246f	00 	. 
	nop			;2470	00 	. 
	nop			;2471	00 	. 
	xor c			;2472	a9 	. 
l2473h:
	nop			;2473	00 	. 
	nop			;2474	00 	. 
	nop			;2475	00 	. 
	nop			;2476	00 	. 
	xor d			;2477	aa 	. 
	nop			;2478	00 	. 
	nop			;2479	00 	. 
	nop			;247a	00 	. 
	nop			;247b	00 	. 
	xor d			;247c	aa 	. 
	nop			;247d	00 	. 
	nop			;247e	00 	. 
	nop			;247f	00 	. 
	nop			;2480	00 	. 
	xor d			;2481	aa 	. 
	nop			;2482	00 	. 
	nop			;2483	00 	. 
	nop			;2484	00 	. 
	nop			;2485	00 	. 
	xor d			;2486	aa 	. 
	nop			;2487	00 	. 
	nop			;2488	00 	. 
	nop			;2489	00 	. 
	nop			;248a	00 	. 
	xor d			;248b	aa 	. 
	nop			;248c	00 	. 
	nop			;248d	00 	. 
	nop			;248e	00 	. 
	nop			;248f	00 	. 
	xor d			;2490	aa 	. 
	ex af,af'			;2491	08 	. 
	ld d,h			;2492	54 	T 
	ld c,c			;2493	49 	I 
	ld c,h			;2494	4c 	L 
	ld b,l			;2495	45 	E 
	ld b,h			;2496	44 	D 
	jr nz,l24ebh		;2497	20 52 	  R 
	ld c,a			;2499	4f 	O 
	ld c,a			;249a	4f 	O 
	ld c,l			;249b	4d 	M 
	jr nz,l24beh		;249c	20 20 	    
	jr nz,l24a0h		;249e	20 00 	  . 
l24a0h:
	nop			;24a0	00 	. 
	nop			;24a1	00 	. 
	nop			;24a2	00 	. 
	nop			;24a3	00 	. 
	nop			;24a4	00 	. 
	nop			;24a5	00 	. 
	nop			;24a6	00 	. 
	nop			;24a7	00 	. 
	nop			;24a8	00 	. 
	nop			;24a9	00 	. 
	nop			;24aa	00 	. 
	nop			;24ab	00 	. 
	nop			;24ac	00 	. 
	nop			;24ad	00 	. 
	nop			;24ae	00 	. 
	nop			;24af	00 	. 
	nop			;24b0	00 	. 
	nop			;24b1	00 	. 
	nop			;24b2	00 	. 
	nop			;24b3	00 	. 
	nop			;24b4	00 	. 
	nop			;24b5	00 	. 
	nop			;24b6	00 	. 
	nop			;24b7	00 	. 
	nop			;24b8	00 	. 
	nop			;24b9	00 	. 
	nop			;24ba	00 	. 
	nop			;24bb	00 	. 
	nop			;24bc	00 	. 
	nop			;24bd	00 	. 
l24beh:
	ld (0c027h),a		;24be	32 27 c0 	2 ' . 
	pop af			;24c1	f1 	. 
	ld e,d			;24c2	5a 	Z 
	ld a,a			;24c3	7f 	 
	add a,e			;24c4	83 	. 
	dec bc			;24c5	0b 	. 
	ld bc,l00a6h		;24c6	01 a6 00 	. . . 
	nop			;24c9	00 	. 
	rlca			;24ca	07 	. 
	dec b			;24cb	05 	. 
	xor d			;24cc	aa 	. 
	rst 38h			;24cd	ff 	. 
	ld a,(bc)			;24ce	0a 	. 
	ret p			;24cf	f0 	. 
	ret p			;24d0	f0 	. 
	ld e,c			;24d1	59 	Y 
	pop af			;24d2	f1 	. 
	adc a,001h		;24d3	ce 01 	. . 
	nop			;24d5	00 	. 
	and l			;24d6	a5 	. 
	ld a,(bc)			;24d7	0a 	. 
	rst 28h			;24d8	ef 	. 
	rst 28h			;24d9	ef 	. 
	ld a,(bc)			;24da	0a 	. 
	sub (hl)			;24db	96 	. 
	rst 28h			;24dc	ef 	. 
	rst 28h			;24dd	ef 	. 
	nop			;24de	00 	. 
	sbc a,(hl)			;24df	9e 	. 
	ld h,l			;24e0	65 	e 
	sub b			;24e1	90 	. 
	sub b			;24e2	90 	. 
	xor c			;24e3	a9 	. 
	sub b			;24e4	90 	. 
	ld d,l			;24e5	55 	U 
	sub b			;24e6	90 	. 
	nop			;24e7	00 	. 
	nop			;24e8	00 	. 
	nop			;24e9	00 	. 
	xor c			;24ea	a9 	. 
l24ebh:
	nop			;24eb	00 	. 
	nop			;24ec	00 	. 
	nop			;24ed	00 	. 
	nop			;24ee	00 	. 
	xor d			;24ef	aa 	. 
	nop			;24f0	00 	. 
	nop			;24f1	00 	. 
	nop			;24f2	00 	. 
	nop			;24f3	00 	. 
	xor d			;24f4	aa 	. 
	nop			;24f5	00 	. 
	nop			;24f6	00 	. 
	nop			;24f7	00 	. 
	nop			;24f8	00 	. 
	xor d			;24f9	aa 	. 
	nop			;24fa	00 	. 
	nop			;24fb	00 	. 
	nop			;24fc	00 	. 
	nop			;24fd	00 	. 
	xor d			;24fe	aa 	. 
	nop			;24ff	00 	. 
	nop			;2500	00 	. 
	nop			;2501	00 	. 
	nop			;2502	00 	. 
	xor d			;2503	aa 	. 
	nop			;2504	00 	. 
	nop			;2505	00 	. 
	nop			;2506	00 	. 
	nop			;2507	00 	. 
	xor d			;2508	aa 	. 
	ex af,af'			;2509	08 	. 
	ld b,a			;250a	47 	G 
	ld b,c			;250b	41 	A 
	ld d,h			;250c	54 	T 
	ld b,l			;250d	45 	E 
	ld b,h			;250e	44 	D 
	jr nz,l2554h		;250f	20 43 	  C 
	ld c,b			;2511	48 	H 
	ld b,c			;2512	41 	A 
	ld c,l			;2513	4d 	M 
	ld b,d			;2514	42 	B 
	ld b,l			;2515	45 	E 
	ld d,d			;2516	52 	R 
	nop			;2517	00 	. 
	nop			;2518	00 	. 
	nop			;2519	00 	. 
	nop			;251a	00 	. 
	nop			;251b	00 	. 
	nop			;251c	00 	. 
	nop			;251d	00 	. 
	nop			;251e	00 	. 
	nop			;251f	00 	. 
	nop			;2520	00 	. 
	nop			;2521	00 	. 
	nop			;2522	00 	. 
	nop			;2523	00 	. 
	nop			;2524	00 	. 
	nop			;2525	00 	. 
	nop			;2526	00 	. 
	nop			;2527	00 	. 
	nop			;2528	00 	. 
	nop			;2529	00 	. 
	nop			;252a	00 	. 
	nop			;252b	00 	. 
	nop			;252c	00 	. 
	nop			;252d	00 	. 
	nop			;252e	00 	. 
	nop			;252f	00 	. 
	nop			;2530	00 	. 
	nop			;2531	00 	. 
	nop			;2532	00 	. 
	nop			;2533	00 	. 
	nop			;2534	00 	. 
	nop			;2535	00 	. 
	ld (0c027h),a		;2536	32 27 c0 	2 ' . 
	ld sp,hl			;2539	f9 	. 
	ld e,d			;253a	5a 	Z 
	add a,h			;253b	84 	. 
	adc a,(hl)			;253c	8e 	. 
	dec bc			;253d	0b 	. 
	ld bc,l00a5h		;253e	01 a5 00 	. . . 
	nop			;2541	00 	. 
	dec c			;2542	0d 	. 
	dec c			;2543	0d 	. 
	xor d			;2544	aa 	. 
	ret m			;2545	f8 	. 
	dec c			;2546	0d 	. 
	ret p			;2547	f0 	. 
	ret p			;2548	f0 	. 
	ld e,c			;2549	59 	Y 
	rrca			;254a	0f 	. 
	inc d			;254b	14 	. 
	jp po,09a00h		;254c	e2 00 9a 	. . . 
	rst 28h			;254f	ef 	. 
	rst 28h			;2550	ef 	. 
	rst 28h			;2551	ef 	. 
	rst 28h			;2552	ef 	. 
	ld d,l			;2553	55 	U 
l2554h:
	rst 28h			;2554	ef 	. 
	rst 28h			;2555	ef 	. 
	nop			;2556	00 	. 
	sub b			;2557	90 	. 
	ld h,l			;2558	65 	e 
	sub b			;2559	90 	. 
	sub b			;255a	90 	. 
	sub b			;255b	90 	. 
	sub b			;255c	90 	. 
	ld d,l			;255d	55 	U 
	sub b			;255e	90 	. 
	nop			;255f	00 	. 
	nop			;2560	00 	. 
	nop			;2561	00 	. 
	xor c			;2562	a9 	. 
	nop			;2563	00 	. 
	nop			;2564	00 	. 
	nop			;2565	00 	. 
	nop			;2566	00 	. 
	xor d			;2567	aa 	. 
	nop			;2568	00 	. 
	nop			;2569	00 	. 
	nop			;256a	00 	. 
	nop			;256b	00 	. 
	xor d			;256c	aa 	. 
	nop			;256d	00 	. 
	nop			;256e	00 	. 
	nop			;256f	00 	. 
	nop			;2570	00 	. 
	xor d			;2571	aa 	. 
	nop			;2572	00 	. 
	nop			;2573	00 	. 
	nop			;2574	00 	. 
	nop			;2575	00 	. 
	xor d			;2576	aa 	. 
	nop			;2577	00 	. 
	nop			;2578	00 	. 
	nop			;2579	00 	. 
	nop			;257a	00 	. 
	xor d			;257b	aa 	. 
	nop			;257c	00 	. 
	nop			;257d	00 	. 
	nop			;257e	00 	. 
	nop			;257f	00 	. 
	xor d			;2580	aa 	. 
	ld a,(bc)			;2581	0a 	. 
	ld c,c			;2582	49 	I 
	ld c,(hl)			;2583	4e 	N 
	ld b,(hl)			;2584	46 	F 
	jr nz,l25d9h		;2585	20 52 	  R 
	ld b,l			;2587	45 	E 
	ld d,(hl)			;2588	56 	V 
	ld b,l			;2589	45 	E 
	ld d,d			;258a	52 	R 
	ld b,d			;258b	42 	B 
	jr nz,l25aeh		;258c	20 20 	    
	jr nz,l2590h		;258e	20 00 	  . 
l2590h:
	nop			;2590	00 	. 
	nop			;2591	00 	. 
	nop			;2592	00 	. 
	nop			;2593	00 	. 
	nop			;2594	00 	. 
	nop			;2595	00 	. 
	nop			;2596	00 	. 
	nop			;2597	00 	. 
	nop			;2598	00 	. 
	nop			;2599	00 	. 
	nop			;259a	00 	. 
	nop			;259b	00 	. 
	nop			;259c	00 	. 
	nop			;259d	00 	. 
	nop			;259e	00 	. 
	nop			;259f	00 	. 
	nop			;25a0	00 	. 
	nop			;25a1	00 	. 
	nop			;25a2	00 	. 
	nop			;25a3	00 	. 
	nop			;25a4	00 	. 
	nop			;25a5	00 	. 
	nop			;25a6	00 	. 
	nop			;25a7	00 	. 
	nop			;25a8	00 	. 
	nop			;25a9	00 	. 
	nop			;25aa	00 	. 
	nop			;25ab	00 	. 
	nop			;25ac	00 	. 
	nop			;25ad	00 	. 
l25aeh:
	ld (0c021h),a		;25ae	32 21 c0 	2 ! . 
	inc de			;25b1	13 	. 
	sbc a,d			;25b2	9a 	. 
	rrca			;25b3	0f 	. 
	add a,c			;25b4	81 	. 
	inc c			;25b5	0c 	. 
	nop			;25b6	00 	. 
	and (hl)			;25b7	a6 	. 
	nop			;25b8	00 	. 
	nop			;25b9	00 	. 
	nop			;25ba	00 	. 
	push de			;25bb	d5 	. 
	ld l,d			;25bc	6a 	j 
	adc a,000h		;25bd	ce 00 	. . 
	rst 28h			;25bf	ef 	. 
	rst 28h			;25c0	ef 	. 
	ld e,c			;25c1	59 	Y 
	rst 28h			;25c2	ef 	. 
	rst 28h			;25c3	ef 	. 
	rst 28h			;25c4	ef 	. 
	rst 28h			;25c5	ef 	. 
	ld d,l			;25c6	55 	U 
	nop			;25c7	00 	. 
	sub b			;25c8	90 	. 
	sub b			;25c9	90 	. 
	sub b			;25ca	90 	. 
	ld d,(hl)			;25cb	56 	V 
	sub b			;25cc	90 	. 
	sub b			;25cd	90 	. 
	sub b			;25ce	90 	. 
	nop			;25cf	00 	. 
	sub l			;25d0	95 	. 
	nop			;25d1	00 	. 
	nop			;25d2	00 	. 
	nop			;25d3	00 	. 
	nop			;25d4	00 	. 
	xor d			;25d5	aa 	. 
	nop			;25d6	00 	. 
	nop			;25d7	00 	. 
	nop			;25d8	00 	. 
l25d9h:
	nop			;25d9	00 	. 
	xor d			;25da	aa 	. 
	nop			;25db	00 	. 
	nop			;25dc	00 	. 
	nop			;25dd	00 	. 
	nop			;25de	00 	. 
	xor d			;25df	aa 	. 
	nop			;25e0	00 	. 
	nop			;25e1	00 	. 
	nop			;25e2	00 	. 
	nop			;25e3	00 	. 
	xor d			;25e4	aa 	. 
	nop			;25e5	00 	. 
	nop			;25e6	00 	. 
	nop			;25e7	00 	. 
	nop			;25e8	00 	. 
	xor d			;25e9	aa 	. 
	nop			;25ea	00 	. 
	nop			;25eb	00 	. 
	nop			;25ec	00 	. 
	nop			;25ed	00 	. 
	xor d			;25ee	aa 	. 
	nop			;25ef	00 	. 
	nop			;25f0	00 	. 
	nop			;25f1	00 	. 
	nop			;25f2	00 	. 
	xor d			;25f3	aa 	. 
	nop			;25f4	00 	. 
	nop			;25f5	00 	. 
	nop			;25f6	00 	. 
	nop			;25f7	00 	. 
	xor d			;25f8	aa 	. 
	add hl,bc			;25f9	09 	. 
	ld d,d			;25fa	52 	R 
	ld c,c			;25fb	49 	I 
	ld b,e			;25fc	43 	C 
	ld c,b			;25fd	48 	H 
	jr nz,l2650h		;25fe	20 50 	  P 
	ld c,h			;2600	4c 	L 
	ld b,c			;2601	41 	A 
	ld d,h			;2602	54 	T 
	ld b,l			;2603	45 	E 
	jr nz,l2626h		;2604	20 20 	    
	jr nz,l2608h		;2606	20 00 	  . 
l2608h:
	nop			;2608	00 	. 
	nop			;2609	00 	. 
	nop			;260a	00 	. 
	nop			;260b	00 	. 
	nop			;260c	00 	. 
	nop			;260d	00 	. 
	nop			;260e	00 	. 
	nop			;260f	00 	. 
	nop			;2610	00 	. 
	nop			;2611	00 	. 
	nop			;2612	00 	. 
	nop			;2613	00 	. 
	nop			;2614	00 	. 
	nop			;2615	00 	. 
	nop			;2616	00 	. 
	nop			;2617	00 	. 
	nop			;2618	00 	. 
	nop			;2619	00 	. 
	nop			;261a	00 	. 
	nop			;261b	00 	. 
	nop			;261c	00 	. 
	nop			;261d	00 	. 
	nop			;261e	00 	. 
	nop			;261f	00 	. 
	nop			;2620	00 	. 
	nop			;2621	00 	. 
	nop			;2622	00 	. 
	nop			;2623	00 	. 
	nop			;2624	00 	. 
	nop			;2625	00 	. 
l2626h:
	ld (0c027h),a		;2626	32 27 c0 	2 ' . 
	call m,07f5ah		;2629	fc 5a 7f 	. Z  
	add a,c			;262c	81 	. 
	dec c			;262d	0d 	. 
	ld bc,l00a6h		;262e	01 a6 00 	. . . 
	nop			;2631	00 	. 
	dec bc			;2632	0b 	. 
	ex af,af'			;2633	08 	. 
	xor d			;2634	aa 	. 
	call p,0f00ch		;2635	f4 0c f0 	. . . 
	ret p			;2638	f0 	. 
	ld e,c			;2639	59 	Y 
	daa			;263a	27 	' 
	inc e			;263b	1c 	. 
	adc a,000h		;263c	ce 00 	. . 
	sbc a,d			;263e	9a 	. 
	rst 28h			;263f	ef 	. 
	rst 28h			;2640	ef 	. 
	rst 28h			;2641	ef 	. 
	rst 28h			;2642	ef 	. 
	ld d,l			;2643	55 	U 
	rst 28h			;2644	ef 	. 
	rst 28h			;2645	ef 	. 
	nop			;2646	00 	. 
	sub b			;2647	90 	. 
	ld h,l			;2648	65 	e 
	sub b			;2649	90 	. 
	sub b			;264a	90 	. 
	sub b			;264b	90 	. 
	sub b			;264c	90 	. 
	ld d,l			;264d	55 	U 
	sub b			;264e	90 	. 
	nop			;264f	00 	. 
l2650h:
	nop			;2650	00 	. 
	nop			;2651	00 	. 
	xor c			;2652	a9 	. 
	nop			;2653	00 	. 
	nop			;2654	00 	. 
	nop			;2655	00 	. 
	nop			;2656	00 	. 
	xor d			;2657	aa 	. 
	nop			;2658	00 	. 
	nop			;2659	00 	. 
	nop			;265a	00 	. 
	nop			;265b	00 	. 
	xor d			;265c	aa 	. 
	nop			;265d	00 	. 
	nop			;265e	00 	. 
	nop			;265f	00 	. 
	nop			;2660	00 	. 
	xor d			;2661	aa 	. 
	nop			;2662	00 	. 
	nop			;2663	00 	. 
	nop			;2664	00 	. 
	nop			;2665	00 	. 
	xor d			;2666	aa 	. 
	nop			;2667	00 	. 
	nop			;2668	00 	. 
	nop			;2669	00 	. 
	nop			;266a	00 	. 
	xor d			;266b	aa 	. 
	nop			;266c	00 	. 
	nop			;266d	00 	. 
	nop			;266e	00 	. 
	nop			;266f	00 	. 
	xor d			;2670	aa 	. 
	add hl,bc			;2671	09 	. 
	ld d,e			;2672	53 	S 
	ld c,l			;2673	4d 	M 
	ld b,c			;2674	41 	A 
	ld c,h			;2675	4c 	L 
	ld c,h			;2676	4c 	L 
	jr nz,l26c9h		;2677	20 50 	  P 
	ld c,h			;2679	4c 	L 
	ld b,c			;267a	41 	A 
	ld d,h			;267b	54 	T 
	ld b,l			;267c	45 	E 
	jr nz,$+34		;267d	20 20 	    
	nop			;267f	00 	. 
	nop			;2680	00 	. 
	nop			;2681	00 	. 
	nop			;2682	00 	. 
	nop			;2683	00 	. 
	nop			;2684	00 	. 
	nop			;2685	00 	. 
	nop			;2686	00 	. 
	nop			;2687	00 	. 
	nop			;2688	00 	. 
	nop			;2689	00 	. 
	nop			;268a	00 	. 
	nop			;268b	00 	. 
	nop			;268c	00 	. 
	nop			;268d	00 	. 
	nop			;268e	00 	. 
	nop			;268f	00 	. 
	nop			;2690	00 	. 
	nop			;2691	00 	. 
	nop			;2692	00 	. 
	nop			;2693	00 	. 
	nop			;2694	00 	. 
	nop			;2695	00 	. 
	nop			;2696	00 	. 
	nop			;2697	00 	. 
	nop			;2698	00 	. 
	nop			;2699	00 	. 
	nop			;269a	00 	. 
	nop			;269b	00 	. 
	nop			;269c	00 	. 
	nop			;269d	00 	. 
	ld (0c027h),a		;269e	32 27 c0 	2 ' . 
	or 05ah		;26a1	f6 5a 	. Z 
	ld a,a			;26a3	7f 	 
	add a,l			;26a4	85 	. 
	ld a,(bc)			;26a5	0a 	. 
	ld bc,l00a6h		;26a6	01 a6 00 	. . . 
	nop			;26a9	00 	. 
	dec bc			;26aa	0b 	. 
	ld a,(bc)			;26ab	0a 	. 
	xor d			;26ac	aa 	. 
	call p,0f00dh		;26ad	f4 0d f0 	. . . 
	ret p			;26b0	f0 	. 
	ld e,c			;26b1	59 	Y 
	ex af,af'			;26b2	08 	. 
	adc a,0dah		;26b3	ce da 	. . 
	nop			;26b5	00 	. 
	sub (hl)			;26b6	96 	. 
	rst 28h			;26b7	ef 	. 
	rst 28h			;26b8	ef 	. 
	rst 28h			;26b9	ef 	. 
	rst 28h			;26ba	ef 	. 
	ld d,l			;26bb	55 	U 
	rst 28h			;26bc	ef 	. 
	rst 28h			;26bd	ef 	. 
	nop			;26be	00 	. 
	sub b			;26bf	90 	. 
	ld h,l			;26c0	65 	e 
	sub b			;26c1	90 	. 
	sub b			;26c2	90 	. 
	sub b			;26c3	90 	. 
	sub b			;26c4	90 	. 
	ld d,l			;26c5	55 	U 
	sub b			;26c6	90 	. 
	nop			;26c7	00 	. 
	nop			;26c8	00 	. 
l26c9h:
	nop			;26c9	00 	. 
	xor c			;26ca	a9 	. 
	nop			;26cb	00 	. 
	nop			;26cc	00 	. 
	nop			;26cd	00 	. 
	nop			;26ce	00 	. 
	xor d			;26cf	aa 	. 
	nop			;26d0	00 	. 
	nop			;26d1	00 	. 
	nop			;26d2	00 	. 
	nop			;26d3	00 	. 
	xor d			;26d4	aa 	. 
	nop			;26d5	00 	. 
	nop			;26d6	00 	. 
	nop			;26d7	00 	. 
	nop			;26d8	00 	. 
	xor d			;26d9	aa 	. 
	nop			;26da	00 	. 
	nop			;26db	00 	. 
	nop			;26dc	00 	. 
	nop			;26dd	00 	. 
	xor d			;26de	aa 	. 
	nop			;26df	00 	. 
	nop			;26e0	00 	. 
	nop			;26e1	00 	. 
	nop			;26e2	00 	. 
	xor d			;26e3	aa 	. 
	nop			;26e4	00 	. 
	nop			;26e5	00 	. 
	nop			;26e6	00 	. 
	nop			;26e7	00 	. 
	xor d			;26e8	aa 	. 
	add hl,bc			;26e9	09 	. 
	ld b,a			;26ea	47 	G 
	ld b,c			;26eb	41 	A 
	ld d,h			;26ec	54 	T 
	ld b,l			;26ed	45 	E 
	ld b,h			;26ee	44 	D 
	jr nz,l2741h		;26ef	20 50 	  P 
	ld c,h			;26f1	4c 	L 
	ld b,c			;26f2	41 	A 
	ld d,h			;26f3	54 	T 
	ld b,l			;26f4	45 	E 
	jr nz,$+34		;26f5	20 20 	    
	nop			;26f7	00 	. 
	nop			;26f8	00 	. 
	nop			;26f9	00 	. 
	nop			;26fa	00 	. 
	nop			;26fb	00 	. 
	nop			;26fc	00 	. 
	nop			;26fd	00 	. 
	nop			;26fe	00 	. 
	nop			;26ff	00 	. 
	nop			;2700	00 	. 
	nop			;2701	00 	. 
	nop			;2702	00 	. 
	nop			;2703	00 	. 
	nop			;2704	00 	. 
	nop			;2705	00 	. 
	nop			;2706	00 	. 
	nop			;2707	00 	. 
	nop			;2708	00 	. 
	nop			;2709	00 	. 
	nop			;270a	00 	. 
	nop			;270b	00 	. 
	nop			;270c	00 	. 
	nop			;270d	00 	. 
	nop			;270e	00 	. 
	nop			;270f	00 	. 
	nop			;2710	00 	. 
	nop			;2711	00 	. 
	nop			;2712	00 	. 
	nop			;2713	00 	. 
	nop			;2714	00 	. 
	nop			;2715	00 	. 
	ld (0c027h),a		;2716	32 27 c0 	2 ' . 
	pop af			;2719	f1 	. 
	ld e,d			;271a	5a 	Z 
	add a,d			;271b	82 	. 
	adc a,l			;271c	8d 	. 
	dec c			;271d	0d 	. 
	ld bc,l00a5h		;271e	01 a5 00 	. . . 
	nop			;2721	00 	. 
	ld c,00eh		;2722	0e 0e 	. . 
	xor d			;2724	aa 	. 
	di			;2725	f3 	. 
	rrca			;2726	0f 	. 
	jp p,059f0h		;2727	f2 f0 59 	. . Y 
	ld sp,0cef8h		;272a	31 f8 ce 	1 . . 
	nop			;272d	00 	. 
	sub (hl)			;272e	96 	. 
	rst 28h			;272f	ef 	. 
	rst 28h			;2730	ef 	. 
	rst 28h			;2731	ef 	. 
	rst 28h			;2732	ef 	. 
	ld d,l			;2733	55 	U 
	rst 28h			;2734	ef 	. 
	rst 28h			;2735	ef 	. 
	nop			;2736	00 	. 
	sub b			;2737	90 	. 
	ld h,l			;2738	65 	e 
	sub b			;2739	90 	. 
	sub b			;273a	90 	. 
	sub b			;273b	90 	. 
	sub b			;273c	90 	. 
	ld d,l			;273d	55 	U 
	sub b			;273e	90 	. 
	nop			;273f	00 	. 
	nop			;2740	00 	. 
l2741h:
	nop			;2741	00 	. 
	xor c			;2742	a9 	. 
	nop			;2743	00 	. 
	nop			;2744	00 	. 
	nop			;2745	00 	. 
	nop			;2746	00 	. 
	xor d			;2747	aa 	. 
	nop			;2748	00 	. 
	nop			;2749	00 	. 
	nop			;274a	00 	. 
	nop			;274b	00 	. 
	xor d			;274c	aa 	. 
	nop			;274d	00 	. 
	nop			;274e	00 	. 
	nop			;274f	00 	. 
	nop			;2750	00 	. 
	xor d			;2751	aa 	. 
	nop			;2752	00 	. 
	nop			;2753	00 	. 
	nop			;2754	00 	. 
	nop			;2755	00 	. 
	xor d			;2756	aa 	. 
	nop			;2757	00 	. 
	nop			;2758	00 	. 
	nop			;2759	00 	. 
	nop			;275a	00 	. 
	xor d			;275b	aa 	. 
	nop			;275c	00 	. 
	nop			;275d	00 	. 
	nop			;275e	00 	. 
	nop			;275f	00 	. 
	xor d			;2760	aa 	. 
	ld c,a			;2761	4f 	O 
	ld d,l			;2762	55 	U 
	ld d,h			;2763	54 	T 
	jr nz,l27bah		;2764	20 54 	  T 
	ld c,a			;2766	4f 	O 
	jr nz,l27b5h		;2767	20 4c 	  L 
	ld d,l			;2769	55 	U 
	ld c,(hl)			;276a	4e 	N 
	ld b,e			;276b	43 	C 
	ld c,b			;276c	48 	H 
	jr nz,$+59		;276d	20 39 	  9 
	ld (04f35h),a		;276f	32 35 4f 	2 5 O 
	ld d,l			;2772	55 	U 
	ld d,h			;2773	54 	T 
	jr nz,l27cah		;2774	20 54 	  T 
	ld c,a			;2776	4f 	O 
	jr nz,l27c5h		;2777	20 4c 	  L 
	ld d,l			;2779	55 	U 
	ld c,(hl)			;277a	4e 	N 
	ld b,e			;277b	43 	C 
	ld c,b			;277c	48 	H 
	jr nz,l27b8h		;277d	20 39 	  9 
	ld (04f35h),a		;277f	32 35 4f 	2 5 O 
	ld d,l			;2782	55 	U 
	ld d,h			;2783	54 	T 
	jr nz,l27dah		;2784	20 54 	  T 
	ld c,a			;2786	4f 	O 
	jr nz,l27d5h		;2787	20 4c 	  L 
	ld d,l			;2789	55 	U 
	ld c,(hl)			;278a	4e 	N 
	ld b,e			;278b	43 	C 
	ld c,b			;278c	48 	H 
	jr nz,l27c8h		;278d	20 39 	  9 
	ld (04f35h),a		;278f	32 35 4f 	2 5 O 
	ld d,l			;2792	55 	U 
	ld d,h			;2793	54 	T 
	jr nz,l27eah		;2794	20 54 	  T 
	ld c,a			;2796	4f 	O 
	jr nz,l27e5h		;2797	20 4c 	  L 
	ld d,l			;2799	55 	U 
	ld c,(hl)			;279a	4e 	N 
	ld b,e			;279b	43 	C 
	ld c,b			;279c	48 	H 
	jr nz,l27d8h		;279d	20 39 	  9 
	ld (04f35h),a		;279f	32 35 4f 	2 5 O 
	ld d,l			;27a2	55 	U 
	ld d,h			;27a3	54 	T 
	jr nz,l27fah		;27a4	20 54 	  T 
	ld c,a			;27a6	4f 	O 
	jr nz,l27f5h		;27a7	20 4c 	  L 
	ld d,l			;27a9	55 	U 
	ld c,(hl)			;27aa	4e 	N 
	ld b,e			;27ab	43 	C 
	ld c,b			;27ac	48 	H 
	jr nz,l27e8h		;27ad	20 39 	  9 
	ld (05435h),a		;27af	32 35 54 	2 5 T 
	ld c,b			;27b2	48 	H 
	ld b,c			;27b3	41 	A 
	ld d,h			;27b4	54 	T 
l27b5h:
	ld d,e			;27b5	53 	S 
	ld b,c			;27b6	41 	A 
	ld c,h			;27b7	4c 	L 
l27b8h:
	ld c,h			;27b8	4c 	L 
	ld b,(hl)			;27b9	46 	F 
l27bah:
	ld c,a			;27ba	4f 	O 
	ld c,h			;27bb	4c 	L 
	ld c,e			;27bc	4b 	K 
	ld d,e			;27bd	53 	S 
	halt			;27be	76 	v 
	halt			;27bf	76 	v 
	halt			;27c0	76 	v 
	halt			;27c1	76 	v 
	halt			;27c2	76 	v 
	rst 38h			;27c3	ff 	. 
	rst 38h			;27c4	ff 	. 
l27c5h:
	rst 38h			;27c5	ff 	. 
	rst 38h			;27c6	ff 	. 
	rst 38h			;27c7	ff 	. 
l27c8h:
	rst 38h			;27c8	ff 	. 
	rst 38h			;27c9	ff 	. 
l27cah:
	rst 38h			;27ca	ff 	. 
	rst 38h			;27cb	ff 	. 
	rst 38h			;27cc	ff 	. 
	rst 38h			;27cd	ff 	. 
	rst 38h			;27ce	ff 	. 
	rst 38h			;27cf	ff 	. 
	rst 38h			;27d0	ff 	. 
	rst 38h			;27d1	ff 	. 
	rst 38h			;27d2	ff 	. 
	rst 38h			;27d3	ff 	. 
	rst 38h			;27d4	ff 	. 
l27d5h:
	rst 38h			;27d5	ff 	. 
	rst 38h			;27d6	ff 	. 
	rst 38h			;27d7	ff 	. 
l27d8h:
	rst 38h			;27d8	ff 	. 
	rst 38h			;27d9	ff 	. 
l27dah:
	rst 38h			;27da	ff 	. 
	rst 38h			;27db	ff 	. 
	rst 38h			;27dc	ff 	. 
	rst 38h			;27dd	ff 	. 
	rst 38h			;27de	ff 	. 
	rst 38h			;27df	ff 	. 
	rst 38h			;27e0	ff 	. 
	rst 38h			;27e1	ff 	. 
	rst 38h			;27e2	ff 	. 
	rst 38h			;27e3	ff 	. 
	rst 38h			;27e4	ff 	. 
l27e5h:
	rst 38h			;27e5	ff 	. 
	rst 38h			;27e6	ff 	. 
	rst 38h			;27e7	ff 	. 
l27e8h:
	rst 38h			;27e8	ff 	. 
	rst 38h			;27e9	ff 	. 
l27eah:
	rst 38h			;27ea	ff 	. 
	rst 38h			;27eb	ff 	. 
	rst 38h			;27ec	ff 	. 
	rst 38h			;27ed	ff 	. 
	rst 38h			;27ee	ff 	. 
	rst 38h			;27ef	ff 	. 
	rst 38h			;27f0	ff 	. 
	rst 38h			;27f1	ff 	. 
	rst 38h			;27f2	ff 	. 
sub_27f3h:
	rst 38h			;27f3	ff 	. 
	rst 38h			;27f4	ff 	. 
l27f5h:
	rst 38h			;27f5	ff 	. 
	rst 38h			;27f6	ff 	. 
	rst 38h			;27f7	ff 	. 
	rst 38h			;27f8	ff 	. 
	rst 38h			;27f9	ff 	. 
l27fah:
	rst 38h			;27fa	ff 	. 
	rst 38h			;27fb	ff 	. 
	rst 38h			;27fc	ff 	. 
	rst 38h			;27fd	ff 	. 
	rst 38h			;27fe	ff 	. 
	rst 38h			;27ff	ff 	. 
	rst 38h			;2800	ff 	. 
l2801h:
	rst 38h			;2801	ff 	. 
	rst 38h			;2802	ff 	. 
	rst 38h			;2803	ff 	. 
	rst 38h			;2804	ff 	. 
	rst 38h			;2805	ff 	. 
	rst 38h			;2806	ff 	. 
	rst 38h			;2807	ff 	. 
	rst 38h			;2808	ff 	. 
	rst 38h			;2809	ff 	. 
	rst 38h			;280a	ff 	. 
	rst 38h			;280b	ff 	. 
	rst 38h			;280c	ff 	. 
	rst 38h			;280d	ff 	. 
	rst 38h			;280e	ff 	. 
	rst 38h			;280f	ff 	. 
	rst 38h			;2810	ff 	. 
	rst 38h			;2811	ff 	. 
	rst 38h			;2812	ff 	. 
	rst 38h			;2813	ff 	. 
	rst 38h			;2814	ff 	. 
	rst 38h			;2815	ff 	. 
	rst 38h			;2816	ff 	. 
	rst 38h			;2817	ff 	. 
	rst 38h			;2818	ff 	. 
	rst 38h			;2819	ff 	. 
	rst 38h			;281a	ff 	. 
	rst 38h			;281b	ff 	. 
	rst 38h			;281c	ff 	. 
	rst 38h			;281d	ff 	. 
	rst 38h			;281e	ff 	. 
	rst 38h			;281f	ff 	. 
	rst 38h			;2820	ff 	. 
	rst 38h			;2821	ff 	. 
	rst 38h			;2822	ff 	. 
	rst 38h			;2823	ff 	. 
	rst 38h			;2824	ff 	. 
	rst 38h			;2825	ff 	. 
	rst 38h			;2826	ff 	. 
	rst 38h			;2827	ff 	. 
	rst 38h			;2828	ff 	. 
	rst 38h			;2829	ff 	. 
	rst 38h			;282a	ff 	. 
	rst 38h			;282b	ff 	. 
	rst 38h			;282c	ff 	. 
	rst 38h			;282d	ff 	. 
	rst 38h			;282e	ff 	. 
	rst 38h			;282f	ff 	. 
	rst 38h			;2830	ff 	. 
	rst 38h			;2831	ff 	. 
	rst 38h			;2832	ff 	. 
	rst 38h			;2833	ff 	. 
	rst 38h			;2834	ff 	. 
	rst 38h			;2835	ff 	. 
	rst 38h			;2836	ff 	. 
	rst 38h			;2837	ff 	. 
l2838h:
	rst 38h			;2838	ff 	. 
	rst 38h			;2839	ff 	. 
l283ah:
	rst 38h			;283a	ff 	. 
	rst 38h			;283b	ff 	. 
	rst 38h			;283c	ff 	. 
	rst 38h			;283d	ff 	. 
	rst 38h			;283e	ff 	. 
	rst 38h			;283f	ff 	. 
	rst 38h			;2840	ff 	. 
	rst 38h			;2841	ff 	. 
	rst 38h			;2842	ff 	. 
	rst 38h			;2843	ff 	. 
	rst 38h			;2844	ff 	. 
	rst 38h			;2845	ff 	. 
	rst 38h			;2846	ff 	. 
	rst 38h			;2847	ff 	. 
	rst 38h			;2848	ff 	. 
	rst 38h			;2849	ff 	. 
	rst 38h			;284a	ff 	. 
	rst 38h			;284b	ff 	. 
	rst 38h			;284c	ff 	. 
	rst 38h			;284d	ff 	. 
	rst 38h			;284e	ff 	. 
	rst 38h			;284f	ff 	. 
	rst 38h			;2850	ff 	. 
	rst 38h			;2851	ff 	. 
	rst 38h			;2852	ff 	. 
	rst 38h			;2853	ff 	. 
	rst 38h			;2854	ff 	. 
	rst 38h			;2855	ff 	. 
	rst 38h			;2856	ff 	. 
	rst 38h			;2857	ff 	. 
	rst 38h			;2858	ff 	. 
	rst 38h			;2859	ff 	. 
	rst 38h			;285a	ff 	. 
	rst 38h			;285b	ff 	. 
	rst 38h			;285c	ff 	. 
	rst 38h			;285d	ff 	. 
	rst 38h			;285e	ff 	. 
	rst 38h			;285f	ff 	. 
	rst 38h			;2860	ff 	. 
	rst 38h			;2861	ff 	. 
	rst 38h			;2862	ff 	. 
	rst 38h			;2863	ff 	. 
	rst 38h			;2864	ff 	. 
	rst 38h			;2865	ff 	. 
	rst 38h			;2866	ff 	. 
	rst 38h			;2867	ff 	. 
	rst 38h			;2868	ff 	. 
	rst 38h			;2869	ff 	. 
	rst 38h			;286a	ff 	. 
	rst 38h			;286b	ff 	. 
	rst 38h			;286c	ff 	. 
	rst 38h			;286d	ff 	. 
	rst 38h			;286e	ff 	. 
	rst 38h			;286f	ff 	. 
	rst 38h			;2870	ff 	. 
	rst 38h			;2871	ff 	. 
	rst 38h			;2872	ff 	. 
	rst 38h			;2873	ff 	. 
	rst 38h			;2874	ff 	. 
l2875h:
	rst 38h			;2875	ff 	. 
	rst 38h			;2876	ff 	. 
	rst 38h			;2877	ff 	. 
	rst 38h			;2878	ff 	. 
	rst 38h			;2879	ff 	. 
	rst 38h			;287a	ff 	. 
	rst 38h			;287b	ff 	. 
	rst 38h			;287c	ff 	. 
	rst 38h			;287d	ff 	. 
	rst 38h			;287e	ff 	. 
	rst 38h			;287f	ff 	. 
	rst 38h			;2880	ff 	. 
	rst 38h			;2881	ff 	. 
	rst 38h			;2882	ff 	. 
	rst 38h			;2883	ff 	. 
	rst 38h			;2884	ff 	. 
	rst 38h			;2885	ff 	. 
	rst 38h			;2886	ff 	. 
	rst 38h			;2887	ff 	. 
	rst 38h			;2888	ff 	. 
	rst 38h			;2889	ff 	. 
	rst 38h			;288a	ff 	. 
	rst 38h			;288b	ff 	. 
	rst 38h			;288c	ff 	. 
	rst 38h			;288d	ff 	. 
	rst 38h			;288e	ff 	. 
	rst 38h			;288f	ff 	. 
	rst 38h			;2890	ff 	. 
	rst 38h			;2891	ff 	. 
	rst 38h			;2892	ff 	. 
	rst 38h			;2893	ff 	. 
	rst 38h			;2894	ff 	. 
	rst 38h			;2895	ff 	. 
	rst 38h			;2896	ff 	. 
	rst 38h			;2897	ff 	. 
	rst 38h			;2898	ff 	. 
	rst 38h			;2899	ff 	. 
	rst 38h			;289a	ff 	. 
	rst 38h			;289b	ff 	. 
	rst 38h			;289c	ff 	. 
	rst 38h			;289d	ff 	. 
	rst 38h			;289e	ff 	. 
	rst 38h			;289f	ff 	. 
	rst 38h			;28a0	ff 	. 
	rst 38h			;28a1	ff 	. 
	rst 38h			;28a2	ff 	. 
	rst 38h			;28a3	ff 	. 
	rst 38h			;28a4	ff 	. 
	rst 38h			;28a5	ff 	. 
	rst 38h			;28a6	ff 	. 
	rst 38h			;28a7	ff 	. 
	rst 38h			;28a8	ff 	. 
	rst 38h			;28a9	ff 	. 
	rst 38h			;28aa	ff 	. 
	rst 38h			;28ab	ff 	. 
	rst 38h			;28ac	ff 	. 
	rst 38h			;28ad	ff 	. 
	rst 38h			;28ae	ff 	. 
	rst 38h			;28af	ff 	. 
	rst 38h			;28b0	ff 	. 
	rst 38h			;28b1	ff 	. 
	rst 38h			;28b2	ff 	. 
	rst 38h			;28b3	ff 	. 
	rst 38h			;28b4	ff 	. 
	rst 38h			;28b5	ff 	. 
	rst 38h			;28b6	ff 	. 
	rst 38h			;28b7	ff 	. 
	rst 38h			;28b8	ff 	. 
	rst 38h			;28b9	ff 	. 
	rst 38h			;28ba	ff 	. 
	rst 38h			;28bb	ff 	. 
	rst 38h			;28bc	ff 	. 
	rst 38h			;28bd	ff 	. 
	rst 38h			;28be	ff 	. 
	rst 38h			;28bf	ff 	. 
	rst 38h			;28c0	ff 	. 
	rst 38h			;28c1	ff 	. 
	rst 38h			;28c2	ff 	. 
	rst 38h			;28c3	ff 	. 
	rst 38h			;28c4	ff 	. 
	rst 38h			;28c5	ff 	. 
	rst 38h			;28c6	ff 	. 
	rst 38h			;28c7	ff 	. 
	rst 38h			;28c8	ff 	. 
	rst 38h			;28c9	ff 	. 
	rst 38h			;28ca	ff 	. 
	rst 38h			;28cb	ff 	. 
	rst 38h			;28cc	ff 	. 
	rst 38h			;28cd	ff 	. 
	rst 38h			;28ce	ff 	. 
	rst 38h			;28cf	ff 	. 
	rst 38h			;28d0	ff 	. 
	rst 38h			;28d1	ff 	. 
	rst 38h			;28d2	ff 	. 
	rst 38h			;28d3	ff 	. 
	rst 38h			;28d4	ff 	. 
	rst 38h			;28d5	ff 	. 
	rst 38h			;28d6	ff 	. 
	rst 38h			;28d7	ff 	. 
	rst 38h			;28d8	ff 	. 
	rst 38h			;28d9	ff 	. 
	rst 38h			;28da	ff 	. 
	rst 38h			;28db	ff 	. 
	rst 38h			;28dc	ff 	. 
	rst 38h			;28dd	ff 	. 
	rst 38h			;28de	ff 	. 
	rst 38h			;28df	ff 	. 
	rst 38h			;28e0	ff 	. 
	rst 38h			;28e1	ff 	. 
	rst 38h			;28e2	ff 	. 
	rst 38h			;28e3	ff 	. 
	rst 38h			;28e4	ff 	. 
	rst 38h			;28e5	ff 	. 
	rst 38h			;28e6	ff 	. 
	rst 38h			;28e7	ff 	. 
	rst 38h			;28e8	ff 	. 
	rst 38h			;28e9	ff 	. 
	rst 38h			;28ea	ff 	. 
	rst 38h			;28eb	ff 	. 
	rst 38h			;28ec	ff 	. 
	rst 38h			;28ed	ff 	. 
	rst 38h			;28ee	ff 	. 
	rst 38h			;28ef	ff 	. 
	rst 38h			;28f0	ff 	. 
	rst 38h			;28f1	ff 	. 
	rst 38h			;28f2	ff 	. 
	rst 38h			;28f3	ff 	. 
	rst 38h			;28f4	ff 	. 
	rst 38h			;28f5	ff 	. 
	rst 38h			;28f6	ff 	. 
	rst 38h			;28f7	ff 	. 
	rst 38h			;28f8	ff 	. 
	rst 38h			;28f9	ff 	. 
	rst 38h			;28fa	ff 	. 
	rst 38h			;28fb	ff 	. 
	rst 38h			;28fc	ff 	. 
	rst 38h			;28fd	ff 	. 
	rst 38h			;28fe	ff 	. 
	rst 38h			;28ff	ff 	. 
	rst 38h			;2900	ff 	. 
	rst 38h			;2901	ff 	. 
	rst 38h			;2902	ff 	. 
	rst 38h			;2903	ff 	. 
	rst 38h			;2904	ff 	. 
	rst 38h			;2905	ff 	. 
	rst 38h			;2906	ff 	. 
	rst 38h			;2907	ff 	. 
	rst 38h			;2908	ff 	. 
	rst 38h			;2909	ff 	. 
	rst 38h			;290a	ff 	. 
	rst 38h			;290b	ff 	. 
	rst 38h			;290c	ff 	. 
	rst 38h			;290d	ff 	. 
	rst 38h			;290e	ff 	. 
	rst 38h			;290f	ff 	. 
	rst 38h			;2910	ff 	. 
	rst 38h			;2911	ff 	. 
	rst 38h			;2912	ff 	. 
	rst 38h			;2913	ff 	. 
	rst 38h			;2914	ff 	. 
	rst 38h			;2915	ff 	. 
	rst 38h			;2916	ff 	. 
	rst 38h			;2917	ff 	. 
	rst 38h			;2918	ff 	. 
	rst 38h			;2919	ff 	. 
	rst 38h			;291a	ff 	. 
	rst 38h			;291b	ff 	. 
	rst 38h			;291c	ff 	. 
	rst 38h			;291d	ff 	. 
	rst 38h			;291e	ff 	. 
	rst 38h			;291f	ff 	. 
	rst 38h			;2920	ff 	. 
	rst 38h			;2921	ff 	. 
	rst 38h			;2922	ff 	. 
	rst 38h			;2923	ff 	. 
	rst 38h			;2924	ff 	. 
	rst 38h			;2925	ff 	. 
	rst 38h			;2926	ff 	. 
	rst 38h			;2927	ff 	. 
	rst 38h			;2928	ff 	. 
	rst 38h			;2929	ff 	. 
	rst 38h			;292a	ff 	. 
	rst 38h			;292b	ff 	. 
	rst 38h			;292c	ff 	. 
	rst 38h			;292d	ff 	. 
	rst 38h			;292e	ff 	. 
	rst 38h			;292f	ff 	. 
	rst 38h			;2930	ff 	. 
	rst 38h			;2931	ff 	. 
	rst 38h			;2932	ff 	. 
	rst 38h			;2933	ff 	. 
	rst 38h			;2934	ff 	. 
	rst 38h			;2935	ff 	. 
	rst 38h			;2936	ff 	. 
	rst 38h			;2937	ff 	. 
	rst 38h			;2938	ff 	. 
	rst 38h			;2939	ff 	. 
	rst 38h			;293a	ff 	. 
	rst 38h			;293b	ff 	. 
	rst 38h			;293c	ff 	. 
	rst 38h			;293d	ff 	. 
	rst 38h			;293e	ff 	. 
	rst 38h			;293f	ff 	. 
	rst 38h			;2940	ff 	. 
	rst 38h			;2941	ff 	. 
	rst 38h			;2942	ff 	. 
	rst 38h			;2943	ff 	. 
	rst 38h			;2944	ff 	. 
	rst 38h			;2945	ff 	. 
	rst 38h			;2946	ff 	. 
	rst 38h			;2947	ff 	. 
	rst 38h			;2948	ff 	. 
	rst 38h			;2949	ff 	. 
	rst 38h			;294a	ff 	. 
	rst 38h			;294b	ff 	. 
	rst 38h			;294c	ff 	. 
	rst 38h			;294d	ff 	. 
	rst 38h			;294e	ff 	. 
	rst 38h			;294f	ff 	. 
	rst 38h			;2950	ff 	. 
	rst 38h			;2951	ff 	. 
	rst 38h			;2952	ff 	. 
	rst 38h			;2953	ff 	. 
	rst 38h			;2954	ff 	. 
	rst 38h			;2955	ff 	. 
	rst 38h			;2956	ff 	. 
	rst 38h			;2957	ff 	. 
	rst 38h			;2958	ff 	. 
	rst 38h			;2959	ff 	. 
	rst 38h			;295a	ff 	. 
	rst 38h			;295b	ff 	. 
	rst 38h			;295c	ff 	. 
	rst 38h			;295d	ff 	. 
	rst 38h			;295e	ff 	. 
	rst 38h			;295f	ff 	. 
	rst 38h			;2960	ff 	. 
	rst 38h			;2961	ff 	. 
	rst 38h			;2962	ff 	. 
	rst 38h			;2963	ff 	. 
	rst 38h			;2964	ff 	. 
	rst 38h			;2965	ff 	. 
	rst 38h			;2966	ff 	. 
	rst 38h			;2967	ff 	. 
	rst 38h			;2968	ff 	. 
	rst 38h			;2969	ff 	. 
	rst 38h			;296a	ff 	. 
	rst 38h			;296b	ff 	. 
	rst 38h			;296c	ff 	. 
	rst 38h			;296d	ff 	. 
	rst 38h			;296e	ff 	. 
	rst 38h			;296f	ff 	. 
	rst 38h			;2970	ff 	. 
	rst 38h			;2971	ff 	. 
	rst 38h			;2972	ff 	. 
	rst 38h			;2973	ff 	. 
	rst 38h			;2974	ff 	. 
	rst 38h			;2975	ff 	. 
	rst 38h			;2976	ff 	. 
	rst 38h			;2977	ff 	. 
	rst 38h			;2978	ff 	. 
	rst 38h			;2979	ff 	. 
	rst 38h			;297a	ff 	. 
	rst 38h			;297b	ff 	. 
	rst 38h			;297c	ff 	. 
	rst 38h			;297d	ff 	. 
	rst 38h			;297e	ff 	. 
	rst 38h			;297f	ff 	. 
	rst 38h			;2980	ff 	. 
	rst 38h			;2981	ff 	. 
	rst 38h			;2982	ff 	. 
	rst 38h			;2983	ff 	. 
	rst 38h			;2984	ff 	. 
	rst 38h			;2985	ff 	. 
	rst 38h			;2986	ff 	. 
	rst 38h			;2987	ff 	. 
	rst 38h			;2988	ff 	. 
	rst 38h			;2989	ff 	. 
	rst 38h			;298a	ff 	. 
	rst 38h			;298b	ff 	. 
	rst 38h			;298c	ff 	. 
	rst 38h			;298d	ff 	. 
	rst 38h			;298e	ff 	. 
	rst 38h			;298f	ff 	. 
	rst 38h			;2990	ff 	. 
	rst 38h			;2991	ff 	. 
	rst 38h			;2992	ff 	. 
	rst 38h			;2993	ff 	. 
	rst 38h			;2994	ff 	. 
	rst 38h			;2995	ff 	. 
	rst 38h			;2996	ff 	. 
	rst 38h			;2997	ff 	. 
	rst 38h			;2998	ff 	. 
	rst 38h			;2999	ff 	. 
l299ah:
	nop			;299a	00 	. 
	cp a			;299b	bf 	. 
	rst 28h			;299c	ef 	. 
	nop			;299d	00 	. 
	rst 38h			;299e	ff 	. 
	rst 38h			;299f	ff 	. 
	rst 38h			;29a0	ff 	. 
	rst 38h			;29a1	ff 	. 
	rst 38h			;29a2	ff 	. 
	rst 38h			;29a3	ff 	. 
	rst 38h			;29a4	ff 	. 
	rst 38h			;29a5	ff 	. 
	rst 38h			;29a6	ff 	. 
	rst 38h			;29a7	ff 	. 
	rst 38h			;29a8	ff 	. 
	rst 38h			;29a9	ff 	. 
	rst 38h			;29aa	ff 	. 
	rst 38h			;29ab	ff 	. 
	rst 38h			;29ac	ff 	. 
	rst 38h			;29ad	ff 	. 
	rst 38h			;29ae	ff 	. 
	rst 38h			;29af	ff 	. 
	rst 38h			;29b0	ff 	. 
	rst 38h			;29b1	ff 	. 
	rst 38h			;29b2	ff 	. 
	rst 38h			;29b3	ff 	. 
	rst 38h			;29b4	ff 	. 
	rst 38h			;29b5	ff 	. 
	rst 38h			;29b6	ff 	. 
	rst 38h			;29b7	ff 	. 
	rst 38h			;29b8	ff 	. 
	rst 38h			;29b9	ff 	. 
	rst 38h			;29ba	ff 	. 
	rst 38h			;29bb	ff 	. 
	rst 38h			;29bc	ff 	. 
	rst 38h			;29bd	ff 	. 
	rst 38h			;29be	ff 	. 
	rst 38h			;29bf	ff 	. 
	rst 38h			;29c0	ff 	. 
	rst 38h			;29c1	ff 	. 
	rst 38h			;29c2	ff 	. 
	rst 38h			;29c3	ff 	. 
	rst 38h			;29c4	ff 	. 
	rst 38h			;29c5	ff 	. 
	rst 38h			;29c6	ff 	. 
	rst 38h			;29c7	ff 	. 
	rst 38h			;29c8	ff 	. 
	rst 38h			;29c9	ff 	. 
	rst 38h			;29ca	ff 	. 
	rst 38h			;29cb	ff 	. 
	rst 38h			;29cc	ff 	. 
	rst 38h			;29cd	ff 	. 
	rst 38h			;29ce	ff 	. 
	rst 38h			;29cf	ff 	. 
	rst 38h			;29d0	ff 	. 
	rst 38h			;29d1	ff 	. 
	rst 38h			;29d2	ff 	. 
	rst 38h			;29d3	ff 	. 
	rst 38h			;29d4	ff 	. 
	rst 38h			;29d5	ff 	. 
	rst 38h			;29d6	ff 	. 
	rst 38h			;29d7	ff 	. 
	rst 38h			;29d8	ff 	. 
	rst 38h			;29d9	ff 	. 
	rst 38h			;29da	ff 	. 
	rst 38h			;29db	ff 	. 
	rst 38h			;29dc	ff 	. 
	rst 38h			;29dd	ff 	. 
	rst 38h			;29de	ff 	. 
	rst 38h			;29df	ff 	. 
	rst 38h			;29e0	ff 	. 
	rst 38h			;29e1	ff 	. 
	rst 38h			;29e2	ff 	. 
	rst 38h			;29e3	ff 	. 
	rst 38h			;29e4	ff 	. 
	rst 38h			;29e5	ff 	. 
	rst 38h			;29e6	ff 	. 
	rst 38h			;29e7	ff 	. 
	rst 38h			;29e8	ff 	. 
	rst 38h			;29e9	ff 	. 
	rst 38h			;29ea	ff 	. 
	rst 38h			;29eb	ff 	. 
	rst 38h			;29ec	ff 	. 
	rst 38h			;29ed	ff 	. 
	rst 38h			;29ee	ff 	. 
	rst 38h			;29ef	ff 	. 
	rst 38h			;29f0	ff 	. 
	rst 38h			;29f1	ff 	. 
	rst 38h			;29f2	ff 	. 
	rst 38h			;29f3	ff 	. 
	rst 38h			;29f4	ff 	. 
	rst 38h			;29f5	ff 	. 
	rst 38h			;29f6	ff 	. 
	jr nz,l2a09h		;29f7	20 10 	  . 
	ld bc,00103h		;29f9	01 03 01 	. . . 
	dec sp			;29fc	3b 	; 
	ld bc,l007ch		;29fd	01 7c 00 	. | . 
	nop			;2a00	00 	. 
	nop			;2a01	00 	. 
	jr nz,l2a24h		;2a02	20 20 	    
	jr nz,l2a26h		;2a04	20 20 	    
	jr nz,l2a28h		;2a06	20 20 	    
	rst 38h			;2a08	ff 	. 
l2a09h:
	rst 38h			;2a09	ff 	. 
	rst 38h			;2a0a	ff 	. 
	rst 38h			;2a0b	ff 	. 
	rst 38h			;2a0c	ff 	. 
	rst 38h			;2a0d	ff 	. 
	rst 38h			;2a0e	ff 	. 
	rst 38h			;2a0f	ff 	. 
	rst 38h			;2a10	ff 	. 
	rst 38h			;2a11	ff 	. 
	rst 38h			;2a12	ff 	. 
	rst 38h			;2a13	ff 	. 
	rst 38h			;2a14	ff 	. 
	rst 38h			;2a15	ff 	. 
	rst 38h			;2a16	ff 	. 
	rst 38h			;2a17	ff 	. 
	rst 38h			;2a18	ff 	. 
	rst 38h			;2a19	ff 	. 
	rst 38h			;2a1a	ff 	. 
	rst 38h			;2a1b	ff 	. 
	rst 38h			;2a1c	ff 	. 
	rst 38h			;2a1d	ff 	. 
	rst 38h			;2a1e	ff 	. 
	rst 38h			;2a1f	ff 	. 
	rst 38h			;2a20	ff 	. 
	rst 38h			;2a21	ff 	. 
	rst 38h			;2a22	ff 	. 
	rst 38h			;2a23	ff 	. 
l2a24h:
	rst 38h			;2a24	ff 	. 
	rst 38h			;2a25	ff 	. 
l2a26h:
	rst 38h			;2a26	ff 	. 
	rst 38h			;2a27	ff 	. 
l2a28h:
	rst 38h			;2a28	ff 	. 
	rst 38h			;2a29	ff 	. 
	rst 38h			;2a2a	ff 	. 
	rst 38h			;2a2b	ff 	. 
	rst 38h			;2a2c	ff 	. 
	rst 38h			;2a2d	ff 	. 
	rst 38h			;2a2e	ff 	. 
	rst 38h			;2a2f	ff 	. 
	rst 38h			;2a30	ff 	. 
	rst 38h			;2a31	ff 	. 
	rst 38h			;2a32	ff 	. 
	rst 38h			;2a33	ff 	. 
	rst 38h			;2a34	ff 	. 
	rst 38h			;2a35	ff 	. 
	rst 38h			;2a36	ff 	. 
	rst 38h			;2a37	ff 	. 
	rst 38h			;2a38	ff 	. 
	rst 38h			;2a39	ff 	. 
	rst 38h			;2a3a	ff 	. 
	rst 38h			;2a3b	ff 	. 
	rst 38h			;2a3c	ff 	. 
	rst 38h			;2a3d	ff 	. 
	rst 38h			;2a3e	ff 	. 
	rst 38h			;2a3f	ff 	. 
	rst 38h			;2a40	ff 	. 
	rst 38h			;2a41	ff 	. 
	rst 38h			;2a42	ff 	. 
	rst 38h			;2a43	ff 	. 
	rst 38h			;2a44	ff 	. 
	rst 38h			;2a45	ff 	. 
	rst 38h			;2a46	ff 	. 
	rst 38h			;2a47	ff 	. 
	rst 38h			;2a48	ff 	. 
	rst 38h			;2a49	ff 	. 
	rst 38h			;2a4a	ff 	. 
	rst 38h			;2a4b	ff 	. 
	rst 38h			;2a4c	ff 	. 
	rst 38h			;2a4d	ff 	. 
	rst 38h			;2a4e	ff 	. 
	rst 38h			;2a4f	ff 	. 
	rst 38h			;2a50	ff 	. 
	rst 38h			;2a51	ff 	. 
	rst 38h			;2a52	ff 	. 
	rst 38h			;2a53	ff 	. 
	rst 38h			;2a54	ff 	. 
	rst 38h			;2a55	ff 	. 
	rst 38h			;2a56	ff 	. 
	rst 38h			;2a57	ff 	. 
	rst 38h			;2a58	ff 	. 
	rst 38h			;2a59	ff 	. 
	rst 38h			;2a5a	ff 	. 
	rst 38h			;2a5b	ff 	. 
	rst 38h			;2a5c	ff 	. 
	rst 38h			;2a5d	ff 	. 
	rst 38h			;2a5e	ff 	. 
	rst 38h			;2a5f	ff 	. 
	rst 38h			;2a60	ff 	. 
	rst 38h			;2a61	ff 	. 
	rst 38h			;2a62	ff 	. 
	rst 38h			;2a63	ff 	. 
	rst 38h			;2a64	ff 	. 
	rst 38h			;2a65	ff 	. 
	rst 38h			;2a66	ff 	. 
	rst 38h			;2a67	ff 	. 
	rst 38h			;2a68	ff 	. 
	rst 38h			;2a69	ff 	. 
	rst 38h			;2a6a	ff 	. 
	rst 38h			;2a6b	ff 	. 
	rst 38h			;2a6c	ff 	. 
	rst 38h			;2a6d	ff 	. 
	rst 38h			;2a6e	ff 	. 
	rst 38h			;2a6f	ff 	. 
	rst 38h			;2a70	ff 	. 
	rst 38h			;2a71	ff 	. 
	rst 38h			;2a72	ff 	. 
	rst 38h			;2a73	ff 	. 
	rst 38h			;2a74	ff 	. 
	rst 38h			;2a75	ff 	. 
	rst 38h			;2a76	ff 	. 
	rst 38h			;2a77	ff 	. 
	rst 38h			;2a78	ff 	. 
	rst 38h			;2a79	ff 	. 
	rst 38h			;2a7a	ff 	. 
	rst 38h			;2a7b	ff 	. 
	rst 38h			;2a7c	ff 	. 
	rst 38h			;2a7d	ff 	. 
	rst 38h			;2a7e	ff 	. 
	rst 38h			;2a7f	ff 	. 
	rst 38h			;2a80	ff 	. 
	rst 38h			;2a81	ff 	. 
	rst 38h			;2a82	ff 	. 
	rst 38h			;2a83	ff 	. 
	rst 38h			;2a84	ff 	. 
	rst 38h			;2a85	ff 	. 
	rst 38h			;2a86	ff 	. 
	rst 38h			;2a87	ff 	. 
	rst 38h			;2a88	ff 	. 
	rst 38h			;2a89	ff 	. 
	rst 38h			;2a8a	ff 	. 
	rst 38h			;2a8b	ff 	. 
	rst 38h			;2a8c	ff 	. 
	rst 38h			;2a8d	ff 	. 
	rst 38h			;2a8e	ff 	. 
	rst 38h			;2a8f	ff 	. 
	rst 38h			;2a90	ff 	. 
	rst 38h			;2a91	ff 	. 
	rst 38h			;2a92	ff 	. 
	rst 38h			;2a93	ff 	. 
	rst 38h			;2a94	ff 	. 
	rst 38h			;2a95	ff 	. 
	rst 38h			;2a96	ff 	. 
	rst 38h			;2a97	ff 	. 
	rst 38h			;2a98	ff 	. 
	rst 38h			;2a99	ff 	. 
	rst 38h			;2a9a	ff 	. 
	rst 38h			;2a9b	ff 	. 
	rst 38h			;2a9c	ff 	. 
	rst 38h			;2a9d	ff 	. 
	rst 38h			;2a9e	ff 	. 
	rst 38h			;2a9f	ff 	. 
	rst 38h			;2aa0	ff 	. 
	rst 38h			;2aa1	ff 	. 
	rst 38h			;2aa2	ff 	. 
	rst 38h			;2aa3	ff 	. 
	rst 38h			;2aa4	ff 	. 
	rst 38h			;2aa5	ff 	. 
	rst 38h			;2aa6	ff 	. 
	rst 38h			;2aa7	ff 	. 
	rst 38h			;2aa8	ff 	. 
	rst 38h			;2aa9	ff 	. 
	rst 38h			;2aaa	ff 	. 
	rst 38h			;2aab	ff 	. 
	rst 38h			;2aac	ff 	. 
	rst 38h			;2aad	ff 	. 
	rst 38h			;2aae	ff 	. 
	rst 38h			;2aaf	ff 	. 
	rst 38h			;2ab0	ff 	. 
	rst 38h			;2ab1	ff 	. 
	rst 38h			;2ab2	ff 	. 
	rst 38h			;2ab3	ff 	. 
	rst 38h			;2ab4	ff 	. 
	rst 38h			;2ab5	ff 	. 
	rst 38h			;2ab6	ff 	. 
	rst 38h			;2ab7	ff 	. 
	rst 38h			;2ab8	ff 	. 
	rst 38h			;2ab9	ff 	. 
	rst 38h			;2aba	ff 	. 
	rst 38h			;2abb	ff 	. 
	rst 38h			;2abc	ff 	. 
	rst 38h			;2abd	ff 	. 
	rst 38h			;2abe	ff 	. 
	rst 38h			;2abf	ff 	. 
	rst 38h			;2ac0	ff 	. 
	rst 38h			;2ac1	ff 	. 
	rst 38h			;2ac2	ff 	. 
	rst 38h			;2ac3	ff 	. 
	rst 38h			;2ac4	ff 	. 
	rst 38h			;2ac5	ff 	. 
	rst 38h			;2ac6	ff 	. 
	rst 38h			;2ac7	ff 	. 
	rst 38h			;2ac8	ff 	. 
	rst 38h			;2ac9	ff 	. 
	rst 38h			;2aca	ff 	. 
	rst 38h			;2acb	ff 	. 
	rst 38h			;2acc	ff 	. 
	jp p,0ffffh		;2acd	f2 ff ff 	. . . 
	rst 38h			;2ad0	ff 	. 
	rst 38h			;2ad1	ff 	. 
	rst 38h			;2ad2	ff 	. 
	rst 38h			;2ad3	ff 	. 
	rst 38h			;2ad4	ff 	. 
	cp 06eh		;2ad5	fe 6e 	. n 
	sbc a,04eh		;2ad7	de 4e 	. N 
	cp (hl)			;2ad9	be 	. 
	ld l,09eh		;2ada	2e 9e 	. . 
	ld c,07eh		;2adc	0e 7e 	. ~ 
	xor 05eh		;2ade	ee 5e 	. ^ 
	adc a,03eh		;2ae0	ce 3e 	. > 
	xor (hl)			;2ae2	ae 	. 
	ld e,08eh		;2ae3	1e 8e 	. . 
	cp 06eh		;2ae5	fe 6e 	. n 
	sbc a,04eh		;2ae7	de 4e 	. N 
	cp (hl)			;2ae9	be 	. 
	ld l,09eh		;2aea	2e 9e 	. . 
	ld c,07eh		;2aec	0e 7e 	. ~ 
	xor 05eh		;2aee	ee 5e 	. ^ 
	adc a,03eh		;2af0	ce 3e 	. > 
	xor (hl)			;2af2	ae 	. 
	ld e,08eh		;2af3	1e 8e 	. . 
	cp 06eh		;2af5	fe 6e 	. n 
	sbc a,04eh		;2af7	de 4e 	. N 
	cp (hl)			;2af9	be 	. 
	ld l,09eh		;2afa	2e 9e 	. . 
	ld c,07eh		;2afc	0e 7e 	. ~ 
	xor 05eh		;2afe	ee 5e 	. ^ 
	adc a,03eh		;2b00	ce 3e 	. > 
	xor (hl)			;2b02	ae 	. 
	ld e,08eh		;2b03	1e 8e 	. . 
	cp 06eh		;2b05	fe 6e 	. n 
	sbc a,0ffh		;2b07	de ff 	. . 
	rst 38h			;2b09	ff 	. 
	rst 38h			;2b0a	ff 	. 
	pop af			;2b0b	f1 	. 
	rst 38h			;2b0c	ff 	. 
	rst 38h			;2b0d	ff 	. 
	ld c,(hl)			;2b0e	4e 	N 
	cp (hl)			;2b0f	be 	. 
	ld l,09eh		;2b10	2e 9e 	. . 
	ld c,07eh		;2b12	0e 7e 	. ~ 
	xor 05eh		;2b14	ee 5e 	. ^ 
	adc a,03eh		;2b16	ce 3e 	. > 
	xor (hl)			;2b18	ae 	. 
	ld e,08eh		;2b19	1e 8e 	. . 
	cp 06eh		;2b1b	fe 6e 	. n 
	sbc a,04eh		;2b1d	de 4e 	. N 
	cp (hl)			;2b1f	be 	. 
	ld l,09eh		;2b20	2e 9e 	. . 
	ld c,07eh		;2b22	0e 7e 	. ~ 
	xor 05eh		;2b24	ee 5e 	. ^ 
	adc a,03eh		;2b26	ce 3e 	. > 
	xor (hl)			;2b28	ae 	. 
	ld e,08eh		;2b29	1e 8e 	. . 
	cp 06eh		;2b2b	fe 6e 	. n 
	rst 38h			;2b2d	ff 	. 
	rst 38h			;2b2e	ff 	. 
	rst 38h			;2b2f	ff 	. 
	rst 38h			;2b30	ff 	. 
	rst 38h			;2b31	ff 	. 
	rst 38h			;2b32	ff 	. 
	rst 38h			;2b33	ff 	. 
	rst 38h			;2b34	ff 	. 
	rst 38h			;2b35	ff 	. 
	rst 38h			;2b36	ff 	. 
	rst 38h			;2b37	ff 	. 
	rst 38h			;2b38	ff 	. 
	rst 38h			;2b39	ff 	. 
	rst 38h			;2b3a	ff 	. 
	rst 38h			;2b3b	ff 	. 
	rst 38h			;2b3c	ff 	. 
	rst 38h			;2b3d	ff 	. 
	rst 38h			;2b3e	ff 	. 
	rst 38h			;2b3f	ff 	. 
	rst 38h			;2b40	ff 	. 
	rst 38h			;2b41	ff 	. 
	rst 38h			;2b42	ff 	. 
	rst 38h			;2b43	ff 	. 
	rst 38h			;2b44	ff 	. 
	rst 38h			;2b45	ff 	. 
	rst 38h			;2b46	ff 	. 
	rst 38h			;2b47	ff 	. 
	rst 38h			;2b48	ff 	. 
	rst 38h			;2b49	ff 	. 
	rst 38h			;2b4a	ff 	. 
	rst 38h			;2b4b	ff 	. 
	pop af			;2b4c	f1 	. 
	rst 38h			;2b4d	ff 	. 
	rst 38h			;2b4e	ff 	. 
	rst 38h			;2b4f	ff 	. 
	rst 38h			;2b50	ff 	. 
	rst 38h			;2b51	ff 	. 
	rst 38h			;2b52	ff 	. 
	rst 38h			;2b53	ff 	. 
	rst 38h			;2b54	ff 	. 
	rst 38h			;2b55	ff 	. 
	cp 0fch		;2b56	fe fc 	. . 
	ei			;2b58	fb 	. 
	ld sp,hl			;2b59	f9 	. 
	ret m			;2b5a	f8 	. 
	or 0f5h		;2b5b	f6 f5 	. . 
	di			;2b5d	f3 	. 
	pop af			;2b5e	f1 	. 
	ret p			;2b5f	f0 	. 
	xor 0edh		;2b60	ee ed 	. . 
	ex de,hl			;2b62	eb 	. 
	jp pe,0e6e8h		;2b63	ea e8 e6 	. . . 
	push hl			;2b66	e5 	. 
	ex (sp),hl			;2b67	e3 	. 
	jp po,0dfe0h		;2b68	e2 e0 df 	. . . 
	defb 0ddh,0dch,0dah	;illegal sequence		;2b6b	dd dc da 	. . . 
	ret c			;2b6e	d8 	. 
	rst 10h			;2b6f	d7 	. 
	push de			;2b70	d5 	. 
	call nc,0d1d2h		;2b71	d4 d2 d1 	. . . 
	rst 8			;2b74	cf 	. 
	call 0cacch		;2b75	cd cc ca 	. . . 
	ret			;2b78	c9 	. 
	rst 0			;2b79	c7 	. 
	add a,0c4h		;2b7a	c6 c4 	. . 
	jp 0bfc1h		;2b7c	c3 c1 bf 	. . . 
	cp (hl)			;2b7f	be 	. 
	cp h			;2b80	bc 	. 
	cp e			;2b81	bb 	. 
	cp c			;2b82	b9 	. 
	cp b			;2b83	b8 	. 
	or (hl)			;2b84	b6 	. 
	or h			;2b85	b4 	. 
	or e			;2b86	b3 	. 
	or c			;2b87	b1 	. 
	rst 38h			;2b88	ff 	. 
	rst 38h			;2b89	ff 	. 
	rst 38h			;2b8a	ff 	. 
	rst 38h			;2b8b	ff 	. 
	rst 38h			;2b8c	ff 	. 
	rst 38h			;2b8d	ff 	. 
	or b			;2b8e	b0 	. 
	xor (hl)			;2b8f	ae 	. 
	xor l			;2b90	ad 	. 
	xor e			;2b91	ab 	. 
	xor d			;2b92	aa 	. 
	xor b			;2b93	a8 	. 
	and (hl)			;2b94	a6 	. 
	and l			;2b95	a5 	. 
	and e			;2b96	a3 	. 
	and d			;2b97	a2 	. 
	and b			;2b98	a0 	. 
	sbc a,a			;2b99	9f 	. 
	sbc a,l			;2b9a	9d 	. 
	sbc a,e			;2b9b	9b 	. 
	sbc a,d			;2b9c	9a 	. 
	sbc a,b			;2b9d	98 	. 
	sub a			;2b9e	97 	. 
	sub l			;2b9f	95 	. 
	sub h			;2ba0	94 	. 
	sub d			;2ba1	92 	. 
	sub c			;2ba2	91 	. 
	adc a,a			;2ba3	8f 	. 
	adc a,l			;2ba4	8d 	. 
	adc a,h			;2ba5	8c 	. 
	adc a,d			;2ba6	8a 	. 
	adc a,c			;2ba7	89 	. 
	add a,a			;2ba8	87 	. 
	add a,(hl)			;2ba9	86 	. 
	add a,h			;2baa	84 	. 
	add a,d			;2bab	82 	. 
	add a,c			;2bac	81 	. 
	rst 38h			;2bad	ff 	. 
	rst 38h			;2bae	ff 	. 
	rst 38h			;2baf	ff 	. 
	rst 38h			;2bb0	ff 	. 
	rst 38h			;2bb1	ff 	. 
	rst 38h			;2bb2	ff 	. 
	rst 38h			;2bb3	ff 	. 
	rst 38h			;2bb4	ff 	. 
	rst 38h			;2bb5	ff 	. 
	rst 38h			;2bb6	ff 	. 
	rst 38h			;2bb7	ff 	. 
	rst 38h			;2bb8	ff 	. 
	rst 38h			;2bb9	ff 	. 
	rst 38h			;2bba	ff 	. 
	rst 38h			;2bbb	ff 	. 
	rst 38h			;2bbc	ff 	. 
	rst 38h			;2bbd	ff 	. 
	rst 38h			;2bbe	ff 	. 
	rst 38h			;2bbf	ff 	. 
	rst 38h			;2bc0	ff 	. 
	rst 38h			;2bc1	ff 	. 
	rst 38h			;2bc2	ff 	. 
	rst 38h			;2bc3	ff 	. 
	rst 38h			;2bc4	ff 	. 
	rst 38h			;2bc5	ff 	. 
	rst 38h			;2bc6	ff 	. 
	rst 38h			;2bc7	ff 	. 
	rst 38h			;2bc8	ff 	. 
	rst 38h			;2bc9	ff 	. 
	rst 38h			;2bca	ff 	. 
	rst 38h			;2bcb	ff 	. 
	rst 38h			;2bcc	ff 	. 
	rst 18h			;2bcd	df 	. 
	rst 38h			;2bce	ff 	. 
	ccf			;2bcf	3f 	? 
	rrca			;2bd0	0f 	. 
	dec sp			;2bd1	3b 	; 
	rst 38h			;2bd2	ff 	. 
	rst 38h			;2bd3	ff 	. 
	rst 38h			;2bd4	ff 	. 
	rst 38h			;2bd5	ff 	. 
	rst 38h			;2bd6	ff 	. 
	rst 38h			;2bd7	ff 	. 
	rst 38h			;2bd8	ff 	. 
	rst 38h			;2bd9	ff 	. 
	rst 38h			;2bda	ff 	. 
	rst 38h			;2bdb	ff 	. 
	rst 38h			;2bdc	ff 	. 
	rst 38h			;2bdd	ff 	. 
	rst 38h			;2bde	ff 	. 
	rst 38h			;2bdf	ff 	. 
	rst 38h			;2be0	ff 	. 
	rst 38h			;2be1	ff 	. 
	rst 38h			;2be2	ff 	. 
	rst 38h			;2be3	ff 	. 
	rst 38h			;2be4	ff 	. 
	rst 38h			;2be5	ff 	. 
	rst 38h			;2be6	ff 	. 
	rst 38h			;2be7	ff 	. 
	rst 38h			;2be8	ff 	. 
	rst 38h			;2be9	ff 	. 
	rst 38h			;2bea	ff 	. 
	rst 38h			;2beb	ff 	. 
	rst 38h			;2bec	ff 	. 
	rst 38h			;2bed	ff 	. 
	rst 38h			;2bee	ff 	. 
	rst 38h			;2bef	ff 	. 
	rst 38h			;2bf0	ff 	. 
	rst 38h			;2bf1	ff 	. 
	rst 38h			;2bf2	ff 	. 
	rst 38h			;2bf3	ff 	. 
	rst 38h			;2bf4	ff 	. 
	rst 38h			;2bf5	ff 	. 
	rst 38h			;2bf6	ff 	. 
	rst 38h			;2bf7	ff 	. 
	rst 38h			;2bf8	ff 	. 
	rst 38h			;2bf9	ff 	. 
	rst 38h			;2bfa	ff 	. 
	rst 38h			;2bfb	ff 	. 
	rst 38h			;2bfc	ff 	. 
	rst 38h			;2bfd	ff 	. 
	rst 38h			;2bfe	ff 	. 
	rst 38h			;2bff	ff 	. 
	rst 38h			;2c00	ff 	. 
	rst 38h			;2c01	ff 	. 
	rst 38h			;2c02	ff 	. 
	rst 38h			;2c03	ff 	. 
	rst 38h			;2c04	ff 	. 
	rst 38h			;2c05	ff 	. 
	rst 38h			;2c06	ff 	. 
	rst 38h			;2c07	ff 	. 
	rrca			;2c08	0f 	. 
	dec sp			;2c09	3b 	; 
	rst 38h			;2c0a	ff 	. 
	rst 18h			;2c0b	df 	. 
	rst 38h			;2c0c	ff 	. 
	rst 38h			;2c0d	ff 	. 
	rst 38h			;2c0e	ff 	. 
	rst 38h			;2c0f	ff 	. 
	rst 38h			;2c10	ff 	. 
	rst 38h			;2c11	ff 	. 
	rst 38h			;2c12	ff 	. 
	rst 38h			;2c13	ff 	. 
	rst 38h			;2c14	ff 	. 
	rst 38h			;2c15	ff 	. 
	rst 38h			;2c16	ff 	. 
	rst 38h			;2c17	ff 	. 
	rst 38h			;2c18	ff 	. 
	rst 38h			;2c19	ff 	. 
	rst 38h			;2c1a	ff 	. 
	rst 38h			;2c1b	ff 	. 
	rst 38h			;2c1c	ff 	. 
	rst 38h			;2c1d	ff 	. 
	rst 38h			;2c1e	ff 	. 
	rst 38h			;2c1f	ff 	. 
	rst 38h			;2c20	ff 	. 
	rst 38h			;2c21	ff 	. 
	rst 38h			;2c22	ff 	. 
	rst 38h			;2c23	ff 	. 
	rst 38h			;2c24	ff 	. 
	rst 38h			;2c25	ff 	. 
	rst 38h			;2c26	ff 	. 
	rst 38h			;2c27	ff 	. 
	rst 38h			;2c28	ff 	. 
	rst 38h			;2c29	ff 	. 
	rst 38h			;2c2a	ff 	. 
	rst 38h			;2c2b	ff 	. 
	rst 38h			;2c2c	ff 	. 
	rst 38h			;2c2d	ff 	. 
	rst 38h			;2c2e	ff 	. 
	rst 38h			;2c2f	ff 	. 
	rst 38h			;2c30	ff 	. 
	rst 38h			;2c31	ff 	. 
	rst 38h			;2c32	ff 	. 
	rst 38h			;2c33	ff 	. 
	rst 38h			;2c34	ff 	. 
	rst 38h			;2c35	ff 	. 
	rst 38h			;2c36	ff 	. 
	rst 38h			;2c37	ff 	. 
	rst 38h			;2c38	ff 	. 
	rst 38h			;2c39	ff 	. 
	rst 38h			;2c3a	ff 	. 
	rst 38h			;2c3b	ff 	. 
	rst 38h			;2c3c	ff 	. 
	rst 38h			;2c3d	ff 	. 
	rst 38h			;2c3e	ff 	. 
	rst 38h			;2c3f	ff 	. 
	rst 38h			;2c40	ff 	. 
	rst 38h			;2c41	ff 	. 
	rst 38h			;2c42	ff 	. 
	rst 38h			;2c43	ff 	. 
	rst 38h			;2c44	ff 	. 
	rst 38h			;2c45	ff 	. 
	rst 38h			;2c46	ff 	. 
	rst 38h			;2c47	ff 	. 
	rst 38h			;2c48	ff 	. 
	rrca			;2c49	0f 	. 
	dec sp			;2c4a	3b 	; 
	rst 38h			;2c4b	ff 	. 
l2c4ch:
	rst 18h			;2c4c	df 	. 
	rst 30h			;2c4d	f7 	. 
	di			;2c4e	f3 	. 
	call p,0f7f7h		;2c4f	f4 f7 f7 	. . . 
	or e			;2c52	b3 	. 
	rst 30h			;2c53	f7 	. 
	or a			;2c54	b7 	. 
	or a			;2c55	b7 	. 
	or a			;2c56	b7 	. 
	cp a			;2c57	bf 	. 
	cp a			;2c58	bf 	. 
	cp a			;2c59	bf 	. 
	cp a			;2c5a	bf 	. 
	cp a			;2c5b	bf 	. 
	cp a			;2c5c	bf 	. 
	cp a			;2c5d	bf 	. 
	cp a			;2c5e	bf 	. 
	cp a			;2c5f	bf 	. 
	cp a			;2c60	bf 	. 
	cp a			;2c61	bf 	. 
	cp a			;2c62	bf 	. 
	cp a			;2c63	bf 	. 
	cp a			;2c64	bf 	. 
	cp a			;2c65	bf 	. 
	cp a			;2c66	bf 	. 
	cp a			;2c67	bf 	. 
	cp a			;2c68	bf 	. 
	cp a			;2c69	bf 	. 
	or a			;2c6a	b7 	. 
	and a			;2c6b	a7 	. 
	or a			;2c6c	b7 	. 
	or a			;2c6d	b7 	. 
	or a			;2c6e	b7 	. 
	or a			;2c6f	b7 	. 
	and a			;2c70	a7 	. 
	and a			;2c71	a7 	. 
	and a			;2c72	a7 	. 
	or a			;2c73	b7 	. 
	or a			;2c74	b7 	. 
	or a			;2c75	b7 	. 
	and a			;2c76	a7 	. 
	and a			;2c77	a7 	. 
	and a			;2c78	a7 	. 
	or a			;2c79	b7 	. 
	or a			;2c7a	b7 	. 
	or a			;2c7b	b7 	. 
	and a			;2c7c	a7 	. 
	and a			;2c7d	a7 	. 
	or a			;2c7e	b7 	. 
	or a			;2c7f	b7 	. 
	and a			;2c80	a7 	. 
	and a			;2c81	a7 	. 
	or a			;2c82	b7 	. 
	or a			;2c83	b7 	. 
	and a			;2c84	a7 	. 
	and a			;2c85	a7 	. 
	or a			;2c86	b7 	. 
	scf			;2c87	37 	7 
	call po,0d3e7h		;2c88	e4 e7 d3 	. . . 
	rst 30h			;2c8b	f7 	. 
	ex (sp),hl			;2c8c	e3 	. 
	and a			;2c8d	a7 	. 
	or a			;2c8e	b7 	. 
	or a			;2c8f	b7 	. 
	and a			;2c90	a7 	. 
	and a			;2c91	a7 	. 
	or a			;2c92	b7 	. 
	or a			;2c93	b7 	. 
	and a			;2c94	a7 	. 
	and a			;2c95	a7 	. 
	or a			;2c96	b7 	. 
	or a			;2c97	b7 	. 
	and a			;2c98	a7 	. 
	and a			;2c99	a7 	. 
	or a			;2c9a	b7 	. 
	or a			;2c9b	b7 	. 
	and a			;2c9c	a7 	. 
	or a			;2c9d	b7 	. 
	or a			;2c9e	b7 	. 
	and a			;2c9f	a7 	. 
	or a			;2ca0	b7 	. 
	or a			;2ca1	b7 	. 
	and a			;2ca2	a7 	. 
	or a			;2ca3	b7 	. 
	or a			;2ca4	b7 	. 
	and a			;2ca5	a7 	. 
	or a			;2ca6	b7 	. 
	or a			;2ca7	b7 	. 
	and a			;2ca8	a7 	. 
	or a			;2ca9	b7 	. 
	or a			;2caa	b7 	. 
	and a			;2cab	a7 	. 
	rst 30h			;2cac	f7 	. 
	rst 30h			;2cad	f7 	. 
	rst 30h			;2cae	f7 	. 
	rst 30h			;2caf	f7 	. 
	rst 30h			;2cb0	f7 	. 
	rst 30h			;2cb1	f7 	. 
	rst 30h			;2cb2	f7 	. 
	rst 30h			;2cb3	f7 	. 
	rst 30h			;2cb4	f7 	. 
	rst 30h			;2cb5	f7 	. 
	rst 30h			;2cb6	f7 	. 
	rst 30h			;2cb7	f7 	. 
	rst 38h			;2cb8	ff 	. 
	rst 38h			;2cb9	ff 	. 
	rst 38h			;2cba	ff 	. 
	rst 38h			;2cbb	ff 	. 
	rst 38h			;2cbc	ff 	. 
	rst 38h			;2cbd	ff 	. 
	rst 38h			;2cbe	ff 	. 
	rst 38h			;2cbf	ff 	. 
	rst 38h			;2cc0	ff 	. 
	rst 38h			;2cc1	ff 	. 
	rst 38h			;2cc2	ff 	. 
	rst 38h			;2cc3	ff 	. 
	rst 38h			;2cc4	ff 	. 
	rst 38h			;2cc5	ff 	. 
	rst 38h			;2cc6	ff 	. 
	rst 38h			;2cc7	ff 	. 
	ccf			;2cc8	3f 	? 
	call m,0d3ffh		;2cc9	fc ff d3 	. . . 
	ld d,a			;2ccc	57 	W 
	ld bc,0c5dfh		;2ccd	01 df c5 	. . . 
	nop			;2cd0	00 	. 
	add a,b			;2cd1	80 	. 
	nop			;2cd2	00 	. 
	nop			;2cd3	00 	. 
	rst 38h			;2cd4	ff 	. 
	rst 38h			;2cd5	ff 	. 
	rst 38h			;2cd6	ff 	. 
	nop			;2cd7	00 	. 
	rst 38h			;2cd8	ff 	. 
	rst 38h			;2cd9	ff 	. 
	rst 38h			;2cda	ff 	. 
	rst 38h			;2cdb	ff 	. 
	rst 38h			;2cdc	ff 	. 
	rst 38h			;2cdd	ff 	. 
	add hl,sp			;2cde	39 	9 
	add hl,sp			;2cdf	39 	9 
	add hl,sp			;2ce0	39 	9 
	add hl,sp			;2ce1	39 	9 
	add hl,sp			;2ce2	39 	9 
	add hl,sp			;2ce3	39 	9 
	rst 38h			;2ce4	ff 	. 
	rst 38h			;2ce5	ff 	. 
	rst 38h			;2ce6	ff 	. 
	rst 38h			;2ce7	ff 	. 
	rst 38h			;2ce8	ff 	. 
	rst 38h			;2ce9	ff 	. 
	rst 38h			;2cea	ff 	. 
	rst 38h			;2ceb	ff 	. 
	rst 38h			;2cec	ff 	. 
	rst 38h			;2ced	ff 	. 
	rst 38h			;2cee	ff 	. 
	rst 38h			;2cef	ff 	. 
	rst 38h			;2cf0	ff 	. 
	rst 38h			;2cf1	ff 	. 
	rst 38h			;2cf2	ff 	. 
	rst 38h			;2cf3	ff 	. 
	rst 38h			;2cf4	ff 	. 
	rst 38h			;2cf5	ff 	. 
	rst 38h			;2cf6	ff 	. 
	rst 38h			;2cf7	ff 	. 
	rst 38h			;2cf8	ff 	. 
	rst 38h			;2cf9	ff 	. 
	rst 38h			;2cfa	ff 	. 
	rst 38h			;2cfb	ff 	. 
	rst 38h			;2cfc	ff 	. 
	rst 38h			;2cfd	ff 	. 
	rst 38h			;2cfe	ff 	. 
	rst 38h			;2cff	ff 	. 
	rst 38h			;2d00	ff 	. 
	ld d,0ffh		;2d01	16 ff 	. . 
	rst 38h			;2d03	ff 	. 
	rst 38h			;2d04	ff 	. 
	rst 38h			;2d05	ff 	. 
	rst 38h			;2d06	ff 	. 
	rst 38h			;2d07	ff 	. 
	rst 38h			;2d08	ff 	. 
	rst 38h			;2d09	ff 	. 
	rst 38h			;2d0a	ff 	. 
	rst 38h			;2d0b	ff 	. 
	rst 38h			;2d0c	ff 	. 
	rst 38h			;2d0d	ff 	. 
	rst 38h			;2d0e	ff 	. 
	rst 38h			;2d0f	ff 	. 
	rst 38h			;2d10	ff 	. 
	rst 38h			;2d11	ff 	. 
	rst 38h			;2d12	ff 	. 
	rst 38h			;2d13	ff 	. 
	rst 38h			;2d14	ff 	. 
	rst 38h			;2d15	ff 	. 
	rst 38h			;2d16	ff 	. 
	rst 38h			;2d17	ff 	. 
	rst 38h			;2d18	ff 	. 
	rst 38h			;2d19	ff 	. 
	rst 38h			;2d1a	ff 	. 
	inc b			;2d1b	04 	. 
	ld bc,0ff00h		;2d1c	01 00 ff 	. . . 
	rst 38h			;2d1f	ff 	. 
	rst 38h			;2d20	ff 	. 
	rst 38h			;2d21	ff 	. 
	rst 38h			;2d22	ff 	. 
	rst 38h			;2d23	ff 	. 
	rst 38h			;2d24	ff 	. 
	rst 38h			;2d25	ff 	. 
	rst 38h			;2d26	ff 	. 
	rst 38h			;2d27	ff 	. 
	rst 38h			;2d28	ff 	. 
	rst 38h			;2d29	ff 	. 
	ld h,01ah		;2d2a	26 1a 	& . 
	ld (bc),a			;2d2c	02 	. 
	ld b,020h		;2d2d	06 20 	.   
	ld (bc),a			;2d2f	02 	. 
	rlca			;2d30	07 	. 
	ld h,002h		;2d31	26 02 	& . 
	ex af,af'			;2d33	08 	. 
	inc l			;2d34	2c 	, 
	ld (bc),a			;2d35	02 	. 
	add hl,bc			;2d36	09 	. 
	ld (l0a02h),a		;2d37	32 02 0a 	2 . . 
	ld b,h			;2d3a	44 	D 
	ld (bc),a			;2d3b	02 	. 
	dec bc			;2d3c	0b 	. 
	djnz l2d4fh		;2d3d	10 10 	. . 
	djnz l2d41h		;2d3f	10 00 	. . 
l2d41h:
	ld (bc),a			;2d41	02 	. 
	ex af,af'			;2d42	08 	. 
	ld e,e			;2d43	5b 	[ 
	ld (bc),a			;2d44	02 	. 
	ld b,059h		;2d45	06 59 	. Y 
	ld d,046h		;2d47	16 46 	. F 
	jp c,0ba4ah		;2d49	da 4a ba 	. J . 
	ld c,(hl)			;2d4c	4e 	N 
	ld a,d			;2d4d	7a 	z 
	ld e,l			;2d4e	5d 	] 
l2d4fh:
	jp c,0ba61h		;2d4f	da 61 ba 	. a . 
	ld h,l			;2d52	65 	e 
	ld a,d			;2d53	7a 	z 
	djnz l2d57h		;2d54	10 01 	. . 
	ld l,c			;2d56	69 	i 
l2d57h:
	ld bc,l016bh		;2d57	01 6b 01 	. k . 
	ld l,l			;2d5a	6d 	m 
	ld bc,l016fh		;2d5b	01 6f 01 	. o . 
	ld (hl),c			;2d5e	71 	q 
	ld bc,l2173h		;2d5f	01 73 21 	. s ! 
	ld a,(bc)			;2d62	0a 	. 
	inc bc			;2d63	03 	. 
	inc c			;2d64	0c 	. 
	ld hl,l030bh+1		;2d65	21 0c 03 	! . . 
	inc c			;2d68	0c 	. 
	ld hl,0030eh		;2d69	21 0e 03 	! . . 
	inc c			;2d6c	0c 	. 
	ld hl,l0310h		;2d6d	21 10 03 	! . . 
	ld b,(hl)			;2d70	46 	F 
	ld hl,l0310h+2		;2d71	21 12 03 	! . . 
	ld b,(hl)			;2d74	46 	F 
	ld hl,l0314h		;2d75	21 14 03 	! . . 
	ld b,(hl)			;2d78	46 	F 
	ld bc,00103h		;2d79	01 03 01 	. . . 
	inc b			;2d7c	04 	. 
	ld bc,l0105h		;2d7d	01 05 01 	. . . 
	ld d,(hl)			;2d80	56 	V 
	ld bc,00157h		;2d81	01 57 01 	. W . 
	ld e,b			;2d84	58 	X 
	ld bc,00175h		;2d85	01 75 01 	. u . 
	inc (hl)			;2d88	34 	4 
	ld bc,l0177h		;2d89	01 77 01 	. w . 
	ld (hl),001h		;2d8c	36 01 	6 . 
	ld a,b			;2d8e	78 	x 
	ld bc,00137h		;2d8f	01 37 01 	. 7 . 
	ld a,c			;2d92	79 	y 
	ld bc,l0138h		;2d93	01 38 01 	. 8 . 
	ld a,d			;2d96	7a 	z 
	ld bc,l0139h		;2d97	01 39 01 	. 9 . 
	ld a,e			;2d9a	7b 	{ 
	ld bc,0ff3ah		;2d9b	01 3a ff 	. : . 
	rst 38h			;2d9e	ff 	. 
	rst 38h			;2d9f	ff 	. 
	rst 38h			;2da0	ff 	. 
	rst 38h			;2da1	ff 	. 
	rst 38h			;2da2	ff 	. 
	rst 38h			;2da3	ff 	. 
	rst 38h			;2da4	ff 	. 
	rst 38h			;2da5	ff 	. 
	rst 38h			;2da6	ff 	. 
	rst 38h			;2da7	ff 	. 
	rst 38h			;2da8	ff 	. 
	rst 38h			;2da9	ff 	. 
	rst 38h			;2daa	ff 	. 
	rst 38h			;2dab	ff 	. 
	rst 38h			;2dac	ff 	. 
	rst 38h			;2dad	ff 	. 
	rst 38h			;2dae	ff 	. 
	rst 38h			;2daf	ff 	. 
	rst 38h			;2db0	ff 	. 
	rst 38h			;2db1	ff 	. 
	rst 38h			;2db2	ff 	. 
	rst 38h			;2db3	ff 	. 
	rst 38h			;2db4	ff 	. 
	rst 38h			;2db5	ff 	. 
	rst 38h			;2db6	ff 	. 
	rst 38h			;2db7	ff 	. 
	rst 38h			;2db8	ff 	. 
	rst 38h			;2db9	ff 	. 
	rst 38h			;2dba	ff 	. 
	rst 38h			;2dbb	ff 	. 
	rst 38h			;2dbc	ff 	. 
	rst 38h			;2dbd	ff 	. 
	rst 38h			;2dbe	ff 	. 
	rst 38h			;2dbf	ff 	. 
	rst 38h			;2dc0	ff 	. 
	rst 38h			;2dc1	ff 	. 
	rst 38h			;2dc2	ff 	. 
	rst 38h			;2dc3	ff 	. 
	rst 38h			;2dc4	ff 	. 
	rst 38h			;2dc5	ff 	. 
	rst 38h			;2dc6	ff 	. 
	rst 38h			;2dc7	ff 	. 
	rst 38h			;2dc8	ff 	. 
	rst 38h			;2dc9	ff 	. 
	rst 38h			;2dca	ff 	. 
	rst 38h			;2dcb	ff 	. 
	rst 38h			;2dcc	ff 	. 
	rst 38h			;2dcd	ff 	. 
	rst 38h			;2dce	ff 	. 
	rst 38h			;2dcf	ff 	. 
	rst 38h			;2dd0	ff 	. 
	rst 38h			;2dd1	ff 	. 
	rst 38h			;2dd2	ff 	. 
	rst 38h			;2dd3	ff 	. 
	rst 38h			;2dd4	ff 	. 
	rst 38h			;2dd5	ff 	. 
	rst 38h			;2dd6	ff 	. 
	rst 38h			;2dd7	ff 	. 
	rst 38h			;2dd8	ff 	. 
	rst 38h			;2dd9	ff 	. 
	rst 38h			;2dda	ff 	. 
	rst 38h			;2ddb	ff 	. 
	rst 38h			;2ddc	ff 	. 
	rst 38h			;2ddd	ff 	. 
	rst 38h			;2dde	ff 	. 
	rst 38h			;2ddf	ff 	. 
	rst 38h			;2de0	ff 	. 
	rst 38h			;2de1	ff 	. 
	rst 38h			;2de2	ff 	. 
	rst 38h			;2de3	ff 	. 
	rst 38h			;2de4	ff 	. 
	rst 38h			;2de5	ff 	. 
	rst 38h			;2de6	ff 	. 
	rst 38h			;2de7	ff 	. 
	rst 38h			;2de8	ff 	. 
	rst 38h			;2de9	ff 	. 
	rst 38h			;2dea	ff 	. 
	rst 38h			;2deb	ff 	. 
	rst 38h			;2dec	ff 	. 
	rst 38h			;2ded	ff 	. 
	rst 38h			;2dee	ff 	. 
	rst 38h			;2def	ff 	. 
	rst 38h			;2df0	ff 	. 
	rst 38h			;2df1	ff 	. 
	rst 38h			;2df2	ff 	. 
	rst 38h			;2df3	ff 	. 
	rst 38h			;2df4	ff 	. 
	rst 38h			;2df5	ff 	. 
	rst 38h			;2df6	ff 	. 
	rst 38h			;2df7	ff 	. 
	rst 38h			;2df8	ff 	. 
	rst 38h			;2df9	ff 	. 
	rst 38h			;2dfa	ff 	. 
	rst 38h			;2dfb	ff 	. 
	rst 38h			;2dfc	ff 	. 
	rst 38h			;2dfd	ff 	. 
	rst 38h			;2dfe	ff 	. 
	rst 38h			;2dff	ff 	. 
	jp p,0ff0ch		;2e00	f2 0c ff 	. . . 
	ld a,e			;2e03	7b 	{ 
	ld a,c			;2e04	79 	y 
	ld (hl),a			;2e05	77 	w 
	call m,0ffffh		;2e06	fc ff ff 	. . . 
	rst 38h			;2e09	ff 	. 
	call m,0fcfdh		;2e0a	fc fd fc 	. . . 
	rst 38h			;2e0d	ff 	. 
	call m,0fcffh		;2e0e	fc ff fc 	. . . 
	rst 38h			;2e11	ff 	. 
	call m,0fcffh		;2e12	fc ff fc 	. . . 
	rst 38h			;2e15	ff 	. 
	cp 0fdh		;2e16	fe fd 	. . 
	rst 38h			;2e18	ff 	. 
	rst 38h			;2e19	ff 	. 
	rst 38h			;2e1a	ff 	. 
	rst 38h			;2e1b	ff 	. 
	cp 0fdh		;2e1c	fe fd 	. . 
	ld a,h			;2e1e	7c 	| 
	rst 38h			;2e1f	ff 	. 
	rst 38h			;2e20	ff 	. 
	rst 38h			;2e21	ff 	. 
	cp 0fdh		;2e22	fe fd 	. . 
	ld a,d			;2e24	7a 	z 
	rst 38h			;2e25	ff 	. 
	rst 38h			;2e26	ff 	. 
	rst 38h			;2e27	ff 	. 
	cp 0fdh		;2e28	fe fd 	. . 
	ld a,b			;2e2a	78 	x 
	rst 38h			;2e2b	ff 	. 
	rst 38h			;2e2c	ff 	. 
	rst 38h			;2e2d	ff 	. 
	cp 0fdh		;2e2e	fe fd 	. . 
	halt			;2e30	76 	v 
	rst 38h			;2e31	ff 	. 
	rst 38h			;2e32	ff 	. 
	rst 38h			;2e33	ff 	. 
	ld l,a			;2e34	6f 	o 
	ld (hl),h			;2e35	74 	t 
	ld l,l			;2e36	6d 	m 
	ld l,e			;2e37	6b 	k 
	ld l,c			;2e38	69 	i 
	ld h,a			;2e39	67 	g 
	ld h,l			;2e3a	65 	e 
	rst 38h			;2e3b	ff 	. 
	rst 38h			;2e3c	ff 	. 
	rst 38h			;2e3d	ff 	. 
	rst 38h			;2e3e	ff 	. 
	pop af			;2e3f	f1 	. 
	cp 0fdh		;2e40	fe fd 	. . 
	rst 38h			;2e42	ff 	. 
	rst 38h			;2e43	ff 	. 
	rst 38h			;2e44	ff 	. 
	rst 38h			;2e45	ff 	. 
	push de			;2e46	d5 	. 
	cp 072h		;2e47	fe 72 	. r 
	rlca			;2e49	07 	. 
	dec (hl)			;2e4a	35 	5 
	call nc,0d4d5h		;2e4b	d4 d5 d4 	. . . 
	sbc a,h			;2e4e	9c 	. 
	inc (hl)			;2e4f	34 	4 
	dec (hl)			;2e50	35 	5 
	inc (hl)			;2e51	34 	4 
	rst 38h			;2e52	ff 	. 
	sbc a,h			;2e53	9c 	. 
	sbc a,h			;2e54	9c 	. 
	rst 38h			;2e55	ff 	. 
	ld (hl),l			;2e56	75 	u 
	ld (hl),e			;2e57	73 	s 
	ld (hl),c			;2e58	71 	q 
	call m,0ffffh		;2e59	fc ff ff 	. . . 
	rst 38h			;2e5c	ff 	. 
	jp nz,0fdfdh		;2e5d	c2 fd fd 	. . . 
	defb 0fdh,005h,0c1h	;illegal sequence		;2e60	fd 05 c1 	. . . 
	jp nz,00dc1h		;2e63	c2 c1 0d 	. . . 
	inc b			;2e66	04 	. 
	dec b			;2e67	05 	. 
	inc b			;2e68	04 	. 
	ld a,e			;2e69	7b 	{ 
	dec c			;2e6a	0d 	. 
	ld a,c			;2e6b	79 	y 
	ld (hl),b			;2e6c	70 	p 
	ld (hl),a			;2e6d	77 	w 
	ld l,(hl)			;2e6e	6e 	n 
	ld (hl),l			;2e6f	75 	u 
	ld l,h			;2e70	6c 	l 
	ld (hl),e			;2e71	73 	s 
	ld l,d			;2e72	6a 	j 
	ld (hl),c			;2e73	71 	q 
	ld l,b			;2e74	68 	h 
	ld l,a			;2e75	6f 	o 
	ld h,(hl)			;2e76	66 	f 
	ld l,l			;2e77	6d 	m 
	ld l,e			;2e78	6b 	k 
	ld l,c			;2e79	69 	i 
	ld h,a			;2e7a	67 	g 
	ld h,l			;2e7b	65 	e 
	rst 38h			;2e7c	ff 	. 
	rst 38h			;2e7d	ff 	. 
	rst 38h			;2e7e	ff 	. 
	pop af			;2e7f	f1 	. 
	rst 38h			;2e80	ff 	. 
	defb 0fdh,0ffh,0fah	;illegal sequence		;2e81	fd ff fa 	. . . 
	jp m,0f3fah		;2e84	fa fa f3 	. . . 
	rst 38h			;2e87	ff 	. 
	rst 38h			;2e88	ff 	. 
	rst 38h			;2e89	ff 	. 
	di			;2e8a	f3 	. 
	di			;2e8b	f3 	. 
	di			;2e8c	f3 	. 
	ld sp,hl			;2e8d	f9 	. 
	di			;2e8e	f3 	. 
	ret m			;2e8f	f8 	. 
	cp c			;2e90	b9 	. 
	rst 30h			;2e91	f7 	. 
	cp c			;2e92	b9 	. 
	or 0b9h		;2e93	f6 b9 	. . 
	push af			;2e95	f5 	. 
	ld sp,hl			;2e96	f9 	. 
	ld sp,hl			;2e97	f9 	. 
	call p,0ffffh		;2e98	f4 ff ff 	. . . 
	rst 38h			;2e9b	ff 	. 
	ret m			;2e9c	f8 	. 
	ret m			;2e9d	f8 	. 
	jp m,0ffffh		;2e9e	fa ff ff 	. . . 
	rst 38h			;2ea1	ff 	. 
	rst 30h			;2ea2	f7 	. 
	rst 30h			;2ea3	f7 	. 
	jp m,0ffffh		;2ea4	fa ff ff 	. . . 
	rst 38h			;2ea7	ff 	. 
	or 0f6h		;2ea8	f6 f6 	. . 
	jp m,0ffffh		;2eaa	fa ff ff 	. . . 
	rst 38h			;2ead	ff 	. 
	push af			;2eae	f5 	. 
	push af			;2eaf	f5 	. 
	jp m,0ffffh		;2eb0	fa ff ff 	. . . 
	rst 38h			;2eb3	ff 	. 
	jp m,0fafah		;2eb4	fa fa fa 	. . . 
	jp m,0fafah		;2eb7	fa fa fa 	. . . 
	jp m,0ffffh		;2eba	fa ff ff 	. . . 
	rst 38h			;2ebd	ff 	. 
	rst 38h			;2ebe	ff 	. 
	rst 38h			;2ebf	ff 	. 
	call p,0fff4h		;2ec0	f4 f4 ff 	. . . 
	rst 38h			;2ec3	ff 	. 
	rst 38h			;2ec4	ff 	. 
	rst 38h			;2ec5	ff 	. 
	call m,0faffh		;2ec6	fc ff fa 	. . . 
	defb 0fdh,0fch,0fch	;illegal sequence		;2ec9	fd fc fc 	. . . 
	call m,0fafch		;2ecc	fc fc fa 	. . . 
	call m,0fcfch		;2ecf	fc fc fc 	. . . 
	rst 38h			;2ed2	ff 	. 
	jp m,0fffah		;2ed3	fa fa ff 	. . . 
	jp m,0fafah		;2ed6	fa fa fa 	. . . 
	cp c			;2ed9	b9 	. 
	rst 38h			;2eda	ff 	. 
	rst 38h			;2edb	ff 	. 
	rst 38h			;2edc	ff 	. 
	rst 38h			;2edd	ff 	. 
	rst 38h			;2ede	ff 	. 
	cp c			;2edf	b9 	. 
	rst 38h			;2ee0	ff 	. 
	rst 38h			;2ee1	ff 	. 
	rst 38h			;2ee2	ff 	. 
	rst 38h			;2ee3	ff 	. 
	rst 38h			;2ee4	ff 	. 
	defb 0fdh,0ffh,0ffh	;illegal sequence		;2ee5	fd ff ff 	. . . 
	rst 38h			;2ee8	ff 	. 
	jp m,0fafdh		;2ee9	fa fd fa 	. . . 
	jp m,0fafah		;2eec	fa fa fa 	. . . 
	jp m,0fafah		;2eef	fa fa fa 	. . . 
	jp m,0fafah		;2ef2	fa fa fa 	. . . 
	jp m,0fafah		;2ef5	fa fa fa 	. . . 
	jp m,0fafah		;2ef8	fa fa fa 	. . . 
	jp m,0ffffh		;2efb	fa ff ff 	. . . 
	rst 38h			;2efe	ff 	. 
	rst 38h			;2eff	ff 	. 
	rst 18h			;2f00	df 	. 
	ret nz			;2f01	c0 	. 
	cp 0ffh		;2f02	fe ff 	. . 
	rst 38h			;2f04	ff 	. 
	rst 38h			;2f05	ff 	. 
	ld c,03fh		;2f06	0e 3f 	. ? 
	nop			;2f08	00 	. 
	inc a			;2f09	3c 	< 
	nop			;2f0a	00 	. 
	ld a,000h		;2f0b	3e 00 	> . 
	ld a,000h		;2f0d	3e 00 	> . 
	ld a,000h		;2f0f	3e 00 	> . 
	ld a,000h		;2f11	3e 00 	> . 
	ld a,000h		;2f13	3e 00 	> . 
	ld a,04fh		;2f15	3e 4f 	> O 
	djnz $+81		;2f17	10 4f 	. O 
	ret p			;2f19	f0 	. 
	rst 28h			;2f1a	ef 	. 
	ld e,c			;2f1b	59 	Y 
	ld c,a			;2f1c	4f 	O 
	djnz l2f6eh		;2f1d	10 4f 	. O 
	ret p			;2f1f	f0 	. 
	rst 28h			;2f20	ef 	. 
	ld e,c			;2f21	59 	Y 
	ld c,a			;2f22	4f 	O 
	djnz l2f74h		;2f23	10 4f 	. O 
	ret p			;2f25	f0 	. 
	rst 28h			;2f26	ef 	. 
	ld e,c			;2f27	59 	Y 
	ld c,a			;2f28	4f 	O 
	djnz l2f7ah		;2f29	10 4f 	. O 
	ret p			;2f2b	f0 	. 
	rst 28h			;2f2c	ef 	. 
	ld e,c			;2f2d	59 	Y 
	ld c,a			;2f2e	4f 	O 
	djnz l2f80h		;2f2f	10 4f 	. O 
	ret p			;2f31	f0 	. 
	rst 28h			;2f32	ef 	. 
	ld e,c			;2f33	59 	Y 
	rst 8			;2f34	cf 	. 
	jp m,0fbfbh		;2f35	fa fb fb 	. . . 
	ei			;2f38	fb 	. 
	ei			;2f39	fb 	. 
	ei			;2f3a	fb 	. 
	rst 38h			;2f3b	ff 	. 
	rst 38h			;2f3c	ff 	. 
	rst 38h			;2f3d	ff 	. 
	rst 38h			;2f3e	ff 	. 
	rst 18h			;2f3f	df 	. 
	ld c,a			;2f40	4f 	O 
	djnz l2f92h		;2f41	10 4f 	. O 
	ret p			;2f43	f0 	. 
	rst 28h			;2f44	ef 	. 
	ld e,c			;2f45	59 	Y 
	rlca			;2f46	07 	. 
	call c,sub_14e7h		;2f47	dc e7 14 	. . . 
	rlca			;2f4a	07 	. 
	call c,sub_14e7h		;2f4b	dc e7 14 	. . . 
	rlca			;2f4e	07 	. 
	call c,sub_14e7h		;2f4f	dc e7 14 	. . . 
	rst 38h			;2f52	ff 	. 
	rst 38h			;2f53	ff 	. 
	ret nz			;2f54	c0 	. 
	cp 0ffh		;2f55	fe ff 	. . 
	rst 38h			;2f57	ff 	. 
	rst 38h			;2f58	ff 	. 
	rrca			;2f59	0f 	. 
	dec sp			;2f5a	3b 	; 
	nop			;2f5b	00 	. 
	inc a			;2f5c	3c 	< 
	rlca			;2f5d	07 	. 
	call c,sub_14e7h		;2f5e	dc e7 14 	. . . 
	rlca			;2f61	07 	. 
	call c,sub_14e7h		;2f62	dc e7 14 	. . . 
	rlca			;2f65	07 	. 
	call c,sub_14e7h		;2f66	dc e7 14 	. . . 
	nop			;2f69	00 	. 
	ld a,000h		;2f6a	3e 00 	> . 
	ld a,000h		;2f6c	3e 00 	> . 
l2f6eh:
	ld a,000h		;2f6e	3e 00 	> . 
	ld a,000h		;2f70	3e 00 	> . 
	ld a,000h		;2f72	3e 00 	> . 
l2f74h:
	ld a,0cfh		;2f74	3e cf 	> . 
	jp m,0fbfbh		;2f76	fa fb fb 	. . . 
	ei			;2f79	fb 	. 
l2f7ah:
	ei			;2f7a	fb 	. 
	ei			;2f7b	fb 	. 
	rst 38h			;2f7c	ff 	. 
	rst 38h			;2f7d	ff 	. 
	rst 38h			;2f7e	ff 	. 
	rst 18h			;2f7f	df 	. 
l2f80h:
	scf			;2f80	37 	7 
	or e			;2f81	b3 	. 
	scf			;2f82	37 	7 
	scf			;2f83	37 	7 
	scf			;2f84	37 	7 
	scf			;2f85	37 	7 
	ret p			;2f86	f0 	. 
	rst 30h			;2f87	f7 	. 
	call p,0b837h		;2f88	f4 37 b8 	. 7 . 
	ccf			;2f8b	3f 	? 
	cp b			;2f8c	b8 	. 
	ccf			;2f8d	3f 	? 
	cp b			;2f8e	b8 	. 
	ccf			;2f8f	3f 	? 
	cp b			;2f90	b8 	. 
	ccf			;2f91	3f 	? 
l2f92h:
	cp b			;2f92	b8 	. 
	ccf			;2f93	3f 	? 
	cp b			;2f94	b8 	. 
	ccf			;2f95	3f 	? 
	add hl,sp			;2f96	39 	9 
	cp h			;2f97	bc 	. 
	rst 38h			;2f98	ff 	. 
	rst 38h			;2f99	ff 	. 
l2f9ah:
	rst 38h			;2f9a	ff 	. 
	ccf			;2f9b	3f 	? 
	add hl,sp			;2f9c	39 	9 
	or h			;2f9d	b4 	. 
l2f9eh:
	rst 20h			;2f9e	e7 	. 
	rst 30h			;2f9f	f7 	. 
	rst 30h			;2fa0	f7 	. 
	scf			;2fa1	37 	7 
	ld sp,0e7a4h		;2fa2	31 a4 e7 	1 . . 
	rst 20h			;2fa5	e7 	. 
	rst 30h			;2fa6	f7 	. 
	scf			;2fa7	37 	7 
	ld sp,0e7a4h		;2fa8	31 a4 e7 	1 . . 
	rst 20h			;2fab	e7 	. 
	rst 30h			;2fac	f7 	. 
	scf			;2fad	37 	7 
	ld sp,0e7a4h		;2fae	31 a4 e7 	1 . . 
	rst 30h			;2fb1	f7 	. 
	rst 30h			;2fb2	f7 	. 
	daa			;2fb3	27 	' 
	and e			;2fb4	a3 	. 
	scf			;2fb5	37 	7 
	scf			;2fb6	37 	7 
	daa			;2fb7	27 	' 
	daa			;2fb8	27 	' 
	scf			;2fb9	37 	7 
	rst 30h			;2fba	f7 	. 
	ex (sp),hl			;2fbb	e3 	. 
	rst 20h			;2fbc	e7 	. 
	rst 30h			;2fbd	f7 	. 
	rst 10h			;2fbe	d7 	. 
	daa			;2fbf	27 	' 
	dec h			;2fc0	25 	% 
	call p,0e7f7h		;2fc1	f4 f7 e7 	. . . 
	rst 20h			;2fc4	e7 	. 
	scf			;2fc5	37 	7 
	jr nc,$-87		;2fc6	30 a7 	0 . 
	and e			;2fc8	a3 	. 
	scf			;2fc9	37 	7 
	jr nc,$-87		;2fca	30 a7 	0 . 
	and e			;2fcc	a3 	. 
	scf			;2fcd	37 	7 
	jr nc,$-87		;2fce	30 a7 	0 . 
	or e			;2fd0	b3 	. 
	rst 30h			;2fd1	f7 	. 
	and e			;2fd2	a3 	. 
	scf			;2fd3	37 	7 
	rst 30h			;2fd4	f7 	. 
	daa			;2fd5	27 	' 
	scf			;2fd6	37 	7 
	scf			;2fd7	37 	7 
	daa			;2fd8	27 	' 
	ret p			;2fd9	f0 	. 
	rst 30h			;2fda	f7 	. 
	call po,sub_3037h		;2fdb	e4 37 30 	. 7 0 
	and a			;2fde	a7 	. 
	or e			;2fdf	b3 	. 
	scf			;2fe0	37 	7 
	jr nc,l2f9ah		;2fe1	30 b7 	0 . 
	or e			;2fe3	b3 	. 
	scf			;2fe4	37 	7 
	jr nc,l2f9eh		;2fe5	30 b7 	0 . 
	or e			;2fe7	b3 	. 
	scf			;2fe8	37 	7 
	or b			;2fe9	b0 	. 
	scf			;2fea	37 	7 
	cp b			;2feb	b8 	. 
	ccf			;2fec	3f 	? 
	cp b			;2fed	b8 	. 
	ccf			;2fee	3f 	? 
	cp b			;2fef	b8 	. 
	ccf			;2ff0	3f 	? 
	cp b			;2ff1	b8 	. 
	ccf			;2ff2	3f 	? 
	cp b			;2ff3	b8 	. 
	ccf			;2ff4	3f 	? 
	cp e			;2ff5	bb 	. 
	ccf			;2ff6	3f 	? 
	ccf			;2ff7	3f 	? 
	ccf			;2ff8	3f 	? 
	ccf			;2ff9	3f 	? 
	ccf			;2ffa	3f 	? 
	rst 38h			;2ffb	ff 	. 
	ei			;2ffc	fb 	. 
	rst 38h			;2ffd	ff 	. 
	rst 10h			;2ffe	d7 	. 
	ld d,a			;2fff	57 	W 
	ld (bc),a			;3000	02 	. 
	adc a,a			;3001	8f 	. 
	push hl			;3002	e5 	. 
	nop			;3003	00 	. 
	nop			;3004	00 	. 
	rst 38h			;3005	ff 	. 
	rst 38h			;3006	ff 	. 
	rst 38h			;3007	ff 	. 
	rst 38h			;3008	ff 	. 
	rst 38h			;3009	ff 	. 
	rst 38h			;300a	ff 	. 
	rra			;300b	1f 	. 
	rra			;300c	1f 	. 
	rra			;300d	1f 	. 
	rra			;300e	1f 	. 
	rra			;300f	1f 	. 
	rra			;3010	1f 	. 
	rst 38h			;3011	ff 	. 
	rst 38h			;3012	ff 	. 
	rst 38h			;3013	ff 	. 
	rst 38h			;3014	ff 	. 
	rst 38h			;3015	ff 	. 
	rst 38h			;3016	ff 	. 
	rst 38h			;3017	ff 	. 
	rst 38h			;3018	ff 	. 
	rst 38h			;3019	ff 	. 
	rst 38h			;301a	ff 	. 
	rst 38h			;301b	ff 	. 
	rst 38h			;301c	ff 	. 
	call z,0cccch		;301d	cc cc cc 	. . . 
	call z,0cccch		;3020	cc cc cc 	. . . 
	rst 38h			;3023	ff 	. 
	rst 38h			;3024	ff 	. 
	rst 38h			;3025	ff 	. 
	rst 38h			;3026	ff 	. 
	rst 38h			;3027	ff 	. 
	rst 38h			;3028	ff 	. 
	rst 38h			;3029	ff 	. 
	rst 38h			;302a	ff 	. 
	rst 38h			;302b	ff 	. 
	rst 38h			;302c	ff 	. 
	nop			;302d	00 	. 
	nop			;302e	00 	. 
	rst 38h			;302f	ff 	. 
	rst 38h			;3030	ff 	. 
	rst 38h			;3031	ff 	. 
	rst 38h			;3032	ff 	. 
	rst 38h			;3033	ff 	. 
	nop			;3034	00 	. 
	rst 38h			;3035	ff 	. 
	rst 38h			;3036	ff 	. 
sub_3037h:
	rst 38h			;3037	ff 	. 
	rst 38h			;3038	ff 	. 
	rst 38h			;3039	ff 	. 
	rst 38h			;303a	ff 	. 
	rst 38h			;303b	ff 	. 
	rst 38h			;303c	ff 	. 
	rst 38h			;303d	ff 	. 
	rst 38h			;303e	ff 	. 
	rst 38h			;303f	ff 	. 
	rst 38h			;3040	ff 	. 
	rst 38h			;3041	ff 	. 
	rst 38h			;3042	ff 	. 
	rst 38h			;3043	ff 	. 
	rst 38h			;3044	ff 	. 
	rst 38h			;3045	ff 	. 
	rst 38h			;3046	ff 	. 
	rst 38h			;3047	ff 	. 
	rst 38h			;3048	ff 	. 
	rst 38h			;3049	ff 	. 
	rst 38h			;304a	ff 	. 
	rst 38h			;304b	ff 	. 
	rst 38h			;304c	ff 	. 
	rst 38h			;304d	ff 	. 
	nop			;304e	00 	. 
	nop			;304f	00 	. 
	nop			;3050	00 	. 
	nop			;3051	00 	. 
	nop			;3052	00 	. 
	nop			;3053	00 	. 
	rst 38h			;3054	ff 	. 
	rst 38h			;3055	ff 	. 
	rst 38h			;3056	ff 	. 
	rst 38h			;3057	ff 	. 
	rst 38h			;3058	ff 	. 
	rst 38h			;3059	ff 	. 
	rst 38h			;305a	ff 	. 
	rst 38h			;305b	ff 	. 
	rst 38h			;305c	ff 	. 
	jr nz,l306fh		;305d	20 10 	  . 
	ld bc,00110h		;305f	01 10 01 	. . . 
	ld a,(de)			;3062	1a 	. 
	ld bc,l0123h+1		;3063	01 24 01 	. $ . 
	dec a			;3066	3d 	= 
	ld bc,l0147h		;3067	01 47 01 	. G . 
	ld d,c			;306a	51 	Q 
	ld hl,0030ah		;306b	21 0a 03 	! . . 
	nop			;306e	00 	. 
l306fh:
	ld hl,04314h		;306f	21 14 43 	! . C 
	inc b			;3072	04 	. 
	ld hl,0831eh		;3073	21 1e 83 	! . . 
	ex af,af'			;3076	08 	. 
	ld hl,0c337h		;3077	21 37 c3 	! 7 . 
	inc c			;307a	0c 	. 
	ld hl,l0341h		;307b	21 41 03 	! A . 
	ld de,04b21h		;307e	11 21 4b 	. ! K 
	ld b,e			;3081	43 	C 
	dec d			;3082	15 	. 
	ld bc,l010ah		;3083	01 0a 01 	. . . 
	inc d			;3086	14 	. 
	ld bc,l011eh		;3087	01 1e 01 	. . . 
	scf			;308a	37 	7 
	ld bc,l0140h+1		;308b	01 41 01 	. A . 
	ld c,e			;308e	4b 	K 
	ld hl,08108h		;308f	21 08 81 	! . . 
	add hl,de			;3092	19 	. 
	ld hl,08112h		;3093	21 12 81 	! . . 
	add hl,de			;3096	19 	. 
	ld (08104h),hl		;3097	22 04 81 	" . . 
	add hl,de			;309a	19 	. 
	inc e			;309b	1c 	. 
	add a,c			;309c	81 	. 
	add hl,de			;309d	19 	. 
	ld hl,08135h		;309e	21 35 81 	! 5 . 
	add hl,de			;30a1	19 	. 
	ld hl,0813fh		;30a2	21 3f 81 	! ? . 
	add hl,de			;30a5	19 	. 
	ld (08106h),hl		;30a6	22 06 81 	" . . 
	add hl,de			;30a9	19 	. 
	ld c,c			;30aa	49 	I 
	add a,c			;30ab	81 	. 
	add hl,de			;30ac	19 	. 
	ld bc,l0153h		;30ad	01 53 01 	. S . 
	ld h,001h		;30b0	26 01 	& . 
	ld d,l			;30b2	55 	U 
	ld bc,l0127h+1		;30b3	01 28 01 	. ( . 
	ld d,a			;30b6	57 	W 
	ld bc,l012ah		;30b7	01 2a 01 	. * . 
	ld e,c			;30ba	59 	Y 
	ld bc,l012ah+2		;30bb	01 2c 01 	. , . 
	ld e,e			;30be	5b 	[ 
	ld bc,0012eh		;30bf	01 2e 01 	. . . 
	ld e,l			;30c2	5d 	] 
	ld bc,l0130h		;30c3	01 30 01 	. 0 . 
	inc b			;30c6	04 	. 
	nop			;30c7	00 	. 
	ld bc,l0006h		;30c8	01 06 00 	. . . 
	inc bc			;30cb	03 	. 
	ld c,018h		;30cc	0e 18 	. . 
	ld (l0c03h),hl		;30ce	22 03 0c 	" . . 
	ld d,020h		;30d1	16 20 	.   
	inc bc			;30d3	03 	. 
	dec sp			;30d4	3b 	; 
	ld b,l			;30d5	45 	E 
	ld c,a			;30d6	4f 	O 
	inc bc			;30d7	03 	. 
	add hl,sp			;30d8	39 	9 
	ld b,e			;30d9	43 	C 
	ld c,l			;30da	4d 	M 
	djnz l30edh		;30db	10 10 	. . 
	rst 38h			;30dd	ff 	. 
	rst 38h			;30de	ff 	. 
	rst 38h			;30df	ff 	. 
	rst 38h			;30e0	ff 	. 
	rst 38h			;30e1	ff 	. 
	rst 38h			;30e2	ff 	. 
	rst 38h			;30e3	ff 	. 
	rst 38h			;30e4	ff 	. 
	rst 38h			;30e5	ff 	. 
	rst 38h			;30e6	ff 	. 
	rst 38h			;30e7	ff 	. 
	rst 38h			;30e8	ff 	. 
	rst 38h			;30e9	ff 	. 
	rst 38h			;30ea	ff 	. 
	rst 38h			;30eb	ff 	. 
	rst 38h			;30ec	ff 	. 
l30edh:
	rst 38h			;30ed	ff 	. 
	rst 38h			;30ee	ff 	. 
	rst 38h			;30ef	ff 	. 
	rst 38h			;30f0	ff 	. 
	rst 38h			;30f1	ff 	. 
	rst 38h			;30f2	ff 	. 
	rst 38h			;30f3	ff 	. 
	rst 38h			;30f4	ff 	. 
	rst 38h			;30f5	ff 	. 
	rst 38h			;30f6	ff 	. 
	rst 38h			;30f7	ff 	. 
	rst 38h			;30f8	ff 	. 
	rst 38h			;30f9	ff 	. 
	rst 38h			;30fa	ff 	. 
	rst 38h			;30fb	ff 	. 
	rst 38h			;30fc	ff 	. 
	rst 38h			;30fd	ff 	. 
	rst 38h			;30fe	ff 	. 
	rst 38h			;30ff	ff 	. 
	rst 38h			;3100	ff 	. 
	rst 38h			;3101	ff 	. 
	rst 38h			;3102	ff 	. 
	rst 38h			;3103	ff 	. 
	rst 38h			;3104	ff 	. 
	rst 38h			;3105	ff 	. 
	rst 38h			;3106	ff 	. 
	rst 38h			;3107	ff 	. 
	rst 38h			;3108	ff 	. 
	rst 38h			;3109	ff 	. 
	rst 38h			;310a	ff 	. 
	rst 38h			;310b	ff 	. 
	rst 38h			;310c	ff 	. 
	rst 38h			;310d	ff 	. 
	rst 38h			;310e	ff 	. 
	rst 38h			;310f	ff 	. 
	rst 38h			;3110	ff 	. 
	rst 38h			;3111	ff 	. 
	rst 38h			;3112	ff 	. 
	rst 38h			;3113	ff 	. 
	rst 38h			;3114	ff 	. 
	rst 38h			;3115	ff 	. 
	rst 38h			;3116	ff 	. 
	rst 38h			;3117	ff 	. 
	rst 38h			;3118	ff 	. 
	rst 38h			;3119	ff 	. 
	rst 38h			;311a	ff 	. 
	rst 38h			;311b	ff 	. 
	rst 38h			;311c	ff 	. 
	rst 38h			;311d	ff 	. 
	rst 38h			;311e	ff 	. 
	rst 38h			;311f	ff 	. 
	rst 38h			;3120	ff 	. 
	rst 38h			;3121	ff 	. 
	rst 38h			;3122	ff 	. 
	rst 38h			;3123	ff 	. 
	rst 38h			;3124	ff 	. 
	rst 38h			;3125	ff 	. 
	rst 38h			;3126	ff 	. 
	rst 38h			;3127	ff 	. 
	rst 38h			;3128	ff 	. 
	rst 38h			;3129	ff 	. 
	rst 38h			;312a	ff 	. 
	rst 38h			;312b	ff 	. 
	rst 38h			;312c	ff 	. 
	rst 38h			;312d	ff 	. 
	rst 38h			;312e	ff 	. 
	rst 38h			;312f	ff 	. 
	rst 38h			;3130	ff 	. 
	rst 38h			;3131	ff 	. 
	rst 38h			;3132	ff 	. 
	jp p,0ffffh		;3133	f2 ff ff 	. . . 
	rst 38h			;3136	ff 	. 
	ld a,(hl)			;3137	7e 	~ 
	rst 38h			;3138	ff 	. 
	ld a,(hl)			;3139	7e 	~ 
	rst 38h			;313a	ff 	. 
	ld a,(hl)			;313b	7e 	~ 
	ld a,a			;313c	7f 	 
	call m,0fcffh		;313d	fc ff fc 	. . . 
	rst 38h			;3140	ff 	. 
	rst 38h			;3141	ff 	. 
	rst 38h			;3142	ff 	. 
	rst 38h			;3143	ff 	. 
	ld a,(iy-001h)		;3144	fd 7e ff 	. ~ . 
	cp h			;3147	bc 	. 
	rst 38h			;3148	ff 	. 
	cp h			;3149	bc 	. 
	rst 38h			;314a	ff 	. 
	rst 38h			;314b	ff 	. 
	rst 38h			;314c	ff 	. 
	rst 38h			;314d	ff 	. 
	cp l			;314e	bd 	. 
	ld a,(hl)			;314f	7e 	~ 
	cp a			;3150	bf 	. 
	ld a,h			;3151	7c 	| 
	rst 38h			;3152	ff 	. 
	ld a,h			;3153	7c 	| 
	rst 38h			;3154	ff 	. 
	rst 38h			;3155	ff 	. 
	rst 38h			;3156	ff 	. 
	rst 38h			;3157	ff 	. 
	ld a,l			;3158	7d 	} 
	cp 07fh		;3159	fe 7f 	.  
	cp (hl)			;315b	be 	. 
	rst 38h			;315c	ff 	. 
	ld a,(hl)			;315d	7e 	~ 
	rst 38h			;315e	ff 	. 
	ld a,0ffh		;315f	3e ff 	> . 
	cp 0ffh		;3161	fe ff 	. . 
	cp (hl)			;3163	be 	. 
	rst 38h			;3164	ff 	. 
	rst 38h			;3165	ff 	. 
	pop af			;3166	f1 	. 
	rst 38h			;3167	ff 	. 
	ld a,(hl)			;3168	7e 	~ 
	rst 38h			;3169	ff 	. 
	inc a			;316a	3c 	< 
	rst 38h			;316b	ff 	. 
	inc a			;316c	3c 	< 
	rst 38h			;316d	ff 	. 
	rst 38h			;316e	ff 	. 
	rst 38h			;316f	ff 	. 
	rst 38h			;3170	ff 	. 
	dec a			;3171	3d 	= 
	ld a,(hl)			;3172	7e 	~ 
	ccf			;3173	3f 	? 
	call m,0fcffh		;3174	fc ff fc 	. . . 
	rst 38h			;3177	ff 	. 
	rst 38h			;3178	ff 	. 
	rst 38h			;3179	ff 	. 
	rst 38h			;317a	ff 	. 
	ld a,(iy-001h)		;317b	fd 7e ff 	. ~ . 
	cp h			;317e	bc 	. 
	rst 38h			;317f	ff 	. 
	cp h			;3180	bc 	. 
	rst 38h			;3181	ff 	. 
	rst 38h			;3182	ff 	. 
	rst 38h			;3183	ff 	. 
	rst 38h			;3184	ff 	. 
	cp l			;3185	bd 	. 
	cp 0bfh		;3186	fe bf 	. . 
	cp (hl)			;3188	be 	. 
	rst 38h			;3189	ff 	. 
	ld a,(hl)			;318a	7e 	~ 
	rst 38h			;318b	ff 	. 
	ld a,0ffh		;318c	3e ff 	> . 
	cp 0ffh		;318e	fe ff 	. . 
	cp (hl)			;3190	be 	. 
	rst 38h			;3191	ff 	. 
	rst 38h			;3192	ff 	. 
	rst 38h			;3193	ff 	. 
	rst 38h			;3194	ff 	. 
	rst 38h			;3195	ff 	. 
	rst 38h			;3196	ff 	. 
	rst 38h			;3197	ff 	. 
	rst 38h			;3198	ff 	. 
	rst 38h			;3199	ff 	. 
	rst 38h			;319a	ff 	. 
	rst 38h			;319b	ff 	. 
	rst 38h			;319c	ff 	. 
	rst 38h			;319d	ff 	. 
	rst 38h			;319e	ff 	. 
	rst 38h			;319f	ff 	. 
	rst 38h			;31a0	ff 	. 
	rst 38h			;31a1	ff 	. 
	rst 38h			;31a2	ff 	. 
	rst 38h			;31a3	ff 	. 
	rst 38h			;31a4	ff 	. 
	rst 38h			;31a5	ff 	. 
	rst 38h			;31a6	ff 	. 
	rst 38h			;31a7	ff 	. 
	rst 38h			;31a8	ff 	. 
	rst 38h			;31a9	ff 	. 
	rst 38h			;31aa	ff 	. 
	rst 38h			;31ab	ff 	. 
	rst 38h			;31ac	ff 	. 
	rst 38h			;31ad	ff 	. 
	rst 38h			;31ae	ff 	. 
	rst 38h			;31af	ff 	. 
	rst 38h			;31b0	ff 	. 
	rst 38h			;31b1	ff 	. 
	pop af			;31b2	f1 	. 
	rst 38h			;31b3	ff 	. 
	rst 38h			;31b4	ff 	. 
	rst 38h			;31b5	ff 	. 
	rst 38h			;31b6	ff 	. 
	and 0ffh		;31b7	e6 ff 	. . 
	and 0ffh		;31b9	e6 ff 	. . 
	and 0e6h		;31bb	e6 e6 	. . 
	rst 38h			;31bd	ff 	. 
	rst 38h			;31be	ff 	. 
	rst 38h			;31bf	ff 	. 
	rst 38h			;31c0	ff 	. 
	rst 38h			;31c1	ff 	. 
	rst 38h			;31c2	ff 	. 
	rst 38h			;31c3	ff 	. 
	rst 38h			;31c4	ff 	. 
	and 0ffh		;31c5	e6 ff 	. . 
	ei			;31c7	fb 	. 
	rst 38h			;31c8	ff 	. 
	ei			;31c9	fb 	. 
	rst 38h			;31ca	ff 	. 
	rst 38h			;31cb	ff 	. 
	rst 38h			;31cc	ff 	. 
	rst 38h			;31cd	ff 	. 
	ei			;31ce	fb 	. 
	and 0fbh		;31cf	e6 fb 	. . 
	rst 30h			;31d1	f7 	. 
	rst 38h			;31d2	ff 	. 
	rst 30h			;31d3	f7 	. 
	rst 38h			;31d4	ff 	. 
	rst 38h			;31d5	ff 	. 
	rst 38h			;31d6	ff 	. 
	rst 38h			;31d7	ff 	. 
	rst 30h			;31d8	f7 	. 
	rst 38h			;31d9	ff 	. 
	rst 30h			;31da	f7 	. 
	ei			;31db	fb 	. 
	rst 38h			;31dc	ff 	. 
	rst 30h			;31dd	f7 	. 
	rst 38h			;31de	ff 	. 
	di			;31df	f3 	. 
	rst 38h			;31e0	ff 	. 
	xor 0ffh		;31e1	ee ff 	. . 
	jp pe,0ffffh		;31e3	ea ff ff 	. . . 
	rst 38h			;31e6	ff 	. 
	rst 38h			;31e7	ff 	. 
	and 0ffh		;31e8	e6 ff 	. . 
	di			;31ea	f3 	. 
	rst 38h			;31eb	ff 	. 
	di			;31ec	f3 	. 
	rst 38h			;31ed	ff 	. 
	rst 38h			;31ee	ff 	. 
	rst 38h			;31ef	ff 	. 
	rst 38h			;31f0	ff 	. 
	di			;31f1	f3 	. 
	and 0f3h		;31f2	e6 f3 	. . 
	xor 0ffh		;31f4	ee ff 	. . 
	xor 0ffh		;31f6	ee ff 	. . 
	rst 38h			;31f8	ff 	. 
	rst 38h			;31f9	ff 	. 
	rst 38h			;31fa	ff 	. 
	xor 0e6h		;31fb	ee e6 	. . 
	xor 0eah		;31fd	ee ea 	. . 
	rst 38h			;31ff	ff 	. 
	jp pe,0ffffh		;3200	ea ff ff 	. . . 
	rst 38h			;3203	ff 	. 
	rst 38h			;3204	ff 	. 
	jp pe,0eaffh		;3205	ea ff ea 	. . . 
	ei			;3208	fb 	. 
	rst 38h			;3209	ff 	. 
	rst 30h			;320a	f7 	. 
	rst 38h			;320b	ff 	. 
	di			;320c	f3 	. 
	rst 38h			;320d	ff 	. 
	xor 0ffh		;320e	ee ff 	. . 
	jp pe,0ffffh		;3210	ea ff ff 	. . . 
	rst 38h			;3213	ff 	. 
	rst 38h			;3214	ff 	. 
	rst 38h			;3215	ff 	. 
	rst 38h			;3216	ff 	. 
	rst 38h			;3217	ff 	. 
	rst 38h			;3218	ff 	. 
	rst 38h			;3219	ff 	. 
	rst 38h			;321a	ff 	. 
	rst 38h			;321b	ff 	. 
	rst 38h			;321c	ff 	. 
	rst 38h			;321d	ff 	. 
	rst 38h			;321e	ff 	. 
	rst 38h			;321f	ff 	. 
	rst 38h			;3220	ff 	. 
	rst 38h			;3221	ff 	. 
	rst 38h			;3222	ff 	. 
	rst 38h			;3223	ff 	. 
	rst 38h			;3224	ff 	. 
	rst 38h			;3225	ff 	. 
	rst 38h			;3226	ff 	. 
	rst 38h			;3227	ff 	. 
	rst 38h			;3228	ff 	. 
	rst 38h			;3229	ff 	. 
	rst 38h			;322a	ff 	. 
	rst 38h			;322b	ff 	. 
	rst 38h			;322c	ff 	. 
	rst 38h			;322d	ff 	. 
l322eh:
	rst 38h			;322e	ff 	. 
	rst 38h			;322f	ff 	. 
	rst 38h			;3230	ff 	. 
	rst 38h			;3231	ff 	. 
	rst 38h			;3232	ff 	. 
	rst 18h			;3233	df 	. 
	rst 38h			;3234	ff 	. 
	adc a,0feh		;3235	ce fe 	. . 
	rst 8			;3237	cf 	. 
	pop af			;3238	f1 	. 
	rst 8			;3239	cf 	. 
	ld sp,hl			;323a	f9 	. 
	ret nz			;323b	c0 	. 
	cp 0ceh		;323c	fe ce 	. . 
	call m,03e0eh		;323e	fc 0e 3e 	. . > 
	ld c,03ch		;3241	0e 3c 	. < 
	xor 0feh		;3243	ee fe 	. . 
	ret nz			;3245	c0 	. 
	cp 0ceh		;3246	fe ce 	. . 
	call m,03e0eh		;3248	fc 0e 3e 	. . > 
	ld c,03ch		;324b	0e 3c 	. < 
	xor 0feh		;324d	ee fe 	. . 
	ret nz			;324f	c0 	. 
	cp 0ceh		;3250	fe ce 	. . 
	call m,03e0eh		;3252	fc 0e 3e 	. . > 
	ld c,03ch		;3255	0e 3c 	. < 
	xor 0feh		;3257	ee fe 	. . 
	adc a,0feh		;3259	ce fe 	. . 
	adc a,0fch		;325b	ce fc 	. . 
	adc a,0fch		;325d	ce fc 	. . 
	adc a,0fch		;325f	ce fc 	. . 
	adc a,0fch		;3261	ce fc 	. . 
	adc a,0fch		;3263	ce fc 	. . 
	rst 38h			;3265	ff 	. 
	rst 18h			;3266	df 	. 
	rst 38h			;3267	ff 	. 
	ret nz			;3268	c0 	. 
	cp 0ceh		;3269	fe ce 	. . 
	call m,03e0eh		;326b	fc 0e 3e 	. . > 
	ld c,03ch		;326e	0e 3c 	. < 
	xor 0feh		;3270	ee fe 	. . 
	ret nz			;3272	c0 	. 
	cp 0ceh		;3273	fe ce 	. . 
	call m,03e0eh		;3275	fc 0e 3e 	. . > 
	ld c,03ch		;3278	0e 3c 	. < 
	xor 0feh		;327a	ee fe 	. . 
	ret nz			;327c	c0 	. 
	cp 0ceh		;327d	fe ce 	. . 
	call m,03e0eh		;327f	fc 0e 3e 	. . > 
	ld c,03ch		;3282	0e 3c 	. < 
	xor 0feh		;3284	ee fe 	. . 
	adc a,0feh		;3286	ce fe 	. . 
	adc a,0fch		;3288	ce fc 	. . 
	adc a,0fch		;328a	ce fc 	. . 
	adc a,0fch		;328c	ce fc 	. . 
	adc a,0fch		;328e	ce fc 	. . 
	adc a,0fch		;3290	ce fc 	. . 
	rst 38h			;3292	ff 	. 
	rst 38h			;3293	ff 	. 
	rst 38h			;3294	ff 	. 
	rst 38h			;3295	ff 	. 
	rst 38h			;3296	ff 	. 
	rst 38h			;3297	ff 	. 
	rst 38h			;3298	ff 	. 
	rst 38h			;3299	ff 	. 
	rst 38h			;329a	ff 	. 
	rst 38h			;329b	ff 	. 
	rst 38h			;329c	ff 	. 
	rst 38h			;329d	ff 	. 
	rst 38h			;329e	ff 	. 
	rst 38h			;329f	ff 	. 
	rst 38h			;32a0	ff 	. 
	rst 38h			;32a1	ff 	. 
	rst 38h			;32a2	ff 	. 
	rst 38h			;32a3	ff 	. 
	rst 38h			;32a4	ff 	. 
	rst 38h			;32a5	ff 	. 
	rst 38h			;32a6	ff 	. 
	rst 38h			;32a7	ff 	. 
	rst 38h			;32a8	ff 	. 
	rst 38h			;32a9	ff 	. 
l32aah:
	rst 38h			;32aa	ff 	. 
	rst 38h			;32ab	ff 	. 
	rst 38h			;32ac	ff 	. 
	rst 38h			;32ad	ff 	. 
	rst 38h			;32ae	ff 	. 
	rst 38h			;32af	ff 	. 
	rst 38h			;32b0	ff 	. 
	rst 38h			;32b1	ff 	. 
	rst 18h			;32b2	df 	. 
	rst 30h			;32b3	f7 	. 
	di			;32b4	f3 	. 
	rst 30h			;32b5	f7 	. 
	scf			;32b6	37 	7 
	rst 30h			;32b7	f7 	. 
	scf			;32b8	37 	7 
	rst 30h			;32b9	f7 	. 
	scf			;32ba	37 	7 
	or e			;32bb	b3 	. 
	scf			;32bc	37 	7 
	rst 38h			;32bd	ff 	. 
	ccf			;32be	3f 	? 
	ret m			;32bf	f8 	. 
	rst 38h			;32c0	ff 	. 
	call m,0bbffh		;32c1	fc ff bb 	. . . 
	ccf			;32c4	3f 	? 
	cp e			;32c5	bb 	. 
	ccf			;32c6	3f 	? 
	rst 38h			;32c7	ff 	. 
	ccf			;32c8	3f 	? 
	ret m			;32c9	f8 	. 
	rst 38h			;32ca	ff 	. 
	call m,0bbffh		;32cb	fc ff bb 	. . . 
l32ceh:
	ccf			;32ce	3f 	? 
	cp e			;32cf	bb 	. 
	scf			;32d0	37 	7 
	rst 20h			;32d1	e7 	. 
	scf			;32d2	37 	7 
	ret p			;32d3	f0 	. 
	rst 30h			;32d4	f7 	. 
	call p,0a3e7h		;32d5	f4 e7 a3 	. . . 
	daa			;32d8	27 	' 
	or e			;32d9	b3 	. 
	scf			;32da	37 	7 
	rst 30h			;32db	f7 	. 
	daa			;32dc	27 	' 
	rst 20h			;32dd	e7 	. 
	daa			;32de	27 	' 
	rst 30h			;32df	f7 	. 
	scf			;32e0	37 	7 
	rst 30h			;32e1	f7 	. 
	daa			;32e2	27 	' 
	rst 20h			;32e3	e7 	. 
	rst 30h			;32e4	f7 	. 
	out (0e7h),a		;32e5	d3 e7 	. . 
	daa			;32e7	27 	' 
	di			;32e8	f3 	. 
	scf			;32e9	37 	7 
	rst 20h			;32ea	e7 	. 
	daa			;32eb	27 	' 
	ret p			;32ec	f0 	. 
	rst 30h			;32ed	f7 	. 
	call po,0b3e7h		;32ee	e4 e7 b3 	. . . 
	scf			;32f1	37 	7 
	and e			;32f2	a3 	. 
	daa			;32f3	27 	' 
	rst 30h			;32f4	f7 	. 
	scf			;32f5	37 	7 
	ret po			;32f6	e0 	. 
	rst 20h			;32f7	e7 	. 
	call p,0a3f7h		;32f8	f4 f7 a3 	. . . 
	daa			;32fb	27 	' 
	or e			;32fc	b3 	. 
	scf			;32fd	37 	7 
	rst 20h			;32fe	e7 	. 
	daa			;32ff	27 	' 
	ret p			;3300	f0 	. 
	rst 30h			;3301	f7 	. 
	call po,0b3f7h		;3302	e4 f7 b3 	. . . 
	daa			;3305	27 	' 
	or e			;3306	b3 	. 
	scf			;3307	37 	7 
	rst 20h			;3308	e7 	. 
	scf			;3309	37 	7 
	rst 30h			;330a	f7 	. 
	daa			;330b	27 	' 
	rst 30h			;330c	f7 	. 
	scf			;330d	37 	7 
	rst 20h			;330e	e7 	. 
	scf			;330f	37 	7 
	rst 30h			;3310	f7 	. 
	rst 20h			;3311	e7 	. 
	rst 30h			;3312	f7 	. 
	rst 30h			;3313	f7 	. 
	rst 30h			;3314	f7 	. 
	rst 30h			;3315	f7 	. 
	rst 30h			;3316	f7 	. 
	rst 30h			;3317	f7 	. 
	rst 30h			;3318	f7 	. 
	rst 30h			;3319	f7 	. 
	rst 30h			;331a	f7 	. 
	rst 30h			;331b	f7 	. 
	rst 30h			;331c	f7 	. 
	rst 30h			;331d	f7 	. 
	rst 38h			;331e	ff 	. 
	rst 38h			;331f	ff 	. 
	rst 38h			;3320	ff 	. 
	rst 38h			;3321	ff 	. 
	rst 38h			;3322	ff 	. 
	rst 38h			;3323	ff 	. 
	rst 38h			;3324	ff 	. 
	rst 38h			;3325	ff 	. 
	rst 38h			;3326	ff 	. 
	rst 38h			;3327	ff 	. 
	rst 38h			;3328	ff 	. 
	rst 38h			;3329	ff 	. 
	rst 38h			;332a	ff 	. 
	rst 38h			;332b	ff 	. 
	rst 38h			;332c	ff 	. 
	rst 38h			;332d	ff 	. 
	rst 38h			;332e	ff 	. 
	rst 38h			;332f	ff 	. 
	rst 38h			;3330	ff 	. 
	out (057h),a		;3331	d3 57 	. W 
	inc bc			;3333	03 	. 
	ld c,a			;3334	4f 	O 
	and 000h		;3335	e6 00 	. . 
	nop			;3337	00 	. 
	rst 38h			;3338	ff 	. 
	rst 38h			;3339	ff 	. 
	rst 38h			;333a	ff 	. 
	rst 38h			;333b	ff 	. 
	rst 38h			;333c	ff 	. 
	rst 38h			;333d	ff 	. 
	halt			;333e	76 	v 
	halt			;333f	76 	v 
	halt			;3340	76 	v 
	halt			;3341	76 	v 
	halt			;3342	76 	v 
	halt			;3343	76 	v 
	rst 38h			;3344	ff 	. 
	rst 38h			;3345	ff 	. 
	rst 38h			;3346	ff 	. 
	rst 38h			;3347	ff 	. 
	rst 38h			;3348	ff 	. 
	rst 38h			;3349	ff 	. 
	rst 38h			;334a	ff 	. 
	rst 38h			;334b	ff 	. 
	rst 38h			;334c	ff 	. 
	rst 38h			;334d	ff 	. 
	rst 38h			;334e	ff 	. 
	rst 38h			;334f	ff 	. 
	rst 38h			;3350	ff 	. 
	rst 38h			;3351	ff 	. 
	rst 38h			;3352	ff 	. 
	rst 38h			;3353	ff 	. 
	rst 38h			;3354	ff 	. 
	rst 38h			;3355	ff 	. 
	rst 38h			;3356	ff 	. 
	rst 38h			;3357	ff 	. 
	rst 38h			;3358	ff 	. 
	rst 38h			;3359	ff 	. 
	rst 38h			;335a	ff 	. 
	rst 38h			;335b	ff 	. 
	rst 38h			;335c	ff 	. 
	rst 38h			;335d	ff 	. 
	nop			;335e	00 	. 
	nop			;335f	00 	. 
	rst 38h			;3360	ff 	. 
	nop			;3361	00 	. 
	rst 38h			;3362	ff 	. 
	rst 38h			;3363	ff 	. 
	rst 38h			;3364	ff 	. 
	rst 38h			;3365	ff 	. 
	rst 38h			;3366	ff 	. 
	ld d,040h		;3367	16 40 	. @ 
	add a,b			;3369	80 	. 
	add a,b			;336a	80 	. 
	add a,b			;336b	80 	. 
	add a,b			;336c	80 	. 
	add a,b			;336d	80 	. 
	add a,b			;336e	80 	. 
	ld b,b			;336f	40 	@ 
	ld d,b			;3370	50 	P 
	ld h,b			;3371	60 	` 
	ld (hl),b			;3372	70 	p 
	add a,b			;3373	80 	. 
	sub b			;3374	90 	. 
	jr nz,$+39		;3375	20 25 	  % 
	jr nc,$+66		;3377	30 40 	0 @ 
	ld d,b			;3379	50 	P 
	ld h,b			;337a	60 	` 
	ld (bc),a			;337b	02 	. 
	ld (de),a			;337c	12 	. 
	jr $+55		;337d	18 35 	. 5 
	add a,b			;337f	80 	. 
	ret m			;3380	f8 	. 
	jr nz,l3384h		;3381	20 01 	  . 
	nop			;3383	00 	. 
l3384h:
	rst 38h			;3384	ff 	. 
	rst 38h			;3385	ff 	. 
	rst 38h			;3386	ff 	. 
	rst 38h			;3387	ff 	. 
	rst 38h			;3388	ff 	. 
	rst 38h			;3389	ff 	. 
	rst 38h			;338a	ff 	. 
	rst 38h			;338b	ff 	. 
	rst 38h			;338c	ff 	. 
	rst 38h			;338d	ff 	. 
	rst 38h			;338e	ff 	. 
	rst 38h			;338f	ff 	. 
	jr nz,l33a2h		;3390	20 10 	  . 
	ld bc,l0123h		;3392	01 23 01 	. # . 
	scf			;3395	37 	7 
	ld bc,l0140h		;3396	01 40 01 	. @ . 
	ld d,d			;3399	52 	R 
	ld bc,l0160h		;339a	01 60 01 	. ` . 
	ld l,(hl)			;339d	6e 	n 
	ld hl,l0111h		;339e	21 11 01 	! . . 
	inc b			;33a1	04 	. 
l33a2h:
	ld hl,l0123h+2		;33a2	21 25 01 	! % . 
	inc b			;33a5	04 	. 
	ld hl,l0140h		;33a6	21 40 01 	! @ . 
	inc b			;33a9	04 	. 
	ld hl,00152h		;33aa	21 52 01 	! R . 
	inc b			;33ad	04 	. 
	ld hl,l0160h		;33ae	21 60 01 	! ` . 
	inc b			;33b1	04 	. 
	ld hl,l016eh		;33b2	21 6e 01 	! n . 
	inc b			;33b5	04 	. 
	ld (bc),a			;33b6	02 	. 
	dec e			;33b7	1d 	. 
	ld hl,l1b02h		;33b8	21 02 1b 	! . . 
	rra			;33bb	1f 	. 
	ld (bc),a			;33bc	02 	. 
	ld sp,l0235h		;33bd	31 35 02 	1 5 . 
	cpl			;33c0	2f 	/ 
	inc sp			;33c1	33 	3 
	ld (bc),a			;33c2	02 	. 
	ld c,h			;33c3	4c 	L 
	ld d,b			;33c4	50 	P 
	ld (bc),a			;33c5	02 	. 
	ld c,d			;33c6	4a 	J 
	ld c,(hl)			;33c7	4e 	N 
	ld (bc),a			;33c8	02 	. 
	ld e,h			;33c9	5c 	\ 
	ld e,a			;33ca	5f 	_ 
	ld (bc),a			;33cb	02 	. 
	ld e,d			;33cc	5a 	Z 
	ld e,l			;33cd	5d 	] 
	ld (bc),a			;33ce	02 	. 
	ld l,d			;33cf	6a 	j 
	ld l,l			;33d0	6d 	m 
	ld (bc),a			;33d1	02 	. 
	ld l,b			;33d2	68 	h 
	ld l,e			;33d3	6b 	k 
	ld bc,00175h		;33d4	01 75 01 	. u . 
	ld (hl),e			;33d7	73 	s 
	ld (bc),a			;33d8	02 	. 
	dec d			;33d9	15 	. 
	add hl,de			;33da	19 	. 
	ld (bc),a			;33db	02 	. 
	inc de			;33dc	13 	. 
	rla			;33dd	17 	. 
	ld (bc),a			;33de	02 	. 
	add hl,hl			;33df	29 	) 
	dec l			;33e0	2d 	- 
	ld (bc),a			;33e1	02 	. 
	daa			;33e2	27 	' 
	dec hl			;33e3	2b 	+ 
	ld (bc),a			;33e4	02 	. 
	ld b,h			;33e5	44 	D 
	ld c,b			;33e6	48 	H 
	ld (bc),a			;33e7	02 	. 
	ld b,d			;33e8	42 	B 
	ld b,(hl)			;33e9	46 	F 
	ld (bc),a			;33ea	02 	. 
	ld d,h			;33eb	54 	T 
	ld d,a			;33ec	57 	W 
	ld (bc),a			;33ed	02 	. 
	ld d,(hl)			;33ee	56 	V 
	ld e,c			;33ef	59 	Y 
	ld (bc),a			;33f0	02 	. 
	ld h,d			;33f1	62 	b 
	ld h,l			;33f2	65 	e 
	ld (bc),a			;33f3	02 	. 
	ld h,h			;33f4	64 	d 
	ld h,a			;33f5	67 	g 
	ld bc,l016fh+1		;33f6	01 70 01 	. p . 
	ld (hl),d			;33f9	72 	r 
	ld bc,00176h		;33fa	01 76 01 	. v . 
	add hl,sp			;33fd	39 	9 
	ld bc,l0178h+1		;33fe	01 79 01 	. y . 
	dec sp			;3401	3b 	; 
	ld bc,l0178h+2		;3402	01 7a 01 	. z . 
	inc a			;3405	3c 	< 
	ld bc,l017bh		;3406	01 7b 01 	. { . 
	dec a			;3409	3d 	= 
	ld bc,l017bh+1		;340a	01 7c 01 	. | . 
	ld a,001h		;340d	3e 01 	> . 
	ld a,l			;340f	7d 	} 
	ld bc,l013fh		;3410	01 3f 01 	. ? . 
	ld bc,00100h		;3413	01 00 01 	. . . 
	inc bc			;3416	03 	. 
	nop			;3417	00 	. 
	nop			;3418	00 	. 
	nop			;3419	00 	. 
	nop			;341a	00 	. 
	nop			;341b	00 	. 
	inc de			;341c	13 	. 
	dec b			;341d	05 	. 
	cp d			;341e	ba 	. 
	add hl,bc			;341f	09 	. 
	sbc a,d			;3420	9a 	. 
	dec c			;3421	0d 	. 
	ld a,d			;3422	7a 	z 
	djnz $+1		;3423	10 ff 	. . 
	rst 38h			;3425	ff 	. 
	rst 38h			;3426	ff 	. 
	rst 38h			;3427	ff 	. 
	rst 38h			;3428	ff 	. 
	rst 38h			;3429	ff 	. 
	rst 38h			;342a	ff 	. 
	rst 38h			;342b	ff 	. 
	rst 38h			;342c	ff 	. 
	rst 38h			;342d	ff 	. 
	rst 38h			;342e	ff 	. 
	rst 38h			;342f	ff 	. 
	rst 38h			;3430	ff 	. 
	rst 38h			;3431	ff 	. 
	rst 38h			;3432	ff 	. 
	rst 38h			;3433	ff 	. 
	rst 38h			;3434	ff 	. 
	rst 38h			;3435	ff 	. 
	rst 38h			;3436	ff 	. 
	rst 38h			;3437	ff 	. 
	rst 38h			;3438	ff 	. 
	rst 38h			;3439	ff 	. 
	rst 38h			;343a	ff 	. 
	rst 38h			;343b	ff 	. 
	rst 38h			;343c	ff 	. 
	rst 38h			;343d	ff 	. 
	rst 38h			;343e	ff 	. 
	rst 38h			;343f	ff 	. 
	rst 38h			;3440	ff 	. 
	rst 38h			;3441	ff 	. 
	rst 38h			;3442	ff 	. 
	rst 38h			;3443	ff 	. 
	rst 38h			;3444	ff 	. 
	rst 38h			;3445	ff 	. 
	rst 38h			;3446	ff 	. 
	rst 38h			;3447	ff 	. 
	rst 38h			;3448	ff 	. 
	rst 38h			;3449	ff 	. 
	rst 38h			;344a	ff 	. 
	rst 38h			;344b	ff 	. 
	rst 38h			;344c	ff 	. 
	rst 38h			;344d	ff 	. 
	rst 38h			;344e	ff 	. 
	rst 38h			;344f	ff 	. 
	rst 38h			;3450	ff 	. 
	rst 38h			;3451	ff 	. 
	rst 38h			;3452	ff 	. 
	rst 38h			;3453	ff 	. 
	rst 38h			;3454	ff 	. 
	rst 38h			;3455	ff 	. 
	rst 38h			;3456	ff 	. 
	rst 38h			;3457	ff 	. 
	rst 38h			;3458	ff 	. 
	rst 38h			;3459	ff 	. 
	rst 38h			;345a	ff 	. 
	rst 38h			;345b	ff 	. 
	rst 38h			;345c	ff 	. 
	rst 38h			;345d	ff 	. 
	rst 38h			;345e	ff 	. 
	rst 38h			;345f	ff 	. 
	rst 38h			;3460	ff 	. 
	rst 38h			;3461	ff 	. 
	rst 38h			;3462	ff 	. 
	rst 38h			;3463	ff 	. 
	rst 38h			;3464	ff 	. 
	rst 38h			;3465	ff 	. 
	jp p,0ffa4h		;3466	f2 a4 ff 	. . . 
	and b			;3469	a0 	. 
	rst 38h			;346a	ff 	. 
	jp nz,0fefdh		;346b	c2 fd fe 	. . . 
	defb 0fdh,004h,0c0h	;illegal sequence		;346e	fd 04 c0 	. . . 
	jp nz,00bc0h		;3471	c2 c0 0b 	. . . 
	ld (bc),a			;3474	02 	. 
	inc b			;3475	04 	. 
	ld (bc),a			;3476	02 	. 
	cp 0ffh		;3477	fe ff 	. . 
	and l			;3479	a5 	. 
	rst 38h			;347a	ff 	. 
	rst 38h			;347b	ff 	. 
	rst 38h			;347c	ff 	. 
	add hl,bc			;347d	09 	. 
	rst 38h			;347e	ff 	. 
	and (hl)			;347f	a6 	. 
	rst 38h			;3480	ff 	. 
	and (hl)			;3481	a6 	. 
	rst 38h			;3482	ff 	. 
	rlca			;3483	07 	. 
	rst 38h			;3484	ff 	. 
	ld a,(bc)			;3485	0a 	. 
	ex af,af'			;3486	08 	. 
	and e			;3487	a3 	. 
	rst 38h			;3488	ff 	. 
	rst 38h			;3489	ff 	. 
	and h			;348a	a4 	. 
	cp 0ech		;348b	fe ec 	. . 
	and c			;348d	a1 	. 
	rst 38h			;348e	ff 	. 
	rst 38h			;348f	ff 	. 
	rst 38h			;3490	ff 	. 
	dec b			;3491	05 	. 
	rst 38h			;3492	ff 	. 
	and d			;3493	a2 	. 
	rst 38h			;3494	ff 	. 
	and d			;3495	a2 	. 
	rst 38h			;3496	ff 	. 
	inc bc			;3497	03 	. 
	rst 38h			;3498	ff 	. 
	ld b,004h		;3499	06 04 	. . 
	sbc a,a			;349b	9f 	. 
	rst 38h			;349c	ff 	. 
	rst 38h			;349d	ff 	. 
	and b			;349e	a0 	. 
	call pe,0ebebh		;349f	ec eb eb 	. . . 
	jp (hl)			;34a2	e9 	. 
	ret pe			;34a3	e8 	. 
	and 0e4h		;34a4	e6 e4 	. . 
	cp 0f1h		;34a6	fe f1 	. . 
	sbc a,l			;34a8	9d 	. 
	rst 38h			;34a9	ff 	. 
	rst 38h			;34aa	ff 	. 
	rst 38h			;34ab	ff 	. 
	ld bc,09effh		;34ac	01 ff 9e 	. . . 
	rst 38h			;34af	ff 	. 
	sbc a,(hl)			;34b0	9e 	. 
	rst 38h			;34b1	ff 	. 
	rst 38h			;34b2	ff 	. 
	rst 38h			;34b3	ff 	. 
	ld (bc),a			;34b4	02 	. 
	nop			;34b5	00 	. 
	sbc a,e			;34b6	9b 	. 
	rst 38h			;34b7	ff 	. 
	cp 09ch		;34b8	fe 9c 	. . 
	jp pe,099ffh		;34ba	ea ff 99 	. . . 
	rst 38h			;34bd	ff 	. 
	rst 38h			;34be	ff 	. 
	defb 0fdh,09ah,0ffh	;illegal sequence		;34bf	fd 9a ff 	. . . 
	ei			;34c2	fb 	. 
	cp 0fch		;34c3	fe fc 	. . 
	sub a			;34c5	97 	. 
	cp 098h		;34c6	fe 98 	. . 
	jp (hl)			;34c8	e9 	. 
	rst 38h			;34c9	ff 	. 
	sub l			;34ca	95 	. 
	rst 38h			;34cb	ff 	. 
	rst 38h			;34cc	ff 	. 
	ld sp,hl			;34cd	f9 	. 
	sub (hl)			;34ce	96 	. 
	rst 38h			;34cf	ff 	. 
	rst 30h			;34d0	f7 	. 
	jp m,093f8h		;34d1	fa f8 93 	. . . 
	cp 094h		;34d4	fe 94 	. . 
	rst 20h			;34d6	e7 	. 
	rst 38h			;34d7	ff 	. 
	sub c			;34d8	91 	. 
	rst 38h			;34d9	ff 	. 
	sub d			;34da	92 	. 
	di			;34db	f3 	. 
	call pe,0e5f4h		;34dc	ec f4 e5 	. . . 
	ex de,hl			;34df	eb 	. 
	jp pe,0e6e8h		;34e0	ea e8 e6 	. . . 
	call po,0f1ffh		;34e3	e4 ff f1 	. . . 
	rst 38h			;34e6	ff 	. 
	call m,0fcffh		;34e7	fc ff fc 	. . . 
	rst 38h			;34ea	ff 	. 
	rst 38h			;34eb	ff 	. 
	rst 38h			;34ec	ff 	. 
	rst 38h			;34ed	ff 	. 
	rst 38h			;34ee	ff 	. 
	rst 38h			;34ef	ff 	. 
	rst 38h			;34f0	ff 	. 
	rst 38h			;34f1	ff 	. 
	rst 38h			;34f2	ff 	. 
	defb 0fdh,0ffh,0ffh	;illegal sequence		;34f3	fd ff ff 	. . . 
	rst 38h			;34f6	ff 	. 
	ei			;34f7	fb 	. 
	ei			;34f8	fb 	. 
	call m,0ffffh		;34f9	fc ff ff 	. . . 
	rst 38h			;34fc	ff 	. 
	defb 0fdh,0ffh,0fch	;illegal sequence		;34fd	fd ff fc 	. . . 
	rst 38h			;3500	ff 	. 
	call m,0fdffh		;3501	fc ff fd 	. . . 
	rst 38h			;3504	ff 	. 
	defb 0fdh,0fdh,0fch	;illegal sequence		;3505	fd fd fc 	. . . 
	rst 38h			;3508	ff 	. 
	rst 38h			;3509	ff 	. 
	call m,0fcfbh		;350a	fc fb fc 	. . . 
	call m,0ffffh		;350d	fc ff ff 	. . . 
	rst 38h			;3510	ff 	. 
	defb 0fdh,0ffh,0fch	;illegal sequence		;3511	fd ff fc 	. . . 
	rst 38h			;3514	ff 	. 
	call m,0fdffh		;3515	fc ff fd 	. . . 
	rst 38h			;3518	ff 	. 
	defb 0fdh,0fdh,0fch	;illegal sequence		;3519	fd fd fc 	. . . 
	rst 38h			;351c	ff 	. 
	rst 38h			;351d	ff 	. 
	call m,0fcfch		;351e	fc fc fc 	. . . 
	call m,0fcfch		;3521	fc fc fc 	. . . 
	call m,0fbfch		;3524	fc fc fb 	. . . 
	rst 38h			;3527	ff 	. 
	call m,0ffffh		;3528	fc ff ff 	. . . 
	rst 38h			;352b	ff 	. 
	defb 0fdh,0ffh,0fch	;illegal sequence		;352c	fd ff fc 	. . . 
	rst 38h			;352f	ff 	. 
	call m,0fcffh		;3530	fc ff fc 	. . . 
	rst 38h			;3533	ff 	. 
	defb 0fdh,0fdh,0fch	;illegal sequence		;3534	fd fd fc 	. . . 
	rst 38h			;3537	ff 	. 
	ei			;3538	fb 	. 
	call m,0fffch		;3539	fc fc ff 	. . . 
	call m,0ffffh		;353c	fc ff ff 	. . . 
	call m,0fffch		;353f	fc fc ff 	. . . 
	call m,0fcfch		;3542	fc fc fc 	. . . 
	call m,0fcfbh		;3545	fc fb fc 	. . . 
	call m,0fcffh		;3548	fc ff fc 	. . . 
	rst 38h			;354b	ff 	. 
	rst 38h			;354c	ff 	. 
	call m,0fffch		;354d	fc fc ff 	. . . 
	call m,0fcfch		;3550	fc fc fc 	. . . 
	call m,0fcfbh		;3553	fc fb fc 	. . . 
	call m,0fcffh		;3556	fc ff fc 	. . . 
	rst 38h			;3559	ff 	. 
	call m,0fcfch		;355a	fc fc fc 	. . . 
	call m,0fcfch		;355d	fc fc fc 	. . . 
	call m,0fcfch		;3560	fc fc fc 	. . . 
	call m,0ffffh		;3563	fc ff ff 	. . . 
	rst 18h			;3566	df 	. 
	jp z,0cafdh		;3567	ca fd ca 	. . . 
	defb 0fdh,007h,0dch	;illegal sequence		;356a	fd 07 dc 	. . . 
	rst 20h			;356d	e7 	. 
	inc d			;356e	14 	. 
	rlca			;356f	07 	. 
	call c,sub_14e7h		;3570	dc e7 14 	. . . 
	rlca			;3573	07 	. 
	call c,sub_14e7h		;3574	dc e7 14 	. . . 
	rrca			;3577	0f 	. 
	add hl,de			;3578	19 	. 
	ld c,(hl)			;3579	4e 	N 
	ld a,(hl)			;357a	7e 	~ 
	adc a,(hl)			;357b	8e 	. 
	cp h			;357c	bc 	. 
	ld c,03eh		;357d	0e 3e 	. > 
	ld c,(hl)			;357f	4e 	N 
	ld a,h			;3580	7c 	| 
	ld c,(hl)			;3581	4e 	N 
	ld a,(hl)			;3582	7e 	~ 
	ld c,0f4h		;3583	0e f4 	. . 
	ld c,03eh		;3585	0e 3e 	. > 
	adc a,0f4h		;3587	ce f4 	. . 
	xor 0feh		;3589	ee fe 	. . 
	rrca			;358b	0f 	. 
	add hl,de			;358c	19 	. 
	ld c,(hl)			;358d	4e 	N 
	ld a,(hl)			;358e	7e 	~ 
	adc a,(hl)			;358f	8e 	. 
	cp h			;3590	bc 	. 
	ld c,03eh		;3591	0e 3e 	. > 
	ld c,(hl)			;3593	4e 	N 
	ld a,h			;3594	7c 	| 
	ld c,(hl)			;3595	4e 	N 
	ld a,(hl)			;3596	7e 	~ 
	ld c,0f4h		;3597	0e f4 	. . 
	ld c,03eh		;3599	0e 3e 	. > 
	adc a,0f4h		;359b	ce f4 	. . 
	xor 0feh		;359d	ee fe 	. . 
	rst 8			;359f	cf 	. 
	jp m,0fbfbh		;35a0	fa fb fb 	. . . 
	ei			;35a3	fb 	. 
l35a4h:
	ei			;35a4	fb 	. 
	ei			;35a5	fb 	. 
	ld c,01eh		;35a6	0e 1e 	. . 
	ld c,(hl)			;35a8	4e 	N 
	ld a,(hl)			;35a9	7e 	~ 
	adc a,(hl)			;35aa	8e 	. 
	cp h			;35ab	bc 	. 
	ld c,03eh		;35ac	0e 3e 	. > 
	ld c,(hl)			;35ae	4e 	N 
	ld a,h			;35af	7c 	| 
l35b0h:
	ld c,(hl)			;35b0	4e 	N 
	ld a,(hl)			;35b1	7e 	~ 
	ld c,0f4h		;35b2	0e f4 	. . 
l35b4h:
	ld c,03eh		;35b4	0e 3e 	. > 
	adc a,0f4h		;35b6	ce f4 	. . 
	ld c,03eh		;35b8	0e 3e 	. > 
	rst 28h			;35ba	ef 	. 
	jp m,l0f3bh		;35bb	fa 3b 0f 	. ; . 
	ld a,(04f7bh)		;35be	3a 7b 4f 	: { O 
	ld a,d			;35c1	7a 	z 
	inc sp			;35c2	33 	3 
	rrca			;35c3	0f 	. 
	ld a,(00e73h)		;35c4	3a 73 0e 	: s . 
	ld a,0efh		;35c7	3e ef 	> . 
	jp m,l0f3bh		;35c9	fa 3b 0f 	. ; . 
	ld a,(04f7bh)		;35cc	3a 7b 4f 	: { O 
	ld a,d			;35cf	7a 	z 
	inc sp			;35d0	33 	3 
	rrca			;35d1	0f 	. 
	ld a,(00e73h)		;35d2	3a 73 0e 	: s . 
	ld a,0efh		;35d5	3e ef 	> . 
	jp m,l0f3bh		;35d7	fa 3b 0f 	. ; . 
	jp m,0cf33h		;35da	fa 33 cf 	. 3 . 
	jp m,0fbffh		;35dd	fa ff fb 	. . . 
	ei			;35e0	fb 	. 
	ei			;35e1	fb 	. 
	ei			;35e2	fb 	. 
	ei			;35e3	fb 	. 
	rst 38h			;35e4	ff 	. 
	rst 18h			;35e5	df 	. 
l35e6h:
	scf			;35e6	37 	7 
	rst 30h			;35e7	f7 	. 
	scf			;35e8	37 	7 
	rst 30h			;35e9	f7 	. 
	scf			;35ea	37 	7 
	jr nc,l35a4h		;35eb	30 b7 	0 . 
	or e			;35ed	b3 	. 
	scf			;35ee	37 	7 
	jr nc,l35b0h		;35ef	30 bf 	0 . 
	cp e			;35f1	bb 	. 
	ccf			;35f2	3f 	? 
	jr c,l35b4h		;35f3	38 bf 	8 . 
	cp e			;35f5	bb 	. 
	ccf			;35f6	3f 	? 
	cp b			;35f7	b8 	. 
	ccf			;35f8	3f 	? 
	ld sp,hl			;35f9	f9 	. 
	rst 38h			;35fa	ff 	. 
	cp 03fh		;35fb	fe 3f 	. ? 
	ret m			;35fd	f8 	. 
	cp a			;35fe	bf 	. 
	rst 38h			;35ff	ff 	. 
	cp a			;3600	bf 	. 
	ei			;3601	fb 	. 
	ccf			;3602	3f 	? 
	call p,0b3a7h		;3603	f4 a7 b3 	. . . 
	scf			;3606	37 	7 
	rst 30h			;3607	f7 	. 
	rst 30h			;3608	f7 	. 
	and e			;3609	a3 	. 
	daa			;360a	27 	' 
	and b			;360b	a0 	. 
	scf			;360c	37 	7 
	push af			;360d	f5 	. 
	di			;360e	f3 	. 
	and 027h		;360f	e6 27 	. ' 
	ret po			;3611	e0 	. 
	or a			;3612	b7 	. 
	rst 30h			;3613	f7 	. 
	or a			;3614	b7 	. 
	ex (sp),hl			;3615	e3 	. 
	daa			;3616	27 	' 
	call p,0e3b7h		;3617	f4 b7 e3 	. . . 
	daa			;361a	27 	' 
	rst 30h			;361b	f7 	. 
	rst 30h			;361c	f7 	. 
	and e			;361d	a3 	. 
	daa			;361e	27 	' 
	or e			;361f	b3 	. 
	scf			;3620	37 	7 
	daa			;3621	27 	' 
	daa			;3622	27 	' 
	scf			;3623	37 	7 
	scf			;3624	37 	7 
	daa			;3625	27 	' 
	ret nz			;3626	c0 	. 
	scf			;3627	37 	7 
	pop af			;3628	f1 	. 
	rst 20h			;3629	e7 	. 
	and 037h		;362a	e6 37 	. 7 
	ret p			;362c	f0 	. 
	and a			;362d	a7 	. 
	rst 20h			;362e	e7 	. 
	or a			;362f	b7 	. 
	di			;3630	f3 	. 
	daa			;3631	27 	' 
	call po,0b3b7h		;3632	e4 b7 b3 	. . . 
	daa			;3635	27 	' 
	rst 30h			;3636	f7 	. 
	scf			;3637	37 	7 
	and b			;3638	a0 	. 
	or a			;3639	b7 	. 
	rst 30h			;363a	f7 	. 
	daa			;363b	27 	' 
	call p,sub_27f3h		;363c	f4 f3 27 	. . ' 
	or l			;363f	b5 	. 
	di			;3640	f3 	. 
	daa			;3641	27 	' 
	or h			;3642	b4 	. 
	or e			;3643	b3 	. 
	daa			;3644	27 	' 
	dec (hl)			;3645	35 	5 
	or b			;3646	b0 	. 
	or a			;3647	b7 	. 
	rst 30h			;3648	f7 	. 
	scf			;3649	37 	7 
	call p,sub_37f3h		;364a	f4 f3 37 	. . 7 
	or l			;364d	b5 	. 
	di			;364e	f3 	. 
	scf			;364f	37 	7 
	or h			;3650	b4 	. 
	cp e			;3651	bb 	. 
	ccf			;3652	3f 	? 
	dec a			;3653	3d 	= 
	cp b			;3654	b8 	. 
	cp a			;3655	bf 	. 
	rst 38h			;3656	ff 	. 
	ccf			;3657	3f 	? 
	call m,sub_3fbbh		;3658	fc bb 3f 	. . ? 
	inc a			;365b	3c 	< 
	cp e			;365c	bb 	. 
	cp a			;365d	bf 	. 
	ccf			;365e	3f 	? 
	ccf			;365f	3f 	? 
	ccf			;3660	3f 	? 
	ccf			;3661	3f 	? 
	ccf			;3662	3f 	? 
	rst 38h			;3663	ff 	. 
	out (057h),a		;3664	d3 57 	. W 
	inc b			;3666	04 	. 
	rst 38h			;3667	ff 	. 
	ld b,a			;3668	47 	G 
	inc bc			;3669	03 	. 
	ld c,0ffh		;366a	0e ff 	. . 
	rst 38h			;366c	ff 	. 
	rst 38h			;366d	ff 	. 
	rst 38h			;366e	ff 	. 
	rst 38h			;366f	ff 	. 
	rst 38h			;3670	ff 	. 
	rst 38h			;3671	ff 	. 
	rst 38h			;3672	ff 	. 
	rst 38h			;3673	ff 	. 
	rst 38h			;3674	ff 	. 
	rst 38h			;3675	ff 	. 
	rst 38h			;3676	ff 	. 
	rst 38h			;3677	ff 	. 
	rst 38h			;3678	ff 	. 
	rst 38h			;3679	ff 	. 
	rst 38h			;367a	ff 	. 
	rst 38h			;367b	ff 	. 
	rst 38h			;367c	ff 	. 
	ld e,a			;367d	5f 	_ 
	ld e,a			;367e	5f 	_ 
	ld e,a			;367f	5f 	_ 
	ld e,a			;3680	5f 	_ 
	ld e,a			;3681	5f 	_ 
	ld e,a			;3682	5f 	_ 
	rst 38h			;3683	ff 	. 
	rst 38h			;3684	ff 	. 
	rst 38h			;3685	ff 	. 
	rst 38h			;3686	ff 	. 
	rst 38h			;3687	ff 	. 
	rst 38h			;3688	ff 	. 
	ccf			;3689	3f 	? 
	ccf			;368a	3f 	? 
	ccf			;368b	3f 	? 
	ccf			;368c	3f 	? 
	ccf			;368d	3f 	? 
	ccf			;368e	3f 	? 
	rst 38h			;368f	ff 	. 
	rst 38h			;3690	ff 	. 
	rst 38h			;3691	ff 	. 
	rst 38h			;3692	ff 	. 
	rst 38h			;3693	ff 	. 
	rst 38h			;3694	ff 	. 
	rst 38h			;3695	ff 	. 
	cp 0ffh		;3696	fe ff 	. . 
	rst 38h			;3698	ff 	. 
	rst 38h			;3699	ff 	. 
	ld d,040h		;369a	16 40 	. @ 
	add a,b			;369c	80 	. 
	cp 020h		;369d	fe 20 	.   
	ld c,b			;369f	48 	H 
	ld (hl),b			;36a0	70 	p 
	ld b,b			;36a1	40 	@ 
	ld b,b			;36a2	40 	@ 
	ld b,b			;36a3	40 	@ 
	ld b,b			;36a4	40 	@ 
	jr nz,$+34		;36a5	20 20 	    
	dec bc			;36a7	0b 	. 
	ld (hl),b			;36a8	70 	p 
	sbc a,b			;36a9	98 	. 
	ret c			;36aa	d8 	. 
	rst 38h			;36ab	ff 	. 
	nop			;36ac	00 	. 
	jr nz,l370fh		;36ad	20 60 	  ` 
	or b			;36af	b0 	. 
	or b			;36b0	b0 	. 
	ld h,b			;36b1	60 	` 
	and b			;36b2	a0 	. 
	cp 020h		;36b3	fe 20 	.   
	ld bc,l3980h		;36b5	01 80 39 	. . 9 
	ld a,(bc)			;36b8	0a 	. 
	ld h,01eh		;36b9	26 1e 	& . 
	adc a,e			;36bb	8b 	. 
	nop			;36bc	00 	. 
	ld l,d			;36bd	6a 	j 
	ld bc,00840h		;36be	01 40 08 	. @ . 
	ld l,0ffh		;36c1	2e ff 	. . 
	jr nz,$+24		;36c3	20 16 	  . 
	ld de,l1eb0h		;36c5	11 b0 1e 	. . . 
	ld (hl),b			;36c8	70 	p 
	inc h			;36c9	24 	$ 
	ld (hl),b			;36ca	70 	p 
	ld d,h			;36cb	54 	T 
	or b			;36cc	b0 	. 
	ld e,d			;36cd	5a 	Z 
	ld (hl),b			;36ce	70 	p 
	ld h,b			;36cf	60 	` 
	ld (hl),b			;36d0	70 	p 
	ld de,l011dh		;36d1	11 1d 01 	. . . 
	ld d,00bh		;36d4	16 0b 	. . 
	nop			;36d6	00 	. 
	dec de			;36d7	1b 	. 
	nop			;36d8	00 	. 
	ld (04d00h),hl		;36d9	22 00 4d 	" . M 
	nop			;36dc	00 	. 
	ld e,b			;36dd	58 	X 
	nop			;36de	00 	. 
	ld e,(hl)			;36df	5e 	^ 
	nop			;36e0	00 	. 
	ld bc,l0118h		;36e1	01 18 01 	. . . 
	ld a,(de)			;36e4	1a 	. 
	ld (bc),a			;36e5	02 	. 
	dec d			;36e6	15 	. 
	ld d,c			;36e7	51 	Q 
	ld (bc),a			;36e8	02 	. 
	rla			;36e9	17 	. 
	ld d,e			;36ea	53 	S 
	add a,d			;36eb	82 	. 
	dec sp			;36ec	3b 	; 
	ld (hl),a			;36ed	77 	w 
	nop			;36ee	00 	. 
	nop			;36ef	00 	. 
	nop			;36f0	00 	. 
	ld (l2801h),hl		;36f1	22 01 28 	" . ( 
	ld e,043h		;36f4	1e 43 	. C 
	jr z,l3716h		;36f6	28 1e 	( . 
	djnz l370ah		;36f8	10 10 	. . 
	nop			;36fa	00 	. 
	ld (bc),a			;36fb	02 	. 
	ld a,07ah		;36fc	3e 7a 	> z 
	ld (bc),a			;36fe	02 	. 
	inc a			;36ff	3c 	< 
	ld a,b			;3700	78 	x 
	inc d			;3701	14 	. 
	inc bc			;3702	03 	. 
	jp c,0ba07h		;3703	da 07 ba 	. . . 
	ld b,l			;3706	45 	E 
	jp c,0ba49h		;3707	da 49 ba 	. I . 
l370ah:
	djnz $+3		;370a	10 01 	. . 
	jr c,l370fh		;370c	38 01 	8 . 
	add hl,sp			;370e	39 	9 
l370fh:
	ld bc,l0139h+1		;370f	01 3a 01 	. : . 
	ld (hl),h			;3712	74 	t 
	ld bc,00175h		;3713	01 75 01 	. u . 
l3716h:
	halt			;3716	76 	v 
	ld hl,l2838h		;3717	21 38 28 	! 8 ( 
	ld e,021h		;371a	1e 21 	. ! 
	add hl,sp			;371c	39 	9 
	jr z,l373dh		;371d	28 1e 	( . 
	ld hl,l283ah		;371f	21 3a 28 	! : ( 
	ld e,021h		;3722	1e 21 	. ! 
	ld (hl),h			;3724	74 	t 
	jr z,l3745h		;3725	28 1e 	( . 
	ld hl,l2875h		;3727	21 75 28 	! u ( 
	ld e,021h		;372a	1e 21 	. ! 
	halt			;372c	76 	v 
	jr z,l374dh		;372d	28 1e 	( . 
	rst 38h			;372f	ff 	. 
	rst 38h			;3730	ff 	. 
	rst 38h			;3731	ff 	. 
	rst 38h			;3732	ff 	. 
	rst 38h			;3733	ff 	. 
	rst 38h			;3734	ff 	. 
	rst 38h			;3735	ff 	. 
	rst 38h			;3736	ff 	. 
sub_3737h:
	rst 38h			;3737	ff 	. 
	rst 38h			;3738	ff 	. 
	rst 38h			;3739	ff 	. 
	rst 38h			;373a	ff 	. 
	rst 38h			;373b	ff 	. 
	rst 38h			;373c	ff 	. 
l373dh:
	rst 38h			;373d	ff 	. 
	rst 38h			;373e	ff 	. 
	rst 38h			;373f	ff 	. 
	rst 38h			;3740	ff 	. 
	rst 38h			;3741	ff 	. 
	rst 38h			;3742	ff 	. 
	rst 38h			;3743	ff 	. 
	rst 38h			;3744	ff 	. 
l3745h:
	rst 38h			;3745	ff 	. 
	rst 38h			;3746	ff 	. 
	rst 38h			;3747	ff 	. 
	rst 38h			;3748	ff 	. 
	rst 38h			;3749	ff 	. 
	rst 38h			;374a	ff 	. 
	rst 38h			;374b	ff 	. 
	rst 38h			;374c	ff 	. 
l374dh:
	rst 38h			;374d	ff 	. 
	rst 38h			;374e	ff 	. 
	rst 38h			;374f	ff 	. 
	rst 38h			;3750	ff 	. 
	rst 38h			;3751	ff 	. 
	rst 38h			;3752	ff 	. 
	rst 38h			;3753	ff 	. 
	rst 38h			;3754	ff 	. 
	rst 38h			;3755	ff 	. 
	rst 38h			;3756	ff 	. 
	rst 38h			;3757	ff 	. 
	rst 38h			;3758	ff 	. 
	rst 38h			;3759	ff 	. 
	rst 38h			;375a	ff 	. 
	rst 38h			;375b	ff 	. 
	rst 38h			;375c	ff 	. 
	rst 38h			;375d	ff 	. 
	rst 38h			;375e	ff 	. 
	rst 38h			;375f	ff 	. 
	rst 38h			;3760	ff 	. 
	rst 38h			;3761	ff 	. 
	rst 38h			;3762	ff 	. 
	rst 38h			;3763	ff 	. 
	rst 38h			;3764	ff 	. 
	rst 38h			;3765	ff 	. 
	rst 38h			;3766	ff 	. 
	rst 38h			;3767	ff 	. 
	rst 38h			;3768	ff 	. 
	rst 38h			;3769	ff 	. 
	rst 38h			;376a	ff 	. 
	rst 38h			;376b	ff 	. 
	rst 38h			;376c	ff 	. 
	rst 38h			;376d	ff 	. 
	rst 38h			;376e	ff 	. 
	rst 38h			;376f	ff 	. 
	rst 38h			;3770	ff 	. 
	rst 38h			;3771	ff 	. 
	rst 38h			;3772	ff 	. 
	rst 38h			;3773	ff 	. 
	rst 38h			;3774	ff 	. 
	rst 38h			;3775	ff 	. 
	rst 38h			;3776	ff 	. 
	rst 38h			;3777	ff 	. 
	rst 38h			;3778	ff 	. 
	rst 38h			;3779	ff 	. 
	rst 38h			;377a	ff 	. 
	rst 38h			;377b	ff 	. 
	rst 38h			;377c	ff 	. 
	rst 38h			;377d	ff 	. 
	rst 38h			;377e	ff 	. 
	rst 38h			;377f	ff 	. 
	rst 38h			;3780	ff 	. 
	rst 38h			;3781	ff 	. 
	rst 38h			;3782	ff 	. 
	rst 38h			;3783	ff 	. 
	rst 38h			;3784	ff 	. 
	rst 38h			;3785	ff 	. 
	rst 38h			;3786	ff 	. 
	rst 38h			;3787	ff 	. 
	rst 38h			;3788	ff 	. 
	rst 38h			;3789	ff 	. 
	rst 38h			;378a	ff 	. 
	rst 38h			;378b	ff 	. 
	rst 38h			;378c	ff 	. 
	rst 38h			;378d	ff 	. 
	rst 38h			;378e	ff 	. 
	rst 38h			;378f	ff 	. 
	rst 38h			;3790	ff 	. 
	rst 38h			;3791	ff 	. 
	rst 38h			;3792	ff 	. 
	rst 38h			;3793	ff 	. 
	rst 38h			;3794	ff 	. 
	rst 38h			;3795	ff 	. 
	rst 38h			;3796	ff 	. 
	rst 38h			;3797	ff 	. 
	rst 38h			;3798	ff 	. 
	jp p,0d8d7h		;3799	f2 d7 d8 	. . . 
	ld b,a			;379c	47 	G 
	rst 38h			;379d	ff 	. 
	rst 38h			;379e	ff 	. 
	ld (hl),h			;379f	74 	t 
	call m,04746h		;37a0	fc 46 47 	. F G 
	ld b,(hl)			;37a3	46 	F 
	jp c,0ffffh		;37a4	da ff ff 	. . . 
	rst 38h			;37a7	ff 	. 
	rst 38h			;37a8	ff 	. 
	rst 38h			;37a9	ff 	. 
	ld b,l			;37aa	45 	E 
	rst 38h			;37ab	ff 	. 
	rst 38h			;37ac	ff 	. 
	add a,074h		;37ad	c6 74 	. t 
	ld b,l			;37af	45 	E 
	ld a,h			;37b0	7c 	| 
	rst 38h			;37b1	ff 	. 
	ld a,l			;37b2	7d 	} 
	ld a,d			;37b3	7a 	z 
	rst 38h			;37b4	ff 	. 
	rst 38h			;37b5	ff 	. 
	ld a,e			;37b6	7b 	{ 
l37b7h:
	sub b			;37b7	90 	. 
	rst 38h			;37b8	ff 	. 
	rst 38h			;37b9	ff 	. 
	ld (hl),h			;37ba	74 	t 
	ld (l0590h),hl		;37bb	22 90 05 	" . . 
	rst 38h			;37be	ff 	. 
	rst 38h			;37bf	ff 	. 
	ld (l052ch),hl		;37c0	22 2c 05 	" , . 
	cp 0deh		;37c3	fe de 	. . 
	sbc a,d			;37c5	9a 	. 
	inc c			;37c6	0c 	. 
	push hl			;37c7	e5 	. 
	ld d,(hl)			;37c8	56 	V 
	rlca			;37c9	07 	. 
	xor (hl)			;37ca	ae 	. 
	ld c,h			;37cb	4c 	L 
	ld sp,06cd3h		;37cc	31 d3 6c 	1 . l 
	add hl,sp			;37cf	39 	9 
	rst 8			;37d0	cf 	. 
	rst 10h			;37d1	d7 	. 
	rst 10h			;37d2	d7 	. 
	rst 10h			;37d3	d7 	. 
	rst 38h			;37d4	ff 	. 
	ld (hl),l			;37d5	75 	u 
	rst 38h			;37d6	ff 	. 
	rst 38h			;37d7	ff 	. 
	rst 38h			;37d8	ff 	. 
	rst 38h			;37d9	ff 	. 
	pop af			;37da	f1 	. 
	halt			;37db	76 	v 
	rst 10h			;37dc	d7 	. 
	rst 38h			;37dd	ff 	. 
	call nc,0ffffh		;37de	d4 ff ff 	. . . 
	ei			;37e1	fb 	. 
	sub l			;37e2	95 	. 
	out (0d4h),a		;37e3	d3 d4 	. . 
	out (04ah),a		;37e5	d3 4a 	. J 
	rst 38h			;37e7	ff 	. 
	rst 38h			;37e8	ff 	. 
	rst 38h			;37e9	ff 	. 
l37eah:
	rst 38h			;37ea	ff 	. 
	rst 38h			;37eb	ff 	. 
	cp 0d5h		;37ec	fe d5 	. . 
	rst 38h			;37ee	ff 	. 
	rst 38h			;37ef	ff 	. 
	ld c,d			;37f0	4a 	J 
	ld a,(hl)			;37f1	7e 	~ 
	push de			;37f2	d5 	. 
sub_37f3h:
	sbc a,h			;37f3	9c 	. 
	rst 38h			;37f4	ff 	. 
	rst 38h			;37f5	ff 	. 
	ld a,l			;37f6	7d 	} 
	inc l			;37f7	2c 	, 
	sbc a,h			;37f8	9c 	. 
	add a,b			;37f9	80 	. 
	rst 38h			;37fa	ff 	. 
	rst 38h			;37fb	ff 	. 
	inc l			;37fc	2c 	, 
	halt			;37fd	76 	v 
	add a,b			;37fe	80 	. 
	ld l,l			;37ff	6d 	m 
	inc sp			;3800	33 	3 
	nop			;3801	00 	. 
	inc sp			;3802	33 	3 
	inc de			;3803	13 	. 
	and e			;3804	a3 	. 
	ld a,l			;3805	7d 	} 
	inc de			;3806	13 	. 
	sbc a,d			;3807	9a 	. 
	ld a,a			;3808	7f 	 
	jr l37eah		;3809	18 df 	. . 
	add a,b			;380b	80 	. 
	inc a			;380c	3c 	< 
	rst 10h			;380d	d7 	. 
	rst 10h			;380e	d7 	. 
	rst 10h			;380f	d7 	. 
	rst 38h			;3810	ff 	. 
	ld a,(hl)			;3811	7e 	~ 
	rst 38h			;3812	ff 	. 
	rst 38h			;3813	ff 	. 
	rst 38h			;3814	ff 	. 
	rst 38h			;3815	ff 	. 
	ld a,a			;3816	7f 	 
	rst 38h			;3817	ff 	. 
	pop af			;3818	f1 	. 
	rst 38h			;3819	ff 	. 
	pop hl			;381a	e1 	. 
	pop hl			;381b	e1 	. 
	rst 38h			;381c	ff 	. 
	rst 38h			;381d	ff 	. 
	rst 38h			;381e	ff 	. 
	rst 38h			;381f	ff 	. 
	cp 0ffh		;3820	fe ff 	. . 
	rst 38h			;3822	ff 	. 
	rst 38h			;3823	ff 	. 
	pop hl			;3824	e1 	. 
	rst 38h			;3825	ff 	. 
	rst 38h			;3826	ff 	. 
	rst 38h			;3827	ff 	. 
	rst 38h			;3828	ff 	. 
	rst 38h			;3829	ff 	. 
	push af			;382a	f5 	. 
	rst 38h			;382b	ff 	. 
	rst 38h			;382c	ff 	. 
	push af			;382d	f5 	. 
l382eh:
	jp p,0fff5h		;382e	f2 f5 ff 	. . . 
	rst 38h			;3831	ff 	. 
	rst 38h			;3832	ff 	. 
	rst 38h			;3833	ff 	. 
	rst 38h			;3834	ff 	. 
	rst 38h			;3835	ff 	. 
	rst 38h			;3836	ff 	. 
	pop af			;3837	f1 	. 
	rst 38h			;3838	ff 	. 
l3839h:
	rst 38h			;3839	ff 	. 
	jp p,0f1efh		;383a	f2 ef f1 	. . . 
	xor 0ffh		;383d	ee ff 	. . 
	rst 38h			;383f	ff 	. 
	rst 28h			;3840	ef 	. 
	push af			;3841	f5 	. 
	xor 0f3h		;3842	ee f3 	. . 
	jp p,0f0f1h		;3844	f2 f1 f0 	. . . 
	xor 0edh		;3847	ee ed 	. . 
	call pe,0e9eah		;3849	ec ea e9 	. . . 
	ret pe			;384c	e8 	. 
	and 0e5h		;384d	e6 e5 	. . 
	call po,0e1e2h		;384f	e4 e2 e1 	. . . 
	pop hl			;3852	e1 	. 
	pop hl			;3853	e1 	. 
	rst 38h			;3854	ff 	. 
	rst 38h			;3855	ff 	. 
	rst 38h			;3856	ff 	. 
	rst 38h			;3857	ff 	. 
	rst 38h			;3858	ff 	. 
	rst 38h			;3859	ff 	. 
	rst 38h			;385a	ff 	. 
	rst 38h			;385b	ff 	. 
	pop hl			;385c	e1 	. 
	rst 38h			;385d	ff 	. 
	cp 0ffh		;385e	fe ff 	. . 
	rst 38h			;3860	ff 	. 
	cp 0feh		;3861	fe fe 	. . 
	cp 0feh		;3863	fe fe 	. . 
	cp 0ech		;3865	fe ec 	. . 
	rst 38h			;3867	ff 	. 
	rst 38h			;3868	ff 	. 
	rst 38h			;3869	ff 	. 
	rst 38h			;386a	ff 	. 
	rst 38h			;386b	ff 	. 
	rst 38h			;386c	ff 	. 
	ex de,hl			;386d	eb 	. 
	rst 38h			;386e	ff 	. 
	rst 38h			;386f	ff 	. 
	call pe,0ebe8h		;3870	ec e8 eb 	. . . 
	rst 20h			;3873	e7 	. 
	rst 38h			;3874	ff 	. 
	rst 38h			;3875	ff 	. 
	ret pe			;3876	e8 	. 
	push hl			;3877	e5 	. 
	rst 20h			;3878	e7 	. 
	ex (sp),hl			;3879	e3 	. 
	rst 38h			;387a	ff 	. 
	rst 38h			;387b	ff 	. 
	push hl			;387c	e5 	. 
	call p,0f3e3h		;387d	f4 e3 f3 	. . . 
	jp p,0eff1h		;3880	f2 f1 ef 	. . . 
	xor 0ech		;3883	ee ec 	. . 
	ex de,hl			;3885	eb 	. 
	jp pe,0e7e8h		;3886	ea e8 e7 	. . . 
	and 0e4h		;3889	e6 e4 	. . 
	ex (sp),hl			;388b	e3 	. 
	jp po,0e1e1h		;388c	e2 e1 e1 	. . . 
	pop hl			;388f	e1 	. 
	rst 38h			;3890	ff 	. 
l3891h:
	rst 38h			;3891	ff 	. 
	rst 38h			;3892	ff 	. 
	rst 38h			;3893	ff 	. 
	rst 38h			;3894	ff 	. 
	rst 38h			;3895	ff 	. 
	rst 38h			;3896	ff 	. 
	rst 38h			;3897	ff 	. 
	rst 38h			;3898	ff 	. 
	rst 18h			;3899	df 	. 
	set 7,(hl)		;389a	cb fe 	. . 
	rlca			;389c	07 	. 
	call nc,sub_1ce7h		;389d	d4 e7 1c 	. . . 
	ld a,(bc)			;38a0	0a 	. 
	call nc,sub_1ceah		;38a1	d4 ea 1c 	. . . 
	nop			;38a4	00 	. 
	ld a,083h		;38a5	3e 83 	> . 
	cp 0f3h		;38a7	fe f3 	. . 
	di			;38a9	f3 	. 
	rrca			;38aa	0f 	. 
	ret c			;38ab	d8 	. 
	rst 28h			;38ac	ef 	. 
	djnz l38b2h		;38ad	10 03 	. . 
	ld a,07eh		;38af	3e 7e 	> ~ 
	ld c,e			;38b1	4b 	K 
l38b2h:
	ld a,a			;38b2	7f 	 
	jr c,$+77		;38b3	38 4b 	8 K 
	ld a,(hl)			;38b5	7e 	~ 
	rst 38h			;38b6	ff 	. 
	rrca			;38b7	0f 	. 
	ret c			;38b8	d8 	. 
	rst 28h			;38b9	ef 	. 
	djnz l38bch		;38ba	10 00 	. . 
l38bch:
	ld a,00fh		;38bc	3e 0f 	> . 
	ret c			;38be	d8 	. 
	rst 28h			;38bf	ef 	. 
	djnz l3891h		;38c0	10 cf 	. . 
	jp m,0fcf3h		;38c2	fa f3 fc 	. . . 
	di			;38c5	f3 	. 
	call m,0f3fbh		;38c6	fc fb f3 	. . . 
	call m,0fcf3h		;38c9	fc f3 fc 	. . . 
	ei			;38cc	fb 	. 
l38cdh:
	di			;38cd	f3 	. 
	call m,0fcf3h		;38ce	fc f3 fc 	. . . 
	rst 38h			;38d1	ff 	. 
	rst 30h			;38d2	f7 	. 
	rst 38h			;38d3	ff 	. 
	cp a			;38d4	bf 	. 
	ld c,d			;38d5	4a 	J 
	ld a,a			;38d6	7f 	 
	call nz,0fffch		;38d7	c4 fc ff 	. . . 
	rst 18h			;38da	df 	. 
	rst 38h			;38db	ff 	. 
	set 7,(hl)		;38dc	cb fe 	. . 
	rlca			;38de	07 	. 
	call nc,sub_1ce7h		;38df	d4 e7 1c 	. . . 
	ld a,(bc)			;38e2	0a 	. 
	call nc,sub_1ceah		;38e3	d4 ea 1c 	. . . 
	nop			;38e6	00 	. 
	ld a,083h		;38e7	3e 83 	> . 
	call m,0fee3h		;38e9	fc e3 fe 	. . . 
	cp 00fh		;38ec	fe 0f 	. . 
	ret c			;38ee	d8 	. 
	rst 28h			;38ef	ef 	. 
	djnz l38f2h		;38f0	10 00 	. . 
l38f2h:
	ld a,00fh		;38f2	3e 0f 	> . 
	ret c			;38f4	d8 	. 
	rst 28h			;38f5	ef 	. 
	djnz l38f8h		;38f6	10 00 	. . 
l38f8h:
	ld a,00fh		;38f8	3e 0f 	> . 
	ret c			;38fa	d8 	. 
	rst 28h			;38fb	ef 	. 
	djnz l38cdh		;38fc	10 cf 	. . 
	jp p,0fbfch		;38fe	f2 fc fb 	. . . 
	di			;3901	f3 	. 
	call m,0fcf3h		;3902	fc f3 fc 	. . . 
	ei			;3905	fb 	. 
	di			;3906	f3 	. 
	call m,0fcf3h		;3907	fc f3 fc 	. . . 
	ei			;390a	fb 	. 
	di			;390b	f3 	. 
	call m,0f7ffh		;390c	fc ff f7 	. . . 
	rst 38h			;390f	ff 	. 
	cp a			;3910	bf 	. 
	ld c,d			;3911	4a 	J 
	ld a,a			;3912	7f 	 
	call nz,0fffch		;3913	c4 fc ff 	. . . 
	rst 38h			;3916	ff 	. 
	rst 38h			;3917	ff 	. 
	rst 18h			;3918	df 	. 
	scf			;3919	37 	7 
	or e			;391a	b3 	. 
l391bh:
	scf			;391b	37 	7 
	ret p			;391c	f0 	. 
	rst 30h			;391d	f7 	. 
	or e			;391e	b3 	. 
	scf			;391f	37 	7 
	jr nc,$-71		;3920	30 b7 	0 . 
	or e			;3922	b3 	. 
	ccf			;3923	3f 	? 
	ret m			;3924	f8 	. 
	rst 38h			;3925	ff 	. 
	jp m,0ffffh		;3926	fa ff ff 	. . . 
	ccf			;3929	3f 	? 
	ret m			;392a	f8 	. 
	rst 38h			;392b	ff 	. 
	cp e			;392c	bb 	. 
	ccf			;392d	3f 	? 
	cp b			;392e	b8 	. 
	ccf			;392f	3f 	? 
	defb 0fdh,0bbh,03fh	;illegal sequence		;3930	fd bb 3f 	. . ? 
	call m,0bffbh		;3933	fc fb bf 	. . . 
	scf			;3936	37 	7 
	ret po			;3937	e0 	. 
	rst 30h			;3938	f7 	. 
	or e			;3939	b3 	. 
	scf			;393a	37 	7 
	or b			;393b	b0 	. 
	daa			;393c	27 	' 
	ret po			;393d	e0 	. 
	rst 20h			;393e	e7 	. 
	or e			;393f	b3 	. 
	scf			;3940	37 	7 
	or e			;3941	b3 	. 
	daa			;3942	27 	' 
	daa			;3943	27 	' 
	daa			;3944	27 	' 
	scf			;3945	37 	7 
	scf			;3946	37 	7 
	scf			;3947	37 	7 
	daa			;3948	27 	' 
	daa			;3949	27 	' 
	scf			;394a	37 	7 
	scf			;394b	37 	7 
	daa			;394c	27 	' 
	daa			;394d	27 	' 
	scf			;394e	37 	7 
	scf			;394f	37 	7 
	daa			;3950	27 	' 
	daa			;3951	27 	' 
	scf			;3952	37 	7 
	rst 30h			;3953	f7 	. 
	daa			;3954	27 	' 
	pop hl			;3955	e1 	. 
	rst 30h			;3956	f7 	. 
	rst 30h			;3957	f7 	. 
	rst 20h			;3958	e7 	. 
	jp l37b7h		;3959	c3 b7 37 	. . 7 
	ex (sp),hl			;395c	e3 	. 
	daa			;395d	27 	' 
	ret p			;395e	f0 	. 
	rst 30h			;395f	f7 	. 
	and e			;3960	a3 	. 
	daa			;3961	27 	' 
	jr nc,l391bh		;3962	30 b7 	0 . 
	and e			;3964	a3 	. 
	daa			;3965	27 	' 
	ret p			;3966	f0 	. 
	rst 30h			;3967	f7 	. 
	and 0f7h		;3968	e6 f7 	. . 
	rst 30h			;396a	f7 	. 
	daa			;396b	27 	' 
	scf			;396c	37 	7 
	or b			;396d	b0 	. 
	rst 20h			;396e	e7 	. 
	or e			;396f	b3 	. 
	scf			;3970	37 	7 
	and b			;3971	a0 	. 
	scf			;3972	37 	7 
	ret p			;3973	f0 	. 
	rst 20h			;3974	e7 	. 
	or e			;3975	b3 	. 
	scf			;3976	37 	7 
	and b			;3977	a0 	. 
	scf			;3978	37 	7 
	ret p			;3979	f0 	. 
	rst 30h			;397a	f7 	. 
	or e			;397b	b3 	. 
	scf			;397c	37 	7 
	or e			;397d	b3 	. 
	scf			;397e	37 	7 
	scf			;397f	37 	7 
l3980h:
	scf			;3980	37 	7 
	scf			;3981	37 	7 
	scf			;3982	37 	7 
	scf			;3983	37 	7 
	ccf			;3984	3f 	? 
	ccf			;3985	3f 	? 
	ccf			;3986	3f 	? 
	ccf			;3987	3f 	? 
	ccf			;3988	3f 	? 
	ccf			;3989	3f 	? 
	ccf			;398a	3f 	? 
	ccf			;398b	3f 	? 
	ccf			;398c	3f 	? 
	ccf			;398d	3f 	? 
	ccf			;398e	3f 	? 
	rst 38h			;398f	ff 	. 
	ccf			;3990	3f 	? 
	ld sp,hl			;3991	f9 	. 
	rst 38h			;3992	ff 	. 
	rst 38h			;3993	ff 	. 
	rst 38h			;3994	ff 	. 
	cp e			;3995	bb 	. 
	rst 38h			;3996	ff 	. 
	rst 10h			;3997	d7 	. 
	ld d,a			;3998	57 	W 
	dec b			;3999	05 	. 
	rst 38h			;399a	ff 	. 
	ld b,a			;399b	47 	G 
	nop			;399c	00 	. 
	ld de,0ffffh		;399d	11 ff ff 	. . . 
	rst 38h			;39a0	ff 	. 
	rst 38h			;39a1	ff 	. 
	rst 38h			;39a2	ff 	. 
	rst 38h			;39a3	ff 	. 
	rst 38h			;39a4	ff 	. 
	rst 38h			;39a5	ff 	. 
	rst 38h			;39a6	ff 	. 
	rst 38h			;39a7	ff 	. 
	rst 38h			;39a8	ff 	. 
	rst 38h			;39a9	ff 	. 
	rst 38h			;39aa	ff 	. 
	rst 38h			;39ab	ff 	. 
	rst 38h			;39ac	ff 	. 
	rst 38h			;39ad	ff 	. 
	rst 38h			;39ae	ff 	. 
	rst 38h			;39af	ff 	. 
	ld e,a			;39b0	5f 	_ 
	ld e,a			;39b1	5f 	_ 
	ld e,a			;39b2	5f 	_ 
	ld e,a			;39b3	5f 	_ 
	ld e,a			;39b4	5f 	_ 
	ld e,a			;39b5	5f 	_ 
	rst 38h			;39b6	ff 	. 
	rst 38h			;39b7	ff 	. 
	rst 38h			;39b8	ff 	. 
	rst 38h			;39b9	ff 	. 
	rst 38h			;39ba	ff 	. 
	rst 38h			;39bb	ff 	. 
	ccf			;39bc	3f 	? 
	ccf			;39bd	3f 	? 
	ccf			;39be	3f 	? 
	ccf			;39bf	3f 	? 
	ccf			;39c0	3f 	? 
	ccf			;39c1	3f 	? 
	rst 38h			;39c2	ff 	. 
	rst 38h			;39c3	ff 	. 
	rst 38h			;39c4	ff 	. 
	rst 38h			;39c5	ff 	. 
	rst 38h			;39c6	ff 	. 
	rst 38h			;39c7	ff 	. 
	rst 38h			;39c8	ff 	. 
	cp 0ffh		;39c9	fe ff 	. . 
	rst 38h			;39cb	ff 	. 
	rst 38h			;39cc	ff 	. 
	ld b,b			;39cd	40 	@ 
	ld b,b			;39ce	40 	@ 
	add a,b			;39cf	80 	. 
	cp 020h		;39d0	fe 20 	.   
	ld h,b			;39d2	60 	` 
	and b			;39d3	a0 	. 
	ld b,b			;39d4	40 	@ 
	ld b,b			;39d5	40 	@ 
	ld b,b			;39d6	40 	@ 
	ld b,b			;39d7	40 	@ 
	jr nz,l39fah		;39d8	20 20 	    
	dec bc			;39da	0b 	. 
	ld d,b			;39db	50 	P 
	sub d			;39dc	92 	. 
	ret po			;39dd	e0 	. 
	rst 38h			;39de	ff 	. 
	nop			;39df	00 	. 
	jr nz,l3a52h		;39e0	20 70 	  p 
	or b			;39e2	b0 	. 
	or b			;39e3	b0 	. 
	ld h,b			;39e4	60 	` 
	and b			;39e5	a0 	. 
	cp 020h		;39e6	fe 20 	.   
	ld bc,05480h		;39e8	01 80 54 	. . T 
	rlca			;39eb	07 	. 
	rst 18h			;39ec	df 	. 
	rla			;39ed	17 	. 
	djnz l39f0h		;39ee	10 00 	. . 
l39f0h:
	rlc b		;39f0	cb 00 	. . 
	ld b,b			;39f2	40 	@ 
	ex af,af'			;39f3	08 	. 
	ld sp,020ffh		;39f4	31 ff 20 	1 .   
	dec d			;39f7	15 	. 
	dec d			;39f8	15 	. 
	or b			;39f9	b0 	. 
l39fah:
	ld (052b0h),hl		;39fa	22 b0 52 	" . R 
	or b			;39fd	b0 	. 
	ld e,e			;39fe	5b 	[ 
	or b			;39ff	b0 	. 
	ld h,c			;3a00	61 	a 
	or b			;3a01	b0 	. 
	ld de,l0121h		;3a02	11 21 01 	. ! . 
	dec d			;3a05	15 	. 
	rrca			;3a06	0f 	. 
	nop			;3a07	00 	. 
	rra			;3a08	1f 	. 
	nop			;3a09	00 	. 
	ld c,a			;3a0a	4f 	O 
	nop			;3a0b	00 	. 
	ld d,(hl)			;3a0c	56 	V 
	nop			;3a0d	00 	. 
	ld e,a			;3a0e	5f 	_ 
	nop			;3a0f	00 	. 
	ld bc,0011ch		;3a10	01 1c 01 	. . . 
	ld e,002h		;3a13	1e 02 	. . 
	add hl,de			;3a15	19 	. 
	ld e,b			;3a16	58 	X 
	ld (bc),a			;3a17	02 	. 
	dec de			;3a18	1b 	. 
	ld e,d			;3a19	5a 	Z 
	add a,d			;3a1a	82 	. 
	add hl,sp			;3a1b	39 	9 
	ld a,b			;3a1c	78 	x 
	nop			;3a1d	00 	. 
	nop			;3a1e	00 	. 
	nop			;3a1f	00 	. 
	ld (0f001h),hl		;3a20	22 01 f0 	" . . 
	rla			;3a23	17 	. 
	ld b,c			;3a24	41 	A 
	ret p			;3a25	f0 	. 
	rla			;3a26	17 	. 
	djnz $+18		;3a27	10 10 	. . 
	nop			;3a29	00 	. 
	ld (bc),a			;3a2a	02 	. 
	inc a			;3a2b	3c 	< 
	ld a,e			;3a2c	7b 	{ 
	ld (bc),a			;3a2d	02 	. 
	ld a,(l1679h)		;3a2e	3a 79 16 	: y . 
	inc bc			;3a31	03 	. 
	jp c,0ba07h		;3a32	da 07 ba 	. . . 
	dec bc			;3a35	0b 	. 
	sbc a,d			;3a36	9a 	. 
	ld b,e			;3a37	43 	C 
	jp c,0ba47h		;3a38	da 47 ba 	. G . 
	ld c,e			;3a3b	4b 	K 
	sbc a,d			;3a3c	9a 	. 
	djnz $+3		;3a3d	10 01 	. . 
	ld (hl),001h		;3a3f	36 01 	6 . 
	scf			;3a41	37 	7 
	ld bc,l0138h		;3a42	01 38 01 	. 8 . 
	ld (hl),l			;3a45	75 	u 
	ld bc,00176h		;3a46	01 76 01 	. v . 
	ld (hl),a			;3a49	77 	w 
	ld hl,0f036h		;3a4a	21 36 f0 	! 6 . 
	rla			;3a4d	17 	. 
	ld hl,0f037h		;3a4e	21 37 f0 	! 7 . 
	rla			;3a51	17 	. 
l3a52h:
	ld hl,0f038h		;3a52	21 38 f0 	! 8 . 
	rla			;3a55	17 	. 
	ld hl,0f075h		;3a56	21 75 f0 	! u . 
	rla			;3a59	17 	. 
	ld hl,0f076h		;3a5a	21 76 f0 	! v . 
	rla			;3a5d	17 	. 
	ld hl,0f077h		;3a5e	21 77 f0 	! w . 
	rla			;3a61	17 	. 
	rst 38h			;3a62	ff 	. 
	rst 38h			;3a63	ff 	. 
	rst 38h			;3a64	ff 	. 
	rst 38h			;3a65	ff 	. 
	rst 38h			;3a66	ff 	. 
	rst 38h			;3a67	ff 	. 
	rst 38h			;3a68	ff 	. 
	rst 38h			;3a69	ff 	. 
	rst 38h			;3a6a	ff 	. 
	rst 38h			;3a6b	ff 	. 
	rst 38h			;3a6c	ff 	. 
	rst 38h			;3a6d	ff 	. 
	rst 38h			;3a6e	ff 	. 
	rst 38h			;3a6f	ff 	. 
	rst 38h			;3a70	ff 	. 
	rst 38h			;3a71	ff 	. 
	rst 38h			;3a72	ff 	. 
	rst 38h			;3a73	ff 	. 
	rst 38h			;3a74	ff 	. 
	rst 38h			;3a75	ff 	. 
	rst 38h			;3a76	ff 	. 
	rst 38h			;3a77	ff 	. 
	rst 38h			;3a78	ff 	. 
	rst 38h			;3a79	ff 	. 
	rst 38h			;3a7a	ff 	. 
	rst 38h			;3a7b	ff 	. 
	rst 38h			;3a7c	ff 	. 
	rst 38h			;3a7d	ff 	. 
	rst 38h			;3a7e	ff 	. 
	rst 38h			;3a7f	ff 	. 
	rst 38h			;3a80	ff 	. 
	rst 38h			;3a81	ff 	. 
	rst 38h			;3a82	ff 	. 
	rst 38h			;3a83	ff 	. 
	rst 38h			;3a84	ff 	. 
	rst 38h			;3a85	ff 	. 
	rst 38h			;3a86	ff 	. 
	rst 38h			;3a87	ff 	. 
	rst 38h			;3a88	ff 	. 
	rst 38h			;3a89	ff 	. 
	rst 38h			;3a8a	ff 	. 
	rst 38h			;3a8b	ff 	. 
	rst 38h			;3a8c	ff 	. 
	rst 38h			;3a8d	ff 	. 
	rst 38h			;3a8e	ff 	. 
	rst 38h			;3a8f	ff 	. 
	rst 38h			;3a90	ff 	. 
	rst 38h			;3a91	ff 	. 
	rst 38h			;3a92	ff 	. 
	rst 38h			;3a93	ff 	. 
	rst 38h			;3a94	ff 	. 
	rst 38h			;3a95	ff 	. 
	rst 38h			;3a96	ff 	. 
	rst 38h			;3a97	ff 	. 
	rst 38h			;3a98	ff 	. 
	rst 38h			;3a99	ff 	. 
	rst 38h			;3a9a	ff 	. 
	rst 38h			;3a9b	ff 	. 
	rst 38h			;3a9c	ff 	. 
	rst 38h			;3a9d	ff 	. 
	rst 38h			;3a9e	ff 	. 
	rst 38h			;3a9f	ff 	. 
	rst 38h			;3aa0	ff 	. 
	rst 38h			;3aa1	ff 	. 
	rst 38h			;3aa2	ff 	. 
	rst 38h			;3aa3	ff 	. 
	rst 38h			;3aa4	ff 	. 
	rst 38h			;3aa5	ff 	. 
	rst 38h			;3aa6	ff 	. 
	rst 38h			;3aa7	ff 	. 
	rst 38h			;3aa8	ff 	. 
	rst 38h			;3aa9	ff 	. 
	rst 38h			;3aaa	ff 	. 
	rst 38h			;3aab	ff 	. 
	rst 38h			;3aac	ff 	. 
	rst 38h			;3aad	ff 	. 
	rst 38h			;3aae	ff 	. 
	rst 38h			;3aaf	ff 	. 
	rst 38h			;3ab0	ff 	. 
	rst 38h			;3ab1	ff 	. 
	rst 38h			;3ab2	ff 	. 
	rst 38h			;3ab3	ff 	. 
	rst 38h			;3ab4	ff 	. 
	rst 38h			;3ab5	ff 	. 
	rst 38h			;3ab6	ff 	. 
	rst 38h			;3ab7	ff 	. 
	rst 38h			;3ab8	ff 	. 
	rst 38h			;3ab9	ff 	. 
	rst 38h			;3aba	ff 	. 
	rst 38h			;3abb	ff 	. 
	rst 38h			;3abc	ff 	. 
	rst 38h			;3abd	ff 	. 
	rst 38h			;3abe	ff 	. 
	rst 38h			;3abf	ff 	. 
	rst 38h			;3ac0	ff 	. 
	rst 38h			;3ac1	ff 	. 
	rst 38h			;3ac2	ff 	. 
	rst 38h			;3ac3	ff 	. 
	rst 38h			;3ac4	ff 	. 
	rst 38h			;3ac5	ff 	. 
	rst 38h			;3ac6	ff 	. 
	rst 38h			;3ac7	ff 	. 
	rst 38h			;3ac8	ff 	. 
	rst 38h			;3ac9	ff 	. 
	rst 38h			;3aca	ff 	. 
	rst 38h			;3acb	ff 	. 
	jp p,0100fh		;3acc	f2 0f 10 	. . . 
	ret pe			;3acf	e8 	. 
	push af			;3ad0	f5 	. 
	rst 38h			;3ad1	ff 	. 
	rst 28h			;3ad2	ef 	. 
	pop de			;3ad3	d1 	. 
	rst 38h			;3ad4	ff 	. 
	ret pe			;3ad5	e8 	. 
	rst 20h			;3ad6	e7 	. 
	adc a,l			;3ad7	8d 	. 
	rst 38h			;3ad8	ff 	. 
	pop de			;3ad9	d1 	. 
	call nz,0ff11h		;3ada	c4 11 ff 	. . . 
	rst 38h			;3add	ff 	. 
	rst 38h			;3ade	ff 	. 
	rst 38h			;3adf	ff 	. 
	rst 38h			;3ae0	ff 	. 
	inc a			;3ae1	3c 	< 
	rst 38h			;3ae2	ff 	. 
	rst 38h			;3ae3	ff 	. 
	xor e			;3ae4	ab 	. 
	ld e,c			;3ae5	59 	Y 
	inc a			;3ae6	3c 	< 
	cp 0ffh		;3ae7	fe ff 	. . 
	rst 38h			;3ae9	ff 	. 
	call m,0ffffh		;3aea	fc ff ff 	. . . 
	ld (iy-001h),c		;3aed	fd 71 ff 	. q . 
	rst 38h			;3af0	ff 	. 
	ld e,c			;3af1	59 	Y 
	dec c			;3af2	0d 	. 
	ld (hl),c			;3af3	71 	q 
	defb 0fdh,0ech,0e4h	;illegal sequence		;3af4	fd ec e4 	. . . 
	pop bc			;3af7	c1 	. 
	adc a,h			;3af8	8c 	. 
	sub c			;3af9	91 	. 
	ld e,l			;3afa	5d 	] 
	dec a			;3afb	3d 	= 
	djnz l3b19h		;3afc	10 1b 	. . 
	rlca			;3afe	07 	. 
	cp (hl)			;3aff	be 	. 
	cp h			;3b00	bc 	. 
	and a			;3b01	a7 	. 
	rrca			;3b02	0f 	. 
	rrca			;3b03	0f 	. 
	rrca			;3b04	0f 	. 
	rst 38h			;3b05	ff 	. 
	jp m,0ffffh		;3b06	fa ff ff 	. . . 
	rst 38h			;3b09	ff 	. 
	rst 38h			;3b0a	ff 	. 
	ei			;3b0b	fb 	. 
	pop af			;3b0c	f1 	. 
	rrca			;3b0d	0f 	. 
	rst 38h			;3b0e	ff 	. 
	add a,h			;3b0f	84 	. 
	rst 38h			;3b10	ff 	. 
	rst 38h			;3b11	ff 	. 
	adc a,h			;3b12	8c 	. 
	ld h,(hl)			;3b13	66 	f 
	rst 38h			;3b14	ff 	. 
	add a,h			;3b15	84 	. 
	add a,c			;3b16	81 	. 
	dec (hl)			;3b17	35 	5 
	rst 38h			;3b18	ff 	. 
l3b19h:
	ld h,(hl)			;3b19	66 	f 
	ld h,e			;3b1a	63 	c 
	cpl			;3b1b	2f 	/ 
	rst 38h			;3b1c	ff 	. 
	rst 38h			;3b1d	ff 	. 
	or l			;3b1e	b5 	. 
	rst 38h			;3b1f	ff 	. 
	rst 38h			;3b20	ff 	. 
	cpl			;3b21	2f 	/ 
	ld h,e			;3b22	63 	c 
	or l			;3b23	b5 	. 
	rst 38h			;3b24	ff 	. 
	rst 38h			;3b25	ff 	. 
	or 0a9h		;3b26	f6 a9 	. . 
	rst 30h			;3b28	f7 	. 
	rst 38h			;3b29	ff 	. 
	ld h,d			;3b2a	62 	b 
	rlca			;3b2b	07 	. 
	xor c			;3b2c	a9 	. 
	add a,d			;3b2d	82 	. 
	rst 38h			;3b2e	ff 	. 
	rst 38h			;3b2f	ff 	. 
	rlca			;3b30	07 	. 
	ld a,e			;3b31	7b 	{ 
	add a,d			;3b32	82 	. 
	adc a,e			;3b33	8b 	. 
	ld l,e			;3b34	6b 	k 
	ld d,e			;3b35	53 	S 
	ld (0e011h),hl		;3b36	22 11 e0 	" . . 
	jp 082cbh		;3b39	c3 cb 82 	. . . 
	ld l,l			;3b3c	6d 	m 
	ld l,h			;3b3d	6c 	l 
	ld c,(hl)			;3b3e	4e 	N 
	ld b,b			;3b3f	40 	@ 
	jr nz,l3b51h		;3b40	20 0f 	  . 
	rrca			;3b42	0f 	. 
	rrca			;3b43	0f 	. 
	rst 38h			;3b44	ff 	. 
	ret m			;3b45	f8 	. 
	rst 38h			;3b46	ff 	. 
	rst 38h			;3b47	ff 	. 
	rst 38h			;3b48	ff 	. 
	rst 38h			;3b49	ff 	. 
	ld sp,hl			;3b4a	f9 	. 
	pop af			;3b4b	f1 	. 
	rst 38h			;3b4c	ff 	. 
	ret pe			;3b4d	e8 	. 
	ret pe			;3b4e	e8 	. 
	rst 38h			;3b4f	ff 	. 
	rst 38h			;3b50	ff 	. 
l3b51h:
	rst 38h			;3b51	ff 	. 
	rst 38h			;3b52	ff 	. 
	rst 38h			;3b53	ff 	. 
	rst 38h			;3b54	ff 	. 
	rst 38h			;3b55	ff 	. 
	rst 38h			;3b56	ff 	. 
	rst 38h			;3b57	ff 	. 
	rst 38h			;3b58	ff 	. 
	rst 38h			;3b59	ff 	. 
	rst 38h			;3b5a	ff 	. 
	ret pe			;3b5b	e8 	. 
	rst 38h			;3b5c	ff 	. 
	rst 38h			;3b5d	ff 	. 
	rst 38h			;3b5e	ff 	. 
	rst 38h			;3b5f	ff 	. 
	rst 38h			;3b60	ff 	. 
	ret m			;3b61	f8 	. 
	rst 38h			;3b62	ff 	. 
	rst 38h			;3b63	ff 	. 
	ret m			;3b64	f8 	. 
	push af			;3b65	f5 	. 
	ret m			;3b66	f8 	. 
	rst 38h			;3b67	ff 	. 
	rst 38h			;3b68	ff 	. 
	rst 38h			;3b69	ff 	. 
	rst 38h			;3b6a	ff 	. 
	rst 38h			;3b6b	ff 	. 
	rst 38h			;3b6c	ff 	. 
	rst 38h			;3b6d	ff 	. 
	call p,0ffffh		;3b6e	f4 ff ff 	. . . 
	push af			;3b71	f5 	. 
	ret m			;3b72	f8 	. 
	call p,0f5f6h		;3b73	f4 f6 f5 	. . . 
	call p,0f2f3h		;3b76	f4 f3 f2 	. . . 
	pop af			;3b79	f1 	. 
	ret p			;3b7a	f0 	. 
	rst 28h			;3b7b	ef 	. 
	xor 0edh		;3b7c	ee ed 	. . 
	call pe,0e9eah		;3b7e	ec ea e9 	. . . 
	ret pe			;3b81	e8 	. 
	ret pe			;3b82	e8 	. 
	ret pe			;3b83	e8 	. 
	ret pe			;3b84	e8 	. 
	rst 38h			;3b85	ff 	. 
	rst 38h			;3b86	ff 	. 
	rst 38h			;3b87	ff 	. 
	rst 38h			;3b88	ff 	. 
	rst 38h			;3b89	ff 	. 
	rst 38h			;3b8a	ff 	. 
	rst 38h			;3b8b	ff 	. 
	rst 38h			;3b8c	ff 	. 
	ret pe			;3b8d	e8 	. 
	rst 38h			;3b8e	ff 	. 
	rst 38h			;3b8f	ff 	. 
	rst 38h			;3b90	ff 	. 
	rst 38h			;3b91	ff 	. 
	rst 38h			;3b92	ff 	. 
	rst 38h			;3b93	ff 	. 
	rst 38h			;3b94	ff 	. 
	rst 38h			;3b95	ff 	. 
	rst 38h			;3b96	ff 	. 
	rst 38h			;3b97	ff 	. 
	rst 38h			;3b98	ff 	. 
	rst 38h			;3b99	ff 	. 
	rst 38h			;3b9a	ff 	. 
	rst 28h			;3b9b	ef 	. 
	rst 38h			;3b9c	ff 	. 
	rst 38h			;3b9d	ff 	. 
	xor 0ffh		;3b9e	ee ff 	. . 
	rst 38h			;3ba0	ff 	. 
	rst 28h			;3ba1	ef 	. 
	ex de,hl			;3ba2	eb 	. 
	xor 0ffh		;3ba3	ee ff 	. . 
	rst 38h			;3ba5	ff 	. 
	rst 38h			;3ba6	ff 	. 
	jp (hl)			;3ba7	e9 	. 
	rst 38h			;3ba8	ff 	. 
	rst 38h			;3ba9	ff 	. 
	ex de,hl			;3baa	eb 	. 
	jp p,0f0e9h		;3bab	f2 e9 f0 	. . . 
	rst 38h			;3bae	ff 	. 
	rst 38h			;3baf	ff 	. 
	jp p,0f0f7h		;3bb0	f2 f7 f0 	. . . 
	or 0f5h		;3bb3	f6 f5 	. . 
	call p,0f2f3h		;3bb5	f4 f3 f2 	. . . 
	ret p			;3bb8	f0 	. 
	rst 28h			;3bb9	ef 	. 
	xor 0edh		;3bba	ee ed 	. . 
	call pe,0eaebh		;3bbc	ec eb ea 	. . . 
	jp (hl)			;3bbf	e9 	. 
	ret pe			;3bc0	e8 	. 
	ret pe			;3bc1	e8 	. 
l3bc2h:
	ret pe			;3bc2	e8 	. 
	ret pe			;3bc3	e8 	. 
	rst 38h			;3bc4	ff 	. 
	rst 38h			;3bc5	ff 	. 
	rst 38h			;3bc6	ff 	. 
	rst 38h			;3bc7	ff 	. 
	rst 38h			;3bc8	ff 	. 
	rst 38h			;3bc9	ff 	. 
	rst 38h			;3bca	ff 	. 
	rst 38h			;3bcb	ff 	. 
	rst 18h			;3bcc	df 	. 
	set 7,(hl)		;3bcd	cb fe 	. . 
	rlca			;3bcf	07 	. 
	call nc,sub_1ce7h		;3bd0	d4 e7 1c 	. . . 
	ld a,(bc)			;3bd3	0a 	. 
	call nc,sub_1ceah		;3bd4	d4 ea 1c 	. . . 
	ld a,(bc)			;3bd7	0a 	. 
	call nc,sub_1ceah		;3bd8	d4 ea 1c 	. . . 
	nop			;3bdb	00 	. 
	ld a,083h		;3bdc	3e 83 	> . 
	cp 0f3h		;3bde	fe f3 	. . 
	di			;3be0	f3 	. 
	rrca			;3be1	0f 	. 
	ret c			;3be2	d8 	. 
	rst 28h			;3be3	ef 	. 
	djnz l3be9h		;3be4	10 03 	. . 
	ld a,07eh		;3be6	3e 7e 	> ~ 
	ld c,e			;3be8	4b 	K 
l3be9h:
	rst 38h			;3be9	ff 	. 
	jr c,$+77		;3bea	38 4b 	8 K 
	ld a,(hl)			;3bec	7e 	~ 
	rst 38h			;3bed	ff 	. 
	rrca			;3bee	0f 	. 
	ret c			;3bef	d8 	. 
	rst 28h			;3bf0	ef 	. 
	djnz l3bc2h		;3bf1	10 cf 	. . 
	jp m,0fcf3h		;3bf3	fa f3 fc 	. . . 
	di			;3bf6	f3 	. 
	call m,0fbfch		;3bf7	fc fc fb 	. . . 
	call p,0f3fch		;3bfa	f4 fc f3 	. . . 
	ei			;3bfd	fb 	. 
	call m,0f4fbh		;3bfe	fc fb f4 	. . . 
l3c01h:
	call m,0f7f7h		;3c01	fc f7 f7 	. . . 
	rst 38h			;3c04	ff 	. 
	cp a			;3c05	bf 	. 
	ld c,d			;3c06	4a 	J 
	ld a,a			;3c07	7f 	 
	call nz,0fffch		;3c08	c4 fc ff 	. . . 
	rst 38h			;3c0b	ff 	. 
	rst 18h			;3c0c	df 	. 
	set 7,(hl)		;3c0d	cb fe 	. . 
	rlca			;3c0f	07 	. 
	call nc,sub_1ce7h		;3c10	d4 e7 1c 	. . . 
	rlca			;3c13	07 	. 
	call nc,sub_1ce7h		;3c14	d4 e7 1c 	. . . 
	ld a,(bc)			;3c17	0a 	. 
	call nc,sub_1ceah		;3c18	d4 ea 1c 	. . . 
	nop			;3c1b	00 	. 
	ld a,0b8h		;3c1c	3e b8 	> . 
	rrca			;3c1e	0f 	. 
	ret c			;3c1f	d8 	. 
	rst 28h			;3c20	ef 	. 
	djnz l3c23h		;3c21	10 00 	. . 
l3c23h:
	ld a,023h		;3c23	3e 23 	> # 
	ld a,0feh		;3c25	3e fe 	> . 
	rrca			;3c27	0f 	. 
	ret c			;3c28	d8 	. 
	rst 28h			;3c29	ef 	. 
	djnz l3c2ch		;3c2a	10 00 	. . 
l3c2ch:
	ld a,00fh		;3c2c	3e 0f 	> . 
	ret c			;3c2e	d8 	. 
	rst 28h			;3c2f	ef 	. 
	djnz l3c01h		;3c30	10 cf 	. . 
	jp p,0fcfbh		;3c32	f2 fb fc 	. . . 
	di			;3c35	f3 	. 
	call m,0fbf4h		;3c36	fc f4 fb 	. . . 
	call m,0fbfbh		;3c39	fc fb fb 	. . . 
	call p,0f3fch		;3c3c	f4 fc f3 	. . . 
	call m,0f7fch		;3c3f	fc fc f7 	. . . 
	rst 30h			;3c42	f7 	. 
	rst 38h			;3c43	ff 	. 
	cp a			;3c44	bf 	. 
	ld c,d			;3c45	4a 	J 
	ld a,a			;3c46	7f 	 
	call nz,0fffch		;3c47	c4 fc ff 	. . . 
	rst 38h			;3c4a	ff 	. 
	rst 18h			;3c4b	df 	. 
	scf			;3c4c	37 	7 
	or e			;3c4d	b3 	. 
	scf			;3c4e	37 	7 
	or b			;3c4f	b0 	. 
	rst 30h			;3c50	f7 	. 
	or e			;3c51	b3 	. 
	scf			;3c52	37 	7 
	ret p			;3c53	f0 	. 
	or a			;3c54	b7 	. 
	or e			;3c55	b3 	. 
	ccf			;3c56	3f 	? 
	ret m			;3c57	f8 	. 
	cp a			;3c58	bf 	. 
	cp e			;3c59	bb 	. 
	ccf			;3c5a	3f 	? 
	ret m			;3c5b	f8 	. 
	rst 38h			;3c5c	ff 	. 
	jp m,0ffffh		;3c5d	fa ff ff 	. . . 
	ccf			;3c60	3f 	? 
	ret m			;3c61	f8 	. 
	rst 38h			;3c62	ff 	. 
	cp e			;3c63	bb 	. 
	ccf			;3c64	3f 	? 
	cp b			;3c65	b8 	. 
	ccf			;3c66	3f 	? 
	defb 0fdh,0bbh,037h	;illegal sequence		;3c67	fd bb 37 	. . 7 
	call po,0b7f3h		;3c6a	e4 f3 b7 	. . . 
	scf			;3c6d	37 	7 
	ret p			;3c6e	f0 	. 
	rst 20h			;3c6f	e7 	. 
	and e			;3c70	a3 	. 
	daa			;3c71	27 	' 
	or e			;3c72	b3 	. 
	scf			;3c73	37 	7 
	scf			;3c74	37 	7 
	daa			;3c75	27 	' 
	daa			;3c76	27 	' 
	daa			;3c77	27 	' 
	scf			;3c78	37 	7 
	scf			;3c79	37 	7 
	scf			;3c7a	37 	7 
	daa			;3c7b	27 	' 
	daa			;3c7c	27 	' 
	scf			;3c7d	37 	7 
	scf			;3c7e	37 	7 
	daa			;3c7f	27 	' 
	daa			;3c80	27 	' 
	scf			;3c81	37 	7 
	inc sp			;3c82	33 	3 
	daa			;3c83	27 	' 
	rst 20h			;3c84	e7 	. 
	scf			;3c85	37 	7 
	pop af			;3c86	f1 	. 
	rst 20h			;3c87	e7 	. 
	rst 20h			;3c88	e7 	. 
	rst 30h			;3c89	f7 	. 
	or e			;3c8a	b3 	. 
	rst 0			;3c8b	c7 	. 
	daa			;3c8c	27 	' 
	di			;3c8d	f3 	. 
	scf			;3c8e	37 	7 
	ret po			;3c8f	e0 	. 
	rst 20h			;3c90	e7 	. 
	or e			;3c91	b3 	. 
	scf			;3c92	37 	7 
	ret po			;3c93	e0 	. 
	and a			;3c94	a7 	. 
	or e			;3c95	b3 	. 
	scf			;3c96	37 	7 
	ret po			;3c97	e0 	. 
	and a			;3c98	a7 	. 
	or e			;3c99	b3 	. 
	scf			;3c9a	37 	7 
	ret po			;3c9b	e0 	. 
	rst 30h			;3c9c	f7 	. 
	ld (hl),0e0h		;3c9d	36 e0 	6 . 
	rst 30h			;3c9f	f7 	. 
	or e			;3ca0	b3 	. 
	daa			;3ca1	27 	' 
	or b			;3ca2	b0 	. 
	rst 30h			;3ca3	f7 	. 
	call po,sub_3737h		;3ca4	e4 37 37 	. 7 7 
	and b			;3ca7	a0 	. 
	rst 30h			;3ca8	f7 	. 
	or e			;3ca9	b3 	. 
	daa			;3caa	27 	' 
	or b			;3cab	b0 	. 
	scf			;3cac	37 	7 
	ret p			;3cad	f0 	. 
	rst 30h			;3cae	f7 	. 
	or e			;3caf	b3 	. 
	scf			;3cb0	37 	7 
	or e			;3cb1	b3 	. 
	scf			;3cb2	37 	7 
	scf			;3cb3	37 	7 
	scf			;3cb4	37 	7 
	scf			;3cb5	37 	7 
	scf			;3cb6	37 	7 
	ccf			;3cb7	3f 	? 
	ccf			;3cb8	3f 	? 
	ccf			;3cb9	3f 	? 
	ccf			;3cba	3f 	? 
	ccf			;3cbb	3f 	? 
	ccf			;3cbc	3f 	? 
	ccf			;3cbd	3f 	? 
	ccf			;3cbe	3f 	? 
	ccf			;3cbf	3f 	? 
	ccf			;3cc0	3f 	? 
	dec sp			;3cc1	3b 	; 
	ccf			;3cc2	3f 	? 
	rst 38h			;3cc3	ff 	. 
	ccf			;3cc4	3f 	? 
	ld sp,hl			;3cc5	f9 	. 
	rst 38h			;3cc6	ff 	. 
	rst 38h			;3cc7	ff 	. 
	rst 38h			;3cc8	ff 	. 
	cp e			;3cc9	bb 	. 
	rst 10h			;3cca	d7 	. 
	ld d,a			;3ccb	57 	W 
	ld b,0ffh		;3ccc	06 ff 	. . 
	ld b,a			;3cce	47 	G 
	inc c			;3ccf	0c 	. 
	djnz $+1		;3cd0	10 ff 	. . 
	jp m,0ffffh		;3cd2	fa ff ff 	. . . 
	rst 38h			;3cd5	ff 	. 
	rst 38h			;3cd6	ff 	. 
	rst 38h			;3cd7	ff 	. 
	rst 38h			;3cd8	ff 	. 
	rst 38h			;3cd9	ff 	. 
	rst 38h			;3cda	ff 	. 
	rst 38h			;3cdb	ff 	. 
	rst 38h			;3cdc	ff 	. 
	rst 38h			;3cdd	ff 	. 
	rst 38h			;3cde	ff 	. 
	rst 38h			;3cdf	ff 	. 
	rst 38h			;3ce0	ff 	. 
	nop			;3ce1	00 	. 
	nop			;3ce2	00 	. 
	ld e,a			;3ce3	5f 	_ 
	ld e,a			;3ce4	5f 	_ 
	ld e,a			;3ce5	5f 	_ 
	ld e,a			;3ce6	5f 	_ 
	rra			;3ce7	1f 	. 
	rra			;3ce8	1f 	. 
	rst 38h			;3ce9	ff 	. 
	rst 38h			;3cea	ff 	. 
	rst 38h			;3ceb	ff 	. 
	rst 38h			;3cec	ff 	. 
	rst 38h			;3ced	ff 	. 
	rst 38h			;3cee	ff 	. 
	rst 38h			;3cef	ff 	. 
	rst 38h			;3cf0	ff 	. 
	rst 38h			;3cf1	ff 	. 
	rst 38h			;3cf2	ff 	. 
	rst 38h			;3cf3	ff 	. 
	rst 38h			;3cf4	ff 	. 
	rst 38h			;3cf5	ff 	. 
	rst 38h			;3cf6	ff 	. 
	rst 38h			;3cf7	ff 	. 
	rst 38h			;3cf8	ff 	. 
	rst 38h			;3cf9	ff 	. 
	rst 38h			;3cfa	ff 	. 
	rst 38h			;3cfb	ff 	. 
	cp 0ffh		;3cfc	fe ff 	. . 
	rst 38h			;3cfe	ff 	. 
	rst 38h			;3cff	ff 	. 
	ld d,060h		;3d00	16 60 	. ` 
	and b			;3d02	a0 	. 
	ret m			;3d03	f8 	. 
	djnz l3d36h		;3d04	10 30 	. 0 
	ld h,b			;3d06	60 	` 
	ld b,b			;3d07	40 	@ 
	ld b,b			;3d08	40 	@ 
	jr nz,$+34		;3d09	20 20 	    
	nop			;3d0b	00 	. 
	nop			;3d0c	00 	. 
	inc b			;3d0d	04 	. 
	ld h,b			;3d0e	60 	` 
	and b			;3d0f	a0 	. 
	ret nc			;3d10	d0 	. 
	rst 38h			;3d11	ff 	. 
	nop			;3d12	00 	. 
	jr nz,l3d55h		;3d13	20 40 	  @ 
	add a,b			;3d15	80 	. 
	ret nz			;3d16	c0 	. 
	ld (hl),b			;3d17	70 	p 
	and b			;3d18	a0 	. 
	ret m			;3d19	f8 	. 
	inc b			;3d1a	04 	. 
	ld bc,07e80h		;3d1b	01 80 7e 	. . ~ 
	dec b			;3d1e	05 	. 
	rst 18h			;3d1f	df 	. 
	dec bc			;3d20	0b 	. 
	dec c			;3d21	0d 	. 
	ld bc,l02abh		;3d22	01 ab 02 	. . . 
	jr nz,l3d2ch		;3d25	20 05 	  . 
	ld (hl),0ffh		;3d27	36 ff 	6 . 
	ld (sub_021ch+1),hl		;3d29	22 1d 02 	" . . 
l3d2ch:
	nop			;3d2c	00 	. 
	ld c,d			;3d2d	4a 	J 
	add a,d			;3d2e	82 	. 
	nop			;3d2f	00 	. 
	inc d			;3d30	14 	. 
	add hl,bc			;3d31	09 	. 
	or b			;3d32	b0 	. 
	dec c			;3d33	0d 	. 
	or b			;3d34	b0 	. 
	ld b,d			;3d35	42 	B 
l3d36h:
	or b			;3d36	b0 	. 
	ld c,h			;3d37	4c 	L 
	or b			;3d38	b0 	. 
	ld (de),a			;3d39	12 	. 
	ld l,000h		;3d3a	2e 00 	. . 
	ld h,(hl)			;3d3c	66 	f 
	nop			;3d3d	00 	. 
	ld (de),a			;3d3e	12 	. 
	dec hl			;3d3f	2b 	+ 
	nop			;3d40	00 	. 
	ld h,e			;3d41	63 	c 
	nop			;3d42	00 	. 
	ld (bc),a			;3d43	02 	. 
	add hl,hl			;3d44	29 	) 
	ld h,d			;3d45	62 	b 
	ld (bc),a			;3d46	02 	. 
	daa			;3d47	27 	' 
	ld h,b			;3d48	60 	` 
	ld (bc),a			;3d49	02 	. 
	jr nc,l3db4h		;3d4a	30 68 	0 h 
	ld (bc),a			;3d4c	02 	. 
	ld (l026ah),a		;3d4d	32 6a 02 	2 j . 
	scf			;3d50	37 	7 
	ld l,l			;3d51	6d 	m 
	inc b			;3d52	04 	. 
	jr c,$+59		;3d53	38 39 	8 9 
l3d55h:
	ld l,(hl)			;3d55	6e 	n 
	ld l,a			;3d56	6f 	o 
	nop			;3d57	00 	. 
	ld (bc),a			;3d58	02 	. 
	inc (hl)			;3d59	34 	4 
	ld l,e			;3d5a	6b 	k 
	ld (0e12dh),hl		;3d5b	22 2d e1 	" - . 
	dec bc			;3d5e	0b 	. 
	ld h,l			;3d5f	65 	e 
	pop hl			;3d60	e1 	. 
	dec bc			;3d61	0b 	. 
	djnz l3d74h		;3d62	10 10 	. . 
	nop			;3d64	00 	. 
	ld bc,l0105h		;3d65	01 05 01 	. . . 
	rlca			;3d68	07 	. 
	inc d			;3d69	14 	. 
	rra			;3d6a	1f 	. 
	jp c,0ba23h		;3d6b	da 23 ba 	. # . 
	ld e,b			;3d6e	58 	X 
	jp c,0ba5ch		;3d6f	da 5c ba 	. \ . 
	ld d,001h		;3d72	16 01 	. . 
l3d74h:
	xor b			;3d74	a8 	. 
	ld de,l15a8h		;3d75	11 a8 15 	. . . 
	xor b			;3d78	a8 	. 
	ld a,0a8h		;3d79	3e a8 	> . 
	ld d,b			;3d7b	50 	P 
	xor b			;3d7c	a8 	. 
	ld d,h			;3d7d	54 	T 
	xor b			;3d7e	a8 	. 
	ld bc,l0139h+1		;3d7f	01 3a 01 	. : . 
	dec sp			;3d82	3b 	; 
	ld bc,l0171h		;3d83	01 71 01 	. q . 
	ld (hl),d			;3d86	72 	r 
	nop			;3d87	00 	. 
	nop			;3d88	00 	. 
	ld hl,0e13ah		;3d89	21 3a e1 	! : . 
	dec bc			;3d8c	0b 	. 
	ld hl,0e13bh		;3d8d	21 3b e1 	! ; . 
	dec bc			;3d90	0b 	. 
	ld hl,0e171h		;3d91	21 71 e1 	! q . 
	dec bc			;3d94	0b 	. 
	ld hl,0e172h		;3d95	21 72 e1 	! r . 
	dec bc			;3d98	0b 	. 
	jr nz,l3dbbh		;3d99	20 20 	    
	rst 38h			;3d9b	ff 	. 
	rst 38h			;3d9c	ff 	. 
	rst 38h			;3d9d	ff 	. 
	rst 38h			;3d9e	ff 	. 
	rst 38h			;3d9f	ff 	. 
	rst 38h			;3da0	ff 	. 
	rst 38h			;3da1	ff 	. 
	rst 38h			;3da2	ff 	. 
	rst 38h			;3da3	ff 	. 
	rst 38h			;3da4	ff 	. 
	rst 38h			;3da5	ff 	. 
	rst 38h			;3da6	ff 	. 
	rst 38h			;3da7	ff 	. 
	rst 38h			;3da8	ff 	. 
	rst 38h			;3da9	ff 	. 
	rst 38h			;3daa	ff 	. 
	rst 38h			;3dab	ff 	. 
	rst 38h			;3dac	ff 	. 
	rst 38h			;3dad	ff 	. 
	rst 38h			;3dae	ff 	. 
	rst 38h			;3daf	ff 	. 
	rst 38h			;3db0	ff 	. 
	rst 38h			;3db1	ff 	. 
	rst 38h			;3db2	ff 	. 
	rst 38h			;3db3	ff 	. 
l3db4h:
	rst 38h			;3db4	ff 	. 
	rst 38h			;3db5	ff 	. 
	rst 38h			;3db6	ff 	. 
	rst 38h			;3db7	ff 	. 
	rst 38h			;3db8	ff 	. 
	rst 38h			;3db9	ff 	. 
	rst 38h			;3dba	ff 	. 
l3dbbh:
	rst 38h			;3dbb	ff 	. 
	rst 38h			;3dbc	ff 	. 
	rst 38h			;3dbd	ff 	. 
	rst 38h			;3dbe	ff 	. 
	rst 38h			;3dbf	ff 	. 
	rst 38h			;3dc0	ff 	. 
	rst 38h			;3dc1	ff 	. 
	rst 38h			;3dc2	ff 	. 
	rst 38h			;3dc3	ff 	. 
	rst 38h			;3dc4	ff 	. 
	rst 38h			;3dc5	ff 	. 
	rst 38h			;3dc6	ff 	. 
	rst 38h			;3dc7	ff 	. 
	rst 38h			;3dc8	ff 	. 
	rst 38h			;3dc9	ff 	. 
	rst 38h			;3dca	ff 	. 
	rst 38h			;3dcb	ff 	. 
	rst 38h			;3dcc	ff 	. 
	rst 38h			;3dcd	ff 	. 
	rst 38h			;3dce	ff 	. 
	rst 38h			;3dcf	ff 	. 
	rst 38h			;3dd0	ff 	. 
	rst 38h			;3dd1	ff 	. 
	rst 38h			;3dd2	ff 	. 
	rst 38h			;3dd3	ff 	. 
	rst 38h			;3dd4	ff 	. 
	rst 38h			;3dd5	ff 	. 
	rst 38h			;3dd6	ff 	. 
	rst 38h			;3dd7	ff 	. 
	rst 38h			;3dd8	ff 	. 
	rst 38h			;3dd9	ff 	. 
	rst 38h			;3dda	ff 	. 
	rst 38h			;3ddb	ff 	. 
	rst 38h			;3ddc	ff 	. 
	rst 38h			;3ddd	ff 	. 
	rst 38h			;3dde	ff 	. 
	rst 38h			;3ddf	ff 	. 
	rst 38h			;3de0	ff 	. 
l3de1h:
	rst 38h			;3de1	ff 	. 
	rst 38h			;3de2	ff 	. 
	rst 38h			;3de3	ff 	. 
	rst 38h			;3de4	ff 	. 
	rst 38h			;3de5	ff 	. 
	rst 38h			;3de6	ff 	. 
	rst 38h			;3de7	ff 	. 
	rst 38h			;3de8	ff 	. 
	rst 38h			;3de9	ff 	. 
	rst 38h			;3dea	ff 	. 
	rst 38h			;3deb	ff 	. 
	rst 38h			;3dec	ff 	. 
	rst 38h			;3ded	ff 	. 
	rst 38h			;3dee	ff 	. 
	rst 38h			;3def	ff 	. 
	rst 38h			;3df0	ff 	. 
	rst 38h			;3df1	ff 	. 
	rst 38h			;3df2	ff 	. 
	rst 38h			;3df3	ff 	. 
	rst 38h			;3df4	ff 	. 
	rst 38h			;3df5	ff 	. 
	rst 38h			;3df6	ff 	. 
	rst 38h			;3df7	ff 	. 
	rst 38h			;3df8	ff 	. 
	rst 38h			;3df9	ff 	. 
	rst 38h			;3dfa	ff 	. 
	rst 38h			;3dfb	ff 	. 
	rst 38h			;3dfc	ff 	. 
	rst 38h			;3dfd	ff 	. 
	rst 38h			;3dfe	ff 	. 
	jp p,0c51ah		;3dff	f2 1a c5 	. . . 
	rra			;3e02	1f 	. 
	push bc			;3e03	c5 	. 
	rra			;3e04	1f 	. 
	ld a,(de)			;3e05	1a 	. 
	ld e,0ffh		;3e06	1e ff 	. . 
	add hl,de			;3e08	19 	. 
	ld a,(bc)			;3e09	0a 	. 
	rra			;3e0a	1f 	. 
	ld a,(bc)			;3e0b	0a 	. 
	and e			;3e0c	a3 	. 
	jp m,0fa19h		;3e0d	fa 19 fa 	. . . 
	ld hl,0a3f9h		;3e10	21 f9 a3 	! . . 
	ld sp,hl			;3e13	f9 	. 
	ld (hl),a			;3e14	77 	w 
	ret m			;3e15	f8 	. 
	ld hl,0feffh		;3e16	21 ff fe 	! . . 
	ld (iy-001h),a		;3e19	fd 77 ff 	. w . 
	rst 38h			;3e1c	ff 	. 
	rst 38h			;3e1d	ff 	. 
	sbc a,(hl)			;3e1e	9e 	. 
	jp p,0f2f7h		;3e1f	f2 f7 f2 	. . . 
	inc de			;3e22	13 	. 
	sbc a,l			;3e23	9d 	. 
	sbc a,(hl)			;3e24	9e 	. 
	sbc a,l			;3e25	9d 	. 
	ei			;3e26	fb 	. 
	add a,c			;3e27	81 	. 
	ld h,0ffh		;3e28	26 ff 	& . 
	rst 38h			;3e2a	ff 	. 
	rst 38h			;3e2b	ff 	. 
	ld e,0fch		;3e2c	1e fc 	. . 
	rst 38h			;3e2e	ff 	. 
	rst 38h			;3e2f	ff 	. 
	rst 38h			;3e30	ff 	. 
	defb 0fdh,0ffh,09ah	;illegal sequence		;3e31	fd ff 9a 	. . . 
	cp 0ffh		;3e34	fe ff 	. . 
	add a,b			;3e36	80 	. 
	jr l3de1h		;3e37	18 a8 	. . 
	ld e,01eh		;3e39	1e 1e 	. . 
	rst 38h			;3e3b	ff 	. 
	pop af			;3e3c	f1 	. 
	xor d			;3e3d	aa 	. 
	ld e,h			;3e3e	5c 	\ 
	rst 38h			;3e3f	ff 	. 
	ld e,h			;3e40	5c 	\ 
	xor c			;3e41	a9 	. 
	adc a,e			;3e42	8b 	. 
	xor d			;3e43	aa 	. 
	adc a,e			;3e44	8b 	. 
	ld a,(hl)			;3e45	7e 	~ 
	ld a,l			;3e46	7d 	} 
	xor c			;3e47	a9 	. 
	rst 38h			;3e48	ff 	. 
	rst 38h			;3e49	ff 	. 
	rst 38h			;3e4a	ff 	. 
	ld hl,08689h		;3e4b	21 89 86 	! . . 
	adc a,c			;3e4e	89 	. 
	and (hl)			;3e4f	a6 	. 
	adc a,b			;3e50	88 	. 
	ld hl,0f288h		;3e51	21 88 f2 	! . . 
	add a,a			;3e54	87 	. 
	and (hl)			;3e55	a6 	. 
	add a,b			;3e56	80 	. 
	jp z,0f2fdh		;3e57	ca fd f2 	. . . 
	ld (de),a			;3e5a	12 	. 
	ld d,l			;3e5b	55 	U 
	ret			;3e5c	c9 	. 
	jp z,0f9c9h		;3e5d	ca c9 f9 	. . . 
	add hl,de			;3e60	19 	. 
	ld hl,0ffffh		;3e61	21 ff ff 	! . . 
	ld e,0fah		;3e64	1e fa 	. . 
	rst 38h			;3e66	ff 	. 
	rst 38h			;3e67	ff 	. 
	rst 38h			;3e68	ff 	. 
	di			;3e69	f3 	. 
	ld hl,00df4h		;3e6a	21 f4 0d 	! . . 
	adc a,d			;3e6d	8a 	. 
	ei			;3e6e	fb 	. 
	rst 38h			;3e6f	ff 	. 
	ld e,01eh		;3e70	1e 1e 	. . 
	rst 38h			;3e72	ff 	. 
	rst 38h			;3e73	ff 	. 
	rst 38h			;3e74	ff 	. 
	rst 38h			;3e75	ff 	. 
	rst 38h			;3e76	ff 	. 
	rst 38h			;3e77	ff 	. 
	rst 38h			;3e78	ff 	. 
	rst 38h			;3e79	ff 	. 
	rst 38h			;3e7a	ff 	. 
	rst 38h			;3e7b	ff 	. 
	rst 38h			;3e7c	ff 	. 
	rst 38h			;3e7d	ff 	. 
	pop af			;3e7e	f1 	. 
	rst 38h			;3e7f	ff 	. 
	ld sp,hl			;3e80	f9 	. 
	ld sp,hl			;3e81	f9 	. 
	call p,0f4f9h		;3e82	f4 f9 f4 	. . . 
	ld sp,hl			;3e85	f9 	. 
	call p,0f9ffh		;3e86	f4 ff f9 	. . . 
	jp m,0faf4h		;3e89	fa f4 fa 	. . . 
	rst 30h			;3e8c	f7 	. 
	ret m			;3e8d	f8 	. 
	ld sp,hl			;3e8e	f9 	. 
	ret m			;3e8f	f8 	. 
	ret m			;3e90	f8 	. 
	ret m			;3e91	f8 	. 
	rst 30h			;3e92	f7 	. 
	ret m			;3e93	f8 	. 
	ret m			;3e94	f8 	. 
	ret m			;3e95	f8 	. 
	ret m			;3e96	f8 	. 
	rst 38h			;3e97	ff 	. 
	rst 38h			;3e98	ff 	. 
	rst 38h			;3e99	ff 	. 
	ret m			;3e9a	f8 	. 
	rst 38h			;3e9b	ff 	. 
	rst 38h			;3e9c	ff 	. 
	rst 38h			;3e9d	ff 	. 
	cp 0feh		;3e9e	fe fe 	. . 
	ret m			;3ea0	f8 	. 
	cp 0feh		;3ea1	fe fe 	. . 
	cp 0feh		;3ea3	fe fe 	. . 
	cp 0feh		;3ea5	fe fe 	. . 
	jp m,0fff7h		;3ea7	fa f7 ff 	. . . 
	rst 38h			;3eaa	ff 	. 
	rst 38h			;3eab	ff 	. 
	call p,0fffeh		;3eac	f4 fe ff 	. . . 
	rst 38h			;3eaf	ff 	. 
	rst 38h			;3eb0	ff 	. 
	cp 0ffh		;3eb1	fe ff 	. . 
	rst 30h			;3eb3	f7 	. 
	cp 0ffh		;3eb4	fe ff 	. . 
	jp m,0f5f9h		;3eb6	fa f9 f5 	. . . 
	call p,0fff4h		;3eb9	f4 f4 ff 	. . . 
	rst 38h			;3ebc	ff 	. 
	push af			;3ebd	f5 	. 
	or 0ffh		;3ebe	f6 ff 	. . 
	or 0f5h		;3ec0	f6 f5 	. . 
	or 0f5h		;3ec2	f6 f5 	. . 
	or 0ffh		;3ec4	f6 ff 	. . 
	rst 38h			;3ec6	ff 	. 
	push af			;3ec7	f5 	. 
	rst 38h			;3ec8	ff 	. 
	rst 38h			;3ec9	ff 	. 
	rst 38h			;3eca	ff 	. 
	call p,0f5f5h		;3ecb	f4 f5 f5 	. . . 
	push af			;3ece	f5 	. 
	call p,0f4f5h		;3ecf	f4 f5 f4 	. . . 
	push af			;3ed2	f5 	. 
	call p,0f4f5h		;3ed3	f4 f5 f4 	. . . 
	rst 38h			;3ed6	ff 	. 
	defb 0fdh,0feh,0f4h	;illegal sequence		;3ed7	fd fe f4 	. . . 
	cp 0fdh		;3eda	fe fd 	. . 
	defb 0fdh,0fdh,0fdh	;illegal sequence		;3edc	fd fd fd 	. . . 
	cp 0f7h		;3edf	fe f7 	. . 
	call p,0ffffh		;3ee1	f4 ff ff 	. . . 
	call p,0fffeh		;3ee4	f4 fe ff 	. . . 
	rst 38h			;3ee7	ff 	. 
	rst 38h			;3ee8	ff 	. 
	cp 0f4h		;3ee9	fe f4 	. . 
	cp 0f7h		;3eeb	fe f7 	. . 
	push af			;3eed	f5 	. 
	ret m			;3eee	f8 	. 
	rst 38h			;3eef	ff 	. 
	call p,0fff4h		;3ef0	f4 f4 ff 	. . . 
	rst 38h			;3ef3	ff 	. 
	rst 38h			;3ef4	ff 	. 
	rst 38h			;3ef5	ff 	. 
	rst 38h			;3ef6	ff 	. 
	rst 38h			;3ef7	ff 	. 
	rst 38h			;3ef8	ff 	. 
	rst 38h			;3ef9	ff 	. 
	rst 38h			;3efa	ff 	. 
	rst 38h			;3efb	ff 	. 
	rst 38h			;3efc	ff 	. 
	rst 38h			;3efd	ff 	. 
	rst 38h			;3efe	ff 	. 
	rst 18h			;3eff	df 	. 
	rlca			;3f00	07 	. 
	defb 0ddh,0e7h,015h	;illegal sequence		;3f01	dd e7 15 	. . . 
	ld b,b			;3f04	40 	@ 
	ld a,(hl)			;3f05	7e 	~ 
	ld c,(hl)			;3f06	4e 	N 
	ld a,l			;3f07	7d 	} 
	rrca			;3f08	0f 	. 
	ret c			;3f09	d8 	. 
	rst 28h			;3f0a	ef 	. 
	djnz l3f1ch		;3f0b	10 0f 	. . 
	ret c			;3f0d	d8 	. 
	rst 28h			;3f0e	ef 	. 
	djnz l3f18h		;3f0f	10 07 	. . 
	defb 0ddh,0e7h,015h	;illegal sequence		;3f11	dd e7 15 	. . . 
	rlca			;3f14	07 	. 
	defb 0ddh,0e7h,015h	;illegal sequence		;3f15	dd e7 15 	. . . 
l3f18h:
	ld c,a			;3f18	4f 	O 
	djnz $+81		;3f19	10 4f 	. O 
	ret p			;3f1b	f0 	. 
l3f1ch:
	rst 28h			;3f1c	ef 	. 
	ld e,c			;3f1d	59 	Y 
	rrca			;3f1e	0f 	. 
	ret c			;3f1f	d8 	. 
	rst 28h			;3f20	ef 	. 
	djnz $+4		;3f21	10 02 	. . 
	defb 0ddh,0e2h,015h	;illegal sequence		;3f23	dd e2 15 	. . . 
	push bc			;3f26	c5 	. 
	cp 009h		;3f27	fe 09 	. . 
	defb 0fdh,007h,03fh	;illegal sequence		;3f29	fd 07 3f 	. . ? 
	ei			;3f2c	fb 	. 
	ret			;3f2d	c9 	. 
	defb 0fdh,0e6h,0f6h	;illegal sequence		;3f2e	fd e6 f6 	. . . 
	ret pe			;3f31	e8 	. 
	defb 0fdh,0c7h,0ffh	;illegal sequence		;3f32	fd c7 ff 	. . . 
	rst 38h			;3f35	ff 	. 
	ret m			;3f36	f8 	. 
	jp m,0fff4h		;3f37	fa f4 ff 	. . . 
l3f3ah:
	rst 38h			;3f3a	ff 	. 
	rst 38h			;3f3b	ff 	. 
	rst 18h			;3f3c	df 	. 
	rlca			;3f3d	07 	. 
	defb 0ddh,0e7h,015h	;illegal sequence		;3f3e	dd e7 15 	. . . 
	rrca			;3f41	0f 	. 
	ret c			;3f42	d8 	. 
	rst 28h			;3f43	ef 	. 
	djnz $+81		;3f44	10 4f 	. O 
	djnz l3f97h		;3f46	10 4f 	. O 
	ret p			;3f48	f0 	. 
l3f49h:
	rst 28h			;3f49	ef 	. 
	ld e,c			;3f4a	59 	Y 
l3f4bh:
	rrca			;3f4b	0f 	. 
	ret c			;3f4c	d8 	. 
l3f4dh:
	rst 28h			;3f4d	ef 	. 
	djnz l3f57h		;3f4e	10 07 	. . 
	defb 0ddh,0e7h,015h	;illegal sequence		;3f50	dd e7 15 	. . . 
	rlca			;3f53	07 	. 
	defb 0ddh,0e7h,015h	;illegal sequence		;3f54	dd e7 15 	. . . 
l3f57h:
	rrca			;3f57	0f 	. 
	ret c			;3f58	d8 	. 
	rst 28h			;3f59	ef 	. 
	djnz $+4		;3f5a	10 02 	. . 
	defb 0ddh,0e2h,015h	;illegal sequence		;3f5c	dd e2 15 	. . . 
	push bc			;3f5f	c5 	. 
	cp 03eh		;3f60	fe 3e 	. > 
	rlca			;3f62	07 	. 
	ccf			;3f63	3f 	? 
	ei			;3f64	fb 	. 
	ret			;3f65	c9 	. 
	defb 0fdh,0e7h,0feh	;illegal sequence		;3f66	fd e7 fe 	. . . 
	defb 0fdh,0c7h,0ffh	;illegal sequence		;3f69	fd c7 ff 	. . . 
	ret m			;3f6c	f8 	. 
	jp m,0f5c1h		;3f6d	fa c1 f5 	. . . 
	rst 38h			;3f70	ff 	. 
	rst 38h			;3f71	ff 	. 
	rst 38h			;3f72	ff 	. 
	rst 38h			;3f73	ff 	. 
	rst 38h			;3f74	ff 	. 
	rst 38h			;3f75	ff 	. 
	rst 38h			;3f76	ff 	. 
	rst 38h			;3f77	ff 	. 
	rst 38h			;3f78	ff 	. 
	rst 38h			;3f79	ff 	. 
	rst 38h			;3f7a	ff 	. 
	rst 38h			;3f7b	ff 	. 
l3f7ch:
	rst 38h			;3f7c	ff 	. 
	rst 38h			;3f7d	ff 	. 
	rst 18h			;3f7e	df 	. 
	scf			;3f7f	37 	7 
	jr nc,$-71		;3f80	30 b7 	0 . 
	or e			;3f82	b3 	. 
	scf			;3f83	37 	7 
l3f84h:
	or c			;3f84	b1 	. 
	scf			;3f85	37 	7 
	push af			;3f86	f5 	. 
	scf			;3f87	37 	7 
l3f88h:
	jr nc,l3f49h		;3f88	30 bf 	0 . 
	cp e			;3f8a	bb 	. 
	ccf			;3f8b	3f 	? 
	jr c,l3f4dh		;3f8c	38 bf 	8 . 
	cp e			;3f8e	bb 	. 
	ccf			;3f8f	3f 	? 
l3f90h:
	jr c,$-63		;3f90	38 bf 	8 . 
	cp e			;3f92	bb 	. 
	ccf			;3f93	3f 	? 
l3f94h:
	jr c,$-63		;3f94	38 bf 	8 . 
	cp e			;3f96	bb 	. 
l3f97h:
	ccf			;3f97	3f 	? 
	add hl,sp			;3f98	39 	9 
	cp h			;3f99	bc 	. 
	rst 38h			;3f9a	ff 	. 
	rst 38h			;3f9b	ff 	. 
	rst 30h			;3f9c	f7 	. 
	daa			;3f9d	27 	' 
	jr nc,l3f57h		;3f9e	30 b7 	0 . 
	or e			;3fa0	b3 	. 
	scf			;3fa1	37 	7 
	jr nz,l3f4bh		;3fa2	20 a7 	  . 
	and e			;3fa4	a3 	. 
	scf			;3fa5	37 	7 
	or e			;3fa6	b3 	. 
	scf			;3fa7	37 	7 
	call po,0e3e7h		;3fa8	e4 e7 e3 	. . . 
	scf			;3fab	37 	7 
	or a			;3fac	b7 	. 
	rst 30h			;3fad	f7 	. 
	rst 20h			;3fae	e7 	. 
	rst 20h			;3faf	e7 	. 
	scf			;3fb0	37 	7 
	rst 30h			;3fb1	f7 	. 
	daa			;3fb2	27 	' 
	and e			;3fb3	a3 	. 
	rst 30h			;3fb4	f7 	. 
	scf			;3fb5	37 	7 
	daa			;3fb6	27 	' 
	daa			;3fb7	27 	' 
	scf			;3fb8	37 	7 
	scf			;3fb9	37 	7 
	rst 20h			;3fba	e7 	. 
sub_3fbbh:
	jp sub_3037h		;3fbb	c3 37 30 	. 7 0 
	rst 20h			;3fbe	e7 	. 
	and e			;3fbf	a3 	. 
	scf			;3fc0	37 	7 
	jr nc,$-87		;3fc1	30 a7 	0 . 
	and e			;3fc3	a3 	. 
	scf			;3fc4	37 	7 
	ld sp,0e7a4h		;3fc5	31 a4 e7 	1 . . 
	rst 30h			;3fc8	f7 	. 
	rst 30h			;3fc9	f7 	. 
	daa			;3fca	27 	' 
	jr nz,l3f84h		;3fcb	20 b7 	  . 
	or e			;3fcd	b3 	. 
	daa			;3fce	27 	' 
	jr nc,l3f88h		;3fcf	30 b7 	0 . 
	and e			;3fd1	a3 	. 
	scf			;3fd2	37 	7 
	jr nc,l3f7ch		;3fd3	30 a7 	0 . 
	or e			;3fd5	b3 	. 
	scf			;3fd6	37 	7 
	jr nz,l3f90h		;3fd7	20 b7 	  . 
	or e			;3fd9	b3 	. 
	daa			;3fda	27 	' 
	jr nc,l3f94h		;3fdb	30 b7 	0 . 
	and e			;3fdd	a3 	. 
	scf			;3fde	37 	7 
	or e			;3fdf	b3 	. 
	scf			;3fe0	37 	7 
	call p,sub_37f3h		;3fe1	f4 f3 37 	. . 7 
	or a			;3fe4	b7 	. 
	rst 30h			;3fe5	f7 	. 
	rst 30h			;3fe6	f7 	. 
	rst 30h			;3fe7	f7 	. 
	scf			;3fe8	37 	7 
	scf			;3fe9	37 	7 
	cp e			;3fea	bb 	. 
	ccf			;3feb	3f 	? 
	ccf			;3fec	3f 	? 
	ccf			;3fed	3f 	? 
	rst 38h			;3fee	ff 	. 
	ccf			;3fef	3f 	? 
	ccf			;3ff0	3f 	? 
	rst 38h			;3ff1	ff 	. 
	ei			;3ff2	fb 	. 
	rst 38h			;3ff3	ff 	. 
	rst 38h			;3ff4	ff 	. 
	rst 38h			;3ff5	ff 	. 
	rst 38h			;3ff6	ff 	. 
	rst 38h			;3ff7	ff 	. 
	rst 38h			;3ff8	ff 	. 
	rst 38h			;3ff9	ff 	. 
	rst 38h			;3ffa	ff 	. 
l3ffbh:
	rst 38h			;3ffb	ff 	. 
	rst 38h			;3ffc	ff 	. 
	rst 10h			;3ffd	d7 	. 
l3ffeh:
	ld d,a			;3ffe	57 	W 
l3fffh:
	nop			;3fff	00 	. 
