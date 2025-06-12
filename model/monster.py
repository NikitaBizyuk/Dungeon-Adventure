import random
from abc import ABC
from model.dungeon_character import DungeonCharacter
import pygame

class Monster(DungeonCharacter, ABC):
    def __init__(self, name, damage_min, damage_max, attack_speed,
                 health_points, chance_to_hit, chance_to_heal=0.2,
                 heal_min=0, heal_max=0):
        super().__init__(name, health_points, damage_min, damage_max, attack_speed, chance_to_hit)
        self._chance_to_heal = chance_to_heal
        self._heal_min = heal_min
        self._heal_max = heal_max
        self._last_hit_time = -1000

    def set_health_points(self, num):
        self._health_points = max(0, num)

    def take_damage(self, amount):
        self.set_health_points(self.health_points - amount)
        print(f"{self.name} took {amount} damage.")
        self.flash_hit()
        self.heal()

    def flash_hit(self):
        self._last_hit_time = pygame.time.get_ticks()

    def is_flashing(self):
        return pygame.time.get_ticks() - self._last_hit_time < 200

    def heal(self):
        if self.is_alive() and random.random() < self._chance_to_heal:
            heal_amount = random.randint(self._heal_min, self._heal_max)
            self.set_health_points(self.health_points + heal_amount)
            print(f"{self.name} healed for {heal_amount} HP!")

    def get_heal_points(self):
        return self._chance_to_heal

    def attack_hero(self, hero):
        if random.random() < self._chance_to_hit:
            damage = random.randint(self._damage_min, self._damage_max)
            print(f"{self.name} attacks {hero.name} for {damage} damage.")
            hero.take_damage(damage)
        else:
            print(f"{self.name}'s attack missed!")
