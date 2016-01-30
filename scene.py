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
import mob
import hero
import monster
import effect

class NewScene():
	
	def execute(self):
		# Process pending events
		for event in pygame.event.get():
			if hasattr(event, 'key') and event.type == pygame.KEYDOWN:
				# One time operations
				if event.key == pygame.K_SPACE:
					game.player.jump()
				elif event.key == pygame.K_ESCAPE:
					game.run = 0
				elif event.key == pygame.K_r:
					# reload map
					self.mainmap = tilemap.NewMap("level1.txt")
			elif hasattr(event, 'button') and event.type == pygame.MOUSEBUTTONDOWN:
				# Mouse buttons (left = 1, right = 3, wheel up = 4, wheel down = 5)
				if event.button == 1:
					game.player.attack(mob.ATTACK_PRIMARY)
				elif event.button == 3:
					game.player.attack(mob.ATTACK_SECONDARY)
			elif event.type == pygame.QUIT:
				game.run = 0 

		# Process move keys (only one can work)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			game.player.move(mob.MOVE_RIGHT)
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			game.player.move(mob.MOVE_LEFT)
		elif keys[pygame.K_UP] or keys[pygame.K_w]:
			game.player.move(mob.MOVE_UP)
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			game.player.move(mob.MOVE_DOWN)
			
		# Process attack keys (only one can work)
		if keys[pygame.K_1]:
			game.player.attack(mob.ATTACK_PRIMARY)
		if keys[pygame.K_2]:
			game.player.attack(mob.ATTACK_SECONDARY)
		if keys[pygame.K_3]:
			game.player.attack(mob.ATTACK_AUX1)
		if keys[pygame.K_4]:
			game.player.attack(mob.ATTACK_AUX2)

		# Update components (order is important)
		game.player.update()
		for effect in self.effects:
			effect.update()
		for monster in self.monsters:
			monster.update()
		self.mainmap.update()
			
		# Return new scene (if required)
		return None

	def draw(self):
		# Draw components (order is important)
		self.mainmap.draw()
		for effect in self.effects:
			effect.update()
		for monster in self.monsters:
			monster.update()
		game.player.draw()

	def tilemap(self):
		return self.mainmap
		
	def __init__(self, name):
		self.effects = []
		self.monsters = []
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
				elif line[0] == 'M':
					# play music file
					pass
				elif line[0] == 'S':
					# assign start location in pixels
					tilex, tiley = [int(i) for i in line[1:].strip().split(',')]
					tilew, tileh = self.mainmap.tilesize()
					framew, frameh = game.player.framesize()
					pixelx = (tilew * tilex) + (tilew / 2) - (framew / 2)
					pixely = tileh * (tiley + 1) - frameh
					game.player.setStartPos(pixelx, pixely)
				elif line[0] == 'E':
					# load exit list
					pass
				elif line[0] == 'M':
					# load monster list
					pass
		file.close()

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()
