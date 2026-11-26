class CodeWriter:
   # responsável por traduzir comandos VM para código Assembly Hack;
   # implementação inicial das operações aritméticas e lógicas.

    def __init__(self, output):
        if hasattr(output, "write"):
            self.output = output
            self.should_close = False
        else:
            self.output = open(output, "w", encoding="utf-8")
            self.should_close = True

        self.label_counter = 0
        self.file_name = "Static"

    def _write(self, code):
        self.output.write(code + "\n")

    def setFileName(self, filename):
        self.file_name = filename.replace("\\", "/").split("/")[-1]
        if self.file_name.endswith(".vm"):
            self.file_name = self.file_name[:-3]

    def writeArithmetic(self, command):
        self._write(f"// {command}")

        if command in ("add", "sub", "and", "or"):
            self._write("@SP")
            self._write("AM=M-1")
            self._write("D=M")
            self._write("A=A-1")

            operations = {
                "add": "M=D+M",
                "sub": "M=M-D",
                "and": "M=D&M",
                "or": "M=D|M"
            }

            self._write(operations[command])

        elif command in ("neg", "not"):
            self._write("@SP")
            self._write("A=M-1")

            if command == "neg":
                self._write("M=-M")
            else:
                self._write("M=!M")

        elif command in ("eq", "gt", "lt"):
            self._write("@SP")
            self._write("AM=M-1")
            self._write("D=M")
            self._write("A=A-1")
            self._write("D=M-D")

            true_label = f"TRUE_{self.label_counter}"
            end_label = f"END_{self.label_counter}"
            self.label_counter += 1

            jump_commands = {
                "eq": "JEQ",
                "gt": "JGT",
                "lt": "JLT"
            }

            self._write(f"@{true_label}")
            self._write(f"D;{jump_commands[command]}")

            self._write("@SP")
            self._write("A=M-1")
            self._write("M=0")

            self._write(f"@{end_label}")
            self._write("0;JMP")

            self._write(f"({true_label})")
            self._write("@SP")
            self._write("A=M-1")
            self._write("M=-1")

            self._write(f"({end_label})")

        else:
            raise ValueError(f"Comando aritmético desconhecido: {command}")

    def writePush(self, segment, index):
        self._write(f"// push {segment} {index}")

        if segment == "constant":
            self._write(f"@{index}")
            self._write("D=A")

        elif segment in ("local", "argument", "this", "that"):
            base = {
                "local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"
            }[segment]

            self._write(f"@{base}")
            self._write("D=M")
            self._write(f"@{index}")
            self._write("A=D+A")
            self._write("D=M")

        elif segment == "temp":
            self._write(f"@{5 + index}")
            self._write("D=M")

        elif segment == "pointer":
            address = "THIS" if index == 0 else "THAT"
            self._write(f"@{address}")
            self._write("D=M")

        elif segment == "static":
            self._write(f"@{self.file_name}.{index}")
            self._write("D=M")

        else:
            raise ValueError(f"Segmento inválido: {segment}")

        self._write("@SP")
        self._write("A=M")
        self._write("M=D")
        self._write("@SP")
        self._write("M=M+1")

    def writePop(self, segment, index):
        self._write(f"// pop {segment} {index}")

        if segment in ("local", "argument", "this", "that"):
            base = {
                "local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"
            }[segment]

            self._write(f"@{base}")
            self._write("D=M")
            self._write(f"@{index}")
            self._write("D=D+A")
            self._write("@R13")
            self._write("M=D")

        elif segment == "temp":
            self._write(f"@{5 + index}")
            self._write("D=A")
            self._write("@R13")
            self._write("M=D")

        elif segment == "pointer":
            address = "THIS" if index == 0 else "THAT"
            self._write(f"@{address}")
            self._write("D=A")
            self._write("@R13")
            self._write("M=D")

        elif segment == "static":
            self._write(f"@{self.file_name}.{index}")
            self._write("D=A")
            self._write("@R13")
            self._write("M=D")

        else:
            raise ValueError(f"Segmento inválido para pop: {segment}")

        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M")
        self._write("@R13")
        self._write("A=M")
        self._write("M=D")

    def close(self):
        if self.should_close:
            self.output.close()