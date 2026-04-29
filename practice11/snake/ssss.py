import pygame
from color_palette import *
import random
import time

pygame.init()

WIDTH = 600
HEIGHT = 600
HEIGHT1 = 770

screen = pygame.display.set_mode((WIDTH, HEIGHT1))

CELL = 50
SQUARE = WIDTH//CELL
counter = 0

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

def draw_text(screen, text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(0, 0), Point(1, 0), Point(2, 0)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy


    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            print("Got food!")
            food.pts += food.value
            
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos(self.body)
            

class Food:
    def __init__(self):
        self.pos = Point((SQUARE - 1) // 2, (SQUARE - 1) // 2)
        self.pts = 0
        self.value = 1
        self.color = colorGREEN
        self.spawn_time = time.time()

    def draw(self):
        pygame.draw.rect( screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL) )

    def generate_random_pos(self, snake_body):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)

            if not any(self.pos.x == s.x and self.pos.y == s.y for s in snake_body):
                break

        food_type = random.randint(1, 4)

        if food_type == 1:
            self.color = colorGREEN
            self.value = 1
        elif food_type == 2:
            self.color = colorBLUE
            self.value = 2
        elif food_type == 3:
            self.color = colorORANGE   
            self.value = 3
        else:
            self.color = colorPUPRLE
            self.value = 5

        self.spawn_time = time.time()


FPS = 5
level = 1
clock = pygame.time.Clock()

food = Food()
snake = Snake()
food.generate_random_pos(snake.body)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1
        
    # checks the right border
    if snake.body[0].x > WIDTH // CELL - 1:
        running = False
    # checks the left border
    if snake.body[0].x < 0:
        running = False
    # checks the bottom border
    if snake.body[0].y > HEIGHT // CELL - 1:
        running = False
    # checks the top border
    if snake.body[0].y < 0:
        running = False

    if not running:
        
        screen.fill((133, 14, 14))
        draw_text(screen, f"GAME OVER", pygame.font.SysFont("Verdana", 69), (252, 229, 155), 96, 245)
        draw_text(screen, f"PTS: {food.pts}", pygame.font.SysFont("Verdana", 50), (252, 229, 155), 209, 340)
        draw_text(screen, f"LEVEL: {level}", pygame.font.SysFont("Verdana", 50), (252, 229, 155), 190, 405)
        pygame.display.flip()
        time.sleep(4.5)
        break
    
    screen.fill(colorBLACK)

    draw_grid()

    draw_text(screen, f"PTS: {food.pts}", pygame.font.SysFont("Verdana", 30), (255, 255, 255), 60, 620)
    draw_text(screen, f"LEVEL: {level}", pygame.font.SysFont("Verdana", 30), (255, 255, 255), 360, 620)
    pygame.draw.rect(screen, colorGREEN, (60, 680, 30, 30))
    pygame.draw.rect(screen, colorBLUE, (60, 730, 30, 30))
    pygame.draw.rect(screen, colorORANGE, (360, 680, 30, 30))
    pygame.draw.rect(screen, colorPUPRLE, (360, 730, 30, 30))
    draw_text(screen, f"- 1 PTS", pygame.font.SysFont("Verdana", 30), (255, 255, 255), 100, 680)
    draw_text(screen, f"- 2 PTS", pygame.font.SysFont("Verdana", 30), (255, 255, 255), 100, 730)
    draw_text(screen, f"- 3 PTS", pygame.font.SysFont("Verdana", 30), (255, 255, 255), 400, 680)
    draw_text(screen, f"- 5 PTS(4s)", pygame.font.SysFont("Verdana", 30), (255, 255, 255), 400, 730)

    snake.move()
    snake.check_collision(food)

    if food.value == 5:
        if time.time() - food.spawn_time >= 4:
            food.generate_random_pos(snake.body)
    

    if food.pts > level * 5:
        level += 1
        FPS += 0.5
    
    print(food.pts, level, FPS)

    snake.draw()
    food.draw()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()