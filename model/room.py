import random
from model.MonsterFactory import MonsterFactory
from model.OOPillars import OOPillars

class Room:
    # ───── Static class-level values ─────
    room_ID = 0
    #loot = ["A", "E", "I","P", "Health Potion", "Vision Potion"]

    _DIFFICULTY_TO_RANGE = {
        "easy": (1, 3),
        "medium": (4, 7),
        "hard": (8, 10),
    }
    _current_difficulty = "medium"

    @classmethod
    def set_difficulty(cls, level):
        """Sets monster spawn difficulty for all future rooms."""
        cls._current_difficulty = level if level in cls._DIFFICULTY_TO_RANGE else "medium"

    # ───── Room Initialization ─────
    def __init__(self, door_r, door_c, width=25, height=15):
        self.width = width
        self.height = height
        self.grid = [["wall" for _ in range(width)] for _ in range(height)]
        self.hero_r = height - 2
        self.hero_c = width // 2
        self.door_r = height - 1
        self.door_c = width // 2
        self.is_trap = random.random() < 0.1
        self._carve_layout()

        # Difficulty-based monster range
        low, high = Room._DIFFICULTY_TO_RANGE[Room._current_difficulty]
        self.num_monsters = random.randint(low, high)

        self.monsters = {
            MonsterFactory.create_random_monster(): (
                random.randint(1, height - 2),
                random.randint(1, width - 2)
            )
            for _ in range(self.num_monsters)
        }

        #random.shuffle(Room.loot)
        Room.room_ID += 1

    def place_item(self, item_symbol):
        empty_tiles = [
            (r, c)
            for r in range(1, self.height - 1)
            for c in range(1, self.width - 1)
            if self.grid[r][c] == "floor"
        ]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.grid[r][c] = item_symbol

    def _carve_layout(self):
         for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
     #             if r == (self.height - 1) / 2 and c == (self.width - 1) / 2:
    #                 random.shuffle(self.loot)
                     self.grid[r][c] = "floor"
    #                 if Room.loot[0] in {"A", "E", "I", "P"}:
    #                     Room.loot.pop(0)
    #             else:
    #                 self.grid[r][c] = "floor"
    #
            self.grid[self.door_r][self.door_c] = "door"
            self.grid[self.hero_r][self.hero_c] = "floor"

    def place_random_loot(self):
        loot_candidates = []
        if random.random() < 0.6:  # 60% chance to place health potion
            loot_candidates.append("Health Potion")
        if random.random() < 0.5:  # 50% chance to place vision potion
            loot_candidates.append("Vision Potion")

        for item in loot_candidates:
            self.place_item(item)

    def move_monsters(self):
        new_positions = {}
        occupied = set(self.monsters.values())
        occupied.add((self.hero_r, self.hero_c))

        for monster in list(self.monsters.keys()):
            r, c = self.monsters[monster]
            dr = 1 if r < self.hero_r else -1 if r > self.hero_r else 0
            dc = 1 if c < self.hero_c else -1 if c > self.hero_c else 0
            new_r = r + dr
            new_c = c + dc

            if random.randint(1, 100) % 7 == 0: new_r += 1
            if random.randint(1, 100) % 9 == 0: new_r += 1
            if random.randint(1, 100) % 4 == 0: new_c += 1
            if random.randint(1, 100) % 9 == 0: new_c += 1

            if (0 <= new_r < self.height and 0 <= new_c < self.width and
                    self.grid[new_r][new_c] in ["floor", "door"] and
                    (new_r, new_c) not in occupied):
                new_positions[monster] = (new_r, new_c)
                occupied.add((new_r, new_c))
            else:
                new_positions[monster] = (r, c)
                occupied.add((r, c))

        self.monsters = new_positions

    def move_hero_in_room(self, dx, dy, back_pack,view):
        nr = self.hero_r + dx
        nc = self.hero_c + dy

        if 0 <= nr < self.height and 0 <= nc < self.width:
            target = self.grid[nr][nc]
            if any((nr, nc) == (mr, mc) for (mr, mc) in self.monsters.values()):
                return None
            if target in ["floor", "door","A","E","I","P","Health Potion","Vision Potion"]:
                self.hero_r = nr
                self.hero_c = nc
                if target == "door":
                    return "exit"
            if target in ["A","E","I","P","Health Potion", "Vision Potion"]:
                back_pack.add(target,view)
                self.grid[nr][nc] = "floor"
                print("my back pack has",back_pack.to_string())
        return None

    # ───── Accessors ─────
    def get_tile(self, r, c):
        return self.grid[r][c]

    def get_hero_position(self):
        return self.hero_r, self.hero_c

    def get_dimensions(self):
        return self.height, self.width

    def get_monsters(self):
        return self.monsters

    def get_monster_at(self, r, c):
        for monster, (mr, mc) in self.monsters.items():
            if (mr, mc) == (r, c):
                return monster
        return None

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