import pygame
import math
import threading
from pygame import mixer
# Variable for thread
mutex = threading.Lock()
aux = 0
# variables for pygame
pygame.init()
mixer.init()
piu=mixer.Sound('Assets/piu(1).mp3')

# mixer.music.load('Assets/gogoDance.mp3')
# mixer.music.set_volume(0.2)
# mixer.music.play()
fps = 30
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = pygame.image.load(f'Assets/bg.png')
banner = pygame.image.load(f'Assets/banner.png')
gun = pygame.transform.scale(pygame.image.load(f'Assets/gun.png'), (150, 150))
target_images = [pygame.transform.scale(pygame.image.load(f'Assets/duckFlying.png'), (150, 150)),
                 pygame.transform.scale(pygame.image.load(f'Assets/duckSleeping.png'), (100, 100))]
pos_target = []
for i in range(2):
    pos_target.append(target_images[i].get_rect())
shot = False  # variable para revisar si hay un tiro o no
class Hilo(threading.Thread):
    global speed
    global image
    global target_rect

    def __init__(self, id, lastTargetX, lastTargetY):
        threading.Thread.__init__(self)
        self.id = id
        self.lastTargetX = lastTargetX
        self.lastTargetY = lastTargetY
        pos_target[1][0] = self.lastTargetX
        pos_target[1][1] = self.lastTargetY - 200
        self.image = 0
        self.speed = [1, -2]
        self._alive = True

    def run(self):
        self.target_rect = pygame.Rect(
            (pos_target[1][0], pos_target[1][1]), (100, 100))
        screen.blit(target_images[self.image], pos_target[1])
        pos_target[1] = pos_target[1].move(self.speed)
        if pos_target[1].left < 0 or pos_target[1].right > WIDTH:
            self.speed[0] = -self.speed[0]
        if pos_target[1].top < 0 or pos_target[1].bottom > HEIGHT - 200:
            self.speed[1] = -self.speed[1]
        if pos_target[1].bottom >= HEIGHT - 210 and not self._alive:
            if mutex.locked():
                return self._revive()

    def _revive(self):
        self.image = 0
        self.speed = [2, -2]
        mutex.release()

    def hit(self):
        shooted = _check_hit(self.target_rect)
       
        if mutex.locked() is False:
            if shooted:
                self._alive = False
                self.speed = [0, 4]
                self.image = 1
                mutex.acquire()

def show_gun():
    mouse_pos = pygame.mouse.get_pos()
    gun_point = (WIDTH/2, HEIGHT-200)
    clicks = pygame.mouse.get_pressed()
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1]-gun_point[1])/(mouse_pos[0]-gun_point[0])
    else:
        slope = -10000000
    angle = math.atan(slope)
    rotation = math.degrees(angle)
    if mouse_pos[1] < 600:
        if mouse_pos[0] < WIDTH/2:
            screen.blit(pygame.transform.rotate(
                gun, 90-rotation), (WIDTH/2-100, HEIGHT-350))
        else:
            screen.blit(pygame.transform.rotate(
                gun, 270-rotation), (WIDTH/2-100, HEIGHT-350))
        if clicks[0]:
            pygame.draw.circle(screen, 'red', mouse_pos, 8)

def _check_hit(target):
    flag = False
    mouse_pos = pygame.mouse.get_pos()
    if target.collidepoint(mouse_pos):
        flag = True
    return flag

run = True
lastTargetY = 700
lastTargetX = 150
duck = Hilo(1, lastTargetX, lastTargetY)
duck.start()
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bg, (0, 0))
    screen.blit(banner, (0, HEIGHT-200))
    show_gun()
    ducks_list = []
    duck.run()
    if shot:  # Evalua si se hizo el disparo
        shooted = _check_hit(duck, pos_target)
        shot = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Detecta la posicion del mouse cuando hace click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            piu.play()
            mouse_position = pygame.mouse.get_pos()
            if (0 < mouse_position[0] < WIDTH) and (0 < mouse_position[1] < HEIGHT - 200):   
                duck.hit()
    pygame.display.update()
pygame.quit()