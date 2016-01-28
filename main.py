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

import os
import sys
import pygame

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

import character
import tilemap

def main(args):
    pygame.init()

    clock = pygame.time.Clock()
    size = width, height = 640, 480
    black = 0, 0, 0

    screen = pygame.display.set_mode((size), pygame.DOUBLEBUF)
    pygame.display.set_caption('Hello Pygame World!')
    pygame.key.set_repeat(300, 10)
    
    # load a tile map
    mainmap = tilemap.CreateMap("level1.txt")
    mainmap.draw(screen)
    pygame.display.flip()
    
    while 1:
        dx = 0
        dy = 0
        for event in pygame.event.get():
            if hasattr(event, 'key') and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # reload map
                    mainmap = tilemap.CreateMap("level1.txt")
                    mainmap.draw(screen)
                    pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    dx -= 1
                elif event.key == pygame.K_LEFT:
                    dx += 1
                elif event.key == pygame.K_UP:
                    dy += 1
                elif event.key == pygame.K_DOWN:
                    dy -= 1
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
            elif event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit()

        if dx != 0 or dy != 0:
            mainmap.scroll(dx,dy)

        screen.fill(black)
        mainmap.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

