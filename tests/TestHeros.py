import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import pygame
import os
import sys
from model.AnimatedHero import AnimatedHero


class TestAnimatedHero(unittest.TestCase):
    def setUp(self):
        # Mock pygame and time functions
        pygame_patcher = patch.dict('sys.modules', {'pygame': MagicMock()})
        self.mock_pygame = pygame_patcher.start()
        self.addCleanup(pygame_patcher.stop)

        # Mock time functions
        self.mock_get_ticks = MagicMock(return_value=0)
        self.mock_pygame.time.get_ticks = self.mock_get_ticks

        # Create a test instance with minimal dependencies
        self.hero = AnimatedHero(
            name="TestHero",
            health_points=100,
            damage_min=10,
            damage_max=20,
            attack_speed=5,
            chance_to_hit=0.8,
            sprite_folder="test_hero"
        )

        # Replace animations with simple mocks
        self.hero.animations = {
            "idle": MagicMock(),
            "running": MagicMock(),
            "slashing": MagicMock(),
            "run_slashing": MagicMock(),
            "throwing": MagicMock(),
            "run_throwing": MagicMock(),
            "hurt": MagicMock(),
            "dead": MagicMock()
        }

    def test_initialization(self):
        """Test basic initialization"""
        self.assertEqual(self.hero.name, "TestHero")
        self.assertEqual(self.hero.health_points, 100)
        self.assertEqual(self.hero.current_animation, "idle")
        self.assertFalse(self.hero._moving)
        self.assertTrue(self.hero.facing_right)
        self.assertFalse(self.hero._dead)

    def test_take_damage_animation(self):
        """Test animation changes when taking damage"""
        # Take damage while alive
        self.mock_get_ticks.return_value = 1000
        self.hero.take_damage(20)
        self.assertEqual(self.hero.current_animation, "hurt")
        self.assertEqual(self.hero._last_animation_change, 1000)

        # Take lethal damage
        self.hero.take_damage(100)
        self.assertEqual(self.hero.current_animation, "dead")

    def test_attack_animation_flow(self):
        """Test attack animation sequence"""
        # Start attack
        self.mock_get_ticks.return_value = 1000
        self.hero.start_attack()
        self.assertEqual(self.hero.current_animation, "slashing")
        self.assertEqual(self.hero._last_animation_change, 1000)

        # During lock period
        self.mock_get_ticks.return_value = 1200
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "slashing")

        # After lock period expires
        self.mock_get_ticks.return_value = 1400  # 400ms later
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "idle")

    def test_movement_animation_transitions(self):
        """Test animation changes based on movement state"""
        # Start moving
        self.hero._moving = True
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "running")

        # Stop moving
        self.hero._moving = False
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "idle")

    def test_animation_priority_rules(self):
        """Test that attack animations override movement"""
        # Start moving then attack
        self.hero._moving = True
        self.mock_get_ticks.return_value = 1000
        self.hero.start_attack()
        self.assertEqual(self.hero.current_animation, "slashing")

        # After attack completes, should return to running
        self.mock_get_ticks.return_value = 1400
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "running")

    def test_death_state_handling(self):
        """Test death animation and state management"""
        # Die
        self.hero.health_points = 0
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "dead")
        self.assertTrue(self.hero._dead)

        # Should stay in dead state
        self.hero.update_animation(0.1)
        self.assertEqual(self.hero.current_animation, "dead")

    def test_flash_hit_mechanism(self):
        """Test hit flash timing"""
        # Initial state
        self.assertFalse(self.hero.is_flashing())

        # Take hit
        self.mock_get_ticks.return_value = 1000
        self.hero.flash_hit()
        self.assertTrue(self.hero.is_flashing())

        # After flash duration
        self.mock_get_ticks.return_value = 1300  # 300ms later
        self.assertTrue(self.hero.is_flashing())

        self.mock_get_ticks.return_value = 1500  # 500ms later
        self.assertFalse(self.hero.is_flashing())

    def test_animation_update_propagation(self):
        """Test that updates reach current animation"""
        # Check idle animation update
        self.hero.update_animation(0.1)
        self.hero.animations["idle"].update.assert_called_with(0.1)

        # Check running animation update
        self.hero._moving = True
        self.hero.animations["idle"].reset_mock()
        self.hero.update_animation(0.2)
        self.hero.animations["running"].update.assert_called_with(0.2)

    def test_pickle_compatibility(self):
        """Test serialization support"""
        import pickle

        # Mock the animation reloading
        with patch.object(self.hero, '_reload_animations') as mock_reload:
            # Serialize and deserialize
            data = pickle.dumps(self.hero)
            new_hero = pickle.loads(data)

            # Should attempt to reload animations
            mock_reload.assert_called_once()

            # Core properties should be preserved
            self.assertEqual(new_hero.name, self.hero.name)
            self.assertEqual(new_hero.health_points, self.hero.health_points)


if __name__ == '__main__':
    unittest.main()