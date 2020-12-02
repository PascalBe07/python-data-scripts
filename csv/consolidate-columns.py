#!/usr/bin/env python3
import csv
from argparse import ArgumentParser
import json

existing_filename = "real_sample.csv"
new_filename = "new." + existing_filename

id_field = "record_id"
consolidateable_column_identifiers = ["C_", "S_"]

generic_columns = {}
fieldnames = []
all_rows = []

with open(existing_filename, "r") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for fieldname in fieldnames:
        for column_identifier in consolidateable_column_identifiers:
            if fieldname.startswith(column_identifier):
                generic_fieldname = fieldname[2:]
                if generic_fieldname not in generic_columns:
                    generic_columns[generic_fieldname] = [fieldname]
                else:
                    generic_columns[generic_fieldname].append(fieldname)

    for row in reader:
        all_rows.append(row)


with open(new_filename, 'w', newline='') as f2:
    extra_fieldnames = []

    for key, value in generic_columns.items():
        if len(value) > 1:
            extra_fieldnames.append(key)

    print(extra_fieldnames)

    new_fieldnames = fieldnames + extra_fieldnames

    writer = csv.DictWriter(f2, fieldnames=new_fieldnames)
    writer.writeheader()

    for row in all_rows:

        for key, value in generic_columns.items():
            if len(value) > 1:
                generic_column_value = None
                for specialized_column in value:
                    specialized_column_value = row[specialized_column]
                    if specialized_column_value != "" and specialized_column_value != None:
                        print(specialized_column, specialized_column_value)
                        if generic_column_value:
                            raise ValueError("The new column \"" + key +
                                             "\" has more than one source column: " + ",".join(value) + " for \"" + row[id_field] + "\".")
                        generic_column_value = specialized_column_value

                row[key] = generic_column_value

        writer.writerow(row)
