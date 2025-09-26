from typing import Optional


class Weapon:
    def __init__(self, name: str, damage_die: str = 'd6'):
        self.name = name
        self.damage_die = damage_die

    def damage_die_spec(self) -> str:
        return self.damage_die

    def __repr__(self):
        return f"Weapon(name={self.name!r}, damage_die={self.damage_die!r})"
