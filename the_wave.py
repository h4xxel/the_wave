#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from engine import *
import random

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		background.draw()
		#ground.draw()
		pyglet.graphics.draw(len(terrain)/2, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", tuple(terrain)))
		sprite.draw()
		
def update(dt):
	background.x+=background.hspeed
	sprite.x+=sprite.hspeed
	if sprite.y<=ground.y+ground.height:
		sprite.y=ground.y+ground.height
		sprite.vspeed=0
	else:
		sprite.vspeed+=sprite.gravity
		sprite.y+=sprite.vspeed
	
	if(sprite.y<=ground.y+ground.height):
		if(keys[key.A]):
			sprite.hspeed=-3
			sprite.animate()
		elif(keys[key.D]):
			sprite.hspeed=3
			sprite.animate()
		else:
			sprite.hspeed=0
		if(keys[key.SPACE]):
			sprite.vspeed+=7
			sprite.y+=1
			sprite.animate()
			
def init_terrain():
	terrain=[0,100, 0,0, 100,100]
	for i in range(100, 800+100, 100):
		terrain.extend([i, 0, i+100,random.randint(50, 100)])
	return terrain

terrain=init_terrain()
sprite=Sprite(img="snubbe.png", x=100, y=500, width=32, height=32, gravity=-0.2)
background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
ground=Sprite(img="block.png", x=0, y=0, width=64, height=64, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()
