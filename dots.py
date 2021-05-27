# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:48:26 2021

@author: eveli
"""

import pygame
from vector import Vector2
from const import *


class Dot(object):
    def __init__(self, x, y):
        self.name = "dot"
        self.position = Vector2(x, y)
        self.color = WHITE
        self.radius = 5
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class DotGroup(object):
    def __init__(self, dotfile):
        self.dotList = []
        self.createDotList(dotfile)


    def createDotList(self, dotfile):
        grid = self.readDotfile(dotfile)
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 'p':
                    self.dotList.append(Dot(col * TILEWIDTH, row * TILEHEIGHT))

    def readDotfile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    def isEmpty(self):
        if len(self.dotList) == 0:
            return True
        return False

    def render(self, screen):
        for dot in self.dotList:
            dot.render(screen)

