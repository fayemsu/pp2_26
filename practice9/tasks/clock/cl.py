import pygame
import math
import datetime

pygame.init()


screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Clock")

background = pygame.image.load("redclock.png")
background = pygame.transform.scale(background, (900, 900))

center_x = 900 // 2 + 2
center_y = 900 // 2 + 8


beige = (240, 229, 168)


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    
    screen.blit(background, (0, 0))

    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second

    minute_angle = math.radians((minute / 60) * 360 - 90)
    second_angle = math.radians((second / 60) * 360 - 90)

  
    min_x = center_x + math.cos(minute_angle) * 221
    min_y = center_y + math.sin(minute_angle) * 221

    sec_x = center_x + math.cos(second_angle) * 300
    sec_y = center_y + math.sin(second_angle) * 300

    
    pygame.draw.line(screen, beige, (center_x, center_y), (min_x, min_y), 5)
    pygame.draw.line(screen, beige, (center_x, center_y), (sec_x, sec_y), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()