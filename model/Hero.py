import random
from abc import ABC, abstractmethod
from model.DungeonCharacter import DungeonCharacter


class Hero(DungeonCharacter, ABC):
    """
    Abstract base class for all heroes.
    Includes shared combat and inventory behavior.
    """

    def __init__(
        self,
        name: str,
        health_points: int,
        damage_min: int,
        damage_max: int,
        attack_speed: int,
        chance_to_hit: float
    ):
        super().__init__(
            name,
            health_points,
            damage_min,
            damage_max,
            attack_speed,
            chance_to_hit
        )
        self._max_health_points = health_points
        self._chance_to_block = 0.90
        self._healing_potions = 0
        self._vision_potions = 0
        self._pillars_found = 0

    # ─── Abstract Methods ──────────────────────────────────────

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def special_skill(self, target):
        pass

    @property
    @abstractmethod
    def projectile_cooldown(self):
        """Time in ms between shots."""
        pass

    @property
    @abstractmethod
    def projectile_speed(self):
        """Pixels per frame."""
        pass

    @property
    @abstractmethod
    def projectile_damage(self):
        """Damage dealt per projectile."""
        pass

    # ─── Properties ────────────────────────────────────────────

    @property
    def max_health_points(self):
        return self._max_health_points

    @property
    def chance_to_block(self):
        return self._chance_to_block

    @chance_to_block.setter
    def chance_to_block(self, value):
        self._chance_to_block = max(0.0, min(1.0, value))

    @property
    def pillars_found(self):
        return self._pillars_found

    @pillars_found.setter
    def pillars_found(self, value):
        self._pillars_found = value

    # ─── Behavior Methods ──────────────────────────────────────

    def take_damage(self, amount):
        if random.random() < self._chance_to_block:
            print(f"{self.name} blocked the attack!")
        else:
            self.health_points -= amount
            print(f"{self.name} took {amount} damage! Remaining HP: {self.health_points}")

    def instant_death(self):
        """Sets health to 0 immediately (e.g., pit death)."""
        self.health_points = 0

    def increment_pillars_found(self):
        self._pillars_found += 1
        self.reduce_block_chance_after_boss()

    def reduce_block_chance_after_boss(self):
        self._chance_to_block = max(0.0, self._chance_to_block - 0.10)
