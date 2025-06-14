class MenuController:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selection = None

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.selection = button.text
                return self.selection
        return None