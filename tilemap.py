#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tilemap.py
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
import collections

# 3rd Party Modules
import pygame

# Local Modules
import main
import game


# Named types
TileDef = collections.namedtuple('TileDef', ['row', 'col', 'wall'])
TokenDef = collections.namedtuple('TokenDef', ['surf', 'width', 'height', 'x', 'y', 'frame'])

# Wall types
WALL_NONE, WALL_BLOCK, WALL_CLIMB = range(3)


class NewMap(pygame.Surface):

	def scroll(self, dx, dy):
		self.x += dx
		self.y += dy
		
	def update(self):
		# bound offset by screen - order forces top left corner
		# to be dominant for maps that are smaller than the 
		# screen
		width, height = self.drawsize()
		if ((self.x + width) < game.SCREEN_WIDTH()):
			self.x = game.SCREEN_WIDTH() - width
		if (self.x > 0):
			self.x = 0
		if ((self.y + height) < game.SCREEN_HEIGHT()):
			self.y = game.SCREEN_HEIGHT() - height
		if (self.y > 0):
			self.y = 0
		
	def draw(self):
		# Map
		rect = self.get_rect().move(self.x, self.y)
		game.screen.blit(self, rect)
		# Tokens
		for token in self.tokendef:
			x = (game.drawstep * token.frame) % token.width
			rect = pygame.Rect(x, 0, token.frame, token.height)
			game.screen.blit(token.surf, ((token.x + self.x), (token.y + self.y)), rect)

	def drawoffset(self):
		return (self.x, self.y)

	def drawsize(self):
		return (self.tileWidth * self.gridWidth, self.tileHeight * self.gridHeight)
		
	def tilesize(self):
		return (self.tileWidth, self.tileHeight)
		
	def gridsize(self):
		return (self.gridWidth, self.gridHeight)

	def collision(self, rect):
		# Start with zero collision
		dx, dy = 0, 0
		# perform edge checks, protect for excessive velocity
		# Check left
		col = rect.left / self.tileWidth
		row = rect.centery / self.tileHeight
		if col < 0:
			col = 0
		if self.tiledef[self.griddef[row][col]].wall == WALL_BLOCK:
			# collision, move right
			dx += ((col + 1) * self.tileWidth) - rect.left
		# Check right
		col = (rect.right - 1) / self.tileWidth
		if col >= self.gridWidth:
			col = self.gridWidth - 1
		if self.tiledef[self.griddef[row][col]].wall == WALL_BLOCK:
			# collision, move left
			dx -= rect.right - (col * self.tileWidth)
		# Check bottom
		col = rect.centerx / self.tileWidth
		row = (rect.bottom - 1) / self.tileHeight
		if row >= self.gridHeight:
			row = self.gridHeight - 1
		if self.tiledef[self.griddef[row][col]].wall == WALL_BLOCK:
			# collision, move up
			dy -= rect.bottom - (row * self.tileHeight)
		# Check top
		row = rect.top / self.tileHeight
		if row < 0:
			row = 0
		if self.tiledef[self.griddef[row][col]].wall == WALL_BLOCK:
			# collision, move down
			dy += ((row + 1) * self.tileHeight) - rect.top
		# return collision pixel values
		return (dx, dy)
		
	def climb(self, rect):
		# rect is in map pixel coords
		col = rect.centerx / self.tileWidth
		# Check upward climb (feet must be on climbing tile)
		row = (rect.bottom - 1) / self.tileHeight
		tile = self.griddef[row][col]
		if self.tiledef[tile].wall == WALL_CLIMB:
			climbup = 1
		else:
			climbup = 0
		# Check downward climb (one pixel below feet must be on climbing tile)
		row = rect.bottom / self.tileHeight
		tile = self.griddef[row][col]
		if self.tiledef[tile].wall == WALL_CLIMB:
			climbdn = 1
		else:
			climbdn = 0
		return (climbup, climbdn)
		
	def __init__(self, name):
		self.x = 0
		self.y = 0
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

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()
