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
            self.select.handle_movement(self.selected_entities)

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
