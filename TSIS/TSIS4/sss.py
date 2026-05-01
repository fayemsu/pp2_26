# FULL PART 1 — Scene System + Username + PostgreSQL + Leaderboard + Personal Best

import pygame
import random
import time
import psycopg2
from datetime import datetime
from color_palette import *

pygame.init()

from config import load_config

config = load_config()
conn = psycopg2.connect(**config)


WIDTH = 600
HEIGHT = 850
CELL = 30
GRID_HEIGHT = 600

START_FPS = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake PostgreSQL Edition")

clock = pygame.time.Clock()




def create_tables():
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    cur.execute( "SELECT id FROM players WHERE username = %s", (username,))

    result = cur.fetchone()

    if result:
        player_id = result[0]
    else:
        cur.execute( "INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    return player_id


def save_game_result(username, score, level):
    player_id = get_or_create_player(username)

    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions
        (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()


def get_top_scores():
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_personal_best(username):
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username = %s
    """, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0


def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont("Verdana", size)
    img = font.render(text, True, color)
    surface.blit(img, (x, y))



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.body = [ Point(2, 0), Point(1, 0), Point(0, 0)]
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

        pygame.draw.rect( screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_food_collision(self, food):
        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            food.points += 1
            self.body.append(Point(head.x, head.y))
            food.generate_random_position(self.body)
            return True

        return False

    def check_wall_collision(self):
        head = self.body[0]

        if head.x < 0:
            return True
        if head.x >= WIDTH // CELL:
            return True
        if head.y < 0:
            return True
        if head.y >= GRID_HEIGHT // CELL:
            return True

        return False


class Food:
    def __init__(self):
        self.pos = Point(5, 5)
        self.points = 0
        self.value = 1
        self.color = colorGREEN
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_position(self, snake_body, obstacles=[]):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, GRID_HEIGHT // CELL - 1)

            overlap = False

            for s in snake_body:
                if s.x == self.pos.x and s.y == self.pos.y:
                    overlap = True

            for o in obstacles:
                if o.x == self.pos.x and o.y == self.pos.y:
                    overlap = True

            if not overlap:
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

        self.spawn_time = pygame.time.get_ticks()



class PoisonFood:
    def __init__(self):
        self.pos = Point(0, 0)
        self.color = colorPOIS

    def draw(self):
        pygame.draw.rect( screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL) )

    def generate_random_position(self, snake_body, obstacles=[]):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, GRID_HEIGHT // CELL - 1)

            overlap = False

            for s in snake_body:
                if s.x == self.pos.x and s.y == self.pos.y:
                    overlap = True

            for o in obstacles:
                if o.x == self.pos.x and o.y == self.pos.y:
                    overlap = True

            if not overlap:
                break

class PowerUp:
    def __init__(self):
        self.pos = Point(0, 0)

        self.types = ["speed", "slow", "shield"]

        self.type = random.choice(self.types)

        self.spawn_time = pygame.time.get_ticks()
        self.duration = 8000

    def draw(self):
        if self.type == "speed":
            color = colorBBLUE

        elif self.type == "slow":
            color = colorWHITE

        else:
            color = colorYELLOW

        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_position(self, snake_body, obstacles=[]):
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, GRID_HEIGHT // CELL - 1)

            overlap = False

            for s in snake_body:
                if s.x == self.pos.x and s.y == self.pos.y:
                    overlap = True

            for o in obstacles:
                if o.x == self.pos.x and o.y == self.pos.y:
                    overlap = True

            if not overlap:
                break


class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)



class UsernameScene(SceneBase):
    def __init__(self):
        super().__init__()
        self.username = ""

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.username.strip() != "":
                        self.SwitchToScene(MenuScene(self.username))

                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]

                else:
                    if len(self.username) < 15:
                        self.username += event.unicode

    def Render(self, screen):
        screen.fill((30, 30, 30))

        draw_text(screen, "ENTER USERNAME", 40, colorWHITE, 110, 200)
        draw_text(screen, self.username, 40, colorGREEN, 140, 300)
        draw_text(screen, "Press ENTER", 28, colorWHITE, 190, 400)


class MenuScene(SceneBase):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.items = ["Play", "Leaderboard", "Quit"]
        self.active = 0

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.active = (self.active - 1) % len(self.items)

                elif event.key == pygame.K_DOWN:
                    self.active = (self.active + 1) % len(self.items)

                elif event.key == pygame.K_RETURN:

                    if self.active == 0:
                        self.SwitchToScene(GameScene(self.username))

                    elif self.active == 1:
                        self.SwitchToScene(
                            LeaderboardScene(self.username)
                        )

                    elif self.active == 2:
                        self.Terminate()

    def Render(self, screen):
        screen.fill((20, 50, 20))

        draw_text(screen, f"PLAYER: {self.username}", 42, colorWHITE, 180, 80)

        for i, item in enumerate(self.items):
            prefix = "> " if i == self.active else ""
            draw_text(screen, prefix + item, 42, colorWHITE, 180, 200 + i * 90)


class LeaderboardScene(SceneBase):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.rows = get_top_scores()

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.SwitchToScene(MenuScene(self.username))

    def Render(self, screen):
        screen.fill((15, 15, 40))

        draw_text(screen, "TOP 10 LEADERBOARD", 32, colorWHITE, 90, 30)
        y = 110
        for i, row in enumerate(self.rows):
            username, score, level, date = row
            text = f"{i+1}. {username} —  {score} pts — Lvl {level}"
            draw_text(screen, text, 24, colorWHITE, 40, y)
            y += 60

        draw_text(screen, "ESC - Back", 24, colorWHITE, 220, 770)


class GameOverScene(SceneBase):
    def __init__(self, username, score, level):
        super().__init__()

        self.username = username
        self.score = score
        self.level = level

        save_game_result(username, score, level)
        self.best = get_personal_best(username)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.SwitchToScene(GameScene(self.username))

                elif event.key == pygame.K_m:
                    self.SwitchToScene(MenuScene(self.username))

    def Render(self, screen):
        screen.fill((120, 20, 20))

        draw_text(screen, "GAME OVER", 50, colorWHITE, 150, 150)
        draw_text(screen, f"Score: {self.score}", 36, colorWHITE, 220, 280)
        draw_text(screen, f"Level: {self.level}", 36, colorWHITE, 220, 340)
        draw_text(screen, f"Best: {self.best}", 36, colorWHITE, 220, 400)

        draw_text(screen, "R - Retry", 28, colorWHITE, 240, 550)
        draw_text(screen, "M - Main Menu", 28, colorWHITE, 200, 610)




class GameScene(SceneBase):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.snake = Snake()

        self.food = Food()
        self.food.generate_random_position(self.snake.body)

        self.poison = PoisonFood()
        self.poison.generate_random_position(self.snake.body)

        self.powerup = None

        self.level = 1
        self.fps = START_FPS
        self.personal_best = get_personal_best(username)

        self.shield = False
        self.powerup_end_time = 0

        self.obstacles = []

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        for _ in range(self.level + 2):
            while True:
                x = random.randint(2, WIDTH // CELL - 3)
                y = random.randint(2, GRID_HEIGHT // CELL - 3)

                too_close = False

                for s in self.snake.body:
                    if abs(s.x - x) <= 1 and abs(s.y - y) <= 1:
                        too_close = True

                if not too_close:
                    self.obstacles.append(Point(x, y))
                    break

    def draw_grid(self):
        for i in range(GRID_HEIGHT // CELL):
            for j in range(WIDTH // CELL):
                pygame.draw.rect(screen, colorGRAY, (j * CELL, i * CELL, CELL, CELL),1)

    def draw_obstacles(self):
        for wall in self.obstacles:
            pygame.draw.rect(screen, (170, 1, 255), (wall.x * CELL, wall.y * CELL, CELL, CELL))

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    self.snake.dx = 1
                    self.snake.dy = 0

                elif event.key == pygame.K_LEFT:
                    self.snake.dx = -1
                    self.snake.dy = 0

                elif event.key == pygame.K_UP:
                    self.snake.dx = 0
                    self.snake.dy = -1

                elif event.key == pygame.K_DOWN:
                    self.snake.dx = 0
                    self.snake.dy = 1

    def check_poison_collision(self):
        head = self.snake.body[0]

        if head.x == self.poison.pos.x and head.y == self.poison.pos.y:
            if len(self.snake.body) <= 2:
                self.SwitchToScene(
                    GameOverScene(self.username, self.food.points, self.level) )
                return

            self.snake.body.pop()
            self.snake.body.pop()
            # self.food.pts -= 1

            self.poison.generate_random_position( self.snake.body, self.obstacles)

    def check_powerup_collision(self):
        if self.powerup is None:
            return

        head = self.snake.body[0]

        if head.x == self.powerup.pos.x and head.y == self.powerup.pos.y:

            now = pygame.time.get_ticks()

            if self.powerup.type == "speed":
                self.fps += 2
                self.powerup_end_time = now + 5000

            elif self.powerup.type == "slow":
                self.fps = max(3, self.fps - 2)
                self.powerup_end_time = now + 5000

            elif self.powerup.type == "shield":
                self.shield = True

            self.powerup = None

    def check_obstacle_collision(self):
        head = self.snake.body[0]

        for wall in self.obstacles:
            if head.x == wall.x and head.y == wall.y:

                if self.shield:
                    self.shield = False
                    return False

                return True

        return False

    def Update(self):
        now = pygame.time.get_ticks()

        self.snake.move()

        if self.snake.check_wall_collision():
            if self.shield:
                self.shield = False
            else:
                self.SwitchToScene(
                    GameOverScene(self.username, self.food.points, self.level) )
                return

        if self.check_obstacle_collision():
            self.SwitchToScene(
                GameOverScene(self.username, self.food.points, self.level) )
            return

        head = self.snake.body[0]

        if head.x == self.food.pos.x and head.y == self.food.pos.y:
            self.food.points += self.food.value

            self.snake.body.append(Point(head.x, head.y) )

            self.food.generate_random_position(self.snake.body, self.obstacles )

        if self.food.value == 5:
            if now - self.food.spawn_time >= 4000:
                self.food.generate_random_position( self.snake.body, self.obstacles)

        self.check_poison_collision()
        self.check_powerup_collision()

        if self.powerup is None and random.randint(1, 200) == 1:
            self.powerup = PowerUp()
            self.powerup.generate_random_position(self.snake.body, self.obstacles)

        if self.powerup:
            if now - self.powerup.spawn_time >= 8000:
                self.powerup = None

        if self.powerup_end_time != 0 and now >= self.powerup_end_time:
            self.fps = START_FPS + (self.level - 1)
            self.powerup_end_time = 0

        if self.food.points > self.level * 5:
            self.level += 1
            self.fps += 1
            self.generate_obstacles()

    def Render(self, screen):
        screen.fill(colorBLACK)

        # self.draw_grid()
        self.draw_obstacles()

        draw_text( screen, f"PTS: {self.food.points}",  28, colorWHITE, 60, 620)

        draw_text( screen, f"LEVEL: {self.level}", 28, colorWHITE, 210, 620)

        draw_text( screen, f"BEST: {self.personal_best}", 28, (242, 236, 121), 400, 620)

        pygame.draw.rect(screen, colorGREEN, (60, 680, 25, 25))
        pygame.draw.rect(screen, colorBLUE, (60, 720, 25, 25))
        pygame.draw.rect(screen, colorORANGE, (60, 760, 25, 25))
        pygame.draw.rect(screen, colorPUPRLE, (60, 800, 25, 25))

        pygame.draw.rect(screen, colorPOIS, (360, 680, 25, 25))
        pygame.draw.rect(screen, colorBBLUE, (360, 720, 25, 25))
        pygame.draw.rect(screen, colorWHITE, (360, 760, 25, 25))
        pygame.draw.rect(screen, colorYELLOW, (360, 800, 25, 25))

        draw_text(screen, f"- 1 PTS", 20, (255, 255, 255), 90, 680)
        draw_text(screen, f"- 2 PTS", 20, (255, 255, 255), 90, 720)
        draw_text(screen, f"- 3 PTS", 20, (255, 255, 255), 90, 760)
        draw_text(screen, f"- 5 PTS(4s)", 20, (255, 255, 255), 90, 800)

        draw_text(screen, f"- snake shortening", 20, (255, 255, 255), 390, 680)
        draw_text(screen, f"- faster", 20, (255, 255, 255), 390, 720)
        draw_text(screen, f"- slower", 20, (255, 255, 255), 390, 760)
        draw_text(screen, f"- shield", 20, (255, 255, 255), 390, 800)

        if self.shield:
            draw_text( screen, "SHIELD ACTIVE", 24, colorYELLOW, 170, 720)

        self.snake.draw()
        self.food.draw()
        self.poison.draw()

        if self.powerup:
            self.powerup.draw()



def run_game(starting_scene):
    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        filtered_events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()

        if isinstance(active_scene, GameScene):
            clock.tick(active_scene.fps)
        else:
            clock.tick(60)



create_tables()
run_game(UsernameScene())

pygame.quit()