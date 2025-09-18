import random

class Wizard:

    #add wizard class stuff here
    def __init__(self):

        stats = {
        "str": 8,
        "dex": 14,
        "intel": 15,
        "wis": 12,
        "Cha": 8
        }

        self.hit_die = random(1, 6)

        pass

    def set_stats(self, stat, modifier):

        self.stats[stat] = stat * modifier

        return self.stats
    
    def get_stats(self):

        return self.stats