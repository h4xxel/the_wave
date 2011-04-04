#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.window import key


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
			
class AnimationFrame():
	image=None
	duration=None
	def __init__(self, image, duration):
		self.image=image
		self.duration=duration
	def __getitem__(self, lol):
		return [self.image, self.duration]
