import unittest
from nep import sep

class Testsep(unittest.TestCase):
    def test_search(self):
        self.assertEqual(sep(22009), 2)

if __name__ == "__main__":
    unittest.main()