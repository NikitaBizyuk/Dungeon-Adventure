import random

class Room:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.has_pit = random.random() < 0.1
        self.has_healing_potion = random.random() < 0.1
        self.has_vision_potion = random.random() < 0.1

    def enter(self, hero):
        print(f"\nYou entered room at ({self.row}, {self.col})")

        if self.has_pit:
            damage = random.randint(1, 20)
            hero.take_damage(damage)
            print(f"You fell into a pit! Took {damage} damage.")

        if self.has_healing_potion:
            heal = random.randint(5, 15)
            hero.heal(heal)
            hero.healing_potions += 1
            print(f"Found a healing potion! Gained {heal} HP. (Auto-used)")

        if self.has_vision_potion:
            hero.vision_potions += 1
            print("Found a vision potion!")
