import pygame
import math
from model.dungeon import Dungeon
from model.Priestess import Priestess
from model.warrior import Warrior
from model.Thief import Thief
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.room import Room
from model.projectile import Projectile
from model.backpack import BackPack
import random
from view.game_view import GameView

class DungeonAdventure:
    def __init__(self,view):
        self.dungeon = Dungeon(difficulty=Room._current_difficulty)
        self.hero = Warrior("Rudy")
        self.my_back_pack = BackPack()
        self.in_room = False
        self.active_room = None
        self.aim_vector = (1, 0)
        self.monster_last_move_time = 0
        self._projectiles = []
        self.last_projectile_time = 0
        self.special_active = False
        self.special_cooldown = 8000
        self.special_duration = 3000
        self.last_special_used = -9999
        self.vision_reveal_start = None
        self.vision_reveal_duration = 3000
        self.view = view
        self.hero_r = ""
        self.hero_c = ""
    def move_hero(self, dx, dy,view):
        if self.dungeon.in_room:
            status = self.dungeon.active_room.move_hero_in_room(dx, dy, self.my_back_pack,view)
            if status == "exit":
                self.dungeon.in_room = False
                self.dungeon.active_room = None
                self.in_room = False
                self.active_room = None
        else:
            self.dungeon.move_hero(dx, dy)
            cell = self.dungeon.maze[self.dungeon.hero_x][self.dungeon.hero_y]
            print("cell:", cell.cell_type, "| pillars:", self.my_back_pack.pillar_cntr)
            if cell.cell_type == "exit" and self.my_back_pack.pillar_cntr == 4:
                self.view.display_message("🏆 You escaped the dungeon!\nAll 4 Pillars Found!", 4000)

                # Force redraw cycle before quitting
                frames_to_show = 60  # show message for 1 second (60 frames at 60 FPS)
                for _ in range(frames_to_show):
                    self.view.draw_maze(self, pygame.display.get_surface().get_width(),
                                        pygame.display.get_surface().get_height(), self.get_hero(), self.get_backpack())
                    pygame.display.flip()
                    pygame.time.delay(16)  # ~60 FPS

                return "win"
            if self.dungeon.in_room:
                self.in_room = True
                self.active_room = self.dungeon.active_room

    def move_monsters(self):
        if self.in_room:
            current_time = pygame.time.get_ticks()
            if current_time - self.monster_last_move_time > 400:
                self.dungeon.active_room.move_monsters()
                self.monster_last_move_time = current_time

    def perform_melee_attack(self):
        if self.in_room and self.active_room:
            hero_r, hero_c = self.active_room.get_hero_position()
            dx, dy = self.aim_vector

            if abs(dx) > abs(dy):
                target_r = hero_r
                target_c = hero_c + (1 if dx > 0 else -1)
            else:
                target_r = hero_r + (1 if dy > 0 else -1)
                target_c = hero_c

            monster = self.active_room.get_monster_at(target_r, target_c)
            if monster:
                print(f"🗡️ {self.hero.name} attacks {monster.name} at ({target_r}, {target_c})")
                if self.special_active:
                    self.hero.special_skill(monster)
                else:
                    self.hero.attack(monster)
                monster.flash_hit()
                print(f"🧟 {monster.name} HP after attack: {monster.health_points}")
                if not monster.is_alive():
                    print(f"💀 {monster.name} has died and is removed from the room.")
                    del self.active_room.monsters[monster]

    def perform_ranged_attack(self, cell_size):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_projectile_time < self.hero.projectile_cooldown:
            return

        dx, dy = self.aim_vector

        if self.in_room and self.active_room:
            hero_r, hero_c = self.active_room.get_hero_position()
        else:
            hero_r, hero_c = self.dungeon.hero_x, self.dungeon.hero_y

        x = hero_c * cell_size + cell_size // 2
        y = hero_r * cell_size + cell_size // 2

        projectile = Projectile(
            x, y, dx, dy,
            speed=self.hero.projectile_speed,
            damage=self.hero.projectile_damage
        )

        self.projectiles.append(projectile)
        self.last_projectile_time = current_time

    def perform_special_attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_special_used < self.special_cooldown:
            return "Special cooling down..."

        self.last_special_used = now
        self.special_active = True
        return "Special activated!"

    def update_projectiles(self, cell_size):
        if not self.in_room or not self.active_room:
            return

        room = self.active_room
        for projectile in self.projectiles:
            projectile.update()
            px, py = projectile.get_position()

            grid_x = int(px / cell_size)
            grid_y = int(py / cell_size)

            monster = room.get_monster_at(grid_y, grid_x)
            if monster:
                print(f"🏹 {self.hero.name}'s projectile hits {monster.name} at ({grid_y}, {grid_x})")
                self.hero.attack(monster, projectile.damage)
                monster.flash_hit()
                if not monster.is_alive():
                    print(f"💀 {monster.name} was killed by a projectile.")
                    del room.monsters[monster]
                projectile.deactivate()

        self._projectiles = [p for p in self.projectiles if p.active]

    @property
    def projectiles(self):
        return self._projectiles

    def monster_attack_hero(self):
        if not self.in_room or not self.active_room:
            return

        hero_r, hero_c = self.active_room.get_hero_position()

        for monster, (mr, mc) in self.active_room.monsters.items():
            if abs(mr - hero_r) + abs(mc - hero_c) == 1:
                print(f"💀 {monster.name} is adjacent to the hero and attacks!")
                monster.attack(self.hero)
                self.check_hero_defeated()

    def check_hero_defeated(self):
        if self.hero.health_points <= 0:
            print(f"💀 {self.hero.name} has been defeated! Returning to maze with full HP...")
            self.hero.health_points = 100
            self.exit_room()

    def get_hero(self):
        return self.hero

    def get_backpack(self):
        return self.my_back_pack

    def exit_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None

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
        remaining = max(0, self.special_duration - (now - self.last_special_used))
        return remaining
