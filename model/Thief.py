import random
import math
from model.AnimatedHero import AnimatedHero

class Thief(AnimatedHero):
    def __init__(self, name):
        super().__init__(name, health_points=125, damage_min=20, damage_max=40,
                         attack_speed=6, chance_to_hit=0.8, sprite_folder="reaper_man_2")

    def attack(self, target, damage=None):
        self.start_attack()
        if damage is not None:
            print(f"{self.name} hurls a throwing knife for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name} performs a quick dual stab!")
            for i in range(2):
                if random.random() < self.chance_to_hit:
                    dmg = random.randint(self.damage_min, self.damage_max)
                    print(f"  Hit {i + 1}: {dmg} damage.")
                    target.take_damage(dmg)
                else:
                    print(f"  Hit {i + 1}: missed!")
        self.end_attack()

    def special_skill(self, target):
        roll = random.random()
        if roll < 0.4:
            print(f"{self.name} performs a surprise double strike!")
            self.attack(target)
            self.attack(target)
        elif roll < 0.6:
            print(f"{self.name}'s surprise attack failed!")
        else:
            print(f"{self.name} performs a surprise attack.")
            self.attack(target)

    @property
    def projectile_cooldown(self): return 300

    @property
    def projectile_speed(self): return 12

    @property
    def projectile_damage(self): return 10

    @property
    def weapon_type(self): return "dagger"

    def get_melee_style(self):
        return {"color": (0, 255, 0), "arc_width": math.pi / 10, "reach": 35, "swings": 2}


    def to_string(self):
        return (
            f"Name: {self.name}\n"
            f"HP: {self.health_points}\n"
            f"Attack Speed: {self.attack_speed}\n"
            f"Damage: {self.damage_min} - {self.damage_max}\n"
            f"Chance to Hit: {self.chance_to_hit}\n"
            f"Chance to Block: {round(self.chance_to_block * 100)}%\n"
            f"Pillars Found: {self.pillars_found}"
        )
