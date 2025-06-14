import pygame
from model.Dungeon import Dungeon
from model.Warrior import Warrior
from model.Room import Room
from model.Projectile import Projectile
from model.Backpack import BackPack
from view.game_view import GameView

class DungeonAdventure:
    """
    Central controller that manages hero, monsters, projectiles, rooms,
    pit deaths, respawns, and a 3-life system.
    """

    def __init__(self, view, hero_cls=Warrior, hero_name: str = "Rudy") -> None:
        self.dungeon = Dungeon(difficulty=Room._current_difficulty)
        self.hero = hero_cls(hero_name)
        self.my_back_pack = BackPack()
        self.in_room = False
        self.active_room = None
        self.game_over = False
        self.lives_remaining = 3

        self.aim_vector = (1, 0)
        self._projectiles = []
        self.last_projectile_time = 0
        self.monster_last_move_time = 0

        self.special_active = False
        self.special_cooldown = 8000
        self.special_duration = 3000
        self.last_special_used = -9999

        self.vision_reveal_start = None
        self.vision_reveal_duration = 3000
        self.view = view

    def move_hero(self, dx, dy, view):
        if self.dungeon.in_room:
            outcome = self.dungeon.active_room.move_hero_in_room(
                dx, dy, self.my_back_pack, view
            )
            if outcome == "pit":
                difficulty = Room._current_difficulty.lower()

                if difficulty == "easy":
                    self.hero.take_damage(30)
                    self.view.display_message("⚠️ You fell into a pit! -30 HP", 2000)
                elif difficulty == "medium":
                    self.hero.take_damage(50)
                    self.view.display_message("⚠️ You fell into a pit! -50 HP", 2000)
                else:  # hard
                    self.hero.instant_death()
                    self._lose_life_and_respawn()
                    self.view.display_message("☠️ You fell into a pit and died!", 2000)
                    return "pit"

                if self.hero.health_points <= 0:
                    self._lose_life_and_respawn()

                return "pit"

            if outcome == "exit":
                self._leave_room()
                return "exit"
            return outcome

        self.dungeon.move_hero(dx, dy)
        cell = self.dungeon.maze[self.dungeon.hero_x][self.dungeon.hero_y]
        print("cell:", cell.cell_type, "| pillars:", self.my_back_pack.pillar_cntr)

        if cell.cell_type == "exit" and self.my_back_pack.pillar_cntr == 4:
            self.view.display_message("🏆 You escaped the dungeon!\nAll 4 Pillars Found!", 4000)
            for _ in range(60):
                self.view.draw_maze(self, pygame.display.get_surface().get_width(),
                                    pygame.display.get_surface().get_height(), self.get_hero(), self.get_backpack())
                pygame.display.flip()
                pygame.time.delay(16)
            return "win"

        if self.dungeon.in_room:
            self.in_room = True
            self.active_room = self.dungeon.active_room
            self.active_room.enter(self)
            return "room_enter"

        return None

    def _lose_life_and_respawn(self):
        self.lives_remaining -= 1
        print(f"❗ Life lost! Lives remaining: {self.lives_remaining}")
        if self.lives_remaining <= 0:
            self.game_over = True
            print("💀 No lives left — game over.")
            return
        self.hero.health_points = self.hero._max_health_points
        self._leave_room()

    def _leave_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None

    def move_monsters(self):
        if not self.in_room or not self.active_room:
            return
        now = pygame.time.get_ticks()
        if now - self.monster_last_move_time > 400:
            self.active_room.move_monsters()
            self.monster_last_move_time = now

    def perform_melee_attack(self):
        if not self.in_room or not self.active_room:
            return
        hero_r, hero_c = self.active_room.get_hero_position()
        dx, dy = self.aim_vector
        if abs(dx) > abs(dy):
            tr, tc = hero_r, hero_c + (1 if dx > 0 else -1)
        else:
            tr, tc = hero_r + (1 if dy > 0 else -1), hero_c

        monster = self.active_room.get_monster_at(tr, tc)
        if monster:
            if self.special_active:
                self.hero.special_skill(monster)
            else:
                self.hero.attack(monster)
            monster.flash_hit()
            if not monster.is_alive():
                del self.active_room.monsters[monster]

    def perform_ranged_attack(self, cell_size: int):
        now = pygame.time.get_ticks()
        if now - self.last_projectile_time < self.hero.projectile_cooldown:
            return
        dx, dy = self.aim_vector

        if self.in_room and self.active_room:
            r, c = self.active_room.get_hero_position()
        else:
            r, c = self.dungeon.hero_x, self.dungeon.hero_y

        px = c * cell_size + cell_size // 2
        py = r * cell_size + cell_size // 2

        self._projectiles.append(
            Projectile(px, py, dx, dy,
                       speed=self.hero.projectile_speed,
                       damage=self.hero.projectile_damage)
        )
        self.last_projectile_time = now

    def perform_special_attack(self) -> str:
        now = pygame.time.get_ticks()
        if now - self.last_special_used < self.special_cooldown:
            return "Special cooling down..."
        self.last_special_used = now
        self.special_active = True
        return "Special activated!"

    def update_projectiles(self, cell_size: int):
        if not self.in_room or not self.active_room:
            return

        room = self.active_room
        for p in self._projectiles:
            p.update()
            gx = int(p.x / cell_size)
            gy = int(p.y / cell_size)
            m = room.get_monster_at(gy, gx)
            if m:
                self.hero.attack(m, p.damage)
                m.flash_hit()
                if not m.is_alive():
                    del room.monsters[m]
                p.deactivate()
        self._projectiles = [p for p in self._projectiles if p.active]

    @property
    def projectiles(self):
        return self._projectiles

    def monster_attack_hero(self):
        if not self.in_room or not self.active_room:
            return
        hr, hc = self.active_room.get_hero_position()
        for m, (mr, mc) in self.active_room.monsters.items():
            if abs(mr - hr) + abs(mc - hc) == 1:
                m.attack(self.hero)
                if self.hero.health_points <= 0:
                    self._lose_life_and_respawn()

    def is_special_active(self):
        if not self.special_active:
            return False
        now = pygame.time.get_ticks()
        if now - self.last_special_used > self.special_duration:
            self.special_active = False
            return False
        return True

    def get_special_remaining_time(self):
        if not self.special_active:
            return 0
        now = pygame.time.get_ticks()
        return max(0, self.special_duration - (now - self.last_special_used))

    def get_hero(self):       return self.hero
    def get_backpack(self):   return self.my_back_pack
    def get_lives(self):      return self.lives_remaining

    def __getstate__(self):
        state = self.__dict__.copy()
        if "view" in state:
            del state["view"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.view = None
