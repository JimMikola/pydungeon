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

# base class for all mobiles in the game
class Mob():
	
    def draw(self, screen):
		self.drawstep += 1

    def move(self, tilemap, dx, dy):
		newx = self.x + dx
		newy = self.y + dy
		
    def __init__(self, name, x, y):
		self.x = x
		self.y = y
		self.drawstep = 0

# If starting in this module, jump to main
if __name__ == '__main__':
	sys.exit(main.main(sys.argv))
	pygame.quit()