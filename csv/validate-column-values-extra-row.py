#!/usr/bin/env python3
import csv
from argparse import ArgumentParser
import json

existing_filename = "sample.csv"
new_filename = "new." + existing_filename

id_field = "record_id"
time_field = "time"
metric_identifier = "m"
number_identifier = "n"

skip_empty_values = True

metric_columns = []
number_columns = []

wrong_entry_count = 0

with open(existing_filename, "r") as f:
    reader = csv.DictReader(f)

    second_row = next(reader)

    for key, value in second_row.items():
        if value == metric_identifier:
            metric_columns.append(key)
        elif value == number_identifier:
            number_columns.append(key)

    for row in reader:
        for key, value in row.items():
            if (not value or not value.strip()) and skip_empty_values:
                continue

            if str(key) in metric_columns:
                try:
                    converted_value = float(value)
                except ValueError:
                    print(row[id_field] + " / " + row[time_field] + "\t" +
                          key + "\t\"" + value + "\".")
                    wrong_entry_count = wrong_entry_count + 1

            if str(key) in number_columns:
                try:
                    converted_value = int(value)
                except ValueError:
                    print(row[id_field] + " / " + row[time_field] + "\t" +
                          key + "\t\"" + value + "\".")
                    wrong_entry_count = wrong_entry_count + 1

print("In total " + str(wrong_entry_count) + " fields are not so nice.")
