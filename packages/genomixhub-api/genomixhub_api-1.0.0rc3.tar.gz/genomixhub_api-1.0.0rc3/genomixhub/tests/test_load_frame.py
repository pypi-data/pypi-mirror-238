import unittest

from genomixhub import genomixhub as ghub


class TestLoadGenomixHub(unittest.TestCase):
    def test_load_frame_invalid(self):
        with self.assertRaises(TypeError):
            ghub.load(123)
        with self.assertRaises(TypeError):
            ghub.load("123")
        with self.assertRaises(ValueError):
            ghub.load([])
        with self.assertRaises(TypeError):
            ghub.load([10, 15])
        with self.assertRaises(ValueError):
            ghub.load(["black", "white"])
        with self.assertRaises(ValueError):
            ghub.load(["rsBlackbox", "rs456raptor"])


if __name__ == "__main__":
    unittest.main()
