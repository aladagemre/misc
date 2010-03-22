# WRITTEN BY NISHIO Hirokazu

import Image
import ImageDraw
import os


SIZE = 200
image = Image.new("RGB", (SIZE, SIZE))
d = ImageDraw.Draw(image)

c = 0.52+0.25j
for x in range(SIZE):
    for y in range(SIZE):
        re = (x * 2.0 / SIZE) - 1.0
        im = (y * 2.0 / SIZE) - 1.0

        z=re+im*1j

        #print "x=%d, y=%d, re=%s, im=%s, z=%s" %(x,y,re,im,z)
        
        for i in range(128):
            if abs(z) > 2.0: break
            z = z * z + c
        d.point((x, y), i * 5)
        #print i*10

image.save(r"julia.png", "PNG")
#os.system("gwenview julia.png&")
