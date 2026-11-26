class CodeWriter:

   # responsável por traduzir comandos VM para código Assembly Hack.
   # implementação inicial das operações aritméticas e lógicas.

    def __init__(self, output):
        if hasattr(output, "write"):
            self.output = output
            self.should_close = False
        else:
            self.output = open(output, "w", encoding="utf-8")
            self.should_close = True

        self.label_counter = 0

    def _write(self, code):
        self.output.write(code + "\n")

    def writeArithmetic(self, command):
        self._write(f"// {command}")

        # Operações binárias
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

        # Operações unárias
        elif command in ("neg", "not"):
            self._write("@SP")
            self._write("A=M-1")

            if command == "neg":
                self._write("M=-M")
            else:
                self._write("M=!M")

        # Operações de comparação
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

            # Resultado falso: 0
            self._write("@SP")
            self._write("A=M-1")
            self._write("M=0")

            self._write(f"@{end_label}")
            self._write("0;JMP")

            # Resultado verdadeiro: -1
            self._write(f"({true_label})")
            self._write("@SP")
            self._write("A=M-1")
            self._write("M=-1")

            self._write(f"({end_label})")

        else:
            raise ValueError(f"Comando aritmético desconhecido: {command}")

    def close(self):
        if self.should_close:
            self.output.close()