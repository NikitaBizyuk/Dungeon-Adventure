import random

from model.hero import Hero
import math

class Priestess(Hero):
    def __init__(self,name):

        health_points = 100
        chance_to_hit = 75
        attack_speed = 5
        damage_min = 25
        damage_max = 45
        super().__init__(name,health_points, damage_min, damage_max, attack_speed, chance_to_hit)

    def attack(self, target, damage=None):
        if damage is not None:
            # Projectile logic: guaranteed hit
            print(f"{self.name} fires a sacred blast for {damage} damage.")
            target.take_damage(damage)
        else:
            # Melee logic with hit chance and healing
            if random.random() < self.chance_to_hit:
                damage = random.randint(self.damage_min, self.damage_max)
                print(f"{self.name} strikes with her staff for {damage} damage.")
                target.take_damage(damage)

                # Only heal if not at max HP, and with lower probability
                if self.health_points < 100 and random.random() < 0.1:  # 10% chance
                    heal = random.randint(8, 16)
                    self.health_points = min(self.health_points + heal, 100)
                    print(f"{self.name} heals herself for {heal} HP! New HP: {self.health_points}")
            else:
                print(f"{self.name}'s staff attack missed!")

    ## Priestess special skill goes here
    def special_skill(self, target):
        pass

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