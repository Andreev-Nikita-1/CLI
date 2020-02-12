import unittest
import tempfile
from src.interpreter import perform
from src.parser import parse
from src.enviroment import *


class TestInterpreter(unittest.TestCase):
    def test_echo(self):
        self.assertEqual("1\n", perform(parse("echo 1")))

    def test_add_variable(self):
        perform(parse("x=5"))
        self.assertEqual("5", get_value("x"))

    def test_read_variable(self):
        add_value("x", "5")
        self.assertEqual("5\n", perform(parse("echo $x")))

    def test_pipeline(self):
        self.assertEqual("1 1 4\n", perform(parse("echo 123 | wc")))

    def test_cat_file(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("abc\n123")
        file.flush()
        add_value("x", file.name)
        self.assertEqual("abc\n123", perform(parse("cat $x")))
        file.close()
        os.unlink(file.name)

    def test_echo_pipe_grep(self):
        self.assertEqual("1234\n", perform(parse("echo 1234 | grep 23")))
