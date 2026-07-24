import unittest

import calc


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(calc.add(-1, 1), 0)


class TestPower(unittest.TestCase):
    def test_power(self):
        self.assertEqual(calc.power(2, 3), 8)

    def test_power_zero_exponent(self):
        self.assertEqual(calc.power(5, 0), 1)


if __name__ == "__main__":
    unittest.main()
