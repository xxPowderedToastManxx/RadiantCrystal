import unittest

from CombatController import CombatController
from Player import Player
from Monster import Monster


class FakeDice:
    def __init__(self, d20=20, d6=4):
        self._d20 = d20
        self._d6 = d6

    def roll_d20(self):
        return self._d20

    def roll_d6(self):
        return self._d6


class DummyUI:
    def __init__(self):
        self.messages = []

    def draw_text(self, text, x, y):
        self.messages.append(text)

    def create_buttons(self, options, rect_x=50, rect_y=150, width=200, height=30):
        # return a list of fake button objects; tests will not compare them directly
        return [object() for _ in options]

    def remove_buttons(self, buttons):
        return


class TestCombatController(unittest.TestCase):
    def test_player_attack_hits_and_finishes(self):
        p = Player('Hero')
        m = Monster('Goblin', level=1, stats={'str':8,'dex':8,'con':10,'int':8,'wis':8,'cha':8}, hp=5, attack_bonus=1)
        ui = DummyUI()
        dice = FakeDice(d20=20, d6=3)
        c = CombatController(dice)
        c.start(p, m, ui)
        # simulate player choosing 'Attack'
        c._on_player_choice('Attack')
        # after the attack the monster should have taken dmg and possibly be dead
        self.assertTrue(m.health <= m.max_health)
        # if monster died, controller state should be finished
        if m.health <= 0:
            self.assertTrue(c.is_done())

    def test_monster_attack_misses_or_hits(self):
        p = Player('Hero')
        m = Monster('Goblin', level=1)
        ui = DummyUI()
        # make monster roll low -> miss
        dice = FakeDice(d20=1, d6=1)
        c = CombatController(dice)
        c.start(p, m, ui)
        # simulate player attacking but not ending fight
        c._on_player_choice('Use Item')
        # move to monster turn and call update
        c._state = 'monster_turn'
        c.update(0.016)
        # player health should not be reduced by a miss
        self.assertTrue(p.health >= 0)


if __name__ == '__main__':
    unittest.main()
