# Class for Monsters
class Monster:
    def __init__(self, name, level, health, attack):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage