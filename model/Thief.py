import random

from model.hero import Hero


class Thief(Hero):
    def __init__(self, name):
        health_points = 125
        damage_min = 35
        damage_max = 60
        attack_speed = 4
        chance_to_hit = 0.8
        super().__init__(name, health_points, damage_min, damage_max, attack_speed, chance_to_hit)


    def attack(self, target):
        if random.random() < self.chance_to_hit():
            damage = random.randint(self.damage_min(), self.damage_max())
            print(f"{self.name()} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name()}'s attack missed!")

    def special_skill(self, target):
        if random.random() < 0.4:
            damage = random.randint(75, 175)
            print(f"{self.name()} uses Crushing Blow for {damage} damage!")
            target.take_damage(damage)
        else:
            print(f"{self.name()}'s Crushing Blow missed!")

    def to_string(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"HP: {self.health_points}\n"
            f"Attack Speed: {self.attack_speed}\n"
            f"Damage: {self.damage_min} - {self.damage_max}\n"
            f"Chance to Hit: {self.chance_to_hit}\n"
            f"Chance to Block: {round(self.chance_to_block * 100)}%\n"
            f"Pillars Found: {self.pillars_found}"
        )