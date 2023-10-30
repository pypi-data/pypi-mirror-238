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

"""This module contains utilities for getting all morphological analysis solutions.
"""
from aclc_ba.morphology.bw_solutions import BwSolution
from aclc_ba.morphology.db_analyzer_based import DbAnalyzedBased
from aclc_ba.utils.translitration import MAP_TRANSLITERATION

class Analysis:
    def __init__(self, words_list: str):
        if isinstance(words_list, str):
            words_list = [words_list]
        self.words_list = words_list
        self.morphology_analysis = self.combine_analysis()
        self.tokenized_analysis = []

    def combine_analysis(self):
        bw = BwSolution()
        bw = bw.analyze_words_bw(self.words_list)
        db = DbAnalyzedBased(self.words_list)
        db = db.get_dis_solution_of_word(self.words_list)
        return db + bw

    def replace_all(self, text: str, replace_dic: dict[str, str]) -> str:
        for i, j in replace_dic.items():
            text = text.replace(i, j)
        return text

    #  maybe static method
    def translitrate_analysis(self):  # tranliterate from buckwalter to Arabic
        sol_list_lists = self.morphology_analysis
        for sol_list in sol_list_lists:
            for sol in sol_list:
                print(sol)
                pr1 = self.replace_all(sol["pr1"], MAP_TRANSLITERATION)
                pr2 = self.replace_all(sol["pr2"], MAP_TRANSLITERATION)
                pr3 = self.replace_all(sol["pr3"], MAP_TRANSLITERATION)
                stem = self.replace_all(sol["stem"], MAP_TRANSLITERATION)
                suf1 = sol["suf1"].split("/")[0]
                suf1 = self.replace_all(suf1, MAP_TRANSLITERATION)
                suf2 = self.replace_all(sol["suf2"], MAP_TRANSLITERATION)
                tokenized = [pr1, pr2, pr3, stem, suf1, suf2]
                tokenized = [segment for segment in tokenized if segment.strip()]
                if tokenized not in self.tokenized_analysis:
                    self.tokenized_analysis.append(tokenized)
        return self.tokenized_analysis
