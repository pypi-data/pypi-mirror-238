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

"""This module contains utilities for getting morphological analysis solutions from db.csv file.
"""

from aclc_ba.utils.data_reader import DataReader
from aclc_ba.morphology.word_solution import WordSolution

"""This module contains utilities for morphological analysis solutions from builtin db.
"""


class DbAnalyzedBased:
    def __init__(
        self, file_path: str = "dis_tag_lemma_logprop.csv"
    ) -> None:  # here we will take token_lst or one token
        """Initialize a wordsolutions for getting morpholoical solutions from builtin db.
        #word (str): The shared vocabulary.
        """
        self.word_morphogical_solutions_db = self.read_word_morpholgical_solutions_db()

    def analyze(self, word: str = ""):
        return self.get_dis_solution_of_word(word)

    def analyze_words(self, words: list[str] = None) -> list[list[WordSolution]]:
        return list(map(lambda w: self.analyze(w), words))

    def read_word_morpholgical_solutions_db(
        self,
    ):  # read words solution dictionary with count from csv file
        dataReader = DataReader()
        if dataReader.assert_exists("dis_tag_lemma_logprop.csv"):
            return dataReader.assert_labels_exists_with_read(
                file_name="dis_tag_lemma_logprop.csv",
                fields=[
                    "word",
                    "lemmaid",
                    "pr1",
                    "pr2",
                    "pr3",
                    "stem",
                    "stems",
                    "tags",
                    "suf1",
                    "suf2",
                    "gen",
                    "num",
                    "arabic_stem",
                    "root",
                    "stem_Pattern",
                    "tag_statistics",
                    "lemma_statistics",
                    "tag_lemma_statistics",
                ],
            )
        else:
            print("Error in calling dic")

    def get_dis_solution_of_word(
        self, searched_word: str
    ) -> list[WordSolution]:  # get all analysis solution from db
        solutions = []
        for word, solutions_from_dic in self.word_morphogical_solutions_db.items():
            if word == searched_word:
                for sol in solutions_from_dic:
                    sol["word"] = word
                    if "/" in sol["stem"]:
                        sol["stem"], sol["tag"] = sol["stem"].split("/", 1)
                    solutions.append(vars(WordSolution(sol)))
        return solutions
