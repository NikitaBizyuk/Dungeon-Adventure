class MazeCell:
    def __init__(self, row, col, cell_type="wall"):
        self.row = row
        self.col = col
        self.cell_type = cell_type  # "wall", "hallway", "door", "exit"
        self.door_id = None         # Only for doors
        self.visible = False        # Currently visible?
        self.explored = False       # Ever seen before?
