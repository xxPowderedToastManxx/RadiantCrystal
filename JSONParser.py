import json

class JSONParser:

    def __init__(self) -> None:
        pass

def load_monsters(path: str = "data/monsters.json"):
    """Load list of monster dicts from the provided JSON file path."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data