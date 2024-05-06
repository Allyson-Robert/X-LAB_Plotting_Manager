import unittest
from utils.calc.iv_calc import split_forward_reverse


class TestSplitForwardReverse(unittest.TestCase):
    def test_unequal_length(self):
        independent = [1, 2, 3]
        dependent = [1, 2]
        with self.assertRaises(ValueError):
            split_forward_reverse(independent, dependent)

    def test_monotonically_increasing(self):
        independent = [1.1, 2.2, 3.3, 4.4]
        dependent = [0.1, 0.2, 0.3, 0.4]
        result = split_forward_reverse(independent, dependent)
        self.assertEqual(result, ([1.1, 2.2, 3.3, 4.4], [], [0.1, 0.2, 0.3, 0.4], []))

    def test_monotonically_decreasing(self):
        independent = [4.4, 3.3, 2.2, 1.1]
        dependent = [0.4, 0.3, 0.2, 0.1]
        result = split_forward_reverse(independent, dependent)
        self.assertEqual(result, ([], [4.4, 3.3, 2.2, 1.1], [], [0.4, 0.3, 0.2, 0.1]))

    def test_increase_then_decrease(self):
        independent = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2]
        dependent = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0]
        result = split_forward_reverse(independent, dependent)
        self.assertEqual(result, ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0.5, 0.4, 0.3, 0.2], [1.1, 2.2, 3.3, 4.4, 5.5, 6.6], [7.7, 8.8, 9.9, 10.0]))

    def test_unequal_length_increase_then_decrease(self):
        independent = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8]
        dependent = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2]
        with self.assertRaises(ValueError):
            split_forward_reverse(independent, dependent)

    def test_multiple_reversions(self):
        independent = [-1, 0, 1, 2, 1, 0, 1, 2, 1, 0]
        dependent = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        with self.assertRaises(ValueError):
            split_forward_reverse(independent, dependent)


if __name__ == '__main__':
    unittest.main()