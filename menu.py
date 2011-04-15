#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from engine import *
from pyglet.window import key

class Window(pyglet.window.Window):
	def on_draw(self):
		self.clear()
		if game_state == states.MENU:
			bg.draw()
			for m in menu:
				m.draw()
	def on_key_press(self, symbol, modifiers):
		global selection, game_state
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

def update(dt):
	for m in menu:
		m.color=(255, 255, 255)
	menu[selection].color=(100, 100, 0)

class states():
	RUN=0
	MENU=1
	PAUSE=2
	HISCORE=3

game_state=states.MENU
bg=pyglet.sprite.Sprite(pyglet.resource.image('thewave.png'))
start=pyglet.sprite.Sprite(pyglet.resource.image('start.png'),x=200, y=350)
hiscore=pyglet.sprite.Sprite(pyglet.resource.image('hiscore.png'),x=200, y=200)
quit=pyglet.sprite.Sprite(pyglet.resource.image('quit.png'),x=200, y=50)
menu=[start, hiscore, quit]
selection=0
music = pyglet.resource.media('snow.ogg')
music.play()

keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()