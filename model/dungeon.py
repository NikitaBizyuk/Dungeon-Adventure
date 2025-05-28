import random
from model.room import Room
from model.maze_cell import MazeCell

class Dungeon:
    def __init__(self, rows=61, cols=61, view_rows=15, view_cols=15, difficulty="large"):
        self.rows = rows
        self.cols = cols
        self.maze = [[MazeCell(r, c) for c in range(cols)] for r in range(rows)]
        self.rooms = {}
        self.hero_x = 0
        self.hero_y = 0
        self.in_room = False
        self.active_room = None
        self.view_rows = view_rows
        self.view_cols = view_cols
        self.room_exit_point = None

        self.room_count = 8 if difficulty == "small" else 20
        self.room_templates = self._define_room_templates()
        self.room_centers = []

        self._generate_handcrafted_layout()
        self._place_doors()
        self._place_exit()
        self._place_hero_start()
        self.update_visibility()

    def _define_room_templates(self):
        return [
            (3, 3), (5, 5), (3, 5), (5, 3), (4, 6), (6, 4),
            (6, 6), (4, 4),
        ]

    def _generate_handcrafted_layout(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.maze[r][c].cell_type = "wall"

        placed_rooms = 0
        attempts = 0

        while placed_rooms < self.room_count and attempts < self.room_count * 10:
            attempts += 1
            h, w = random.choice(self.room_templates)
            top = random.randint(2, self.rows - h - 2)
            left = random.randint(2, self.cols - w - 2)

            if self._can_place_room(top, left, h, w):
                self._carve_room(top, left, h, w)
                self.room_centers.append((top + h // 2, left + w // 2))
                placed_rooms += 1

        self._connect_rooms_with_path()

    def _can_place_room(self, top, left, height, width):
        for r in range(top - 1, top + height + 1):
            for c in range(left - 1, left + width + 1):
                if self.maze[r][c].cell_type != "wall":
                    return False
        return True

    def _carve_room(self, top, left, height, width):
        for r in range(top, top + height):
            for c in range(left, left + width):
                self.maze[r][c].cell_type = "hallway"

    def _connect_rooms_with_path(self):
        random.shuffle(self.room_centers)
        connected = [self.room_centers[0]]
        for target in self.room_centers[1:]:
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
                if 0 <= r < self.rows and 0 <= c1 + i < self.cols:
                    self.maze[r][c1 + i].cell_type = "hallway"
        for c in range(min(c1, c2), max(c1, c2) + 1):
            for i in range(-1, 2):
                if 0 <= r1 + i < self.rows and 0 <= c < self.cols:
                    self.maze[r1 + i][c].cell_type = "hallway"

    def _place_hero_start(self):
        self.hero_x, self.hero_y = self.room_centers[0]

    def _place_doors(self):
        door_id = 0
        for r, c in self.room_centers:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr * 2, c + dc * 2
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr][nc].cell_type == "wall":
                    self.maze[nr][nc].cell_type = "door"
                    self.maze[nr][nc].door_id = door_id
                    self.rooms[door_id] = Room(nr, nc)
                    door_id += 1
                    break

    def _place_exit(self):
        farthest = self.room_centers[-1]
        self.maze[farthest[0]][farthest[1]].cell_type = "exit"

    def update_visibility(self):
        radius = 6
        for r in range(self.rows):
            for c in range(self.cols):
                self.maze[r][c].visible = False

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = self.hero_x + dx
                y = self.hero_y + dy
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    self.maze[x][y].visible = True
                    self.maze[x][y].explored = True

    def move_hero(self, dx, dy):
        if self.in_room:
            status = self.active_room.move_hero_in_room(dx, dy)
            if status == "exit":
                self.in_room = False
                self.active_room = None
        else:
            nx, ny = self.hero_x + dx, self.hero_y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                target = self.maze[nx][ny]
                if target.cell_type in ["hallway", "door", "exit"]:
                    self.hero_x, self.hero_y = nx, ny
                    self.update_visibility()
                    if target.cell_type == "door":
                        room = self.rooms[target.door_id]
                        self.in_room = True
                        self.active_room = room
                        print(f"Entered room at door {target.door_id}")
                    elif target.cell_type == "exit":
                        print("Reached exit!")
