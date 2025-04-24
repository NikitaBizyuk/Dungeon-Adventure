from my_model import Model
from my_view import View

class Controller:

    def __init__(self):
        self.model = Model(self)
        self.view = View(self)


    def main(self):
        print("This is the main method")

if __name__ == '__main__':
    dungeon_adventure = Controller()
    dungeon_adventure.main()
    