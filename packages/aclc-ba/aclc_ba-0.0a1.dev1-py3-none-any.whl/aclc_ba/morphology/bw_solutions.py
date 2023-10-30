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

"""This module contains utilities for getting morphological analysis solutions from buckwalter job.
"""

from aclc_ba.utils.data_reader import DataReader
import subprocess
from aclc_ba.morphology.word_solution import WordSolution


class BwSolution:
    def __init__(self) -> None:  # here we will take token_list or one token
        """Initialize a BwSolution for getting morpholoical solutions from builtin bw app.
        word (str): The shared vocabulary.
        """
        self.data_reader = DataReader()
        self.bw_path = self.data_reader.assert_exists()

    def analyze_words_bw(
        self, words_list: list[str] = None
    ) -> list[list[WordSolution]]:
        self.run_bw(words_list)
        if isinstance(words_list, str):
            words_list = [words_list]
        return list(map(lambda w: self.get_bw_dis_solution_of_word(w), words_list))

    def write_to_bw(
        self, words_list: list[str]
    ) -> None:  # write word to buckwalter input file
        in_file_path = self.data_reader.assert_exists(
            str(self.bw_path) + "/Buckwalter/data/in.txt"
        )
        if in_file_path:
            with open(in_file_path, "w", encoding="utf-8") as f:
                if isinstance(words_list, str):
                    words_list = [words_list]
                f.write("\n".join(words_list))
            return in_file_path
        else:
            print("I can not write in BW in.txt file")

    def run_bw(self, words_list: list[str]):
        in_file_path = self.write_to_bw(
            words_list
        )  # create subprocess to run perl file of BW
        in_file_path = str(in_file_path)
        perl_file_path = self.data_reader.assert_exists(
            str(self.bw_path) + "/Buckwalter/data/AraMorph.pl"
        )
        perl_file_path = str(perl_file_path)
        path_to_write_solutions = self.data_reader.assert_exists(
            str(self.bw_path) + "/Buckwalter/data/bw_solutions_out.csv"
        )
        with open(path_to_write_solutions, "w", encoding="utf-8") as fout:
            subprocess.run(
                ["perl", "-w", perl_file_path, in_file_path], stdout=fout, shell=True
            )

    def read_word_morpholgical_solutions_bw(
        self,
    ):  # read words solution from buckwalter out file
        dataReader = DataReader()
        if dataReader.assert_exists(
            str(self.bw_path) + "/Buckwalter/data/bw_solutions_out.csv"
        ):
            return dataReader.assert_labels_exists_with_read(
                file_name=str(self.bw_path) + "/Buckwalter/data/bw_solutions_out.csv",
                fields=[
                    "word",
                    "root",
                    "stem_pattern",
                    "lemmaid",
                    "voc",
                    "pr",
                    "stem",
                    "suf",
                    "gloss",
                ],
            )
        else:
            print("Error in calling dic")

    def get_bw_dis_solution_of_word(
        self, searched_word: str
    ) -> list[WordSolution]:  # get all analysis solution from bw out file
        solutions = []
        for (
            word,
            solutions_from_dic,
        ) in self.read_word_morpholgical_solutions_bw().items():
            if word == searched_word:
                for sol in solutions_from_dic:
                    sol["word"] = word
                    if "/" in sol["stem"]:
                        sol["stem"], sol["tag"] = sol["stem"].split("/", 1)
                    else:
                        sol["stem"], sol["tag"] = "", ""
                    if "+" in sol["pr"]:
                        sol["pr1"], sol["pr2"], sol["pr3"] = sol["pr"].split("+")
                    else:
                        sol["pr1"] = sol["pr"]
                    if "+" in sol["suf"]:
                        sol["suf1"], sol["suf2"] = sol["suf"].split("+")
                        if sol["suf1"] == "AF/NOUN":
                            sol["suf1"] = sol["suf1"].replace("AF/NOUN", "")
                    else:
                        sol["suf1"] = sol["suf"]
                    if "/NEG_PART" in sol["stem"]:
                        sol["suf1"], sol["suf2"] = "", ""
                    solutions.append(vars(WordSolution(sol)))
        return solutions