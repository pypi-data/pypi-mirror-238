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


"""Collection of open source Python modules for Arabic language processing developed by Bibliotheca Alexandrina.
"""
import os

try:
    with open(os.path.join(os.path.dirname(__file__),'VERSION')) as version_file:
        __version__ = version_file.read().strip()
except NameError:
    __version__ = "unknown (running code interactively?)"
except OSError as ex:
    __version__ = "unknown (%s)" % ex