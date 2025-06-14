import unittest
from unittest.mock import patch, MagicMock
from model.MonsterFactory import MonsterFactory

class TestMonsterFactory(unittest.TestCase):

    def setUp(self):
        self.mock_stats = {
            "Ogre": {
                "hp": 100, "attack_speed": 2, "chance_to_hit": 0.8,
                "damage_min": 10, "damage_max": 20,
                "chance_to_heal": 0.1, "heal_min": 5, "heal_max": 10
            }
        }

    @patch.object(MonsterFactory, "load_monster_stats")
    def test_create_known_monster(self, mock_load):
        MonsterFactory._monster_stats = self.mock_stats
        monster = MonsterFactory.create("Ogre")
        self.assertEqual(monster.name, "Ogre")
        self.assertEqual(monster.get_heal_points(), .1)

    @patch.object(MonsterFactory, "load_monster_stats")
    def test_create_unsupported_monster_raises(self, mock_load):
        MonsterFactory._monster_stats = {}
        with self.assertRaises(ValueError):
            MonsterFactory.create("Dragon")

    @patch.object(MonsterFactory, "load_monster_stats")
    def test_create_random_monster_returns_instance(self, mock_load):
        MonsterFactory._monster_stats = self.mock_stats
        monster = MonsterFactory.create_random_monster()
        self.assertTrue(monster.name in MonsterFactory._monster_stats)

    def tearDown(self):
        MonsterFactory._monster_stats = {}

