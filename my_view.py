

class View:

    def __init__(self,controller):
        #Constructor
        self.controller = controller
    def main(self):
        #Call this method in controllers main method to initialize GUI.
        print("This is main method for GUI")
