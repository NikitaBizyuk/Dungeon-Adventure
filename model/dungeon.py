import random
import os
from typing import List


class Dungeon:

    def __init__(self):
        #myMazes stores 10 randomly generated mazes
        self.__myMazes = self.create_mazes()
        #gamePlayMaze stores the random maze that the player will see on the screen
        self.__gamePlayMaze = self.select_random_maze()
        #myPositionX stores the players X position
        self.__myPositionX = 1
        #myPositionY stores the players Y position
        self.__myPositionY = 1

    """
    create_mazes() scans 10 randomly generated mazes from a .txt file
    and places the mazes in a 2D list. Every index position of the list
    stores a maze. Size of maze and number of rooms vary.
    """
    def create_mazes(self) -> list[list[object]]:
        result: list[list[object]] = []
        try:
            current_dir = os.path.dirname(__file__)
            file_path = os.path.join(current_dir, "random_mazes.txt")
            with open(file_path, 'r') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    row_col_line = lines[i].strip()
                    if not row_col_line or not row_col_line[0].isdigit():
                        i += 1
                        continue
                    try:
                        parts = row_col_line.split()
                        if len(parts) < 2:
                            raise ValueError("Not enough values for rows and cols.")
                        rows, cols = int(parts[0]), int(parts[1])
                        i += 1
                    except ValueError:
                        print(f"Invalid row/col format at line {i + 1}: {lines[i]}")
                        i += 1
                        continue
                    # Read the maze lines
                    maze: list[object] = []
                    for _ in range(rows):
                        if i < len(lines):
                            maze.append(lines[i].strip())

                            i += 1
                    result.append(maze)
        except FileNotFoundError:
            print("File not found")
        return result

    def select_random_maze(self) -> list[object]:
        maze = random.choice(self.__myMazes)
        return maze

    """
    add_rooms will iterate through the gamePlayMaze and replace every
    R character with a room object.
    """
    def add_rooms(self, rooms: list[object]) -> None:
        # logic to add rooms goes here
        pass

    """
    current_to_string displays the randomly selected
    gamePlayMaze
    """
    def current_to_string(self) -> str:
        result = "Current Maze\n"
        for line in self.__gamePlayMaze:
            result += line + "\n"
        return result