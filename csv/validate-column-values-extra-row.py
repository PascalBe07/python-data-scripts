#!/usr/bin/env python3
import csv
from argparse import ArgumentParser
import json

existing_filename = "sample.csv"
new_filename = "new." + existing_filename

id_field = "record_id"
time_field = "redcap_event_name"
metric_identifier = "m"
number_identifier = "n"

skip_empty_values = True
check_only = True

metric_columns = []
number_columns = []

wrong_entry_count = 0
fieldnames = []
all_rows = []
second_row = None

with open(existing_filename, "r") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

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

                    if not check_only:
                        new_value = input("Replace value? Enter new one or press enter")
                        if new_value:
                            row[key] = new_value

            if str(key) in number_columns:
                try:
                    converted_value = int(value)
                except ValueError:
                    print(row[id_field] + " / " + row[time_field] + "\t" +
                          key + "\t\"" + value + "\".")
                    wrong_entry_count = wrong_entry_count + 1

                    if not check_only:
                        new_value = input("Replace value? Enter new one or press enter")
                        if new_value:
                            row[key] = new_value
        all_rows.append(row)

if not check_only:
    with open(new_filename, "w") as f2:
        writer = csv.DictWriter(f2, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(second_row)

        for row in all_rows:
            writer.writerow(row)

print("In total " + str(wrong_entry_count) + " fields were not so nice.")
