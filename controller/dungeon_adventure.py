from model.Ogre import Ogre
from model.warrior import Warrior

hero = Warrior("Conan")
monster = Ogre("Thok")

round_number = 1
while hero.is_alive() and monster.is_alive():
    print(f"\n--- Round {round_number} ---")
    print(hero.get_status())
    print(monster.get_status())

    for _ in range(hero.get_attack_speed()):
        if monster.is_alive():
            hero.attack(monster)

    for _ in range(monster.get_attack_speed()):
        if hero.is_alive():
            monster.attack(hero)

    round_number += 1

print("\n--- Battle Over ---")
print(hero.get_status())
print(monster.get_status())
if hero.is_alive():
    print(f"{hero.get_name()} wins!")
else:
    print(f"{monster.get_name()} wins!")
