import random

from model.hero import Hero


class Warrior(Hero):
    def __init__(self, name):
        # sets default Warrior stats
        super().__init__(name, 125, 35, 60, 4, 0.8, 0.2, "Crushing Blow")

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            dmg = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} attacks for {dmg} damage.")
            target.take_damage(dmg)
        else:
            print(f"{self.get_name()}'s attack missed.")

    def use_skill(self, target):
        if random.random() < 0.4:
            dmg = random.randint(75, 175)
            print(f"{self.get_name()} uses Crushing Blow for {dmg} damage!")
            target.take_damage(dmg)
        else:
            print(f"{self.get_name()}'s Crushing Blow missed!")