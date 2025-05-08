import pygame
import random
import math
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.boom_sound = pygame.mixer.Sound('./src/boom.mp3')
        self.shoot_sound = pygame.mixer.Sound('./src/shoot.mp3')

    def play_boom(self):
        pygame.mixer.Sound.play(self.boom_sound)

    def play_shoot(self):
        pygame.mixer.Sound.play(self.shoot_sound)

class Boom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 30  
        self.active = True

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False

    def draw(self, screen):
        font = pygame.font.SysFont(None, 36)
        text = font.render('BOOM', True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

class Tank:
    def __init__(self, x, y, sound_manager):
        self.x = x
        self.y = y
        self.width = 40
        self.speed = 5
        self.color = (0, 255, 0)
        self.angle = 0
        self.bullets = []
        self.score = 0 
        self.booms = []  
        self.sound_manager = sound_manager

    def draw(self, screen):
        point1 = (self.x + self.width * math.cos(self.angle), self.y + self.width * math.sin(self.angle))
        point2 = (self.x + self.width * math.cos(self.angle + 2 * math.pi / 3),
                  self.y + self.width * math.sin(self.angle + 2 * math.pi / 3))
        point3 = (self.x + self.width * math.cos(self.angle - 2 * math.pi / 3),
                  self.y + self.width * math.sin(self.angle - 2 * math.pi / 3))
        pygame.draw.polygon(screen, self.color, [point1, point2, point3])

        for bullet in self.bullets:
            bullet.draw(screen)

        for boom in self.booms:  
            boom.draw(screen)
            
    def move(self, keys):
        if keys[pygame.K_w]:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
        if keys[pygame.K_s]:
            self.x -= self.speed * math.cos(self.angle)
            self.y -= self.speed * math.sin(self.angle)
        if keys[pygame.K_a]:
            self.angle -= 0.1
        if keys[pygame.K_d]:
            self.angle += 0.1

        for bullet in self.bullets:
            bullet.move()

        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        self.booms = [boom for boom in self.booms if boom.active]
        for boom in self.booms:
            boom.update()

    def shoot(self):
        bullet = Bullet(self.x, self.y, self.angle)
        self.bullets.append(bullet)
        self.sound_manager.play_shoot()  # Play shoot sound

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.width // 2, self.width, self.width)

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.active = True
        self.angle = angle

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)

    def get_rect(self):
        return pygame.Rect(self.x - 5, self.y - 5, 10, 10)

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.bg_image = pygame.image.load('./src/background.jpg')
        self.sound_manager = SoundManager() 

        self.tank = Tank(self.screen_width // 2, self.screen_height // 2, self.sound_manager)
        self.enemies = []
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

    def check_collision(self):
        player_rect = self.tank.get_rect()
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.game_over = True

        for bullet in self.tank.bullets:
            for enemy in self.enemies:
                if bullet.active and bullet.get_rect().colliderect(enemy.get_rect()):
                    bullet.active = False
                    self.tank.booms.append(Boom(enemy.x + enemy.width // 2, enemy.y + enemy.width // 2))
                    self.enemies.remove(enemy)
                    self.sound_manager.play_boom() 
                    self.tank.score += 1  

    def run(self):
        while self.running:
            self.screen.blit(self.bg_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.tank.shoot()

            keys = pygame.key.get_pressed()

            if not self.game_over:
                self.tank.move(keys)
                self.check_collision()

            self.tank.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()