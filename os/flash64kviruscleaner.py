#!/usr/bin/python
#-*-encoding:utf8-*-

#################################################################
#
#  flash64kviruscleaner.py
#  The 64,5 KB flash disk virus cleaner...
#
#  Created by Ahmet Emre Aladağ on 05.07.2008
#  http://www.emrealadag.com
#  Copyright 2008 under GPL2. All rights reserved.
#
#  This program intends to find the 64,5K flash disk virus which
#  copies itself in every directory with that directory's name.
#
#
#################################################################

import os,sys


def superficialFind(dirpath):
	for filename in os.listdir(dirpath):				# for each file, inspect
		path = dirpath+"/"+filename				# find the path
		if filename[-4:] == ".exe" and os.stat(path)[6]==66023L:# is it 64,5K size?
			print "Virus:", path,				# then mark it as virus (type 1 error!)
			try:
				os.remove(path)				# try to delete it
				print "Deleted..."
			except:
				print "Couldn't delete, try sudo."	# might not delete, requires root permissions.
			

def carefullyFind(dirpath):
	dirname = dirpath.split("/")[-1]
	if dirname+".exe" in os.listdir(dirpath):			# if the same named exe exists,
		path = dirpath+"/"+dirname+".exe"			# set the path variable
		if os.stat(path)[6]==66023L:				# if 64,5K size
			print "Virus:", path,				# print the path of the exe
			try:
				os.remove(path)				# try to delete it
				print "Deleted..."
			except:
				print "Couldn't delete, try sudo."	# might not delete, requires root permissions.
		else:
			print dirpath+"/"+dirname+".exe is not 64,5K"	# the same name but not the same size, suspicious.
	
	
findFunction = carefullyFind 						# Default inspect method!

def traverse(root):
	if not os.path.exists(root):					# If the input path is invalid,
		print root, "does not exist."
		return
	findFunction(root) 						# search for the virus
	dirs = []				
	elements = os.listdir(root)					# the files inside the directory.
	for element in elements:					# for each file/directory
		path = root+"/"+element					# find the path
		if os.path.isdir(path):					# if it is a directory
			dirs.append(path)				# then add it to the dir list.
			
	for directory in dirs:						# for each other directory inside,
		traverse(directory)					# traverse them too.
	
def main():
	global findFunction, superficialFind, carefullyFind
	print "Welcome, this program intends to find the 64,5K flash disk virus which copies itself in every directory with that directory's name. Provide your flash disk's path for the program to scan."
	print
	print "Would you like to consider the virus's name and directory to have the same name or equality in size is enough to consider the exe as a virus?"
	print "0 - Consider names and size"
	print "1 - Consider only size"
	
	choice = input("Enter your choice:")
	if choice==0:
		findFunction = carefullyFind
	elif choice==1:
		findFunction = superficialFind
	else:
		print "Invalid choice"
		sys.exit()
	
	# Now get the path...
	
	path = raw_input("Enter the path to inspect (/media/sda1):")
	if not path:
		path = "/media/sda1"
		
	traverse(path)
	
	print "Finished..."
	
if __name__ == "__main__":
	main()
