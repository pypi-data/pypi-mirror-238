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

"""This module contains utilities for handling csv files and return data.
"""

from pathlib import Path
import csv
import itertools


class DataReader:
    def assert_exists(self, file_name: str = "") -> str:
        file_name_path = (
            Path.cwd() / "aclc_ba/utils" / file_name
        )  # call in the dir of aclc_ba
        file_name_path = file_name_path.resolve()
        if file_name_path.exists():
            return file_name_path

    def assert_labels_exists_with_read(self, **kwargs) -> dict:
        file_name_path = DataReader.assert_exists(kwargs["file_name"])
        file_name_path = Path.joinpath(file_name_path, str(kwargs["file_name"]))
        file_name_path = file_name_path.resolve()
        with open(file_name_path, "r", encoding="utf-8-sig") as csvfile:
            csv_test_bytes = csvfile.read(
                1024
            )  # Grab a sample of the CSV for format detection.
            csvfile.seek(0)  # Rewind
            has_header = csv.Sniffer().has_header(
                csv_test_bytes
            )  # Check to see if there's a header in the file.
            dialect = csv.Sniffer().sniff(
                csv_test_bytes
            )  # Check what kind of csv/tsv file we have.
            inputreader = csv.DictReader(csvfile, dialect=dialect)
            return_data_dic = {}
            if has_header:
                i = inputreader.fieldnames
                if kwargs["fields"] == i:
                    for row in inputreader:
                        if kwargs["file_name"] == "edited_word_count.csv":
                            return_data_dic[row["word"].strip()] = int(row["count"])
                        else:
                            self.read_list_values_of_one_key(
                                return_data_dic,
                                row["word"],
                                dict(
                                    itertools.islice(
                                        row.items(), 1, len(kwargs["fields"])
                                    )
                                ),
                            )
                else:
                    print("error in fields matching")
            return return_data_dic

    def read_list_values_of_one_key(self, data_dic, key, value):
        if key not in data_dic:
            data_dic[key] = [value]
        elif isinstance(data_dic[key], list):
            data_dic[key].append(value)
        else:
            data_dic[key] = [data_dic[key], value]
