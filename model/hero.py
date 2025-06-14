import random
from abc import ABC, abstractmethod
from model.dungeon_character import DungeonCharacter


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
        """Regular attack; concrete subclasses implement."""
        pass

    @abstractmethod
    def special_skill(self, target):
        """Special ability unique to each hero."""
        pass

    # ─── Chance-to-block handling ────────────────────────────────
    @property
    def chance_to_block(self) -> float:
        return self._chance_to_block

    @chance_to_block.setter
    def chance_to_block(self, value: float) -> None:
        self._chance_to_block = max(0.0, min(1.0, value))

    def reduce_block_chance_after_boss(self) -> None:
        """Called each time a pillar is found to make later fights tougher."""
        self._chance_to_block = max(0.0, self._chance_to_block - 0.10)
        print(
            f"{self.name}'s block chance reduced to "
            f"{round(self._chance_to_block * 100)}%."
        )

    # ─── Damage intake ───────────────────────────────────────────
    def take_damage(self, amount: int) -> None:
        if random.random() < self._chance_to_block:
            print(f"{self.name} blocked the attack!")
        else:
            self.health_points -= amount
            print(
                f"{self.name} took {amount} damage. "
                f"HP: {self.health_points}"
            )

    # ─── NEW: Instant death (used by pits) ───────────────────────
    def instant_death(self) -> None:
        """Sets HP to zero immediately."""
        self.health_points = 0
        print(f"{self.name} fell into a pit and died!")

    # ─── Projectile specs (abstract) ─────────────────────────────
    @property
    @abstractmethod
    def projectile_cooldown(self) -> int:
        """Milliseconds between projectile shots."""
        raise NotImplementedError

    @property
    @abstractmethod
    def projectile_speed(self) -> float:
        """Pixels per frame for projectiles."""
        raise NotImplementedError

    @property
    @abstractmethod
    def projectile_damage(self) -> int:
        """Damage dealt per projectile."""
        raise NotImplementedError

    # ─── Pillar tracking ─────────────────────────────────────────
    @property
    def pillars_found(self) -> int:
        return self._pillars_found

    @pillars_found.setter
    def pillars_found(self, value: int) -> None:
        self._pillars_found = value

    def increment_pillars_found(self) -> None:
        self._pillars_found += 1
        self.reduce_block_chance_after_boss()

    # ─── Potion inventory helpers (optional) ─────────────────────
    @property
    def healing_potions(self) -> int:
        return self._healing_potions

    @healing_potions.setter
    def healing_potions(self, value: int) -> None:
        self._healing_potions = max(0, value)

    @property
    def vision_potions(self) -> int:
        return self._vision_potions

    @vision_potions.setter
    def vision_potions(self, value: int) -> None:
        self._vision_potions = max(0, value)