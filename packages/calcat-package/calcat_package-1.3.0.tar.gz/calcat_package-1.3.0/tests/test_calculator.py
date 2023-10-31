import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """
        Set up a Calculator instance before each test.
        """
        self.calc = Calculator()

    def test_addition(self):
        """
        Test the addition operation.
        """
        self.calc.add(2, 3)
        self.assertEqual(self.calc.memory, 5)

    def test_subtraction(self):
        """
        Test the subtraction operation.
        """
        self.calc.subtract(5, 3)
        self.assertEqual(self.calc.memory, 2)

    def test_multiplication(self):
        """
        Test the multiplication operation.
        """
        self.calc.multiply(2, 4)
        self.assertEqual(self.calc.memory, 8)

    def test_division(self):
        """
        Test the division operation.
        """
        self.calc.divide(10, 2)
        self.assertEqual(self.calc.memory, 5)

    def test_division_invalid(self):
        """
        Test division by zero handling.
        """
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertEqual(str(context.exception), "Division by zero is not allowed.")

    def test_exponentiation(self):
        """
        Test the exponentiation operation.
        """
        self.calc.power(2, 3)
        self.assertEqual(self.calc.memory, 8)

    def test_square_root(self):
        """
        Test the square root operation.
        """
        self.calc.root(16, 2)
        self.assertEqual(self.calc.memory, 4)

if __name__ == '__main__':
    unittest.main()