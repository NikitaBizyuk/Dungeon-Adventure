import pygame

from model.AnimatedHero import AnimatedHero
from model.Dungeon import Dungeon
from model.Warrior import Warrior
from model.Room import Room
from model.Projectile import Projectile
from model.Backpack import BackPack
from view.game_view import GameView


class DungeonAdventure:
    """Central controller that manages gameplay and game state."""

    def __init__(self, view: GameView, hero_cls=Warrior, hero_name: str = "Rudy") -> None:
        self._dungeon = Dungeon(difficulty=Room._current_difficulty)
        self._hero = hero_cls(hero_name)
        self._backpack = BackPack()
        self._in_room = False
        self._active_room = None
        self._game_over = False
        self._lives_remaining = 3

        self._aim_vector = (1, 0)
        self._projectiles = []
        self._last_projectile_time = 0
        self._monster_last_move_time = 0

        self._special_active = False
        self._special_cooldown = 8000
        self._special_duration = 3000
        self._last_special_used = -9999

        self._vision_reveal_start = None
        self._vision_reveal_duration = 3000
        self._view = view
        self._hero_facing = "down"
        self._last_hero_tile = None

    def move_hero(self, dx, dy, view):
        if dx == -1:
            self._hero_facing = "up"
        elif dx == 1:
            self._hero_facing = "down"
        elif dy == -1:
            self._hero_facing = "left"
        elif dy == 1:
            self._hero_facing = "right"
        if self._dungeon.in_room:
            r_before, c_before = self._dungeon.active_room.get_hero_position()
            outcome = self._dungeon.active_room.move_hero_in_room(dx, dy, self._backpack, view)
            r_after, c_after = self._dungeon.active_room.get_hero_position()

            if outcome == "pit":
                r_after, c_after = self._dungeon.active_room.get_hero_position()

                if self._last_hero_tile != "pit":
                    difficulty = Room._current_difficulty.lower()
                    if difficulty == "easy":
                        self._hero.take_damage(30)
                        self._view.display_message("⚠️ You fell into a pit! -30 HP", 2000)
                    elif difficulty == "medium":
                        self._hero.take_damage(50)
                        self._view.display_message("⚠️ You fell into a pit! -50 HP", 2000)
                    else:
                        self._hero.instant_death()
                        self._view.display_message("☠️ You fell into a pit and died!", 2000)

                    if self._hero.health_points <= 0:
                        self._lose_life_and_respawn()

                self._last_hero_tile = "pit"
                return "pit"




            elif outcome == "exit":
                self._in_room = False
                self._dungeon.in_room = False
                self._active_room = None
                self._dungeon.update_visibility()
                return "exit"
            if outcome != "pit":
                self._last_hero_tile = outcome
            return outcome

        self._dungeon.move_hero_in_room(dx, dy, self._backpack, self._view)

        cell = self._dungeon.maze[self._dungeon.hero_x][self._dungeon.hero_y]

        if cell.cell_type == "exit" and self._backpack.pillar_cntr == 4:
            self._view.display_message("🏆 You escaped the dungeon!\nAll 4 Pillars Found!", 4000)
            for _ in range(60):
                self._view.draw_maze(self, pygame.display.get_surface().get_width(),
                                     pygame.display.get_surface().get_height(),
                                     self._hero, self._backpack)
                pygame.display.flip()
                pygame.time.delay(16)
            return "win"

        if self._dungeon.in_room:
            self._in_room = True
            self._active_room = self._dungeon.active_room
            self._active_room.enter(self)
            return "room_enter"

        return None

    def _lose_life_and_respawn(self):
        self._lives_remaining -= 1
        if self._lives_remaining <= 0:
            self._game_over = True
            return
        self._hero.health_points = self._hero.max_health_points
        self._leave_room()

    def _leave_room(self):
        self._in_room = False
        self._dungeon.in_room = False
        self._active_room = None


    def move_monsters(self):
        if not self._in_room or not self._active_room:
            return
        now = pygame.time.get_ticks()
        if now - self._monster_last_move_time > 400:
            self._active_room.move_monsters()
            self._monster_last_move_time = now

    def perform_melee_attack(self):
        if not self._in_room or not self._active_room:
            return
        hero_r, hero_c = self._active_room.get_hero_position()
        dx, dy = self._aim_vector
        if abs(dx) > abs(dy):
            tr, tc = hero_r, hero_c + (1 if dx > 0 else -1)
        else:
            tr, tc = hero_r + (1 if dy > 0 else -1), hero_c

        monster = self._active_room.get_monster_at(tr, tc)
        if monster:
            if self._special_active:
                self._hero.special_skill(monster)
            else:
                self._hero.attack(monster)
            if isinstance(self._hero, AnimatedHero):
                self._hero.current_animation = "slashing"
                self._hero._last_animation_change = pygame.time.get_ticks()
            monster.flash_hit()
            if not monster.is_alive():
                del self._active_room.monsters[monster]

    def perform_ranged_attack(self, cell_size: int):
        now = pygame.time.get_ticks()
        if now - self._last_projectile_time < self._hero.projectile_cooldown:
            return
        dx, dy = self._aim_vector

        if self._in_room and self._active_room:
            r, c = self._active_room.get_hero_position()
        else:
            r, c = self._dungeon.hero_x, self._dungeon.hero_y

        px = c * cell_size + cell_size // 2
        py = r * cell_size + cell_size // 2

        self._projectiles.append(
            Projectile(px, py, dx, dy,
                       speed=self._hero.projectile_speed,
                       damage=self._hero.projectile_damage)
        )
        self._last_projectile_time = now

        # ✅ Trigger "throwing" animation for AnimatedHero
        if isinstance(self._hero, AnimatedHero):
            if self._hero._moving:
                self._hero.current_animation = "run_throwing"
            else:
                self._hero.current_animation = "throwing"
            self._hero._last_animation_change = pygame.time.get_ticks()

    def perform_special_attack(self) -> str:
        now = pygame.time.get_ticks()
        if now - self._last_special_used < self._special_cooldown:
            return "Special cooling down..."
        self._last_special_used = now
        self._special_active = True
        return "Special activated!"

    def update_projectiles(self, cell_size: int):
        if not self._in_room or not self._active_room:
            return
        room = self._active_room
        for p in self._projectiles:
            p.update()
            gx = int(p.x / cell_size)
            gy = int(p.y / cell_size)
            m = room.get_monster_at(gy, gx)
            if m:
                self._hero.attack(m, p.damage)
                m.flash_hit()
                if not m.is_alive():
                    del room.monsters[m]
                p.deactivate()
        self._projectiles = [p for p in self._projectiles if p.active]

    def monster_attack_hero(self):
        if not self._in_room or not self._active_room:
            return
        hr, hc = self._active_room.get_hero_position()
        for m, (mr, mc) in self._active_room.monsters.items():
            if abs(mr - hr) + abs(mc - hc) == 1:
                if hasattr(m, "can_attack") and m.can_attack():
                    m.attack(self._hero)
                if self._hero.health_points <= 0:
                    self._hero.getting_hit = False
                    self._hero.current_animation = "dead"
                    self._lose_life_and_respawn()

    @property
    def special_active(self):
        if not self._special_active:
            return False
        now = pygame.time.get_ticks()
        if now - self._last_special_used > self._special_duration:
            self._special_active = False
            return False
        return True

    @property
    def special_remaining_time(self):
        if not self._special_active:
            return 0
        now = pygame.time.get_ticks()
        return max(0, self._special_duration - (now - self._last_special_used))

    @property
    def aim_vector(self):
        return self._aim_vector

    @aim_vector.setter
    def aim_vector(self, value):
        self._aim_vector = value

    @property
    def projectiles(self):
        return self._projectiles

    @property
    def hero(self):
        return self._hero

    @property
    def hero_weapon_type(self):
        return self._hero.weapon_type

    @property
    def backpack(self):
        return self._backpack

    @property
    def lives_remaining(self):
        return self._lives_remaining

    @property
    def game_over(self):
        return self._game_over

    @property
    def dungeon(self):
        return self._dungeon

    @property
    def active_room(self):
        return self._active_room

    @property
    def in_room(self):
        return self._in_room

    @property
    def last_special_used(self):
        return self._last_special_used

    @property
    def special_cooldown(self):
        return self._special_cooldown

    @property
    def special_duration(self):
        return self._special_duration

    @property
    def vision_reveal_start(self):
        return self._vision_reveal_start

    @property
    def vision_reveal_duration(self):
        return self._vision_reveal_duration

    @property
    def hero_facing(self):
        return self._hero_facing

    def attach_view(self, view):
        self._view = view

    @vision_reveal_start.setter
    def vision_reveal_start(self, value):
        self._vision_reveal_start = value
    def __getstate__(self):
        state = self.__dict__.copy()
        if "_view" in state:
            del state["_view"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._view = None