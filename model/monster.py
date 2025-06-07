import random
from abc import ABC
from model.dungeon_character import DungeonCharacter
import pygame

class Monster(DungeonCharacter, ABC):
    def __init__(self, name, damage_min, damage_max, attack_speed, health_points, chance_to_hit, chance_to_heal=0.2):
        super().__init__(name, health_points, damage_min, damage_max, attack_speed, chance_to_hit)
        self._chance_to_heal = chance_to_heal
        self._last_hit_time = -1000

    def set_health_points(self, num):
        self._health_points = max(0, num)


    def take_damage(self, amount):
        self.set_health_points(self.health_points - amount)
        print(f"Monster took {amount} damage.")
        self.heal()

    def flash_hit(self):
        self._last_hit_time = pygame.time.get_ticks()

    def is_flashing(self):
        return pygame.time.get_ticks() - self._last_hit_time < 200

    def heal(self):
        if self.is_alive() and random.random() < self._chance_to_heal:
            heal_amount = random.randint(0, 10)
            self.set_health_points(self.health_points + heal_amount)
            print(f"Monster healed for {heal_amount} HP!")

    def get_heal_points(self):
        return self._chance_to_heal

    def attack_hero(self, hero):
        if random.random() < self._chance_to_hit:
            damage = random.randint(self._damage_min, self._damage_max)
            print(f"{self._name} attacks {hero.name} for {damage} damage.")
            hero.take_damage(damage)
        else:
            print(f"{self._name}'s attack missed!")
