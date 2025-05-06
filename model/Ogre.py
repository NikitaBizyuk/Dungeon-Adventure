import random

from model.monster import Monster


class Ogre(Monster):
    def __init__(self, name="Ogre"):
        super().__init__(name, 200, 30, 60, 2, 0.6, 0.1)

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            dmg = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} slams for {dmg} damage.")
            target.take_damage(dmg)
        else:
            print(f"{self.get_name()}'s slam missed.")