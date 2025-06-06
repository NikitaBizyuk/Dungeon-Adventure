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

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} strikes with her staff for {damage} damage.")
            target.take_damage(damage)
            # 25% chance to self-heal for 10–20 HP
            if random.random() < 0.25:
                heal = random.randint(10, 20)
                self.health_points += heal
                print(f"{self.name} heals herself for {heal} HP! New HP: {self.health_points}")
        else:
            print(f"{self.name}'s staff attack missed!")

## Priestess special skill goes here
    def special_skill(self, target):
        pass

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