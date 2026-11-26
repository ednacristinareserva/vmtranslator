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


    def test_push_constant(self):
        self.writer.writePush("constant", 10)
        output = self.read_output()

        self.assertIn("// push constant 10", output)
        self.assertIn("@10", output)
        self.assertIn("D=A", output)

    def test_push_local(self):
        self.writer.writePush("local", 2)
        output = self.read_output()

        self.assertIn("@LCL", output)
        self.assertIn("@2", output)
        self.assertIn("A=D+A", output)

    def test_push_argument(self):
        self.writer.writePush("argument", 3)
        output = self.read_output()

        self.assertIn("@ARG", output)

    def test_push_this(self):
        self.writer.writePush("this", 1)
        output = self.read_output()

        self.assertIn("@THIS", output)

    def test_push_that(self):
        self.writer.writePush("that", 1)
        output = self.read_output()

        self.assertIn("@THAT", output)

    def test_push_temp(self):
        self.writer.writePush("temp", 2)
        output = self.read_output()

        self.assertIn("@7", output)

    def test_push_pointer(self):
        self.writer.writePush("pointer", 0)
        output = self.read_output()

        self.assertIn("@THIS", output)

    def test_push_static(self):
        self.writer.setFileName("Teste.vm")
        self.writer.writePush("static", 3)
        output = self.read_output()

        self.assertIn("@Teste.3", output)

    def test_pop_local(self):
        self.writer.writePop("local", 2)
        output = self.read_output()

        self.assertIn("@LCL", output)
        self.assertIn("@R13", output)
        self.assertIn("M=D", output)

    def test_pop_temp(self):
        self.writer.writePop("temp", 3)
        output = self.read_output()

        self.assertIn("@8", output)
        self.assertIn("@R13", output)

    def test_pop_pointer(self):
        self.writer.writePop("pointer", 1)
        output = self.read_output()

        self.assertIn("@THAT", output)

    def test_pop_static(self):
        self.writer.setFileName("Teste.vm")
        self.writer.writePop("static", 2)
        output = self.read_output()

        self.assertIn("@Teste.2", output)


if __name__ == "__main__":
    unittest.main()