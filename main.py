#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
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

# Standard Libs
import os
import sys

# 3rd Party Modules
import pygame
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Local Modules
import game
import scene

def main(args):
	# Initialize display, input, sound, and initialize shared data
	pygame.init()
	game.clock = pygame.time.Clock()
	game.screen = pygame.display.set_mode((game.SCREEN_WIDTH(), game.SCREEN_HEIGHT()), pygame.DOUBLEBUF)
	pygame.display.set_caption('pydungeon')
	pygame.key.set_repeat(300, 10)
	
	# we always start with the main scene
	game.scene = scene.NewScene("main.txt")
	
	# game loop
	while game.run == 1:
		# Execute the scene
		newscene = game.scene.execute()
		# Load a new scene if required
		if newscene is not None:
			game.scene = scene.NewScene(newscene)
		# Draw the scene
		game.screen.fill(game.FILL_COLOR())
		game.scene.draw()
		pygame.display.flip()
		# Time base
		game.clock.tick(30)
			
	# exit
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
	pygame.quit()

