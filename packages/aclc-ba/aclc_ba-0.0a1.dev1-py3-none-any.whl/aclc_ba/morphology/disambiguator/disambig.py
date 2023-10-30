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

"""This module contains utilities for disambiguate morphological analysis solutions based on different language models.
"""
from aclc_ba.morphology.bw_solutions import BwSolution
from aclc_ba.utils.data_reader import DataReader


class Disambig:
    def __init__(self):
        self.db_solutions = {}
        pass

    def bw_solutions(self, word):
        bw = BwSolution()
        bw = bw.analyze_words_bw(word)
        return bw

    def statistical_model(self, words_list, language_model, key=""):
        if isinstance(words_list, str):
            words_list = [words_list]
        words_list = words_list
        if language_model == "freq":
            file = "freq_lemma_tag.csv"
            self.db_solutions = self.read_word_morpholgical_solutions_lm(file)
            if key == "tag":
                analysis = [self.get_top_tag(word, file) for word in words_list]
            elif key == "lemma":
                analysis = [self.get_top_lemma(word, file) for word in words_list]
        elif(language_model == "prop"):
            file = "sol_tag_lemma_pro.csv"
            self.db_solutions = self.read_word_morpholgical_solutions_lm(file)
            if key == "tag":
                analysis = [self.get_top_tag(word, file) for word in words_list]
            elif key == "lemma":
                analysis = [self.get_top_lemma(word, file) for word in words_list]
        elif(language_model == "logprop"):
            file = "dis_tag_lemma_logprop.csv"
            self.db_solutions = self.read_word_morpholgical_solutions_lm(file)
            if key == "tag":
                analysis = [self.get_top_tag(word, file) for word in words_list]
            elif key == "lemma":
                analysis = [self.get_top_lemma(word, file) for word in words_list]
            elif key == "tag_lemma":
                analysis = [self.get_top_tag_lemma(word, file) for word in words_list]
        else:
            print("Please pass model name")
        return analysis

    def read_word_morpholgical_solutions_lm(
        self, file
    ):  # read words solution from LM file
        dataReader = DataReader()
        if dataReader.assert_exists(file):
            self.db_solutions =  dataReader.assert_labels_exists_with_read(
                file_name=file,
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
            return self.db_solutions
        else:
            print("Error in calling dic")

    def get_solutions_of_lemma_tag(
        self, bw_sol
    ):
        for (
            word, solutions_from_dic
        ) in self.db_solutions.items():
            for solution in  solutions_from_dic:
                if solution['lemmaid'] == bw_sol['lemmaid'] and solution['tags'] == bw_sol['tags']:
                    bw_sol['tag_lemma_statistics'] = solution['tag_lemma_statistics']
                    bw_sol
        return  bw_sol

    def get_solutions_of_word(
        self, searched_word: str, file
    ):  # get all analysis solution from bw out file #pass one word
        solutions = []
        has_no_solutions = True
        for (
            word,
            solutions_from_dic,
        ) in self.db_solutions.items():
            if word == searched_word:
                for sol in solutions_from_dic:
                    sol["word"] = word
                    solutions.append(sol)
                    has_no_solutions = False
                    return solutions
        if has_no_solutions:
            bw_sols = self.bw_solutions(searched_word)
            if len(bw_sols[0]) == 0:
                return []
            if len(bw_sols[0]) == 1 and ('x' in bw_sols[0][0]['lemmaid'] or 'X' in bw_sols[0][0]['lemmaid'] ): # have one solution with lemma 'xxx'
                return bw_sols[0]
            bw_sols = [self.get_solutions_of_lemma_tag(bw_sol) for bw_sol in bw_sols[0]]# مليئ 
        return bw_sols

    def get_top_tag(self, word, file):
        if isinstance(word, list):
            top_solution_with_tag = [self.get_top_tag(word_in_list,file) for word_in_list in word]
            return top_solution_with_tag
        solutions = self.get_solutions_of_word(word, file)
        if solutions:
            top_solution_with_tag = max(solutions, key=lambda x: float(x["tag_statistics"]))
            return top_solution_with_tag
        else:
            print("No solutions")

    def get_top_lemma(self, word, file):
        solutions = self.get_solutions_of_word(word, file)
        top_solution_with_lemma = max(solutions, key=lambda x: float(x["lemma_statistics"]))
        return top_solution_with_lemma
    
    def get_top_tag_lemma(self, word, file):
        if isinstance(word, list):
            top_solution_with_ta_lemma = [self.get_top_tag_lemma(word_in_list,file) for word_in_list in word]
            return top_solution_with_ta_lemma
        solutions = self.get_solutions_of_word(word, file)
        top_solution_with_ta_lemma = max(solutions, key=lambda x: float(x["tag_lemma_statistics"]))
        return top_solution_with_ta_lemma
