import random
from abc import ABC, abstractmethod

from model.dungeon_character import DungeonCharacter


class Hero(DungeonCharacter, ABC):
    def __init__(self, name, health_points, damage_min, damage_max, attack_speed, chance_to_hit):
        super().__init__(name, health_points, damage_min, damage_max, attack_speed, chance_to_hit)
        self._chance_to_block = 0.90
        self._healing_potions = 0
        self._vision_potions = 0
        self._pillars_found = 0


    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def special_skill(self, target):
        pass

    @property
    def chance_to_block(self):
        return self._chance_to_block

    @chance_to_block.setter
    def chance_to_block(self, value):
        self._chance_to_block = max(0.0, min(1.0, value))

    def reduce_block_chance_after_boss(self):
        self._chance_to_block = max(0.0, self._chance_to_block - 0.10)
        print(f"{self.name}'s block chance reduced to {round(self._chance_to_block * 100)}%.")

    def take_damage(self, amount):
        if random.random() < self._chance_to_block:
            print(f"{self.name} blocked the attack!")
        else:
            self.health_points -= amount
            print(f"{self.name} took {amount} damage. HP: {self.health_points}")



    @property
    def pillars_found(self):
        return self._pillars_found

    @pillars_found.setter
    def pillars_found(self, value):
        self._pillars_found = value

    def increment_pillars_found(self):
        self._pillars_found += 1
        self.reduce_block_chance_after_boss()
