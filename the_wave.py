#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import random
from pyglet.window import key

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		if game_state == states.RUN:
			glClearColor(0, 128, 128, 255)
			#background.draw()
			terrain.draw()
			sprite.draw()
		if game_state == states.MENU:
			bg.draw()
			for m in menu:
				m.draw()
		if game_state == states.PAUSE:
			pause.draw()
			for m in pause_menu:
				m.draw()
		
	def on_key_press(self, symbol, modifiers):
		global selection, game_state, pause_selection, double_jump
		if game_state == states.MENU:
			if symbol == key.DOWN:
				selection+=1
				if selection == 3:
					selection=0
			if symbol == key.UP:
				selection-=1
				if selection == -1:
					selection=2
			if symbol == key.RETURN:
				if selection == 0:
					game_state=states.RUN
				if selection == 1:
					game_state=states.HISCORE
				if selection == 2:
					self.close()
			


		if game_state == states.PAUSE:
			if symbol == key.DOWN:
				pause_selection+=1
				if pause_selection == 2:
					pause_selection=0
			if symbol == key.UP:
				pause_selection-=1
				if pause_selection == -1:
					pause_selection=1
			if symbol == key.RETURN:
				if pause_selection == 0:
					game_state = states.RUN
				if pause_selection == 1:
					game_state = states.MENU
				
		if game_state == states.RUN:
			if symbol == key.ESCAPE:
				game_state = states.PAUSE
		
def update(dt):
	for m in menu:
		m.color=(255, 255, 255)
	menu[selection].color=(100, 100, 0)
	for m in pause_menu:
		m.color=(255, 255, 255)
	pause_menu[pause_selection].color=(100, 100, 0)
	
	if game_state == states.RUN:
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

class states():
	RUN=0
	MENU=1
	PAUSE=2
	HISCORE=3

game_state=states.MENU
#menu
bg=pyglet.sprite.Sprite(pyglet.resource.image('thewave.png'))
start=pyglet.sprite.Sprite(pyglet.resource.image('start.png'),x=200, y=350)
hiscore=pyglet.sprite.Sprite(pyglet.resource.image('hiscore.png'),x=200, y=200)
quit=pyglet.sprite.Sprite(pyglet.resource.image('quit.png'),x=200, y=50)
menu=[start, hiscore, quit]
selection=0
#pause menu
resume=pyglet.sprite.Sprite(pyglet.resource.image('start.png'),x=200, y=350)
pause=pyglet.sprite.Sprite(pyglet.resource.image('pause.png'))
pause_quit=pyglet.sprite.Sprite(pyglet.resource.image('quit.png'),x=200, y=200)
pause_menu=[resume, pause_quit]
pause_selection=0
#some nice music
music = pyglet.resource.media('snow.ogg')
music.play()
#sound effects

terrain=Terrain()
sprite=Sprite(img="snubbe.png", x=100, y=500, width=32, height=32, gravity=-0.2)
background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
ground=Sprite(img="block.png", x=0, y=0, width=64, height=64, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()