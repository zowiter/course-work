# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:49:31 2021

@author: eveli
"""
#Создание окна, где будет все происходить :)


import pygame
from pygame.locals import *
from pacman import Pacman
from nodes import NodeGroup
from vector import Vector2
from const import *
from ghosts import Ghost


class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.nodes = NodeGroup("maze.txt")
        self.pacman = Pacman(self.nodes)
        self.ghost = Ghost(self.nodes)

    
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt, self.pacman)
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
