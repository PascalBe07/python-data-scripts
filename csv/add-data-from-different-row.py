#!/usr/bin/env python3
import csv
from argparse import ArgumentParser
import json

existing_filename = "sample.csv"
new_filename = "new." + existing_filename

id_field = "record_id"
time_field = "time"
new_field = "age"
specific_time_fields = ["T1", "T2", "T3"]

all_entities = {}
all_rows = []
headers = []


with open(existing_filename, "r") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames

    for row in reader:
        all_rows.append(row)
        id_value = row[id_field]

        if id_value not in all_entities:
            all_entities[id_value] = {}

        for specific_time_field in specific_time_fields:
            if row[specific_time_field]:
                if specific_time_field in all_entities[id_value]:
                    raise ValueError(id_value + " has " + specific_time_field + " multiple times.")
                all_entities[id_value][specific_time_field] = row[specific_time_field]


with open(new_filename, 'w', newline='') as f2:
    newFieldnames = reader.fieldnames
    newFieldnames.append(new_field)

    for specific_time_field in specific_time_fields:
        newFieldnames.remove(specific_time_field)

    writer = csv.DictWriter(f2, fieldnames=newFieldnames)
    writer.writeheader()

    for row in all_rows:
        id_value = row[id_field]
        time_value = row[time_field]
        if time_value in all_entities[id_value]:
            row[new_field] = all_entities[id_value][time_value]
        else:
            print("No " + time_value + " for " + id_value)

        for specific_time_field in specific_time_fields:
            del row[specific_time_field]

        writer.writerow(row)
