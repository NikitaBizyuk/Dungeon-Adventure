import pygame
from view.button import Button  # Adjust if Button is elsewhere

class MenuController:
    def __init__(self, buttons: list[Button]) -> None:
        """
        Initialize the menu controller with a list of UI buttons.

        :param buttons: A list of Button objects representing the menu options.
        """
        self._buttons = buttons
        self._selection = None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """
        Handle a pygame event (usually a mouse click) and update selection.

        :param event: Pygame event object
        :return: Text of the selected button if clicked, else None
        """
        for button in self._buttons:
            if button.is_clicked(event):
                self._selection = button.text
                return self._selection
        return None

    @property
    def selection(self) -> str | None:
        """Return the current selected menu option."""
        return self._selection
