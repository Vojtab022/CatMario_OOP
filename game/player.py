import pygame
import os
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image_loaded = False

        for name in ["Cat_Mario", "cat", "player", "kocka"]:
            for ext in ["png", "jpg", "jpeg", "webp"]:
                try:
                    image_path = os.path.join("img", f"{name}.{ext}")
                    self.image = pygame.image.load(image_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    print(f"Načten obrázek hráče: {image_path}")
                    image_loaded = True

                    break
                
                except (pygame.error, FileNotFoundError):
                    print(f"Player nebyl nalezen {pygame.error}")
                    continue
        
        if not image_loaded:
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(PLAYER_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = False
    
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
        
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_POWER
            self.on_ground = False

        self.velocity_y += GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15
        
        self.rect.x += self.velocity_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        self.rect.y += self.velocity_y

        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0 

        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)       