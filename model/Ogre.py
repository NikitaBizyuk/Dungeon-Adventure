import random
from model.monster import Monster

class Ogre(Monster):
    def __init__(self, name, hp, attack_speed, chance_to_hit,
                 damage_min, damage_max, chance_to_heal, heal_min, heal_max):
        super().__init__(name, damage_min, damage_max, attack_speed, hp, chance_to_hit, chance_to_heal)
        self._heal_min = heal_min
        self._heal_max = heal_max

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} slams for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name}'s slam missed!")

    def get_heal_range(self):
        return (self._heal_min, self._heal_max)

    @property
    def name(self):
        return self._name

    def __str__(self):
        return (
            f"Monster: {self._name}\n"
            f"HP: {self._health_points}\n"
            f"Attack Speed: {self._attack_speed}\n"
            f"Chance to Hit: {self._chance_to_hit}\n"
            f"Damage: {self._damage_min}-{self._damage_max}\n"
            f"Chance to Heal: {self._chance_to_heal}\n"
            f"Heal Amount: {self._heal_min}-{self._heal_max}"
        )
