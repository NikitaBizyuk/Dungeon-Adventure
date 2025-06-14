import random
from model.MonsterFactory import MonsterFactory

<<<<<<< Updated upstream
class Room:
    # ───── Static class-level values ─────
    room_ID = 0
    loot = ["Encapsulation", "Abstraction", "Polymorphism",
            "Inheritance", "Health Potion", "Vision Potion"]
=======
>>>>>>> Stashed changes

class Room:
    # ──────────────────────────────────────────────────────────────
    room_ID = 0
    loot = ["A", "E", "I", "P", "Health Potion", "Vision Potion"]

    _DIFFICULTY_TO_MONSTER_RANGE = {
        "easy":   (1, 3),
        "medium": (4, 7),
        "hard":   (8, 10),
    }
    _DIFFICULTY_TO_PIT = {
        "easy":   (0.15, (0, 1)),
        "medium": (0.45, (1, 2)),
        "hard":   (0.75, (2, 3)),
    }

    _current_difficulty = "medium"

    # ──────────────────────────────────────────────────────────────
    @classmethod
    def set_difficulty(cls, level: str):
        cls._current_difficulty = (
            level if level in cls._DIFFICULTY_TO_MONSTER_RANGE else "medium"
        )

    # ──────────────────────────────────────────────────────────────
    def __init__(self, door_r: int, door_c: int, width: int = 25, height: int = 15):
        self.width  = width
        self.height = height
        self.grid   = [["wall" for _ in range(width)] for _ in range(height)]

        self.hero_r = height - 2
        self.hero_c = width  // 2
        self.door_r = height - 1
<<<<<<< Updated upstream
        self.door_c = width // 2
=======
        self.door_c = width  // 2
>>>>>>> Stashed changes

        self._carve_layout()
        self._spawn_pits()
        self._spawn_monsters()
        Room.room_ID += 1

    # ──────────────────────────────────────────────────────────────
    def _carve_layout(self):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
<<<<<<< Updated upstream
                if r == (self.height - 1) / 2 and c == (self.width - 1) / 2:
=======
                if r == (self.height - 1) // 2 and c == (self.width - 1) // 2:
                    random.shuffle(Room.loot)
>>>>>>> Stashed changes
                    self.grid[r][c] = Room.loot[0]
                    if Room.loot[0] in {"Encapsulation", "Abstraction", "Polymorphism", "Inheritance"}:
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
        low, high = Room._DIFFICULTY_TO_MONSTER_RANGE[Room._current_difficulty]
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
        new_pos  = {}
        occupied = set(self.monsters.values())
        occupied.add((self.hero_r, self.hero_c))

        for m in list(self.monsters):
            r, c = self.monsters[m]
            dr = 1 if r < self.hero_r else -1 if r > self.hero_r else 0
            dc = 1 if c < self.hero_c else -1 if c > self.hero_c else 0
            nr, nc = r + dr, c + dc

            if (0 <= nr < self.height and 0 <= nc < self.width and
                    self.grid[nr][nc] in ["floor", "door"] and
                    (nr, nc) not in occupied):
                new_pos[m] = (nr, nc)
                occupied.add((nr, nc))
            else:
                new_pos[m] = (r, c)

        self.monsters = new_pos

<<<<<<< Updated upstream
    def move_hero_in_room(self, dx, dy):
        nr = self.hero_r + dx
        nc = self.hero_c + dy

        if 0 <= nr < self.height and 0 <= nc < self.width:
            target = self.grid[nr][nc]
            if any((nr, nc) == (mr, mc) for (mr, mc) in self.monsters.values()):
                return None
            if target in ["floor", "door"]:
                self.hero_r = nr
                self.hero_c = nc
                if target == "door":
                    return "exit"
=======
    # ──────────────────────────────────────────────────────────────
    def move_hero_in_room(self, dx: int, dy: int, backpack):
        nr, nc = self.hero_r + dx, self.hero_c + dy
        if not (0 <= nr < self.height and 0 <= nc < self.width):
            return None

        tile = self.grid[nr][nc]
        if any((nr, nc) == pos for pos in self.monsters.values()):
            return None

        if tile in [
            "floor", "door", "pit",
            "A", "E", "I", "P",
            "Health Potion", "Vision Potion",
        ]:
            self.hero_r, self.hero_c = nr, nc
            if tile == "door":
                return "exit"
            if tile == "pit":
                return "pit"
            if tile in {"A", "E", "I", "P", "Health Potion", "Vision Potion"}:
                backpack.add(tile)
                self.grid[nr][nc] = "floor"
>>>>>>> Stashed changes
        return None

    # ──────────────────────────────────────────────────────────────
    def reset_hero_start(self):
        """Call when hero first enters (or re-enters) the room."""
        self.hero_r = self.height - 2
        self.hero_c = self.width  // 2

    # ──────────────────────────────────────────────────────────────
    # Accessors
    # ──────────────────────────────────────────────────────────────
    def get_tile(self, r, c):            return self.grid[r][c]
    def get_hero_position(self):         return self.hero_r, self.hero_c
    def get_dimensions(self):            return self.height, self.width
    def get_monsters(self):              return self.monsters
    def get_monster_at(self, r, c):
        for m, (mr, mc) in self.monsters.items():
            if (mr, mc) == (r, c):
                return m
        return None