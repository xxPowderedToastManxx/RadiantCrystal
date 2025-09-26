import random
from typing import Optional

from JSONParser import load_monsters
from Monster import Monster


_MONSTER_CACHE = None


def _ensure_cache(path: str = "data/monsters.json"):
    global _MONSTER_CACHE
    if _MONSTER_CACHE is None:
        _MONSTER_CACHE = load_monsters(path)
    return _MONSTER_CACHE


def get_monster_by_name(name: str, path: str = "data/monsters.json") -> Optional[Monster]:
    """Return a Monster instance matching the given name, or None if not found."""
    data = _ensure_cache(path)
    for entry in data:
            if entry.get("name", "").lower() == name.lower():
                return Monster(entry.get("name"), entry.get("level", 1), entry.get("stats"), entry.get("hp"), entry.get("attack_bonus", 0), entry.get("damage_die") or entry.get("damage_die_spec"))
    return None


def random_monster(path: str = "data/monsters.json") -> Monster:
    """Return a random Monster instance from the JSON list."""
    data = _ensure_cache(path)
    entry = random.choice(data)
    return Monster(entry.get("name"), entry.get("level", 1), entry.get("stats"), entry.get("hp"), entry.get("attack_bonus", 0), entry.get("damage_die") or entry.get("damage_die_spec"))


def list_monsters(path: str = "data/monsters.json"):
    """Return a list of monster names (in order) from the JSON file."""
    data = _ensure_cache(path)
    return [entry.get("name", "") for entry in data]


def get_monster_by_index(index: int, path: str = "data/monsters.json") -> Optional[Monster]:
    data = _ensure_cache(path)
    if index < 0 or index >= len(data):
        return None
    entry = data[index]
    return Monster(entry.get("name"), entry.get("level", 1), entry.get("stats"), entry.get("hp"), entry.get("attack_bonus", 0), entry.get("damage_die") or entry.get("damage_die_spec"))
