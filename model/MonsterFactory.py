import random

from model import Ogre, Skeleton, Gremlin
from model.monster import Monster

class MonsterFactory():
    @staticmethod
    def create_random_monster():
        monster_classes = [Ogre, Skeleton, Gremlin]
        return random.choice(monster_classes)()
    @staticmethod
    def create_Ogre():
        return Ogre

    @staticmethod
    def create_Skeleton():
        return Skeleton

    @staticmethod
    def create_Gremlin():
        return Gremlin