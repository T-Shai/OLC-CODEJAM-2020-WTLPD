# -*- coding: utf-8 -*-
import pygame as pg


def loadImage(l):
    return pg.image.load(l).convert_alpha()