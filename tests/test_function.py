import random
import unittest
from function import Function

class FunctionTestCase(unittest.TestCase):
    def test_boolean_true(self):
        random.seed(1)
        function = Function('boolean', [], 0)
        self.assertEqual(function.run(), 'true', 'incorrect boolean value')
