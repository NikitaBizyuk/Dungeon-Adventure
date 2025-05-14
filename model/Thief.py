import random

from model.hero import Hero


class Thief(Hero):
    def __init__(self, name):
        super().__init__(name, 75, 20, 40, 6, 0.8, 0.4, "Surprise Attack")

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s attack missed!")

    def use_skill(self, target):
        roll = random.random()
        if roll < 0.4:
            print(f"{self.get_name()} performs a surprise double attack!")
            self.attack(target)
            self.attack(target)
        elif roll < 0.6:
            print(f"{self.get_name()} was caught and failed to attack!")
        else:
            print(f"{self.get_name()} performs a normal attack.")
            self.attack(target)