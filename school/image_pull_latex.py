"""Asks for image URL, downloads it to images folder. 
Generates bibtex record and appends it to the end of the bib file.
Prints the figure LaTeX code."""

import urllib
import shutil
import os

def download_file(url, binary=True):
    filename = url.split('/')[-1].split("?")[0]
    print "Downloading", url
    webFile = urllib.urlopen(url)

    if binary:
        mode = 'wb'
    else:
        mode = 'w'
    localFile = open(filename, mode)
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    return filename

def download_file_to(url, path, binary=True):
	
	new_filename = filename = download_file(url, binary)
	
	cols = filename.split(".")
	if len(cols)>1:
		new_filename = "_".join(cols[:-1]) + "." + cols[-1]
		path = path + "/" + new_filename
	try:
		shutil.move(filename, path)
	except:
		print "File already exists?"

	return new_filename


bibtex_file = "tez.bib"
url = raw_input("Enter the URL: ")

# Bibtex key
key_default = ".".join(url.split("/")[-1].split(".")[:-1])
key = raw_input("Enter the bibtex key (default: %s): " % key_default) or key_default

# Where to save the file
directory_default="introduction"
directory = raw_input("Directory to save in (default: %s):" % directory_default ) or directory_default
filename = download_file_to(url, "images/%s" % directory )

# Convert to png if it's in gif format.
if url.strip().endswith(".gif"):
	new_name = key_default+".png"
	os.system("convert images/%s/%s images/%s/%s" % (directory, filename, directory, new_name))
	filename = new_name

# Label and description for the figure
label_default = key + "-figure"
figure_label = raw_input("Figure label (default: %s):" % label_default) or label_default
description = raw_input("Description:")


bib = """
@MISC{%s,
howpublished = {\url{%s}}
}""" % (key, url)

figure ="""\\begin{figure}
\\includegraphics[scale=0.5]{images/%s/%s}
\\centering\\caption{%s \\cite{%s}}
\\label{Flo:%s}
\\end{figure}""" % (directory, filename, description, key, figure_label)

f = open(bibtex_file, "a")
f.write(bib)
f.close()

print
print figure

