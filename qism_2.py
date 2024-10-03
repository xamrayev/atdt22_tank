import pygame
import math

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.speed = 5
        self.color = (0, 255, 0)  
        self.angle = 0  

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

            keys = pygame.key.get_pressed()

            self.tank.move(keys)
            
            self.screen.fill(self.bg_color)
            
            self.tank.draw(self.screen)
            
            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
