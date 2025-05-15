import random
from abc import ABC, abstractmethod

from model.dungeon_character import DungeonCharacter


class Hero(DungeonCharacter, ABC):
    def __init__(self, name,damage_min, damage_max, attack_speed, chance_to_hit):
        super().__init__(name, damage_min, damage_max, attack_speed, chance_to_hit)
        self._chance_to_block = 0
        self._hp = 100




    def get_chance_to_block(self) -> float:
        self._chance_to_block = random.uniform(0.85,1.0)
        return self._chance_to_block

    def set_chance_to_block(self, chance_to_block, num) -> None:
        self._chance_to_block = chance_to_block + num


    def take_damage(self, amount) -> None:
        if random.random() < self._chance_to_block:
            print(f"{self.get_name()} blocked the attack!")
        else:
            self.set_health_points(self.get_hit_points() - amount)
            print(f"{self.get_name()} took {amount} damage.")

