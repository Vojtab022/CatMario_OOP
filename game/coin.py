import pygame
import os
from config import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Pokus o načtení obrázku mince
        image_path = os.path.join("img", "Coin.png")
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        except (pygame.error, FileNotFoundError):
            print(f"Obrázek mince nenalezen v {image_path}, použiju zlatý čtverec.")
            self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
            self.image.fill((255, 215, 0)) # Zlatá barva

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)