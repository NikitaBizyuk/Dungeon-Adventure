from abc import ABC, abstractmethod
from dungeon_character import DungeonCharacter


class Hero(ABC, DungeonCharacter):
    """
        Abstract base class representing a Hero character in the dungeon game.

        A Hero is a specialized type of DungeonCharacter with additional abilities
        such as blocking attacks and using a unique skill. This class serves as a
        blueprint for all specific hero types and cannot be instantiated directly.

        Attributes:
            _chance_to_block (float): The probability (0.0 to 1.0) that the hero can block an incoming attack.
            _skill (str): The name or description of the hero's unique skill or ability.

        Inherits:
            DungeonCharacter: Base class with core combat attributes such as name, health points, damage range,
                              attack speed, and chance to hit.

        Args:
            name (str): The hero's name.
            health_points (int): The initial health value of the hero.
            damage_min (int): Minimum damage the hero can deal.
            damage_max (int): Maximum damage the hero can deal.
            attack_speed (int): Number of attacks per round.
            chance_to_hit (float): Probability (0.0 to 1.0) that the hero lands an attack.
            chance_to_block (float): Probability (0.0 to 1.0) that the hero blocks an attack.
            skill (str): Description of the hero’s special ability.
        """
    def __init__(self,name, health_points, damage_min,
                 damage_max, attack_speed, chance_to_hit, chance_to_block, skill) -> None:
        super().__init__(name,health_points, damage_min, damage_max, attack_speed, chance_to_hit)
        self._chance_to_block = chance_to_block
        self._skill = skill

