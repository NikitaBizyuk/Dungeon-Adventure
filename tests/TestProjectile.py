import unittest
import pygame
from pygame.math import Vector2
from model.Projectile import Projectile


class TestProjectile(unittest.TestCase):
    def setUp(self):
        pygame.init()  # Initialize pygame for surface creation
        self.test_surface = pygame.Surface((800, 600))
        self.start_pos = (100, 100)
        self.direction = (1, 0)  # Right direction
        self.speed = 10
        self.damage = 10
        self.projectile = Projectile(*self.start_pos, *self.direction,
                                     speed=self.speed, damage=self.damage)

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        """Test that projectile initializes with correct values"""
        self.assertEqual(self.projectile.x, self.start_pos[0])
        self.assertEqual(self.projectile.y, self.start_pos[1])
        self.assertEqual(self.projectile.radius, 5)
        self.assertEqual(self.projectile.damage, self.damage)
        self.assertTrue(self.projectile.active)

        # Test velocity normalization and speed
        expected_velocity = Vector2(self.direction).normalize() * self.speed
        self.assertEqual(self.projectile.velocity, expected_velocity)

    def test_update_movement(self):
        """Test that projectile moves correctly with update()"""
        initial_x, initial_y = self.projectile.x, self.projectile.y

        # Test movement after one update
        self.projectile.update()
        self.assertEqual(self.projectile.x, initial_x + self.speed)
        self.assertEqual(self.projectile.y, initial_y)

        # Test movement after multiple updates
        for _ in range(5):
            self.projectile.update()
        self.assertEqual(self.projectile.x, initial_x + 6 * self.speed)
        self.assertEqual(self.projectile.y, initial_y)

    def test_inactive_update(self):
        """Test that inactive projectiles don't move"""
        self.projectile.deactivate()
        initial_x, initial_y = self.projectile.x, self.projectile.y

        self.projectile.update()
        self.assertEqual(self.projectile.x, initial_x)
        self.assertEqual(self.projectile.y, initial_y)

    def test_draw(self):
        """Test that drawing works without errors"""
        try:
            self.projectile.draw(self.test_surface)
            # If we get here, drawing succeeded
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Drawing failed with exception: {e}")

    def test_draw_inactive(self):
        """Test that inactive projectiles don't draw"""
        self.projectile.deactivate()

        # Get pixel color at projectile position before drawing
        before_color = self.test_surface.get_at((int(self.projectile.x), int(self.projectile.y)))

        self.projectile.draw(self.test_surface)

        # Get pixel color after drawing
        after_color = self.test_surface.get_at((int(self.projectile.x), int(self.projectile.y)))

        # Should be unchanged since projectile is inactive
        self.assertEqual(before_color, after_color)

    def test_get_position(self):
        """Test position getter returns correct values"""
        pos = self.projectile.get_position()
        self.assertEqual(pos, (self.projectile.x, self.projectile.y))

        # After movement
        self.projectile.update()
        new_pos = self.projectile.get_position()
        self.assertEqual(new_pos, (self.projectile.x, self.projectile.y))

    def test_deactivate(self):
        """Test that deactivate() works correctly"""
        self.assertTrue(self.projectile.active)
        self.projectile.deactivate()
        self.assertFalse(self.projectile.active)

        # Test deactivating already inactive projectile
        self.projectile.deactivate()  # Should not raise error
        self.assertFalse(self.projectile.active)

    def test_diagonal_movement(self):
        """Test movement in diagonal direction"""
        diagonal_projectile = Projectile(0, 0, 1, 1, speed=10)

        # Calculate expected normalized velocity
        expected_velocity = Vector2(1, 1).normalize() * 10

        # Test velocity initialization
        self.assertAlmostEqual(diagonal_projectile.velocity.x, expected_velocity.x, places=5)
        self.assertAlmostEqual(diagonal_projectile.velocity.y, expected_velocity.y, places=5)

        # Test movement
        initial_x, initial_y = diagonal_projectile.x, diagonal_projectile.y
        diagonal_projectile.update()
        self.assertAlmostEqual(diagonal_projectile.x, initial_x + expected_velocity.x, places=5)
        self.assertAlmostEqual(diagonal_projectile.y, initial_y + expected_velocity.y, places=5)


if __name__ == '__main__':
    unittest.main()