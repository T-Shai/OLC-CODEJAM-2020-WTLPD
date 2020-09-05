# -*- coding: utf-8 -*-
import pygame as pg

class InputBox:
    COLOR_INACTIVE = pg.Color("lightblue")
    COLOR_ACTIVE =  pg.Color("blue")
    pg.font.init()
    FONT =  pg.font.SysFont("consolas", 25)
    def __init__(self, x, y, w, h, window, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = InputBox.FONT.render(text, True, self.color)
        self.active = False
        self.window = window

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)
                

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        screen = self.window.getScreen()
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
    
    def getText(self):
        return self.text