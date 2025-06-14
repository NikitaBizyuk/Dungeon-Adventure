from model.OOPillars import OOPillars

class BackPack:
    def __init__(self):
        self._inventory = []
        self._healing_cntr = 0
        self._vision_cntr = 0
        self._abstraction = 0
        self._encapsulation = 0
        self._inheritance = 0
        self._polymorphism = 0
        self._pillar_cntr = 0

    def add(self, name, view=None):
        self._inventory.append(name)

        # Pillars
        if name in {"A", "E", "I", "P"}:
            if name == "A":
                self._abstraction += 1
            elif name == "E":
                self._encapsulation += 1
            elif name == "I":
                self._inheritance += 1
            elif name == "P":
                self._polymorphism += 1

            self._pillar_cntr += 1
            if view:
                if self._pillar_cntr < 4:
                    view.display_message(f"You found Pillar {self._pillar_cntr}/4", 2500)
                else:
                    view.display_message(
                        "🎉 Congrats! You found all 4 Pillars of OOP!\n🏁 Find the exit to win the game!",
                        3000
                    )

        # Vision Potion
        elif name == "Vision Potion":
            self._vision_cntr += 1
            if view:
                view.display_message("You found a Vision Potion", 2500)

        # Healing Potion
        elif name == "Health Potion":
            self._healing_cntr += 1
            if view:
                view.display_message("You found a Healing Potion", 2500)

    def use_healing_potion(self):
        if self._healing_cntr > 0:
            self._healing_cntr -= 1

    def use_vision_potion(self):
        if self._vision_cntr > 0:
            self._vision_cntr -= 1
            return True
        return False

    def found_all_pillars(self):
        return self._pillar_cntr == 4

    def to_string(self):
        return ", ".join(self._inventory)

    # ────── Properties ──────

    @property
    def inventory(self):
        return self._inventory

    @property
    def healing_cntr(self):
        return self._healing_cntr

    @property
    def vision_cntr(self):
        return self._vision_cntr

    @property
    def pillar_cntr(self):
        return self._pillar_cntr

    @property
    def abstraction(self):
        return self._abstraction

    @property
    def encapsulation(self):
        return self._encapsulation

    @property
    def inheritance(self):
        return self._inheritance

    @property
    def polymorphism(self):
        return self._polymorphism
