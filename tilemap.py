#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  character.py
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

import os
import sys
import collections

import pygame

TileDef = collections.namedtuple('TileDef', ['row', 'col', 'wall'])

class CreateMap(pygame.Surface):
     
    def __init__(self, name):
		# Load tilemap defintion file
		fullname = os.path.join('maps', name)
		try:
			file = open(fullname, 'r')
		except pygame.error, message:
			print 'Cannot load tilemap:', name
			raise SystemExit, message
		self.tiledef = []
		defcnt = 0
		gridcnt = 0
		dofill = 0
		for line in file:
			if len(line) > 1:
				if line[0] == '$':
					tilefile = os.path.join('tiles', line[1:].strip())
				if line[0] == '!':
					tiledat = line[1:].strip().split();
					self.tiledef.append(TileDef._make([int(i) for i in tiledat]))
					print 'TILE', defcnt, ': ', self.tiledef[defcnt]
					defcnt += 1
				elif line[0] == 'F':
					fillsrc = pygame.Rect([int(i) for i in line[1:].strip().split(',')])
					dofill = 1
					print 'FILL: ', fillsrc
				elif line[0] == '@':
					size = line[1:].strip().split(',')
					self.tileWidth = int(size[0])
					self.tileHeight = int(size[1])
					self.gridHeight = int(size[2])
					self.gridWidth = int(size[3])
					self.griddef = [[0 for x in range(self.gridWidth)] for x in range(self.gridHeight)]
				elif line[0] == ':':
					c = 0
					for tile in line[1:].strip().split(' '):
						self.griddef[gridcnt][c] = int(tile)
						c += 1
					print 'GRID: ', self.griddef[gridcnt]
					gridcnt += 1
		file.close()
		
		# Load tile surfaces (temporary)
		src = pygame.image.load(tilefile).convert_alpha()
			
		# Create surface to hold rendered map
		pygame.Surface.__init__(self, size=(self.tileWidth * self.gridWidth, self.tileHeight * self.gridHeight))

		# Fill surface with background
		if dofill != 0:
			rows = (self.tileHeight * self.gridHeight) / fillsrc.height
			cols = (self.tileWidth * self.gridWidth) / fillsrc.width
			for r in range(rows):
				for c in range(cols):
					self.blit(src, (c * fillsrc.width, r * fillsrc.height), fillsrc)
			
		# Draw tiles into surface
		for r in range(self.gridHeight):
			for c in range(self.gridWidth):
				t = self.griddef[r][c]
				rect = pygame.Rect(self.tiledef[t].col * self.tileWidth, self.tiledef[t].row * self.tileHeight, self.tileWidth, self.tileHeight)
				self.blit(src, (c * self.tileWidth, r * self.tileHeight), rect)
				
		
