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

from aclc_ba.utils.segmentation_matching import URL_MATCH
from aclc_ba.utils.segmentation_matching import EMAIL_MATCH
from aclc_ba.utils.segmentation_matching import CHECK_IN_WORD_OR_LINE
from aclc_ba.utils.segmentation_matching import INVALIDCHARS
from typing import Tuple


class SentenceMarkup:
    def __init__(self, text: str = "") -> None:
        self.text = text
        self.splited_paragraphs_with_markup = []
        self.title = None
        self.paragraphs = []
        self.sentences_len = None
        self.paragraphs_max_len = None
        self.markup_text()

    def replace_all(self, text: str, replace_dic: dict[str, str]) -> str:
        for i, j in replace_dic.items():
            text = text.replace(i, j)
        return text

    def get_paragraph_with_max_len(self) -> Tuple[int, str]:
        max_paragraph = max(self.paragraphs, key=len, default=0)
        return self.paragraphs_max_len, max_paragraph

    def sentencizer_without_markup(self) -> list[str]:
        markups = ["/D", "/T", "T/", "/P", "P/", "D/"]
        return list(
            filter(lambda s: s not in markups, self.splited_paragraphs_with_markup)
        )

    def markup_text(self) -> None:
        lines = self.text
        lines = lines.splitlines()
        fstLine = True
        for i, line in enumerate(lines):
            if fstLine and line:
                first = next(s for s in lines if s)
                if (
                    any(c in line for c in CHECK_IN_WORD_OR_LINE)
                    and URL_MATCH.search(line) == None
                    and EMAIL_MATCH.search(line) == None
                ):
                    rep = {
                        "-": " - ",
                        ".": " . ",
                        "،": " ، ",
                        ",": " , ",
                        "  ": " ",
                        "   ": " ",
                        "= =": "==",
                        "- -": "--",
                        "… …": "……",
                        ". .": "..",
                        ":": " : ",
                    }
                    line = self.replace_all(first, rep)
                    first = line
                self.title = first
                self.splited_paragraphs_with_markup.extend(["/D", "/T", first, "T/"])
                fstLine = False
            elif fstLine == False and line.strip() != "":
                for s in INVALIDCHARS:
                    if (
                        s != "-"
                        and s != ","
                        and s != "'"
                        and s != "..."
                        and s != "."
                        and s != "،"
                        and URL_MATCH.search(line) == None
                        and EMAIL_MATCH.search(line) == None
                    ):
                        line = line.replace(s, " " + s + " ")
                    elif s == "'":
                        line = line.replace(s, '"')
                if (
                    any(c in line for c in CHECK_IN_WORD_OR_LINE)
                    and URL_MATCH.search(line) == None
                    and EMAIL_MATCH.search(line) == None
                ):
                    rep_not_invalide = {"-": " - ", ".": " . ", "،": " ، ", ",": " , "}
                    line = self.replace_all(line, rep_not_invalide)
                rep_not_firat_line = {
                    "  ": " ",
                    "    ": " ",
                    "= =": "==",
                    "- -": "--",
                    "… …": "……",
                    ". .": "..",
                }
                line = self.replace_all(line, rep_not_firat_line)
                self.paragraphs.extend([line])
                self.splited_paragraphs_with_markup.extend(["/P", line, "P/"])
        self.sentences_len = len(self.paragraphs) + 1
        self.splited_paragraphs_with_markup.extend(["D/"])
        self.paragraphs_max_len = (
            len((max(self.paragraphs, key=len)).split()) if self.paragraphs else 0
        )
