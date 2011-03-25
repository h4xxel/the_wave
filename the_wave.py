#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from engine import *

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		sprite.draw()
		label.draw()
		
def update(dt):
	if(keys[key.A]):
		sprite.x-=5
		sprite.animate()
	if(keys[key.D]):
		sprite.x+=5
		sprite.animate()
	if(keys[key.W]):
		sprite.y+=5
		sprite.animate()
	if(keys[key.S]):
		sprite.y-=5
		sprite.animate()

label=pyglet.text.Label("lol", x=20, y=50)


sprite=Sprite(img="test.png", x=100, y=100, width=64, height=64)
keys=key.KeyStateHandler()
window=Window()
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()
