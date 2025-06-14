import pygame


class Projectile:
    def __init__(self, x, y, dx, dy, speed=10, damage=10):
        self._x = x
        self._y = y
        self._velocity = pygame.math.Vector2(dx, dy).normalize() * speed
        self._radius = 5
        self._damage = damage
        self._active = True

    def update(self):
        if not self._active:
            return
        self._x += self._velocity.x
        self._y += self._velocity.y

    def draw(self, surface):
        if self._active:
            pygame.draw.circle(surface, (255, 50, 50), (int(self._x), int(self._y)), self._radius)

    def deactivate(self):
        self._active = False

    # ────── Properties ──────

    @property
    def position(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def velocity(self):
        return self._velocity

    @property
    def radius(self):
        return self._radius

    @property
    def damage(self):
        return self._damage

    @property
    def active(self):
        return self._active
