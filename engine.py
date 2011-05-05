#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.window import key
from pyglet.gl import *
import random

#cahce
image_cache={}

#use our own sprite class, because pyglet's sprite class is buggy with animations
class Sprite(pyglet.sprite.Sprite):
	animation=None
	x=0; y=0
	hspeed=0; vspeed=0
	gravity=0
	def __init__(self, img, x, y, width, height, hspeed=0, vspeed=0, gravity=0):
		frames=[]
		#image=pyglet.resource.image(img)
		for i in range(0, img.width, width):
			frames.append([img.get_region(i, 0, width, height), 0.2])
		self.animation=Animation(frames)
		self.x=x; self.y=y
		self.hspeed=hspeed; self.vspeed=vspeed
		self.gravity=gravity

	def draw(self):
		self.animation.blit(self.x, self.y, self.color)

	def animate(self):
		self.animation.progress()

	def get_width(self):
		return self.animation.width

	def get_height(self):
		return self.animation.height
		
	def collision_with(self, sprite2):
		#blunt check by bounding box
		if(self.x+self.width>sprite2.x and self.x<sprite2.x+sprite2.width and self.y+self.height>sprite2.y and self.y<sprite2.y+sprite2.height):
			#pixel perfect collision algorithm based on https://swiftcoder.wordpress.com/2009/05/16/sprite-collision-revisited/
			#new bsd license, see pixel-perfect-license
			ir=(int(max(self.x, sprite2.x)), int(max(self.y, sprite2.y)), int(min(self.x+self.width, sprite2.x+sprite2.width)), int(min(self.y+self.width, sprite2.y+sprite2.height)))
			i1=self.animation.frames[int(self.animation.active_frame)][0]
			i2=sprite2.animation.frames[int(sprite2.animation.active_frame)][0]
			
			if(i1 in image_cache):
				d1=image_cache[i1]
			else:
				d1=i1.get_image_data().get_data("A", i1.width)
				image_cache[i1]=d1
				
			if(i2 in image_cache):
				d2=image_cache[i2]
			else:
				d2=i2.get_image_data().get_data("A", i2.width)
				image_cache[i2]=d2
					
			offx1, offy1 = int(ir[0] - self.x), int(ir[1] - self.y)
			offx2, offy2 = int(ir[0] - sprite2.x), int(ir[1] - sprite2.y)
			p1 = cast(d1, POINTER(c_ubyte))
			p2 = cast(d2, POINTER(c_ubyte))

			for i in range(0, ir[2]-ir[0]):
				for j in range(0, ir[3]-ir[1]):
					c1 = p1[(offx1+i) + (j + offy1)*self.width]
					c2 = p2[(offx2+i) + (j + offy2)*sprite2.width]
					if(c1>0 and c2>0):
						return True
		return False

	width=property(get_width); height=property(get_height)

class Animation():
	# [[image, speed], [image, speed]] ...
	frames=[[]]
	active_frame=0
	def __init__(self, frames):
		self.frames=frames

	def progress(self):
		self.active_frame+=self.frames[int(self.active_frame)][1]
		if(self.active_frame>=len(self.frames)): self.active_frame=0

	def blit(self, x, y, tint=(255, 255, 255)):
		image=self.frames[int(self.active_frame)][0]
		s=pyglet.sprite.Sprite(img=image, x=x, y=y)
		s.color=tint
		s.draw()
		s.delete()

	def get_width(self):
		return self.frames[int(self.active_frame)][0].width

	def get_height(self):
		return self.frames[int(self.active_frame)][0].height

	width=property(get_width); height=property(get_height)

class Terrain():
	terrain=[]
	texturemap=[]
	terrain_progress=0
	hole=0
	hole_length=0
	
	def regenerate(self):
		self.terrain=[0,100, 0,0, 100,100]
		self.texturemap=[0,1, 0,0, 1,1]
		self.terrain_progress=0; self.hole=0
		for i in range(100, 800+200, 200):
			t_y=random.randint(50, 100)
			self.terrain.extend([i, 0, i+100,t_y, i+100,0, i+200,t_y])
			self.texturemap.extend([1.0,0, 0,float(t_y)/100.0, 0,0, 1.0,float(t_y)/100.0])

	def get_y(self, x):
		y1=self.terrain[4*(x//100)+1]
		y2=self.terrain[4*(x//100)+5]
		dx=float(x-100*(x//100))
		return y1+int(float(y2-y1)*(dx/100))
		
	def get_slope(self, x):
		y1=self.terrain[4*(x//100)+1]
		y2=self.terrain[4*(x//100)+5]
		return float(y2)/float(y1)

	def draw(self, texture):
		#pyglet.graphics.draw(len(self.terrain)/2, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", tuple(self.terrain)))
		
		#setting up opengl to properly display the texture
		glEnable(texture.target)
		glTexParameteri(texture.target, GL_TEXTURE_WRAP_S, GL_REPEAT);
		glTexParameteri (texture.target, GL_TEXTURE_WRAP_T, GL_REPEAT);
		glTexParameteri (texture.target, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
		glTexParameteri (texture.target, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
		
		glBindTexture(texture.target, texture.id)
		pyglet.graphics.draw(len(self.terrain)/2, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", tuple(self.terrain)), ('t2f', tuple(self.texturemap)))
		glDisable(texture.target)

	def progress(self, steps=1):
		for i in range(0, len(self.terrain), 2):
			self.terrain[i]-=steps
		self.terrain_progress+=steps
		if(not(self.terrain_progress%200)):
			h=self.hole
			if(h==0):
				t_y=random.randint(25, 125)
				self.terrain.extend([900,0, 1000,t_y, 1000,0, 1100,t_y])
				self.texturemap.extend([1.0,0, 0,float(t_y)/100.0, 0,0, 1.0,float(t_y)/100.0])
				if(random.randint(1, 6)==1):
					self.hole=1
					self.hole_length=random.randint(1,2)
			elif(h==1):
				self.terrain.extend([900,0, 1000,25, 1000,-100, 1100,-100])
				self.texturemap.extend([1.0,0, 0,25.0/100.0, 1.0,-100.0/100.0, 1.0,1.0])
				self.hole+=1
			elif(h>self.hole_length):
				self.terrain.extend([900,-100, 1000,-100, 1100,-100, 1100,25])
				self.texturemap.extend([1.0,0, 0,-100.0/100.0, 1.0,-100.0/100.0, 1.0,1.0])
				self.hole=0
			else:
				self.terrain.extend([900,-100, 1000,-100, 1100,-100, 1100,-100])
				self.texturemap.extend([1.0,0, 0,-100.0/100.0, 1.0,-100.0/100.0, 1.0,1.0])
				self.hole+=1

def cache_image(img):
	if not(img in image_cache):
		image_cache[img]=img.get_image_data().get_data("A", img.width)
