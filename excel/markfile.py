#!/usr/bin/env python3

from argparse import ArgumentParser
from openpyxl import load_workbook

# arguments of the script
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="file to read", metavar="FILENAME", default="testfile.xlsx")
parser.add_argument("-s", "--sheetname", dest="sheetname",
                    help="sheet to read", metavar="SHEETNAME")
args = parser.parse_args()
sheetname = args.sheetname
filename = args.filename

# get all cells
workbook = load_workbook(filename)
worksheet = workbook.active if sheetname == None else workbook[sheetname]
rowList = list(worksheet.rows)
allCells = list(sum(rowList, ()))

# filter cells
matchingCells = [x for x in allCells if isinstance(
    x.value, int) and (x.value > 99)]
print(str(len(matchingCells)) + ' matching cells.')

# run specific code for cell


def conditionalCode(cell):
    print(cell, cell.value, type(cell.value))
    # cell.style = 'Accent2'


[conditionalCode(x) for x in matchingCells]

# print('Saving file')
# workbook.save(filename)
