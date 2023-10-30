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

"""This module contains utilities for more tokenization.
"""

from aclc_ba.utils.data_reader import DataReader
from pathlib import Path


class PostTokenizer:
    def __init__(
        self, tokenized_list: list[str] = None
    ):  # here we will take token_lst or one token
        self.source_token = ""
        self.tokenized_list = tokenized_list
        self.edited_part1 = ""  # edited_one
        self.edited_part2 = ""  # edited_two
        self.words_dic = dict()  # vocab with frequency
        self.post_tokenized_dic = (
            dict()
        )  # [{'edited_word': [{ source_word}], 'edited_word_2': [{source_word}] ]
        self.post_tokenized_list = []
        self.send_tokwenizedlist_token(self.tokenized_list)

    def in_call(self, token):  # call all methodes here
        tuple_to_exend = token
        alef_letters = ["إ", "أ", "آ", "ا"]
        double_alef_list = ["أا", "اأ", "اا", "اإ", "إا", "ءأ", "ءإ", "ءء"]
        if any(substring in token for substring in double_alef_list):
            tuple_to_exend = self.tokenize_double_alef(token)
        elif token[:2] == "ما" and len(token) > 4 and " " not in tuple_to_exend:
            tuple_to_exend = self.check_ma_intizalize(token)
        elif token[:2] == "لا" and len(token) > 4 and " " not in tuple_to_exend:
            tuple_to_exend = self.check_la_intizalize(token)
        elif (
            token[:2] == "بو"
            or token[:3] == "ابو"
            or token[:3] == "أبو"
            and " " not in tuple_to_exend
        ):
            tuple_to_exend = self.check_abo_intizalize(token)
        elif any(c in token[:4] for c in alef_letters) and " " not in tuple_to_exend:
            tuple_to_exend = self.check_hamza(token)
        if (
            tuple_to_exend[-1] == "ي"
            or tuple_to_exend[-1] == "ى"
            and " " not in tuple_to_exend
        ):
            tuple_to_exend = self.correct_ya(tuple_to_exend)
        if " " not in tuple_to_exend and not type(tuple_to_exend) == list:
            tuple_to_exend = self.split_custome_cases(tuple_to_exend)
        if type(tuple_to_exend) == list:
            self.post_tokenized_list.extend(tuple_to_exend)
            self.post_tokenized_dic[tuple_to_exend[0]] = token
            self.post_tokenized_dic[tuple_to_exend[1]] = token
        else:
            self.post_tokenized_list.append(tuple_to_exend)
            self.post_tokenized_dic[tuple_to_exend] = token

    def send_tokwenizedlist_token(self, tokenize_list: list[str]) -> list[str]:
        for token in tokenize_list:  # list of lists come from tokenize
            self.in_call(token)
        return self.post_tokenized_list

    def tokenize_double_alef(self, token):  # tokenize_double_alef
        Last_Index = -1
        char_pos = 0
        source_word = token
        if (
            "أا" in source_word
            and not source_word.startswith("أا")
            and not source_word.endswith("أا")
        ):
            char_pos = source_word.index("أا")
        elif (
            "اأ" in source_word
            and not source_word.startswith("اأ")
            and not source_word.endswith("اأ")
        ):
            char_pos = source_word.index("اأ")
        elif (
            "اا" in source_word
            and not source_word.startswith("اا")
            and not source_word.endswith("اا")
        ):
            char_pos = source_word.index("اا")
        elif (
            "اإ" in source_word
            and not source_word.startswith("اإ")
            and not source_word.endswith("اإ")
        ):
            char_pos = source_word.index("اإ")
        elif (
            "إا" in source_word
            and not source_word.startswith("إا")
            and not source_word.endswith("إا")
        ):
            char_pos = source_word.index("إا")
        elif (
            "ءأ" in source_word
            and not source_word.startswith("ءأ")
            and not source_word.endswith("ءأ")
        ):
            char_pos = source_word.index("ءأ")
        elif (
            "ءإ" in source_word
            and not source_word.startswith("ءإ")
            and not source_word.endswith("ءإ")
        ):
            char_pos = source_word.index("ءإ")
        elif (
            "ءء" in source_word
            and not source_word.startswith("ءء")
            and not source_word.endswith("ءء")
        ):
            char_pos = source_word.index("ءء")
        if char_pos != 0:
            self.edited_part1 = source_word[: char_pos + 1]
            self.edited_part2 = source_word[char_pos + 1 :]
        return [self.edited_part1, self.edited_part2]

    def read_word_list_count(self):  # read words list with count from csv file
        dataReader = DataReader()
        if dataReader.assert_exists("edited_word_count.csv"):
            return dataReader.assert_labels_exists_with_read(
                file_name="edited_word_count.csv", fields=["word", "count"]
            )
        else:
            print("Error in calling dic")

    def word_probability(self, word):  # get propapplity of target word
        N = sum(self.words_dic.values())
        return self.words_dic[word] / N

    def split_alef_of_word(
        self, word
    ):  # split source_word to replace hamza in 3 tuples with the first 3 char
        word = word.replace("[إأآا]", "ا")
        return [(word[:i], word[i:]) for i in range(3)]

    def replace_alef_of_word(
        self, word
    ):  # replace all split_alef_of_word with one edit distance from source word
        alef_letters = "إأآا"
        return [
            l + c + r[1:]
            for l, r in self.split_alef_of_word(word)
            if r
            for c in alef_letters
        ]

    def check_hamza(
        self, token
    ):  # note --this work fine with words greater than three chars
        self.words_dic = (
            self.read_word_list_count()
        )  # read words_list with its frequence
        candidates = self.replace_alef_of_word(token) or [
            token
        ]  # apply one edit distance for the first 4 chars of target word
        valid_candidates = [
            w for w in candidates if w in self.words_dic
        ]  # get all valid edit distance source_word in words_list
        if valid_candidates:
            self.edited_part1 = max(
                valid_candidates, key=self.word_probability
            )  # get source_word with max probabilty
            return self.edited_part1  # self.edited_word
        else:
            return token

    def correct_ya(
        self, token
    ):  #  check if starts with alef because if it is wrong no answer will back
        source_word = token
        self.words_dic = self.read_word_list_count()
        if source_word.endswith("ي") or source_word.endswith("ى"):
            candidates = [source_word[:-1] + "ي", source_word[:-1] + "ى"]
            valid_candidates = [w for w in candidates if w in self.words_dic]
            self.edited_part1 = max(valid_candidates, key=self.word_probability)
            return self.edited_part1  # self.edited_word

    def check_ma_intizalize(self, token):  # split_ma_intizalize
        self.words_dic = self.read_word_list_count()
        splited_word = token.split("ما") if token.startswith("ما") else token
        correct_splited_word = (
            token.replace("ما", "ما ")
            if str(splited_word[1]) in self.words_dic
            else token
        )
        self.edited_part1, self.edited_part2 = (
            correct_splited_word.split() if " " in correct_splited_word else token,
            "",
        )
        return correct_splited_word

    def check_la_intizalize(self, token):  # split_la_intizalize
        self.words_dic = self.read_word_list_count()
        splited_word = token.split("لا") if token.startswith("لا") else token
        correct_splited_word = (
            token.replace("لا", "لا ")
            if str(splited_word[1]) in self.words_dic
            else token
        )
        self.edited_part1, self.edited_part2 = (
            correct_splited_word.split() if " " in correct_splited_word else token,
            "",
        )
        return correct_splited_word

    def check_abo_intizalize(self, token):  # split_abo_intizalize
        self.words_dic = self.read_word_list_count()
        splited_word = token.split("بو") if token.startswith("بو") else token
        splited_word = token.split("أبو") if token.startswith("أبو") else token
        splited_word = token.split("ابو") if token.startswith("ابو") else token
        correct_splited_word = (
            token.replace("بو", "بو ")
            if str(splited_word[1]) in self.words_dic
            else token
        )
        correct_splited_word = (
            token.replace("أبو", "أبو ")
            if str(splited_word[1]) in self.words_dic
            else token
        )
        correct_splited_word = (
            token.replace("ابو", "ابو ")
            if str(splited_word[1]) in self.words_dic
            else token
        )
        self.edited_part1, self.edited_part2 = (
            correct_splited_word.split() if " " in correct_splited_word else token,
            "",
        )
        return correct_splited_word

    def replace_all(self, text: str, replace_dic: dict[str, str]) -> str:
        for i, j in replace_dic.items():
            text = text.replace(i, j)
        return text

    def split_custome_cases(self, token):
        replaced_word = token
        self.words_dic = self.read_word_list_count()
        custome_words_replace = {
            "اللاشئ": "لا شئ",
            "اللاشىء": "لا شىء",
            "اللاشيء": "لا شيء",
            "يالها": "يا لها",
            "ياريت": "يا ريت",
            "يامهلبية": "يا مهلبية",
            "فيما": "في ما",
            "احداهم": "احد اهم",
            "جيجاطن": "جيجا طن",
            "وثلاث": "و ثلاث",
            "جنكيزخان": "جنكيز خان",
            "بنبرك": "بن برك",
            "لاتفعل": "لا تفعل",
            "نصرالله": "نصر الله",
            "بورسعيد": "بور سعيد",
        }
        if token in custome_words_replace:
            replaced_word = self.replace_all(token, custome_words_replace)
            self.edited_part1, self.edited_part2 = replaced_word.split()
        elif not token.startswith("ة") and (
            (not token.endswith("ة") and token.count("ة") >= 1) and "ة" in token
        ):
            replaced_word = token.replace("ة", "ة ").split()
            self.edited_part1, self.edited_part2 = replaced_word[0], replaced_word[1]
        elif (
            not token.startswith("ى")
            and not token.endswith("ى")
            and "ى" in token
            and not token.endswith("ىء")
        ):
            replaced_word = token.replace("ى", "ى ").split()
            self.edited_part1, self.edited_part2 = replaced_word[0], replaced_word[1]
        elif "_" in token and token != "ـ": # Tatwil/Kashida
            self.edited_part1 = token.replace("ـ", "")
            replaced_word = token.replace("ـ", "")
        elif token.startswith("اوال"):
            replaced_word = token.replace("او", "او ").split()
            if str(replaced_word[1]) in self.words_dic:
                self.edited_part1, self.edited_part2 = replaced_word[0], replaced_word[1]
        # here I shoud distinguish between source word which has no edit and if it has edit (edit1_edit2)
        elif token.startswith("أوال"):
            replaced_word = token.replace("أو", "أو ").split()
            if str(replaced_word[1]) in self.words_dic:
                self.edited_part1, self.edited_part2 = replaced_word[0], replaced_word[1]
        elif token.startswith("عبدال"):
            replaced_word = token.replace("عبد", "عبد ").split()
            if str(replaced_word[1]) in self.words_dic:
                self.edited_part1, self.edited_part2 = replaced_word[0], replaced_word[1]
        elif token.startswith("فخرال"):
            replaced_word = token.replace("فخر", "فخر ").split()
            if str(replaced_word[1]) in self.words_dic:
                self.edited_part1, self.edited_part2 = replaced_word[0], replaced_word[1]
        return replaced_word
