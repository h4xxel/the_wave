#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.window import key
import random

#use our own sprite class, because pyglet's sprite class is buggy with animations
class Sprite(pyglet.sprite.Sprite):
	animation=None
	x=0; y=0
	hspeed=0; vspeed=0
	gravity=0
	def __init__(self, img, x, y, width, height, hspeed=0, vspeed=0, gravity=0):
		frames=[]
		image=pyglet.resource.image(img)
		for i in range(0, image.width, width):
			frames.append([image.get_region(i, 0, width, height), 0.3])
		self.animation=Animation(frames)
		self.x=x; self.y=y
		self.hspeed=hspeed; self.vspeed=vspeed
		self.gravity=gravity

	def draw(self):
		self.animation.blit(self.x, self.y)

	def animate(self):
		self.animation.progress()

	def get_width(self):
		return self.animation.width

	def get_height(self):
		return self.animation.height
		
	def collision_with(self, sprite2):
		if(self.x+self.width>sprite2.x and self.x<sprite2.x+sprite2.width and self.y+self.height>sprite2.y and self.y<sprite2.y+sprite2.height):
			return True
		else:
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

	def blit(self, x, y):
		image=self.frames[int(self.active_frame)][0]
		s=pyglet.sprite.Sprite(img=image, x=x, y=y)
		s.draw()

	def get_width(self):
		return self.frames[int(self.active_frame)][0].width

	def get_height(self):
		return self.frames[int(self.active_frame)][0].height

	width=property(get_width); height=property(get_height)

#~ class AnimationFrame():
	#~ image=None
	#~ duration=None
	#~ def __init__(self, image, duration):
		#~ self.image=image
		#~ self.duration=duration
	#~ def __getitem__(self, lol):
		#~ return [self.image, self.duration]

class Terrain():
	terrain=[]
	terrain_progress=0
	def __init__(self):
		self.terrain=[0,100, 0,0, 100,100]
		for i in range(100, 800+200, 100):
			self.terrain.extend([i, 0, i+100,random.randint(50, 100)])

	def get_y(self, x):
		y1=self.terrain[4*(x//100)+1]
		y2=self.terrain[4*(x//100)+5]
		dx=float(x-100*(x//100))
		return y1+int(float(y2-y1)*(dx/100))

	def draw(self):
		pyglet.graphics.draw(len(self.terrain)/2, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", tuple(self.terrain)))

	def progress(self, steps=1):
		for i in range(0, len(self.terrain), 2):
			self.terrain[i]-=steps
		self.terrain_progress+=steps
		if(not(self.terrain_progress%100)):
			self.terrain.extend([900, 0, 1000, random.randint(50, 100)])