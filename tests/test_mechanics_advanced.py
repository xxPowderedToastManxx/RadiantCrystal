import unittest
from DiceController import DiceController
from mechanics import roll_d20, resolve_attack


class FakeDice:
    def __init__(self, seq):
        # seq is an iterable of values to return for consecutive roll_d20 calls
        self._iter = iter(seq)

    def roll_d20(self):
        try:
            return next(self._iter)
        except StopIteration:
            return 1

    def roll_d6(self):
        return 3


class Attacker:
    def __init__(self, atk=2):
        self.attack = atk

    def damage_die(self):
        return 4


class Defender:
    def __init__(self, ac=10):
        self._ac = ac

    @property
    def ac(self):
        return self._ac


class TestMechanicsAdvanced(unittest.TestCase):
    def test_critical_hit_natural_20(self):
        dice = FakeDice([20])
        a = Attacker(atk=2)
        d = Defender(ac=15)
        hit, roll, total, dmg = resolve_attack(a, d, dice)
        self.assertTrue(hit)
        self.assertEqual(roll, 20)
        # damage should be doubled (damage_die called twice) -> 8
        self.assertEqual(dmg, 8)

    def test_natural_1_miss(self):
        dice = FakeDice([1])
        a = Attacker(atk=10)
        d = Defender(ac=5)
        hit, roll, total, dmg = resolve_attack(a, d, dice)
        self.assertFalse(hit)
        self.assertEqual(roll, 1)
        self.assertEqual(dmg, 0)

    def test_advantage_chooses_high(self):
        dice = FakeDice([7, 14])
        # roll_d20 will be called and roll_d20(dice, advantage) will pick 14 as best
        best, other = roll_d20(dice, advantage=1)
        self.assertEqual(best, 14)

    def test_disadvantage_chooses_low(self):
        dice = FakeDice([7, 14])
        best, other = roll_d20(dice, advantage=-1)
        self.assertEqual(best, 7)


if __name__ == '__main__':
    unittest.main()
