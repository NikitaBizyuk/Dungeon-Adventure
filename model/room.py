import pygame

from model.MonsterFactory import MonsterFactory
import random
from model.MonsterFactory import MonsterFactory
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre

class Room:
    room_ID = 0
    loot = ["Encapsulation", "Abstraction","Polymorphism",
            "Inheritance","Health Potion","Vision Potion"]
    def __init__(self, door_r, door_c, width=25, height=15):
        self.width = width
        self.height = height
        self.grid = [["wall" for _ in range(width)] for _ in range(height)]
        self.hero_r = height - 2  # hero spawns just above the door
        self.hero_c = width // 2
        self.door_r = height - 1  # door is now on the bottom row
        self.door_c = width // 2
        self._carve_layout()
        self.num_monsters = random.randint(3,10)
        self.monsters = {
            MonsterFactory.create_random_monster(): (
            random.randint(1, height - 2), random.randint(1, width - 2))
            for _ in range(self.num_monsters)
        }
        random.shuffle(Room.loot)
        Room.room_ID +=1


    def _carve_layout(self):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                if r == (self.height - 1)/2 and c == (self.width - 1)/2:
                    self.grid[r][c] = Room.loot[0]
                    if (Room.loot[0] == "Encapsulation" or Room.loot[0] == "Abstraction" or
                        Room.loot[0] == "Polymorphism" or Room.loot[0] == "Inheritance"):
                        Room.loot.pop(0)
                else:
                    self.grid[r][c] = "floor"
        self.grid[self.door_r][self.door_c] = "door"
        self.grid[self.hero_r][self.hero_c] = "floor"

    def move_monsters(self):
        cntr = 0
        for monster in self.monsters:
            r, c = self.monsters[monster]
            dr = 1 if r < self.hero_r else -1 if r > self.hero_r else 0
            dc = 1 if c < self.hero_c else -1 if c > self.hero_c else 0
            new_r = r + dr
            new_c = c + dc
            if (new_r, new_c) == (self.hero_r,self.hero_c):
                continue
            if (new_r, new_c) in self.monsters.values():
                continue
            if random.randint(1,100) % 7 == 0:
                new_r += 1
            if random.randint(1,100) % 9 == 0:
                new_r += 1
            if random.randint(1,100) % 4 == 0:
                new_c += 1
            if random.randint(1,100) % 9 == 0:
                new_c += 1
            cntr += 1
            # Check if within bounds and walkable
            if 0 <= new_r < self.height and 0 <= new_c < self.width:
                if self.grid[new_r][new_c] in ["floor", "door"]:
                    self.monsters[monster] = (new_r, new_c)
        return None

    def move_hero_in_room(self, dx, dy):
        nr = self.hero_r + dx
        nc = self.hero_c + dy
        if 0 <= nr < self.height and 0 <= nc < self.width:
            target = self.grid[nr][nc]
            if target in ["floor", "door"]:
                self.hero_r = nr
                self.hero_c = nc
                if target == "door":
                    return "exit"
        return None

    def get_tile(self, r, c):
        return self.grid[r][c]

    def get_hero_position(self):
        return self.hero_r, self.hero_c

    def get_dimensions(self):
        return self.height, self.width
    def get_monsters(self):
        return self.monsters
    #
    # def toString(self):
    #     result = ""
    #     for r in range(15):
    #         for c in range(100):
    #             # Top and bottom borders
    #             if r == 0 or r == 14:
    #                 result += "*"
    #             # Side borders
    #             elif c == 0 or c == 99:
    #                 result += "*"
    #             elif c == 50 and r == 14:
    #                 result += "_"  # door in the middle bottom
    #
    #             # Interior space
    #             else:
    #                 result += " "
    #         result += "\n"
    #     return result


#__repr__