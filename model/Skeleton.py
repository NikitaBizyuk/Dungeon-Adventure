import random
import pygame
from model.AnimatedMonster import AnimatedMonster
import os
from view.sprite_animator import SpriteAnimator

class Skeleton(AnimatedMonster):
    _cached_animations = None

    def __init__(self, name, hp, attack_speed, chance_to_hit,
                 damage_min, damage_max, chance_to_heal, heal_min, heal_max):
        if Skeleton._cached_animations is None:
            base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "skeleton_warrior_1")
            Skeleton._cached_animations = {
                "idle": SpriteAnimator(os.path.join(base_path, "idle")),
                "running": SpriteAnimator(os.path.join(base_path, "running")),
                "slashing": SpriteAnimator(os.path.join(base_path, "slashing")),
                "hurt": SpriteAnimator(os.path.join(base_path, "hurt")),
                "dying": SpriteAnimator(os.path.join(base_path, "dying")),
            }

        super().__init__(name, hp, attack_speed, chance_to_hit,
                         damage_min, damage_max, chance_to_heal, heal_min, heal_max,
                         animations=Skeleton._cached_animations)


    def attack(self, target):

        now = pygame.time.get_ticks()
        if now - self._last_attack_time < (1000 / self.attack_speed):
            return
        self._last_attack_time = now

        self.start_attack()
        if random.random() < self.chance_to_hit:
            damage = random.randint(self.damage_min, self.damage_max)
            print(f"{self.name} slashes {target.name} for {damage} damage.")
            target.take_damage(damage)
        else:
            print(f"{self.name}'s slash missed!")

        if "slashing" in self.animations:
            self.current_animation = "slashing"
            self._last_animation_change = pygame.time.get_ticks()

        self.end_attack()

    def get_heal_range(self):
        return self.heal_min, self.heal_max

    def update_animation(self, dt):
        now = pygame.time.get_ticks()

        # Auto-revert temporary animations like hurt/slashing after lock duration
        if self.current_animation in ["hurt",
                                      "slashing"] and now - self._last_animation_change > self._animation_lock_duration:
            self.current_animation = "idle"

        if self.current_animation in self.animations:
            self.animations[self.current_animation].update(dt)

    def get_current_frame(self):
        return self.animations[self.current_animation].get_current_frame()

    def __str__(self):
        return (
            f"{self.name} the Skeleton - "
            f"HP: {self.health_points}, "
            f"DMG: {self.damage_min}-{self.damage_max}, "
            f"Heal: {self.heal_min}-{self.heal_max}"
        )
