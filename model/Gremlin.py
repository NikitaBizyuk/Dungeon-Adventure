import random
from model.Monster import Monster

class Gremlin(Monster):
    def __init__(self, name, hp, attack_speed, chance_to_hit,
                 damage_min, damage_max, chance_to_heal, heal_min, heal_max):
        super().__init__(name, damage_min, damage_max, attack_speed, hp, chance_to_hit, chance_to_heal)
        self._heal_min = heal_min
        self._heal_max = heal_max

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} scratches {target.name} for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name}'s attack missed!")

    def get_heal_range(self):
        return self._heal_min, self._heal_max

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f"{self.name} the Gremlin - HP: {self.health_points}, DMG: {self.damage_min}-{self.damage_max}, Heal: {self._heal_min}-{self._heal_max}"
