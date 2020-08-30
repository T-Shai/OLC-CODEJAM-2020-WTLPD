# -*- coding: utf-8 -*-
import pygame as pg

from window import *
from machine import *
from ga import *

class Game(Window):

    def __init__(self, name, width, height, icon = None):
        super().__init__( name, width, height, icon )

        # SETUP
        # reward 
        Machine.rewards.append(Reward(width/2, height/2, 25, 25, "red", self))
        
        self.gen = GA(80, 0.01, self)
        
        
        
        
    def update(self):
        self.gen.update()
        

    def draw(self):
        self.gen.draw()

if __name__ == "__main__":
    
    # constants
    wTitle = "OLC CODEJAM 2020 - SAI#8680"
    fillColor = "black"
    WIDTH = 1200
    HEIGHT = 600
    
    # game 
    g = Game(wTitle, WIDTH, HEIGHT)
    g.setFillColor(name=fillColor)
    g.setFPS(60)

    g.loop()