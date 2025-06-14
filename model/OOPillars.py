from enum import Enum
import random

class OOPillars(Enum):
    ABSTRACTION = ('A', "The Abstraction Pillar of OO:\n"
                        "Hides complexity by exposing only essential features.")
    ENCAPSULATION = ('E', "The Encapsulation Pillar of OO:\n"
                          "Bundles data and methods to protect internal state.")
    INHERITANCE = ('I', "The Inheritance Pillar of OO:\n"
                        "Allows a class to acquire properties and behavior of another class.")
    POLYMORPHISM = ('P', "The Polymorphism Pillar of OO:\n"
                         "Enables objects to take many forms and redefine methods.")

    def __init__(self, symbol: str, description: str):
        self._symbol = symbol
        self._description = description

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def description(self) -> str:
        return self._description

    def __str__(self):
        return f"{self.name.capitalize()} ({self.symbol}): {self.description}"
