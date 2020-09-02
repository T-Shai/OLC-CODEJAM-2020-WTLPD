# -*- coding: utf-8 -*-
import os
import pygame as pg

def pygameInit():
    # centering screen 
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # intialising pygame stuff
    pg.init()

class Window():
    """
     Window class helps create a window
    """
    def __init__(self, name, width, height, icon = None):

        # initialising
        self._width = width
        self._height = height
        self._name = name

        self._screen = pg.display.set_mode((self._width, self._height))
        pg.display.set_caption(self._name) 

        if icon is not None:
            pg.display.set_icon(icon) # setting icon if provided 

        self._clock = pg.time.Clock()
        self._dt = 0
        self._FPS = 60

        self._fillColor = pg.Color("black")

        self._running = True


    
    def setFillColor(self, r = -1, g = -1 ,b = -1, a = -1, name = None):
        """
            setting the filling color
            i.e Window.setFillColor(0, 0, 0)
                Window.setFillColor(0, 154, 200, 5)
                Window.setFillColor(name="red") # Pygame's color constants 
        """
        if name == None:
            if a != -1 :
                self._fillColor = pg.Color(r, g, b, a)
            else :
                self._fillColor = pg.Color(r, g, b, 255)
        else :
            self._fillColor = pg.Color(name)

    def setFPS(self, FPS : int):
        """
            Set to the given FPS
        """
        self._FPS = FPS

    def getScreen(self):
        """
            screen getter
        """
        return self._screen
    
    def getFPS(self):
        """
            FPS getter
        """
        return int(self._clock.get_fps())

    def getWidth(self):
        """
            window's screen width getter
        """

        return self._width

    def getHeight(self):
        """
            window's screen height getter
        """

        return self._height
    
    def getDeltaTime(self):
        """
        """
        return self._dt
    
    def update(self):
        pass
    
    def draw(self):
        pass

    def loop(self):
        """
            main loop of the display window
        """

        while self._running:
            #setting FPS and getting delta time
            self._dt = self._clock.tick(self._FPS)
            # Filling screen
            self._screen.fill(self._fillColor)

            # Events
            pg.key.set_repeat(1, 100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._running = False
            
            self.update()
            self.draw()

            pg.display.update()
            # end of while loop

        pg.quit()
    
class WindowObject:

    def __init__(self, window):
        self.window = window
    
    def update(self):
        NotImplementedError("Overwrite update from the windowObject !")

    def draw(self):
        NotImplementedError("Overwrite draw from the windowObject !")


if __name__ == "__main__":
    w = Window("Ceci est une fenetre de qualite", 500, 600)
    w.setFillColor(name="green")
    w.loop()