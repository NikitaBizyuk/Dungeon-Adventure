import unittest
from unittest.mock import MagicMock, patch
from abc import ABC, abstractmethod
from model.DungeonCharacter import DungeonCharacter


class TestDungeonCharacter(unittest.TestCase):
    class ConcreteDungeonCharacter(DungeonCharacter):
        """Concrete implementation for testing abstract methods"""

        def attack(self, target):
            return f"Attacked {target.name}"

        def take_damage(self, amount):
            self.health_points -= amount
            return f"Took {amount} damage"

    def setUp(self):
        """Create a test instance of the concrete implementation"""
        self.test_char = self.ConcreteDungeonCharacter(
            name="Test Hero",
            health_points=100,
            damage_min=5,
            damage_max=10,
            attack_speed=3,
            chance_to_hit=0.8
        )

    def test_initialization(self):
        """Test that initialization sets properties correctly"""
        self.assertEqual(self.test_char.name, "Test Hero")
        self.assertEqual(self.test_char.health_points, 100)
        self.assertEqual(self.test_char.damage_min, 5)
        self.assertEqual(self.test_char.damage_max, 10)
        self.assertEqual(self.test_char.attack_speed, 3)
        self.assertEqual(self.test_char.chance_to_hit, 0.8)

    def test_is_alive(self):
        """Test the is_alive() method"""
        self.assertTrue(self.test_char.is_alive())

        # Test when health is exactly 0
        self.test_char.health_points = 0
        self.assertFalse(self.test_char.is_alive())

        # Test when health is negative
        self.test_char.health_points = -10
        self.assertFalse(self.test_char.is_alive())

    def test_health_points_property(self):
        """Test the health_points property setter/getter"""
        # Test normal setting
        self.test_char.health_points = 50
        self.assertEqual(self.test_char.health_points, 50)

        # Test clamping to 0
        self.test_char.health_points = -10
        self.assertEqual(self.test_char.health_points, 0)

        # Test setting above max (should allow)
        self.test_char.health_points = 1000
        self.assertEqual(self.test_char.health_points, 1000)

    def test_abstract_methods(self):
        """Test that abstract methods are implemented and work"""
        mock_target = MagicMock()
        mock_target.name = "Test Target"

        # Test attack method
        result = self.test_char.attack(mock_target)
        self.assertEqual(result, "Attacked Test Target")

        # Test take_damage method
        result = self.test_char.take_damage(15)
        self.assertEqual(result, "Took 15 damage")
        self.assertEqual(self.test_char.health_points, 85)

    def test_get_status(self):
        """Test the get_status() method"""
        self.assertEqual(self.test_char.get_status(), "Test Hero: 100 HP")

        # Test after damage
        self.test_char.health_points = 25
        self.assertEqual(self.test_char.get_status(), "Test Hero: 25 HP")

        # Test when dead
        self.test_char.health_points = 0
        self.assertEqual(self.test_char.get_status(), "Test Hero: 0 HP")

    def test_property_accessors(self):
        """Test all property accessors"""
        self.assertEqual(self.test_char.name, "Test Hero")
        self.assertEqual(self.test_char.damage_min, 5)
        self.assertEqual(self.test_char.damage_max, 10)
        self.assertEqual(self.test_char.attack_speed, 3)
        self.assertEqual(self.test_char.chance_to_hit, 0.8)

    def test_cannot_instantiate_abstract_class(self):
        """Test that DungeonCharacter cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            char = DungeonCharacter(
                name="Should Fail",
                health_points=100,
                damage_min=5,
                damage_max=10,
                attack_speed=3,
                chance_to_hit=0.8
            )


if __name__ == '__main__':
    unittest.main()