import sqlite3
import random
import os
from model.Ogre import Ogre
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Monster import Monster

class MonsterFactory:
    _monster_stats: dict[str, dict] = {}

    @classmethod
    def _load_monster_stats(cls) -> None:
        """Load monster stats from SQLite database into class-level dictionary."""
        if cls._monster_stats:
            return  # Already loaded

        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "monsters.db"))
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM monsters")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            name, hp, speed, hit, dmg_min, dmg_max, heal_chance, heal_min, heal_max = row
            cls._monster_stats[name] = {
                "hp": hp,
                "attack_speed": speed,
                "chance_to_hit": hit,
                "damage_min": dmg_min,
                "damage_max": dmg_max,
                "chance_to_heal": heal_chance,
                "heal_min": heal_min,
                "heal_max": heal_max
            }

    @classmethod
    def create(cls, name: str) -> Monster:
        """Create a monster instance by name using loaded stats."""
        cls._load_monster_stats()
        stats = cls._monster_stats.get(name)

        if not stats:
            raise ValueError(f"No stats found for monster: {name}")

        if name == "Ogre":
            return Ogre(name, **stats)
        elif name == "Gremlin":
            return Gremlin(name, **stats)
        elif name == "Skeleton":
            return Skeleton(name, **stats)
        else:
            raise ValueError(f"Unsupported monster type: {name}")

    @classmethod
    def create_random_monster(cls) -> Monster:
        """Randomly select a monster type and return an instance."""
        cls._load_monster_stats()
        monster_type = random.choice(list(cls._monster_stats.keys()))
        return cls.create(monster_type)
