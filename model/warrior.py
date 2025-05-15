import random

from model.hero import Hero


class Warrior(Hero):
    def __init__(self,name, damage_min, damage_max, attack_speed, chance_to_hit):
        super().__init__(name, damage_min, damage_max, attack_speed, chance_to_hit)
        self.__name = name
       ##self.__special_skill =
        self.__attack_speed = attack_speed
        self._damage_min = damage_min
        self.__damage_max = damage_max
        self._chance_to_hit = chance_to_hit


    def attack(self, target):
        if random.random() < self.get_chance_to_hit():
            damage = random.randint(self.get_damage_min(), self.get_damage_max())
            print(f"{self.get_name()} attacks for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s attack missed!")

    def use_skill(self, target):
        if random.random() < 0.4:
            damage = random.randint(75, 175)
            print(f"{self.get_name()} uses Crushing Blow for {damage} damage!")
            target.take_damage(damage)
        else:
            print(f"{self.get_name()}'s Crushing Blow missed!")

    def special_skill(self) -> None:
        print("PLACE SPECIAL SKILL HERE")
        pass

    def to_String(self) -> str:
        result = ((("Name: " + self._name +
                  "\nHP: " + str(self._health_points)) +
                  "\nAttack speed: " + str(self.__attack_speed) +
                  "\nDamage min: " + str(self._damage_min)) +
                  "\nDamage max: " + str(self.__damage_max) +
                  "\nChance to hit: " + str(self._chance_to_hit))
        return result
