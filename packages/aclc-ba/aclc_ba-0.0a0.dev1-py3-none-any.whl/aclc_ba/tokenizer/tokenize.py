# -*- coding: utf-8 -*-
# Copyright (C) 2023 Bibliotheca Alexandrina <www.bibalex.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module contains utilities for simple tokenization.
"""

from aclc_ba.utils.segmentation_matching import URL_MATCH
from aclc_ba.utils.segmentation_matching import EMAIL_MATCH
from aclc_ba.utils.segmentation_matching import CHECK_IN_WORD_OR_LINE
from aclc_ba.utils.segmentation_matching import UNICODE_INTERGER_LIST
from aclc_ba.utils.segmentation_matching import ARABIC_DIACRATICS_MATCH
from aclc_ba.utils.segmentation_matching import NEGATIVE_NUMBERS
from aclc_ba.utils.segmentation_matching import INVALIDCHARS
from aclc_ba.tokenizer.sentence_markup import SentenceMarkup
from aclc_ba.tokenizer.post_tokenize import PostTokenizer

import re


class Tokenize:
    def __init__(self, **kwargs) -> None:
        self.tokenized = []
        self.post_tokenized = []
        if kwargs.get("post_tokenize"):
            if kwargs.get("text_to_tokenize"):
                self.list_out_of_sentencizer = SentenceMarkup(
                    kwargs.get("text_to_tokenize")
                ).splited_paragraphs_with_markup
                self.tokenized = self.send_tokenize_sentence(
                    self.list_out_of_sentencizer
                )
                for token in self.tokenized:
                    tkn = PostTokenizer(token)
                    self.post_tokenized.append(tkn.post_tokenized_list)
            elif kwargs.get("list_to_tokenize"):  # passed one list
                self.tokenized = kwargs.get("list_to_tokenize")
                tkns = PostTokenizer(self.tokenized)
                self.post_tokenized.extend(tkns.post_tokenized_list)
        elif kwargs.get("text_to_tokenize"):
            self.list_out_of_sentencizer = SentenceMarkup(
                kwargs.get("text_to_tokenize")
            ).splited_paragraphs_with_markup
            self.tokenized = self.send_tokenize_sentence(self.list_out_of_sentencizer)
        elif kwargs.get("list_to_tokenize"):
            self.tokenized = self.send_tokenize_sentence(kwargs.get("list_to_tokenize"))
        else:
            pass

    def replace_all(self, text: str, dic: dict) -> str:
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def send_tokenize_sentence(self, list_to_tokenize: list[str]) -> list[str]:
        for sentence in list_to_tokenize:
            self.tokenized.append(self.tokenize(sentence))
        return self.tokenized

    def tokenize(self, sentence: str) -> list[str]:
        words_pure = []
        word_index = 0
        sent = sentence.replace("\u200f", "")
        for word in sent.split(" "):
            if URL_MATCH.search(word) == None:
                if EMAIL_MATCH.search(word) == None:
                    if bool(
                        re.search("[a-zA-Z]", word)
                    ):  #  if arabic concted with english

                        reg = re.compile(
                            "([\u0600-\u06FF]+(?:\s+[\u0600-\u06FF]+)*)\s*"
                        )  #  tokenize_concated_arabic_with_non_arabic
                        word_list = list(filter(None, reg.split(word)))
                        words_pure = words_pure + word_list
                        continue
                    if bool(re.search(r"\d", word)):  #  if has digits
                        word_list = list(
                            filter(None, re.split(r"(-?\d+[\.|\,|%|/]?\d*[/]?\d*)", word))
                        )
                        words_pure = words_pure + word_list
                        continue
            if (
                any(c in word for c in INVALIDCHARS)
                and URL_MATCH.search(word) == None
                and EMAIL_MATCH.search(word) == None
                and NEGATIVE_NUMBERS.search(word) == None
            ):
                for c in INVALIDCHARS:
                    word = word.replace(c, " " + c + " ")
            word = re.sub(ARABIC_DIACRATICS_MATCH, "", word)
            rep_out_word = {
                " الخ ": " إلخ ",
                "  ": " ",
                ". .": "..",
                "- -": "--",
                "… …": "……",
            }
            word = self.replace_all(word, rep_out_word)

            word = word.translate({ord(c): None for c in UNICODE_INTERGER_LIST}).strip()
            word = word.replace("'", "''")
            if ("&" in word or "<" in word or ">" in word) and len(word) > 1:
                word = word.replace("&", " ")
                word = word.replace(">", " ")
                word = word.replace("<", " ")
            if word:
                words_pure.append(word.strip())
            word_index += 1
        word_index += 1

        return words_pure
