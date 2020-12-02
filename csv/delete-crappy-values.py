#!/usr/bin/env python3

import csv
from argparse import ArgumentParser
import json

existing_filename = "sample.csv"
new_filename = "new." + existing_filename

crappy_values = ["see comments", "na", "not asked", "see comment section below", "Not assessed."]

id_field = "record_id"
time_field = "timepoint"

bad_cells = []

all_rows = []
fieldnames = []

with open(existing_filename, "r") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        for key, value in row.items():
            for crappy_value in crappy_values:
                if value.lower() == crappy_value.lower():
                    bad_cells.append({
                        "subject": row[id_field],
                        "timepoint": row[time_field],
                        "column": key,
                        "value": value
                    })

        all_rows.append(row)

with open(new_filename, "w", newline='') as f2:
    writer = csv.DictWriter(f2, fieldnames=fieldnames)
    writer.writeheader()

    for row in all_rows:
        for cell in bad_cells:
            if row[id_field] == cell["subject"] and row[time_field] == cell["timepoint"]:
                row[cell["column"]] = None

        writer.writerow(row)

for cell in bad_cells:
    print(cell["subject"] + " / " + cell["timepoint"] + "\t" + cell["column"] + "\t\"" + cell["value"] + "\".")

print(str(len(bad_cells)) + " values recognized, which can be deleted.")
