#!/usr/local/bin/perl -w
################################################################################
# Buckwalter Arabic Morphological Analyzer Version 2.0
# Portions (c) 2002-2004 QAMUS LLC (www.qamus.org), 
# (c) 2002-2004 Trustees of the University of Pennsylvania 
# 
# LDC USER AGREEMENT
# 
# Use of this version of the Buckwalter Arabic Morphological Analyzer Version 2
# distributed by the Linguistic Data Consortium (LDC) of the University of 
# Pennsylvania is governed by the following terms: 
# 
# This User Agreement is provided by the Linguistic Data Consortium as a 
# condition of accepting the databases named or described herein. 
# 
# This Agreement describes the terms between User/User's Research Group and 
# Linguistic Data Consortium (LDC), in which User will receive material, as 
# specified below, from LDC. The terms of this Agreement supercede the terms of 
# any previous Membership Agreement in regard to the Buckwalter Arabic 
# Morphological Analyzer Version 2.
# 
# Under this agreement User will receive one or more CD-ROM discs, DVDs, 
# electronic files or other media as appropriate, containing linguistic tools, 
# speech, video, and/or text data. User agrees to use the material received 
# under this agreement only for non-commercial linguistic education and research
# purposes. Unless explicitly permitted herein, User shall have no right to 
# copy, redistribute, transmit, publish or otherwise use the LDC Databases for 
# any other purpose and User further agrees not to disclose, copy, or 
# re-distribute the material to others outside of User's research group. 
# 
# Government use, including any use within or among government organizations and
# use by government contractors to produce or evaluate resources and 
# technologies for government use, is permitted under this license.
# 
# Organizations interested in licensing the Buckwalter Arabic Morphological 
# Analyzer Version 2 for commercial use should contact: 
# 
#    QAMUS LLC 
#    448 South 48th St. 
#    Philadelphia, PA 19143 
#    ATTN: Tim Buckwalter 
#    email: license@qamus.org
# 
# Except for Government use as specified above, commercial uses of this corpus 
# include, but are not limited to, imbedded use of the Analyzer, Analyzer 
# methods, Analyzer derived works, Analyzer output data, algorithms, lexicons, 
# and downloaded data in a commercial product or a fee for service project; 
# use of the Analyzer, Analyzer methods, Analyzer derived works, Analyzer 
# output data, algorithms, and downloaded data to create or develop a 
# commercial product or perform a fee for service project; use of Analyzer, 
# Analyzer methods, Analyzer derived works, Analyzer output data, algorithms, 
# lexicons, and downloaded data as a development tool to measure performance of
# a commercial product or work product developed on a fee for service basis; 
# redistribution of Analyzer, Analyzer methods, Analyzer derived works, Analyzer 
# output data, algorithms, lexicons and downloaded data to any third party for 
# imbedding in a commercial product or fee for service project, for deriving a 
# commercial product or fee for service project, or for measuring the 
# performance of a commercial product or fee for service project.
# 
# USER ACKNOWLEDGES AND AGREES THAT "CORPORA RECEIVED" ARE PROVIDED ON AN "AS-IS"
# BASIS AND THAT LDC, ITS HOST INSTITUTION THE UNIVERSITY OF PENNSYLVANIA, AND 
# ITS DATA PROVIDERS AND CORPUS AUTHORS MAKE NO REPRESENTATIONS OR WARRANTIES OF 
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR CONFORMITY WITH 
# WHATEVER DOCUMENTATION IS PROVIDED. IN NO EVENT SHALL LDC, ITS HOST 
# INSTITUTION, DATA PROVIDORS OR CORPUS AUTHORS BE LIABLE FOR SPECIAL, DIRECT, 
# INDIRECT, CONSEQUENTIAL, PUNITIVE, INCIDENTAL OR OTHER DAMAGES, LOSSES, COSTS, 
# CHARGES, CLAIMS, DEMANDS, FEES OR EXPENSES OF ANY NATURE OR KIND ARISING IN ANY
# WAY FROM THE FURNISHING OF OR USER'S USE OF THE CORPORA RECEIVED. 
# 
#
################################################################################
# usage: 
# perl -w AraMorph.pl < infile.txt > outfile.xml
# were "infile" is the input text in Arabic Windows encoding (Windows-1256) 
# and "outfile.xml" is the output text in UTF-8 encoding with morphology analyses 
# and POS tags. The list of "not found" items is written to filename "nf" and 
# related statistics are written to STDERR. For example:
# 
# perl -w AraMorph.pl < infile.txt > outfile.xml
# loading dictPrefixes ... 548 entries
# loading dictStems ...  40219 lemmas and 78839 entries
# loading dictSuffixes ... 906 entries
# reading input line 28
# tokens: 67  -- not found (types): 1 (1.49253731343284%)

################################################################################
#!/usr/local/bin/perl -w
use FindBin;
use Encode qw/encode decode/;
binmode STDOUT, ":utf8"; # Perl 5.8.0

#print header
print"word,root,stem_pattern,lemmaid,voc,pr,stem,suf,gloss\n";

# load 3 compatibility tables (load these first so when we load the lexicons we can check for 
#   undeclared $cat values) -- this has not been implemented yet
%hash_AB = load_table("$FindBin::Bin/tableAB"); # compatibility table for prefix-stem combinations    (AB)
%hash_AC = load_table("$FindBin::Bin/tableAC"); # compatibility table for prefix-suffix combinations  (AC)
%hash_BC = load_table("$FindBin::Bin/tableBC"); # compatibility table for stem-suffix combinations    (BC)

# load 3 lexicons
%prefix_hash = load_dict("$FindBin::Bin/dictPrefixes"); # dict of prefixes (A)
%stem_hash   = load_dict("$FindBin::Bin/dictStems");    # dict of stems    (B)
%suffix_hash = load_dict("$FindBin::Bin/dictSuffixes"); # dict of suffixes (C)

$tokens = 0;
my $file = $ARGV[0];
open (FH, '<', $file) or die "Can't open '$file' for read: $!";
binmode FH, ":utf8"; # Perl 5.8.0
$not_found_cnt = 0; 

while (<FH>) {

   print STDERR "reading input line $.\r";
   @tokens = tokenize($_); # returns a list of tokens (one line at a time)
   foreach $token (@tokens) {
      $token  = encode("cp1256", $token);
      # (1) process Arabic words
      if ($token =~ m/[\x81\x8D\x8E\x90\xC1-\xD6\xD8-\xDB\xDD-\xDF\xE1\xE3-\xE6\xEC-\xED\xF0-\xF3\xF5\xF6\xF8\xFA]/) { # it's an Arabic word
         $utf8_token  = decode("cp1256", $token); 
         $lookup_word = get_lookup($token); # returns the Arabic string without vowels/diacritics and converted to transliteration
         if ( $lookup_word eq "" ) { # input was one or more zero-width diacritics not attached to any char (i.e., a typo)
            $xml_variant = $token; 
            $xml_variant =~ tr/\xF0\xF1\xF2\xF3\xF5\xF6\xF8\xFA/FNKaui~o/; # convert to transliteration
            print "  <variant>$xml_variant\n"; print"word,root,spattern,lemmaID,voc,pr,Stem,Suf,gloss\n";
            print "    <solution>\n";
            print "      <voc>$xml_variant</voc>,";
            print "      <pos>$xml_variant/NOUN</pos>,";
            print "      <gloss>[loose diacritic(s)]</gloss>,";
            print "    </solution>\n";
            print "  </variant>\n"; 
         }
         else {
            $lookup_word =~ s/Y(?=([^']))/y/g; # Y is always y unless /(Y$|Y'$)/ (we convert /Y'$/ to /}/ and /y'/ later)
            $not_found = 1; $tokens++; #$types{$lookup_word}++; 
            if ( exists($seen_lookup_words{$lookup_word}) ) { 
               print "$seen_lookup_words{$lookup_word}"; # no need to look up the same word twice
            } 
            else {
               @variants = get_variants($lookup_word); # always returns at least one: the initial $lookup_word
               foreach $variant (@variants) {
                  $xml_variant = $variant; # get a copy to modify and print to XML output file
                  $xml_variant =~ s/&/&amp;/g; $xml_variant =~ s/>/&gt;/g; $xml_variant =~ s/</&lt;/g;
                  $seen_lookup_words{$lookup_word} .= "  <variant>$xml_variant\n";
                  if ( @solutions = analyze($variant) ) { # if the variant has 1 or more solutions
                     $not_found = 0; 
                     foreach $solution (@solutions) {
                        print "\n$solution"; 
                        $seen_lookup_words{$lookup_word} .= "\n$solution";
                     }
                  }
                  if ( @no_solutions = analyze_notfound($variant) ) { # if variant has 1 or more "no_solutions"
                     foreach $no_solution (@no_solutions) {
                        print "\n$no_solution"; 
                        $seen_lookup_words{$lookup_word} .= "\n$no_solution";
                     }
                  }
                  #print "  </variant>\n"; 
                  $seen_lookup_words{$lookup_word} .= "  </variant>\n"; 
               }  # end foreach
               if ( $not_found == 1 ) { print NOTFOUND "$utf8_token\n"; $not_found_cnt++ }
            } # end else
         }
      }
      # (2) process non-Arabic strings (Latin, punctuation, numbers)
      else {
         @nonArabictokens = tokenize_nonArabic($token); # tokenize it on white space
         foreach $nonArabictoken (@nonArabictokens) {
         
           # tokenize non-Arabic strings into Latin, numbers, and punctuation
           #  extract Latin strings first (they may have embedded nums & punct), then extracts nums & punct
           unless ($nonArabictoken eq " " or $nonArabictoken eq "") {
              $nonArabictoken =~ s/(\d)o(\d)/$1.$2/g; # "o" is temp numeric period in Ummah corpus
              if ($nonArabictoken =~ m/[^A-Z0-9]+$/i) { # string ends in 1 or more PUNCT chars
                 $before = $`; $after  = $&;
                 unless ($before eq "") {
                    if ($before =~ m/[A-Z]/i) { # treat entire string as LATIN
                       print "\n";
					        print "$before,";
                       print ",,,,,,";
                       print "$before/LATIN,";
                       print ",\n";
                    }
                    else { # string has numbers, with optional embedded punct
                       @list = split (m/(\d+[\.\-\,\_\xB1]?(\d*[\.\-]*)+|\.\d+)/ ,$before);
                       foreach $item_num_punc (@list) {
                          if ($item_num_punc =~ m/[0-9]/) {
                             $item_num_punc =~ s/\xB1/\xDC/g; # restore kashida \xDC from temp char \xB1 �
                             $utf8_item_num_punc = decode("cp1256", $item_num_punc); 
							        print "$utf8_item_num_punc,";
                             print ",,,,,";
                             $item_num_punc =~ tr/\xA1\xBA\xBF\xDC/\,\;\?\_/; 
                             print "$item_num_punc/NUM,";
                             print ",\n";
                          }
                          else {
                             @punc_list = split ( "" ,$item_num_punc);
                             foreach $punc_item (@punc_list) {
                                $punc_item =~ s/\xB1/\xDC/g; # restore kashida \xDC from temp char \xB1 �
                                $utf8_punc_item = decode("cp1256", $punc_item);
								        print "$utf8_punc_item,";
                                print ",,,,,";
                                $punc_item =~ tr/\xA1\xBA\xBF\xDC/\,\;\?\_/; 
                                print "$punc_item/PUNC,";
                                print ",\n";
                             }
                          }
                       }
                    }
                 }#end unless
                 @punc_list = split ( "" ,$after);
                 foreach $punc_item (@punc_list) {
                    $punc_item =~ s/\xB1/\xDC/g; # restore kashida \xDC from temp char \xB1 �
                    $utf8_punc_item = decode("cp1256", $punc_item);
                    $utf8_punc_item =~ s/,/","/g;
					     print "\n$utf8_punc_item,";
                    print ",,,,,";
                    $punc_item =~ tr/\xA1\xBA\xBF\xDC/\,\;\?\_/; 
                    $punc_item =~ s/,/","/g;
                    print "$punc_item/Punc,";
                    print ",\n";
                 }
              }#end if

              else { # string ends in 1 or more LATIN or NUM chars
                 if ($nonArabictoken =~ m/[A-Z]/i) { # treat entire string as LATIN
					     print "$nonArabictoken,";
                    print ",,,,,";
                    print "$nonArabictoken/LATIN,";
                    print ",\n";
                 }
                 else { # string has numbers
                    @list = split (m/(\d+[\.\-\,\_\xB1]?(\d*[\.\-]*)+|\.\d+)/ ,$nonArabictoken);
                    foreach $item_num_punc (@list) {
                       if ($item_num_punc =~ m/[0-9]/) {
                          $item_num_punc =~ s/\xB1/\xDC/g; # restore kashida \xDC from temp char \xB1 �
                          $utf8_item_num_punc = decode("cp1256", $item_num_punc);
						        print "$utf8_item_num_punc,";
                          print ",,,,,";
                          $item_num_punc =~ tr/\xA1\xBA\xBF\xDC/\,\;\?\_/; 
                          print "$item_num_punc/NUM,";
                          print ",\n";
                       }
                       else {
                          @punc_list = split ( "" ,$item_num_punc);
                          foreach $punc_item (@punc_list) {
                             $punc_item =~ s/\xB1/\xDC/g; # restore kashida \xDC from temp char \xB1 �
                             $utf8_punc_item = decode("cp1256", $punc_item);
                             $punc_item =~ tr/\xA1\xBA\xBF\xDC/\,\;\?\_/; 
							        print "$utf8_punc_item,";
                             print ",,,,,";
                             print "$punc_item/PUNC,";
                             print ",\n";
                          }
                       }
                    }
                 }
              }
              #print join ("+", @nonArabicSolutions); print "\n";
           }#end unless
        }#end foreach
      }#end else
   }#end foreach

}#end while (<STDIN>)

if ( $not_found_cnt > 0 ) {
   $not_found_percent = $not_found_cnt * 100 / $tokens;
}
else { $not_found_percent = 0 }

print STDERR "\ntokens: $tokens  -- not found (types): $not_found_cnt ";
print STDERR "($not_found_percent\%)";

# ============================
sub analyze { # returns a list of 1 or more solutions

   $this_word = shift @_; @solutions = (); $cnt = 0;
   @segmented = segmentword($this_word); # get a list of valid segmentations
   foreach $segmentation (@segmented) {
      ($prefix,$stem,$suffix) = split ("\t",$segmentation); #print $segmentation, "\n";
      if (exists($prefix_hash{$prefix})) {
         if (exists($stem_hash{$stem})) {
            if (exists($suffix_hash{$suffix})) {
               # all 3 components exist in their respective lexicons, but are they compatible? (check the $cat pairs)
               foreach $prefix_value (@{$prefix_hash{$prefix}}) {
                  ($prefix, $voc_a, $cat_a, $gloss_a, $pos_a) = split (/\t/, $prefix_value);
                  $voc_a =~ s/&/&amp;/g; $voc_a =~ s/>/&gt;/g; $voc_a =~ s/</&lt;/g; 
                  $pos_a =~ s/&/&amp;/g; $pos_a =~ s/>/&gt;/g; $pos_a =~ s/</&lt;/g; 
                  foreach $stem_value (@{$stem_hash{$stem}}) {
                     ($stem, $voc_b, $cat_b, $gloss_b, $pos_b, $lemmaID, $root, $spattern) = split (/\t/, $stem_value);
                     $lemmaID =~ s/&/&amp;/g; $lemmaID =~ s/>/&gt;/g; $lemmaID =~ s/</&lt;/g; 
					      $root =~ s/&/&amp;/g; $root =~ s/>/&gt;/g; $root =~ s/</&lt;/g; 
					      $spattern =~ s/&/&amp;/g; $spattern =~ s/>/&gt;/g; $spattern =~ s/</&lt;/g; 
                     $voc_b =~ s/&/&amp;/g; $voc_b =~ s/>/&gt;/g; $voc_b =~ s/</&lt;/g; 
                     $pos_b =~ s/&/&amp;/g; $pos_b =~ s/>/&gt;/g; $pos_b =~ s/</&lt;/g; 
                     if ( exists($hash_AB{"$cat_a"." "."$cat_b"}) ) {
                        foreach $suffix_value (@{$suffix_hash{$suffix}}) {
                           ($suffix, $voc_c, $cat_c, $gloss_c, $pos_c) = split (/\t/, $suffix_value);
                           $voc_c =~ s/&/&amp;/g; $voc_c =~ s/>/&gt;/g; $voc_c =~ s/</&lt;/g; 
                           $pos_c =~ s/&/&amp;/g; $pos_c =~ s/>/&gt;/g; $pos_c =~ s/</&lt;/g; 
                           if ( exists($hash_AC{"$cat_a"." "."$cat_c"}) ) {
                              if ( exists($hash_BC{"$cat_b"." "."$cat_c"}) ) {
                                 $voc_str = "$voc_a+$voc_b+$voc_c"; 
                                 $voc_str =~ s/^((wa|fa)?(bi|ka)?Al)\+([tvd\*rzs\$SDTZln])/$1$4~/; # moon letters
                                 $voc_str =~ s/^((wa|fa)?lil)\+([tvd\*rzs\$SDTZln])/$1$3~/; # moon letters
                                 $voc_str =~ s/A\+a([pt])/A$1/; # e.g.: Al+HayA+ap
                                 $voc_str =~ s/\{/A/g; 
                                 $voc_str =~ s/\+//g; 
                                 $pos_a =~ s/^\+//; $pos_a =~ s/\+$//; 
								 $pos_b =~ s/^\+//; $pos_b =~ s/\+$//; 
								 $pos_c =~ s/^\+//; $pos_c =~ s/\+$//; 
								 $gloss_str = "$gloss_a + $gloss_b + $gloss_c"; $gloss_str =~ s/^\s*\+\s*//; $gloss_str =~ s/\s*\+\s*$//; 
                                 push (@solutions,"$utf8_token,$root,$spattern,$lemmaID,$voc_str,$pre_str,$pos_b,$pos_c,$gloss_str"); # unless $pos_str =~ m/PREP.+ACC/;}
                              }
                           }
                        }
                     }
                  }
               }# end foreach $prefix_value
            }
         }# end if (exists($stem_hash{$stem}))
      }
   }# end foreach $segmentation
   return (@solutions);

}
# ==============================================================
sub analyze_notfound { # returns a list of 1 or more "solutions" based on wildcard stem

   $this_word = shift @_; @no_solutions = (); $cnt = 0;
   segmentword($this_word); # get a list of valid segmentations
   foreach $segmentation (@segmented) {
      ($prefix,$stem,$suffix) = split ("\t",$segmentation); #print $segmentation, "\n";
      $stemX = $stem; $stemX =~ s/./X/g;
      $stem  =~ s/&/&amp;/g; $stem  =~ s/>/&gt;/g; $stem  =~ s/</&lt;/g; 
      if (exists($prefix_hash{$prefix}) and $not_found==1) {
         if (exists($stem_hash{$stemX})) {
            if (exists($suffix_hash{$suffix})) {
               # all 3 components exist in their respective lexicons, but are they compatible? (check the $cat pairs)
               foreach $prefix_value (@{$prefix_hash{$prefix}}) {
                  ($prefix, $voc_a, $cat_a, $gloss_a, $pos_a) = split (/\t/, $prefix_value);
                  $voc_a =~ s/&/&amp;/g; $voc_a =~ s/>/&gt;/g; $voc_a =~ s/</&lt;/g; 
                  $pos_a =~ s/&/&amp;/g; $pos_a =~ s/>/&gt;/g; $pos_a =~ s/</&lt;/g;
                  foreach $stem_value (@{$stem_hash{$stemX}}) {
                     ($stemX, $voc_b, $cat_b, $gloss_b, $pos_b, $lemmaID, $root, $spattern) = split (/\t/, $stem_value);
                     $pos_b =~ s|X+/|$stem/|; #$lemmaID =~ s|X+|$stem|;
                     if ( exists($hash_AB{"$cat_a"." "."$cat_b"}) ) {
                        foreach $suffix_value (@{$suffix_hash{$suffix}}) {
                           ($suffix, $voc_c, $cat_c, $gloss_c, $pos_c) = split (/\t/, $suffix_value);
                           if ( exists($hash_AC{"$cat_a"." "."$cat_c"}) ) {
                              if ( exists($hash_BC{"$cat_b"." "."$cat_c"}) ) {
                                 $voc_str = "$voc_a+$voc_b+$voc_c"; 
                                 $voc_str =~ s/^((wa|fa)?(bi|ka)?Al)\+([tvd\*rzs\$SDTZln])/$1$4~/; # moon letters
                                 $voc_str =~ s/^((wa|fa)?lil)\+([tvd\*rzs\$SDTZln])/$1$3~/; # moon letters
                                 $voc_str =~ s/A\+a([pt])/A$1/; # e.g.: Al+HayA+ap
                                 $voc_str =~ s/\{/A/g; 
                                 $voc_str =~ s/\+//g; 
                                 $pos_str = "$pos_b+$pos_c"; $pos_str =~ s/^\+//; $pos_str =~ s/\+$//; $pre_str = "$pos_a";
                                 $gloss_str = "$gloss_a + $gloss_b + $gloss_c"; $gloss_str =~ s/^\s*\+\s*//; $gloss_str =~ s/\s*\+\s*$//; 
                                 push (@no_solutions,"$utf8_token,$root,$spattern,$lemmaID,$voc_str,$pre_str,$pos_b,$pos_c,$gloss_str"); # unless $pos_str =~ m/PREP.+ACC/;}
                              }
                           }
                        }
                     }
                  }
               }# end foreach $prefix_value
            }
         }# end if (exists($stem_hash{$stem}))
      }
   }# end foreach $segmentation
   return (@no_solutions);

}

# ===========================================            
sub get_variants { # builds a list of orthographic variants

   my $lookup_word = shift @_; 
   my @variants = ();
   my %seen_variants = ();
   my $str = '';

   push (@variants, $lookup_word); 
   $seen_variants{$lookup_word} = 1; # we don't want any duplicates

   # loop through the list of variants and add more variants if necessary
   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/Y'$/}/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }

   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/w'/&/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }

   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/y'$/}/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }

   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/^>/A/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }
   
    @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/^Al>/AlA/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }
   
   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/^l>/lA/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }
   
   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/^</A/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }
   
   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/y$/Y/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }
   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/Y/y/g) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }

   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/h$/p/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }

   @list = @variants; 
   foreach $item (@list) {
      $str = $item;
      if ($str =~ s/p$/h/) { 
         unless ( exists $seen_variants{$str} ) {
            push (@variants,$str);
            $seen_variants{$str} = 1;
         }
      }
   }

   return @variants;
   
}
# ============================
sub tokenize { # returns a list of tokens
   my $line = shift @_; chomp($line);
   $line =~ s/\xA0/ /g; # convert NBSP to SP
   $line =~ s/\s+/ /g; $line =~ s/^\s+//; $line =~ s/\s+$//; # minimize and trim white space
   $line =~ s/([^\xC8\xCA-\xCE\xD3-\xD6\xD8-\xDF\xE1\xE3-\xE5\xEC\xED])\xDC/$1\xB1/g; 
   @tokens = split (/([^\x81\x8D\x8E\x90\xC1-\xD6\xD8-\xDF\xE1\xE3-\xE6\xEC-\xED\xF0-\xF3\xF5\xF6\xF8\xFA]+)/,$line);
   return @tokens;
}
# ============================
sub tokenize_nonArabic { # tokenize non-Arabic strings by splitting them on white space
   $nonArabic = shift @_;
   $nonArabic =~ s/^\s+//; $nonArabic =~ s/\s+$//; # remove leading & trailing space
   @nonArabictokens = split (/\s+/, $nonArabic);
   return @nonArabictokens;
}
# ================================
sub get_lookup { # creates a lookup version of the Arabic input string (removes diacritics; transliterates)
   my $input_str = shift @_;
   my $tmp_word = $input_str; # we need to modify the input string for lookup
   $tmp_word =~ s/\xDC//g;  # remove kashida/taTwiyl (U+0640)
   $tmp_word =~ s/\xF0\xC7/\xC7\xF0/g;  # change -FA to canonical -AF
   $tmp_word =~ s/\xC7\xF0/\xC7\x21/g;  # change -AF temporarily to -A!
   $tmp_word =~ s/[\xF0-\xF3\xF5\xF6\xF8\xFA]//g;  # remove all vowels/diacritics
   $tmp_word =~ s/\xC7\x21/\xC7\xF0/g;  # restore -AF from temporary -A!
   $tmp_word =~ tr/\x81\x8D\x8E\x90\xA1\xBA\xBF\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF\xE1\xE3\xE4\xE5\xE6\xEC\xED\xF0\xF1\xF2\xF3\xF5\xF6\xF8\xFA/PJRG,;?'|>&<}AbptvjHxd*rzs\$SDTZEg_fqklmnhwYyFNKaui~o/; # convert to transliteration
   return $tmp_word;
}
# ============================
sub segmentword { # returns a list of valid segmentations

   $str = shift @_;
   @segmented = ();
   $prefix_len = 0;
   $suffix_len = 0;
   $str_len = length($str);

   while ( $prefix_len <= 4 ) {
      $prefix = substr($str, 0, $prefix_len);
      $stem_len = ($str_len - $prefix_len); 
      $suffix_len = 0;
      while (($stem_len >= 1) and ($suffix_len <= 6)) {
         $stem   = substr($str, $prefix_len, $stem_len);
         $suffix = substr($str, ($prefix_len + $stem_len), $suffix_len);
         push (@segmented, "$prefix\t$stem\t$suffix");
         $stem_len--;
         $suffix_len++;
      }
      $prefix_len++;
   }
   return @segmented;

}

# ==============================================================
sub load_dict { # loads a dict into a hash table where the key is $entry and its value is a list (each $entry can have multiple values)

   %temp_hash = (); $entries = 0; $lemmaID = ""; $root = ""; $spattern = "";
   $filename = shift @_;
   open (IN, $filename) || die "cannot open: $!";
   print STDERR "loading $filename ...";
   while (<IN>) {
	if  (m/;; /) {  
         $lemmaID = $'; 
         chomp($lemmaID);
         if ( exists($seen{$lemmaID}) ) { 
         }
         else { 
            $seen{$lemmaID} = 1; $lemmas++;
         } 
      } 
		elsif (m/;--- /) {  
        $root = $';
         chomp($root); #$root+;
         }			
      elsif (m/;;;-- /) {  
        $spattern = $';
         chomp($spattern); #$root+;
         }
      elsif (m/^;/) {  } # comment
      else {
         chomp(); $entries++;
         # a little error-checking won't hurt:
         $trcnt = tr/\t/\t/; if ($trcnt != 3) { die "entry in $filename (line $.) doesn't have 4 fields (3 tabs)\n" };
         ($entry, $voc, $cat, $glossPOS) = split (/\t/, $_); # get the $entry for use as key
         # two ways to get the POS info:
         # (1) explicitly, by extracting it from the gloss field:
         if ($glossPOS =~ m!<pos>(.+?)</pos>!) {
            $POS = $1; # extract $POS from $glossPOS
            $gloss = $glossPOS; # we clean up the $gloss later (see below)
         }
         # (2) by deduction: use the $cat (and sometimes the $voc and $gloss) to deduce the appropriate POS
         else {
            $gloss = $glossPOS; # we need the $gloss to guess proper names
            if     ($cat  =~ m/^(Pref-0|Suff-0)$/) {$POS = ""} # null prefix or suffix
            elsif  ($cat  =~ m/^F/)          {$POS = "$voc/FUNC_WORD"}
            elsif  ($cat  =~ m/^IV.*?_Pass/) {$POS = "$voc/IV_PASS"} # added 12/18/2002
            elsif  ($cat  =~ m/^IV/)         {$POS = "$voc/IV"}
            elsif  ($cat  =~ m/^PV.*?_Pass/) {$POS = "$voc/PV_PASS"} # added 12/18/2002
            elsif  ($cat  =~ m/^PV/)         {$POS = "$voc/PV"}
            elsif  ($cat  =~ m/^CV/)         {$POS = "$voc/CV"}
            elsif (($cat  =~ m/^N/)
              and ($gloss =~ m/^[A-Z]/))     {$POS = "$voc/NOUN_PROP"} # educated guess (99% correct)
            elsif (($cat  =~ m/^N/)
              and  ($voc  =~ m/iy~$/))       {$POS = "$voc/NOUN"} # (was NOUN_ADJ: some of these are really ADJ's and need to be tagged manually)
            elsif  ($cat  =~ m/^N/)          {$POS = "$voc/NOUN"}
            else                             { die "no POS can be deduced in $filename (line $.)"; }; 
         }

         # clean up the gloss: remove POS info and extra space
         $gloss =~ s!<pos>.+?</pos>!!; $gloss =~ s/\s+$//; $gloss =~ s!;!/!g;

         # create list of orthographic variants for the entry:
         @entry_forms = ($entry);
         $temp_entry = $entry; # get a temporary working copy of the $entry
         if ( $temp_entry =~ s/^[>|<{]/A/ ) { # stem begins with hamza
            push ( @entry_forms, $temp_entry ); 
         }
         # now load the variant forms
         foreach $entry_form (@entry_forms) {
            push ( @{ $temp_hash{$entry_form} }, "$entry_form\t$voc\t$cat\t$gloss\t$POS\t$lemmaID\t$root\t$spattern") ;
         }
      }
   }
   close IN;
   print STDERR "  $roots roots and" unless ($root eq "");
    print STDERR "  $spatterns spatterns and" unless ($spattern eq "");
   print STDERR "  $lemmas lemmas and" unless ($lemmaID eq "");
      print STDERR " $entries entries \n";
   return %temp_hash;

}

# ==============================================================
sub load_table { # loads a compatibility table into a hash table

   %temp_hash = ();
   $filename = shift @_;
   open (IN, $filename) || die "cannot open: $!";
   while (<IN>) {
      unless ( m/^;/ ) {
         chomp();
         s/^\s+//; s/\s+$//; s/\s+/ /g; # remove or minimize white space
         $temp_hash{$_} = 1;
      }
   }
   close IN;
   return %temp_hash;

}
# ==============================================================
