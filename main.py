import pgzrun
import random
from pgzhelper import *

#dimensões da tela
WIDTH = 800
HEIGHT = 600

#cores
grey = (75, 75, 75)
brown = ( 71, 34, 18)  
red = (255, 67, 53)
white = (255, 255, 255)

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

#obstáculos
obstacles = []
obstacles_timeout = 0

#movimento menino zombie
zombie = Actor('meninozombie1')
zombie.x = 100
zombie.y = 435
zombie.images = ['meninozombie1', 'meninozombie2', 'meninozombie3', 'meninozombie4', 
                 'meninozombie5', 'meninozombie6', 'meninozombie7', 'meninozombie8', 'meninozombie9', 'meninozombie10']
zombie.fps = 40

velocity = 0
gravity = 1
isJumping = False

ghost = Actor('fantasma')
ghost.x = random.randint(900, 5000)
ghost.y = random.randint(250, 350)

ghost_collected = False
score = 0

def update():
    global velocity, isJumping, ghost_collected, score, obstacles_timeout

    zombie.animate()

    if keyboard.space and not isJumping:
        velocity = -18
        isJumping = True

    velocity += gravity
    zombie.y += velocity

    if zombie.y >= 435:
        zombie.y = 435
        velocity = 0
        isJumping = False

    bat.animate()
    bat.x -= 5 #faz a animação andar até o fim
    if bat.x < -50:
        bat.x = random.randint(1000, 15000)
        bat.y = random.randint(100, 250)

    ghost.x -= 5
    if ghost.x < - 50:
     ghost.x = random.randint(900, 5000)
     ghost.y = random.randint(200, 280)
     ghost_collected = False

    if isJumping and zombie.colliderect(ghost) and not ghost_collected:
        sounds.collect.play()
        ghost_collected = True 
        score += 5

        ghost.x = random.randint(900, 1500)
        ghost.y = random.randint(200, 280)

        #tumbas
    obstacles_timeout += 1
    if obstacles_timeout > random.randint(60,700):
          tombstone = Actor('lapide')
          tombstone.x = 860
          tombstone.y = 500
          obstacles.append(tombstone)
          obstacles_timeout = 0

    for tombstone in obstacles:
          tombstone.x -= 8 
          if tombstone.x < -50:
               obstacles.remove(tombstone)
               score += 1


def draw():
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (grey)) #céu
    screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #chão

    moon.draw()
    houses.draw()
    bat.draw()
    zombie.draw()
    ghost.draw()
    screen.draw.text('Score:' + str(score), (20, 20), color=(red), fontname='zombie', fontsize = 30)

    for tombstone in obstacles:
        tombstone.draw()

pgzrun.go()
