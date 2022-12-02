import pygame
import math
import threading
import random
from pygame import mixer

aux = 0
# variables for pygame
pygame.init()
mixer.init()
piu=mixer.Sound('Assets/piu(1).mp3')
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
for i in range(5):
    pos_target.append(target_images[1].get_rect())
shot = False  # variable para revisar si hay un tiro o no
class Hilo(threading.Thread):
    global speed
    global image
    global target_rect

    def __init__(self, id, lastTargetX, lastTargetY):
        threading.Thread.__init__(self)
        self.id = id
        self.semaphore = threading.Lock()
        self.lastTargetX = lastTargetX
        self.lastTargetY = lastTargetY
        pos_target[self.id][0] = self.lastTargetX
        pos_target[self.id][1] = self.lastTargetY - 200
        self.image = 0
        varX = random.randint(-3,5)
        varY = random.randint(1,6)
        self.speed = [varX, varY]
        self._alive = True

    def run(self):
        self.target_rect = pygame.Rect((pos_target[self.id][0],pos_target[self.id][1]), (100, 100))
        screen.blit(target_images[self.image], pos_target[self.id])
        pos_target[self.id] = pos_target[self.id].move(self.speed)
        
        if pos_target[self.id].left < 0 or pos_target[self.id].right > WIDTH:
            self.speed[0] = -self.speed[0]
            
        if pos_target[self.id].top < 0 or pos_target[self.id].bottom > HEIGHT - 200:
            self.speed[1] = -self.speed[1]
            
        if pos_target[self.id].bottom >= HEIGHT - 210 and not self._alive:
            if self.semaphore.locked():
                return self._revive()

    def _revive(self):
        self.image = 0
        varX = random.randint(-3,5)
        varY = random.randint(1,6)
        self.speed = [varX, varY]
        self.semaphore.release()

    def hit(self):
        shooted = _check_hit(self.target_rect)
        if self.semaphore.locked() is False:
            if shooted:
                self._alive = False
                self.speed = [0, 6]
                self.image = 1
                self.semaphore.acquire()

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
        return True
    return flag

run = True
lastTargetY = 700
ducks_list = []
for n in range(5): #loop ducks
    spawnX = random.randint(0,800)
    duck = Hilo(n, spawnX, lastTargetY)
    duck.start()
    ducks_list.append(duck)
    

while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bg, (0, 0))
    screen.blit(banner, (0, HEIGHT-200))
    show_gun()
    
    for t in ducks_list:
        t.run()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            piu.play()
            mouse_position = pygame.mouse.get_pos()
            if (0 < mouse_position[0] < WIDTH) and (0 < mouse_position[1] < HEIGHT - 200):   
                for i in ducks_list:
                    i.hit()
    pygame.display.update()
pygame.quit()