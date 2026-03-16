import pygame
import os
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        image_path = os.path.join("img", "Enemy.png")
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Nové proměnné pro náhodný pohyb
        self.direction = random.choice([-1, 1])
        self.speed = ENEMY_SPEED
        self.move_timer = random.randint(30, 90) # Časovač do další změny pohybu (v počtu snímků)

    def update(self):
        # 1. Odpočet časovače
        self.move_timer -= 1
        
        # 2. Když časovač dojde do nuly, vymyslíme nový pohyb
        if self.move_timer <= 0:
            self.direction = random.choice([-1, 1, 0])  # Doleva, doprava, nebo stát
            self.speed = random.uniform(1, 3.5)         # Náhodná rychlost
            self.move_timer = random.randint(30, 100)   # Znovu natáhnout časovač na náhodnou dobu

        # 3. Aplikace pohybu
        self.rect.x += self.direction * self.speed
        
        # 4. Kontrola okrajů (aby nám neutekl ze hřiště)
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1 # Odrážka zpět doprava
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1 # Odrážka zpět doleva

    def draw(self, screen):
        screen.blit(self.image, self.rect)