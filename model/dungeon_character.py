from abc import ABC, abstractmethod

class DungeonCharacter(ABC):

    def __init__(self, name, health_points, damage_min,
                 damage_max, attack_speed, chance_to_hit) -> None:
        """
               Initialize the dungeon character with combat stats.

               Parameters:
                   name (str): Character's name.
                   health_points (int): Starting health.
                   damage_min (int): Minimum damage per attack.
                   damage_max (int): Maximum damage per attack.
                   attack_speed (int): Number of attacks per round.
                   chance_to_hit (float): Chance to successfully hit the opponent (0.0 to 1.0).
               """
        self.__name = name
        self.__health_points = health_points
        self.__damage_min = damage_min
        self.__damage_max = damage_max
        self.__attack_speed = attack_speed
        self.__chance_to_hit = chance_to_hit


    @abstractmethod
    def attack(self, target: "DungeonCharacter") -> None:
        """Perform an attack on the target character."""
        pass
    @abstractmethod
    def take_damage(self, the_amount: "int") -> None:
        """
                Apply damage to this character.

                Parameters:
                    the_amount (int): The amount of damage to subtract from health.
                """
        pass
    @abstractmethod
    def get_name(self) -> str:
        """Return the character's name."""
        pass
    @abstractmethod
    def get_health_points(self) -> int:
        """Return the current health points of the character."""
        pass
    @abstractmethod
    def get_damage_min(self) -> int:
        """Return the minimum possible damage this character can deal."""
        pass
    @abstractmethod
    def get_damage_max(self) -> int:
        """Return the maximum possible damage this character can deal."""
        pass
    @abstractmethod
    def get_attack_speed(self) -> int:
        """Return the character's attack speed (attacks per round)."""
        pass
    @abstractmethod
    def get_chance_to_hit(self) -> float:
        """Return the probability (0.0–1.0) that this character lands a hit."""
        pass
    @abstractmethod
    def set_health_points(self,the_points: "int") -> None:
        """
                Set the character's current health points.

                Parameters:
                    the_points (int): The new health value.
                """
        pass



