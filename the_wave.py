#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import ctypes
import random

class Window(pyglet.window.Window):
	def on_draw(self):
		global tex_sand, health
		for m in menu:
			m.color=(255, 255, 255)
		menu[selection].color=(100, 100, 0)
		for m in pause_menu:
			m.color=(255, 255, 255)
		pause_menu[pause_selection].color=(100, 100, 0)
		window.clear()
		if game_state == States.RUN:
			glClearColor(0, 128, 128, 255)
			#background.draw()
			terrain.draw(tex_sand)
			for k in objectlist:
				k.draw()
			sprite.draw()
			scoretext.draw()
			wave.draw()
			
			#healthbar
			pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", (16,600-32, 16,600-16, 116,600-32, 116,600-16)), ("c3B", (196,196,196, 196,196,196, 196,196,196, 196,196,196)))
			pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", (16,600-32, 16,600-16, 16+health,600-32, 16+health,600-16)), ("c3B", (0,255,0, 0,255,0, 0,255,0, 0,255,0)))
			
			#pyglet.graphics.draw(len(lolomg)/2, pyglet.gl.GL_POINTS, ("v2i", tuple(lolomg)), ("c3i", tuple(lolcol)))
			
			
		if game_state == States.MENU:
			bg.draw()
			for m in menu:
				m.draw()
		if game_state == States.PAUSE:
			pause.draw()
			for m in pause_menu:
				m.draw()
		if game_state == States.GAMEOVER:
			gameover.draw()
		
		#fps_display.draw() #show fps

	def on_key_press(self, symbol, modifiers):
		global double_jump, selection, game_state, pause_selection, score,objectlist
		if(symbol==key.SPACE and(sprite.y-5<=terrain.get_y(int(sprite.x+(sprite.width/2)+terrain.terrain_progress)) or double_jump==True)):
			djump.play() if double_jump else jump.play()
			sprite.vspeed=7
			sprite.y+=10
			double_jump=not double_jump
		if game_state == States.MENU:
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
					game_state=States.RUN
					score = 0
					objectlist=[]
					terrain.regenerate()
					sprite.x=256;sprite.y=terrain.get_y(sprite.x);sprite.hspeed=0;sprite.vspeed=0
					background_music.play()
					pyglet.clock.schedule(update)
				if selection == 1: 
					game_state=States.HISCORE
				if selection == 2:
					self.close()
			
		if game_state == States.PAUSE:
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
					game_state = States.RUN
				if pause_selection == 1:
					game_state = States.MENU
					background_music.pause()
					background_music.seek(0)

		if game_state == States.RUN:
			if symbol == key.ESCAPE:
				game_state = States.PAUSE
				
		if game_state == States.GAMEOVER:
			pyglet.clock.unschedule(update)
			if symbol == key.ENTER or symbol == key.ESCAPE:
				game_state = States.MENU

def update(dt):
	global score, double_jump, game_state, health
	if game_state == States.RUN:
		
		addobject=random.randint(1,100)
		
		if addobject ==1 :
			objectlist.append(Sprite(img=barrel, x=random.randint(300,1000), y=600, width=32, height=32, gravity=-0.2))
		for k in objectlist:
			k.hspeed=-random.randint(1,4)
			k.vspeed+=k.gravity
			k.y+=k.vspeed
			k.x+=k.hspeed
			if sprite.collision_with(k):
				health-=15
				objectlist.remove(k)
			if k.y<0:
				objectlist.remove(k)
		if(health<=0):
			background_music.pause()
			background_music.seek(0)
			game_state=States.GAMEOVER
			gameoversound.play()
				
		score+=0.1
		scoretext.text="Score: "+str(int(score))
		#background.x+=background.hspeed
		terrain.progress(4)
		terrain_y=terrain.get_y(int(sprite.x+(sprite.width/2)+terrain.terrain_progress))
		if sprite.y<=terrain_y:
			sprite.vspeed=0
			sprite.hspeed-=terrain.get_slope(int(sprite.x+(sprite.width/2)+terrain.terrain_progress))*0.8
			sprite.y=terrain_y
			double_jump=False
		else:
			sprite.vspeed+=sprite.gravity
			sprite.y+=sprite.vspeed
		sprite.x+=sprite.hspeed
		if(sprite.y-5<=terrain_y):
			sprite.animate()
			sprite.y=terrain_y
			if(keys[key.LEFT]):
				sprite.hspeed=-4 
			elif(keys[key.RIGHT]):
				sprite.hspeed=2
			else:
				sprite.hspeed=-1
			#if(keys[key.SPACE]):
				#sprite.vspeed+=7
				#sprite.y+=10
		else:
			sprite.animation.active_frame=8+int(double_jump)
			if(keys[key.LEFT]):
				sprite.hspeed=-2
			elif(keys[key.RIGHT]):
				sprite.hspeed=1
		if(sprite.x+sprite.width>=window.width-50):
			sprite.x=window.width-sprite.width-50
		if(sprite.x<=-48) or (sprite.y<-48):
			background_music.pause()
			background_music.seek(0)
			gameoversound.play()
			game_state=States.GAMEOVER

img_sand=pyglet.image.load('sand.png')
tex_sand=img_sand.get_texture()
#~ glTexImage2D (tex_sand.target, 0, GL_RGB, block.width, block.height, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_sand);
class States():
	RUN=0
	MENU=1
	PAUSE=2
	HISCORE=3
	GAMEOVER=4

game_state=States.MENU
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
#gameover
gameover=pyglet.sprite.Sprite(pyglet.resource.image('gameover.png'))

#akta diggggg
addobject=0
objectlist=[]

#sound effects
jump=pyglet.resource.media('jump.ogg',streaming=False)
djump=pyglet.resource.media('djump.ogg',streaming=False)
gameoversound=pyglet.resource.media('gameover.ogg',streaming=False)
background_music=pyglet.media.Player()
background_music.volume=0.5
background_music.eos_action=pyglet.media.Player.EOS_LOOP
background_music.queue(pyglet.resource.media('music.ogg'))

barrel=pyglet.resource.image('block.png')
cache_image(barrel)

score=0.0
health=100
double_jump=False
scoretext=pyglet.text.Label("Score: ", font_name="Arial", font_size=16, x=128, y=600-32, color=(0,0,0,255))
terrain=Terrain()
sprite=Sprite(img=pyglet.resource.image("canman.png"), x=256, y=150, width=150, height=188, gravity=-0.2)
for i in sprite.animation.frames:
	cache_image(i[0])

wave=Sprite(img=pyglet.resource.image("wave.png"), x=0, y=0, width=128, height=512)
#background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
fps_display = pyglet.clock.ClockDisplay()
pyglet.app.run()