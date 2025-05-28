import random

from model.monster import Monster


class Ogre(Monster):

    def __init__(self,name = "OGREBOGRE"):
        damage_min = 30
        damage_max = 60
        attack_speed = 2
        hit_points = 200
        heal_points = 60
        chance_to_hit = 10
        super().__init__(name, damage_min, damage_max, attack_speed,hit_points,heal_points)

    def attack(self, target):
        if random.random() < self.chance_to_hit():
            damage = random.randint(self.damage_min(), self.get_damage_max())
            print(" Ogre slams for" + str(damage) + " damage.")
            target.take_damage(damage)
        else:
            print("Ogre's slam missed!")

    @property
    def name(self):
        return self._name
    @property
    def chance_to_hit(self):
        return self._chance_to_hit
    @property
    def damage_min(self):
        return self._damage_min
    @property
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
