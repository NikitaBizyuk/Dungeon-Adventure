import random
from model.room import Room
from model.maze_cell import MazeCell

class Dungeon:
    def __init__(self, rows=11, cols=11):
        self.rows = rows
        self.cols = cols
        self.maze = [[MazeCell(r, c, "wall") for c in range(cols)] for r in range(rows)]
        self.rooms = {}  # door_id -> Room
        self.hero_x = 1  # should be a hallway
        self.hero_y = 1
        self.in_room = False
        self._generate_simple_maze()
        self._place_doors_and_rooms()
        self.in_room = False
        self.active_room = None

    def _generate_simple_maze(self):
        # Simple DFS maze generation for now
        def carve_passages(cx, cy):
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)
            self.maze[cx][cy].cell_type = "hallway"

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < self.rows - 1 and 1 <= ny < self.cols - 1:
                    if self.maze[nx][ny].cell_type == "wall":
                        self.maze[cx + dx // 2][cy + dy // 2].cell_type = "hallway"  # carve connection
                        carve_passages(nx, ny)

        carve_passages(1, 1)

    def _place_doors_and_rooms(self):
        door_id = 0
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                if self.maze[r][c].cell_type == "hallway" and random.random() < 0.1:
                    # place door to side
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if self.maze[nr][nc].cell_type == "wall":
                            self.maze[nr][nc].cell_type = "door"
                            self.maze[nr][nc].door_id = door_id
                            self.rooms[door_id] = Room(nr, nc)
                            door_id += 1
                            break

    def get_hero_cell(self):
        return self.maze[self.hero_x][self.hero_y]

    def move_hero(self, dx, dy):
        nx, ny = self.hero_x + dx, self.hero_y + dy
        if 0 <= nx < self.rows and 0 <= ny < self.cols:
            target = self.maze[nx][ny]
            if target.cell_type in ["hallway", "door"]:
                self.hero_x, self.hero_y = nx, ny
                if target.cell_type == "door":
                    room = self.rooms[target.door_id]
                    room.enter(None)
                    self.in_room = True
                    self.active_room = room
                    print(f"Entered room at door {target.door_id}")

    def draw_maze(self, screen, cell_size):
        import pygame
        colors = {
            "wall": (40, 40, 40),
            "hallway": (200, 200, 200),
            "door": (0, 128, 255)
        }
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
                cell = self.maze[r][c]
                pygame.draw.rect(screen, colors[cell.cell_type], rect)
                if r == self.hero_x and c == self.hero_y:
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, cell_size // 3)

    def print_text_maze(self):
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                cell = self.maze[r][c]
                if r == self.hero_x and c == self.hero_y:
                    row += "H"
                elif cell.cell_type == "wall":
                    row += "#"
                elif cell.cell_type == "hallway":
                    row += " "
                elif cell.cell_type == "door":
                    row += "D"
            print(row)
