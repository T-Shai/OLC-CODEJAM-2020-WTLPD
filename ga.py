# -*- coding: utf-8 -*
from square import *


class GA:

    generationTime = 10e3
    MIN_POPSIZE = 5
    def __init__(self, x : float, y: float, popSize :int, mutChance: float, window : Window):
        
        self.startPos = (x, y)
        if popSize < GA.MIN_POPSIZE:
            popSize = GA.MIN_POPSIZE
        self.popSize = popSize
        self.muChance = mutChance
        
        self.window = window

        # create population
        self.population = [Machine(x, y, window) for _ in range(popSize)]


        self.timer = 0

        self.nGen = 0

    
    def SortByFitness(self):
        self.population.sort(key=lambda x: x.fitness/self.timer, reverse=True)
        self.population = self.population[ :GA.MIN_POPSIZE]
    
    def nextGen(self):
        self.SortByFitness()
        newPop = list()
        for _ in range(self.popSize):
            child = random.choice(self.population).getClone(self.startPos)
            if random.random() < self.muChance:
                child.mutate()
            newPop.append(child)
        
        self.population = newPop
        self.nGen += 1


    def update(self):
        dt = self.window.getDeltaTime()
        self.timer += dt

        for indv in self.population:
            indv.update()

        if self.timer > GA.generationTime:
            self.nextGen()
            self.timer = 0
    
    def drawPopulation(self):
        for indv in self.population:
            indv.draw()

    @staticmethod
    def addReward(x, y, window):
        Machine.rewards.append(Reward(x, y, window))

    def drawReward(self):
        for rew in Machine.rewards:
            rew.draw()
