#!/usr/bin/python
"""
Copyright 2014 Clinton W. Brownley
Available at https://github.com/cbrownley
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
import csv
import glob
import os
import string
import sys
from datetime import date
from xlrd import open_workbook, xldate_as_tuple

item_numbers_file = sys.argv[1]
path_to_folder = sys.argv[2]
output_file = sys.argv[3]

item_numbers_to_find = []
with open(item_numbers_file, 'rU') as item_numbers_csv_file:
	filereader = csv.reader(item_numbers_csv_file)
	for row in filereader:
		item_numbers_to_find.append(row[0])
print item_numbers_to_find

filewriter = csv.writer(open(output_file, 'ab'))

file_counter = 0
line_counter = 0
count_of_item_numbers = 0
for input_file in glob.glob(os.path.join(path_to_folder, '*.*')):
	file_counter += 1
	if input_file.split('.')[1] == 'csv':
		with open(input_file, 'rU') as csv_in_file:
			filereader = csv.reader(csv_in_file)
			header = next(filereader, None)
			for row in filereader:
				row_of_output = []
				for column in range(len(header)):
					if column < 3:
						cell_value = str(row[column]).strip()
						row_of_output.append(cell_value)
					elif column == 3:
						cell_value = str(row[column]).lstrip('$').replace(',','').split('.')[0].strip()
						row_of_output.append(cell_value)
					else:
						cell_value = str(row[column]).strip()
						row_of_output.append(cell_value)
				row_of_output.append(os.path.basename(input_file))
				if row[0] in item_numbers_to_find:
					filewriter.writerow(row_of_output)
					count_of_item_numbers += 1
				line_counter += 1
	elif input_file.split('.')[1] == 'xls' or input_file.split('.')[1] == 'xlsx':
		workbook = open_workbook(input_file)
		for worksheet in workbook.sheets():
			try:
				header = worksheet.row_values(0)
			except IndexError:
				pass
			for row in range(1, worksheet.nrows):
				row_of_output = []
				for column in range(len(header)):
					if column < 3:
						cell_value = str(worksheet.cell_value(row,column)).strip()
						row_of_output.append(cell_value)
					elif column == 3:
						cell_value = str(worksheet.cell_value(row,column)).split('.')[0].strip()
						row_of_output.append(cell_value)
					else:
						cell_value = xldate_as_tuple(worksheet.cell(row,column).value,workbook.datemode)
						cell_value = str(date(*cell_value[0:3])).strip()
						row_of_output.append(cell_value)
				row_of_output.append(os.path.basename(input_file))
				row_of_output.append(worksheet.name)
				if str(worksheet.cell(row,0).value).split('.')[0].strip() in item_numbers_to_find:
					filewriter.writerow(row_of_output)
					count_of_item_numbers += 1
				line_counter += 1
print 'Number of files:', file_counter
print 'Number of lines:', line_counter
print 'Number of item numbers', count_of_item_numbers