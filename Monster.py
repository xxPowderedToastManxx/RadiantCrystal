"""Monster model with simple D&D-like stats.

Keeps the class minimal but adds ability scores, AC (10 + DEX mod), hp,
and a damage_die callable used by mechanics.resolve_attack.
"""

from typing import Dict


class Monster:
    def __init__(self, name: str, level: int = 1, stats: Dict[str, int] = None, hp: int = None, attack_bonus: int = 0, damage_die_spec: str = None):
        self.name = name
        self.level = level
        # ability scores default to 8 for weaker monsters
        default = {"str": 8, "dex": 8, "con": 8, "int": 8, "wis": 8, "cha": 8}
        self.stats = dict(default) if stats is None else dict(stats)
        # hp: if provided use it else derive from CON mod
        con_mod = (self.stats.get("con", 8) - 10) // 2
        base_hp = max(1, 6 + con_mod)
        self.max_health = hp if hp is not None else base_hp + (level - 1) * base_hp
        self.health = self.max_health
        # optional damage die string like 'd6', 'd8'
        self.damage_die_spec = damage_die_spec
        self.attack = attack_bonus

    @property
    def ac(self) -> int:
        return 10 + ((self.stats.get("dex", 8) - 10) // 2)

    def take_damage(self, damage: int) -> None:
        if damage < 0:
            raise ValueError("damage must be non-negative")
        self.health -= damage

    def damage_die(self):
        """Default damage die for monsters: d6."""
        # avoid importing DiceController at module import time; do a local import
        from DiceController import DiceController

        dc = DiceController()
        return dc.roll_d6()

    def damage_die_with_controller(self, dice_controller=None):
        """Return damage using the monster's configured damage die.

        Accepts an optional dice_controller for testing. If no spec set,
        defaults to d6.
        """
        from DiceController import DiceController

        dc = dice_controller or DiceController()
        spec = getattr(self, 'damage_die_spec', None) or 'd6'
        spec = spec.lower().strip()
        if spec == 'd4':
            return dc.roll_d4()
        if spec == 'd6':
            return dc.roll_d6()
        if spec == 'd8':
            return dc.roll_d8()
        if spec == 'd10':
            return dc.roll_d10()
        if spec == 'd12':
            return dc.roll_d12()
        if spec == 'd20':
            return dc.roll_d20()
        # fallback
        return dc.roll_d6()
