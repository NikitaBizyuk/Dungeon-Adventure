import random

from model import Ogre, Skeleton, Gremlin
from model.monster import Monster

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
        skeleton = Skeleton(name)
        return skeleton

    @staticmethod
    def create_gremlin(name):
        return Gremlin(name)
