class Parser:

    ARITHMETIC_COMMANDS = {
        "add", "sub", "neg",
        "eq", "gt", "lt",
        "and", "or", "not"
    }

    MEMORY_SEGMENTS = {
        "constant", "local", "argument",
        "this", "that", "temp", "pointer", "static"
    }

    def __init__(self, filename):
        self.commands = []
        self.index = -1
        self.tokens = []
        self.line_number = None

        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.split("//")[0].strip()

                if line:
                    self.commands.append({
                        "tokens": line.split(),
                        "line": line_number
                    })

    def hasMoreCommands(self):
        return self.index + 1 < len(self.commands)

    def advance(self):
        if not self.hasMoreCommands():
            raise StopIteration("Não existem mais comandos.")

        self.index += 1
        current = self.commands[self.index]

        self.tokens = current["tokens"]
        self.line_number = current["line"]

    def commandType(self):
        if not self.tokens:
            raise ValueError("Nenhum comando selecionado.")

        command = self.tokens[0]

        if command in self.ARITHMETIC_COMMANDS:
            if len(self.tokens) != 1:
                raise ValueError(
                    f"Comando inválido na linha {self.line_number}."
                )
            return "C_ARITHMETIC"

        if command in ("push", "pop"):
            if len(self.tokens) != 3:
                raise ValueError(
                    f"Comando inválido na linha {self.line_number}."
                )

            segment = self.tokens[1]

            if segment not in self.MEMORY_SEGMENTS:
                raise ValueError(
                    f"Segmento inválido na linha {self.line_number}: {segment}"
                )

            if command == "pop" and segment == "constant":
                raise ValueError(
                    f"Não é permitido pop constant na linha {self.line_number}."
                )

            self.arg2()

            if command == "push":
                return "C_PUSH"

            return "C_POP"

        raise ValueError(
            f"Comando desconhecido na linha {self.line_number}: {command}"
        )

    def arg1(self):
        command_type = self.commandType()

        if command_type == "C_ARITHMETIC":
            return self.tokens[0]

        return self.tokens[1]

    def arg2(self):
        if len(self.tokens) != 3 or self.tokens[0] not in ("push", "pop"):
            raise ValueError("arg2() só pode ser usado com push ou pop.")

        try:
            index = int(self.tokens[2])
        except ValueError:
            raise ValueError(
                f"Índice inválido na linha {self.line_number}."
            )

        if index < 0:
            raise ValueError(
                f"Índice negativo na linha {self.line_number}."
            )

        segment = self.tokens[1]

        if segment in ("temp", "pointer") and index > (7 if segment == "temp" else 1):
            raise ValueError(
                f"Índice fora do limite para {segment} na linha {self.line_number}."
            )

        return index