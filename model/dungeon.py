import random
from model.room import Room

class Dungeon:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.rooms = [[Room(r, c) for c in range(cols)] for r in range(rows)]
        self.entrance = (0, 0)
        self.exit = (rows - 1, cols - 1)
        self._generate_maze(0, 0)
        self._place_special_rooms()

    def _generate_maze(self, r, c):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)
        self.rooms[r][c].visited = True

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.rooms[nr][nc].visited:
                self._generate_maze(nr, nc)

    def _place_special_rooms(self):
        # Place entrance and exit
        self.rooms[0][0].is_entrance = True
        self.rooms[self.exit[0]][self.exit[1]].is_exit = True

        # Place 4 pillars randomly
        pillars = ['A', 'E', 'I', 'P']
        placed = 0
        while placed < 4:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            room = self.rooms[r][c]
            if not room.is_entrance and not room.is_exit and room.pillar is None:
                room.pillar = pillars[placed]
                placed += 1

    def get_room(self, row, col):
        return self.rooms[row][col]

    def place_hero(self, hero, x, y):
        # Clear previous hero markers
        for row in self.rooms:
            for room in row:
                room.has_hero = False
        self.rooms[x][y].enter(hero)

    def print_dungeon(self):
        for r in range(self.rows):
            # Top walls (*** for boundary, *-* for internal)
            top_line = ""
            mid_line = ""
            bot_line = ""
            for c in range(self.cols):
                top_line += "*-*   "
                mid_line += f"|{self.rooms[r][c].display_center()}|   "
                bot_line += "*-*   "
            print(top_line)
            print(mid_line)
            print(bot_line + "\n")