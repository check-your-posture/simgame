class Entity:
    def __init__(self, shape):
        self.shape = shape

    def draw(self, screen):
        self.shape.draw(screen)

    def move(self, dx, dy):
        self.shape.move_ip(dx, dy)

    # Check if a point is within the Entity
    def contains_point(self, point):
        return self.shape.collidepoint(point)

class Obstacle(Entity):
    # Obstacle inherits from Entity, so we just pass all the arguments to the Entity constructor
    def __init__(self, shape):
        super().__init__(shape)

class NPC(Entity):
    # NPC inherits from Entity, so we just pass all the arguments to the Entity constructor
    def __init__(self, shape):
        super().__init__(shape)
