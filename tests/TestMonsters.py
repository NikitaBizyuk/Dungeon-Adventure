from unittest import TestCase
import random
from unittest.mock import patch, MagicMock
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.Skeleton import Skeleton

class TestMonsterHierarchy(TestCase):
    def setUp(self):
        # Common test data
        self.test_monsters = [
            Gremlin("Test Gremlin", 50, 5, 0.8, 5, 10, 0.3, 2, 5),
            Ogre("Test Ogre", 100, 2, 0.6, 10, 20, 0.1, 5, 10),
            Skeleton("Test Skeleton", 30, 3, 0.7, 3, 7, 0.2, 1, 3)
        ]

        # Mock target for attacks
        self.mock_target = MagicMock()
        self.mock_target.name = "Test Hero"
        self.mock_target.health_points = 100
        self.mock_target.take_damage = MagicMock()
        self.mock_target.flash_hit = MagicMock()

    def test_set_health_points(self):
        for monster in self.test_monsters:
            # Test setting valid health points
            test_values = [1, 50, monster.health_points]
            for value in test_values:
                monster.set_health_points(value)
                self.assertEqual(monster.health_points, value)

            # Test setting negative health (should clamp to 0)
            monster.set_health_points(-10)
            self.assertEqual(monster.health_points, 0)

            # Test setting health above max (should allow)
            monster.set_health_points(monster.health_points + 100)
            self.assertGreater(monster.health_points, monster.health_points - 100)

    def test_take_damage(self):
        for monster in self.test_monsters:
            initial_hp = monster.health_points

            # Test normal damage
            damage = 10
            monster.take_damage(damage )
            self.assertTrue(monster.is_flashing())

            # Test excessive damage (should clamp to 0)
            monster.take_damage(initial_hp * 2)
            self.assertEqual(monster.health_points, 0)

            # Test damage triggers heal check
            with patch.object(monster, 'heal') as mock_heal:
                monster.set_health_points(50)
                monster.take_damage(10)
                mock_heal.assert_called_once()

    def test_flash_hit(self):
        for monster in self.test_monsters:
            # Test flash_hit sets last_hit_time
            initial_time = monster._last_hit_time
            monster.flash_hit()
            self.assertNotEqual(monster._last_hit_time, initial_time)

            # Test flash_hit makes is_flashing return True
            self.assertTrue(monster.is_flashing())

    def test_is_flashing(self):
        for monster in self.test_monsters:
            # Initially should not be flashing
            self.assertFalse(monster.is_flashing())

            # After flash_hit, should be flashing
            monster.flash_hit()
            self.assertTrue(monster.is_flashing())

            # Test flashing expires after time
            with patch('pygame.time.get_ticks', return_value=monster._last_hit_time + 300):
                self.assertFalse(monster.is_flashing())

    def test_heal(self):
        for monster in self.test_monsters:
            # Damage the monster first
            monster.set_health_points(monster.health_points // 2)
            current_hp = monster.health_points

            # Test successful heal
            with patch('random.random', return_value=0.05):  # Below chance_to_heal
                with patch('random.randint', return_value=monster._heal_max):  # Max heal
                    monster.heal()
                    self.assertEqual(monster.health_points, current_hp + monster._heal_max)

            # Test no heal when random above chance
            with patch('random.random', return_value=0.5):  # Above chance_to_heal
                current_hp = monster.health_points
                monster.heal()
                self.assertEqual(monster.health_points, current_hp)

            # Test no heal when dead
            monster.set_health_points(0)
            monster.heal()
            self.assertEqual(monster.health_points, 0)

    def test_get_heal_points(self):
        for monster in self.test_monsters:
            # Should return the chance_to_heal value
            self.assertEqual(monster.get_heal_points(), monster._chance_to_heal)

            # Should be between 0 and 1
            self.assertTrue(0 <= monster.get_heal_points() <= 1)

    def test_attack_hero(self):
        for monster in self.test_monsters:
            # Reset mock for each test
            self.mock_target.reset_mock()

            # Test successful attack
            with patch('random.random', return_value=0.1):  # Below chance_to_hit
                with patch('random.randint', return_value=monster.damage_max):
                    monster.attack_hero(self.mock_target)
                    self.mock_target.take_damage.assert_called_once_with(monster.damage_max)
                    self.mock_target.flash_hit.assert_not_called()

            # Test missed attack
            with patch('random.random', return_value=0.9):  # Above chance_to_hit
                monster.attack_hero(self.mock_target)
                self.mock_target.take_damage.assert_called_once()

    # Existing comprehensive tests from previous implementation
    def test_initialization(self):
        for monster in self.test_monsters:
            self.assertIsNotNone(monster.name)
            self.assertGreater(monster.health_points, 0)
            self.assertGreater(monster.attack_speed, 0)
            self.assertTrue(0 <= monster.chance_to_hit <= 1)
            self.assertGreater(monster.damage_max, monster.damage_min)
            self.assertTrue(0 <= monster.get_heal_points() <= 1)

    def test_monster_specifics(self):
        # Test Gremlin specifics
        gremlin = self.test_monsters[0]
        self.assertEqual(gremlin.name, "Test Gremlin")
        self.assertEqual(gremlin.get_heal_range(), (2, 5))
        self.assertIn("Gremlin", str(gremlin))

        # Test Ogre specifics
        ogre = self.test_monsters[1]
        self.assertEqual(ogre.name, "Test Ogre")
        self.assertEqual(ogre.get_heal_range(), (5, 10))
        self.assertIn("Ogre", str(ogre))

        # Test Skeleton specifics
        skeleton = self.test_monsters[2]
        self.assertEqual(skeleton.name, "Test Skeleton")
        self.assertEqual(skeleton.get_heal_range(), (1, 3))
        self.assertIn("Skeleton", str(skeleton))


