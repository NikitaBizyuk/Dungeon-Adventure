import os
import pygame
from model.Hero import Hero
from view.sprite_animator import SpriteAnimator

class AnimatedHero(Hero):
    def __init__(self, name, health_points, damage_min, damage_max,
                 attack_speed, chance_to_hit, sprite_folder):
        super().__init__(name, health_points, damage_min, damage_max,
                         attack_speed, chance_to_hit)

        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", sprite_folder)
        base_path = os.path.abspath(base_path)

        self.animations = {
            "idle": SpriteAnimator(os.path.join(base_path, "idle")),
            "running": SpriteAnimator(os.path.join(base_path, "running")),
            "slashing": SpriteAnimator(os.path.join(base_path, "slashing")),
            "run_slashing": SpriteAnimator(os.path.join(base_path, "run_slashing")),  # ✅ add
            "throwing": SpriteAnimator(os.path.join(base_path, "throwing")),
            "run_throwing": SpriteAnimator(os.path.join(base_path, "run_throwing")),  # ✅ add
            "hurt": SpriteAnimator(os.path.join(base_path, "hurt")),
        }

        self.current_animation = "idle"
        self._moving = False
        self.facing_right = True
        self._last_hit_time = -1000
        self._last_animation_change = 0
        self._animation_lock_duration = 300
        self._dead = False
        self._sprite_folder = "valkyrie_2"
        self._reload_animations()

    def take_damage(self, amount):
        self.health_points -= amount
        print(f"{self.name} took {amount} damage! Remaining HP: {self.health_points}")

        self.flash_hit()
        if "hurt" in self.animations:
            self.current_animation = "hurt"
            self._last_animation_change = pygame.time.get_ticks()

        if self.health_points <= 0 and "dying" in self.animations:
            self.current_animation = "dying"
            self._last_animation_change = pygame.time.get_ticks()


    def flash_hit(self):
        self._last_hit_time = pygame.time.get_ticks()

    def is_flashing(self):
        return pygame.time.get_ticks() - self._last_hit_time < 200

    def start_attack(self):
        self.current_animation = "slashing"
        self._last_animation_change = pygame.time.get_ticks()

    def end_attack(self):
        self.current_animation = "idle"

    def update_animation(self, dt):

        if not self.is_alive():
            self.current_animation = "dead"
            self.animations["dead"].update(dt)
            return
        now = pygame.time.get_ticks()

        # Revert temporary animations after lock duration
        if self.current_animation in ["slashing", "throwing", "run_slashing", "run_throwing"]:
            if now - self._last_animation_change > self._animation_lock_duration:
                self.current_animation = "running" if self._moving else "idle"

        # If not locked, decide animation based on movement
        elif self.current_animation not in self.animations or self.current_animation in ["idle", "running"]:
            self.current_animation = "running" if self._moving else "idle"

        # Finally update the animator
        if self.current_animation in self.animations:
            self.animations[self.current_animation].update(dt)

    def get_current_frame(self):
        return self.animations[self.current_animation].get_current_frame()

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpickleable parts (SpriteAnimator instances)
        if "animations" in state:
            del state["animations"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Reload animations after unpickling
        self._reload_animations()

    def _reload_animations(self):
        import os
        from view.sprite_animator import SpriteAnimator

        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", self._sprite_folder)
        )

        self.animations = {
            "idle": SpriteAnimator(os.path.join(base_path, "idle")),
            "running": SpriteAnimator(os.path.join(base_path, "running")),
            "slashing": SpriteAnimator(os.path.join(base_path, "slashing")),
            "run_slashing": SpriteAnimator(os.path.join(base_path, "run_slashing")),
            "throwing": SpriteAnimator(os.path.join(base_path, "throwing")),
            "run_throwing": SpriteAnimator(os.path.join(base_path, "run_throwing")),
            "hurt": SpriteAnimator(os.path.join(base_path, "hurt")),
        }
