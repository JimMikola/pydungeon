#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hero.py
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
import mob

# Hero class
class NewHero(mob.Mob):
		
	def update(self):
		dx = self.x
		dy = self.y
		mob.Mob.update(self)
		dx -= self.x
		dy -= self.y
		# if hero is not in center of screen then don't scroll
		herox, heroy = game.player.drawpos()
		if (dx > 0):
			# moving left
			if herox > (game.SCREEN_WIDTH() / 2):
				dx = 0
		elif (dx < 0):
			# moving right
			if herox < (game.SCREEN_WIDTH() / 2):
				dx = 0
		if (dy > 0):
			# moving up
			if heroy > (game.SCREEN_HEIGHT() / 2):
				dy = 0
		elif (dy < 0):
			# moving down
			if heroy < (game.SCREEN_HEIGHT() / 2):
				dy = 0
		game.scene.tilemap().scroll(dx, dy)

	def setStartPos(self,x,y):
		# x and y are in pixels
		self.x = x
		self.y = y
		
	def __init__(self, name):
		# Calculate file path
		temp = os.path.join('heroes', name)
		# Allow base class to load file first
		mob.Mob.__init__(self, temp, 0, 0)
		# Reprocess file for class specific data
		try:
			file = open(temp, 'r')
		except pygame.error, message:
			raise SystemExit, message
		for line in file:
			pass
		file.close()

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()
