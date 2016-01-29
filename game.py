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

# Local Modules
import main

# Constants
def SCREEN_WIDTH():
	return 640
	
def SCREEN_HEIGHT():
	return 480

def FILL_COLOR():
	return (0,0,0)
			
# pygame Surface assigned to the display
screen = None

# pygame clock
clock = None

# current scene in play
scene = None

# GUI overlay for the screen
gui = None

# current score
score = 0

# current hero list (persists from screen to screen)
heroes = []

# quit flag
run = 1

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()


