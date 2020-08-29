# -*- coding: utf-8 -*-
import random
from typing import TypedDict, List, NamedTuple

import pygame as pg

from utils import getAttributes
class gameObject():

    objList = list()

    def __init__(self, x : int, y : int, w : int, h : int, color : str):

        self.rect = pg.rect.Rect(x, y, w, h)
        self.color = color
        gameObject.objList.append(self)

    def update(self):
        pass
    
    def draw(self, screen):
        pg.draw.rect(screen, pg.Color(self.color), self.rect)

class Status(NamedTuple):
    # energie
    maxFuel : float         # maximum fuel capacity
    fuel : float            # current fuel
    fuelPerPower : float    # d fuel / power
    
    # power and speed
    powerPerTime : float    # power of the machine
    tempPerPower : float    # d temperature / power
    speedPerPower : float   # d speed / power
    
    # temperature
    temperature : float     # current temperature
    maxTemp : float         # maximum temparature before overheat
    isOverHeat : bool       # if true machine will slow down

    # mass
    machineMass : float            # mass of the machine
    fuelMass : float        # mass of the fuel
    fuelMassPerFuel : float # d mass fuel / fuel

    def print(self):
        n = 0
        for i in self._fields:
            print(i.ljust(8) +"\t:"+ str(self[n]))
            n += 1


class Machine(gameObject):

    machines = list()
    
    def __init__(self,  x : int, y : int, w : int, h : int, color : str, status):
        super().__init__(x, y, w, h, color)
        self.status = status
        Machine.machines.append(self)
    
    def update(self):
        self.rect.x += random.randint(0,1)
        self.rect.y += random.randint(0,1)
        self.rect.x -= random.randint(0,1)
        self.rect.y -= random.randint(0,1)

    def createMachine( 
                    x : int,
                    y : int,
                    w : int,
                    h : int,
                    color : str,
                    maxFuel : float,
                    fuel : float,
                    fuelPerPower : float,
                    powerPerTime : float,
                    tempPerPower : float,
                    speedPerPower : float,
                    temperature : float,
                    maxTemp : float,
                    isOverHeat : bool,
                    machineMass : float,
                    fuelMass : float,
                    fuelMassPerFuel : float):

                s = Status(
                    maxFuel,
                    fuel,
                    fuelPerPower,
                    powerPerTime,
                    tempPerPower,
                    speedPerPower,
                    temperature,
                    maxTemp,
                    isOverHeat,
                    machineMass,
                    fuelMass,
                    fuelMassPerFuel)
                
                return Machine(x, y, w, h, color, s)
    
    def createRandomStatusMachine(sWidth : int, sHeight : int):

        # pos scale and color
        MIN_WIDTH = 10
        MAX_WIDTH = 100
        MIN_HEIGHT = 10
        MAX_HEIGHT = 100

        w = random.randint(MIN_WIDTH, MAX_WIDTH)
        h = random.randint(MIN_HEIGHT, MAX_HEIGHT)
        x = random.randint(0, sWidth - w)
        y = random.randint(0, sHeight - h)

        COLORS = [
            "red",
            "green",
            "blue",
            "yellow",
            "pink",
            "purple",
            "cyan"
        ]
        color = random.choice(COLORS)

        # status
        maxFuel = random.uniform(1.0e5, 1.0e10)
        maxTemp = random.uniform(350.0, 500.0)
        
        machineMass = w * h * 10

        fuel = maxFuel

        mini = 0.1
        maxi = 1.0

        fuelPerPower = random.uniform(mini, maxi)
        powerPerTime = random.uniform(mini, maxi)
        tempPerPower = random.uniform(mini, maxi)
        speedPerPower = random.uniform(mini, maxi)
        fuelMassPerFuel = random.uniform(mini, maxi)

        temperature = 0.0

        isOverHeat = False

        fuelMass = fuel * fuelMassPerFuel




        return Machine.createMachine(x, y, w, h, 
                    color, 
                    maxFuel, 
                    fuel, 
                    fuelPerPower,
                    powerPerTime,
                    tempPerPower,
                    speedPerPower,
                    temperature,
                    maxTemp,
                    isOverHeat,
                    machineMass,
                    fuelMass,
                    fuelMassPerFuel
        )

