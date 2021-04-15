# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 19:40:36 2021

@author: eveli
"""

from vector import Vector2

TILEWIDTH = 16
TILEHEIGHT = 16
NROWS = 36
BLACK = (0, 0, 0)
NCOLS = 28
SCREENWIDTH = NCOLS*TILEWIDTH
SCREENHEIGHT = NROWS*TILEHEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
STOP = Vector2()
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
RIGHT = Vector2(1, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LEFT = Vector2(-1, 0)