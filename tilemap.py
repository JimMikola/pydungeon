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
TokenDef = collections.namedtuple('TokenDef', ['surf', 'width', 'height', 'x', 'y', 'frame'])

class CreateMap(pygame.Surface):

    def scroll(self, dx, dy):
		self.x += dx * self.tileWidth
		self.y += dy * self.tileHeight

    def draw(self, screen):
		# Map
		rect = self.get_rect().move(self.x, self.y)
		screen.blit(self, rect)
		# Tokens
		for token in self.tokendef:
			x = (self.drawstep * token.frame) % token.width
			rect = pygame.Rect(x, 0, token.frame, token.height)
			screen.blit(token.surf, ((token.x + self.x), (token.y + self.y)), rect)
		# Finish
		self.drawstep += 1 

    def __init__(self, name):
		self.x = 0
		self.y = 0
		self.drawstep = 0
		# Load tilemap defintion file
		temp = os.path.join('maps', name)
		try:
			file = open(temp, 'r')
		except pygame.error, message:
			print 'Cannot load tilemap:', name
			raise SystemExit, message
		self.tiledef = []
		self.tokendef = []
		decor = []
		gridcnt = 0
		fillrect = pygame.Rect(0,0,0,0)
		lastsrc = ""
		for line in file:
			if len(line) > 1:
				if line[0] == '$':
					tilefile = os.path.join('tiles', line[1:].strip())
				if line[0] == '!':
					temp = line[1:].strip().split();
					self.tiledef.append(TileDef._make([int(i) for i in temp]))
					temp = len(self.tiledef) - 1
				elif line[0] == 'F':
					fillrect = pygame.Rect([int(i) for i in line[1:].strip().split(',')])
				elif line[0] == 'A':
					temp = line[1:].strip().split(',');
					newsrc = os.path.join('tiles', temp[0].strip())
					if newsrc != lastsrc:
						src = pygame.image.load(newsrc).convert_alpha()
						lastsrc = newsrc
						rect = src.get_rect()
					self.tokendef.append(TokenDef._make([src,rect.width,rect.height,int(temp[2]),int(temp[3]),int(temp[1])]))
					temp = len(self.tokendef) - 1
				elif line[0] == 'B':
					decor.append(line[1:].strip())
				elif line[0] == '@':
					temp = line[1:].strip().split(',')
					self.tileWidth = int(temp[0].strip())
					self.tileHeight = int(temp[1].strip())
					self.gridHeight = int(temp[2].strip())
					self.gridWidth = int(temp[3].strip())
					self.griddef = [[0 for x in range(self.gridWidth)] for x in range(self.gridHeight)]
				elif line[0] == ':':
					c = 0
					for tile in line[1:].strip().split():
						self.griddef[gridcnt][c] = int(tile.strip())
						c += 1
					gridcnt += 1
		file.close()
		
		# Load tile surfaces (temporary)
		src = pygame.image.load(tilefile).convert_alpha()
			
		# Create surface to hold rendered map
		pygame.Surface.__init__(self, (self.tileWidth * self.gridWidth, self.tileHeight * self.gridHeight))

		# Fill surface with background
		if fillrect.width > 0 and fillrect.height > 0:
			rows = (self.tileHeight * self.gridHeight) / fillrect.height
			cols = (self.tileWidth * self.gridWidth) / fillrect.width
			for r in range(rows):
				for c in range(cols):
					self.blit(src, (c * fillrect.width, r * fillrect.height), fillrect)
		
		# Draw tiles into surface
		for r in range(self.gridHeight):
			for c in range(self.gridWidth):
				t = self.griddef[r][c]
				rect = pygame.Rect(self.tiledef[t].col * self.tileWidth, self.tiledef[t].row * self.tileHeight, self.tileWidth, self.tileHeight)
				self.blit(src, (c * self.tileWidth, r * self.tileHeight), rect)
        
		# Draw decor
		lastsrc = ""
		for d in decor:
			items = d.split(',')
			newsrc = os.path.join('tiles', items[0].strip())
			if newsrc != lastsrc:
				src = pygame.image.load(newsrc).convert_alpha()
				lastsrc = newsrc
			rect = pygame.Rect(int(items[1]), int(items[2]), int(items[3]), int(items[4]))
			self.blit(src, (int(items[5]), int(items[6])), rect)
