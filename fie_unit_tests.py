# File: fie_unit_tests.py

import unittest
import fiecommands as cmds

class TestFieBotCommands(unittest.TestCase):

    def test_solve(self):
        cmd = "fie solve"
        op_tests = [
            (f"{cmd} sqrt 121", "The result is 11.0!"),
            (f"{cmd} average 5 7 9 11", "The result is 8.0!"),
            (f"{cmd} 3 * 5", "The result is 15.0!"),
            (f"{cmd} 4 +", "Hey dummy, your operation '4 +' is malformed."),
            (f"{cmd} 9 + 3 + 7", "Hey, my brain can only do so much at once! Give me a break :slight_frown:"),
            (f"{cmd} 5 !", "The result is 120!")
        ]

        for test in op_tests:
            self.assertEqual(cmds.fie_solve(test[0]), test[1])
