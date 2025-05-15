import random

from model.monster import Monster


class Ogre(Monster):

    def __init__(self,name, damage_min, damage_max, attack_speed,hit_chance,heal_points):
        super().__init__(name, damage_min, damage_max, attack_speed,hit_chance,heal_points)

    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(" Ogre slams for" + str(damage) + " damage.")
            target.take_damage(damage)
        else:
            print("Ogre's slam missed!")


    def get_name(self):
        return self._name

    def get_chance_to_hit(self):
        return self._chance_to_hit

    def get_damage_min(self):
        return self._damage_min

    def get_damage_max(self):
        return self._damage_max


    def to_String(self) -> str:
        result = ((("Name: " + self._name +
                    "\nHP: " + str(self._health_points)) +
                   "\nAttack speed: " + str(self._attack_speed) +
                   "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self._damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result
