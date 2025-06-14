import unittest
from model.Thief import Thief
from model.Warrior import Warrior
from model.Priestess import Priestess


class TestDungeonCharacterViaHeroes(unittest.TestCase):

    def setUp(self):
        self.thief = Thief("Tess")
        self.warrior = Warrior("Walt")
        self.priestess = Priestess("Paula")

    def test_get_status(self):
        self.assertEqual(self.thief.get_status(), f"Tess: {self.thief.health_points} HP")
        self.assertEqual(self.warrior.get_status(), f"Walt: {self.warrior.health_points} HP")
        self.assertEqual(self.priestess.get_status(), f"Paula: {self.priestess.health_points} HP")

    def test_is_alive_true_and_false(self):
        self.assertTrue(self.thief.is_alive())
        self.thief.health_points = 0
        self.assertFalse(self.thief.is_alive())

    def test_properties_access(self):
        for hero in [self.thief, self.warrior, self.priestess]:
            self.assertIsInstance(hero.name, str)
            self.assertIsInstance(hero.health_points, int)
            self.assertIsInstance(hero.damage_min, int)
            self.assertIsInstance(hero.damage_max, int)
            self.assertIsInstance(hero.attack_speed, int)
            self.assertIsInstance(hero.chance_to_hit, float if isinstance(hero.chance_to_hit, float) else int)

    def test_health_points_never_negative(self):
        self.warrior.health_points = -100
        self.assertEqual(self.warrior.health_points, 0)

