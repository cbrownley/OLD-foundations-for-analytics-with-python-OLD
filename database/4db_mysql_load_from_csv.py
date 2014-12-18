#!/usr/bin/python
"""
Copyright 2014 Clinton W. Brownley
Available at https://github.com/cbrownley
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
import csv
import MySQLdb
import sys
from string import strip

# Path to and name of a CSV input file
input_file = sys.argv[1]

# Connect to a MySQL database
con = MySQLdb.connect(host='localhost', port=3306, db='my_suppliers', user='python_training', passwd='python_training')
c = con.cursor()

# Read the CSV file
# Insert the data into the Suppliers table
file_reader = csv.reader(open(input_file, 'r'), delimiter=',')
header = next(file_reader, None)
for row in file_reader:
	data = []
	for column_index in range(len(header)):
		data.append(str(row[column_index]).strip())
	print data
	c.execute("""INSERT INTO Suppliers VALUES (%s, %s, %s, %s, %s);""", data)
con.commit()

# Query the Suppliers table
c.execute("SELECT * FROM Suppliers")
rows = c.fetchall()
for row in rows:
	for column_index in range(len(row)):
		print row[column_index],
	print ''
