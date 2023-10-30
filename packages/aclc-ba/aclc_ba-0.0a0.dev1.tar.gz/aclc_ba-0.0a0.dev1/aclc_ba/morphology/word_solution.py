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


"""This module contains utilities for morphological analysis solutions.
"""
from typing import Dict


class WordSolution:
    def __init__(self, initial_data: Dict[str, str] = None) -> None:
        self.word = initial_data.get("word", "")
        self.lemmaid = initial_data.get("lemmaid", "")
        self.pr1 = initial_data.get("pr1", "")
        self.pr2 = initial_data.get("pr2", "")
        self.pr3 = initial_data.get("pr3", "")
        self.stem = initial_data.get("stem", "")
        self.suf1 = initial_data.get("suf1", "")
        self.suf2 = initial_data.get("suf2", "")
        self.gen = initial_data.get("gen", "")
        self.num = initial_data.get("num", "")
        self.arabic_stem = initial_data.get("arabic_stem", "")
        self.root = initial_data.get("root", "")
        self.tag_statistics = initial_data.get("tag_statistics", "0.0")
        self.lemma_statistics = initial_data.get("lemma_statistics", "0.0")
        self.tag_lemma_statistics = initial_data.get("tag_lemma_statistics", "0.0")
        self.stems = ""
        self.tags = initial_data.get("tag", "")
        self.stem_Pattern = ""

