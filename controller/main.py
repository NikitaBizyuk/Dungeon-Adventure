from controller.dungeon_adventure import DungeonAdventure

game = DungeonAdventure()
game.startGame()

while True:
    key = input("Move (w/a/s/d): ")
    if key == "w":
        game.moveHero("up")
    elif key == "s":
        game.moveHero("down")
    elif key == "a":
        game.moveHero("left")
    elif key == "d":
        game.moveHero("right")
    elif key == "q":
        break
