import random

from model.hero import Hero


class Thief(Hero):
    def __init__(self,name, damage_min, damage_max, attack_speed, chance_to_hit):
        super().__init__(name, damage_min, damage_max, attack_speed, chance_to_hit)

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s attack missed!")

#Thief special skill goes here
    def use_skill(self, target):
        pass


    def to_String(self) -> str:
        result = ((("Name: " + self._name +
                    "\nHP: " + str(self._health_points)) +
                   "\nAttack speed: " + str(self._attack_speed) +
                   "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self._damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result