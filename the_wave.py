#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import ctypes
import random
import getpass
import urllib

def reset_boost(dt):
	global boost
	boost=0

class SplashScreen(pyglet.window.Window):
	def on_close(self):
		pass
	
	def on_draw(self):
		splash_background.blit(0, 0)

class Window(pyglet.window.Window):
	def on_close(self):
		global game_state
		if game_state==States.RUN:
			game_state=States.PAUSE
		else:
			pyglet.app.exit()
	
	def on_draw(self):
		global tex_sand, health, username, highscores, backgrounds, background_progress
		if game_state == States.MENU:
			for m in menu:
				m.color=(255, 255, 255, 255)
			menu[selection].color=(128, 0, 0, 255)
		if game_state == States.PAUSE:
			for m in pause_menu:
				m.color=(255, 255, 255, 255)
			pause_menu[selection].color=(128, 0, 0, 255)
		if game_state == States.GAMEOVER:
			for m in over_menu:
				m.color=(255, 255, 255, 255)
			over_menu[selection].color=(128, 0, 0, 255)
		window.clear()
		if game_state == States.RUN:
			glClearColor(0, 0, 0, 255)
			bw=0
			for i in range(0,len(backgrounds)-1):
				bw+=backgrounds[i].width
				if bw>=background_progress:
					dx=int(bw-background_progress)
					backgrounds[i].blit(dx-backgrounds[i].width,0)
					if dx<self.width:
						backgrounds[i+1].blit(dx,0)
					break
				if(i>=len(backgrounds)-2):
					background_progress-=float(backgrounds[i].width+backgrounds[i+1].width)
					backgrounds[-1].blit(0,0)
					break
					
			
			#background.draw()
			terrain.draw(tex_sand)
			for k in objectlist:
				k.draw()
			for m in medkitlist:
				m.draw()
			for s in speedkitlist:
				s.draw()
			sprite.draw()
			scoretext.draw()
			house.draw()
			wave.draw()
			
			#healthbar
			pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", (16,600-32, 16,600-16, 116,600-32, 116,600-16)), ("c3B", (196,196,196, 196,196,196, 196,196,196, 196,196,196)))
			pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", (16,600-32, 16,600-16, 16+health,600-32, 16+health,600-16)), ("c3B", (0,255,0, 0,255,0, 0,255,0, 0,255,0)))
			pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ("v2i", (-1,-1)), ("c3B", (255,255,255))) #small hack to avoid everything being tinted green on faildows..
			
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
			bw=0
			for i in range(0,len(backgrounds)-1):
				bw+=backgrounds[i].width
				if bw>=background_progress:
					dx=int(bw-background_progress)
					backgrounds[i].blit(dx-backgrounds[i].width,0)
					if dx<self.width:
						backgrounds[i+1].blit(dx,0)
					break
				if(i>=len(backgrounds)-2):
					background_progress-=float(backgrounds[i].width+backgrounds[i+1].width)
					backgrounds[-1].blit(0,0)
					break
			terrain.draw(tex_sand)
			for k in objectlist:
				k.draw()
			sprite.draw()
			wave.draw()
			#darken the screen when paused
			glEnable (GL_BLEND)
			glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
			pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP, ("v2i", (0,0, 0,600, 800,0, 800,600)), ("c4B", (0,0,0,196, 0,0,0,196, 0,0,0,196, 0,0,0,196)))
			pyglet.text.Label("Game Paused", font_name="Arial", font_size=64, x=128, y=500, color=(255,255,255,255)).draw()
			glDisable(GL_BLEND)
			for m in pause_menu:
				m.draw()
		if game_state == States.GAMEOVER:
			gameover.blit(0,0)
			for m in over_menu:
				m.draw()
		if game_state == States.INSTRUCTIONS:
			instructions.blit(0,0)
		
		#fps_display.draw() #show fps
	
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
		global double_jump, selection, game_state, score, objectlist, health, highscores, username, background_progress, addobject, \
		medkitlist, speedkitlist, boost
		if(game_state==States.RUN):
			terrain_y=terrain.get_y(int(sprite.x+(sprite.width/2)+terrain.terrain_progress))
			if(sprite.x>house.x and sprite.x<house.x+house.width):
				terrain_y=200
			if(symbol==key.SPACE and(sprite.y-5<=terrain_y or double_jump==True)):
				djump.play() if double_jump else jump.play()
				sprite.vspeed=7
				sprite.y+=10
				double_jump=not double_jump
			elif symbol==key.PLUS and background_music.volume<1:
				background_music.volume+=0.1
			elif symbol==key.MINUS and background_music.volume>0:
				background_music.volume-=0.1
			
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
					selection=len(menu)-1
			if symbol == key.RETURN:
				if selection == 0:
					game_state=States.RUN
					score = 0
					objectlist=[]
					terrain.regenerate()
					sprite.x=256;sprite.y=terrain.get_y(sprite.x);sprite.hspeed=0;sprite.vspeed=0
					house.x=1000
					health=100
					background_progress=0.0
					background_music.play()
					addobject=0
					boost=0
					objectlist=[]; medkitlist=[]; speedkitlist=[]
					pyglet.clock.unschedule(reset_boost)
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
					pyglet.app.exit()
			
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


def update(dt):
	global score, double_jump, game_state, health, background_progress, boost, addobject, medkitlist, speedkitlist, objectlist, speedkit
	if game_state == States.RUN: #just some extra redundancy.. we do not want to have a crash
		#start dropping barrels when approaching the power plant
		if score>700:
			if addobject==0:
				alertsound.play()
			addobject=random.randint(1,(80 if score>2000 else 130))
			if addobject ==1 and len(objectlist)<3:
				objectlist.append(Sprite(img=barrel, x=random.randint(300,1000), y=600, width=64, height=64, gravity=-0.2, anchor_x=32, anchor_y=32))
		for k in objectlist:
			k.hspeed=-random.randint(1,4)
			k.vspeed+=k.gravity
			k.y+=k.vspeed
			k.x+=k.hspeed
			k.rotation+=5.0
			if sprite.collision_with(k):
				hitsound.play()
				health-=15
				objectlist.remove(k)
			if k.y<0:
				objectlist.remove(k)
				
		terrain.progress(4)
		#speedkits
		if random.randint(1,650)==1 and score>200:
			speedkitlist.append(Sprite(img=speedkit,x=random.randint(500,1000), y=600, width=32, height=32, gravity=-0.2))
		for s in speedkitlist:
			if s.x<800:
				terrain_s=terrain.get_y(int(s.x+(s.width/2)+terrain.terrain_progress))
				if s.y<=terrain_s:
					s.y=terrain_s 
					s.hspeed=-4
					s.x+=s.hspeed
				else:
					s.hspeed=-random.randint(1,4)
					s.x+=s.hspeed
					s.vspeed+=s.gravity
					s.y+=s.vspeed
			elif s.y<0 or s.x>800:
				s.y=150
			if sprite.collision_with(s):
				#hitsound.play()
				boost=2
				pyglet.clock.unschedule(reset_boost)
				pyglet.clock.schedule_once(reset_boost, 10)
				speedkitlist.remove(s)
			if s.y<0:
				speedkitlist.remove(s)
		
		
		#and we don't need medkits until we have barrels
		if random.randint(1,500)==1 and score>800:
			medkitlist.append(Sprite(img=medkit,x=random.randint(500,1000), y=600, width=32, height=32, gravity=-0.2))
		for m in medkitlist:
			if m.x<800:
				terrain_m=terrain.get_y(int(m.x+(m.width/2)+terrain.terrain_progress))
				if m.y<=terrain_m:
					m.y=terrain_m 
					m.hspeed=-4
					m.x+=m.hspeed
				else:
					m.hspeed=-random.randint(1,4)
					m.x+=m.hspeed
					m.vspeed+=m.gravity
					m.y+=m.vspeed
			elif m.y<0 or m.x>800:
				m.y=150
			if sprite.collision_with(m):
				#hitsound.play()
				health+=10
				medkitlist.remove(m)
			if m.y<0:
				medkitlist.remove(m)
		if(health>100): health=100
		
		if(health<=0):
			pyglet.clock.unschedule(update)
			background_music.pause()
			background_music.seek(0)
			game_state=States.GAMEOVER
			selection=0
			gameoversound.play()
			return
				
		score+=0.1
		background_progress+=1
		scoretext.text="Score: "+str(int(score))
		#background.x+=background.hspeed
		#terrain.progress(4)
		terrain_y=terrain.get_y(int(sprite.x+(sprite.width/2)+terrain.terrain_progress))
		if(sprite.x+sprite.width/4>house.x and sprite.x<house.x+house.width-200):
			if sprite.y>200-6:
				terrain_y=200
			sprite.x+=sprite.hspeed
			if(sprite.y-5<=terrain_y) and not(sprite.vspeed>0):
				sprite.vspeed=0
				#sprite.hspeed-=terrain.get_slope(int(sprite.x+(sprite.width/2)+terrain.terrain_progress))*0.8
				sprite.y=terrain_y
				double_jump=False
				
				sprite.animate()
				if(keys[key.LEFT]):
					sprite.hspeed=-5-boost
				elif(keys[key.RIGHT]):
					sprite.hspeed=2+boost if terrain_y==200 else -4
				else:
					sprite.hspeed=-1 if terrain_y==200 else -4
			else:
				sprite.vspeed+=sprite.gravity
				sprite.y+=sprite.vspeed
				sprite.animation.active_frame=8+int(double_jump)
				if(keys[key.LEFT]):
					sprite.hspeed=-2-boost
				elif(keys[key.RIGHT]):
					sprite.hspeed=1+boost if terrain_y==200 else -4
				
		else:
			if(sprite.y<=terrain_y):
				sprite.hspeed-=terrain.get_slope(int(sprite.x+(sprite.width/2)+terrain.terrain_progress))*0.8
			sprite.x+=sprite.hspeed
			if(sprite.y-5<=terrain_y):
				sprite.vspeed=0
				sprite.y=terrain_y
				double_jump=False
				
				sprite.animate()
				if(keys[key.LEFT]):
					sprite.hspeed=-5-boost
				elif(keys[key.RIGHT]):
					sprite.hspeed=2+boost
				else:
					sprite.hspeed=-1
			else:
				sprite.vspeed+=sprite.gravity
				sprite.y+=sprite.vspeed
				sprite.animation.active_frame=8+int(double_jump)
				if(keys[key.LEFT]):
					sprite.hspeed=-2-boost
				elif(keys[key.RIGHT]):
					sprite.hspeed=1+boost
		
		wave.animate()
		#when we reach the city we create foreground houses as well
		if(boost>0):
			sprite.animate()
			sprite.tint=(0,255,0)
		else:
			sprite.tint=(255,255,255)
		if score>1400: house.x+=house.hspeed
		if house.x<-500:
			house.x=800+random.randint(200, 600)
			house.animation.active_frame=0
		if house.x<600 and house.animation.active_frame<len(house.animation.frames)-1: 
			if(house.animation.active_frame==0.0):
				collapse.play()
			house.animate()
		
		#sprite.y=300; sprite.x=400; health=100 # I am too awesome for this game
		if(sprite.x+sprite.width>=window.width-100):
			sprite.x=window.width-sprite.width-100
		if(sprite.x<=-48) or (sprite.y<-48):
			pyglet.clock.unschedule(update)
			background_music.pause()
			background_music.seek(0)
			gameoversound.play()
			game_state=States.GAMEOVER
			selection=0
			return
			
def init(dt):
	global bg, menu, pause_menu, gameover, over_menu, instructions, jump, djump, gameoversound, hitsound, \
		background_music, house, barrel, medkit, tex_sand, backgrounds, scoretext, terrain, sprite, window, keys, \
		splash_window, fps_display, wave, collapse, alertsound, speedkit
	#menu
	bg=pyglet.resource.image('menu.png')
	menu=[pyglet.text.Label("Start game",x=128, y=350, font_name="Arial", font_size=64),
		pyglet.text.Label("Instructions",x=128, y=250, font_name="Arial", font_size=64),
		pyglet.text.Label("Highscores",x=128, y=150, font_name="Arial", font_size=64),
		pyglet.text.Label("Exit game",x=128, y=50, font_name="Arial", font_size=64)]
	#pause menu
	pause_menu=[
		pyglet.text.Label("Resume game",x=128, y=300, font_name="Arial", font_size=64), 
		pyglet.text.Label("Quit to menu",x=128, y=200, font_name="Arial", font_size=64)]
	#gameover
	gameover=pyglet.resource.image('gameover.png')
	over_menu=[
		pyglet.text.Label("Submit score",x=128, y=150, font_name="Arial", font_size=64), 
		pyglet.text.Label("Quit to menu",x=128, y=50, font_name="Arial", font_size=64)]
	#instructions
	instructions=pyglet.resource.image('instructions.png')

	#sound effects
	jump=pyglet.resource.media('jump.ogg',streaming=False)
	djump=pyglet.resource.media('djump.ogg',streaming=False)
	collapse=pyglet.resource.media('collapse.ogg',streaming=False)
	gameoversound=pyglet.resource.media('gameover.ogg',streaming=False)
	hitsound=pyglet.resource.media('hit.ogg', streaming=False)
	alertsound=pyglet.resource.media('warning.ogg', streaming=False)
	background_music=pyglet.media.Player()
	background_music.volume=0.5
	background_music.eos_action=pyglet.media.Player.EOS_LOOP
	background_music.queue(pyglet.resource.media('music.ogg'))
	
	house=Sprite(img=pyglet.resource.image("house.png"), x=1000, y=0, width=460, height=400, hspeed=-4, anim_speed=0.1)
	
	barrel=pyglet.resource.image('barrel.png')
	cache_image(barrel)
	medkit=pyglet.resource.image('medkit.png')
	cache_image(medkit)
	speedkit=pyglet.resource.image('speedkit.png')
	cache_image(speedkit)

	tex_sand=pyglet.resource.texture('sand.png')

	backgrounds=(
		pyglet.resource.image("beach1.png"),
		pyglet.resource.image("beach2.png"),
		pyglet.resource.image("forrest1.png"),
		pyglet.resource.image("forrest2.png"),
		pyglet.resource.image("pplant1.png"),
		pyglet.resource.image("village1.png"),
		pyglet.resource.image("village2.png"),
		pyglet.resource.image("pplant2.png"),
		pyglet.resource.image("city1.png"),
		pyglet.resource.image("city2.png"),
		pyglet.resource.image("city1.png")
	)

	scoretext=pyglet.text.Label("Score: ", font_name="Arial", font_size=16, x=128, y=600-32, color=(0,0,0,255))
	terrain=Terrain()
	sprite=Sprite(img=pyglet.resource.image("canman.png"), x=256, y=150, width=150, height=188, gravity=-0.2)
	for i in sprite.animation.frames:
		cache_image(i[0])

	wave=Sprite(img=pyglet.resource.image("wave.png"), x=-200, y=0, width=600, height=600, anim_speed=0.1)
	#background=Sprite(img=pyglet.resource.image("city1.png"), x=0, y=0, width=1077, height=600, hspeed=-0.5)
	window=Window(width=800, height=600, caption="The Wave", vsync=False, visible=False)
	window.push_handlers(keys)
	window.set_icon(
		pyglet.resource.image("icon16.png"),
		pyglet.resource.image("icon32.png"),
		pyglet.resource.image("icon48.png")
	)
	splash_window.set_visible(False)
	window.set_visible(True) #make sure the window gets its icon
	fps_display = pyglet.clock.ClockDisplay()

#~ glTexImage2D (tex_sand.target, 0, GL_RGB, block.width, block.height, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_sand);
class States():
	RUN=0
	MENU=1
	PAUSE=2
	HISCORE=3
	SUBMITSCORE=4
	GAMEOVER=5
	INSTRUCTIONS=6

pyglet.resource.path = ['res', 'res/backgrounds']
pyglet.resource.reindex()

splash_background=pyglet.resource.image("splash.png")
screen = pyglet.window.get_platform().get_default_display().get_default_screen()
splash_window=SplashScreen(width=640, height=480, caption="The Wave", style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, visible=False)
splash_window.set_icon(
	pyglet.resource.image("icon16.png"),
	pyglet.resource.image("icon32.png"),
	pyglet.resource.image("icon48.png")
)
splash_window.set_visible(True)
splash_window.set_location(x=screen.width/2-640/2, y=screen.height/2-480/2)

game_state=States.MENU
selection=0

#menu
bg=None
menu=[]
#pause menu
pause_menu=[]
#gameover
gameover=None
over_menu=[]
#instructions
instructions=None

#akta diggggg
addobject=0
objectlist=[]

#powerupz
addmedkit=0
medkitlist=[]
addspeedkit=0
speedkitlist=[]

boost=0

#sound effects
jump=None
djump=None
collapse=None
gameoversound=None
hitsound=None
alertsound=None
background_music=None

house=None
barrel=None
medkit=None
speedkit=None

tex_sand=None

backgrounds=None
background_progress=0.0

score=0.0
health=100
double_jump=False
scoretext=None
terrain=None
sprite=None

wave=None
keys=key.KeyStateHandler()
window=None
fps_display=None

username=getpass.getuser()
highscores=[]

pyglet.clock.schedule_once(init, 1) #schedule the init function to do the real loading.. we want the splash as soon as possible

pyglet.app.run()