import sys, pygame
import math
from pygame import *
pygame.init()

import time
counter = 0
timer = time.time()

size = width, height = 1024, 768
speed = [6,6]
speedtom = [6,6]
black = 0, 0, 0
blue = 0, 0, 255
white = 255,255,255
screen = pygame.display.set_mode(size)

class ball:
	def __init__(self, image_name):
		self.ballimage = pygame.image.load(image_name)
		self.myball = self.ballimage.get_rect()

		
	def move(self,speed):
		self.myball = self.myball.move(speed)


	def top(self, increment = 0):
		self.myball.top += increment
		return self.myball.top
	def left(self, increment = 0):
		self.myball.left += increment
		return self.myball.left
	def right(self, increment = 0):
		self.myball.right += increment
		return self.myball.right
	def bottom(self, increment = 0):
		self.myball.bottom += increment
		return self.myball.bottom
	def width(self):
		return self.myball.width
	def height(self):
		return self.myball.height

	def mid(self):
		return [self.myball.left+self.myball.width/2 , self.myball.top+self.myball.height/2]


	def center(self,posi):
		self.myball.left = posi[0] - self.myball.width/2
		self.myball.top = posi[1] - self.myball.height/2


	def go(self, key):

	    step = 30
	    
	    if (key == K_RIGHT):
		self.myball.left += step
	    elif (key == K_LEFT):
		self.myball.left -= step
	    elif (key == K_UP):
		self.myball.top -= step
	    elif (key == K_DOWN):
		self.myball.top += step

bom = ball("cheese.jpg")
tom = ball("mouse2.gif")
tom.myball.left = width - tom.myball.width
score = 0
def kes(ball1,ball2,tour):
	right1 = ball1.right()
	right2 = ball2.right()
	bottom1= ball1.bottom()
	bottom2= ball2.bottom()
	top1 = ball1.top()
	top2 = ball2.top()
	left1 = ball1.left()
	left2 = ball2.left()
	
	if left1 < left2 and left2 < right1:
		if top1 < bottom2 and bottom2 < bottom1:
			
			return 1
		elif bottom1 < top2 and top2 < top1:
			return 1
	
	elif tour==1:
		return 0
	else:
		kes(ball2,ball1,1)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		elif event.type == pygame.MOUSEMOTION:

			#tom.center(event.pos)
			pass
		elif event.type == pygame.KEYDOWN:
		    if ((event.key == pygame.K_RIGHT)
		    or (event.key == pygame.K_LEFT)
		    or (event.key == pygame.K_UP)
		    or (event.key == pygame.K_DOWN)):
		        bom.go(event.key)
			
	if kes(bom,tom,0):
		speed[0] = -speed[0]
		speed[1] = -speed[1]
		speedtom[0] = -speedtom[0]
		speed[1] = -speedtom[1]
		score+=1



	bom.move(speed)
	
	if bom.left() < 0 or bom.right() > width:
		speed[0] = -speed[0]
		
		
	if bom.top() < 0 or bom.bottom() > height:
		speed[1] = -speed[1]
	

	if tom.left() < 0 or tom.right() > width:
		speedtom[0] = -speedtom[0]
		
		
	if tom.top() < 0 or tom.bottom() > height:
		speedtom[1] = -speedtom[1]
	
	bm=bom.mid()
	tm=tom.mid()
	deltax = bm[0] - tm[0]
	deltay = bm[1] - tm[1]		
	sum = deltax*deltax + deltay*deltay
	
	while sum > 2*speed[0]*speed[0]:
		deltax*=0.9
		deltay*=0.9
		sum = deltax*deltax + deltay*deltay

	speedtom = deltax, deltay

	tom.move(speedtom)


	screen.fill(white)
	screen.blit(bom.ballimage, bom.myball)
	screen.blit(tom.ballimage, tom.myball)
	if pygame.font:

	    font = pygame.font.Font(None, 36)
	    text = font.render("Puan: %s" % score, 1, (255, 0, 0))
            textpos = text.get_rect(width/2)
	    screen.blit(text, textpos)
	    diff = time.time() - timer
	    m = (diff - diff % 60)/60
	    s = math.floor(diff % 60)

	    count = font.render("%s:%s" % (m,s), 1, (0,0,255))
	    countpos = count.get_rect()
	    countpos.left = width - 100
	    screen.blit(count,countpos)

	pygame.display.flip()


