import pygame
from config import *

class Platform(pygame.sprite.Sprite):
    """
    Třída Platform - představuje jednu platformu (zelenou plošinu)
    
    Co je platforma?
    - Zelený obdélník, na kterém hráč může stát
    - Statický objekt (nepohybuje se)
    - Hráč na ni může skákat a stát
    
    Dědičnost:
    - Dědí od pygame.sprite.Sprite
    - Sprite = základní herní objekt v Pygame
    - Díky tomu máme metody jako .image, .rect automaticky
    """

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        """
        Konstruktor platformy - vytvoří jednu platformu
        
        Parametry:
            x: Pozice levého horního rohu (osa X, zleva doprava)
            y: Pozice levého horního rohu (osa Y, shora dolů)
            width: Šířka platformy v pixelech
            height: Výška platformy v pixelech
        
        Příklad:
            Platform(100, 500, 200, 20)
            - Vytvoří platformu na pozici X=100, Y=500
            - Šířka 200px, výška 20px
            - Bude to "dlouhý tenký" obdélník
        """
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)