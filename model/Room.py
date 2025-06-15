import random
from model.MonsterFactory import MonsterFactory
import heapq
from model.pathfinding import a_star_search

class Room:
    _room_id = 0
    _current_difficulty = "medium"
    _DIFFICULTY_TO_RANGE = {
        "easy": (1, 3),
        "medium": (4, 7),
        "hard": (8, 10),
    }

    @classmethod
    def set_difficulty(cls, level):
        if level in cls._DIFFICULTY_TO_RANGE:
            cls._current_difficulty = level

    def __init__(self, door_r, door_c, width=25, height=15):
        self._width = width
        self._height = height
        self._grid = [["wall" for _ in range(width)] for _ in range(height)]

        self._door_r = height - 1
        self._door_c = width // 2
        self._hero_r = height - 2
        self._hero_c = width // 2
        self._is_trap = random.random() < 0.1

        self._carve_layout()
        self.place_random_pits()

        low, high = Room._DIFFICULTY_TO_RANGE[Room._current_difficulty]
        self._num_monsters = random.randint(low, high)

        self._monsters = {
            MonsterFactory.create_random_monster(): (
                random.randint(1, height - 2),
                random.randint(1, width - 2)
            )
            for _ in range(self._num_monsters)
        }

        Room._room_id += 1

    def _carve_layout(self):
        for r in range(1, self._height - 1):
            for c in range(1, self._width - 1):
                self._grid[r][c] = "floor"
        self._grid[self._door_r][self._door_c] = "door"
        self._grid[self._hero_r][self._hero_c] = "floor"

    def place_item(self, item_symbol):
        empty_tiles = [
            (r, c)
            for r in range(1, self._height - 1)
            for c in range(1, self._width - 1)
            if self._grid[r][c] == "floor"
        ]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self._grid[r][c] = item_symbol

    def place_random_loot(self):
        loot_candidates = []
        if random.random() < 0.6:
            loot_candidates.append("Health Potion")
        if random.random() < 0.5:
            loot_candidates.append("Vision Potion")

        for item in loot_candidates:
            self.place_item(item)

    def place_random_pits(self):
        num_pits = random.randint(1, 3)
        placed = 0
        while placed < num_pits:
            r = random.randint(1, self._height - 2)
            c = random.randint(1, self._width - 2)
            if self._grid[r][c] == "floor":
                self._grid[r][c] = "pit"
                placed += 1


    def move_monsters(self):
        new_positions = {}
        occupied = set(self._monsters.values())
        occupied.add((self._hero_r, self._hero_c))

        for monster in list(self._monsters.keys()):
            start = self._monsters[monster]
            goal = (self._hero_r, self._hero_c)

            path = a_star_search(self._grid, start, goal)
            moved = False

            # Move one step if path exists
            if path:
                next_step = path[0]
                if next_step not in occupied:
                    new_positions[monster] = next_step
                    moved = next_step != start
                    occupied.add(next_step)
                else:
                    new_positions[monster] = start
            else:
                new_positions[monster] = start

            monster.set_position(*new_positions[monster])

            # Flip facing
            dx = new_positions[monster][1] - start[1]
            if hasattr(monster, "facing_right"):
                if dx < 0:
                    monster.facing_right = False
                elif dx > 0:
                    monster.facing_right = True

            # Animation logic
            if hasattr(monster, "is_attacking") and monster.is_attacking():
                monster.current_animation = "slashing"
            elif moved:
                monster.current_animation = "running"
            else:
                monster.current_animation = "idle"

        self._monsters = new_positions

    def move_hero_in_room(self, dx, dy, backpack, view=None):
        nr = self._hero_r + dx
        nc = self._hero_c + dy

        if 0 <= nr < self._height and 0 <= nc < self._width:
            target = self._grid[nr][nc]

            if any((nr, nc) == (mr, mc) for (mr, mc) in self._monsters.values()):
                return None

            if target == "pit":
                self._hero_r = nr
                self._hero_c = nc
                print("💥 You fell into a pit!")  # This is fine
                return "pit"  # ✅ Correct – doesn't overwrite grid

            elif target in ["floor", "door", "A", "E", "I", "P", "Health Potion", "Vision Potion"]:
                self._hero_r = nr
                self._hero_c = nc

                if target == "door":
                    if Room._current_difficulty == "easy":
                        return "exit"
                    elif not self._monsters:
                        return "exit"
                    else:
                        if view:
                            view.display_message("❌ Defeat all monsters to exit!", 2000)
                        return None  # Prevent exiting while monsters are alive


                if target in ["A", "E", "I", "P", "Health Potion", "Vision Potion"]:
                    backpack.add(target, view)
                    self._grid[nr][nc] = "floor"
                    print("🎒 Backpack now contains:", backpack.to_string())

        return None

    def enter(self, hero):
        """Place hero just inside the door and move monsters away from the spawn area."""
        self._hero_r = self._door_r
        self._hero_c = self._door_c

        # Step the hero into the room (away from door depending on where door is)
        if self._door_r == 0:  # Top door
            self._hero_r += 1
        elif self._door_r == self._height - 1:  # Bottom door
            self._hero_r -= 1
        elif self._door_c == 0:  # Left door
            self._hero_c += 1
        elif self._door_c == self._width - 1:  # Right door
            self._hero_c -= 1

        spawn_area = {
            (self._hero_r + dx, self._hero_c + dy)
            for dx in range(-2, 3)
            for dy in range(-2, 3)
            if 0 <= self._hero_r + dx < self._height and 0 <= self._hero_c + dy < self._width
        }

        safe_positions = [
            (r, c)
            for r in range(1, self._height - 1)
            for c in range(1, self._width - 1)
            if self._grid[r][c] in {"floor", "door"} and (r, c) not in spawn_area
        ]
        random.shuffle(safe_positions)

        new_monsters = {}
        for monster in self._monsters:
            current_pos = self._monsters[monster]
            if current_pos in spawn_area and safe_positions:
                new_monsters[monster] = safe_positions.pop()
            else:
                new_monsters[monster] = current_pos

        self._monsters = new_monsters

    # ───── Accessors ─────

    def get_tile(self, r, c):
        return self._grid[r][c]

    def get_hero_position(self):
        return self._hero_r, self._hero_c

    def get_dimensions(self):
        return self._height, self._width

    def get_monsters(self):
        return self._monsters

    def get_monster_at(self, r, c):
        for monster, (mr, mc) in self._monsters.items():
            if (mr, mc) == (r, c):
                return monster
        return None

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def monsters(self):
        return self._monsters

    def to_string(self):
        result = ""
        for r in range(self._height):
            for c in range(self._width):
                if r == 0 or r == self._height - 1:
                    result += "*"
                elif c == 0 or c == self._width - 1:
                    result += "*"
                elif c == self._door_c and r == self._door_r:
                    result += "_"
                else:
                    result += " "
            result += "\n"
        return result
