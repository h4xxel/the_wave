#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from engine import *

<<<<<<< HEAD
window=pyglet.window.Window()
pyglet.app.run()
=======
class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		background.draw()
		ground.draw()
		sprite.draw()
		
def update(dt):
	sprite.update(ground.y+ground.height)
	background.update()
	if(sprite.y<=ground.y+ground.height):
		if(keys[key.A]):
			sprite.hspeed=-5
			sprite.animate()
		elif(keys[key.D]):
			sprite.hspeed=5
			sprite.animate()
		else:
			sprite.hspeed=0
		if(keys[key.SPACE]):
			sprite.vspeed+=5
			sprite.y+=1
			sprite.animate()

ground=150
sprite=Sprite(img="snubbe.png", x=100, y=500, width=32, height=32, gravity=-0.2)
background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
ground=Sprite(img="ground.png", x=0, y=0, width=1600, height=150, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()
>>>>>>> 1f7079d6c44c9a76c175fb3fca525ec2f8b1b351
