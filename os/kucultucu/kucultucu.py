from PIL import Image
from PIL import ImageDraw, ImageFont
import glob, os

size = 218, 176
size_in = 215, 164


def kucult(folder):

	path = folder+"\\kucuk"
	
	if not os.path.exists(path):
		print "%s Mevcut Degil" % path
		os.mkdir(path)

	for infile in glob.glob("%s\\*.jpg" % folder):
		#print infile
		file, ext = os.path.splitext(infile)
		pwd_dirs = file.split("\\")
		filename = pwd_dirs[-1]
		
		im = Image.open(infile)
		im.thumbnail(size_in, Image.ANTIALIAS)
		draw = ImageDraw.Draw(im)
		font = ImageFont.truetype("arial.ttf", 9, encoding="unic")
		w, h = im.size
		#print w,h
		draw.text((w-90, h-12), "www.elbesofrasi.com", font=font, fill=(0,0,0))		
		im.save(folder+"\\kucuk\\"+ filename + ".kucuk.jpg", "JPEG")

"""Module docstring.

This serves as a long usage message.
"""
import sys
import getopt


def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        kucult(arg) # process() is defined elsewhere

if __name__ == "__main__":
    main() 
