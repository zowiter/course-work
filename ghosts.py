# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:32:47 2021

@author: eveli
"""

import pygame
from movement import Entity
from const import *
from vector import Vector2
from random import randint
from chasing import Mode
from stack import Stack

class Ghost(Entity):
    def __init__(self, nodes):
        Entity.__init__(self, nodes)
        self.name = "ghost"
        self.goal = Vector2()
        self.points = 200
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0


    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.forceBacktrack())
        return validDirections

    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]

    def getClosestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction*TILEWIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]

    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            self.portal()
            validDirections = self.getValidDirections()
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT

    def portalSlowdown(self):
        self.speed = 100
        if self.node.portalNode or self.target.portalNode:
            self.speed = 50

    def setupModeStack(self):
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", time=5))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        return modes

    def freightMode(self):
        if self.mode.name != "SPAWN":
            if self.mode.name != "FREIGHT":
                if self.mode.time is not None:
                    dt = self.mode.time - self.modeTimer
                    self.modeStack.push(Mode(name=self.mode.name, time=dt))
                else:
                    self.modeStack.push(Mode(name=self.mode.name))
                self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
                self.modeTimer = 0
            else:
                self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
                self.modeTimer = 0
            self.reverseDirection()

    def randomGoal(self):
        x = randint(0, NCOLS * TILEWIDTH)
        y = randint(0, NROWS * TILEHEIGHT)
        self.goal = Vector2(x, y)

    def scatterGoal(self):
        self.goal = Vector2(SCREENSIZE[0], 0)

    def chaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position

    def modeUpdate(self, dt):
        self.modeTimer += dt
        if self.mode.time is not None:
            if self.modeTimer >= self.mode.time:
                self.reverseDirection()
                self.mode = self.modeStack.pop()
                self.modeTimer = 0

    def update(self, dt, pacman, blinky=None):
        self.visible = True
        self.portalSlowdown()
        speedMod = self.speed * self.mode.speedMult
        self.position += self.direction*speedMod*dt
        self.modeUpdate(dt)
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman, blinky)
        elif self.mode.name == "SCATTER":
            self.scatterGoal()
        elif self.mode.name == "FREIGHT":
            self.randomGoal()
        self.moveBySelf()

    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node
        self.setPosition()

class Blinky(Ghost):
    def __init__(self, nodes):
        Ghost.__init__(self, nodes)
        self.name = "blinky"
        self.color = RED
        self.setStartPosition()

    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.blinkyStartNode:
                return node
        return None

class Pinky(Ghost):
    def __init__(self, nodes):
        Ghost.__init__(self, nodes)
        self.name = "pinky"
        self.color = PINK
        self.setStartPosition()

    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.pinkyStartNode:
                return node
        return None

    def scatterGoal(self):
        self.goal = Vector2()

    def chaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position + pacman.direction * TILEWIDTH * 4

class Inky(Ghost):
    def __init__(self, nodes):
        Ghost.__init__(self, nodes)
        self.name = "inky"
        self.color = TEAL
        self.setStartPosition()

    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.inkyStartNode:
                return node
        return None

    def scatterGoal(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chaseGoal(self, pacman, blinky=None):
        vec1 = pacman.position + pacman.direction * TILEWIDTH * 2
        vec2 = (vec1 - blinky.position) * 2
        self.goal = blinky.position + vec2

class Clyde(Ghost):
    def __init__(self, nodes):
        Ghost.__init__(self, nodes)
        self.name = "clyde"
        self.color = ORANGE
        self.setStartPosition()

    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.clydeStartNode:
                return node
        return None

    def scatterGoal(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chaseGoal(self, pacman, blinky=None):
        d = pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatterGoal()
        else:
            self.goal = pacman.position + pacman.direction * TILEWIDTH * 4

class GhostGroup(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes), Pinky(nodes), Inky(nodes), Clyde(nodes)]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt, pacman):
        for ghost in self:
            ghost.update(dt, pacman, self.ghosts[0])

    def freightMode(self):
        for ghost in self:
            ghost.freightMode()

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)


