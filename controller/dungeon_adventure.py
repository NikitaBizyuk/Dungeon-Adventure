from model.dungeon import Dungeon
from model.room import Room
from model.warrior import Warrior  # or Hero base class if no subclass yet

class DungeonAdventure:
    def __init__(self):
        self.myDungeon = Dungeon()
        self.myHero = Warrior("Rudy")  # Example hero
        self.myHeroX = 0  # Start location
        self.myHeroY = 0

    def moveHero(self, direction):
        if direction == "up":
            self.myHeroX -= 1
        elif direction == "down":
            self.myHeroX += 1
        elif direction == "left":
            self.myHeroY -= 1
        elif direction == "right":
            self.myHeroY += 1

        # Bounds check
        self.myHeroX = max(0, min(self.myHeroX, len(self.myDungeon.myRooms) - 1))
        self.myHeroY = max(0, min(self.myHeroY, len(self.myDungeon.myRooms[0]) - 1))

        currentRoom = self.myDungeon.getRoom(self.myHeroX, self.myHeroY)
        currentRoom.enter(self.myHero)

        self.printHeroInfo()

    def printHeroInfo(self):
        print(f"HP: {self.myHero.getHitPoints()}")
        print(f"Healing potions: {self.myHero.getNumHealingPotions()}")
        print(f"Vision potions: {self.myHero.getNumVisionPotions()}")
        print(f"Pillars found: {self.myHero.getPillarsFound()}")

    def startGame(self):
        print("Game started! Use arrow keys to move.")
