import pygame

from model.dungeon import Dungeon
from model.Priestess import Priestess
from model.warrior import Warrior
from model.Thief import Thief
from model.MonsterFactory import MonsterFactory
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.room import Room
import random
from model.projectile import Projectile
import math


class DungeonAdventure:
    def __init__(self):
        self.dungeon = Dungeon(difficulty=Room._current_difficulty)
        self.hero = Priestess("Rudy")
        self.in_room = False
        self.active_room = None
        self.aim_vector = (1, 0)
        self.monster_last_move_time = 0
        self._projectiles = []

    def move_hero(self, dx, dy):
        if self.dungeon.in_room:
            status = self.dungeon.active_room.move_hero_in_room(dx, dy)
            if status == "exit":
                self.dungeon.in_room = False
                self.dungeon.active_room = None
                self.in_room = False
                self.active_room = None
        else:
            self.dungeon.move_hero(dx, dy)
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
                print(f"🗡️ Rudy attacks {monster.name} at ({target_r}, {target_c})")
                self.hero.attack(monster)
                monster.flash_hit()
                print(f"🧟 {monster.name} HP after attack: {monster.health_points}")
                if not monster.is_alive():
                    print(f"💀 {monster.name} has died and is removed from the room.")
                    del self.active_room.monsters[monster]

    def perform_ranged_attack(self, cell_size):
        dx, dy = self.aim_vector

        if self.in_room and self.active_room:
            hero_r, hero_c = self.active_room.get_hero_position()
        else:
            hero_r, hero_c = self.dungeon.hero_x, self.dungeon.hero_y

        # Convert grid position to pixel position
        x = hero_c * cell_size + cell_size // 2
        y = hero_r * cell_size + cell_size // 2

        projectile = Projectile(x, y, dx, dy)
        self.projectiles.append(projectile)

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
                print(f"🏹 Rudy's projectile hits {monster.name} at ({grid_y}, {grid_x})")
                self.hero.attack(monster)
                monster.flash_hit()
                if not monster.is_alive():
                    print(f"💀 {monster.name} was killed by a projectile.")
                    del room.monsters[monster]
                projectile.deactivate()

        self._projectiles = [p for p in self.projectiles if p.active]

    @property
    def projectiles(self):
        return self._projectiles

    def exit_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None
