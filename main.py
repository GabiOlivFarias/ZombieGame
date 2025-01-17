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

#casas assombradas
houses = Actor('casas')
houses.x = 397
houses.y = 308

#morcego
bat = Actor('morcego')
# bat.scale = 0.5 #diminui aqui ou pelo gimp direto
bat.x = 400
bat.y = 100
bat.images = ['morcego', 'morcego2', 'morcego3', 'morcego2']

def  update():
    bat.animate()

def draw():
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (grey)) #céu
    screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #chão

    moon.draw()
    houses.draw()
    bat.draw()

pgzrun.go()
