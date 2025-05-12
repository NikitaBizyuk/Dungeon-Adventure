class Room:
    def __init__(self, hasPit=False, hasHealingPotion=False, hasVisionPotion=False, pillar=None):
        self.myHasPit = hasPit
        self.myHasHealingPotion = hasHealingPotion
        self.myHasVisionPotion = hasVisionPotion
        self.myPillar = pillar  # can be "Abstraction", "Encapsulation", etc.

    def enter(self, hero):
        print("\n--- You entered a room ---")
        if self.myHasPit:
            print("You fell into a pit!")
        if self.myHasHealingPotion:
            print("You found a healing potion!")
        if self.myHasVisionPotion:
            print("You found a vision potion!")
        if self.myPillar:
            print(f"You found the Pillar of {self.myPillar}!")
        if not (self.myHasPit or self.myHasHealingPotion or self.myHasVisionPotion or self.myPillar):
            print("The room is empty.")
