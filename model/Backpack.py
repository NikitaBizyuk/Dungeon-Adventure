from model.OOPillars import OOPillars
class BackPack:

    def __init__(self):
        self.inventory = []
        self.healing_cntr = 0
        self.vision_cntr = 0
        self.abstraction = 0
        self.encapsulation = 0
        self.inheritance = 0
        self.polymorphism = 0
        self.pillar_cntr = 0

    def add(self,name,view):
        self.inventory.append(name)
        if name in {"A", "E", "I", "P"}:
            if name == "A":
                self.abstraction += 1
            elif name == "E":
                self.encapsulation += 1
            elif name == "I":
                self.inheritance += 1
            else:
                self.polymorphism += 1
            self.pillar_cntr = self.pillar_cntr + 1
            if self.pillar_cntr < 4:
                view.display_message(f"You found Pillar {self.pillar_cntr}/4", 2500)
            else:
                view.display_message("🎉 Congrats! You found all 4 Pillars of OOP!\n🏁 Find the exit to win the game!",
                                     3000)
        if name == "Vision Potion":
            self.vision_cntr = self.vision_cntr + 1
            view.display_message(f"You found A Vision Potion ", 2500)
        if name == "Health Potion":
            self.healing_cntr = self.healing_cntr + 1
            if self.pillar_cntr < 4:
                view.display_message(f"You found A Healing Potion ", 2500)
            else:
                view.display_message("🎉 Congrats! You found all 4 Pillars of OOP!\n"
                                          " Find the exit to win the game!", 3000)
    def get_inventory(self):
        return self.inventory
    def get_healing_cntr(self):
        return self.healing_cntr
    def get_vision_cntr(self):
        return self.vision_cntr
    def get_pillar_cntr(self):
        return self.pillar_cntr
    def use_healing_potion(self):
        if self.healing_cntr > 0:
            self.healing_cntr -= 1
    def use_vision_potion(self):
        if self.vision_cntr > 0:
            self.vision_cntr -= 1
            return True
        return False
    def found_all_pillars(self):
        return self.pillar_cntr == 4
    def to_string(self):
        result = ""
        for i in range(len(self.inventory)):
            result += self.inventory[i] + ", "
        return result