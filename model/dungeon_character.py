from abc import ABC, abstractmethod
import random

class DungeonCharacter(ABC):
    def __init__(self, name, damage_min, damage_max, attack_speed, chance_to_hit):
        self._name = name
        self._health_points = 100
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

    def get_name(self):
        return self._name

    def get_hit_points(self):
        return self._health_points

    def get_damage_min(self):
        return self._damage_min

    def get_damage_max(self):
        return self._damage_max

    def get_attack_speed(self):
        return self._attack_speed

    def get_chance_to_hit(self):
        return self._chance_to_hit

    def set_health_points(self, hp):
        self._health_points = max(0, hp)

    def get_status(self):
        return f"{self._name}: {self._health_points} HP"