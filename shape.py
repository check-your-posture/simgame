import pygame

class Rect(pygame.Rect):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, size)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
    
    def draw_outline(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self, 2)

class Ellipse(Rect):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)
        
    # This draw() function overrides the Rect draw() function. The reason we can do this is because PyGame Ellipses are actually rectangles under the hood.
    # The main difference is that the Ellipse draw() function calls pygame.draw.ellipse() instead of pygame.draw.rect() to achieve an ellipse shape.
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self)
    
    def draw_outline(self, screen):
        pygame.draw.ellipse(screen, (255, 0, 0), self, 2)