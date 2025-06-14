import random
import math
from model.Hero import Hero

class Warrior(Hero):
    def __init__(self, name):
        super().__init__(name, health_points=125, damage_min=35, damage_max=60,
                         attack_speed=4, chance_to_hit=0.8)

    def attack(self, target, damage=None):
        if damage is not None:
            print(f"{self.name} hurls a heavy axe for {damage} damage!")
            target.take_damage(damage)
        else:
            if random.random() < self.chance_to_hit:
                dmg = random.randint(self.damage_min, self.damage_max)
                print(f"{self.name} slashes for {dmg} damage.")
                target.take_damage(dmg)
            else:
                print(f"{self.name}'s sword attack missed!")

    def special_skill(self, target):
        print(f"{self.name} attempts a Crushing Blow!")
        if random.random() < 0.4:
            damage = random.randint(75, 175)
            print(f"💪 Crushing Blow lands for {damage} damage!")
            target.take_damage(damage)
        else:
            print("❌ Crushing Blow missed!")

    @property
    def projectile_cooldown(self):
        return 800

    @property
    def projectile_speed(self):
        return 8

    @property
    def projectile_damage(self):
        return 25

    def get_melee_style(self):
        return {
            "color": (255, 0, 0),
            "arc_width": math.pi / 4,
            "reach": 50,
            "swings": 1
        }

    def to_string(self):
        return (
            f"Name: {self.name}\n"
            f"HP: {self.health_points}\n"
            f"Attack Speed: {self.attack_speed}\n"
            f"Damage: {self.damage_min} - {self.damage_max}\n"
            f"Chance to Hit: {self.chance_to_hit}\n"
            f"Chance to Block: {round(self.chance_to_block * 100)}%\n"
            f"Pillars Found: {self.pillars_found}"
        )
