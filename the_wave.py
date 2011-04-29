#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import ctypes
import random

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		glClearColor(0, 128, 128, 255)
		#background.draw()
		terrain.draw()
		sprite.draw()
		scoretext.draw()
		wave.draw()
	
	def on_key_press(self, symbol, modifiers):
		global double_jump
		if(symbol==key.SPACE and(sprite.y-5<=terrain.get_y(sprite.x+(sprite.width/2)+terrain.terrain_progress) or double_jump==True)):
			sprite.vspeed=7
			sprite.y+=10
			double_jump=not double_jump

def update(dt):
	global score, double_jump
	score+=0.1
	scoretext.text="Score: "+str(int(score))
	#background.x+=background.hspeed
	terrain.progress(4)
	sprite.x+=sprite.hspeed
	terrain_y=terrain.get_y(sprite.x+(sprite.width/2)+terrain.terrain_progress)
	if sprite.y<=terrain_y:
		sprite.vspeed=0
		sprite.y=terrain_y
		double_jump=False
	else:
		sprite.vspeed+=sprite.gravity
		sprite.y+=sprite.vspeed
	if(sprite.y-5<=terrain_y):
		sprite.y=terrain_y
		if(keys[key.LEFT]):
			sprite.hspeed=-3
		elif(keys[key.RIGHT]):
			sprite.hspeed=1
		else:
			sprite.hspeed=-1
		#if(keys[key.SPACE]):
			#sprite.vspeed+=7
			#sprite.y+=10
	else:
		if(keys[key.LEFT]):
			sprite.hspeed=-2
		elif(keys[key.RIGHT]):
			sprite.hspeed=1
	if(sprite.x+sprite.width>=window.width-200):
		sprite.x=window.width-sprite.width-200
	if(sprite.x<=32):
		pyglet.app.exit()
		sprite.x=32
	sprite.animate()

glEnable(GL_TEXTURE_2D)
block=pyglet.image.load('block.png')
loltexture=block.get_texture()
glBindTexture(GL_TEXTURE_2D, loltexture.id);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL);
#glTexImage2D (GL_TEXTURE_2D, 0, GL_RGB, block.width, block.height, 0, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(loltexture.image_data));

score=0.0
double_jump=False
scoretext=pyglet.text.Label("Score: ", font_name="Arial", font_size=16, x=0, y=600-24, color=(0,0,0,255))
terrain=Terrain()
sprite=Sprite(img="snubbe.png", x=256, y=500, width=32, height=32, gravity=-0.2)
wave=Sprite(img="wave.png", x=0, y=0, width=128, height=512)
#background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()
