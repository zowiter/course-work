# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:12:55 2021

@author: eveli
"""

import math

class Vector2(object):
    # x, y - это координаты, на которые указывает вектор.
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
    #следующие 6 функций-методов - арифметические операции с векторами 
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)
#устанавливает равенство векторов, т.е. например, вектор с координатами (4,1) будет эквивалентен
#вектору с координатами (4.000001, 1.000001)
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def __hash__(self):
        return id(self)
#для сравнивания векторов нам нужна его длина 
    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    def dot(self, other):
        return self.x*other.x, self.y*other.y

    def copy(self):
        return Vector2(self.x, self.y)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return self.__div__(mag)
        return None

    def asTuple(self):
        return self.x, self.y
    
    def asInt(self):
        return int(self.x), int(self.y)
