import sys, pygame

pygame.init()

size = width, height = 640, 480
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
ball = pygame.transform.scale(pygame.image.load(f'Assets/duckFlying.png'),(150,150)).convert()
# ball.set_color(255,255,255)
ballrect = ball.get_rect()

loop = 1
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = 0

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()