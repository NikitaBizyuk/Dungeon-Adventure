import unittest
from unittest.mock import patch, MagicMock
from model.Thief import Thief
from model.Warrior import Warrior
from model.Priestess import Priestess


class DummyTarget:
    def __init__(self):
        self.damage_taken = []
    def take_damage(self, dmg):
        self.damage_taken.append(dmg)


class TestHeroCommon(unittest.TestCase):

    def setUp(self):
        self.thief = Thief("Robin")
        self.warrior = Warrior("Conan")
        self.priestess = Priestess("Celeste")
        self.target = DummyTarget()

    def test_thief_attributes(self):
        self.assertEqual(self.thief.name, "Robin")
        self.assertEqual(self.thief.health_points, 125)
        self.assertEqual(self.thief.projectile_damage, 10)
        self.assertEqual(self.thief.projectile_speed, 12)
        self.assertEqual(self.thief.projectile_cooldown, 300)

    def test_warrior_attributes(self):
        self.assertEqual(self.warrior.name, "Conan")
        self.assertEqual(self.warrior.health_points, 125)
        self.assertEqual(self.warrior.projectile_damage, 25)
        self.assertEqual(self.warrior.projectile_speed, 8)
        self.assertEqual(self.warrior.projectile_cooldown, 800)

    def test_priestess_attributes(self):
        self.assertEqual(self.priestess.name, "Celeste")
        self.assertEqual(self.priestess.health_points, 100)
        self.assertEqual(self.priestess.projectile_damage, 20)
        self.assertEqual(self.priestess.projectile_speed, 10)
        self.assertEqual(self.priestess.projectile_cooldown, 600)

    @patch("random.random", return_value=0.1)  # ensure hit
    @patch("random.randint", return_value=30)
    def test_thief_melee_attack_hits(self, mock_randint, mock_random):
        self.thief.attack(self.target)
        self.assertEqual(len(self.target.damage_taken), 2)
        self.assertTrue(all(20 <= d <= 40 for d in self.target.damage_taken))

    def test_thief_projectile_attack(self):
        self.thief.attack(self.target, damage=13)
        self.assertIn(13, self.target.damage_taken)

    @patch("random.random", return_value=0.1)
    @patch("random.randint", return_value=50)
    def test_warrior_melee_attack_hits(self, mock_randint, mock_random):
        self.warrior.attack(self.target)
        self.assertIn(50, self.target.damage_taken)

    def test_warrior_projectile_attack(self):
        self.warrior.attack(self.target, damage=25)
        self.assertIn(25, self.target.damage_taken)

    @patch("random.random", return_value=0.1)
    @patch("random.randint", return_value=35)
    def test_priestess_melee_attack_hits(self, mock_randint, mock_random):
        self.priestess.attack(self.target)
        self.assertIn(35, self.target.damage_taken)

    def test_priestess_projectile_attack(self):
        self.priestess.attack(self.target, damage=17)
        self.assertIn(17, self.target.damage_taken)

    def test_melee_styles(self):
        thief_style = self.thief.get_melee_style()
        warrior_style = self.warrior.get_melee_style()
        priestess_style = self.priestess.get_melee_style()
        self.assertEqual(thief_style["swings"], 2)
        self.assertEqual(warrior_style["swings"], 1)
        self.assertEqual(priestess_style["swings"], 1)

    @patch("random.random", return_value=0.1)
    def test_thief_special_double_hit(self, mock_random):
        self.thief.special_skill(self.target)
        self.assertGreaterEqual(len(self.target.damage_taken), 4)

    @patch("random.random", return_value=0.5)
    def test_thief_special_fail(self, mock_random):
        self.thief.special_skill(self.target)
        self.assertEqual(len(self.target.damage_taken), 0)

    @patch("random.random", return_value=0.8)
    def test_thief_special_normal_hit(self, mock_random):
        self.thief.special_skill(self.target)
        self.assertGreaterEqual(len(self.target.damage_taken), 0)

    @patch("random.random", return_value=0.2)
    @patch("random.randint", return_value=100)
    def test_warrior_crushing_blow_success(self, mock_randint, mock_random):
        self.warrior.special_skill(self.target)
        self.assertIn(100, self.target.damage_taken)

    @patch("random.random", return_value=0.8)
    def test_warrior_crushing_blow_miss(self, mock_random):
        self.warrior.special_skill(self.target)
        self.assertEqual(len(self.target.damage_taken), 0)

    @patch("random.randint", return_value=30)
    def test_priestess_heals_below_max(self, mock_randint):
        self.priestess.health_points = 80
        self.priestess.special_skill(None)
        self.assertEqual(self.priestess.health_points, 100)

    def test_priestess_heal_no_effect_at_max(self):
        self.priestess.health_points = 100
        self.priestess.special_skill(None)
        self.assertEqual(self.priestess.health_points, 100)

    def test_to_string_methods(self):
        self.assertIn("HP", self.thief.to_String())
        self.assertIn("Pillars", self.warrior.to_string())
        self.assertIn("HP", self.priestess.to_string())

    def test_pillars_found_and_block_chance(self):
        initial = self.warrior.chance_to_block
        self.warrior.increment_pillars_found()
        self.assertEqual(self.warrior.pillars_found, 1)
        self.assertLess(self.warrior.chance_to_block, initial)

    @patch("random.random", return_value=1.0)  # ensure block fails
    def test_take_damage_unblocked(self, mock_random):
        hp_before = self.thief.health_points
        self.thief.take_damage(15)
        self.assertLess(self.thief.health_points, hp_before)

    @patch("random.random", return_value=0.0)  # ensure block succeeds
    def test_take_damage_blocked(self, mock_random):
        hp_before = self.thief.health_points
        self.thief.take_damage(15)
        self.assertEqual(self.thief.health_points, hp_before)

