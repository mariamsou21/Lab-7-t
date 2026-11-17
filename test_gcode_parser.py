import unittest
from gcode_parser import parse_line


class TestParseLine(unittest.TestCase):
    def test_g1_both_params(self):
        self.assertEqual(parse_line("G1 S47.847 E57.273"),
                         {"command": "G1", "params": {"S": 47.847, "E": 57.273}})

    def test_g1_shoulder_only(self):
        self.assertEqual(parse_line("G1 S90"),
                         {"command": "G1", "params": {"S": 90.0}})

    def test_g1_no_params(self):
        self.assertEqual(parse_line("G1"), {"command": "G1", "params": {}})

    def test_m_commands(self):
        for c in ("M3", "M5", "M18"):
            self.assertEqual(parse_line(c), {"command": c, "params": {}})

    def test_whitespace_and_newline(self):
        self.assertEqual(parse_line("   M3  \n")["command"], "M3")

    def test_blank_and_comment(self):
        self.assertIsNone(parse_line("   \n"))
        self.assertIsNone(parse_line("; just a comment"))

    def test_trailing_comment(self):
        self.assertEqual(parse_line("M5 ; pen up")["command"], "M5")


if __name__ == "__main__":
    unittest.main()
