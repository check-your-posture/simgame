import pygame

class Select:
    def __init__(self):
        self.last_move_time = 0
        self.MOVE_DISTANCE = 1
        self.MOVE_DELAY = 40

    class SelectedEntity:
        def __init__(self, entity):
            self.entity = entity

        # Draw the selected entity and a red outline
        def draw(self, screen):
            self.entity.draw(screen)
            self.entity.shape.draw_outline(screen) # I'm not really sure if this is hacky?

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
            # If an entity was being dragged, skip the selection rectangle logic
            if dragged_entity:
                dragged_entity = None
            else:
                self.deselect_entities(selected_entities)
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