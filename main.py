import pgzrun
import random
from pgzhelper import *

#dimensões da tela
WIDTH = 800
HEIGHT = 600

#cores
grey = (75, 75, 75)
brown = ( 71, 34, 18)  

#Lua
moon = Actor('lua')
moon.x = 700
moon.y = 80

def draw():
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (grey)) #céu
    screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #chão

    moon.draw()

pgzrun.go()
