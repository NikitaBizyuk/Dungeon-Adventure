import random

from model.dungeon_character import DungeonCharacter


class Monster(DungeonCharacter):
    """
    Abstract class for monsters. Adds chance-based healing behavior.
    """

    def __init__(self, name, hp, dmg_min, dmg_max, speed, hit_chance, heal_chance):
        super().__init__(name, hp, dmg_min, dmg_max, speed, hit_chance)
        self._chance_to_heal = heal_chance

    def get_chance_to_heal(self):
        return self._chance_to_heal

    def heal(self, min_heal, max_heal):
        """Applies healing if chance succeeds."""
        if self.get_hit_points() > 0 and random.random() < self._chance_to_heal:
            heal_amount = random.randint(min_heal, max_heal)
            self.set_health_points(self.get_hit_points() + heal_amount)
            print(f"{self.get_name()} healed for {heal_amount} HP!")