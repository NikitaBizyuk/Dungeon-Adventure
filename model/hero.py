import random
from abc import abstractmethod

from model.dungeon_character import DungeonCharacter


class Hero(DungeonCharacter):
    """
    Abstract class for heroes. Adds block chance and skill system.
    """

    def __init__(self, name, hp, dmg_min, dmg_max, speed, hit_chance, block_chance, skill_name):
        super().__init__(name, hp, dmg_min, dmg_max, speed, hit_chance)
        self._chance_to_block = block_chance
        self._skill = skill_name

    def get_chance_to_block(self):
        return self._chance_to_block

    def get_skill(self):
        return self._skill

    def take_damage(self, amount):
        """Overrides to allow blocking damage."""
        if random.random() < self._chance_to_block:
            print(f"{self.get_name()} blocked the attack!")
        else:
            self.set_health_points(self.get_hit_points() - amount)
            print(f"{self.get_name()} took {amount} damage.")

    @abstractmethod
    def use_skill(self, target):
        """Each hero must define how their skill works."""
        pass