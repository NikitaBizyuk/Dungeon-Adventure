import pygame

class Projectile:
    def __init__(self, x, y, dx, dy, speed=10, damage=10):
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(dx, dy).normalize() * speed
        self.radius = 5
        self.damage = damage
        self.active = True

    def update(self):
        if not self.active:
            return
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, (255, 50, 50), (int(self.x), int(self.y)), self.radius)

    def get_position(self):
        return self.x, self.y

    def deactivate(self):
        self.active = False
