**********************************************************************
BUCKWALTER ARABIC MORPHOLOGICAL ANALYZER VERSION 2.0
Portions (c) 2002-2004 QAMUS LLC (www.qamus.org),
(c) 2002-2004 Trustees of the University of Pennsylvania
**********************************************************************

LDC USER AGREEMENT

Use of this version of the Buckwalter Arabic Morphological Analyzer Version 2
distributed by the Linguistic Data Consortium (LDC) of the University of 
Pennsylvania is governed by the following terms: 

This User Agreement is provided by the Linguistic Data Consortium as a 
condition of accepting the databases named or described herein. 

This Agreement describes the terms between User/User's Research Group and 
Linguistic Data Consortium (LDC), in which User will receive material, as 
specified below, from LDC. The terms of this Agreement supercede the terms of 
any previous Membership Agreement in regard to the Buckwalter Arabic 
Morphological Analyzer Version 2.

Under this agreement User will receive one or more CD-ROM discs, DVDs, 
electronic files or other media as appropriate, containing linguistic tools, 
speech, video, and/or text data. User agrees to use the material received 
under this agreement only for non-commercial linguistic education and research
purposes. Unless explicitly permitted herein, User shall have no right to 
copy, redistribute, transmit, publish or otherwise use the LDC Databases for 
any other purpose and User further agrees not to disclose, copy, or 
re-distribute the material to others outside of User's research group. 

Government use, including any use within or among government organizations and
use by government contractors to produce or evaluate resources and 
technologies for government use, is permitted under this license.

Organizations interested in licensing the Buckwalter Arabic Morphological 
Analyzer Version 2 for commercial use should contact: 

   QAMUS LLC 
   448 South 48th St. 
   Philadelphia, PA 19143 
   ATTN: Tim Buckwalter 
   email: license@qamus.org

Except for Government use as specified above, commercial uses of this corpus 
include, but are not limited to, imbedded use of the Analyzer, Analyzer 
methods, Analyzer derived works, Analyzer output data, algorithms, lexicons, 
and downloaded data in a commercial product or a fee for service project; 
use of the Analyzer, Analyzer methods, Analyzer derived works, Analyzer 
output data, algorithms, and downloaded data to create or develop a 
commercial product or perform a fee for service project; use of Analyzer, 
Analyzer methods, Analyzer derived works, Analyzer output data, algorithms, 
lexicons, and downloaded data as a development tool to measure performance of
a commercial product or work product developed on a fee for service basis; 
redistribution of Analyzer, Analyzer methods, Analyzer derived works, Analyzer 
output data, algorithms, lexicons and downloaded data to any third party for 
imbedding in a commercial product or fee for service project, for deriving a 
commercial product or fee for service project, or for measuring the 
performance of a commercial product or fee for service project.

USER ACKNOWLEDGES AND AGREES THAT "CORPORA RECEIVED" ARE PROVIDED ON AN "AS-IS"
BASIS AND THAT LDC, ITS HOST INSTITUTION THE UNIVERSITY OF PENNSYLVANIA, AND 
ITS DATA PROVIDERS AND CORPUS AUTHORS MAKE NO REPRESENTATIONS OR WARRANTIES OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR CONFORMITY WITH 
WHATEVER DOCUMENTATION IS PROVIDED. IN NO EVENT SHALL LDC, ITS HOST 
INSTITUTION, DATA PROVIDORS OR CORPUS AUTHORS BE LIABLE FOR SPECIAL, DIRECT, 
INDIRECT, CONSEQUENTIAL, PUNITIVE, INCIDENTAL OR OTHER DAMAGES, LOSSES, COSTS, 
CHARGES, CLAIMS, DEMANDS, FEES OR EXPENSES OF ANY NATURE OR KIND ARISING IN ANY
WAY FROM THE FURNISHING OF OR USER'S USE OF THE CORPORA RECEIVED. 

**********************************************************************
README
**********************************************************************

This document describes the components of the Buckwalter Arabic Morphological Analyzer Version 2.0, including the morphology analysis algorithm and the structure and content of the output data it generates.

Files included with this document:

* Three lexicon files: dictPrefixes, dictStems, and dictSuffixes.
* Three compatibility tables: tableAB, tableAC, and tableBC.
* Perl code (AraMorph.pl) that makes use of the three lexicon files and three compatibility tables in order to perform morphological analysis and POS-tagging of Arabic words.
* Sample Arabic input file (infile.txt) in Windows 1256 encoding.
* Sample morphology analysis output file (outfile.xml) in Unicode UTF-8 encoding.
* Documentation (this readme.txt file).


**********************************************************************
CONTENTS
**********************************************************************
1. Description of the three lexicon files
2. Description of the three compatibility tables
3. Description of the morphology analysis algorithm
4. Miscellaneous observations
5. Main differences between versions 1.0 and 2.0
6. Acknowledgements
Appendix: Buckwalter transliteration


**********************************************************************
1. DESCRIPTION OF THE THREE LEXICON FILES
**********************************************************************

Each entry in the three lexicon files consists of four tab-delimited fields:
(1) the entry (prefix, stem, or suffix) WITHOUT short vowels and diacritics
(2) the entry (prefix, stem, or suffix) WITH    short vowels and diacritics
(3) its morphological category (for controlling the compatibility of prefixes, stems, and suffixes)
(4) its English gloss(es), including selective POS data within XML tags <pos>...</pos>

Only fields 1 and 3 are required for morphological analysis proper. Fields 2 and 4 provide additional information once the morphology analysis proper has concluded.

Arabic script data in the lexicons is provided in the Buckwalter transliteration scheme (See below: "BUCKWALTER TRANSLITERATION"). The Perl code implementation accepts input in Arabic Windows encoding (cp1256). 


The following is a description of the three lexicon files:

"dictPrefixes" contains all Arabic prefixes and their concatenations. Sample entries:

w	wa	Pref-Wa	and <pos>wa/CONJ</pos>
f	fa	Pref-Wa	and;so <pos>fa/CONJ</pos>
b	bi	NPref-Bi	by;with <pos>bi/PREP</pos>
k	ka	NPref-Bi	like;such as <pos>ka/PREP</pos>
wb	wabi	NPref-Bi	and + by/with <pos>wa/CONJ+bi/PREP</pos>
fb	fabi	NPref-Bi	and + by/with <pos>fa/CONJ+bi/PREP</pos>
wk	waka	NPref-Bi	and + like/such as <pos>wa/CONJ+ka/PREP</pos>
fk	faka	NPref-Bi	and + like/such as <pos>fa/CONJ+ka/PREP</pos>
Al	Al	NPref-Al	the <pos>Al/DET</pos>
wAl	waAl	NPref-Al	and + the        <pos>wa/CONJ+Al/DET+</pos>
fAl	faAl	NPref-Al	and/so + the     <pos>fa/CONJ+Al/DET+</pos>
bAl	biAl	NPref-BiAl	with/by + the                     <pos>bi/PREP+Al/DET+</pos>
kAl	kaAl	NPref-BiAl	like/such as + the                <pos>ka/PREP+Al/DET+</pos>
wbAl	wabiAl	NPref-BiAl	and + with/by the         <pos>wa/CONJ+bi/PREP+Al/DET+</pos>
fbAl	fabiAl	NPref-BiAl	and/so + with/by + the    <pos>fa/CONJ+bi/PREP+Al/DET+</pos>
wkAl	wakaAl	NPref-BiAl	and + like/such as + the  <pos>wa/CONJ+ka/PREP+Al/DET+</pos>
fkAl	fakaAl	NPref-BiAl	and + like/such as + the  <pos>fa/CONJ+ka/PREP+Al/DET+</pos>


"dictSuffixes" contains all Arabic suffixes and their concatenations. Sample entries:

p	ap	NSuff-ap	[fem.sg.]                     <pos>ap/NSUFF_FEM_SG</pos>
ty	atayo	NSuff-tay	two [acc.]                    <pos>atayo/NSUFF_FEM_DU_ACC_POSS</pos>
tyh	atayohi	NSuff-tay	two [acc.] + his/its          <pos>atayo/NSUFF_FEM_DU_ACC_POSS+hi/POSS_PRON_3MS</pos>
tyhmA	atayohimA	NSuff-tay	two [acc.] + their            <pos>atayo/NSUFF_FEM_DU_ACC_POSS+himA/POSS_PRON_3D</pos>
tyhm	atayohim	NSuff-tay	two [acc.] + their            <pos>atayo/NSUFF_FEM_DU_ACC_POSS+him/POSS_PRON_3MP</pos>
tyhA	atayohA	NSuff-tay	two [acc.] + its/their/her    <pos>atayo/NSUFF_FEM_DU_ACC_POSS+hA/POSS_PRON_3FS</pos>
tyhn	atayohin~a	NSuff-tay	two [acc.] + their            <pos>atayo/NSUFF_FEM_DU_ACC_POSS+hin~a/POSS_PRON_3FP</pos>
tyk	atayoka	NSuff-tay	two [acc.] + your [masc.sg.]  <pos>atayo/NSUFF_FEM_DU_ACC_POSS+ka/POSS_PRON_2MS</pos>
tyk	atayoki	NSuff-tay	two [acc.] + your [fem.sg.]   <pos>atayo/NSUFF_FEM_DU_ACC_POSS+ki/POSS_PRON_2FS</pos>
tykmA	atayokumA	NSuff-tay	two [acc.] + your [du.]       <pos>atayo/NSUFF_FEM_DU_ACC_POSS+kumA/POSS_PRON_2D</pos>
tykm	atayokum	NSuff-tay	two [acc.] + your [masc.pl.]  <pos>atayo/NSUFF_FEM_DU_ACC_POSS+kum/POSS_PRON_2MP</pos>
tykn	atayokun~a	NSuff-tay	two [acc.] + your [fem.pl.]   <pos>atayo/NSUFF_FEM_DU_ACC_POSS+kun~a/POSS_PRON_2FP</pos>
ty	atay~a	NSuff-tay	two [acc.] + my               <pos>atayo/NSUFF_FEM_DU_ACC_POSS+ya/POSS_PRON_1S</pos>
tynA	atayonA	NSuff-tay	two [acc.] + our              <pos>atayo/NSUFF_FEM_DU_ACC_POSS+nA/POSS_PRON_1P</pos>


"dictStems" contains all Arabic stems. Sample entries:

;--- ktb
;; katab-u_1
ktb	katab	PV	write
ktb	kotub	IV	write
ktb	kutib	PV_Pass	be written;be fated;be destined
ktb	kotab	IV_Pass_yu	be written;be fated;be destined
;; kAtab_1
kAtb	kAtab	PV	correspond with
kAtb	kAtib	IV_yu	correspond with
;; >akotab_1
>ktb	>akotab	PV	dictate;make write
ktb	kotib	IV_yu	dictate;make write
ktb	kotab	IV_Pass_yu	be dictated
;; kitAb_1
ktAb	kitAb	Ndu	book
ktb	kutub	N	books
;; kitAboxAnap_1
ktAbxAn	kitAboxAn	NapAt	library;bookstore
ktbxAn	kutuboxAn	NapAt	library;bookstore
;; kutubiy~_1
ktby	kutubiy~	Ndu	book-related
;; kutubiy~_2
ktby	kutubiy~	Ndu	bookseller
ktby	kutubiy~	Nap	booksellers
;; kut~Ab_1
ktAb	kut~Ab	N	kuttab (village school);Quran school
ktAtyb	katAtiyb	Ndip	kuttab (village schools);Quran schools
;; kutay~ib_1
ktyb	kutay~ib	NduAt	booklet
;; kitAbap_1
ktAb	kitAb	Nap	writing
;; kitAbap_2
ktAb	kitAb	Napdu	essay;piece of writing
ktAb	kitAb	NAt	writings;essays
;; kitAbiy~_1
ktAby	kitAbiy~	N-ap	writing;written     <pos>kitAbiy~/ADJ</pos>
;; katiybap_1
ktyb	katiyb	Napdu	brigade;squadron;corps
ktA}b	katA}ib	Ndip	brigades;squadrons;corps
ktA}b	katA}ib	Ndip	Phalangists
;; katA}ibiy~_1
ktA}by	katA}ibiy~	Nall	brigade;corps
ktA}by	katA}ibiy~	Nall	brigade;corps     <pos>katA}ibiy~/ADJ</pos>
;; katA}ibiy~_2
ktA}by	katA}ibiy~	Nall	Phalangist
ktA}by	katA}ibiy~	Nall	Phalangist     <pos>katA}ibiy~/ADJ</pos>
;; makotab_1
mktb	makotab	Ndu	bureau;office;department
mkAtb	makAtib	Ndip	bureaus;offices
;; makotabiy~_1
mktby	makotabiy~	N-ap	office     <pos>makotabiy~/ADJ</pos>
;; makotabap_1
mktb	makotab	NapAt	library;bookstore
mkAtb	makAtib	Ndip	libraries;bookstores



The POS information of each entry is made explicit for all entries only in the lexicons of Prefixes and Suffixes. The POS information for each entry in the lexicon of Stems is assigned when the lexicon is read into memory, on the basis of each entry's morphological category. Here is the actual code for that:

   if     ($cat  =~ m/^(Pref-0|Suff-0)$/) {$POS = ""} 
   elsif  ($cat  =~ m/^F/)          {$POS = "$voc/FUNC_WORD"}
   elsif  ($cat  =~ m/^IV.*?_Pass/) {$POS = "$voc/IV_PASS"}
   elsif  ($cat  =~ m/^IV/)         {$POS = "$voc/IV"}
   elsif  ($cat  =~ m/^PV.*?_Pass/) {$POS = "$voc/PV_PASS"}
   elsif  ($cat  =~ m/^PV/)         {$POS = "$voc/PV"}
   elsif  ($cat  =~ m/^CV/)         {$POS = "$voc/CV"}
   elsif (($cat  =~ m/^N/)
     and ($gloss =~ m/^[A-Z]/))     {$POS = "$voc/NOUN_PROP"}
   elsif (($cat  =~ m/^N/)
     and  ($voc  =~ m/iy~$/))       {$POS = "$voc/NOUN"}
   elsif  ($cat  =~ m/^N/)          {$POS = "$voc/NOUN"}
   else                             { die "no POS can be deduced in $filename (line $.)" }

Explicit POS information is needed in the lexicon of Stems in cases where the above algorithm would produce an incorrect or vague POS assignment. Typically this applies to Function Words that are assigned tags such as PREP, ADV, CONJ, INTERJ, DEM_PRON, and NEG_PART, instead of the vague POS tag FUNC_WORD.

A 6th field of information is the unique Lemma ID, currently stored in the lexicon of Stems as a quasi-comment line (with two semicolons):

;; katab-u_1
;; kAtab_1
;; >akotab_1
;; kitAb_1
;; kitAboxAnap_1
;; kutubiy~_1
;; kutubiy~_2
;; kut~Ab_1
;; kutay~ib_1
;; kitAbap_1
;; kitAbap_2
;; kitAbiy~_1
;; katiybap_1
;; katA}ibiy~_1
;; katA}ibiy~_2
;; makotab_1
;; makotabiy~_1
;; makotabap_1


When the lexicon is loaded into memory we extract the lemma ID and lexicon entries as follows:

   if (m/^;; /)  {  
      $lemmaID = $';  # lemma ID line
   }
   elsif (m/^;/) {
      # comment line
   }
   else {
      ($entry,$voc,$cat,$glossPOS) = split (/\t/, $_); # entry line
   }


We subsequently split the English gloss and POS information ($glossPOS) into separate $gloss and $POS data fields. When the lexicon is read into memory the gloss and POS and lemma ID information are stored as the 4th, 5th and 6th fields, respectively, as seen in the following line of code:

   push ( @{ $temp_hash{$entry} }, "$entry\t$voc\t$cat\t$gloss\t$POS\t$lemmaID") ; 



**********************************************************************
2. DESCRIPTION OF THE THREE COMPATIBILITY TABLES
**********************************************************************

Each of the three compatibility tables lists pairs of compatible morphological categories:

Compatibility table "tableAB" lists compatible Prefix and Stem morphological categories, such as:

  NPref-Al N
  NPref-Al N-ap
  NPref-Al N-ap_L
  NPref-Al N/At
  NPref-Al N/At_L
  NPref-Al N/ap
  NPref-Al N/ap_L

Compatibility table "tableAC" lists compatible Prefix and Suffix morphological categories, such as:

  NPref-Al Suff-0
  NPref-Al NSuff-u
  NPref-Al NSuff-a
  NPref-Al NSuff-i
  NPref-Al NSuff-An
  NPref-Al NSuff-ayn

Compatibility table "tableBC" lists compatible Stem and Suffix morphological categories, such as:

  PV PVSuff-a
  PV PVSuff-ah
  PV PVSuff-A
  PV PVSuff-Ah
  PV PVSuff-at
  PV PVSuff-ath

In the above examples, Prefix category "NPref-Al" is listed as being compatible with Stem categories "N", "N-ap", and "N-ap_L", and Suffix categories "Suff-0", "NSuff-u", etc. Morphological category pairs that are not listed in the compatibility tables (e.g. "NPref-Al PVSuff-a") are simply incompatible.


**********************************************************************
3. DESCRIPTION OF THE MORPHOLOGY ANALYSIS ALGORITHM
**********************************************************************

The algorithm performs the following functions:
 - tokenization
 - word segmentation
 - dictionary lookup
 - compatibility check
 - analysis report
 - orthographic variants

------------
TOKENIZATION
------------

In order to function with ordinary Arabic text the current algorithm performs some very basic tokenization. Arabic words are defined as one or more contiguous Arabic characters. Non-Arabic strings are split on white space. In version 1.0 these non-Arabic strings were simply labeled "Non-Alphabetic Data" and left untagged. In version 2.0 non-Arabic strings are tagged appropriately as LATIN, PUNC, or NUM.

Ideally, tokenization should take place prior to morphology analysis proper, primarily because we believe that the nature of Arabic orthography calls for a statistical analysis of the entire input text in order to determine the best tokenization strategy. The analysis should identify and deal with potential problems such as:

 1. use of the letter ra' (U+0631) is as numeric comma
 2. use of the Arabic-Indic digit zero (U+0660) as punctuation
 3. confusion of word-final ya' (U+064A) and alif maqsura (U+0649)
 4. confusion of word-final ha' (U+0647) and ta' marbuta (U+0629)
 5. run-on words (e.g.: Ezwjl, fqdtm, mAHdv, AldArAlbyDa')

For a more detailed discussion of this problem, see the following publication:

   * Tim Buckwalter. "Issues in Arabic Orthography and Morphology Analysis," in Proceedings of the Workshop on Computational Approaches to Arabic Script-based Languages, COLING 2004, Geneva, August 28, 2004. http://www.ldc.upenn.edu/Papers/COLING2004/Buckwalter_Arabic-orthography-morphology.pdf


-----------------
WORD SEGMENTATION
-----------------

Arabic words are segmented into prefix, stem and suffix strings according to the following rules:

  - the prefix can be 0 to 4 characters long
  - the stem can be 1 to infinite characters long
  - the suffix can be 0 to 6 characters long

Given these rules, the input word is segmented into a finite number of 3-part segments: prefix, stem, and suffix. For example, the following are the possible segmentation of the world "wAlgAz":

	wAlgAz
	wAlgA	z
	wAlg	Az
	wAl	gAz
	wA	lgAz
	w	AlgAz
w	AlgAz
w	AlgA	z
w	Alg	Az
w	Al	gAz
w	A	lgAz
wA	lgAz
wA	lgA	z
wA	lg	Az
wA	l	gAz
wAl	gAz
wAl	gA	z
wAl	g	Az
wAlg	Az
wAlg	A	z


-----------------
DICTIONARY LOOKUP
-----------------

Dictionary lookup consists of asking, for each segmentation:

  does the prefix exist? (in the hash table of prefixes)
  does the stem exist? (in the hash table of stems)
  does the suffix exist? (in the hash table of suffixes)

If all three components (prefix, stem, suffix) are found in their respective hash tables, the next step is to determine whether their respective morphological categories are compatible.


-------------------
COMPATIBILITY CHECK
-------------------

For each of the three components (prefix, stem, suffix) the compatibily check asks:

  is prefix category A compatible with the stem category B? (does the pair exist in hash table AB?)
  is prefix category A compatible with suffix category B? (does the pair exist in hash table AC?)
  is stem category B compatible with suffix category C? (does the pair exist in hash table BC?)

If all three pairs are found in their respective tables, the three components are compatible and the word is valid.


---------------
ANALYSIS REPORT
---------------

The output of version 2.0 is in XML format and UTF-8 encoding (see sample "outfile.xml"). The structure is as follows:

<AraMorph_output ...>                        <--- the root element and timestamp

<token_Arabic>»«·„»«œÏ¡                      <--- the input string, unmodified
  <variant>bAlmbAdY'                         <--- the first orthographic variant (same as input string, unmodified)
    <x_solution>                             <--- stem is not found, hence "X Solution" (discussed below)
      <voc>bAlmbAdY'</voc>
      <pos>bAlmbAdY'/NOUN_PROP</pos>
      <gloss>NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>                             <--- prefix "bi-" is found, hence second "X Solution"
      <voc>biAlmbAdY'</voc>
      <pos>bi/PREP+AlmbAdY'/NOUN_PROP</pos>
      <gloss>by/with + NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>                             <--- prefix "biAl-" is found, hence third "X Solution"
      <voc>biAlmbAdY'</voc>
      <pos>bi/PREP+Al/DET+mbAdY'/NOUN_PROP</pos>
      <gloss>with/by + the + NOT_IN_LEXICON</gloss>
    </x_solution>
  </variant>
  <variant>bAlmbAd}                          <--- the second orthographic variant (modifed input string)
    <solution>
      <lemmaID>maboda&gt;_1</lemmaID>
      <voc>biAlmabAdi}</voc>                 <--- vocalization of input string 
      <pos>bi/PREP+Al/DET+mabAdi}/NOUN</pos>
      <gloss>with/by + the + principles/bases</gloss>
    </solution>
    <solution>
      <lemmaID>maboda&gt;_1</lemmaID>
      <voc>biAlmabAdi}i</voc>
      <pos>bi/PREP+Al/DET+mabAdi}/NOUN+i/CASE_DEF_GEN</pos>
      <gloss>with/by + the + principles/bases + [def.gen.]</gloss>
    </solution>
    <x_solution>
      <voc>bAlmbAd}</voc>
      <pos>bAlmbAd}/NOUN_PROP</pos>
      <gloss>NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>biAlmbAd}</voc>
      <pos>bi/PREP+AlmbAd}/NOUN_PROP</pos>
      <gloss>by/with + NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>biAlmbAd}</voc>
      <pos>bi/PREP+Al/DET+mbAd}/NOUN_PROP</pos>
      <gloss>with/by + the + NOT_IN_LEXICON</gloss>
    </x_solution>
  </variant>
  <variant>bAlmbAdy'                         <--- the third orthographic variant (modifed input string)
    <x_solution>
      <voc>bAlmbAdy'</voc>
      <pos>bAlmbAdy'/NOUN_PROP</pos>
      <gloss>NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>biAlmbAdy'</voc>
      <pos>bi/PREP+AlmbAdy'/NOUN_PROP</pos>
      <gloss>by/with + NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>biAlmbAdy'</voc>
      <pos>bi/PREP+Al/DET+mbAdy'/NOUN_PROP</pos>
      <gloss>with/by + the + NOT_IN_LEXICON</gloss>
    </x_solution>
  </variant>
</token_Arabic>
</AraMorph_output>


---------------------
ORTHOGRAPHIC VARIANTS
---------------------

Words that contain certain characters, especially at the end of the word, are possible orthographic variants or non-canonical spellings. In version 1.0 when a word returned "not found" we checked for the presence of specific letters in the input string and then performed a second lookup using one or more alternate spellings of the input string. In version 2.0 we generate all possible spellings of the input string regardless of whether each lookup suceeds or returns "not found." In version 1.0 the input word "Ely" was analyzed as the proper noun "Ali", even in cases where the context clearly showed that it was a typo for the preposition "ElY". In version 2.0, however, the input strings "Ely" and "ElY" now return identical analyses (the proper name "Ali" and the preposition "`ala"), although in different order.



**********************************************************************
4. MISCELLANEOUS OBSERVATIONS
**********************************************************************

Topics discussed below:
 - orthographic anomalies
 - short vowels and diacritics
 - noun case endings and verb mood endings

----------------------
ORTHOGRAPHIC ANOMALIES
----------------------

The Buckwalter Arabic Morphological Analyzer is being used for POS-tagging a considerable amount of text data at the LDC, and various orthographic anomalies have been observed during the manual annotation process. Most of these anomalies are handled successfully by generating and looking up all valid orthographic variants of the input string. Certain anomalies have been re-classified in light of new research. A case in point is the "qAl >n" (qala 'anna) problem, which was previously treated as a typographic mistake for "qAl <n" (qala 'inna). Today, however, free variation of both forms is accepted, at least in newsire text.

Version 1.0 handled the issue of missing stem-initial hamza above/below alif and missing madda above alif by listing both forms in the lexicon of stems:

  |b	|b	Nprop	August
  Ab	|b	Nprop	August
  >b	>ab~	PV_V	desire;aspire
  Ab	>ab~	PV_V	desire;aspire

In version 2.0 the bare-alif form has been removed from the lexicon and is now generated automatically:

         if ( $temp_entry =~ s/^[>|<{]/A/ ) { # stem begins with hamza
            push ( @entry_forms, $temp_entry ); 
         }

The spelling of stem-medial and stem-final hamza on alif as a bare alif is not standard orthography and is largely avoided because it results in ambiguity. For example, note the pairs bd>/bdA and s>l/sAl. The spelling "tAkyd" (for "t>kyd"), however, was found to be frequent, probably because omission of the hamza does not result in the valid spelling of a different word. In order to deal with this problem, in version 1.0 we made additional entries in the stem lexicon and labeled them (in comment lines) with "AFP missing hamza". Examples:

   ;; {isota>ojar_1
   <st>jr	{isota>ojar	PV	hire;rent
   Ast>jr	{isota>ojar	PV	hire;rent
   ; AFP missing hamza
   AstAjr	{isota>ojar	PV	hire;rent
   st>jr	sota>ojir	IV	hire;rent

This, however, is a problem that cannot be solved by making additional entries indefinitely. In preparing version 2.0 we experimented briefly with a solution that involved generating these variants automatically when loading the lexicon into memory, but this resulted in serious over-generation of implausible solutions (e.g., k>n = kAn). We are currently investigating alternate solutions.


---------------------------
SHORT VOWELS AND DIACRITICS
---------------------------

In version 1.0 all short vowels and diacritics were stripped out of the input string and played no part in the analysis. This holds true with version 2.0 but with one exception: we retain the fatHatan in the unique word-final combination of alif-fatHatan (also spelled fatHatan-alif). The automatic removal of the fatHatan from the alif chair often resulted in the unlikely analysis of the alif as a marker for the dual. This no longer occurs in version 2.0.

It has been suggested that if short vowels and diacritics are present in the input string they could be used in pattern-matching with the vocalized string of the entry, and thus unlikely solutions could be eliminated. For example, if the input string is "EumAn" then why display the solutions "Eam~An" and "Eam~+Ani"? This question assumes that all uses of short vowels and diacritics are reliable, and we suspect that this is true perhaps 95% of the time (we are not aware of any studies on this important issue). We currently achieve more robust analyses by eliminating all short vowels and diacritics than by trusting their accuracy and using them to eliminate unlikely solutions. We have noticed that the short vowels and diacritics are often wrong, and this is usually because short vowels and diacritics are zero-width glyphs that can be stacked on each other ad infinitum with only the last one remaining visible. Note the relatively high Google frequencies of typographical errors such as ">yDAFF" (268), ">yDAaF" (200), and ">yDAuF" (25). These typos are analyzed correctly in version 2.0 because we remove all short vowels and diacritics but preserve any remaining -AF combination. (We have placed these typo strings in the sample "infile.txt").


---------------------------------------
NOUN CASE ENDINGS AND VERB MOOD ENDINGS
---------------------------------------

Prior to the release of version 1.0 (Nov. 2002) we implemented the case ending system (the short vowels and nunation) for nouns. We made the necessary short-vowel case ending entries in "dictSuffixes" and the appropriate entries in the compatibility tables to account for them, but after the feature was implemented, a decision was taken to disable it, so the entries in "dictSuffixes" were all commented out, although the entries in the compatibility tables were left intact. In version 2.0 we have re-implements the case endings for nouns, and extended that implementation to the mood markers of the imperfect verb (the short vowels used for marking the indicative, subjunctive and jussive moods):

<token_Arabic>Ìﬂ »
  <variant>yktb
    <solution>
      <lemmaID>katab-u_1</lemmaID>
      <voc>yakotubu</voc>
      <pos>ya/IV3MS+kotub/IV+u/IVSUFF_MOOD:I</pos>
      <gloss>he/it + write + [ind.]</gloss>
    </solution>
    <solution>
      <lemmaID>katab-u_1</lemmaID>
      <voc>yakotuba</voc>
      <pos>ya/IV3MS+kotub/IV+a/IVSUFF_MOOD:S</pos>
      <gloss>he/it + write + [sub.]</gloss>
    </solution>
    <solution>
      <lemmaID>katab-u_1</lemmaID>
      <voc>yakotubo</voc>
      <pos>ya/IV3MS+kotub/IV+o/IVSUFF_MOOD:J</pos>
      <gloss>he/it + write + [jus.]</gloss>
    </solution>
      ...
      ...
  </variant>
</token_Arabic>



**********************************************************************
5. MAIN DIFFERENCES BETWEEN VERSIONS 1.0 AND 2.0
**********************************************************************

(1) Alignment with the morphology annotation data in Arabic Tree Bank Part 3 (the Annahar corpus). 

Whereas version 1.0 (released Nov. 2002) represents a stage of development somewhere between the Penn Arabic Treebank Part 1 (the AFP corpus) and the Penn Arabic Treebank Part 2 (the Ummah corpus), version 2.0 is the version that was used for morphological annotation and POS tagging of the Penn Arabic Tree Bank Part 3 (the Annahar corpus). Here are links to published Penn Arabic Treebanks:

   Arabic Treebank: Part 1 v 2.0 http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2003T06
   Arabic Treebank: Part 2 v 2.0 http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2004T02
   Arabic Treebank: Part 3 v 1.0 http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2004T11


(2) Output in XML format and UTF-8 encoding.

Version 2.0 requires use of the Encode module and Perl 5.8. The code for generating the XML output is quite inelegant but it works. In the future we would like to do it right, by storing the analysis data for each input token in the proper data structure and then generating the XML output with a single print command. The output XML files are quite large now and this could be a problem. We typically test the lexicon coverage and parser performance by feeding it the top 50,000 most frequent word of the day, which results in a 100MB+ output file. One solution to the size problem might be to consider a different XML data structure that eliminates much of the redundancy found in the present structure, where many analyses are identical except for the various case endings.


(3) The main lexicon (dictStems) in version 2.0 has 40,219 lemmas (vs. 38,600 in version 1.0).

Most new entries are proper names, especially foreign names. Whereas the Analyzer registered 90% accuracy in the analysis of the AFP corpus, it registered 99.24% and 99.25% with the Ummah and Annahar corpora, respectively.


(4) More detailed POS tagset, especially for function words.

The vague FUNC_WORD (function word) tag was replaced in version 2.0 with more precise tags, such as VERB_PART (e.g., qad laqad) and PART (e.g., >ay~uhA <in~a >ay).

The SUB_CONJ tag was created and populated with former CONJ and FUNC_WORD items (e.g., <in <in~a >an >al~A >an~a <i* <i*A <il~A <in~amA Eal~a law).

Some PREP items were tagged also as NOUN, in order to distinguish different syntactic structures, such as "bayona" (PREP), and "min bayoni" (PREP + NOUN).

In version 2.0 we added tags for passive verbs: PV_PASS (Perfect Verb Passive) and IV_PASS (Imperfect Verb Passive).


(5) Implementation of full vocalization, including mood markers for imperfect verbs

See above, "SHORT VOWELS AND DIACRITICS."


(6) New algorithm for POS-tagging of Latin characters, punctuation, and numbers

Whereas version 1.0 simply echoed non-Arabic strings and returned them without any analysis, version 2.0 does some rudimentary parsing of non-Arabic strings, and assigns LAT, PUNC, and NUM tags as appropriate. The following examples come from the sample analysis file "outfile.xml":

   <token_notArabic>3-2
     <analysis>3-2/NUM</analysis>
   </token_notArabic>
   
   <token_notArabic>°
     <analysis>,/PUNC</analysis>
   </token_notArabic>
   
   <token_notArabic>TMA
     <analysis>TMA/LATIN</analysis>
   </token_notArabic>


(7) Improved algorithm for handling orthographic variants and substandard orthography

See above, "ORTHOGRAPHIC VARIANTS" and "ORTHOGRAPHIC ANOMALIES."


(8) Words that are not found because their stems are not in the lexicon of stems can still be partially analysed by using existing prefix and suffix entries and stem entries with wildcards, such as the following:

  ;; XX_1
  XX	XX	N0	NOT_IN_LEXICON     <pos>XX/NOUN_PROP</pos>
  ;; XXX_1
  XXX	XXX	N0	NOT_IN_LEXICON     <pos>XXX/NOUN_PROP</pos>
  ;; XXXX_1
  XXXX	XXXX	N0	NOT_IN_LEXICON     <pos>XXXX/NOUN_PROP</pos>
  ;; XXXXX_1
  XXXXX	XXXXX	N0	NOT_IN_LEXICON     <pos>XXXXX/NOUN_PROP</pos>

We have called these "X Solutions." For example, assuming that the stem for the word "AlfAlwjp" were absent in the lexicon ("AlfAlwjp" is a variant spelling of the more common "Alflwjp"), the word can still be identified and POS-tagged as a proper noun (including proper tagging of the definite article and any other prefixes), by using the "X Solution" method. The following example has 4 "X Solutions" (the last one is the right one):

<token_Arabic>Ê»«·›«·ÊÃ…
  <variant>wbAlfAlwjp
    <x_solution>
      <voc>wbAlfAlwjp</voc>
      <pos>wbAlfAlwjp/NOUN_PROP</pos>
      <gloss>NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>wabAlfAlwjp</voc>
      <pos>wa/CONJ+bAlfAlwjp/NOUN_PROP</pos>
      <gloss>and + NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>wabiAlfAlwjp</voc>
      <pos>wa/CONJ+bi/PREP+AlfAlwjp/NOUN_PROP</pos>
      <gloss>and + by/with + NOT_IN_LEXICON</gloss>
    </x_solution>
    <x_solution>
      <voc>wabiAlfAlwjp</voc>
      <pos>wa/CONJ+bi/PREP+Al/DET+fAlwjp/NOUN_PROP</pos>
      <gloss>and + with/by + the + NOT_IN_LEXICON</gloss>
    </x_solution>
  </variant>
</token_Arabic>


**********************************************************************
6. ACKNOWLEDGEMENTS
**********************************************************************

This work could not have been done without the support of the Linguistic Data Consortium, especially the Arabic Annotation staff under the directorship of Mohamed Maamouri. The Arabic Annotation staff provided valuable daily feedback on the Analyzer performance and lexicon coverage during the manual tagging of three newswire corpora at the LDC. These efforts are described in the following published papers:

   * Mohamed Maamouri and Ann Bies. "Developing an Arabic Treebank: Methods, Guidelines, Procedures, and Tools," in Proceedings of the Workshop on Computational Approaches to Arabic Script-based Languages, COLING 2004, Geneva, August 28, 2004. http://www.ldc.upenn.edu/Papers/COLING2004/Maamouri-Bies_Penn-Arabic-Treebank.pdf

   * Tim Buckwalter. "Issues in Arabic Orthography and Morphology Analysis," in Proceedings of the Workshop on Computational Approaches to Arabic Script-based Languages, COLING 2004, Geneva, August 28, 2004. http://www.ldc.upenn.edu/Papers/COLING2004/Buckwalter_Arabic-orthography-morphology.pdf

I'd like to thank my colleague at the LDC, David Graff, for providing a very thorough critique of version 1.0. Several of his suggestions are still on my "to do" list!

My good friend Hans Paulussen exported the dictionary hash tables to DBM files and registered a slightly faster dictionary load time. He attributed the slow load time to the nature of the hash, where "the key refers to an array which has to be unpacked."

Fellow Arabist and Perl enthusiast Ota Smrz provided (and continues to provide) extremely valuable critique on the content of the output, especially the grammatical and morphological information provided. He also found the time to write an Encode Arabic module extension to handle conversions involving my transliteration and ArabTeX (http://ckl.mff.cuni.cz/smrz/). For now I have decided to keep things simple by handling all input data conversions outside the Analyzer. 

Pierrick Brihaye (http://www.nongnu.org/aramorph/french/index.html) ported the Analyzer to Java and used it "for indexing and full text retrieval on top of Lucene" (http://jakarta.apache.org/lucene/docs/index.html). Pierrick provided some valuable feedback on the functionality of the compatibility tables.



**********************************************************************
APPENDIX: BUCKWALTER TRANSLITERATION 
**********************************************************************
http://www.qamus.org/transliteration.htm

Fields are: Buckwalter transliteration, Arabic Windows (1256), and Unicode.

'  C1  U+0621 ARABIC LETTER HAMZA
|  C2  U+0622 ARABIC LETTER ALEF WITH MADDA ABOVE
>  C3  U+0623 ARABIC LETTER ALEF WITH HAMZA ABOVE
&  C4  U+0624 ARABIC LETTER WAW WITH HAMZA ABOVE
<  C5  U+0625 ARABIC LETTER ALEF WITH HAMZA BELOW
}  C6  U+0626 ARABIC LETTER YEH WITH HAMZA ABOVE
A  C7  U+0627 ARABIC LETTER ALEF
b  C8  U+0628 ARABIC LETTER BEH
p  C9  U+0629 ARABIC LETTER TEH MARBUTA
t  CA  U+062A ARABIC LETTER TEH
v  CB  U+062B ARABIC LETTER THEH
j  CC  U+062C ARABIC LETTER JEEM
H  CD  U+062D ARABIC LETTER HAH
x  CE  U+062E ARABIC LETTER KHAH
d  CF  U+062F ARABIC LETTER DAL
*  D0  U+0630 ARABIC LETTER THAL
r  D1  U+0631 ARABIC LETTER REH
z  D2  U+0632 ARABIC LETTER ZAIN
s  D3  U+0633 ARABIC LETTER SEEN
$  D4  U+0634 ARABIC LETTER SHEEN
S  D5  U+0635 ARABIC LETTER SAD
D  D6  U+0636 ARABIC LETTER DAD
T  D8  U+0637 ARABIC LETTER TAH
Z  D9  U+0638 ARABIC LETTER ZAH
E  DA  U+0639 ARABIC LETTER AIN
g  DB  U+063A ARABIC LETTER GHAIN
_  DC  U+0640 ARABIC TATWEEL
f  DD  U+0641 ARABIC LETTER FEH
q  DE  U+0642 ARABIC LETTER QAF
k  DF  U+0643 ARABIC LETTER KAF
l  E1  U+0644 ARABIC LETTER LAM
m  E3  U+0645 ARABIC LETTER MEEM
n  E4  U+0646 ARABIC LETTER NOON
h  E5  U+0647 ARABIC LETTER HEH
w  E6  U+0648 ARABIC LETTER WAW
Y  EC  U+0649 ARABIC LETTER ALEF MAKSURA
y  ED  U+064A ARABIC LETTER YEH
F  F0  U+064B ARABIC FATHATAN
N  F1  U+064C ARABIC DAMMATAN
K  F2  U+064D ARABIC KASRATAN
a  F3  U+064E ARABIC FATHA
u  F5  U+064F ARABIC DAMMA
i  F6  U+0650 ARABIC KASRA
~  F8  U+0651 ARABIC SHADDA
o  FA  U+0652 ARABIC SUKUN
`      U+0670 ARABIC LETTER SUPERSCRIPT ALEF
{      U+0671 ARABIC LETTER ALEF WASLA
P  81  U+067E ARABIC LETTER PEH
J  8D  U+0686 ARABIC LETTER TCHEH
V      U+06A4 ARABIC LETTER VEH
G  90  U+06AF ARABIC LETTER GAF

Tim Buckwalter
QAMUS LLC
448 South 48th St.
Philadelphia, PA 19143-1727
www.qamus.org


**********************************************************************
                                END OF FILE
**********************************************************************
