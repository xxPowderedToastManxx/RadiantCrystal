
import unittest

from DiceController import DiceController



class UnitTester(unittest.TestCase):

    def __init__(self):
        # super().__init__(methodName)

        self.dice_controller = DiceController()


    def roll_test(self):

       # def test_all(self):
         #   return self.result
        
        # def test_d4(self):

        def test_upper(self):
            self.assertEqual('foo'.upper(), 'FOO')

        result = self.dice_controller.roll_d4()
        print(result)
        self.assertTrue(1 <= result <= 4, "Generated number is outside expected range")

        # return self.result
            
unit_test = UnitTester()

if __name__ == '__main__':
    unittest.main(unit_test.roll_test())
    
    