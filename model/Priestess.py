import random
import math
from model.Hero import Hero

class Priestess(Hero):
    def __init__(self, name):
        super().__init__(name, health_points=100, damage_min=25, damage_max=45,
                         attack_speed=5, chance_to_hit=0.75)

    def attack(self, target, damage=None):
        if damage is not None:
            print(f"{self.name} fires a sacred blast for {damage} damage.")
            target.take_damage(damage)
        else:
            if random.random() < self.chance_to_hit:
                dmg = random.randint(self.damage_min, self.damage_max)
                print(f"{self.name} strikes with her staff for {dmg} damage.")
                target.take_damage(dmg)
            else:
                print(f"{self.name}'s staff attack missed!")

    def special_skill(self, target):
        if self.health_points >= self.max_health_points:
            print(f"{self.name} is already at full health!")
            return
        heal_amount = random.randint(20, 35)
        actual_heal = min(heal_amount, self.max_health_points - self.health_points)
        self.health_points += actual_heal
        print(f"{self.name} uses Divine Grace and heals for {actual_heal} HP. New HP: {self.health_points}")

    @property
    def projectile_cooldown(self):
        return 600

    @property
    def projectile_speed(self):
        return 10

    @property
    def projectile_damage(self):
        return 20

    def get_melee_style(self):
        return {
            "color": (160, 32, 240),
            "arc_width": math.pi / 6,
            "reach": 40,
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
