import random
from abc import ABC
import pygame
from model.DungeonCharacter import DungeonCharacter


class Monster(DungeonCharacter, ABC):
    def __init__(self, name, damage_min, damage_max, attack_speed,
                 health_points, chance_to_hit, chance_to_heal=0.2,
                 heal_min=0, heal_max=0):
        super().__init__(name, health_points, damage_min, damage_max, attack_speed, chance_to_hit)
        self._chance_to_heal = chance_to_heal
        self._heal_min = heal_min
        self._heal_max = heal_max
        self._last_hit_time = -1000  # for flashing effect
        self._last_position = None
        self._current_position = None
        self._attacking = False
        self._animations = {}  # ✅ prevents unresolved reference warning
        self._last_animation_change = 0
        self._animation_lock_duration = 300
        self._last_attack_time = 0

    def take_damage(self, amount):
        self.health_points -= amount
        print(f"{self.name} took {amount} damage.")
        self.flash_hit()

        if hasattr(self, "animations") and "hurt" in self._animations:
            self.current_animation = "hurt"
            self._last_animation_change = pygame.time.get_ticks()

        self.heal()

        if self.health_points <= 0:
            if hasattr(self, "animations") and "dying" in self._animations:
                self.current_animation = "dying"
                self._last_animation_change = pygame.time.get_ticks()

    def flash_hit(self):
        """Triggers a flash timer used for visual feedback."""
        self._last_hit_time = pygame.time.get_ticks()

    def can_attack(self):
        now = pygame.time.get_ticks()
        return now - self._last_attack_time >= (1000 / self.attack_speed)

    def is_flashing(self):
        """Returns True if the monster should currently be flashing."""
        return pygame.time.get_ticks() - self._last_hit_time < 200

    def heal(self):
        """Heals the monster if chance condition is met."""
        if self.is_alive() and random.random() < self._chance_to_heal:
            heal_amount = random.randint(self._heal_min, self._heal_max)
            self.health_points += heal_amount
            print(f"{self.name} healed for {heal_amount} HP!")

    def attack_hero(self, hero):
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} attacks {hero.name} for {damage} damage.")
            hero.take_damage(damage)
        else:
            pass

    def set_position(self, row, col):
        self._last_position = self._current_position
        self._current_position = (row, col)

    def is_moving(self):
        return self._last_position is not None and self._current_position != self._last_position

    def start_attack(self):
        self._attacking = True

    def end_attack(self):
        self._attacking = False

    def is_attacking(self):
        return self._attacking



    # ─── Properties ─────────────────────────────────────────────

    @property
    def chance_to_heal(self):
        return self._chance_to_heal

    @chance_to_heal.setter
    def chance_to_heal(self, value):
        self._chance_to_heal = value

    @property
    def heal_min(self):
        return self._heal_min

    @heal_min.setter
    def heal_min(self, value):
        self._heal_min = value

    @property
    def heal_max(self):
        return self._heal_max

    @heal_max.setter
    def heal_max(self, value):
        self._heal_max = value
