import pygame
import sys
import random

# Move to a graphics specific file after verifying that this works
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
        
    # Overrides the Rect draw() method since pygame.ellipse shapes use rectangles under the hood,
    # but still need to call a different draw function to appear as an ellipse
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self)
    
    def draw_outline(self, screen):
        pygame.draw.ellipse(screen, (255, 0, 0), self, 2)

class Entity:
    # Initialize the entity with position and shape
    def __init__(self, shape):
        self.shape = shape

    # Draw the entity on the screen
    def draw(self, screen):
        self.shape.draw(screen)

    # Move the entity
    def move(self, dx, dy):
        self.shape.move_ip(dx, dy)

class Obstacle(Entity):
    # Initialize the obstacle with position, shape, and color
    def __init__(self, shape):
        super().__init__(shape)

    # Check if a point is within the Obstacle
    def contains_point(self, point):
        return self.shape.collidepoint(point)

class NPC(Entity):
    # NPC inherits from Entity, so we just pass all the arguments to the Entity constructor
    def __init__(self, shape):
        super().__init__(shape)

    # Check if a point is within the NPC
    def contains_point(self, point):
        return self.shape.collidepoint(point)

class Game:
    # Initialize the game
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.last_move_time = 0
        self.WIDTH, self.HEIGHT = 640, 480
        self.MOVE_DISTANCE = 1
        self.MOVE_DELAY = 40

        # Setup the screen and entities
        self.screen, self.entities = self.setup()
        self.selected_entities = []

    # Start the main game loop
    def main(self):
        self.main_game_loop()

    class SelectedEntity:
        # Initialize the selected entity
        def __init__(self, entity):
            self.entity = entity

        # Draw the selected entity and a red outline
        def draw(self, screen):
            self.entity.draw(screen)
            self.entity.shape.draw_outline(screen) # I'm not really sure if this is hacky?

        # Move the selected entity
        def move(self, dx, dy):
            self.entity.move(dx, dy)

    # Select entities that are within the selection rectangle
    def select_entities(self, entities, selection_rect):
        return [self.SelectedEntity(entity) for entity in entities if entity.shape.colliderect(selection_rect)]

    # Deselect all entities
    def deselect_entities(self, selected_entities):
        selected_entities.clear()

    # Handle mouse events for selection
    def handle_selection(self, event, entities, selected_entities, selecting, dragged_entity, start_pos, end_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            selecting = True
            start_pos = event.pos
            dragged_entity = next((entity for entity in entities if entity.contains_point(event.pos)), None)
            if dragged_entity:
                self.deselect_entities(selected_entities)
                selected_entities.extend(self.select_entities([dragged_entity], dragged_entity.shape))
        elif event.type == pygame.MOUSEBUTTONUP:
            selecting = False
            end_pos = event.pos
            self.deselect_entities(selected_entities)
            dragged_entity = None
            if start_pos == end_pos:
                clicked_entity = next((entity for entity in entities if entity.contains_point(event.pos)), None)
                if clicked_entity:
                    selected_entities.extend(self.select_entities([clicked_entity], clicked_entity.shape))
            else:
                selection_rect = pygame.Rect(min(start_pos[0], end_pos[0]), 
                                             min(start_pos[1], end_pos[1]), 
                                             abs(start_pos[0] - end_pos[0]), 
                                             abs(start_pos[1] - end_pos[1]))
                selected_entities.extend(self.select_entities(entities, selection_rect))
            start_pos = (0, 0)
            end_pos = None
        elif event.type == pygame.MOUSEMOTION and selecting:
            if dragged_entity and pygame.mouse.get_pressed(num_buttons=3)[0]:
                dragged_entity.shape.center = event.pos
            elif selecting:
                end_pos = event.pos

        return selecting, dragged_entity, start_pos, end_pos

    # Handle keyboard events for movement
    def handle_movement(self, selected_entities):
        moved = False
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dy = -self.MOVE_DISTANCE
            moved = True
        if keys[pygame.K_DOWN]:
            dy = self.MOVE_DISTANCE
            moved = True
        if keys[pygame.K_LEFT]:
            dx = -self.MOVE_DISTANCE
            moved = True
        if keys[pygame.K_RIGHT]:
            dx = self.MOVE_DISTANCE
            moved = True
        if moved and pygame.time.get_ticks() - self.last_move_time > self.MOVE_DELAY:
            for selected_entity in selected_entities:
                selected_entity.move(dx, dy)
            self.last_move_time = pygame.time.get_ticks()

    # Set up the game screen and entities
    def setup(self):
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        npc_count = random.randint(4, 9)
        obstacle_count = random.randint(2, 4)
        
        generate_random_ellipse = lambda: Ellipse(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        generate_random_square = lambda: Rect(random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), 30, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        npcs = [NPC(generate_random_ellipse()) for _ in range(npc_count)]
        obstacles = [Obstacle(generate_random_square()) for _ in range(obstacle_count)]
        
        entities = npcs + obstacles
        return screen, entities

    # Main game loop
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
                    selecting, dragged_entity, start_pos, end_pos = self.handle_selection(event, self.entities, self.selected_entities, selecting, dragged_entity, start_pos, end_pos)
            self.handle_movement(self.selected_entities)

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
