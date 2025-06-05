import random

from model.Ogre import Ogre
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin

class MonsterFactory:
    @staticmethod
    def create_random_monster(name = "MONSTER"):
        monster_classes = [Ogre, Skeleton, Gremlin]
        random_monster = random.choice(monster_classes)
        return random_monster(name)

    @staticmethod
    def create_ogre(name):
        return Ogre(name)

    @staticmethod
    def create_skeleton(name):
        my_skeleton = Skeleton(name)
        return my_skeleton

    @staticmethod
    def create_gremlin(name):
        return Gremlin(name)
