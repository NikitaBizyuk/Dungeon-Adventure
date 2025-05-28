# Expanded Room class for in-room movement and layout

class Room:
    def __init__(self, door_r, door_c, width=25, height=15):
        self.width = width
        self.height = height
        self.grid = [["wall" for _ in range(width)] for _ in range(height)]
        self.hero_r = height - 2  # hero spawns just above the door
        self.hero_c = width // 2
        self.door_r = height - 1  # door is now on the bottom row
        self.door_c = width // 2

        self._carve_layout()

    def _carve_layout(self):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                self.grid[r][c] = "floor"
        self.grid[self.door_r][self.door_c] = "door"
        self.grid[self.hero_r][self.hero_c] = "floor"

    def move_hero_in_room(self, dx, dy):
        nr = self.hero_r + dx
        nc = self.hero_c + dy
        if 0 <= nr < self.height and 0 <= nc < self.width:
            target = self.grid[nr][nc]
            if target in ["floor", "door"]:
                self.hero_r = nr
                self.hero_c = nc
                if target == "door":
                    return "exit"
        return None

    def get_tile(self, r, c):
        return self.grid[r][c]

    def get_hero_position(self):
        return self.hero_r, self.hero_c

    def get_dimensions(self):
        return self.height, self.width
    #
    # def toString(self):
    #     result = ""
    #     for r in range(15):
    #         for c in range(100):
    #             # Top and bottom borders
    #             if r == 0 or r == 14:
    #                 result += "*"
    #             # Side borders
    #             elif c == 0 or c == 99:
    #                 result += "*"
    #             elif c == 50 and r == 14:
    #                 result += "_"  # door in the middle bottom
    #
    #             # Interior space
    #             else:
    #                 result += " "
    #         result += "\n"
    #     return result


