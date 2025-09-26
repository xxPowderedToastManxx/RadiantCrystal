import unittest
from monster_factory import list_monsters, get_monster_by_index


class TestMonsterFactory(unittest.TestCase):
    def test_list_and_get(self):
        names = list_monsters()
        self.assertTrue(isinstance(names, list))
        if names:
            m = get_monster_by_index(0)
            self.assertIsNotNone(m)
            self.assertEqual(m.name, names[0])


if __name__ == '__main__':
    unittest.main()
