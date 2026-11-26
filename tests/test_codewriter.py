import os
import tempfile
import unittest

from codewriter.codewriter import CodeWriter


class TestCodeWriter(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".asm",
            encoding="utf-8",
            delete=False
        )
        self.temp.close()

        self.writer = CodeWriter(self.temp.name)

    def tearDown(self):
        self.writer.close()
        os.remove(self.temp.name)

    def read_output(self):
        self.writer.output.flush()

        with open(self.temp.name, "r", encoding="utf-8") as file:
            return file.read()

    def test_add(self):
        self.writer.writeArithmetic("add")
        output = self.read_output()

        self.assertIn("// add", output)
        self.assertIn("M=D+M", output)

    def test_sub(self):
        self.writer.writeArithmetic("sub")
        output = self.read_output()

        self.assertIn("M=M-D", output)

    def test_neg(self):
        self.writer.writeArithmetic("neg")
        output = self.read_output()

        self.assertIn("M=-M", output)

    def test_not(self):
        self.writer.writeArithmetic("not")
        output = self.read_output()

        self.assertIn("M=!M", output)

    def test_and(self):
        self.writer.writeArithmetic("and")
        output = self.read_output()

        self.assertIn("M=D&M", output)

    def test_or(self):
        self.writer.writeArithmetic("or")
        output = self.read_output()

        self.assertIn("M=D|M", output)

    def test_comparisons(self):
        for command in ("eq", "gt", "lt"):
            with self.subTest(command=command):
                self.writer.writeArithmetic(command)

        output = self.read_output()

        self.assertIn("D;JEQ", output)
        self.assertIn("D;JGT", output)
        self.assertIn("D;JLT", output)
        self.assertIn("M=-1", output)
        self.assertIn("M=0", output)

    def test_unknown_command(self):
        with self.assertRaises(ValueError):
            self.writer.writeArithmetic("invalid")


if __name__ == "__main__":
    unittest.main()