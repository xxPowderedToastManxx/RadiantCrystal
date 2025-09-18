import unittest

from mechanics import ability_mod, proficiency_bonus, resolve_attack
from DiceController import DiceController


class Dummy:
    def __init__(self, attack=0):
        self.attack = attack


class Defender:
    def __init__(self, ac=10):
        self._ac = ac

    @property
    def ac(self):
        return self._ac


class TestMechanics(unittest.TestCase):
    def test_ability_mod(self):
        self.assertEqual(ability_mod(10), 0)
        self.assertEqual(ability_mod(12), 1)
        self.assertEqual(ability_mod(9), -1)
        self.assertEqual(ability_mod(1), -5)

    def test_proficiency(self):
        self.assertEqual(proficiency_bonus(1), 2)
        self.assertEqual(proficiency_bonus(5), 3)
        self.assertEqual(proficiency_bonus(9), 4)
        self.assertEqual(proficiency_bonus(13), 5)
        self.assertEqual(proficiency_bonus(20), 6)

    def test_roll_and_resolve(self):
        dc = DiceController()
        attacker = Dummy(attack=2)
        defender = Defender(ac=12)
        # force a hit by monkeypatching roll_d20 to return high
        dc.roll_d20 = lambda: 20
        hit, roll, total, dmg = resolve_attack(attacker, defender, dc)
        self.assertTrue(hit)
        self.assertEqual(roll, 20)
        self.assertEqual(total, 22)
        self.assertGreaterEqual(dmg, 0)


if __name__ == '__main__':
    unittest.main()
