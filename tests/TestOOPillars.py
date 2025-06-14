from unittest import TestCase
from model.OOPillars import OOPillars


class TestOOPillars(TestCase):

    def test_enum_properties(self):
        self.assertEqual(OOPillars.ABSTRACTION.symbol, "A")
        self.assertEqual(OOPillars.ABSTRACTION.description,
                         "The Abstraction Pillar of OO: \nHides Complexity by exposing only essential features.")

        self.assertEqual(OOPillars.ENCAPSULATION.symbol, "E")
        self.assertEqual(OOPillars.ENCAPSULATION.description,
                         "The Encapsulation Pillar of OO: \nBundles data and methods to protect internal state")

        self.assertEqual(OOPillars.INHERITANCE.symbol, "I")
        self.assertEqual(OOPillars.INHERITANCE.description,
                         "The Inheritance Pillar of OO: \nAllows a class to acquire properties and behavior of another class.")

        self.assertEqual(OOPillars.POLYMORPHISM.symbol, "P")
        self.assertEqual(OOPillars.POLYMORPHISM.description,
                         "The Polymorphism Pillar of OO: \nEnables objects to take many forms and redefine methods.")

    def test_enum_string_representation(self):
        self.assertEqual(str(OOPillars.ABSTRACTION),
                         "Abstraction (A): The Abstraction Pillar of OO: \nHides Complexity by exposing only essential features.")

