# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:49:31 2021

@author: eveli
"""
#Все, что нужно для запуска игры


import pygame
from pygame.locals import *
from pacman import Pacman
from nodes import NodeGroup
from vector import Vector2
from const import *
from ghosts import GhostGroup

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
        self.ghosts = GhostGroup(self.nodes)
        self.gameover = False

    
    def update(self):
        if not self.gameover:
            dt = self.clock.tick(30) / 1000.0
            self.pacman.update(dt)
            self.ghosts.update(dt, self.pacman)
        self.checkGhostEvents()
        self.checkEvents()
        self.render()

    def checkGhostEvents(self):
        ghost = self.pacman.eatGhost(self.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                ghost.spawnMode(speed=2)
                self.pacman.visible = False
                ghost.visible = False
            elif ghost.mode.name == "CHASE" or ghost.mode.name == "SCATTER":
                #self.pacman.loseLife()
                exit()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.gameover:
                        self.startGame()

    def restartLevel(self):
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes)

    #def resolveDeath(self):
        #if self.pacman.lives == 0:
            #self.gameover = True
        #else:
            #self.restartLevel()


    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        #self.pacman.renderLives(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
