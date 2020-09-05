 # -*- coding: utf-8 -*-
from ga import *
from textInput import *

class MainWindow(Window): 
    
    def __init__(self):
        
        super().__init__("OLC CODEJAM 2020 - while True : Live, Program, Die by SAI#8680 ", 1280, 720, "rsc/reward_1.png")
        
        
        self.gen = None

        self.speed = 1

        self.font = pg.font.SysFont('consolas', 20)

        self.timer = 0

        self.state = "Start"

        self.indvFocus = None

        self.startingBot = Machine(self._width/2, self._height/2, self)

        self.popSizeIB = InputBox(self._width/2, 200, 150, 50, self, text="1000")
        self.mutChanceIB = InputBox(self._width/2, 275, 150, 50, self, text="0.03")
        self.configTextPS = self.font.render("Population size (> {}) :".format(GA.MIN_POPSIZE), True, (0, 150, 255))
        self.configTextMC = self.font.render("Mutation chance (> 0)  :", True, (0, 150, 255))

        self.Schoose = pg.mixer.Sound("rsc/choose.wav")
        self.Schoose.set_volume(0.5)
        self.Sreset = pg.mixer.Sound("rsc/reset.wav")
        self.Sreset.set_volume(0.5)
        pg.mixer.music.load("rsc/music.mp3")
        pg.mixer.music.play(-1)
    
    def initialise(self):
        popSize = int(self.popSizeIB.getText())

        if popSize < GA.MIN_POPSIZE:
            popSize = GA.MIN_POPSIZE+1
        mutChance = float(self.mutChanceIB.getText())

        if mutChance < 0.0:
            mutChance = 0.001

        self.gen = GA(600, 50, popSize, mutChance, self)

        nRewards = random.randint(1, 4)
        Machine.rewards = list()
        Machine.obstacles = list()
        for _ in range(nRewards):
            x = random.randint(100, self._width)
            y = random.randint(int( self._height/2), self._height)
            GA.addReward(x, y, self)
        
        self.speed = 1
        self.timer = 0
        pg.mixer.music.play(-1)
    
    def update(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self._running = False
            
            if self.state == "Configuration":
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.Schoose.play()

                self.popSizeIB.handle_event(event)
                self.popSizeIB.update()
                self.mutChanceIB.handle_event(event)
                self.mutChanceIB.update()

            if event.type == pg.KEYDOWN:
                
                if self.state == "Start":
                    if event.key == pg.K_SPACE:
                        self.state = "Configuration"
                        self.Schoose.play()

                if self.state == "Configuration":
                    if event.key == pg.K_RETURN:
                        self.state = "Simulation"
                        if self.gen == None:
                            self.initialise()
                            self.Sreset.play()

                if event.key == pg.K_r:
                    if self.state == "Inspection" or self.state == "Simulation":
                        self.initialise()
                        self.Sreset.play()

                if event.key == pg.K_e:
                    if self.state == "Inspection" or self.state == "Simulation":
                        mx, my = pg.mouse.get_pos()
                        self.gen.addObstacle(mx, my, self)
                        self.Schoose.play()

                if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:

                    if self.state == "Inspection" or self.state == "Simulation":
                        self.state = "Inspection" if self.state == "Simulation" and self.state != "Start" else "Simulation"
                        self.Schoose.play()
            
        if self.state == "Start":
            self.startingBot.update()
            pg.mixer.music.unpause()
        
        if self.state == "Configuration":
            pg.mixer.music.pause()

        if self.state == "Inspection":
            pg.mixer.music.pause()
            mX, mY = pg.mouse.get_pos()
            c = (255 - self._fillColor.r, 255 - self._fillColor.g, 255 - self._fillColor.b, 125)
            for i in self.gen.population :
                if i.rect.collidepoint(mX, mY):
                    pg.draw.rect(self._screen, c, i.rect, 2)
                    if pg.mouse.get_pressed()[0]:
                        self.indvFocus = i
                        self.Schoose.play()
                    break
                else:
                    if pg.mouse.get_pressed()[0]:
                        self.indvFocus = None

        if self.state == "Simulation":
            pg.mixer.music.unpause()
            self.timer += self.getDeltaTime()

            for _ in range(self.speed * self.speed):
                self.gen.update()
            
            

        
                


    def draw(self):
        texts = list()
        c = (255 , 0, 0, 100)

        if self.state == "Start":

            t = pg.font.SysFont("consolas", 35).render("*biip* * boop* Press space on keyboard to start *beeeep*", True, c)
            texts.append((t, (int(self._width/2 - t.get_width()/2), int(self._height - t.get_height()))))
            t = pg.font.SysFont("consolas", 40).render("While True : Live, Program, Die !", True, c)
            texts.append((t, (int(self._width/2 - t.get_width()/2), int(self._height/2 - t.get_height()/2))))
            t = pg.font.SysFont("consolas", 20).render("by SAI#8680", True, c)
            texts.append((t, (int(self._width/2 - t.get_width()/2), int(self._height/1.5 - t.get_height()/3))))

            self.startingBot.draw()

        else :

            mode = "Mode : " + self.state
            t = self.font.render(mode, True, c)
            texts.append((t, (0, t.get_height())))


        if self.state == "Configuration":
            self.popSizeIB.draw()
            self.mutChanceIB.draw()
            info = "Press ENTER to start the simulation phase"
            t = self.font.render(info, True, c)
            texts.append((t, (self._width-t.get_width(), self._height - t.get_height())))
            texts.append((self.configTextPS, (self._width/2 - self.configTextPS.get_width() -20, 200)))
            texts.append((self.configTextMC, (self._width/2 - self.configTextMC.get_width() -20, 275)))

        if self.state == "Simulation" or self.state == "Inspection":

            self.gen.drawPopulation()
            self.gen.drawReward()
            self.gen.drawObstacle()

            info = "FPS : " + str(self.getFPS()) + " | nGen : " +str(self.gen.nGen)+" |  Fitness testing : "+ str(int(self.gen.timer/GA.generationTime *100)) +"%"
            t = self.font.render(info, True, c)
            texts.append((t, (self._width-t.get_width(), self._height-t.get_height())))
            
            prevLineH = self._height-t.get_height()
            info = "Press CTRL to toggle between inspect mode and simulation mode"
            t = self.font.render(info, True, c)
            texts.append((t, (self._width-t.get_width(), prevLineH - t.get_height())))

            prevLineH = prevLineH-t.get_height()
            info = "Press r to reset the simulation"
            t = self.font.render(info, True, c)
            texts.append((t, (self._width-t.get_width(), prevLineH - t.get_height())))
            
            prevLineH = prevLineH-t.get_height()
            info = "Press e to place obstacle"
            t = self.font.render(info, True, c)
            texts.append((t, (self._width-t.get_width(), prevLineH - t.get_height())))

            prevLineH = prevLineH-t.get_height() - 40
            info = "{} androids teleported out of {}".format(Machine.nTeleported, int(self.popSizeIB.getText()))
            t = self.font.render(info, True, c)
            texts.append((t, (self._width-t.get_width(), prevLineH - t.get_height())))

        if self.state == "Inspection":
            if self.indvFocus != None :
                s = pg.Surface((int(self._width),self._height), pg.SRCALPHA)
                s.fill((0, 0, 0, 100))
                self._screen.blit(s, (0,0))

                i = self.indvFocus

                name = "Name : " + i.name +" the "+ str(self.gen.nGen)+"th"
                t = self.font.render(name, True, c)
                texts.append((t, (self._width-t.get_width(), t.get_height())))
                
                prevLineH = t.get_height()

                coord = "Coordinates | " + str((i.rect.centerx, i.rect.centery))
                t = self.font.render(coord, True, c)
                texts.append((t, (self._width-t.get_width(), prevLineH + t.get_height())))

                prevLineH += t.get_height() + 20

                nLine = 10
                for n in range(i.nCommand - nLine, i.nCommand + nLine):
                    if n == i.nCommand:
                        commands = "executing order -->"
                    else :
                        commands = "  "
                    
                    if n < 0:
                        n = len(i.algorithm) - n

                    commands += "\"" + i.algorithm[n%len(i.algorithm)] + "\""

                    t = self.font.render(commands, True, c)
                    texts.append((t, (self._width-t.get_width(), prevLineH + t.get_height())))
                    prevLineH +=  t.get_height()
        
        if self.state == "Simulation":
            s = pg.Surface((250,200), pg.SRCALPHA)
            s.fill((0, 0, 0, 150))
            self._screen.blit(s, (0,0))
            
            f = pg.font.SysFont('consolas', 30)

            t = f.render("Speed : " + str(self.speed), True, c)
            self._screen.blit(t , (0, 40))


            sRect = pg.draw.rect(self._screen, c, (20, 80, 40, 40), 3)
            t = f.render("+", True, c)
            self._screen.blit(t, (int(sRect.centerx - t.get_width()/2), int(sRect.centery - t.get_height()/2 )))

            sRect2 = pg.draw.rect(self._screen, c, (20, 130, 40, 40), 3)
            t = f.render("-", True, c)
            self._screen.blit(t, (int(sRect2.centerx - t.get_width()/2), int(sRect2.centery - t.get_height()/2) ))

            mX, mY = pg.mouse.get_pos()
            if sRect.collidepoint(mX, mY):
                if pg.mouse.get_pressed()[0] and self.speed < 100:
                    self.speed += 1
            
            if sRect2.collidepoint(mX, mY):
                if pg.mouse.get_pressed()[0] and self.speed > 1:
                    self.speed -= 1

                
        for text in texts:
            x, y = text[1]
            self._screen.blit(text[0], (int(x), int(y)))

if __name__ == "__main__":
    w = MainWindow()
    w.setFillColor(name="darkblue")
    w.loop()