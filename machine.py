# -*- coding: utf-8 -*-
import random
import math
from typing import TypedDict, List, NamedTuple

import pygame as pg

from utils import *

class gameObject():

    objList = list()

    def __init__(self, x : int, y : int, w : int, h : int, color : str, game):

        self.game = game

        self.rect = pg.rect.Rect(x, y, w, h)
        self.fpos = (x*1.0, y*1.0)
        self.color = color
        gameObject.objList.append(self)

    def update(self):
        pass
    
    def draw(self):
        pg.draw.rect(self.game.getScreen(), pg.Color(self.color), self.rect)
    
    def distanceTo(self, other):
        return math.sqrt(abs(self.rect.centerx - other.rect.centerx)**2 + abs(self.rect.centery - other.rect.centery)**2)
    
    def wrapCoordinate(self):
        x = self.fpos[0]
        y = self.fpos[1]
        w = self.rect.w
        h = self.rect.h


        sw = self.game.getWidth()
        sh = self.game.getHeight()

        if x + w < 0 :
            x = sw * 1.0
            self.rect.x = sw 
        if x > sw :
            x = -w * 1.0
            self.rect.x = -w
        
        if y + h < 0:
            y = sh * 1.0
            self.rect.y = sh
        if y > sh:
            y = -h * 1.0
            self.rect.y = -h
        
        self.fpos = (x, y)
    
    def changePos(self):
        self.rect.x = int(self.fpos[0])
        self.rect.y = int(self.fpos[1])
    
    def setPos(self, x, y):
        self.fpos = (x,y)
        self.changePos()

class Reward(gameObject):
    
    def __init__(self, x : int, y : int, w : int, h : int, color : str, game):
        super().__init__(x, y, w, h, color, game)
    
    def draw(self):
        pg.draw.circle(self.game.getScreen(), pg.Color(self.color),(self.rect.centerx, self.rect.centery), self.rect.w)

        

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

    # mass
    machineMass : float            # mass of the machine
    fuelMass : float        # mass of the fuel
    fuelMassPerFuel : float # d mass fuel / fuel

    def print(self):
        n = 0
        for i in self._fields:
            print(i.ljust(8) +"\t:"+ str(self[n]))
            n += 1

class Decision(NamedTuple):
    """
        each condition can have 4 state 0, 1, 2 or 3
        except perception € [5 ; screenwidth/10]
    """
    # if close to a machine
    ifCloseMachineAtLeft : int
    ifCloseMachineAtRight : int
    ifCloseMachineAtUp : int
    ifCloseMachineAtDown : int

    # if close to reward
    ifCloseRewardLeft : int
    ifCloseRewardRight : int
    ifCloseRewardUp : int
    ifCloseRewardDown : int

    # if nothing is close
    ifNothing : int

    # perception of the environnement
    perception : int

    def print(self):
        n = 0
        for i in self._fields:
            print(i.ljust(8) +"\t:"+ str(self[n]))
            n += 1

class Machine(gameObject):

    machines = list()
    dead = list()
    rewards = list()
    ID_GENERATOR = 0
    def __init__(self,  x : int, y : int, w : int, h : int, color : str, game , status : Status, decisions : Decision):
        super().__init__(x, y, w, h, color, game)
        self.id = Machine.ID_GENERATOR
        Machine.ID_GENERATOR += 1

        self.dx = 0.0
        self.dy = 0.0

        self.status = status
        self.decisions = decisions

        self.isAlive = True
        self.isOverheat = False # not used

        self.focusM = None
        self.distanceToFocus = math.inf

        self.reward = None
        self.distanceToReward = math.inf

        self.fitness = 1

        Machine.machines.append(self)
    
    def update(self):
        # if machine is Dead remove
        if not self.isAlive:
            Machine.machines.remove(self)
            Machine.dead.append(self)
            return
        
        # decision
        MOVES = ["up", "down", "left", "right", "stay", "upLeft", "upRight", "downLeft", "downRight"]
        # closest machine
        self.focusM, self.distanceToFocus = self.getClosestMachine()
        self.reward, self.distanceToReward = self.getClosestReward()
        # if the machine can see it
        d = self.decisions
        per = self.decisions.perception

        if self.distanceToFocus <= per or self.distanceToReward <= per:

            if self.distanceToFocus <= per and self.distanceToFocus != 0:
                self.move(MOVES[d.ifNothing])
                # other machine
                dirx = sign(self.focusM.rect.centerx - self.rect.centerx)
                diry = sign(self.focusM.rect.centerx - self.rect.centerx)

                if dirx < 0 :
                    self.move(MOVES[d.ifCloseMachineAtLeft])

                if dirx > 0 :
                    self.move(MOVES[d.ifCloseMachineAtRight])

                if diry < 0 :
                    self.move(MOVES[d.ifCloseMachineAtUp])

                if diry > 0 :
                    self.move(MOVES[d.ifCloseMachineAtDown])
            
            if self.distanceToReward <= per:
                if self.distanceToReward <= 20:
                    self.fitness += 1
                # other machine
                dirx = sign(self.reward.rect.centerx - self.rect.centerx)
                diry = sign(self.reward.rect.centerx - self.rect.centerx)

                if dirx < 0 :
                    self.move(MOVES[d.ifCloseRewardLeft])

                if dirx > 0 :
                    self.move(MOVES[d.ifCloseRewardRight])

                if diry < 0 :
                    self.move(MOVES[d.ifCloseRewardUp])

                if diry > 0 :
                    self.move(MOVES[d.ifCloseRewardDown])
        
        else :
            self.move(MOVES[d.ifNothing])
        
        rewardRectList = [i.rect for i in Machine.rewards]
        if self.rect.collidelist(rewardRectList) != -1:
            self.fitness += 1000
            
        # moving
        s = self.status
        dt = self.game.getDeltaTime()
        x, y = self.fpos
        maxSpeed = 0.3
        x += min(((self.dx * dt)) * 1.0e-1, maxSpeed)
        y += min(((self.dy * dt)) * 1.0e-1, maxSpeed)

        self.fpos = (x, y)

        self.changePos()

        self.wrapCoordinate()
    
    def move(self, direction : str):
        s = self.status
        dt =self.game.getDeltaTime()
        dfuel = -1 * s.fuelPerPower * s.powerPerTime * dt
        # print(s.fuel - dfuel)
        if s.fuel + dfuel > 0:
            if direction == "left":
                self.dx = -1 * s.speedPerPower * s.powerPerTime * dt

            if direction == "right":
                self.dx = s.speedPerPower * s.powerPerTime * dt

            if direction == "up":
                self.dy = -1 * s.speedPerPower * s.powerPerTime * dt
            
            if direction == "upLeft":
                self.dy = -1 * s.speedPerPower * s.powerPerTime * dt
                self.dx = -1 * s.speedPerPower * s.powerPerTime * dt
            
            if direction == "upRight":
                self.dy = -1 * s.speedPerPower * s.powerPerTime * dt
                self.dx = s.speedPerPower * s.powerPerTime * dt

            if direction == "down":
                self.dy = s.speedPerPower * s.powerPerTime * dt

            if direction == "downLeft":
                self.dy = s.speedPerPower * s.powerPerTime * dt
                self.dx = -1 * s.speedPerPower * s.powerPerTime * dt
            
            if direction == "downRight":
                self.dy = s.speedPerPower * s.powerPerTime * dt
                self.dx = s.speedPerPower * s.powerPerTime * dt

            if direction == "stay":
                self.dy = 0
                self.dx = 0


            dtemp = s.tempPerPower * s.powerPerTime * dt
            dfuelMass = s.fuelMassPerFuel * dfuel

            s = s._replace(fuel = s.fuel + dfuel)
            s = s._replace(temperature = s.temperature + dtemp)
            s = s._replace(fuelMass = s.fuelMass + dfuelMass)
            self.status = s
        else :
            self.isAlive = False
    
    def draw(self):
        if self.isAlive:
            super().draw()

    @staticmethod
    def drawReward():
        for i in Machine.rewards:
            i.draw()
    
    def print(self):
        print(self.id, self.color)
        self.status.print()
        self.decisions.print()


    def getGene(self):
        return list(self.status) + list(self.decisions)

    def setGene(self, gene):
        self.status = Status(*gene[:len(self.status)])
        self.decisions = Decision(*gene[len(self.status):])  

    def getClosestMachine(self):
        distance = math.inf
        closestM = None
        Machine.machines.remove(self)
        for m in Machine.machines:
            if m.id != self.id:
                
                d = self.distanceTo(m)
                if distance > d:
                    distance = d
                    closestM = m

        Machine.machines.append(self)

        return closestM, distance
    
    def getClosestReward(self):

        distance = math.inf
        closestM = None

        for m in Machine.rewards:
                d = self.distanceTo(m)
                if distance > d:
                    distance = d
                    closestM = m

        return closestM, distance
    
    def getClone(self):
        m = Machine(0, 0, self.rect.w, self.rect.h, self.color, self.game, self.status._replace(fuel = self.status.maxFuel), self.decisions._replace(ifNothing = self.decisions.ifNothing))
        m.fitness = 1
        return m

    def mutate(self, mutChance):
        geneS = list(self.status) 
        geneD = list(self.decisions)
        for i in range(len(geneS)):
            if random.random() <= mutChance:
                 geneS[i] += random.uniform(-0.01, 0.01)
                 print("mutate !")
        
        for i in range(len(geneD)-1):
            if random.random() <= mutChance:
                 geneD[i] = random.randint(0, 8)
                 print("mutate !")

        if random.random() <= mutChance:
            geneD[len(geneD)-1] = random.randint(-10, 10)
            print("mutate !")
        
        self.setGene(geneS + geneD)
                

    @staticmethod
    def createMachine( 
                    x : int,
                    y : int,
                    w : int,
                    h : int,
                    color : str,
                    game,
                    maxFuel : float,
                    fuel : float,
                    fuelPerPower : float,
                    powerPerTime : float,
                    tempPerPower : float,
                    speedPerPower : float,
                    temperature : float,
                    maxTemp : float,
                    machineMass : float,
                    fuelMass : float,
                    fuelMassPerFuel : float,
                    ifCloseMachineAtLeft : int,
                    ifCloseMachineAtRight : int,
                    ifCloseMachineAtUp : int,
                    ifCloseMachineAtDown : int,
                    ifCloseRewardLeft : int,
                    ifCloseRewardRight : int,
                    ifCloseRewardUp : int,
                    ifCloseRewardDown : int,
                    ifNothing : int,
                    perception : int):

                s = Status(
                    maxFuel,
                    fuel,
                    fuelPerPower,
                    powerPerTime,
                    tempPerPower,
                    speedPerPower,
                    temperature,
                    maxTemp,
                    machineMass,
                    fuelMass,
                    fuelMassPerFuel)
                
                d = Decision(
                    ifCloseMachineAtLeft,
                    ifCloseMachineAtRight,
                    ifCloseMachineAtUp,
                    ifCloseMachineAtDown,
                    ifCloseRewardLeft,
                    ifCloseRewardRight,
                    ifCloseRewardUp,
                    ifCloseRewardDown,
                    ifNothing,
                    perception)
                
                return Machine(x, y, w, h, color, game, s, d)
    
    @staticmethod
    def createRandomStatusMachine(game):
        
        sWidth = game.getWidth()
        sHeight = game.getHeight()

        # pos scale and color
        MIN_WIDTH = int(sWidth/200)
        MAX_WIDTH = int(sWidth/20)


        w = random.randint(MIN_WIDTH, MAX_WIDTH)
        h = w
        x = 0
        y = 0

        COLORS = [
            "green",
            "blue",
            "yellow",
            "pink",
            "purple",
            "cyan"
        ]

        color = random.choice(COLORS)

        # status
        maxFuel = random.uniform(1.0e2, 1.0e4)
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


        fuelMass = fuel * fuelMassPerFuel

        ifCloseMachineAtLeft = random.randint(0, 8)
        ifCloseMachineAtRight = random.randint(0, 8)
        ifCloseMachineAtUp = random.randint(0, 8)
        ifCloseMachineAtDown = random.randint(0, 8)

        ifCloseRewardLeft = random.randint(0, 8)
        ifCloseRewardRight = random.randint(0, 8)
        ifCloseRewardUp = random.randint(0, 8)
        ifCloseRewardDown = random.randint(0, 8)

        ifNothing = random.randint(0, 8)

        perception = random.randint(10, int(game.getWidth()/10))

        return Machine.createMachine(x, y, w, h, 
                    color,
                    game, 
                    maxFuel, 
                    fuel, 
                    fuelPerPower,
                    powerPerTime,
                    tempPerPower,
                    speedPerPower,
                    temperature,
                    maxTemp,
                    machineMass,
                    fuelMass,
                    fuelMassPerFuel,
                    ifCloseMachineAtLeft,
                    ifCloseMachineAtRight,
                    ifCloseMachineAtUp,
                    ifCloseMachineAtDown,
                    ifCloseRewardLeft,
                    ifCloseRewardRight,
                    ifCloseRewardUp,
                    ifCloseRewardDown,
                    ifNothing,
                    perception)

