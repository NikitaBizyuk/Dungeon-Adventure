import unittest
from unittest.mock import patch, MagicMock
from model.MonsterFactory import MonsterFactory
from model.Ogre import Ogre
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin


class TestMonsterFactory(unittest.TestCase):

    @patch("sqlite3.connect")
    def test_load_monster_stats(self, mock_connect):
        # Mock DB rows
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("Ogre", 100, 2, 0.6, 30, 50, 0.1, 20, 40),
            ("Skeleton", 75, 3, 0.8, 15, 30, 0.2, 10, 25),
            ("Gremlin", 60, 4, 0.7, 10, 20, 0.15, 5, 15),
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Clear any previous state
        MonsterFactory._monster_stats = {}

        # Trigger load
        MonsterFactory._load_monster_stats()

        # Check dictionary population
        self.assertIn("Ogre", MonsterFactory._monster_stats)
        self.assertEqual(MonsterFactory._monster_stats["Skeleton"]["hp"], 75)
        self.assertEqual(MonsterFactory._monster_stats["Gremlin"]["damage_max"], 20)

    @patch.object(MonsterFactory, "_load_monster_stats")
    def test_create_known_monsters(self, mock_load):
        MonsterFactory._monster_stats = {
            "Ogre": {
                "hp": 100, "attack_speed": 2, "chance_to_hit": 0.6,
                "damage_min": 30, "damage_max": 50,
                "chance_to_heal": 0.1, "heal_min": 20, "heal_max": 40
            },
            "Skeleton": {
                "hp": 75, "attack_speed": 3, "chance_to_hit": 0.8,
                "damage_min": 15, "damage_max": 30,
                "chance_to_heal": 0.2, "heal_min": 10, "heal_max": 25
            },
            "Gremlin": {
                "hp": 60, "attack_speed": 4, "chance_to_hit": 0.7,
                "damage_min": 10, "damage_max": 20,
                "chance_to_heal": 0.15, "heal_min": 5, "heal_max": 15
            },
        }

        self.assertIsInstance(MonsterFactory.create("Ogre"), Ogre)
        self.assertIsInstance(MonsterFactory.create("Skeleton"), Skeleton)
        self.assertIsInstance(MonsterFactory.create("Gremlin"), Gremlin)

    def test_create_invalid_monster(self):
        MonsterFactory._monster_stats = {}
        with self.assertRaises(ValueError):
            MonsterFactory.create("Dragon")

    @patch.object(MonsterFactory, "create")
    @patch.object(MonsterFactory, "_load_monster_stats")
    def test_create_random_monster(self, mock_load, mock_create):
        MonsterFactory._monster_stats = {
            "Ogre": {},
            "Skeleton": {},
            "Gremlin": {},
        }
        mock_create.return_value = Ogre("Ogre", 100, 2, 0.6, 30, 50, 0.1, 20, 40)

        result = MonsterFactory.create_random_monster()
        self.assertIsInstance(result, Ogre)


if __name__ == "__main__":
    unittest.main()
