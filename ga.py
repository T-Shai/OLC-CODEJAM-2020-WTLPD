from machine import *

class GA:

    def __init__(self, popSize, mutChance, game):

        self.popSize = popSize
        self.mutChance = mutChance
        self.timer = 0
        self.game = game
        
        for _ in range(popSize):
            Machine.createRandomStatusMachine(game)
        
        self.population = Machine.machines.copy()
        self.nGen = 0

    def update(self):
        for m in Machine.machines:
            m.update()
        
        self.timer += self.game.getDeltaTime()

        if not Machine.machines or self.timer > 8000: # empty
            self.timer = 0
            self.normaliseFitness()
            self.nextGen()

    def draw(self):
        for m in Machine.machines:
            m.draw()
        Machine.drawReward()

    def normaliseFitness(self):
        totalFitness = 0
        for m in self.population:
            totalFitness += m.fitness
        if totalFitness == 0:
            totalFitness = 1
        for m in self.population:
            m.fitness /= totalFitness

    def pickOne(self):
        indx = 0
        r = random.random()
        while(r > 0):
            r = r - self.population[indx].fitness
            indx += 1
        return self.population[indx-1]
    
    def nextGen(self):
        newPop = list()

        for _ in range(self.popSize):
            child = self.pickOne().getClone()
            child.isAlive = True
            child.mutate(self.mutChance)
            newPop.append(child)
        
        self.population = newPop
        Machine.machines = self.population
        self.nGen += 1
            
            