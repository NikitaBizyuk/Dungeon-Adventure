from model.dungeon import Dungeon
from model.warrior import Warrior

class DungeonAdventure:
    def __init__(self):
        self.dungeon = Dungeon(rows = 5, cols = 5)
        self.hero = Warrior("Rudy")
        self.hero_x = 0
        self.hero_y = 0
        self.dungeon.place_hero(self.hero, self.hero_x, self.hero_y)

    def move_hero(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dx = -1
        elif direction == "down":
            dx = 1
        elif direction == "left":
            dy = -1
        elif direction == "right":
            dy = 1

        new_x = max(0, min(self.hero_x + dx, self.dungeon.rows - 1))
        new_y = max(0, min(self.hero_y + dy, self.dungeon.cols - 1))

        self.hero_x, self.hero_y = new_x, new_y
        room = self.dungeon.get_room(self.hero_x, self.hero_y)
        room.enter(self.hero)

        self.print_hero_info()
        self.dungeon.print_dungeon()


    def print_hero_info(self):
        print(f"\n--- Hero Stats ---")
        print(f"Name: {self.hero.name}")
        print(f"HP: {self.hero.health_points}")
        print(f"Pillars Found: {self.hero.pillars_found}\n")

    def start_game(self):
        print("Game started! Use 'up', 'down', 'left', 'right' to move. Type 'quit' to exit.\n")
        while self.hero.health_points > 0:
            command = input("Move: ").strip().lower()
            if command == "quit":
                print("Thanks for playing!")
                break
            elif command in {"up", "down", "left", "right"}:
                self.move_hero(command)
            else:
                print("Invalid input. Try 'up', 'down', 'left', or 'right'.")
