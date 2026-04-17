import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Clock")

WHITE = (255, 255, 255)

background = pygame.image.load("redclock.png")
minute_hand = pygame.image.load("actmin.png")
second_hand = pygame.image.load("min12.png")

background = pygame.transform.scale(background, (900, 900))
minute_hand = pygame.transform.scale(minute_hand, (250, 80))
second_hand = pygame.transform.scale(second_hand, (300, 70))

clock_center = (450, 450)

clock = pygame.time.Clock()
over = False


def draw_hand(image, angle, center_pos):
    rotated_image = pygame.transform.rotate(image, -angle)

    offset = pygame.math.Vector2(-image.get_width() / 2, 0)
    rotated_offset = offset.rotate(angle)

    new_center = (
        center_pos[0] - rotated_offset.x,
        center_pos[1] - rotated_offset.y
    )

    rect = rotated_image.get_rect(center=new_center)
    screen.blit(rotated_image, rect)


while not over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                over = True


    second = datetime.datetime.now().second 
    minute = datetime.datetime.now().minute 

    minute_angle = (minute / 60) * 360 - 90
    second_angle = (second / 60) * 360 - 90

    screen.blit(background)

    draw_hand(minute_hand, minute_angle, clock_center)
    draw_hand(second_hand, second_angle, clock_center)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()