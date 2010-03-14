from distutils.core import setup
import py2exe
#First 2 is static import for PIL
import JpegImagePlugin
from PIL import Image, ImageDraw, ImageFont


setup(console=['kucultucu.py'])