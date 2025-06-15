import random
from model.Room import Room
from model.MazeCell import MazeCell
from model.OOPillars import OOPillars


class Dungeon:
    def __init__(self, difficulty="medium"):
        self._difficulty = difficulty.lower()
        self._rows, self._cols, self._room_count = self._configure_difficulty(self._difficulty)

        self._maze = []
        self._rooms = {}
        self._hero_x = 0
        self._hero_y = 0
        self._in_room = False
        self._active_room = None
        self._room_exit_point = None
        self._room_centers = []
        self._room_templates = self._define_room_templates()

        self._generate_maze_with_valid_rooms()
        self._place_exit()
        self._place_hero_start()
        self.update_visibility()
        self._place_pillars()

    def _configure_difficulty(self, difficulty):
        if difficulty == "easy":
            return 41, 41, 8
        elif difficulty == "hard":
            return 81, 81, 25
        else:
            return 61, 61, 15

    def _define_room_templates(self):
        return [(3, 3), (5, 5), (3, 5), (5, 3), (4, 6), (6, 4), (6, 6), (4, 4)]

    def _generate_maze_with_valid_rooms(self):
        for _ in range(5):
            self._maze = [[MazeCell(r, c) for c in range(self._cols)] for r in range(self._rows)]
            self._rooms = {}
            self._room_centers = []

            self._generate_handcrafted_layout()
            self._place_doors()

            if len(self._rooms) >= 4:
                return

        raise Exception("Failed to generate enough rooms with doors.")

    def _generate_handcrafted_layout(self):
        for r in range(self._rows):
            for c in range(self._cols):
                self._maze[r][c].cell_type = "wall"

        placed = 0
        attempts = 0
        while placed < self._room_count and attempts < self._room_count * 10:
            h, w = random.choice(self._room_templates)
            top = random.randint(2, self._rows - h - 2)
            left = random.randint(2, self._cols - w - 2)
            if self._can_place_room(top, left, h, w):
                self._carve_room(top, left, h, w)
                self._room_centers.append((top + h // 2, left + w // 2))
                placed += 1
            attempts += 1

        self._connect_rooms_with_path()

    def _can_place_room(self, top, left, height, width):
        for r in range(top - 1, top + height + 1):
            for c in range(left - 1, left + width + 1):
                if self._maze[r][c].cell_type != "wall":
                    return False
        return True

    def _carve_room(self, top, left, height, width):
        for r in range(top, top + height):
            for c in range(left, left + width):
                self._maze[r][c].cell_type = "hallway"

    def _connect_rooms_with_path(self):
        random.shuffle(self._room_centers)
        connected = [self._room_centers[0]]
        for target in self._room_centers[1:]:
            closest = min(connected, key=lambda rc: abs(rc[0] - target[0]) + abs(rc[1] - target[1]))
            self._carve_path(closest, target)
            connected.append(target)

    def _carve_path(self, start, end):
        x1, y1 = start
        x2, y2 = end
        if random.random() < 0.5:
            self._carve_hallway(x1, y1, x2, y1)
            self._carve_hallway(x2, y1, x2, y2)
        else:
            self._carve_hallway(x1, y1, x1, y2)
            self._carve_hallway(x1, y2, x2, y2)

    def _carve_hallway(self, r1, c1, r2, c2):
        for r in range(min(r1, r2), max(r1, r2) + 1):
            for i in range(-1, 2):
                if 0 <= r < self._rows and 0 <= c1 + i < self._cols:
                    self._maze[r][c1 + i].cell_type = "hallway"
        for c in range(min(c1, c2), max(c1, c2) + 1):
            for i in range(-1, 2):
                if 0 <= r1 + i < self._rows and 0 <= c < self._cols:
                    self._maze[r1 + i][c].cell_type = "hallway"

    def _place_doors(self):
        door_id = 0
        for r, c in self._room_centers:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr * 2, c + dc * 2
                if 0 <= nr < self._rows and 0 <= nc < self._cols and self._maze[nr][nc].cell_type == "wall":
                    self._maze[nr][nc].cell_type = "door"
                    self._maze[nr][nc].door_id = door_id
                    self._rooms[door_id] = Room(nr, nc)
                    self._rooms[door_id].place_random_loot()
                    door_id += 1
                    break

    def _place_exit(self):
        r, c = self._room_centers[-1]
        self._maze[r][c].cell_type = "exit"

    def _place_hero_start(self):
        self._hero_x, self._hero_y = self._room_centers[0]

    def _place_pillars(self):
        pillar_symbols = [
            OOPillars.ABSTRACTION.symbol,
            OOPillars.ENCAPSULATION.symbol,
            OOPillars.INHERITANCE.symbol,
            OOPillars.POLYMORPHISM.symbol
        ]
        selected_rooms = random.sample(list(self._rooms.values()), 4)
        for room, symbol in zip(selected_rooms, pillar_symbols):
            room.place_item(symbol)

    def update_visibility(self):
        radius = 6
        for r in range(self._rows):
            for c in range(self._cols):
                self._maze[r][c].visible = False
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = self._hero_x + dx
                y = self._hero_y + dy
                if 0 <= x < self._rows and 0 <= y < self._cols:
                    self._maze[x][y].visible = True
                    self._maze[x][y].explored = True

    def move_hero_in_room(self, dx, dy, backpack, view=None):
        if self._in_room:
            status = self._active_room.move_hero_in_room(dx, dy, backpack, view)
            self._active_room.move_monsters()
            if status == "exit":
                # Move hero one tile away from door after exiting
                if self._room_exit_point:
                    ex, ey = self._room_exit_point
                    dx, dy = 0, 0
                    if self._maze[ex - 1][ey].cell_type != "wall":
                        dx = -1
                    elif self._maze[ex + 1][ey].cell_type != "wall":
                        dx = 1
                    elif self._maze[ex][ey - 1].cell_type != "wall":
                        dy = -1
                    elif self._maze[ex][ey + 1].cell_type != "wall":
                        dy = 1
                    self._hero_x, self._hero_y = ex + dx, ey + dy
                self._in_room = False
                if hasattr(self, "hero") and self.hero:
                    self.hero.getting_hit = False
                self._active_room = None
                self.update_visibility()
        else:
            nx, ny = self._hero_x + dx, self._hero_y + dy
            if 0 <= nx < self._rows and 0 <= ny < self._cols:
                tile = self._maze[nx][ny]
                if tile.cell_type in ["hallway", "door", "exit"]:
                    self._hero_x, self._hero_y = nx, ny
                    self.update_visibility()
                    if tile.cell_type == "door":
                        room = self._rooms[tile.door_id]
                        self._room_exit_point = (self._hero_x, self._hero_y)
                        room.enter(self)
                        self._in_room = True
                        self._active_room = room
                        print(f"Entered room at door {tile.door_id}")
                    elif tile.cell_type == "exit":
                        print("Reached exit!")

    # ────── Properties for External Access ──────
    @property
    def maze(self): return self._maze

    @property
    def hero_x(self): return self._hero_x

    @property
    def hero_y(self): return self._hero_y

    @property
    def in_room(self): return self._in_room

    @in_room.setter
    def in_room(self, value): self._in_room = value

    @property
    def active_room(self): return self._active_room

    @property
    def rooms(self): return self._rooms

    @property
    def rows(self): return self._rows

    @property
    def cols(self): return self._cols
