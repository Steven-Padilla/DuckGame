import pygame
import math
import threading

#Variable for thread
mutex = threading.Lock()

#variables for pygame
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
target_images=[pygame.transform.scale(pygame.image.load(f'Assets/duckFlying.png'),(150,150)),
               pygame.transform.scale(pygame.image.load(f'Assets/duckSleeping.png'),(100,100))]
pos_target=[]
for i in range(2):
    pos_target.append(target_images[i].get_rect())

speed=[2,-2]

class Hilo(threading.Thread):
    global image;
    image=0
    def __init__(self,id,lastTargetX,lastTargetY):
        threading.Thread.__init__(self)
        self.id=id
        self.lastTargetX=lastTargetX
        self.lastTargetY=lastTargetY
        pos_target[1][0]=self.lastTargetX 
        pos_target[1][1]=self.lastTargetY -200

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos) 
        screen.blit(target_images[image],pos_target[1])
        
        pos_target[1]=pos_target[1].move(speed)
        if pos_target[1].left < 0 or pos_target[1].right > WIDTH:
            speed[0] = -speed[0]
        if pos_target[1].top < 0 or pos_target[1].bottom > HEIGHT -200:
            speed[1] = -speed[1]
            
        # pos_target[1].center= self.lastTargetX, self.lastTargetY
        # if pos_target[1][0] < 800 :
        #     if pos_target[1][1]>0:
        #         screen.blit(target_images[image],pos_target[1])
        #         self.lastTargetY-=2
        #         self.lastTargetX+=1
        #         print(pos_target[1][1])
        # elif pos_target[1][0]<800 and pos_target[1][1]<600:
        #     screen.blit(target_images[image],pos_target[1])
        #     self.lastTargetY+=2
        #     self.lastTargetX+=1
    

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


def show_ducks(duck,lastTargetX,lastTargetY):
    coords_list=[]
    
    
    pos_target[1].center= lastTargetX, lastTargetY
    screen.blit(target_images[0],pos_target[1])
    
    print(lastTargetX)
    pygame.display.update()
    
    # for i in range(5):
    #     coords_list.append([lastTargetX,lastTargetY])
    #     lastTargetX+=150    
    
    # for i in range(5):
    #     # pos_target[0].center= lastTargetX, 700
    #     pos_target[1].center= coords_list[i]
    #     lastTargetX+=150
    #     screen.blit(target_images[1],pos_target[1])
    #     coords_list[0][1]-=1
    #     print(coords_list[0][1])
    
    

run = True 
lastTargetY=700
lastTargetX=150
duck=Hilo(1,lastTargetX,lastTargetY)
duck.start()
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(bg,(0,0))
    screen.blit(banner,(0,HEIGHT-200))
    show_gun()
    
    ducks_list=[]
    duck.run()
    # for i in range(5):
    #     ducks_list.append(Hilo(i,lastTargetX,lastTargetY))
    #     lastTargetX+=150
    # for duck in ducks_list:
    #     duck.start()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
    
    pygame.display.update()
pygame.quit()