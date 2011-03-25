#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#!/usr/bin/env python
import pyglet
from pyglet.window import key

class Sprite(pyglet.sprite.Sprite):
	animation=None
	x=0; y=0
	def __init__(self, img, x, y, width, height):
		frames=[]
		image=pyglet.resource.image(img)
		for i in range(0, image.width, width):
			frames.append([image.get_region(i, 0, width, height), 0.1])
		self.animation=Animation(frames)
		self.x=x; self.y=y
		
	def draw(self):
		self.animation.blit(self.x, self.y)
	
	def animate(self):
		self.animation.progress()

class Animation():
	frames=[[]]
	active_frame=0
	def __init__(self, frames):
		self.frames=frames
	
	def progress(self):
		self.active_frame+=1
		if(self.active_frame>=len(self.frames)): self.active_frame=0
			
	def blit(self, x, y):
		image=self.frames[self.active_frame][0]
		image.blit(x, y)
			
class AnimationFrame():
	image=None
	duration=None
	def __init__(self, image, duration):
		self.image=image
		self.duration=duration
	def __getitem__(self, lol):
		return [self.image, self.duration]
