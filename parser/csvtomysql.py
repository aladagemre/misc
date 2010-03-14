# -*- coding: utf-8 -*-
#
# Copyright © 2008 Ahmet Emre Aladağ
# Website: http://www.emrealadag.com
# Last Modification: 23.05.2008, Istanbul, Türkiye.
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Usage: python csvtomysql.py > output.sql

import os	# For iterating on the files.
import re	# For date recognition
import sys

# --------- CONFIGURATION ------------------

delimiter=";"						# Delimiter of your CSV file.
dbname = "mydb"						# Your MySQL DB Name
csvdir="/home/%s/tables/" % os.getlogin()	# The directory where your CSV files are located in.
convert_to_yymmdd=True					# If your DATE data is in dd/mm/yy format and you'd like to convert it yy/mm/dd like MySQL wants, keep this True (which is default)

# ------------------------------------------

# -------- NOW THE JOURNEY STARTS! ---------

if not os.path.exists(csvdir):
	print "No such directory: %s" % csvdir
	sys.exit()

for file in os.listdir(csvdir): 			# For every file
	(tablename, ext) = file.split(".")		# Split into name and extension
	if ext=="csv":					# If this is an CSV file
		d = open(csvdir+file)			# Open it!
		firstline = d.readline().strip("\n")	# Extract the header (field names) from the first line.
		headers = firstline.split(delimiter)	# Split them according to the delimiter you defined above.
		header_types=[]				# Create a new list for storing the field types.
		insert_sql=""				# Set the initial insert statement bulk string.(will include many INSERT statements one below another.
		
		for stupidloop in range(0,headers.__len__()+1):	# For all the fields,
			header_types.append("INT")		# Let's define default type as INT.
		
		for line in d:					# For the data in the CSV file,
			line = line.strip("\n")			# Remove the new line character!
			entries = line.split(delimiter)		# Split it according to the delimiter and you get the value list.
			
			for entry in entries:			# For every entry(value), we're going to determine the associated field type and set it in header_types.
				
				#if entry is empty, then it is assumed to be a standard varchar and NULL valued.
				if entry=='': 			
					header_types[entries.index(entry)]="VARCHAR"
					entries[entries.index(entry)]="NULL"
				#elif it matched date	
				elif re.match("\d+/\d+/\d+", entry): 
					header_types[entries.index(entry)]="DATE"
					
					# Now I want to convert default Base dd/mm/yy format to yy/mm/dd for MYSQL.
					# If your data is OK, skip this!
					if convert_to_yymmdd==True:
						# Split it into a list, and reverse, join and put it into its original place.
						ints = entry.split("/")
						ints.reverse()		
						entries[entries.index(entry)]='"'+"/".join(ints)+'"'		
					
						
				#If it is not empty and not a date, then it should be a VARCHAR or INT.
				else:
					#if it has double quote in it, it is VARCHAR
					if '"' in entry: 		
						header_types[entries.index(entry)]="VARCHAR" 
					#if it does not have quotes, it is INT
					else:				
						header_types[entries.index(entry)]="INT"
				
				
			#Now create the insert statement for the row.
			insert_sql += "INSERT INTO %s VALUES (%s);\n" % (tablename, ",".join(entries))
			
			
		#After finishing the insert statements and type determination of the fields,
		#Now generate the CREATE TABLE statements.
		
		create_table = "CREATE TABLE `%s`.`%s` (\n" % (dbname, tablename)
		for header in headers:
			# A genius method to determine a field as DATE if it has "date" in its name! :)
			if "date" in header:
				# Do not forget to print warning! We might have been wrong.
				print "/* Warning: Setting %s as DATE type. */" % header
				# Now we can set the type as DATE with a clear consience.
				header_types[headers.index(header)] = "DATE"
			
			# If the type of this header is DATE, we mustn't specify a length like DATE (50)!
			if header_types[headers.index(header)] == "DATE":
				new_line = "\t`%s` %s,\n" % (header.strip('"'), "DATE")
			# If not DATE, then we can use 50 as the max length for INT/VARCHAR.
			# Yes, I know that it is not a safe thing to do but let's calm down!
			# If you have spare time, you can go over all the values inserted into the table and determine the maximum length of those to set this value.
			else:		
				new_line = "\t`%s` %s( 50 ),\n" % (header.strip('"'), header_types[headers.index(header)])
			# Add this new field to the CREATE TABLE statement.
			create_table += new_line
		# Now let's finish this statement!
		create_table=create_table[:-2] + "\n) ENGINE = MYISAM;\n"
		
		# AT THE END! WE'RE FINISHED!
		
		print create_table	# Let's print our CREATE TABLE statement for this CSV file.
		print insert_sql	# Let's print our INSERT INTO statement(s) for this CSV file.