#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
#  
#  Copyright 2016 Jim Mikola
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# Standard Modules
import os
import sys

# 3rd Party Modules
import pygame

# Local Modules
import main
import hero

# Constants
def SCREEN_WIDTH():
	return 640
	
def SCREEN_HEIGHT():
	return 480

def FILL_COLOR():
	return (0,0,0)

def GRAVITY():
	return 1
				
# pygame Surface assigned to the display
screen = None

# pygame clock
clock = None

# current scene in play
scene = None

# GUI overlay for the screen
overlay = None

# current score
score = 0

# current player (persists from screen to screen)
player = None

# draw step
drawstep = 0

# quit flag
run = 1

# Load Game API
def Load(name):
	# Identify globals from 'game.py' that we are using
	global player
	# Load tilemap defintion file
	temp = os.path.join('saves', name)
	try:
		file = open(temp, 'r')
	except pygame.error, message:
		print 'Cannot load game:', name
		raise SystemExit, message
	for line in file:
		if len(line) > 1:
			if line[0] == 'H':
				# load hero type
				player = hero.NewHero(line[1:].strip())
	file.close()

# Save Game API
def Save(name):
	# Identify globals from 'game.py' that we are using
	global player
	
# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()


