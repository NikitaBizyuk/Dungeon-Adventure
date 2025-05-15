from model.room import Room

class Dungeon:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.rooms = [[Room(row, col) for col in range(cols)] for row in range(rows)]

    def place_hero(self, hero, x, y):
        self.rooms[x][y].enter(hero)

    def get_room(self, x, y):
        return self.rooms[x][y]