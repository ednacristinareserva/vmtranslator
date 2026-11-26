import os
import tempfile
import unittest

from parser.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".vm",
            encoding="utf-8",
            delete=False
        )

        self.temp.write("""
            // Comentário
            push constant 10
            push local 0
            add
            pop argument 2 // Comentário final
            sub
            not
        """)

        self.temp.close()
        self.parser = Parser(self.temp.name)

    def tearDown(self):
        os.remove(self.temp.name)

    def test_has_more_commands(self):
        self.assertTrue(self.parser.hasMoreCommands())

    def test_push_command(self):
        self.parser.advance()

        self.assertEqual(self.parser.commandType(), "C_PUSH")
        self.assertEqual(self.parser.arg1(), "constant")
        self.assertEqual(self.parser.arg2(), 10)

    def test_arithmetic_command(self):
        self.parser.advance()
        self.parser.advance()
        self.parser.advance()

        self.assertEqual(self.parser.commandType(), "C_ARITHMETIC")
        self.assertEqual(self.parser.arg1(), "add")

    def test_pop_command(self):
        for _ in range(4):
            self.parser.advance()

        self.assertEqual(self.parser.commandType(), "C_POP")
        self.assertEqual(self.parser.arg1(), "argument")
        self.assertEqual(self.parser.arg2(), 2)

    def test_comments_are_ignored(self):
        self.assertEqual(len(self.parser.commands), 6)

    def test_arg2_on_arithmetic_raises_error(self):
        self.parser.advance()
        self.parser.advance()
        self.parser.advance()

        with self.assertRaises(ValueError):
            self.parser.arg2()


if __name__ == "__main__":
    unittest.main()