import unittest

from Player import Player
from Monster import Monster


class TestModels(unittest.TestCase):
    def test_player_defaults(self):
        p = Player('Alice')
        self.assertEqual(p.get_stat('str'), 10)
        self.assertTrue(p.ac >= 9 and p.ac <= 11)
        self.assertTrue(p.health >= 1)

    def test_monster_defaults(self):
        m = Monster('Gob', level=1)
        self.assertTrue(m.ac >= 8 and m.ac <= 12)
        self.assertTrue(m.health >= 1)


if __name__ == '__main__':
    unittest.main()
