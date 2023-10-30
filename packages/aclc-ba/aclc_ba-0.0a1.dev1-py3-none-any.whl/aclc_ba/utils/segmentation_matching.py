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

"""This module contains utilities for word and clean text for tokenization.
"""
import re

NEGATIVE_NUMBERS = re.compile(r"\w+-?[0-9]+(?:(\.|\,)[0-9]+)?\w+")
URL_MATCH = re.compile(r'((?:<a href=")?https?://\S+[^\s,.:;])')
EMAIL_MATCH = re.compile(r"^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$")
ARABIC_DIACRATICS_MATCH = re.compile(
    """ ّ    | # Tashdid
                        َ    | # Fatha
                        ً    | # Tanwin Fath
                        ُ    | # Damma
                        ٌ    | # Tanwin Damm
                        ِ    | # Kasra
                        ٍ    | # Tanwin Kasr
                        ْ    | # Sukun
                    """,
    re.VERBOSE,
)


UNICODE_INTERGER_LIST = frozenset(
    [
        chr(10),
        chr(13),
        chr(28),
        chr(29),
        chr(30),
        chr(31),
        chr(157),
        chr(158),
        chr(160),
        chr(253),
        chr(254),
        chr(240),
        chr(241),
        chr(243),
        chr(245),
        chr(246),
        chr(8206),
        chr(248),
        chr(250),
        chr(1611),
        chr(1612),
        chr(1613),
        chr(1614),
        chr(1616),
        chr(8207),
        chr(1615),
        chr(1617),
        chr(1618),
        chr(15),
        chr(3),
        chr(17),
        chr(22),
        chr(27),
        chr(2),
        chr(26),
        chr(1),
        chr(4),
        chr(21),
        chr(16),
        chr(14),
        chr(8204),
        chr(8205),
    ]
)
INVALIDCHARS = frozenset(
    [
        "/",
        "'",
        "'",
        "...",
        '"',
        "#",
        "&",
        "$",
        "%",
        "?",
        "؟",
        "=",
        "+",
        "%",
        "_",
        "^",
        "*",
        "•",
        "`",
        "‘",
        "’",
        ";",
        "؛",
        ":",
        "»",
        "«",
        "”",
        "“",
        "{",
        "}",
        "[",
        "]",
        "\\",
        "|",
        ">",
        "<",
        "(",
        ")",
        "!",
        ".",
        "،",
        ",",
        "-",
        "—",
        "¯",
        "…",
        "ـ",
    ]
)

CHECK_IN_WORD_OR_LINE = frozenset(["/", "-", ".", "،", ",", ":"])
