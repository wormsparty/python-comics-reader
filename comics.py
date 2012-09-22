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

# We can specify any number of archives, 
# read one after another
if len(sys.argv) == 1:
	print("Usage: " + sys.argv[0] + " (archive)+")
	sys.exit(1)

# We keep a list of sane files.
archives = []

for i in sys.argv[1:]:
	try:
		archive.Archive(i)
		archives.append(i)
	except archive.core.Error:
		print(i + " doesn't to be an archive.")

# The current archive instance and archive number.
a = None
archive_index = 0

# Call to read the archive associated with 'idx'.
def load_archive(idx):
	global a
	global position
	global archive_index

	# By going back the program doesn't exit if it reached the end.
	if idx < 0:
		idx = 0

	# Don't read futher than you can!		
	if idx >= len(archives):
		print("Done :)")
		sys.exit(0)

	try:
		a = iter(archive.Archive(archives[idx]))
	except archive.core.Error:
		# Shouldn't happen since we already checked the existence of
		# the file. If this happens, at least dont crash!
		load_archive(idx + 1)

	if idx < archive_index:
		# Here it's a bit hard, since we need to
		# know how many entries there are. pyarchive
		# doesn't look like it provised a 'len' field, so...
		try:
			while True:
				a.__next__()
				position += 1
		except StopIteration:
			position -= 2
		
		# Go one step back...
		try:
			a = iter(archive.Archive(archives[idx]))
		except archive.core.Error:
			# Shouldn't happen.
			# Go back to the one that didn't fail.
			load_archive(idx + 1)

		for x in range(0, position):
			a.__next__()
	else:
		position = 0

	archive_index = idx

# Load the first archive.
load_archive(0)

# Initialize graphics
window = pyglet.window.Window(fullscreen=True)
img = None

def load_image(buff, filename):
	global img

	# Since the images are taller than large, we need to rotate them
	# by 90° to be visible on monitors, which are wider than tall.
	f = io.BytesIO(buff)
	img = pyglet.sprite.Sprite(pyglet.image.load(filename, file=f))
	img.scale = float(window.height) / float(img.image.width)
	img.set_position(img.image.height * img.scale, 0)
	img.rotation = -90.0

def load_next_image():
	global a
	global position

	try:
		element = a.__next__()
		position += 1
	except StopIteration:
		load_archive(archive_index + 1)
		load_next_image()
		return

	buff = element.read()

	if len(buff) > 0:
		load_image(buff, element.filename)
	else:
		load_next_image()	

def load_prev_image():
	global a
	global position
	global idx
	
	if position <= 1:
		load_archive(archive_index - 1)
		load_next_image()
	else:
		position -= 1
	
		try:
			a = iter(archive.Archive(archives[archive_index]))
		except archive.core.Error:
			# This is really bad :/
			# Skip to next archive.
			load_archive(archive_index + 1)

		element = a.__next__()

		for i in range(1, position):
			element = a.__next__()

		buff = element.read()
		
		if len(buff) > 0:
			load_image(buff, element.filename)
		else:
			load_prev_image()

# Load the first image of the archive.
load_next_image()

# Just the callbacks we need for pyglet.
@window.event
def on_draw():
	window.clear()

	if img is not None:	
		img.draw()

@window.event
def on_key_press(symbol, modifiers):
	# 'q' or escape exit.
	if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.ESCAPE:
		sys.exit(0)
	# Only left gets the previous one.
	elif symbol == pyglet.window.key.LEFT:
		load_prev_image()
	# All others go to the next image.
	else:
		load_next_image()

# And go!
pyglet.app.run()
