import pygame
import math

pygame.init()
fps=60
timer= pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',32)
WIDTH = 900
HEIGHT= 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg=pygame.image.load(f'Assets/bg.png')
banner=pygame.image.load(f'Assets/banner.png')
gun=pygame.transform.scale(pygame.image.load(f'Assets/gun.png'),(150,150))

def show_gun():
    mouse_pos= pygame.mouse.get_pos()
    gun_point= (WIDTH/2 , HEIGHT-200)
    clicks=pygame.mouse.get_pressed()
    if mouse_pos[0]!=gun_point[0]:
        slope=(mouse_pos[1]-gun_point[1])/(mouse_pos[0]-gun_point[0])
    else:
        slope=-10000000
    
    angle=math.atan(slope)
    rotation=math.degrees(angle)
    # if mouse_pos[0]<WIDTH/2:
    #     gun_aux=pygame.transform.flip(gun, True, False)
    if mouse_pos[1] < 600 :
        if mouse_pos[0]< WIDTH/2:
            screen.blit(pygame.transform.rotate(gun,90-rotation),(WIDTH/2-100, HEIGHT-350))
        else:
            screen.blit(pygame.transform.rotate(gun,270-rotation),(WIDTH/2-100, HEIGHT-350))
        if clicks[0]:
            pygame.draw.circle(screen, 'red', mouse_pos, 8 )
    # else:


run = True 

while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(bg,(0,0))
    screen.blit(banner,(0,HEIGHT-200))
    show_gun()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
    
    pygame.display.flip()
pygame.quit()