import pygame

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen_width = 800
        self.screen_height = 600
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tank Game")
        
        self.bg_color = (0, 0, 0)  
        
        self.clock = pygame.time.Clock()
        
        self.running = True
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill(self.bg_color)

            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
