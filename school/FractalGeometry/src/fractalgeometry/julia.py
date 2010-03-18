import math
from PIL import Image, ImageDraw
import os

#c = complex(0.687 + 0.312)
#c = complex(-0.70176, -0.3842)
#c =0.45+0.1428j
cs = (0.70176-0.3842j, 0.835-0.2321j, 0.8+0.156j)
blowup = 2.0
size = 500

c = 0.70176-0.3842j



def f(z):
    #return z**3 - 1
    
    return z**2 + c #+ ((z**5) / (5 - z)) + ((z**3) / (3 - z)) + z / c

def convertToRGB(color):
    if color <= 85:
        return (color, 0, 0)
    elif color <=170:
        return (255, color-85, 0)
    else:
        return (255, 255, color-170)


color_matrix = []
for y in range(size):
    new_row = []
    for x in range(size):
        z = complex(x*2.0/size -1.0,y*2.0/size -1.0)

        result = f(z)
        norm = abs(result) #math.sqrt(result.real**2 + result.imag**2)
        #print norm
        iteration = 0

        while norm <= blowup and iteration < 256:
            z = complex(result.real, result.imag)
            result = f(z)
            norm = abs(result) #math.sqrt(result.real**2 + result.imag**2)
            iteration+=1

        new_row.append(iteration)



        #print "(%d, %d) - %s" % (x,y,z)
        #new_row.append(z)
    color_matrix.append(new_row)

im = Image.new("RGB", (size, size))
draw = ImageDraw.Draw(im)

#print color_matrix
for row_index in range(len(color_matrix)):
    for col_index in range(len(color_matrix[row_index])):
        value = color_matrix[row_index][col_index]*5
        #print value
        draw.point((col_index, row_index) , convertToRGB(value))

del draw
# write to stdout
filename="%.3f%.3fi.png" % (c.real, c.imag)
im.save(filename, "PNG")
#os.system("gwenview %s&" %filename)