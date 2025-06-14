class MazeCell:
    def __init__(self, row, col, cell_type="wall"):
        self._row = row
        self._col = col
        self._cell_type = cell_type  # "wall", "hallway", "door", "exit"
        self._door_id = None         # Only used for doors
        self._visible = False        # Currently visible to player
        self._explored = False       # Was ever visible

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def cell_type(self):
        return self._cell_type

    @cell_type.setter
    def cell_type(self, value):
        self._cell_type = value

    @property
    def door_id(self):
        return self._door_id

    @door_id.setter
    def door_id(self, value):
        self._door_id = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = bool(value)

    @property
    def explored(self):
        return self._explored

    @explored.setter
    def explored(self, value):
        self._explored = bool(value)
