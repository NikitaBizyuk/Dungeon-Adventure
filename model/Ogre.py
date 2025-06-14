import random
from model.Monster import Monster

class Ogre(Monster):
    def __init__(self, name, hp, attack_speed, chance_to_hit,
                 damage_min, damage_max, chance_to_heal, heal_min, heal_max):
        super().__init__(name, damage_min, damage_max, attack_speed, hp,
                         chance_to_hit, chance_to_heal, heal_min, heal_max)

    def attack(self, target):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} slams for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name}'s slam missed!")

    def get_heal_range(self):
        return (self.heal_min, self.heal_max)

    def __str__(self):
        return (
            f"Monster: {self.name}\n"
            f"HP: {self.health_points}\n"
            f"Attack Speed: {self.attack_speed}\n"
            f"Chance to Hit: {self.chance_to_hit}\n"
            f"Damage: {self.damage_min}-{self.damage_max}\n"
            f"Chance to Heal: {self.chance_to_heal}\n"
            f"Heal Amount: {self.heal_min}-{self.heal_max}"
        )
