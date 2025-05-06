import random

from model.hero import Hero


class Priestess(Hero):
    def __init__(self, name):
        super().__init__(name, 75, 25, 45, 5, 0.7, 0.3, "Heal")

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s attack missed!")

    def use_skill(self, target=None):
        heal_amount = random.randint(25, 40)
        self.set_health_points(self.get_hit_points() + heal_amount)
        print(f"{self.get_name()} healed herself for {heal_amount} HP.")