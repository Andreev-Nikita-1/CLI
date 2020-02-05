import unittest
import tempfile
from src.commands import *


class TestCommands(unittest.TestCase):
    def test_echo(self):
        self.assertEqual("a b c", echo(["a", "b", "c"]))

    def test_cat(self):
        file = tempfile.NamedTemporaryFile("w")
        file.write("abc\n123")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w")
        file2.write("def\n456")
        file2.flush()
        self.assertEqual("abc\n123def\n456", cat([file.name, file2.name]))
        file.close()
        file2.close()

    def test_wc(self):
        file = tempfile.NamedTemporaryFile("w")
        file.write("abc\n123")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w")
        file2.write("def\n456")
        file2.flush()
        self.assertEqual("2 2 7 " + file.name + "\n2 2 7 " + file2.name + "\n", wc([file.name, file2.name]))
        file.close()
        file2.close()
