import random

from model.Hero import Hero
import math

class Priestess(Hero):
    def __init__(self,name):

        health_points = 100
        chance_to_hit = 75
        attack_speed = 5
        damage_min = 25
        damage_max = 45
        super().__init__(name,health_points, damage_min, damage_max, attack_speed, chance_to_hit)
        self._max_health_points = health_points

    def attack(self, target, damage=None):
        if damage is not None:
            # Projectile logic: guaranteed hit
            print(f"{self.name} fires a sacred blast for {damage} damage.")
            target.take_damage(damage)
        else:
            # Melee logic with hit chance only
            if random.random() < self.chance_to_hit:
                damage = random.randint(self.damage_min, self.damage_max)
                print(f"{self.name} strikes with her staff for {damage} damage.")
                target.take_damage(damage)
            else:
                print(f"{self.name}'s staff attack missed!")

    def special_skill(self, target):
        if self.health_points >= self._max_health_points:
            print(f"{self.name} is already at full health!")
            return

        heal_amount = random.randint(20, 35)
        actual_heal = min(heal_amount, self._max_health_points - self.health_points)
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
            "color": (160, 32, 240),  # Purple
            "arc_width": math.pi / 6,
            "reach": 40,
            "swings": 1
        }

    def to_string(self) -> str:
        result = ((("Name: " + self._name +
                    "\nHP: " + str(self._health_points)) +
                   "\nAttack speed: " + str(self._attack_speed) +
                   "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self._damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result