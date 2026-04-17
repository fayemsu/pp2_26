import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball")

clock = pygame.time.Clock()

ball_radius = 25
move_amount = 20


ball_x = 400
ball_y = 300


running = True
while running:
    clock.tick(60)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if ball_x - move_amount - ball_radius >= 0:
                    ball_x -= move_amount

            elif event.key == pygame.K_RIGHT:
                if ball_x + move_amount + ball_radius <= WIDTH:
                    ball_x += move_amount

            elif event.key == pygame.K_UP:
                if ball_y - move_amount - ball_radius >= 0:
                    ball_y -= move_amount

            elif event.key == pygame.K_DOWN:
                if ball_y + move_amount + ball_radius <= HEIGHT:
                    ball_y += move_amount

   
    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    pygame.display.flip()

pygame.quit()