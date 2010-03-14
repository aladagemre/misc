#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Ahmet Emre Aladağ
# Website: http://www.emrealadag.com
# Last Modification: 24.06.2009, Istanbul, Türkiye.
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Scans the specified directory for duplicate directories
# of at least the specified size.
#
# Verilen dizini muhtemel (belirtilen boyuttan büyük) kopya
# dizinler için tarar.

import os,sys

folder = raw_input("Dizin: ")
min_size = raw_input("Minimum boyut (byte cinsinden) [öntanımlı 1MB için boş bırakın]:")
if not min_size:
    print "1MB varsayılıyor"
    min_size = 1048576
else:
    min_size = int(min_size)

folder_size = 0
l = []
for (path, dirs, files) in os.walk(folder):
    for directory in dirs:
	dir_path=path+"/"+directory
	#dir_path = dir_path.replace(" ", "\ ") #For windows?
	dir_size=os.popen('du -B 1 -s "'+dir_path+'"').read().split("\t")[0]
	try:
	    dir_size = int(dir_size)
	except:
	    pass
	if dir_size > min_size:
	    l.append((dir_size, directory, dir_path))
l.sort()
l.reverse()

r = 0
total_size=0
while r < l.__len__():
    x = r
    
    try:
	files1 = os.listdir(l[x][2])
	files2 = os.listdir(l[x+1][2])
	if l[x][0] == l[x+1][0] and len(files1) ==  len(files2):
	    print "%d\t%s" % (x, l[x])
	    while (l[x][0] == l[x+1][0]):
		print "%d\t%s" % (x+1, l[x+1])
		total_size+=l[x+1][0]
		x+=1
	    r = x+1
	    print
	else:
	    r+=1
    except:
	r+=1
    
print "Muhtemel Fazlalık:", total_size
