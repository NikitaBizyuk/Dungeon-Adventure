import random
import os
import pygame
from model.Monster import Monster
from view.sprite_animator import SpriteAnimator

class AnimatedMonster(Monster):
    def __init__(self, name, hp, attack_speed, chance_to_hit,
                 damage_min, damage_max, chance_to_heal, heal_min, heal_max,
                 animations=None, sprite_folder=None):
        super().__init__(name, damage_min, damage_max, attack_speed, hp,
                         chance_to_hit, chance_to_heal, heal_min, heal_max)

        if animations:
            self.animations = animations
        else:
            base_path = os.path.abspath(os.path.join("assets", "sprites", sprite_folder))
            self.animations = {
                "idle": SpriteAnimator(os.path.join(base_path, "idle")),
                "running": SpriteAnimator(os.path.join(base_path, "running")),
                "slashing": SpriteAnimator(os.path.join(base_path, "slashing")),
                "hurt": SpriteAnimator(os.path.join(base_path, "hurt")),
                "dying": SpriteAnimator(os.path.join(base_path, "dying")),
            }

        self.current_animation = "idle"
        self.facing_right = True
        self._last_hit_time = -1000
        self._last_animation_change = 0
        self._animation_lock_duration = 300
        self._sprite_folder = "zombie_villager_1"
        self._reload_animations()


    def update_animation(self, dt):
        if self.current_animation in self.animations:
            self.animations[self.current_animation].update(dt)

    def get_current_frame(self):
        frame = self.animations[self.current_animation].get_current_frame()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        return frame

    def take_damage(self, amount):
        self.health_points -= amount
        print(f"{self.name} took {amount} damage.")
        self.flash_hit()

        if "hurt" in self.animations:
            self.current_animation = "hurt"
            self._last_animation_change = pygame.time.get_ticks()

        self.heal()

        if self.health_points <= 0 and "dying" in self.animations:
            self.current_animation = "dying"
            self._last_animation_change = pygame.time.get_ticks()

    def flash_hit(self):
        self._last_hit_time = pygame.time.get_ticks()

    def is_flashing(self):
        return pygame.time.get_ticks() - self._last_hit_time < 200

    def start_attack(self):
        self._attacking = True
        if "slashing" in self.animations:
            self.current_animation = "slashing"
            self._last_animation_change = pygame.time.get_ticks()

    def end_attack(self):
        self._attacking = False
        self.current_animation = "idle"

    def is_attacking(self):
        return self._attacking

    def __getstate__(self):
        state = self.__dict__.copy()
        if "animations" in state:
            del state["animations"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._reload_animations()

    def _reload_animations(self):
        import os
        from view.sprite_animator import SpriteAnimator

        # ✅ Store this in __init__: self._sprite_folder = "zombie_villager_1"
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", self._sprite_folder)
        )

        self.animations = {
            "idle": SpriteAnimator(os.path.join(base_path, "idle")),
            "running": SpriteAnimator(os.path.join(base_path, "running")),
            "slashing": SpriteAnimator(os.path.join(base_path, "slashing")),
            "hurt": SpriteAnimator(os.path.join(base_path, "hurt")),
            "dying": SpriteAnimator(os.path.join(base_path, "dying")),
        }

