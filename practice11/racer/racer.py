import pygame
import random
import time

pygame.init() # initializes all the pygame sub-modules

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating a game window
# set_mode() takes a tuple as an argument

image_background = pygame.image.load('AnimatedStreet.png')
image_player = pygame.image.load('hann2.png')
image_enemy = pygame.image.load('will2.png')

pygame.mixer.music.load('LoveCrime.mp3')
pygame.mixer.music.set_volume(0.31)
pygame.mixer.music.play(-1, start = 22.31, fade_ms=2000)
    

def draw_text(screen, text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

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
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 5

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.coin1 = pygame.image.load("wine2.png")   # weight = 1
        self.coin2 = pygame.image.load("deer2.png")   # weight = 2
        self.coin3 = pygame.image.load("heart2.png")    # weight = 3

        self.speed = 5
        self.weight = 1
        self.image = self.coin1
        self.rect = self.image.get_rect()

        self.generate_random_rect()

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

        choice = random.randint(1, 3)

        if choice == 1:
            self.image = self.coin1
            self.weight = 1
        elif choice == 2:
            self.image = self.coin2
            self.weight = 2
        else:
            self.image = self.coin3
            self.weight = 3


    def move(self):
    
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.generate_random_rect()

running = True
counter = 0
record = 0


# this object allows us to set the FPS
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin = Coin()
enemy.generate_random_rect()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)


while running: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    
    
    player.move()

    screen.blit(image_background, (0, 0))
    draw_text(screen, f"PTS: {counter}", pygame.font.SysFont("Verdana", 20), (0, 0, 0), 320, 20)
    

    for entity in all_sprites:
        entity.move()

        screen.blit(entity.image, entity.rect)
    
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('bonk.mp3')
        pygame.mixer.music.play(start=1.161)

        time.sleep(2)

        running = False
        screen.fill((133, 14, 14))
        draw_text(screen, f"GAME OVER", pygame.font.SysFont("Verdana", 50), (252, 229, 155), 50, 245)
        draw_text(screen, f"PTS: {counter}", pygame.font.SysFont("Verdana", 40), (252, 229, 155), 130, 315)
        pygame.display.flip()
        
        time.sleep(4)
    

    if pygame.sprite.spritecollideany(player, coin_sprites):
        counter += coin.weight

        if counter % 4 == 0:
            enemy.speed += 1.5

        coin.generate_random_rect()
        
    
    pygame.display.flip() # updates the screen
    clock.tick(FPS) # sets the FPS

pygame.quit()

with open("scoreboard.txt", "a") as f:
    f.write(f'Score: {counter}\n')