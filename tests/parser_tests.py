import unittest
from src.parser import *
from src.enviroment import *


class TestFindQuotes(unittest.TestCase):

    def test_no_quotes(self):
        self.assertEqual([], find_quotes("abcde"))

    def test_double_quotes(self):
        self.assertEqual([(2, 6, 'd')], find_quotes("12\"abc\"45"))

    def test_single_quotes(self):
        self.assertEqual([(2, 6, 's')], find_quotes("12\'abc\'45"))

    def test_inserted(self):
        self.assertEqual([(2, 8, 'd'), (11, 17, 's')], find_quotes("12\"a\'b\'c\"45\'ef\"gh\'"))


class TestTokenize(unittest.TestCase):
    def test_without_quotes(self):
        self.assertEqual(['echo 3 ', ' wc'], tokenize("echo 3 | wc", "\|"))

    def test_in_quotes(self):
        self.assertEqual(['echo 3 \"|\" wc'], tokenize("echo 3 \"|\" wc", "\|"))

    def test_double_quotes_disrespect(self):
        self.assertEqual(['echo 3 \"', '\" wc'], tokenize("echo 3 \"|\" wc", "\|", double_quotes_respect=False))


class TestInsertVars(unittest.TestCase):
    def setUp(self):
        add_value("x", "x_value")
        add_value("x_1", "x_1_value")

    def test_insert(self):
        self.assertEqual("x_value", insert_vars("$x"))

    def test_quotes(self):
        self.assertEqual("x_1 = \"x_1_value\", x_1 != \'$x_1\'", insert_vars("x_1 = \"$x_1\", x_1 != \'$x_1\'"))


class TestPeel(unittest.TestCase):
    def test_without_quotes(self):
        self.assertEqual("abc def", peel("abc def"))

    def test_combined_quotes(self):
        self.assertEqual("a\'bc de\"f", peel("\"a\'b\"c d\'e\"f\'"))


class TestParse(unittest.TestCase):
    def test_echo(self):
        self.assertEqual([['echo', '1']], parse("echo 1"))

    def test_echo_with_quotes(self):
        self.assertEqual([['echo', '1']], parse("\"ec\"\'ho\' 1"))

    def test_echo_with_variable(self):
        add_value("x", "1")
        self.assertEqual([['echo', '1']], parse("echo $x"))

    def test_echo_from_variable(self):
        add_value("x", "ec")
        add_value("y", "ho")
        self.assertEqual([['echo', '1']], parse("\"$x\"$y 1"))

    def test_echo_with_pipeline(self):
        self.assertEqual([['echo', '1'], ['wc']], parse("echo 1 | wc"))
