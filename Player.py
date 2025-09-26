import json

import CharacterCreator as character_creator
import Inventory

from typing import Dict, Any, Optional

from mechanics import ability_mod
from weapon import Weapon
from typing import Optional as TypingOptional


"""Player model with D&D-like stats and helpers.

This extends the previous minimal Player to include ability scores
('str','dex','con','int','wis','cha'), an AC computed from DEX, and
simple HP bookkeeping. The class remains lightweight and backward
compatible with existing code that expects .health and .attack.
"""


DEFAULT_STATS: Dict[str, int] = {
    "str": 10,
    "dex": 10,
    "con": 10,
    "int": 10,
    "wis": 10,
    "cha": 10,
}


class Player:
    def __init__(
        self,
        name: str,
        player_class: str = "Adventurer",
        level: int = 1,
        health: Optional[int] = None,
        attack: int = 1,
        magic_power: int = 0,
        experience: int = 0,
        money: int = 0,
        stats: Optional[Dict[str, int]] = None,
    ) -> None:
        self.name = name
        self.player_class = player_class
        self.level = level
        # stats holds ability scores; copy defaults so instances don't share dict
        self.stats: Dict[str, int] = dict(DEFAULT_STATS) if stats is None else dict(stats)
        # compute derived values
        self.attack = attack
        self.magic_power = magic_power
        self.experience = experience
        self.inventory = Inventory.Inventory()
        self.money = money

        # health: if not provided compute simple HP from CON modifier
        con_mod = ability_mod(self.stats.get("con", 10))
        # simple HP rule: base 8 + CON mod per level
        base_hp = 8 + con_mod
        self.max_health = health if health is not None else max(1, base_hp + (level - 1) * max(1, base_hp))
        self.health = self.max_health
        # equipped weapon (optional)
        self.equipped_weapon: TypingOptional[Weapon] = None

    def damage_die_with_controller(self, dice_controller=None):
        """Return damage using equipped weapon if present, otherwise fallback to d6."""
        if self.equipped_weapon is not None:
            spec = getattr(self.equipped_weapon, 'damage_die', None)
            # create a temporary Monster-like object to reuse monster damage logic
            class _Tmp:
                pass

            t = _Tmp()
            t.damage_die_spec = spec
            from Monster import Monster
            # piggyback on Monster.damage_die_with_controller
            return Monster('tmp').damage_die_with_controller(dice_controller)
        # fallback
        from DiceController import DiceController
        dc = dice_controller or DiceController()
        return dc.roll_d6()

    @property
    def ac(self) -> int:
        """Armor Class computed as 10 + DEX modifier (simple rule)."""
        return 10 + ability_mod(self.stats.get("dex", 10))

    def take_damage(self, damage: int) -> None:
        """Apply damage to the player (health can go to zero or negative)."""
        if damage < 0:
            raise ValueError("damage must be non-negative")
        self.health -= damage

    def heal(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("heal amount must be non-negative")
        self.health = min(self.max_health, self.health + amount)

    def gain_experience(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("experience amount must be non-negative")
        self.experience += amount

    def get_stat(self, key: str) -> int:
        """Return the named stat. Raises KeyError if stat not present."""
        return self.stats[key]

    def set_stat(self, key: str, value: int) -> None:
        """Set a stat to a given integer value. Validates inputs."""
        if key not in self.stats:
            raise KeyError(f"Unknown stat '{key}'")
        if not isinstance(value, int):
            raise TypeError("stat value must be int")
        self.stats[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "class": self.player_class,
            "level": self.level,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "magic_power": self.magic_power,
            "experience": self.experience,
            "money": self.money,
            "stats": dict(self.stats),
            "ac": self.ac,
            "equipped_weapon": repr(self.equipped_weapon) if self.equipped_weapon is not None else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        stats = data.get("stats")
        p = cls(
            name=data.get("name", "Player"),
            player_class=data.get("class", "Adventurer"),
            level=data.get("level", 1),
            health=data.get("max_health"),
            attack=data.get("attack", 1),
            magic_power=data.get("magic_power", 0),
            experience=data.get("experience", 0),
            money=data.get("money", 0),
            stats=stats,
        )
        # if there was a current health value set it
        if "health" in data:
            p.health = data["health"]
        return p