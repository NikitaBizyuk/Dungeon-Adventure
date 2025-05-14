import random

from model.monster import Monster


class Skeleton(Monster):
    def __init__(self, name="Skeleton"):
        super().__init__(name, 100, 30, 50, 3, 0.8, 0.3)

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} slashes for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s slash missed!")