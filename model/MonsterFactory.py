import sqlite3
import random
import os
from model.Ogre import Ogre
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin

class MonsterFactory:
    _monster_stats = {}

    @staticmethod
    def load_monster_stats():
        if MonsterFactory._monster_stats:
            return  # already loaded

        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "monsters.db"))
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT * FROM monsters")
        rows = c.fetchall()

        for row in rows:
            name, hp, speed, hit, dmg_min, dmg_max, heal_chance, heal_min, heal_max = row
            MonsterFactory._monster_stats[name] = {
                "hp": hp,
                "attack_speed": speed,
                "chance_to_hit": hit,
                "damage_min": dmg_min,
                "damage_max": dmg_max,
                "chance_to_heal": heal_chance,
                "heal_min": heal_min,
                "heal_max": heal_max
            }

        conn.close()

    @staticmethod
    def create(name):
        MonsterFactory.load_monster_stats()
        stats = MonsterFactory._monster_stats.get(name)
        if not stats:
            raise ValueError(f"No stats found for monster: {name}")

        if name == "Ogre":
            return Ogre(
                name,
                stats["hp"],
                stats["attack_speed"],
                stats["chance_to_hit"],
                stats["damage_min"],
                stats["damage_max"],
                stats["chance_to_heal"],
                stats["heal_min"],
                stats["heal_max"]
            )
        elif name == "Gremlin":
            return Gremlin(
                name,
                stats["hp"],
                stats["attack_speed"],
                stats["chance_to_hit"],
                stats["damage_min"],
                stats["damage_max"],
                stats["chance_to_heal"],
                stats["heal_min"],
                stats["heal_max"]
            )
        elif name == "Skeleton":
            return Skeleton(
                name,
                stats["hp"],
                stats["attack_speed"],
                stats["chance_to_hit"],
                stats["damage_min"],
                stats["damage_max"],
                stats["chance_to_heal"],
                stats["heal_min"],
                stats["heal_max"]
            )
        else:
            raise ValueError(f"Unsupported monster type: {name}")

    @staticmethod
    def create_random_monster():
        MonsterFactory.load_monster_stats()
        monster_type = random.choice(list(MonsterFactory._monster_stats.keys()))
        return MonsterFactory.create(monster_type)
