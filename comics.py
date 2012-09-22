#!/usr/bin/python3

#
# Copyright (C) 2012 Marc-Olivier Bloch <wormsparty [at] gmail [dot] com>
#
# This program is a free software: you can redistribute it 
# and/or modify it under the terms of the 'New BSD License'.
# See COPYING for more information.
#

import archive
import pyglet
import sys
import io

if len(sys.argv) == 1:
	print("Usage: " + sys.argv[0] + " (archive)+")
	sys.exit(1)

idx = 1
a = None

def load_next_archive():
	global idx
	global a

	if idx < len(sys.argv):
		a = iter(archive.Archive(sys.argv[idx]))
		idx += 1
	else:
		print("Done :)")
		sys.exit(0)

load_next_archive()

# Initialize graphics
window = pyglet.window.Window(fullscreen=True)
img = None

def load_next_image():
	global img
	global a

	try:
		element = a.__next__()
		print("Loading " + element.filename)
	except StopIteration:
		load_next_archive()
		load_next_image()
		return

	buff = element.read()	

	if len(buff) > 0:
		f = io.BytesIO(buff)
		img = pyglet.sprite.Sprite(pyglet.image.load(element.filename, file=f))
		img.scale = float(window.height) / float(img.image.width)
		img.set_position(img.image.height * img.scale, 0)
		img.rotation = -90.0
	else:
		load_next_image()

load_next_image()

@window.event
def on_draw():
	window.clear()

	if img is not None:	
		img.draw()

@window.event
def on_key_press(symbol, modifiers):
	if symbol == pyglet.window.key.Q:
		sys.exit(0)
	else:
		load_next_image()

pyglet.app.run()
