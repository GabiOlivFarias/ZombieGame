import pgzrun
import random
from pgzhelper import *
import pygame ##coloquei somente pra tocar a musica de fundo, somente isso

#Comentários feitos para que eu ou um adulto entenda, para uma criança os comentários serão mais detalhados.

#dimensões da tela
WIDTH = 800
HEIGHT = 600

#Música de fundo
pygame.mixer.init()
pygame.mixer.music.load('musics/ambientesound.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

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
final_score = 0
game_over = False
end_game = False

def play_lose_sound():
    sounds.losegame.play()

def update():
    global velocity, isJumping, ghost_collected, score, obstacles_timeout, game_over, end_game, final_score

    if game_over:
        if not end_game:
            clock.schedule_unique(play_lose_sound, 1.5)
            pygame.mixer.music.stop()
            end_game = True
        return
    
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
        bat.y = random.randint(200, 250)

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
          tombstone.x -= 4 
          if tombstone.x < -50:
               obstacles.remove(tombstone)
               score -= 1
               game_over = True
               if end_game == False:
                   sounds.losegame.play()
               end_game = True

    for tombstone in obstacles[:]:
          tombstone.x -= 8  # Move a lápide para a esquerda

        # Detecção de colisão
          if 110 < tombstone.x < 150: 
               if zombie.colliderect(tombstone): 
                    sounds.crash.play()
                    final_score = score
                    obstacles.remove(tombstone)
                    score = 0
                    game_over = True

          elif tombstone.x < -50: 
               obstacles.remove(tombstone)

    if score <= -1:
          game_over = True


def draw():
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (grey)) #céu
    screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #chão

    if game_over:
        screen.draw.text('Game Over', centerx = 380, centery = 150, color = (red), fontname = 'zombie', fontsize = 80)
        if score >= 0:
          screen.draw.text('Score: ' + str(final_score), centerx = 380, centery = 250, color = (white), fontname = 'zombie', fontsize = 60)
        else:
          screen.draw.text('Score: ' + str(0), centerx = 380, centery = 250, color = (white), fontname = 'zombie', fontsize = 60)
    else:      
     moon.draw()
     houses.draw()
     bat.draw()
     zombie.draw()
     ghost.draw()
     screen.draw.text('Score: ' + str(score), (20, 20), color=(red), fontname='zombie', fontsize = 30)

     for tombstone in obstacles:
          tombstone.draw()

pgzrun.go()
