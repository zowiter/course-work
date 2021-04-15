# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:41:03 2021

@author: eveli
"""

class Mode(object):
    def __init__(self, name="", time=None, speedMult=1, direction=None):
        self.name = name
        self.time = time
        self.speedMult = speedMult
        self.direction = direction