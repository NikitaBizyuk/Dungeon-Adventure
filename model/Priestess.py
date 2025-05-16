import random

from model.hero import Hero


class Priestess(Hero):
    def __init__(self,name):
        name = name
        health_points = 100
        chance_to_hit = 75
        attack_speed = 5
        damage_min = 25
        damage_max = 45
        super().__init__(name,health_points, damage_min, damage_max, attack_speed, chance_to_hit)

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name}'s attack missed!")

## Priestess special skill goes here
    def special_skill(self, target):
        pass


    def to_string(self) -> str:
        result = ((("Name: " + self._name +
                    "\nHP: " + str(self._health_points)) +
                   "\nAttack speed: " + str(self._attack_speed) +
                   "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self._damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result