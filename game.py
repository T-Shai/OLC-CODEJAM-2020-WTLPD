# -*- coding: utf-8 -*-
import pygame as pg

from window import *
from machine import *

class Game(Window):

    def __init__(self, name, width, height, icon = None):
        super().__init__( name, width, height, icon )

        # SETUP
        for _ in range(10):
            Machine.createRandomStatusMachine(width, height)
        
    def update(self):
        for m in Machine.machines:
            m.update()

    def draw(self):
        for m in Machine.machines:
            m.draw(self.getScreen())


if __name__ == "__main__":
    
    # constants
    wTitle = "OLC CODEJAM 2020 - SAI#8680"
    fillColor = "black"
    WIDTH = 1200
    HEIGHT = int(WIDTH * 9 / 16)
    
    # game 
    g = Game(wTitle, WIDTH, HEIGHT)
    g.setFillColor(name=fillColor)
    g.setFPS(30)

    g.loop()