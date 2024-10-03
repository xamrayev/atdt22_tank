import pygame
import random
import math

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.speed = 5
        self.color = (0, 255, 0)
        self.angle = 0
        self.bullets = []
        self.score = 0  

    def draw(self, screen):
        point1 = (self.x + self.width * math.cos(self.angle), self.y + self.width * math.sin(self.angle))
        point2 = (self.x + self.width * math.cos(self.angle + 2 * math.pi / 3),
                  self.y + self.width * math.sin(self.angle + 2 * math.pi / 3))
        point3 = (self.x + self.width * math.cos(self.angle - 2 * math.pi / 3),
                  self.y + self.width * math.sin(self.angle - 2 * math.pi / 3))
        pygame.draw.polygon(screen, self.color, [point1, point2, point3])

        for bullet in self.bullets:
            bullet.draw(screen)

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

    def shoot(self):
        bullet = Bullet(self.x, self.y, self.angle)
        self.bullets.append(bullet)

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


class EnemyTank:
    def __init__(self, x, y, player_tank):
        self.x = x
        self.y = y
        self.width = 40
        self.speed = 3
        self.color = (255, 0, 0)
        self.player_tank = player_tank

    def move(self):
        angle = math.atan2(self.player_tank.y - self.y, self.player_tank.x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.width)


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tank Game")
        self.bg_color = (0, 0, 0)
        self.tank = Tank(self.screen_width // 2, self.screen_height // 2)
        self.enemies = []
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

    def spawn_enemy(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, self.screen_width)
            y = -40
        elif side == 'bottom':
            x = random.randint(0, self.screen_width)
            y = self.screen_height + 40
        elif side == 'left':
            x = -40
            y = random.randint(0, self.screen_height)
        else:
            x = self.screen_width + 40
            y = random.randint(0, self.screen_height)

        enemy = EnemyTank(x, y, self.tank)
        self.enemies.append(enemy)

    def check_collision(self):
        player_rect = self.tank.get_rect()
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.game_over = True

        for bullet in self.tank.bullets:
            for enemy in self.enemies:
                if bullet.active and bullet.get_rect().colliderect(enemy.get_rect()):
                    bullet.active = False
                    self.enemies.remove(enemy)
                    self.tank.score += 1  

    def reset_game(self):
        self.tank = Tank(self.screen_width // 2, self.screen_height // 2)
        self.enemies = []
        self.game_over = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.tank.shoot()

            keys = pygame.key.get_pressed()

            if not self.game_over:
                self.tank.move(keys)

                for enemy in self.enemies:
                    enemy.move()

                self.check_collision()

                if pygame.time.get_ticks() % 1000 < 16:
                    self.spawn_enemy()
            else:
                if keys[pygame.K_c]:
                    self.reset_game()

            self.screen.fill(self.bg_color)

            if not self.game_over:
                self.tank.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                font = pygame.font.SysFont(None, 36)
                score_text = font.render(f'Tank Score: {self.tank.score}', True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))
            else:
                font = pygame.font.SysFont(None, 55)
                text = font.render('Game Over. Press C to Restart', True, (255, 255, 255))
                self.screen.blit(text, (self.screen_width // 2 - 200, self.screen_height // 2 - 30))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
