from model.OOPillars import OOPillars
class BackPack:

    def __init__(self):
        self.inventory = []
        self.healing_cntr = 0
        self.vision_cntr = 0
        self.pillar_cntr = 0

    def add(self,name):
        self.inventory.append(name)
        if isinstance(name,OOPillars) and (name == OOPillars.ENCAPSULATION or
                name == OOPillars.ABSTRACTION or name == OOPillars.INHERITANCE or
                name == OOPillars.POLYMORPHISM):
            self.pillar_cntr = self.pillar_cntr + 1
        if name == "Vision Potion":
            self.vision_cntr = self.vision_cntr + 1
        if name == "Health Potion":
            self.healing_cntr = self.healing_cntr + 1
    def remove(self,name):
        pass
    def get_inventory(self):
        return self.inventory
    def get_healing_cntr(self):
        return self.healing_cntr
    def get_vision_cntr(self):
        return self.vision_cntr
    def get_pillar_cntr(self):
        return self.pillar_cntr
    def to_string(self):
        result = ""
        for i in range(len(self.inventory)):
            result += self.inventory[i] + ", "
        return result