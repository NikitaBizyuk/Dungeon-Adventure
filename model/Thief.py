import random

from model.hero import Hero


class Thief(Hero):
    def __init__(self,name):
        health_points = 125
        damage_min = 20
        damage_max = 40
        attack_speed = 6
        chance_to_hit = 0.8
        super().__init__(name,health_points, damage_min, damage_max, attack_speed, chance_to_hit)

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min(), self.damage_max())
            print(f"{self.name()} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name()}'s attack missed!")

#Thief special skill goes here
    def special_skill(self, target):
        pass


    def to_String(self) -> str:
        result = ((("Name: " + self._name +
                    "\nHP: " + str(self._health_points)) +
                   "\nAttack speed: " + str(self._attack_speed) +
                   "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self._damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result