from abc import ABC, abstractmethod


class DungeonCharacter(ABC):
    def __init__(self, name, health_points, damage_min, damage_max, attack_speed, chance_to_hit):
        self._name = name
        self._health_points = health_points
        self._damage_min = damage_min
        self._damage_max = damage_max
        self._attack_speed = attack_speed
        self._chance_to_hit = chance_to_hit

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def take_damage(self, amount):
        pass

    def is_alive(self):
        return self._health_points > 0

    @property
    def name(self):
        return self._name

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        self._health_points = max(0, value)

    @property
    def damage_min(self):
        return self._damage_min

    @property
    def damage_max(self):
        return self._damage_max

    @property
    def attack_speed(self):
        return self._attack_speed

    @property
    def chance_to_hit(self):
        return self._chance_to_hit

    def get_status(self):
        return f"{self.name}: {self.health_points} HP"