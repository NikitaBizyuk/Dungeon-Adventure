
from model.dungeon import Dungeon
from model.warrior import Warrior

class DungeonAdventure:
    def __init__(self, view_rows=15, view_cols=15):
        self.dungeon = Dungeon(rows=51, cols=51, view_rows=view_rows, view_cols=view_cols)
        self.hero = Warrior("Rudy")
        self.in_room = False
        self.active_room = None

    def move_hero(self, dx, dy):
        if not self.in_room:
            self.dungeon.move_hero(dx, dy)
            if self.dungeon.in_room:
                self.in_room = True
                self.active_room = self.dungeon.active_room

    def exit_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None