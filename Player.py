import json

import CharacterCreator as character_creator
import Inventory 


"""Player model with basic stats and inventory handling.

Provides a minimal, working Player class used by other components.
"""

from typing import Dict, Any, Optional

import Inventory


DEFAULT_STATS: Dict[str, int] = {
    "str": 10,
    "dex": 10,
    "intel": 10,
    "wis": 10,
    "cha": 10,
}


class Player:
    def __init__(
        self,
        name: str,
        player_class: str = "Adventurer",
        level: int = 1,
        health: int = 10,
        attack: int = 1,
        magic_power: int = 0,
        experience: int = 0,
        money: int = 0,
        stats: Optional[Dict[str, int]] = None,
    ) -> None:
        self.name = name
        self.player_class = player_class
        self.level = level
        self.health = health
        self.attack = attack
        self.magic_power = magic_power
        self.experience = experience
        # Inventory.Inventory() keeps current Inventory implementation encapsulated
        self.inventory = Inventory.Inventory()
        self.money = money
        # copy defaults so instances don't share the same dict
        self.stats: Dict[str, int] = dict(DEFAULT_STATS) if stats is None else dict(stats)

    def take_damage(self, damage: int) -> None:
        """Apply damage to the player (health can go to zero or negative)."""
        if damage < 0:
            raise ValueError("damage must be non-negative")
        self.health -= damage

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
            "attack": self.attack,
            "magic_power": self.magic_power,
            "experience": self.experience,
            "money": self.money,
            "stats": dict(self.stats),
        }