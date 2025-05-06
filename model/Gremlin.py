import random

from model.monster import Monster


class Gremlin(Monster):
    def __init__(self, name="Gremlin"):
        super().__init__(name, 70, 15, 30, 5, 0.8, 0.4)

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} scratches for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s attack missed!")