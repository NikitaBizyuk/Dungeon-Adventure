class MazeCell:
    def __init__(self, row, col, cell_type="wall"):
        self.row = row
        self.col = col
        self.cell_type = cell_type  # "wall", "hallway", "door"
        self.door_id = None         # if cell_type == "door", this links to a room
