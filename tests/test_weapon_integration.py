import unittest
from Player import Player
from weapon import Weapon
from DiceController import DiceController
from mechanics import resolve_attack


class FakeDice(DiceController):
    def __init__(self, d6=3, d8=5):
        self._d6 = d6
        self._d8 = d8

    def roll_d6(self):
        return self._d6

    def roll_d8(self):
        return self._d8

    def roll_d20(self):
        return 15


class DummyDefender:
    def __init__(self, ac=10):
        self._ac = ac

    @property
    def ac(self):
        return self._ac


class TestWeaponIntegration(unittest.TestCase):
    def test_player_weapon_used_for_damage(self):
        p = Player('Hero')
        p.equipped_weapon = Weapon('Short Sword', damage_die='d6')
        d = DummyDefender(ac=10)
        dice = FakeDice(d6=4)
        hit, roll, total, dmg = resolve_attack(p, d, dice)
        self.assertTrue(hit)
        self.assertEqual(dmg, 4)

    def test_player_weapon_critical(self):
        p = Player('Hero')
        p.equipped_weapon = Weapon('Rusty Spear', damage_die='d8')
        d = DummyDefender(ac=10)
        # fake dice that returns 20 for crit and d8=6
        class CritDice(FakeDice):
            def roll_d20(self):
                return 20

        dice = CritDice(d8=6)
        hit, roll, total, dmg = resolve_attack(p, d, dice)
        self.assertTrue(hit)
        self.assertEqual(dmg, 12)  # doubled d8


if __name__ == '__main__':
    unittest.main()
