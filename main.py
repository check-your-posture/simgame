import pygame
import sys
import random
from shape import Rect, Ellipse
from entity import NPC, Obstacle
from selection import Select

class Game:
    # Initialize the game
    def __init__(self):
        pygame.init()
        #self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = 640, 480

        # Setup the screen and entities
        self.screen, self.entities = self.setup()

        self.select = Select()
        self.selected_entities = []

    # Start the main game loop
    def main(self):
        self.main_game_loop()

    # Set up the game screen and entities
    def setup(self):
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        npc_count = random.randint(4, 9)
        obstacle_count = random.randint(2, 4)

        # Lambdas are like on-the-fly functions, you can make them quick, small, wherever you need them, and you can pass them into functions as if they are objects.
        generate_random_ellipse = lambda: Ellipse(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        generate_random_square = lambda: Rect(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 30, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        npcs = [NPC(generate_random_ellipse()) for _ in range(npc_count)]
        obstacles = [Obstacle(generate_random_square()) for _ in range(obstacle_count)]
        
        entities = npcs + obstacles
        return screen, entities

    # This is the first version of the collision checking. It's extremely simple, all it does is take the entity's current position and add the change in x and y to it, and then check if the new position collides with any other entity.
    # It does this by iterating through all the existing entities, checking each to see if the moving entity will collide with any others.
    # I want to improve on this in a few ways:
    #   1. Abstract the code further by turning `colliderect()` into a function that can be called on any shape (not just rectangles)
    #   2. Right now, to do the collision checking, we have to create a new tempory rectangle (this is the `pygame.Rect()` call below) and check if collision is going to happen at that new location.
    #       The code below is sloppy because it assumes that every entity that's passed into the function is a rectangle, which will definitely not always be the case.
    #       Perhaps what I'll do is I'll make it so that, down at the entity level where this lambda eventually gets called, the entity itself will be responsible for passing in an updated shape.
    #       That way, the collision checking lambda can be written in a way that doesn't assume the entity is a rectangle.
    def check_collision(self, entity, dx, dy):
        new_position = pygame.Rect(entity.shape.x + dx, entity.shape.y + dy, entity.shape.width, entity.shape.height)
        return any(new_position.colliderect(other_entity.shape) for other_entity in self.entities if other_entity != entity)

    def main_game_loop(self):
        selecting = False
        dragged_entity = None
        start_pos = (0, 0)
        end_pos = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    selecting, dragged_entity, start_pos, end_pos = self.select.handle_selection(event, self.entities, self.selected_entities, selecting, dragged_entity, start_pos, end_pos) 

            # For clarity: what I'm doing here is passing the check_collision function itself into the handle_movement function.
            # This way, the handle_movement function can call the check_collision function (do collision checking) whenever it needs to, and it doesn't need to know anything about how the collision checking works.
            # This will also allow us to change the check_collision function later on.
            self.select.handle_movement(self.selected_entities, self.check_collision)

            self.screen.fill((0, 0, 0))
            for entity in self.entities:
                entity.draw(self.screen)
            for selected_entity in self.selected_entities:
                selected_entity.draw(self.screen)

            # Draws the selection box
            if selecting and end_pos is not None:
                selection_rect = pygame.Rect(min(start_pos[0], end_pos[0]), 
                                             min(start_pos[1], end_pos[1]), 
                                             abs(start_pos[0] - end_pos[0]), 
                                             abs(start_pos[1] - end_pos[1]))
                pygame.draw.rect(self.screen, (255, 0, 0), selection_rect, 2)
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.main()
    pygame.quit()
