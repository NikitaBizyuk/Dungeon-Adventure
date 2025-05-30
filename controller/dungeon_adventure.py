import pygame

from model.dungeon import Dungeon
from model.warrior import Warrior
from model.MonsterFactory import MonsterFactory
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.room import Room
import random

class DungeonAdventure:
    def __init__(self):
        self.dungeon = Dungeon(rows=61, cols=61, difficulty="large")
        self.hero = Warrior("Rudy")
        self.in_room = False
        self.active_room = None
        self.monster_last_move_time = 0

    def move_hero(self, dx, dy):
        current_time = pygame.time.get_ticks()
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

    def exit_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None
