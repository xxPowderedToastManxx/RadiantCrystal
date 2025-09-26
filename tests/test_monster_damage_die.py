import unittest
from Monster import Monster


class FakeDice:
    def __init__(self, values):
        self._values = list(values)

    def roll_d4(self):
        return self._values.pop(0)

    def roll_d6(self):
        return self._values.pop(0)

    def roll_d8(self):
        return self._values.pop(0)

    def roll_d10(self):
        return self._values.pop(0)

    def roll_d12(self):
        return self._values.pop(0)

    def roll_d20(self):
        return self._values.pop(0)


class TestMonsterDamageDie(unittest.TestCase):
    def test_damage_die_spec_d4(self):
        m = Monster('Test', damage_die_spec='d4')
        fake = FakeDice([3])
        self.assertEqual(m.damage_die_with_controller(fake), 3)

    def test_damage_die_spec_d8(self):
        m = Monster('Test', damage_die_spec='d8')
        fake = FakeDice([7])
        self.assertEqual(m.damage_die_with_controller(fake), 7)

    def test_damage_die_default(self):
        m = Monster('Test')
        fake = FakeDice([5])
        self.assertEqual(m.damage_die_with_controller(fake), 5)


if __name__ == '__main__':
    unittest.main()
