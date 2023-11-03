import unittest

from genomixhub import genomixhub as ghub


class TestDevGenomixHub(unittest.TestCase):
    def test_load_frame_dev_valid(self):
        frame = ghub.load(["rs123", "rs456"])
        self.assertIsNotNone(frame)
        self.assertIsInstance(frame, ghub._GenomixHubFrameDev)

    def test_mock_frame_dev(self):
        frame = ghub.load(["rs123", "rs456"])
        self.assertIsNotNone(frame)
        self.assertIsInstance(frame, ghub._GenomixHubFrameDev)

        with self.assertRaises(TypeError):
            frame.mock(["rs123", "rs456"])

        with self.assertRaises(TypeError):
            frame.mock({"rs123": [], "rs456": 31})

        with self.assertRaises(ValueError):
            frame.mock({"rs123": "BA", "rs456": "KT"})

        frame.mock({"rs123": "AT", "rs456": "DI"})

        with self.assertRaises(ValueError):
            frame.get_value("rs789")

        self.assertEqual("AT", frame.get_value("rs123"))
        self.assertEqual("DI", frame.get_value("rs456"))

    def test_get_value_frame_dev(self):
        frame = ghub.load(["rs123", "rs456"])
        frame.mock({"rs123": "AT"})
        self.assertEqual("AT", frame.get_value("rs123"))
        self.assertIsNone(frame.get_value("rs456"))

        with self.assertRaises(ValueError):
            frame.get_value("rs4242")


if __name__ == "__main__":
    unittest.main()
