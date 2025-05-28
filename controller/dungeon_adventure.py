from model.dungeon import Dungeon
from model.warrior import Warrior

class DungeonAdventure:
    def __init__(self):
        self.dungeon = Dungeon(rows=61, cols=61, difficulty="large")
        self.hero = Warrior("Rudy")
        self.in_room = False
        self.active_room = None

    def move_hero(self, dx, dy):
        if self.dungeon.in_room:
            status = self.dungeon.active_room.move_hero_in_room(dx, dy)
            if status == "exit":
                self.dungeon.in_room = False
                self.dungeon.active_room = None
                self.in_room = False
                self.active_room = None
        else:
            self.dungeon.move_hero(dx, dy)
            if self.dungeon.in_room:
                self.in_room = True
                self.active_room = self.dungeon.active_room

    def exit_room(self):
        self.in_room = False
        self.dungeon.in_room = False
        self.active_room = None
