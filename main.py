 # -*- coding: utf-8 -*-
from ga import *

class MainWindow(Window): 
    
    def __init__(self):
        
        super().__init__("test", 1200, 600)
        self.gen = GA(600, 50, 1000, 0.3, self)
        # GA.addReward(1120, 400, self)
        
        GA.addReward(80, 400, self)

        self.speed = 1

        self.font = pg.font.SysFont('helvetica', 18)

        self.timer =0
    def update(self):
        self.timer += self.getDeltaTime()

        for _ in range(self.speed):
            self.gen.update()
        
        d = pg.key.get_pressed()

        if self.timer % 2e2 < 10:

            if d[pg.K_p]:
                self.speed += 1
            if d[pg.K_m]:
                self.speed -= 1

        
                


    def draw(self):
        self.gen.drawPopulation()
        self.gen.drawReward()

        info = "speed : "+str(self.speed)+" | nGen : " +str(self.gen.nGen)+" |  timer : "+str(self.gen.timer)
        textsurface = self.font.render(info, False, (255, 255, 255))
        self._screen.blit(textsurface, (self._width-textsurface.get_width(), self._height-textsurface.get_height()))
if __name__ == "__main__":
    w = MainWindow()
    w.loop()