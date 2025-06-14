import random
from model.MonsterFactory import MonsterFactory
from model.OOPillars import OOPillars

class Room:
    # ───── Static class-level values ─────
    room_ID = 0
    loot = ["A", "E", "I","P", "Health Potion", "Vision Potion"]

    _DIFFICULTY_TO_RANGE = {
        "easy": (1, 3),
        "medium": (4, 7),
        "hard": (8, 10),
    }
    _DIFFICULTY_TO_PIT = {
        "easy":   (0.15, (0, 1)),
        "medium": (0.45, (1, 2)),
        "hard":   (0.75, (2, 3)),
    }

    _current_difficulty = "medium"

    @classmethod
    def set_difficulty(cls, level):
        """Sets monster spawn difficulty for all future rooms."""
        cls._current_difficulty = level if level in cls._DIFFICULTY_TO_RANGE else "medium"

    # ──────────────────────────────────────────────────────────────
    def __init__(self, door_r: int, door_c: int, width: int = 25, height: int = 15):
        self.width  = width
        self.height = height
        self.grid = [["wall" for _ in range(width)] for _ in range(height)]
        self.hero_r = height - 2
        self.hero_c = width // 2
        self.door_r = height - 1
        self.door_c = width // 2
        self.is_trap = random.random() < 0.1
        self._carve_layout()
        self._spawn_pits()
        self._spawn_monsters()
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

        random.shuffle(Room.loot)
        Room.room_ID += 1

    # ───── Layout + Movement ─────
    def _carve_layout(self):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                if r == (self.height - 1) / 2 and c == (self.width - 1) / 2:
                    random.shuffle(self.loot)
                    self.grid[r][c] = Room.loot[0]
                    if Room.loot[0] in {"A", "E", "I", "P"}:
                        Room.loot.pop(0)
                else:
                    self.grid[r][c] = "floor"

        self.grid[self.door_r][self.door_c] = "door"
        self.grid[self.hero_r][self.hero_c] = "floor"

    # ──────────────────────────────────────────────────────────────
    def _spawn_pits(self):
        prob, (min_p, max_p) = Room._DIFFICULTY_TO_PIT[Room._current_difficulty]
        if random.random() > prob:
            return

        target = random.randint(min_p, max_p)
        placed = 0
        attempts = 0
        while placed < target and attempts < target * 25:
            attempts += 1
            r = random.randint(1, self.height - 2)
            c = random.randint(1, self.width  - 2)
            if self.grid[r][c] != "floor":
                continue
            if (r, c) in [(self.hero_r, self.hero_c), (self.door_r, self.door_c)]:
                continue
            self.grid[r][c] = "pit"
            placed += 1

    # ──────────────────────────────────────────────────────────────
    def _spawn_monsters(self):
        low, high = Room._DIFFICULTY_TO_RANGE[Room._current_difficulty]
        target = random.randint(low, high)
        self.monsters = {}
        attempts = 0
        while len(self.monsters) < target and attempts < target * 25:
            attempts += 1
            r = random.randint(1, self.height - 2)
            c = random.randint(1, self.width  - 2)
            if self.grid[r][c] != "floor":
                continue
            monster = MonsterFactory.create_random_monster()
            self.monsters[monster] = (r, c)

    # ──────────────────────────────────────────────────────────────
    def move_monsters(self):
        new_positions = {}
        occupied = set(self.monsters.values())
        occupied.add((self.hero_r, self.hero_c))

        # Difficulty level affects aggressiveness
        difficulty = Room._current_difficulty
        jitter_chance = {
            "easy": 0.6,
            "medium": 0.4,
            "hard": 0.2
        }[difficulty]

        for monster in list(self.monsters.keys()):
            r, c = self.monsters[monster]

            # Add random jitter to reduce clumping
            jitter = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
            random.shuffle(jitter)

            # Greedy direction toward hero
            dr = 1 if r < self.hero_r else -1 if r > self.hero_r else 0
            dc = 1 if c < self.hero_c else -1 if c > self.hero_c else 0

            best_pos = (r, c)
            best_dist = abs(r - self.hero_r) + abs(c - self.hero_c)

            for jdr, jdc in jitter:
                # Apply jitter based on difficulty
                if random.random() < jitter_chance:
                    jdr = random.choice([-1, 0, 1])
                    jdc = random.choice([-1, 0, 1])

                nr = r + dr + jdr
                nc = c + dc + jdc

                if (0 <= nr < self.height and 0 <= nc < self.width and
                        self.grid[nr][nc] in ["floor", "door"] and
                        (nr, nc) not in occupied):
                    dist = abs(nr - self.hero_r) + abs(nc - self.hero_c)
                    if dist < best_dist:
                        best_pos = (nr, nc)
                        best_dist = dist

            new_positions[monster] = best_pos
            occupied.add(best_pos)

        self.monsters = new_positions

    def move_hero_in_room(self, dx, dy, back_pack):
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
                back_pack.add(target)
                self.grid[nr][nc] = "floor"
                print("my back pack has",back_pack.to_string())
        return None

    def enter(self, hero):
        """Place hero at door and move monsters away from spawn point."""
        self.hero_r = self.door_r - 1
        self.hero_c = self.door_c

        # Define the danger zone (near the door)
        spawn_area = {
            (self.hero_r + dx, self.hero_c + dy)
            for dx in range(-2, 3)
            for dy in range(-2, 3)
            if 0 <= self.hero_r + dx < self.height and 0 <= self.hero_c + dy < self.width
        }

        # Find valid positions away from spawn zone
        safe_positions = [
            (r, c)
            for r in range(1, self.height - 1)
            for c in range(1, self.width - 1)
            if self.grid[r][c] in {"floor", "door"} and (r, c) not in spawn_area
        ]
        random.shuffle(safe_positions)

        # Reassign monster positions if they're in the danger zone
        new_monsters = {}
        for monster in self.monsters:
            current_pos = self.monsters[monster]
            if current_pos in spawn_area and safe_positions:
                new_monsters[monster] = safe_positions.pop()
            else:
                new_monsters[monster] = current_pos

        self.monsters = new_monsters

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