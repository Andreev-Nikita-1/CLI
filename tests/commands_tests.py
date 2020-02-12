import unittest
import tempfile
from src.commands import *


class TestEcho(unittest.TestCase):
    def test_simple(self):
        self.assertEqual("a b c\n", echo(["a", "b", "c"]))

    def test_empty(self):
        self.assertEqual("\n", echo([]))


class TestCat(unittest.TestCase):
    def test_one(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("abc\n123")
        file.flush()
        self.assertEqual("abc\n123", cat([file.name]))
        file.close()
        os.unlink(file.name)

    def test_two(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("abc\n123")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w", delete=False)
        file2.write("def\n456")
        file2.flush()
        self.assertEqual("abc\n123def\n456", cat([file.name, file2.name]))
        file.close()
        file2.close()
        os.unlink(file.name)
        os.unlink(file2.name)


class TestWc(unittest.TestCase):
    def test_one(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("abc\n123")
        file.flush()
        self.assertEqual("2 2 8 " + file.name + "\n", wc([file.name]))
        file.close()
        os.unlink(file.name)

    def test_two(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("abc\n123")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w", delete=False)
        file2.write("def\n456")
        file2.flush()
        self.assertEqual("2 2 8 " + file.name + "\n2 2 8 " + file2.name + "\n", wc([file.name, file2.name]))
        file.close()
        file2.close()
        os.unlink(file.name)
        os.unlink(file2.name)


class TestGrep(unittest.TestCase):
    def test_simple(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("""abc def
ABC DEF
AbC DeF""")
        file.flush()
        self.assertEqual("abc def\n", grep(["def", file.name]))
        file.close()
        os.unlink(file.name)

    def test_case_ignoring(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("""abc def
ABC DEF
AbC DeF""")
        file.flush()
        self.assertEqual("""abc def
ABC DEF
AbC DeF
""", grep(["-i", "abc", file.name]))
        file.close()
        os.unlink(file.name)

    def test_full_words(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("""abc def
ABC DEF
AbC_DeF""")
        file.flush()
        self.assertEqual("""AbC_DeF
""", grep(["-i", "-w", "c.d", file.name]))
        file.close()
        os.unlink(file.name)

    def test_n_lines_after(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("""abc def
1 line
2 line
3 line
4 line
abc 2
line 1
line 2
line 3
line 4""")
        file.flush()
        self.assertEqual("""abc def
1 line
2 line
3 line

abc 2
line 1
line 2
line 3

""", grep(["-A", "3", "abc", file.name]))
        file.close()
        os.unlink(file.name)

    def test_two_files(self):
        file = tempfile.NamedTemporaryFile("w", delete=False)
        file.write("""abc
AXC
A C
""")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w", delete=False)
        file2.write("""a_c
a__c
""")
        file2.flush()
        self.assertEqual(file.name + ":\nabc\nAXC\n" + file2.name + ":\na_c\n",
                         grep(["-i", "-w", "a.c", file.name, file2.name]))
        file.close()
        file2.close()
        os.unlink(file.name)
        os.unlink(file2.name)
