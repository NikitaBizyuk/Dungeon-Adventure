import unittest
from model.MazeCell import MazeCell  # Assuming your class is in maze_cell.py

class TestMazeCell(unittest.TestCase):

    def test_initialization(self):
        cell = MazeCell(2, 3)
        self.assertEqual(cell.row, 2)
        self.assertEqual(cell.col, 3)
        self.assertEqual(cell.cell_type, "wall")
        self.assertIsNone(cell.door_id)
        self.assertFalse(cell.visible)
        self.assertFalse(cell.explored)

    def test_custom_initialization(self):
        cell = MazeCell(1, 1, "door")
        self.assertEqual(cell.cell_type, "door")
        cell.door_id = "D1"
        self.assertEqual(cell.door_id, "D1")

    def test_visibility_exploration(self):
        cell = MazeCell(0, 0, "hallway")
        cell.visible = True
        self.assertTrue(cell.visible)

        cell.explored = True
        self.assertTrue(cell.explored)

if __name__ == '__main__':
    unittest.main()