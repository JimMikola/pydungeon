#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mob.py
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

# Enumeration of move commands
MOVE_NONE, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, MOVE_JUMP = range(6)

# Enumeration of attack commands
ATTACK_NONE, ATTACK_PRIMARY, ATTACK_SECONDARY, ATTACK_AUX1, ATTACK_AUX2 = range(5)

# base class for all mobiles in the game
class Mob():
    	
	def move(self, command):
		self.move_cmd = command

	def attack(self, command):
		self.attack_cmd = command

	def jump(self):
		self.jump_cmd = MOVE_JUMP
		
	def update(self):
		# Get our region on map
		rect = pygame.Rect(self.x, self.y, self.framew, self.frameh)
		# check if we can climb
		climbup, climbdn = game.scene.tilemap().climb(rect)
		# update position
		dx, dy = 0, 0
		if self.move_cmd == MOVE_RIGHT:
			dx += self.move_step
		elif self.move_cmd == MOVE_LEFT:
			dx -= self.move_step
		elif self.move_cmd == MOVE_UP and 0 != climbup:
			dy -= self.move_step
		elif self.move_cmd == MOVE_DOWN and 0 != climbdn:
			dy += self.move_step
		if self.jump_cmd == MOVE_JUMP and 0 == self.velocity:
			self.velocity -= self.jumpvel
		# gravity (if not climbing)
		if 0 == climbdn:
			self.velocity += game.GRAVITY()
			dy += self.velocity
		else:
			self.velocity = 0
		# finsh move command
		rect.move_ip(dx, dy)
		self.move_cmd = MOVE_NONE
		self.jump_cmd = MOVE_NONE
		# check for collision with wall
		dx, dy = game.scene.tilemap().collision(rect)
		rect.move_ip(dx, dy)
		if 0 != dy:
			self.velocity = 0
		# commit position change
		self.x = rect.left
		self.y = rect.top

	def framesize(self):
		return (self.framew, self.frameh)

	def drawpos(self):
		screenx, screeny = game.scene.tilemap().drawoffset()
		return (screenx + self.x, screeny + self.y)

	def draw(self):
		rect = pygame.Rect(self.framex, self.framey, self.framew, self.frameh)
		screenx, screeny = game.scene.tilemap().drawoffset()
		game.screen.blit(self.surf, self.drawpos(), rect)

	def __init__(self, name, x, y):
		self.x = x
		self.y = y
		self.jump_cmd = 0
		self.jumpvel = 0
		self.move_cmd = MOVE_NONE
		self.attack_cmd = ATTACK_NONE
		self.can_fall = 0
		self.can_climb = 0
		self.framex = 0
		self.framey = 0
		self.move_step = 0
		self.velocity = 0
		try:
			file = open(name, 'r')
		except pygame.error, message:
			print 'Cannot load mob:', name
			raise SystemExit, message
		for line in file:
			if len(line) > 1:
				if line[0] == 'J':
					# assign jump velocity
					self.jumpvel = int(line[1:].strip())
				elif line[0] == 'F':
					# assign fall flag
					if 0 != int(line[1:].strip()):
						self.can_fall = 1
				elif line[0] == 'C':
					# assign climb flag
					if 0 != int(line[1:].strip()):
						self.can_climb = 1
				elif line[0] == 'M':
					# assign move step
					self.move_step = int(line[1:].strip())
					if (self.move_step < 0):
						self.move_step = 0
				elif line[0] == 'T':
					# texture data
					lines = line[1:].strip().split(',')
					mobfile = os.path.join('mobs', lines[0].strip())
					self.surf = pygame.image.load(mobfile).convert_alpha()
					self.framew = int(lines[1].strip())
					self.frameh = int(lines[2].strip())
		file.close()

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()
