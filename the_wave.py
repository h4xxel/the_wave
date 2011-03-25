#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from engine import *

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		background.draw()
		ground.draw()
		sprite.draw()
		
def update(dt):
	sprite.update(ground.y+ground.height)
	background.update()
	if(keys[key.A]):
		sprite.x-=5
		sprite.animate()
	if(keys[key.D]):
		sprite.x+=5
		sprite.animate()
	if(keys[key.SPACE] and sprite.y<=ground.y+ground.height):
		sprite.vspeed+=10
		sprite.y+=1
		sprite.animate()

ground=150
sprite=Sprite(img="test.png", x=100, y=500, width=64, height=64, gravity=-0.2)
background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
ground=Sprite(img="ground.png", x=0, y=0, width=1600, height=150, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()
