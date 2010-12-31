# -*- coding: utf-8 -*-
import sys

def find_header(infile, outfile):
    col_vals = [ ]

    f = open(infile)
    lines = f.readlines()
    f.close()

    o = open(outfile, "w")
    
    col_num = lines[0].count(",") + 1
    for i in range(col_num):
	col_vals.append([ ])

    for line in lines:
	cols = line.strip().split(",")
	for i,col in enumerate(cols):
	    l = col_vals[i]
	    l.append(col)
	    col_vals[i] = l

    for i, col in enumerate(col_vals):
	elements = sorted(list(set(col)))
	o.write( "@ATTRIBUTE class%d        {%s}\n" %  (i,",".join ( elements )) )
    o.write( "%Change 'class' with appropriate category name.\n\n" )
    
    o.write("@DATA\n")
    for line in lines:
	o.write(line)
    o.close()
    

if __name__ == "__main__":
    infile, outfile = sys.argv[1], sys.argv[2]
    find_header(infile, outfile)
    
    