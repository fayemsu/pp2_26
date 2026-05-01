import pygame
import random
import json
import os
import time

pygame.init()
pygame.mixer.init()


WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (140, 20, 20)
GREEN = (20, 150, 20)
GRAY = (170, 170, 170)
GOLD = (252, 229, 155)

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

FONT_SMALL = pygame.font.SysFont("Verdana", 18)
FONT_MEDIUM = pygame.font.SysFont("Verdana", 28)
FONT_BIG = pygame.font.SysFont("Verdana", 44)

player_name = "Player"

image_background = pygame.image.load("AnimatedStreet.png")
image_player = pygame.image.load("hann2.png")
image_enemy = pygame.image.load("will2.png")
image_wine = pygame.image.load("wine2.png")     # +1
image_deer = pygame.image.load("deer2.png")     # +2
image_heart = pygame.image.load("heart2.png")   # +3
image_oil = pygame.image.load("oil2.png")
image_barrier = pygame.image.load("barrier2.png")
image_pothole = pygame.image.load("pothole2.png")
image_nitro = pygame.image.load("nitro2.png")
image_shield = pygame.image.load("shield2.png")
image_repair = pygame.image.load("repair2.png")
image_traffic = pygame.image.load("will2.png")

pygame.mixer.music.load("LoveCrime.mp3")
pygame.mixer.music.set_volume(0.3)

DEFAULT_SETTINGS = {
    "sound": True,
    "difficulty": "Normal",
    "car_color": "Default"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_score(name, score, distance):
    board = load_leaderboard()

    board.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]

    save_leaderboard(board)


settings = load_settings()

def draw_text(screen, text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))



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



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img=image_enemy, speed=5):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.speed = speed
        self.generate()

    def generate(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.generate()

    def generate(self):
        choice = random.randint(1, 3)

        if choice == 1:
            self.image = image_wine
            self.value = 1
        elif choice == 2:
            self.image = image_deer
            self.value = 2
        else:
            self.image = image_heart
            self.value = 3

        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [image_oil, image_barrier, image_pothole]
        self.speed = 5
        self.generate()

    def generate(self):
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.type = None
        self.timer = 0
        self.generate()

    def generate(self):
        choice = random.choice(["nitro", "shield", "repair"])

        if choice == "nitro":
            self.image = image_nitro
        elif choice == "shield":
            self.image = image_shield
        else:
            self.image = image_repair

        self.type = choice
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0
        self.timer = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, self.speed)

        # disappear after timeout
        if self.rect.top > HEIGHT or pygame.time.get_ticks() - self.timer > 5000:
            self.generate()



class MainMenuScene(SceneBase):
    def __init__(self):
        super().__init__()
        self.items = [
            "Play",
            "Leaderboard",
            "Settings",
            "Quit"
        ]
        self.index = 0

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.items)

                elif event.key == pygame.K_UP:
                    self.index = (self.index - 1) % len(self.items)

                elif event.key == pygame.K_RETURN:
                    if self.index == 0:
                        self.SwitchToScene(UsernameScene())

                    elif self.index == 1:
                        self.SwitchToScene(LeaderboardScene())

                    elif self.index == 2:
                        self.SwitchToScene(SettingsScene())

                    elif self.index == 3:
                        self.Terminate()

    def Render(self, screen):
        screen.fill((20, 20, 20))
        draw_text(screen, "HANNIBAL RACER", pygame.font.SysFont("Verdana", 40), GOLD, 19, 96)
        for i, item in enumerate(self.items):
            text = item
            if i == self.index:
                text = "> " + text

            draw_text(screen, text, FONT_MEDIUM, WHITE, 90, 200 + i * 60)


class UsernameScene(SceneBase):
    def __init__(self):
        super().__init__()
        self.name = ""

    def ProcessInput(self, events, pressed_keys):
        global player_name

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.name.strip() != "":
                        player_name = self.name
                        self.SwitchToScene(GameScene())

                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                else:
                    if len(self.name) < 12:
                        self.name += event.unicode

    def Render(self, screen):
        screen.fill(BLACK)

        draw_text(screen, "ENTER NAME", FONT_BIG, GOLD, 60, 150)
        draw_text(screen, self.name, FONT_MEDIUM, WHITE, 100, 280)


class SettingsScene(SceneBase):
    def __init__(self):
        super().__init__()
        self.items = ["Sound", "Difficulty", "Back"]
        self.index = 0

    def ProcessInput(self, events, pressed_keys):
        global settings

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.items)

                elif event.key == pygame.K_UP:
                    self.index = (self.index - 1) % len(self.items)

                elif event.key == pygame.K_RETURN:

                    if self.index == 0:
                        settings["sound"] = not settings["sound"]

                    elif self.index == 1:
                        if settings["difficulty"] == "Easy":
                            settings["difficulty"] = "Normal"
                        elif settings["difficulty"] == "Normal":
                            settings["difficulty"] = "Hard"
                        else:
                            settings["difficulty"] = "Easy"

                    elif self.index == 2:
                        save_settings(settings)
                        self.SwitchToScene(MainMenuScene())

    def Render(self, screen):
        screen.fill((30, 30, 30))

        draw_text(screen, "SETTINGS", FONT_BIG, GOLD, 100, 80)

        sound = "ON" if settings["sound"] else "OFF"

        if not settings['sound']:
            pygame.mixer.music.stop()


        lines = [
            f"Sound: {sound}",
            f"Difficulty: {settings['difficulty']}",
            "Back"
        ]

        for i, item in enumerate(lines):
            text = item
            if i == self.index:
                text = "> " + text

            draw_text(screen, text, FONT_MEDIUM, WHITE, 60, 200 + i * 70)


class LeaderboardScene(SceneBase):
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.SwitchToScene(MainMenuScene())

    def Render(self, screen):
        screen.fill(BLCK if False else BLACK)

        draw_text(screen, "TOP 10", FONT_BIG, GOLD, 120, 40)

        board = load_leaderboard()

        y = 120
        for i, item in enumerate(board):
            text = f"{i+1}.     {item['name']:<15}  {item['score']:<15}  {item['distance']}m"
            draw_text(screen, text, FONT_SMALL, WHITE, 20, y)
            y += 40

        draw_text(screen, "ENTER = BACK", FONT_SMALL, GRAY, 130, 550)


class GameScene(SceneBase):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.enemy = Enemy()
        self.coin = Coin()
        self.obstacle = Obstacle()
        self.powerup = PowerUp()

        self.score = 0
        self.distance = 0

        self.active_power = None
        self.power_end = 0

        if settings["sound"]:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def ProcessInput(self, events, pressed_keys):
        pass

    def activate_power(self, kind):
        self.active_power = kind

        if kind == "nitro":
            self.player.speed = 9
            self.power_end = pygame.time.get_ticks() + 4000

        elif kind == "shield":
            self.player.shield = True
            self.power_end = 999999999

        elif kind == "repair":
            self.score += 10
            self.active_power = None

    def Update(self):
        self.player.move()
        self.enemy.move()
        self.coin.move()
        self.obstacle.move()
        self.powerup.move()

        self.distance += 1

        # difficulty scaling
        if self.distance % 400 == 0:
            self.enemy.speed += 1
            self.obstacle.speed += 1

        # coin
        if pygame.sprite.collide_rect(self.player, self.coin):
            self.score += self.coin.value
            self.coin.generate()

        # powerup
        if pygame.sprite.collide_rect(self.player, self.powerup):
            self.activate_power(self.powerup.type)
            self.powerup.generate()

        # power timeout
        if self.active_power == "nitro":
            if pygame.time.get_ticks() > self.power_end:
                self.player.speed = 5
                self.active_power = None

        # enemy collision
        if pygame.sprite.collide_rect(self.player, self.enemy):
            if self.player.shield:
                self.player.shield = False
                self.active_power = None
                self.enemy.generate()
            else:
                add_score(player_name, self.score, self.distance)
                self.SwitchToScene(GameOverScene(self.score, self.distance))

        # obstacle collision
        if pygame.sprite.collide_rect(self.player, self.obstacle):
            if self.player.shield:
                self.player.shield = False
                self.active_power = None
                self.obstacle.generate()
            else:
                add_score(player_name, self.score, self.distance)
                self.SwitchToScene(GameOverScene(self.score, self.distance))

    def Render(self, screen):
        screen.blit(image_background, (0, 0))

        for obj in [self.enemy, self.coin, self.obstacle, self.powerup, self.player]:
            screen.blit(obj.image, obj.rect)

        draw_text(screen, f"PTS: {self.score}", FONT_SMALL, BLACK, 290, 20)
        draw_text(screen, f"DIST: {self.distance}", FONT_SMALL, BLACK, 250, 45)

        if self.active_power:
            draw_text(screen, f"POWER: {self.active_power}", FONT_SMALL, RED, 20, 20)


class GameOverScene(SceneBase):
    def __init__(self, score, distance):
        super().__init__()
        self.score = score
        self.distance = distance

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.SwitchToScene(GameScene())

                elif event.key == pygame.K_RETURN:
                    self.SwitchToScene(MainMenuScene())

    def Render(self, screen):
        screen.fill((80, 0, 0))

        draw_text(screen, "GAME OVER", FONT_BIG, GOLD, 65, 150)
        draw_text(screen, f"SCORE: {self.score}", FONT_MEDIUM, WHITE, 130, 260)
        draw_text(screen, f"DISTANCE: {self.distance}", FONT_MEDIUM, WHITE, 95, 310)

        draw_text(screen, "R = Retry", FONT_SMALL, WHITE, 155, 430)
        draw_text(screen, "ENTER = Menu", FONT_SMALL, WHITE, 130, 470)




def run_game(start_scene):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hannibal Racer")

    clock = pygame.time.Clock()
    active_scene = start_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active_scene.Terminate()
            else:
                events.append(event)

        active_scene.ProcessInput(events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


run_game(MainMenuScene())