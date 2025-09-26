import json

class JSONParser:

    def __init__(self) -> None:
        pass

def load_monsters(path: str = "data/monsters.json"):
    """Load list of monster dicts from the provided JSON file path."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Monsters JSON must be a list of monster objects")

    # basic validation for required fields per monster
    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError(f"Monster entry at index {idx} is not an object")
        if "name" not in entry:
            raise ValueError(f"Monster at index {idx} missing required field 'name'")
        # optional fields: stats (dict), hp (int), attack_bonus (int)
        if "stats" in entry and not isinstance(entry["stats"], dict):
            raise ValueError(f"Monster '{entry.get('name', idx)}' has invalid 'stats' field; expected object")

    return data