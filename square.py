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
    
class Obstacle(WindowObject):

    def __init__(self, x, y, w, h, window: Window):
        super().__init__(window)
        self.surface = pg.Surface((int(w), int(h)))
        self.surface.fill((0,0,0))
        self.pos = [x ,y]
        self.w = w
        self.h = h
    
    def draw(self):
        self.window.getScreen().blit(self.surface, (self.pos[0], self.pos[1]))
    
    def getRect(self):
        r = self.surface.get_rect()
        r.x = self.pos[0]
        r.y = self.pos[1]
        return r

class Machine(WindowObject):
    
    NAMES = ["Billy", "David", "Sai", "Coder", "Elsa", "Mickey", "Armstrong", "Paul", "Paris", "Steven", "Emma", "Lisa", "John", "Joe", "Edward", "Elisabeth", "Emmanuel", "Brigitte", "Sarah", "Nicolas", "Francois"]
    FAMILY_NAME = ["The lone Coder", "John", "Doe", "Simpsons", "The python programmer", "The c++ programmer", "The legend", "i forgot my family name", "The rusher", "The Terminator", "Connor", "A Skynet operator", "An advance AI", "Javidx's clone"]
    IMAGES = list()
    MOVES = ["up", "down", "right", "left", "stay"]
    SPEED = 0.4
    N_COMMAND = 100
    rewards = list()
    obstacles = list()
    perceptionRadius = 20

    nTeleported = 0

    def __init__(self, x :float, y :float, window: Window):
        super().__init__(window)
        if Machine.IMAGES == list():
            Machine.loadImages()

        self.name = random.choice(Machine.NAMES) + ", " + (random.choice(Machine.FAMILY_NAME).upper())
        self.image = random.choice(Machine.IMAGES).copy()
        rgb = random.randint(0, 150),random.randint(0, 150),random.randint(0, 150)
        self.image.fill(rgb, special_flags = pg.BLEND_MAX)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.nCommand = 0
        self.algorithm = Machine.createRandomAlgorithm()

        self.fitness = 0

        self.isTeleported = False
    
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

        if direction == "up":
            self.rect.centery -= Machine.SPEED * dt 

        elif direction == "down" :
            self.rect.centery += Machine.SPEED * dt
        
        elif direction == "right" :
            self.rect.centerx += Machine.SPEED * dt

        elif direction == "left" :
            self.rect.centerx -= Machine.SPEED * dt
        
        else :
            return

    def update(self):
        if self.isTeleported:
            return

        for obs in Machine.obstacles:
            if self.rect.colliderect(obs.getRect()):
                self.fitness = -1
                return

        d = self.getClosestReward()
        if d < self.rect.w + Machine.perceptionRadius:
            self.fitness *= 2
            if not self.isTeleported:
                Machine.nTeleported += 1
                self.isTeleported = True
            return

        dt = 27.1
        self.move(self.algorithm[self.nCommand], dt)
        self.nCommand += 1

        if self.nCommand == Machine.N_COMMAND:
            self.nCommand = 0
        
        

        self.fitness = max(self.fitness, 1/(d + 1 ) )

        
    
    def draw(self):
        if not self.isTeleported:
            s = self.window.getScreen()
            s.blit(self.image, self.rect)

    
    # GA STUFF
    def getClone(self, startPos):
        m = Machine(startPos[0], startPos[1], self.window)
        m.image = self.image.copy()
        m.algorithm = self.algorithm.copy()
        return m
    
    def mutate(self):
        rgb = random.randint(0, 150),random.randint(0, 150),random.randint(0, 150)
        self.image.fill(rgb, special_flags = pg.BLEND_MAX)
        indx = random.randint(0, Machine.N_COMMAND -1)
        move = random.choice(Machine.MOVES)

        while move == self.algorithm[indx]:
            move = random.choice(Machine.MOVES)

        self.algorithm[indx] = move

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

    


