#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import ctypes
import random
import getpass
import urllib

class Window(pyglet.window.Window):
	def on_draw(self):
		global tex_sand, health, username, highscores
		if game_state == States.MENU:
			for m in menu:
				m.color=(255, 255, 255, 255)
			menu[selection].color=(100, 100, 0, 255)
		if game_state == States.PAUSE:
			for m in pause_menu:
				m.color=(255, 255, 255, 255)
			pause_menu[selection].color=(100, 100, 0, 255)
		if game_state == States.GAMEOVER:
			for m in over_menu:
				m.color=(255, 255, 255, 255)
			over_menu[selection].color=(100, 100, 0, 255)
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
			pyglet.graphics.draw(4, pyglet.gl.GL_POINTS, ("v2i", (-1,-1)), ("c3B", (255,255,255))) #small hack to avoid everything being tinted green..
			
			#pyglet.graphics.draw(len(lolomg)/2, pyglet.gl.GL_POINTS, ("v2i", tuple(lolomg)), ("c3i", tuple(lolcol)))
			
		if game_state == States.SUBMITSCORE:
			glClearColor(0, 0, 0, 255)
			pyglet.text.Label("Submitting score", font_name="Arial", font_size=64, x=64, y=500, color=(255,255,255,255)).draw()
			pyglet.text.Label("Nickname: %s|" % username, font_name="Arial", font_size=20, x=100, y=300, color=(255,255,255,255)).draw()
			pyglet.text.Label("Press enter to submit or escape to return to the menu", font_name="Arial", font_size=18, x=100, y=50, color=(255,255,255,255)).draw()
		if game_state == States.HISCORE:
			glClearColor(0, 0, 0, 255)
			for i in range(0, len(highscores)):
				s=highscores[i][0:-1].partition(",")
				pyglet.text.Label(s[0], font_name="Arial", font_size=20, x=64, y=500-32*i, color=(255,255,255,255)).draw()
				pyglet.text.Label(s[2], font_name="Arial", font_size=20, x=600, y=500-32*i, color=(255,255,255,255)).draw()
			pyglet.text.Label("Press enter or escape to return to the menu", font_name="Arial", font_size=18, x=120, y=50, color=(255,255,255,255)).draw()
		if game_state == States.MENU:
			bg.blit(0,0)
			for m in menu:
				m.draw()
		if game_state == States.PAUSE:
			pause.blit(0,0)
			for m in pause_menu:
				m.draw()
		if game_state == States.GAMEOVER:
			gameover.blit(0,0)
			for m in over_menu:
				m.draw()
		if game_state == States.INSTRUCTIONS:
			instructions.blit(0,0)
		
		fps_display.draw() #show fps
	
	def on_text(self, text):
		global username
		#input text for submitting score
		if(game_state==States.SUBMITSCORE and len(username)<16):
			username+=text.replace("\n", "").replace("\r","").replace(",","")
	
	def on_text_motion(self, motion):
		global username
		if(game_state==States.SUBMITSCORE and motion==key.MOTION_BACKSPACE):
			username=username[0:-1]

	def on_key_press(self, symbol, modifiers):
		global double_jump, selection, game_state, score, objectlist, health, highscores, username
		if(game_state==States.RUN and symbol==key.SPACE and(sprite.y-5<=terrain.get_y(int(sprite.x+(sprite.width/2)+terrain.terrain_progress)) or double_jump==True)):
			djump.play() if double_jump else jump.play()
			sprite.vspeed=7
			sprite.y+=10
			double_jump=not double_jump
			
		if game_state == States.HISCORE and(symbol == key.ENTER or symbol == key.ESCAPE):
			game_state = States.MENU
			symbol=None
			
		if game_state == States.INSTRUCTIONS and(symbol == key.ENTER or symbol == key.ESCAPE):
			game_state = States.MENU
			symbol=None
		
		if game_state == States.SUBMITSCORE:
			if symbol == key.ENTER and len(username)>0:
				try:
					u=urllib.urlopen("http://h4xxel.ath.cx/software/wave/highscore_api.php?name=%s&score=%s" % (urllib.quote(username), urllib.quote(str(score))))
					highscores=u.readlines()
					u.close()
				except:
					highscores=["Please check your internet connection "]
				game_state = States.HISCORE
				symbol=None
			if symbol == key.ESCAPE:
				game_state=States.MENU
				symbol=None
		
		if game_state == States.MENU:
			if symbol == key.DOWN:
				selection+=1
				if selection == 4:
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
					health=100
					background_music.play()
					pyglet.clock.schedule_interval(update, 1.0/60.0)
					pyglet.clock.schedule_interval(update, 1.0/60.0) #somehow this works and one schedule on 1/120 does not.. whatever
					#pyglet.clock.schedule(update)
					symbol=None
				if selection == 1:
					game_state=States.INSTRUCTIONS
					symbol=None
				if selection == 2: 
					game_state=States.HISCORE
					try:
						u=urllib.urlopen("http://h4xxel.ath.cx/software/wave/highscore_api.php")
						highscores=u.readlines()
						u.close()
					except:
						highscores=["Please check your internet connection "]
				if selection == 3:
					self.close()
			
		if game_state == States.PAUSE:
			if symbol == key.DOWN:
				selection+=1
				if selection == 2:
					selection=0
			if symbol == key.UP:
				selection-=1
				if selection == -1:
					selection=1
			if symbol == key.RETURN:
				if selection == 0:
					game_state = States.RUN
					background_music.play()
				if selection == 1:
					pyglet.clock.unschedule(update)
					game_state = States.MENU
					background_music.seek(0)
					selection=0
		
		if game_state == States.GAMEOVER:
			if symbol == key.DOWN:
				selection+=1
				if selection == 2:
					selection=0
			if symbol == key.UP:
				selection-=1
				if selection == -1:
					selection=1
			if symbol == key.RETURN:
				if selection == 0:
					game_state = States.SUBMITSCORE
					symbol=None
					selection=0
				if selection == 1:
					game_state = States.MENU
					background_music.seek(0)
					symbol=None
					selection=0
			if symbol == key.ESCAPE:
				game_state=States.MENU
				symbol=None
				selection=0
				
		if game_state == States.RUN:
			if symbol == key.ESCAPE:
				selection=0
				game_state = States.PAUSE
				background_music.pause()
				
		#~ if game_state == States.GAMEOVER:
			#~ if symbol == key.ENTER:
				#~ game_state=States.SUBMITSCORE
				#~ symbol=None
			#~ if symbol == key.ESCAPE:
				#~ game_state=States.MENU
				#~ symbol=None
				#~ selection=0
				#game_state = States.MENU

def update(dt):
	global score, double_jump, game_state, health
	if game_state == States.RUN: #just some extra redundancy.. we do not want to have a crash
		addobject=random.randint(1,100)
		
		if addobject ==1 :
			objectlist.append(Sprite(img=barrel, x=random.randint(300,1000), y=600, width=32, height=32, gravity=-0.2))
		for k in objectlist:
			k.hspeed=-random.randint(1,4)
			k.vspeed+=k.gravity
			k.y+=k.vspeed
			k.x+=k.hspeed
			if sprite.collision_with(k):
				hitsound.play()
				health-=15
				objectlist.remove(k)
			if k.y<0:
				objectlist.remove(k)
		if(health<=0):
			pyglet.clock.unschedule(update)
			background_music.pause()
			background_music.seek(0)
			game_state=States.GAMEOVER
			selection=0
			gameoversound.play()
			return
				
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
			pyglet.clock.unschedule(update)
			background_music.pause()
			background_music.seek(0)
			gameoversound.play()
			game_state=States.GAMEOVER
			selection=0
			return

#~ glTexImage2D (tex_sand.target, 0, GL_RGB, block.width, block.height, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_sand);
class States():
	RUN=0
	MENU=1
	PAUSE=2
	HISCORE=3
	SUBMITSCORE=4
	GAMEOVER=5
	INSTRUCTIONS=6

pyglet.resource.path = ['res']
pyglet.resource.reindex()

game_state=States.MENU
selection=0
#menu
bg=pyglet.resource.image('thewave.png')
menu=[pyglet.text.Label("Start game",x=200, y=350, font_name="Arial", font_size=64),
	pyglet.text.Label("Instructions",x=200, y=250, font_name="Arial", font_size=64),
	pyglet.text.Label("Highscores",x=200, y=150, font_name="Arial", font_size=64),
	pyglet.text.Label("Exit game",x=200, y=50, font_name="Arial", font_size=64)]
#pause menu
pause=pyglet.resource.image('pause.png')
pause_menu=[
	pyglet.text.Label("Resume game",x=200, y=300, font_name="Arial", font_size=64), 
	pyglet.text.Label("Quit to menu",x=200, y=200, font_name="Arial", font_size=64)]
#gameover
gameover=pyglet.resource.image('gameover.png')
over_menu=[
	pyglet.text.Label("Submit score",x=200, y=150, font_name="Arial", font_size=64), 
	pyglet.text.Label("Quit to menu",x=200, y=50, font_name="Arial", font_size=64)]
#instructions
instructions=pyglet.resource.image('instructions.png')

#akta diggggg
addobject=0
objectlist=[]

#sound effects
jump=pyglet.resource.media('jump.ogg',streaming=False)
djump=pyglet.resource.media('djump.ogg',streaming=False)
gameoversound=pyglet.resource.media('gameover.ogg',streaming=False)
hitsound=pyglet.resource.media('hit.ogg', streaming=False)
background_music=pyglet.media.Player()
background_music.volume=0.5
background_music.eos_action=pyglet.media.Player.EOS_LOOP
background_music.queue(pyglet.resource.media('music.ogg'))

barrel=pyglet.resource.image('barrel.png')
cache_image(barrel)

tex_sand=pyglet.resource.texture('sand.png')

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
window=Window(width=800, height=600, caption="The Wave", vsync=False, visible=False)
window.push_handlers(keys)
window.set_icon(
	pyglet.resource.image("icon16.png"),
	pyglet.resource.image("icon32.png"),
	pyglet.resource.image("icon48.png")
)
window.set_visible(True) #make sure the window gets its icon
fps_display = pyglet.clock.ClockDisplay()

username=getpass.getuser()
highscores=[]

pyglet.app.run()