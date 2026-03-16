import pygame
import os
import random
from config import *
from game.player import Player
from game.platform import Platform
from game.coin import Coin
from game.enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # --- FONDY A UI ---
        self.font = pygame.font.Font(None, 45)       
        self.large_font = pygame.font.Font(None, 70) 
        
        try:
            self.ui_coin_img = pygame.image.load(os.path.join("img", "Coin.png")).convert_alpha()
            self.ui_coin_img = pygame.transform.scale(self.ui_coin_img, (35, 35))
        except (pygame.error, FileNotFoundError):
            self.ui_coin_img = pygame.Surface((35, 35))
            self.ui_coin_img.fill((255, 215, 0))

        # Tímto se poprvé "zapne" hra a vytvoří se level
        self.reset_game()

    def reset_game(self):
        """Vyresetuje hru do počátečního stavu (vytvoří level od znova)"""
        self.state = "PLAYING" 
        self.score = 0
        
        self.all_sprites = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        # 1. PLATFORMY
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        plat1 = Platform(200, 450, 150, 20)
        plat2 = Platform(450, 350, 150, 20)
        plat3 = Platform(150, 200, 150, 20)
        
        for p in [ground, plat1, plat2, plat3]:
            self.platform.add(p)
            self.all_sprites.add(p)

        # 2. NÁHODNÉ MINCE
        # Tady definujeme všechny možné body, kde se mince můžou objevit (X, Y)
        possible_coin_positions = [
            (250, 400), # Nad plat1 (vlevo)
            (300, 400), # Nad plat1 (vpravo)
            (500, 300), # Nad plat2 (vlevo)
            (550, 300), # Nad plat2 (vpravo)
            (200, 150), # Nad plat3
            (600, SCREEN_HEIGHT - 80), # Na zemi vpravo
            (150, SCREEN_HEIGHT - 80), # Na zemi vlevo
            (350, SCREEN_HEIGHT - 80)  # Na zemi uprostřed
        ]

        # Pomocí random.sample vybereme z našeho seznamu náhodně 4 pozice.
        # Výhoda random.sample je, že nikdy nevybere stejnou pozici dvakrát!
        chosen_positions = random.sample(possible_coin_positions, 4)
        
        # Vytvoříme mince na vylosovaných pozicích
        for pos_x, pos_y in chosen_positions:
            c = Coin(pos_x, pos_y)
            self.coins.add(c)
            self.all_sprites.add(c)

        # 3. NEPŘÍTEL NA ZEMI
        enemy1 = Enemy(400, SCREEN_HEIGHT - 40 - ENEMY_HEIGHT)
        self.enemies.add(enemy1)
        self.all_sprites.add(enemy1)

        self.total_coins = len(self.coins)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state in ["GAME_OVER", "VICTORY"]:
                    if event.key == pygame.K_r:    
                        self.reset_game()
                    elif event.key == pygame.K_q:  
                        self.running = False

    def update(self):
        if self.state == "PLAYING":
            
            fell_off = self.player.update(self.platform)
            if fell_off:
                self.state = "GAME_OVER"

            for enemy in self.enemies:
                enemy.update()

            # --- SBÍRÁNÍ MINCÍ ---
            collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
            if collected_coins:
                self.score += len(collected_coins)
                
                if self.score >= self.total_coins:
                    self.state = "VICTORY"

            # --- KOLIZE S NEPŘÍTELEM (SMRT vs. ZAŠLÁPNUTÍ) ---
            enemy_hit = pygame.sprite.spritecollideany(self.player, self.enemies)
            
            if enemy_hit:
                # Hráč padá (velocity_y > 0) a je nad nepřítelem
                if self.player.velocity_y > 0 and self.player.rect.bottom <= enemy_hit.rect.centery + 15:
                    
                    enemy_hit.kill() # Zabije nepřítele
                    self.player.velocity_y = -8 # Odrazí kočku
                    
                    # Vytvoří novou minci na místě nepřítele
                    dropped_coin = Coin(enemy_hit.rect.x, enemy_hit.rect.y)
                    self.coins.add(dropped_coin)
                    self.all_sprites.add(dropped_coin)
                    
                    # ŘÁDEK self.total_coins += 1 BYL SMAZÁN!
                    # Cíl zůstává pořád 4 mince.
                    
                else:
                    self.state = "GAME_OVER"

    def draw_center_text(self, text, color, y_offset=0, use_large_font=True):
        font = self.large_font if use_large_font else self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        for sprite in self.all_sprites:
            sprite.draw(self.screen)
            
        self.screen.blit(self.ui_coin_img, (15, 15))
        score_text = f"{self.score} / {self.total_coins}"
        text_surface = self.font.render(score_text, True, (0, 0, 0)) 
        self.screen.blit(text_surface, (60, 18))
        
        if self.state != "PLAYING":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128) 
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        if self.state == "GAME_OVER":
            self.draw_center_text("Jste se posral za 5", (255, 50, 50), -30)
            self.draw_center_text("Stiskni R pro restart nebo Q pro konec", (255, 255, 255), 40, use_large_font=False)
        
        elif self.state == "VICTORY":
            self.draw_center_text("Vyhrál jsi! Všechny mince jsou tvé!", (50, 255, 50), -30)
            self.draw_center_text("Stiskni R pro restart nebo Q pro konec", (255, 255, 255), 40, use_large_font=False)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)