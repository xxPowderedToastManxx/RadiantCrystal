import unittest

import sys
sys.path.append(r"c:\Users\kenny\Documents\Programming and Computing\Python\Py\Radiant Crystal")

from Player import Player
from DiceController import DiceController
from CombatController import CombatController


class DummyUI:
    def __init__(self):
        self.texts = []
    def draw_text(self, text, x, y):
        self.texts.append((text, x, y))
    def wait_for_action(self, options):
        # always choose Attack for deterministic behavior
        return "Attack"


class TestBasic(unittest.TestCase):
    def test_player_stats_and_damage(self):
        p = Player("Alice")
        self.assertEqual(p.get_stat("str"), 10)
        p.set_stat("str", 15)
        self.assertEqual(p.get_stat("str"), 15)
        p.take_damage(3)
        self.assertEqual(p.health, 7)

    def test_dice_rolls(self):
        d = DiceController()
        self.assertIn(d.roll_d4(), range(1, 5))
        self.assertIn(d.roll_d6(), range(1, 7))
        self.assertIn(d.roll_d20(), range(1, 21))

    def test_combat_happy_path(self):
        p = Player("Bob")
        class M:
            def __init__(self):
                self.name = "Goblin"
                self.level = 1
                self.health = 3
                self.attack = 1
            def take_damage(self, d):
                self.health -= d

        m = M()
        ui = DummyUI()
        cc = CombatController()
        cc.start(p, m, ui)
        # Drive the controller by simulating a single player attack choice via direct call
        cc._on_player_choice('Attack')
        # update to process monster turn
        cc.update(0.016)
        # basic sanity checks
        self.assertIs(cc.player, p)
        self.assertIs(cc.monster, m)
        if cc.is_done():
            self.assertIn(cc.get_result()['winner'], ('player', 'monster'))


if __name__ == '__main__':
    unittest.main()
