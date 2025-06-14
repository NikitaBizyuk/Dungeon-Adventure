import random
from abc import ABC, abstractmethod
from model.DungeonCharacter import DungeonCharacter


class Hero(DungeonCharacter, ABC):
    """
    Abstract base class for all heroes.
    Adds:
        • instant_death()  – used when the hero falls into a pit
    """

    # ─── Construction ────────────────────────────────────────────
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
        self._chance_to_block   = 0.90
        self._healing_potions   = 0
        self._vision_potions    = 0
        self._pillars_found     = 0

    # ─── Abstract combat interface ───────────────────────────────
    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def special_skill(self, target):
        pass

    @property
    def chance_to_block(self):
        return self._chance_to_block

    @chance_to_block.setter
    def chance_to_block(self, value):
        self._chance_to_block = max(0.0, min(1.0, value))

    def reduce_block_chance_after_boss(self):
        self._chance_to_block = max(0.0, self._chance_to_block - 0.10)
        print(f"{self.name}'s block chance reduced to {round(self._chance_to_block * 100)}%.")

    def take_damage(self, amount):
        if random.random() < self._chance_to_block:
            print(f"{self.name} blocked the attack!")
        else:
            self.health_points -= amount
            print(f"{self.name} took {amount} damage. HP: {self.health_points}")

    # ─── NEW: Instant death (used by pits) ───────────────────────
    def instant_death(self) -> None:
        """Sets HP to zero immediately."""
        self.health_points = 0
        print(f"{self.name} fell into a pit and died!")

    # ─── Projectile specs (abstract) ─────────────────────────────
    @property
    @abstractmethod
    def projectile_cooldown(self):
        """Time in ms between shots."""
        raise NotImplementedError("Each hero must define their projectile cooldown.")

    @property
    @abstractmethod
    def projectile_speed(self):
        """Pixels per frame."""
        raise NotImplementedError("Each hero must define their projectile speed.")

    @property
    @abstractmethod
    def projectile_damage(self):
        """Damage dealt per projectile."""
        raise NotImplementedError("Each hero must define their projectile damage.")

    @property
    def pillars_found(self):
        return self._pillars_found

    @pillars_found.setter
    def pillars_found(self, value):
        self._pillars_found = value

    def increment_pillars_found(self):
        self._pillars_found += 1
        self.reduce_block_chance_after_boss()
