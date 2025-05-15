"""
from dungeon_adventure import DungeonAdventure
from model.dungeon import Dungeon
from model.warrior import Warrior
from model.Priestess import Priestess
from model.Thief import Thief
from model.dungeon import Dungeon
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.Skeleton import Skeleton



def main():

    my_gremlin = Gremlin("Gremlin",10,20,5,4,25)
    print( my_gremlin.to_String() + "\n")
    my_ogre = Ogre("Ogre", 50,24,72,90,30)
    my_skeleton = Skeleton("Skeleton",50,35,22,75,80)
    print(my_ogre.to_String() + "\n")
    print(my_skeleton.to_String() + "\n")

    my_warrior = Warrior("warrior",10,10,10,10)
    my_priestess = Priestess("Priestess",10,10,10,10)
    my_thief = Thief("thief",10,10,10,10)
    print(my_warrior.to_String() + "\n")
    print(my_priestess.to_String() + "\n")
    print(my_thief.to_String() + "\n")

    my_dungeon = Dungeon()
if __name__ == "__main__":
    main()

"""

from dungeon_adventure import DungeonAdventure

def main():
    game = DungeonAdventure()
    game.start_game()


if __name__ == "__main__":
    main()