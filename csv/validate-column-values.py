#!/usr/bin/env python3
import csv
from argparse import ArgumentParser
import json

existing_filename = "real_sample.csv"
new_filename = "new." + existing_filename

id_field = "record_id"
metric_identifier = "[m]"
boolean_identifier = "[b]"


skip_empty_values = True


with open(existing_filename, "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        for key, value in row.items():
            if not value and skip_empty_values:
                continue

            if str(key).startswith(metric_identifier):
                try:
                    converted_value = int(value)
                except ValueError:
                    print("Column " + key + " of subject " +
                          row[id_field] + " is not a number as expected. It is \"" + value + "\".")

            elif str(key).startswith(boolean_identifier):
                try:
                    converted_value = int(value)
                    if converted_value != 0 and converted_value != 1:
                        raise ValueError("Not 0 / 1")
                except ValueError:
                    print("Column " + key + " of subject " +
                          row[id_field] + " is not a 0 / 1 as expected. It is \"" + value + "\".")
