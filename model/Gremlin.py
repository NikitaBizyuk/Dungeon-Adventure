import random
from model.Monster import Monster

class Gremlin(Monster):
    def __init__(self, name, hp, attack_speed, chance_to_hit,
                 damage_min, damage_max, chance_to_heal, heal_min, heal_max):
        super().__init__(name, damage_min, damage_max, attack_speed, hp,
                         chance_to_hit, chance_to_heal, heal_min, heal_max)

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            target.take_damage(damage)


    def get_heal_range(self):
        return self.heal_min, self.heal_max

    def __str__(self):
        return (
            f"{self.name} the Gremlin - "
            f"HP: {self.health_points}, "
            f"DMG: {self.damage_min}-{self.damage_max}, "
            f"Heal: {self.heal_min}-{self.heal_max}"
        )
