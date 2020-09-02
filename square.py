# -*- coding: utf-8 -*-
import random
import copy
import math 

from window import *
from utils import *

pygameInit()

class Reward(WindowObject):
    IMAGES = list()

    def __init__(self, x :float, y :float, window: Window):
        super().__init__(window)
        if Reward.IMAGES == list():
            Reward.loadImage()
        
        self.image = random.choice(Reward.IMAGES).copy()
        rgb = random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)
        self.image.fill(rgb, special_flags = pg.BLEND_MAX)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    
    def draw(self):
        s = self.window.getScreen()
        s.blit(self.image, self.rect)
        

    @staticmethod
    def loadImage():
        Reward.IMAGES = [loadImage("rsc/reward_1.png")]
    
class Machine(WindowObject):
    
    IMAGES = list()
    MOVES = ["up", "down", "right", "left", "stay"]
    SPEED = 0.3
    N_COMMAND = 100
    rewards = list()
    perceptionRadius = 20

    def __init__(self, x :float, y :float, window: Window):
        super().__init__(window)
        if Machine.IMAGES == list():
            Machine.loadImages()

        self.image = random.choice(Machine.IMAGES).copy()
        rgb = random.randint(0, 150),random.randint(0, 150),random.randint(0, 150)
        self.image.fill(rgb, special_flags = pg.BLEND_MAX)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.nCommand = 0
        self.algorithm = Machine.createRandomAlgorithm()

        self.fitness = 0
    
    def reset(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.nCommand = 0
        self.fitness = 0
    
    @staticmethod
    def createRandomAlgorithm() -> list:
        lr = list()

        for _ in range(Machine.N_COMMAND):
            lr.append(random.choice(Machine.MOVES))
        
        return lr

    def move(self, direction, dt):
        alea = random.uniform(0.01, 1)
        if direction == "up":
            self.rect.centery -= Machine.SPEED * dt + alea

        elif direction == "down" :
            self.rect.centery += Machine.SPEED * dt + alea
        
        elif direction == "right" :
            self.rect.centerx += Machine.SPEED * dt + alea

        elif direction == "left" :
            self.rect.centerx -= Machine.SPEED * dt + alea
        
        else :
            return

    def update(self):
        dt = self.window.getDeltaTime()
        self.move(self.algorithm[self.nCommand], dt)
        self.nCommand += 1

        if self.nCommand == Machine.N_COMMAND:
            self.nCommand = 0
        
        d = self.getClosestReward()

        if d < self.rect.w:
            self.fitness *= 10
            return

        self.fitness = max(self.fitness, 1/(d + 1 ) )

        
    
    def draw(self):
        s = self.window.getScreen()
        s.blit(self.image, self.rect)

    
    # GA STUFF
    def getClone(self, startPos):
        m = Machine(startPos[0], startPos[1], self.window)
        m.image = self.image.copy()
        m.algorithm = self.algorithm.copy()
        return m
    
    def mutate(self):
        indx = random.randint(0, Machine.N_COMMAND -1)
        self.algorithm[indx] = random.choice(Machine.MOVES)

    # REWARDS
    def distanceTo(self, other):
        return ((self.rect.centerx - other.rect.centerx)**2 + (self.rect.centery - other.rect.centery)**2)
    
    def getClosestReward(self):

        distance = math.inf
        closestM = None

        for m in Machine.rewards:
                d = self.distanceTo(m)
                if distance > d:
                    distance = d
                    closestM = m

        return distance
    
    
    @staticmethod
    def loadImages():
        Machine.IMAGES  = [loadImage("rsc/machine_1.png")]

    


