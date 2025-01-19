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
green = (60, 208, 20)
black = (0, 0, 0)
yellow = (253, 223, 28)

game_state = "menu"

zombie_menu = Actor('zombiemenu')
zombie_menu.x = 100
zombie_menu.y = 435

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
obstacles_gap = 100

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
win_game = False

def play_lose_sound():
    sounds.losegame.play()

def play_victory_sound():
    sounds.wingame.play()

def adjust_obstacle_speed(base_speed): #bloco personalizado alterando a velocidade de acrdo com a pontuação
    return base_speed + (score // 5)

def adjust_obstacle_generation_interval():
    return max(50, 300 - (score * 10))

def start_game():
    global game_state, score, final_score, game_over, end_game, win_game, obstacles, obstacles_timeout, ghost_collected
    game_state = "playing"
    pygame.mixer.music.play(-1)
    score = 0
    final_score = 0
    game_over = False
    end_game = False
    win_game = False
    obstacles = []
    obstacles_timeout = 0
    ghost_collected = False

def update():
    global velocity, isJumping, ghost_collected, score, obstacles_timeout, game_over, end_game, final_score, win_game, game_state

    if game_state == "menu":
          zombie_menu.animate()
          return

    if game_over or win_game:
        if not end_game:
            if game_over:
                clock.schedule_unique(play_lose_sound, 1.5)
            if win_game:
                clock.schedule_unique(play_victory_sound, 0.75)
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
     ghost.y = random.randint(280, 320)
     ghost_collected = False

          
    if isJumping and zombie.colliderect(ghost) and not ghost_collected:
        sounds.collect.play()
        ghost_collected = True 
        score += 5
        ghost.x = random.randint(900, 1500)
        ghost.y = random.randint(280, 320)

     #tumbas
    obstacles_timeout += 1
    if obstacles_timeout > adjust_obstacle_generation_interval():
          if len(obstacles) == 0 or (860 - obstacles[-1].x) > obstacle_gap:
               tombstone = Actor('lapide')
               tombstone.x = 860
               tombstone.y = 500
               obstacles.append(tombstone)
               obstacles_timeout = 0

    for tombstone in obstacles[:]:
        tombstone.x -= adjust_obstacle_speed(4)  # Velocidade inicial ajustada
        if tombstone.x < -50:
               obstacles.remove(tombstone)

        if 110 < tombstone.x < 150 and zombie.colliderect(tombstone):
               sounds.crash.play()
               final_score = score
               obstacles.remove(tombstone)
               score = 0
               game_over = True

    if score <= -1:
          game_over = True

    if score >= 50:
          win_game = True
          final_score = score


def draw():
    if game_state == "menu":
          screen.clear()
          zombie_menu.draw()
          screen.draw.text("Bem-vindo ao Zombie Runnig!", center=(400, 100), color=white, fontname = 'zombie', fontsize=60)
          screen.draw.text("Regras do jogo:", center=(400, 200), color=white,fontname = 'zombie', fontsize=40)
          screen.draw.text("- Colete fantasmas para ganhar pontos.", center=(400, 250), color=yellow, fontsize=30)
          screen.draw.text("- Evite as lápides para não perder o jogo.", center=(400, 300), color=yellow, fontsize=30)
          screen.draw.text("- Pressione 'Espaço' para pular.", center=(400, 350), color=yellow, fontsize=30)
          screen.draw.text("Pressione ENTER para começar.", center=(400, 450), color=green, fontname = 'zombie', fontsize=40)
          return
    
    screen.draw.filled_rect(Rect(0, 0, 800, 500), (grey)) #céu
    screen.draw.filled_rect(Rect(0, 500, 800, 600), (brown)) #chão

    if win_game:
        screen.clear()
        screen.draw.text('You Win', centerx = 380, centery = 150, color = (green), fontname = 'zombie', fontsize = 80)
        screen.draw.text('Score: ' + str(score), centerx = 380, centery = 250, color = (white), fontname = 'zombie', fontsize = 60)
    elif game_over:
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

def on_key_down(key):
     global game_state
     if game_state == "menu" and key == keys.RETURN:
          start_game()

pgzrun.go()
