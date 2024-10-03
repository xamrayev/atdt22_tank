import pygame
import math

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.radius = 5
        self.color = (255, 0, 0)  

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 40 
        self.color = (0, 255, 0)  
        self.angle = 0  
        self.bullets = []  

    def draw(self, screen):
        point1 = (self.x + self.width * math.cos(self.angle), self.y + self.width * math.sin(self.angle))
        point2 = (self.x + self.width * math.cos(self.angle + 2 * math.pi / 3),
                  self.y + self.width * math.sin(self.angle + 2 * math.pi / 3))
        point3 = (self.x + self.width * math.cos(self.angle - 2 * math.pi / 3),
                  self.y + self.width * math.sin(self.angle - 2 * math.pi / 3))
        pygame.draw.polygon(screen, self.color, [point1, point2, point3])

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

    def fire(self):
        bullet = Bullet(self.x, self.y, self.angle)
        self.bullets.append(bullet)

    def update_bullets(self, screen_width, screen_height):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
                self.bullets.remove(bullet)

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen_width = 800
        self.screen_height = 600
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tank Game")
        
        self.bg_color = (0, 0, 0) 
        
        self.tank = Tank(self.screen_width // 2, self.screen_height // 2)
        
        self.clock = pygame.time.Clock()
        
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.tank.fire()

            keys = pygame.key.get_pressed()

            self.tank.move(keys)
            
            self.tank.update_bullets(self.screen_width, self.screen_height)
            
            self.screen.fill(self.bg_color)
            
            self.tank.draw(self.screen)

            for bullet in self.tank.bullets:
                bullet.draw(self.screen)
            
            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
