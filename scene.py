#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  scene.py
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
import game
import tilemap
import hero
import monster
import effect

class NewScene():
	
	def __init__(self, name):
		# Load tilemap defintion file
		temp = os.path.join('scenes', name)
		try:
			file = open(temp, 'r')
		except pygame.error, message:
			print 'Cannot load scene:', name
			raise SystemExit, message
		for line in file:
			if len(line) > 1:
				if line[0] == 'T':
				# load a tile map
					self.mainmap = tilemap.NewMap(line[1:].strip())
				if line[0] == 'S':
					# assign start location
					pass
				elif line[0] == 'E':
					# load exit list
					pass
				elif line[0] == 'M':
					# load monster list
					pass
		file.close()

	def execute(self):
		dx = 0
		dy = 0
		for event in pygame.event.get():
			if hasattr(event, 'key') and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					# reload map
					self.mainmap = tilemap.NewMap("level1.txt")
				if event.key == pygame.K_RIGHT:
					dx -= 1
				elif event.key == pygame.K_LEFT:
					dx += 1
				elif event.key == pygame.K_UP:
					dy += 1
				elif event.key == pygame.K_DOWN:
					dy -= 1
				elif event.key == pygame.K_ESCAPE:
					game.run = 0
			elif event.type == pygame.QUIT:
				game.run = 0 

		if dx != 0 or dy != 0:
			self.mainmap.scroll(dx,dy)

	def draw(self):
		self.mainmap.draw()
		pygame.display.flip()

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()
