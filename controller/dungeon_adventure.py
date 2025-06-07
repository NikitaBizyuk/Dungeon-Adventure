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
from model.backpack import BackPack
import random

class DungeonAdventure:
    def __init__(self):
        self.dungeon = Dungeon(difficulty=Room._current_difficulty)
        self.hero = Priestess("Rudy")
        self.my_back_pack = BackPack()
        self.in_room = False
        self.active_room = None
        self.aim_vector = (1, 0)
        self.monster_last_move_time = 0

    def move_hero(self, dx, dy):
        if self.dungeon.in_room:
            status = self.dungeon.active_room.move_hero_in_room(dx, dy,self.my_back_pack)
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

    def get_hero(self):
        return self.hero

    def get_backpack(self):
        return self.my_back_pack

    def exit_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None
