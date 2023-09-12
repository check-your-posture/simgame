class Entity:
    def __init__(self, shape):
        self.shape = shape

    def draw(self, screen):
        self.shape.draw(screen)

    def move(self, dx, dy, checkCollision):
        # The decision to require a collision checking lambda to be passed in all the way down into the Entity class (here) is to ensure that collision checking is ALWAYS ran whenever the entity moves.
        # In other words, you can't actually call this function WITHOUT doing collision checking. That way we don't ever accidentally write code that moves an entity without checking for collisions.
        # If we TRULY want the entity to move without collision, we will need to go through the trouble of writing a lambda that always returns False, and then passing it into this Entity move() function.
        #
        # TODO: One bug I'm seeing is that, if an entity is moving diagonally (two direction at the same time) and collides with another entity, it will stop moving in BOTH directions.
        #       This seems kind of undesirable, maybe...?
        doesCollisionOccur = checkCollision(self, dx, dy)
        if(doesCollisionOccur == False): # If there is no collision, let the entity move
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
