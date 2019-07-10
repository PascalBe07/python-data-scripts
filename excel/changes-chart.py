#!/usr/bin/env python3

from argparse import ArgumentParser
from openpyxl import load_workbook
from openpyxl.chart import (LineChart, Reference)

# arguments of the script
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="file to read", metavar="FILENAME", default="testfile.xlsx")
parser.add_argument("-s", "--sheetname", dest="sheetname",
                    help="sheet to read", metavar="SHEETNAME")
parser.add_argument("-t", "--targetsheet", dest="targetsheet",
                    help="sheet to write the result to", metavar="TARGETSHEET")
parser.add_argument("-r", "--sourcerownumber", dest="sourcerow", required=True,
                    help="row number to use for the chart", metavar="SOURCEROWNUMBER")
args = parser.parse_args()
sheetname = args.sheetname
filename = args.filename
targetsheet = args.targetsheet
sourceRowNumber = int(args.sourcerow)

# get excel sheet to read from
workbook = load_workbook(filename)
readingWorksheet = workbook[workbook.sheetnames[0]] if sheetname == None else workbook[sheetname]

# create excel sheet to write to
newWorksheetName = "changes-as-chart" if targetsheet == None else targetsheet
# remove worksheet, if it already exists
if newWorksheetName in workbook.sheetnames:
    workbook.remove(workbook[newWorksheetName])
# create sheet from scratch
writingWorksheet = workbook.create_sheet(newWorksheetName)

# get required data
rowList = list(readingWorksheet.rows)
headerRow = rowList[0][1:]
dataRow = rowList[sourceRowNumber-1][1:]
columnNumber = len(headerRow)


# write values for chart to a sheet, so that table can reference these values
for (index, column) in enumerate(headerRow):
    writingWorksheet.cell(1, index+1, column.value)
    writingWorksheet.cell(2, index+1, 0)
    writingWorksheet.cell(3, index+1, dataRow[index].value)


chart = LineChart()
chart.title = "Relative Changes as chart"
chart.style = 13
chart.y_axis.title = "Relative Change"
chart.x_axis.title = "Time"
chartData = Reference(writingWorksheet, min_col=1, min_row=1, max_col=columnNumber+1, max_row=3)

writingWorksheet.add_chart(chart, "A5")


workbook.save(filename)
