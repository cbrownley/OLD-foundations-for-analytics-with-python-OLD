#!/usr/bin/python
"""
Copyright 2014 Clinton W. Brownley
Available at https://github.com/cbrownley
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
import csv
import sys
import xlrd

input_file = sys.argv[1]
#output_file = sys.argv[2]

with xlrd.open_workbook(input_file) as workbook:
	#with open(output_file, 'wb') as csv_out_file:
		#filewriter = csv.writer(csv_out_file, delimiter=',')
		worksheet = workbook.sheet_by_name('january_2013')
		for row_index in range(worksheet.nrows):
			if row_index > 0:
				amount = worksheet.cell_value(row_index,3)
				if amount > 1400.0:
					print worksheet.row_values(row_index)
					#filewriter.writerow(worksheet.row_values(row_index))
				else:
					pass
			else:
				print worksheet.row_values(row_index)
				#filewriter.writerow(worksheet.row_values(row_index))