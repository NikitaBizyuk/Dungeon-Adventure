import sqlite3

def init_monster_database():
    conn = sqlite3.connect("data/monsters.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS monsters")

    c.execute("""
    CREATE TABLE monsters (
        name TEXT PRIMARY KEY,
        hp INTEGER,
        attack_speed INTEGER,
        chance_to_hit REAL,
        damage_min INTEGER,
        damage_max INTEGER,
        chance_to_heal REAL,
        heal_min INTEGER,
        heal_max INTEGER
    )
    """)

    monsters = [
        ("Ogre", 200, 2, 0.6, 30, 60, 0.1, 30, 60),
        ("Gremlin", 70, 5, 0.8, 15, 30, 0.4, 20, 40),
        ("Skeleton", 100, 3, 0.8, 30, 50, 0.3, 30, 50)
    ]

    c.executemany("INSERT INTO monsters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", monsters)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_monster_database()
