import random
from abc import ABC

from model.dungeon_character import DungeonCharacter


class Monster(DungeonCharacter, ABC):
    def __init__(self, name, damage_min, damage_max, speed, heal_points ,chance_to_hit):
        super().__init__(name, damage_min, damage_max, speed,heal_points, chance_to_hit)
        self._chance_to_heal = heal_points

    def set_health_points(self,num):
        self._health_points = self._health_points + num

    def take_damage(self, amount):
        self.set_health_points(self.get_hit_points() - amount)
        print("Monster took" + str(amount)+ " damage.")
        self.heal()

    def heal(self):
        if self.is_alive() and random.random() < self._chance_to_heal:
            min_heal, max_heal = 20, 40
            heal_amount = random.randint(min_heal, max_heal)
            self.set_health_points(self.get_hit_points() + heal_amount)
            print("monster healed for" + str(heal_amount) +" HP!")
    def get_heal_points(self):
        return self._chance_to_heal