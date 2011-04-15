#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import random

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		glClearColor(0, 128, 128, 255)
		#background.draw()
		terrain.draw()
		sprite.draw()
		
def update(dt):
	#background.x+=background.hspeed
	terrain.progress()
	sprite.x+=sprite.hspeed
	terrain_y=terrain.get_y(sprite.x+(sprite.width/2)+terrain.terrain_progress)
	if sprite.y<=terrain_y:
		sprite.y=ground.y+ground.height
		sprite.vspeed=0
		sprite.y=terrain_y
	else:
		sprite.vspeed+=sprite.gravity
		sprite.y+=sprite.vspeed
	if(sprite.y-5<=terrain_y):
		sprite.y=terrain_y
		if(keys[key.A]):
			sprite.hspeed=-3
		elif(keys[key.D]):
			sprite.hspeed=3
		else:
			sprite.hspeed=0
		if(keys[key.SPACE]):
			sprite.vspeed+=7
			sprite.y+=10
	if(sprite.x+sprite.width>=window.width):
		sprite.x=window.width-sprite.width
	if(sprite.x<=0):
		sprite.x=0
	sprite.animate()
			

glEnable(GL_TEXTURE_2D)

terrain=Terrain()
sprite=Sprite(img="snubbe.png", x=100, y=500, width=32, height=32, gravity=-0.2)
background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
ground=Sprite(img="block.png", x=0, y=0, width=64, height=64, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()
