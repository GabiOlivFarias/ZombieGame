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
bat.x = 800
bat.y = 100
bat.images = ['morcego', 'morcego2', 'morcego3', 'morcego2']
bat.fps = 7

#movimento menino zombie
zombie = Actor('meninozombie01')
zombie.x = 100
zombie.y = 470
zombie.images = ['meninozombie01', 'meninozombie02', 'meninozombie03', 'meninozombie04', 
                 'meninozombie05', 'meninozombie06', 'meninozombie07', 'meninozombie08', 'meninozombie09', 'meninozombie10']
zombie.fps = 40

velocity = 0
gravity = 1
isJumping = False


def update():
    global velocity, isJumping

    zombie.animate()

    if keyboard.space and not isJumping:
        velocity = -18
        isJumping = True

    velocity += gravity
    zombie.y += velocity

    if zombie.y >= 470:
        zombie.y = 470
        velocity = 0
        isJumping = False

    bat.animate()
    bat.x -= 5 #faz a animação andar até o fim
    if bat.x < -50:
        bat.x = random.randint(1000, 15000)
        bat.y = random.randint(100, 250)

def draw():
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (grey)) #céu
    screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #chão

    moon.draw()
    houses.draw()
    bat.draw()
    zombie.draw()

pgzrun.go()
