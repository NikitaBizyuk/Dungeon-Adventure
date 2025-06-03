import random

from model.monster import Monster


class Gremlin(Monster):
    def __init__(self, name="GARGOYLEMLIN"):
        damage_min = 15
        damage_max = 30
        attack_speed = 5
        health_points = 120
        chance_to_hit = 0.4
        chance_to_heal = 0.3
        super().__init__(name, damage_min, damage_max, attack_speed, health_points, chance_to_hit, chance_to_heal)

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} scratches for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name}'s attack missed!")


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
    def damage_max(self):
        return self._damage_max


    def to_String(self) -> str:
        result = ((("Name: " + self._name +
                    "\nHP: " + str(self._health_points)) +
                   "\nAttack speed: " + str(self._attack_speed) +
                   "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self._damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result