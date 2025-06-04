import random
import pygame

from model.MonsterFactory import MonsterFactory
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre


class Room:
    """
    A single rectangular room in the dungeon.
    The number of monsters spawned now depends on the global difficulty
    chosen via Room.set_difficulty("easy" | "medium" | "hard").
    """

    # ────────── difficulty → (min, max) monster range ────────── #
    _DIFFICULTY_TO_RANGE = {
        "easy":   (1, 3),
        "medium": (4, 7),   # matches original behaviour
        "hard":   (8, 10),
    }
    _current_difficulty = "medium"

    @classmethod
    def set_difficulty(cls, level: str) -> None:
        """Set the difficulty that all subsequently created rooms will use."""
        cls._current_difficulty = level if level in cls._DIFFICULTY_TO_RANGE else "medium"

    # ───────────────────────────────────────────────────────────── #

    room_ID = 0
    loot = [
        "Encapsulation",
        "Abstraction",
        "Polymorphism",
        "Inheritance",
        "Health Potion",
        "Vision Potion",
    ]

    def __init__(self, door_r, door_c, width=25, height=15):
        self.width = width
        self.height = height
        self.grid = [["wall" for _ in range(width)] for _ in range(height)]

        # hero + door positions
        self.hero_r = height - 2
        self.hero_c = width // 2
        self.door_r = height - 1
        self.door_c = width // 2

        # carve room layout
        self._carve_layout()

        # monster count based on difficulty
        low, high = Room._DIFFICULTY_TO_RANGE[Room._current_difficulty]
        self.num_monsters = random.randint(low, high)

        # place monsters
        self.monsters = {
            MonsterFactory.create_random_monster(): (
                random.randint(1, height - 2),
                random.randint(1, width - 2),
            )
            for _ in range(self.num_monsters)
        }

        random.shuffle(Room.loot)
        Room.room_ID += 1

    # ───────────────────────────────────────────────────────────── #

    def _carve_layout(self):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                if r == (self.height - 1) / 2 and c == (self.width - 1) / 2:
                    self.grid[r][c] = Room.loot[0]
                    if Room.loot[0] in (
                        "Encapsulation",
                        "Abstraction",
                        "Polymorphism",
                        "Inheritance",
                    ):
                        Room.loot.pop(0)
                else:
                    self.grid[r][c] = "floor"
        self.grid[self.door_r][self.door_c] = "door"
        self.grid[self.hero_r][self.hero_c] = "floor"

    def move_monsters(self):
        for monster in self.monsters:
            r, c = self.monsters[monster]
            dr = 1 if r < self.hero_r else -1 if r > self.hero_r else 0
            dc = 1 if c < self.hero_c else -1 if c > self.hero_c else 0
            new_r = r + dr
            new_c = c + dc
            if (new_r, new_c) == (self.hero_r, self.hero_c):
                continue
            if (new_r, new_c) in self.monsters.values():
                continue
            if random.randint(1, 100) % 7 == 0:
                new_r += 1
            if random.randint(1, 100) % 9 == 0:
                new_r += 1
            if random.randint(1, 100) % 4 == 0:
                new_c += 1
            if random.randint(1, 100) % 9 == 0:
                new_c += 1
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