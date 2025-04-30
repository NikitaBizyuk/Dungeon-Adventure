from abc import ABC, abstractmethod
from dungeon_character import DungeonCharacter

class Monster(ABC, DungeonCharacter):
    """
        Abstract base class representing a Monster character in
        the dungeon game.

        A Monster is a type of DungeonCharacter with unique
        healing abilities.
        This class is a blueprint for all monster types and
        cannot be instantiated directly.

        Attributes:
            _chance_to_heal (float): The probability (0.0 to 1.0)
            that the monster can heal itself during combat.

        Inherits:
            DungeonCharacter: Base class with core combat attributes
            such as name, health points, damage range, attack speed,
            and chance to hit.

        Args:
            name (str): The monster's name.
            health_points (int): The initial health value of the monster.
            damage_min (int): Minimum damage the monster can deal.
            damage_max (int): Maximum damage the monster can deal.
            attack_speed (int): Number of attacks per round.
            chance_to_hit (float): Probability (0.0 to 1.0) that the monster
            lands an attack.
            chance_to_heal (float): Probability (0.0 to 1.0) that the monster
            can heal itself.
        """
    def __init__(self, name,health_points, damage_min,
                 damage_max, attack_speed, chance_to_hit, chance_to_heal ) -> None:

        super().__init__(name, health_points, damage_min, damage_max,
                         attack_speed, chance_to_hit)
        self._chance_to_heal = chance_to_heal
