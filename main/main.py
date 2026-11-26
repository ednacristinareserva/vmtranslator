import sys
from pathlib import Path

from parser.parser import Parser
from codewriter.codewriter import CodeWriter


def translate_file(input_file):
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {input_path}"
        )

    if input_path.suffix.lower() != ".vm":
        raise ValueError("O arquivo informado deve ter extensão .vm")

    output_path = input_path.with_suffix(".asm")

    parser = Parser(str(input_path))
    writer = CodeWriter(str(output_path))

    writer.setFileName(input_path.name)

    try:
        while parser.hasMoreCommands():
            parser.advance()

            command_type = parser.commandType()

            if command_type == "C_ARITHMETIC":
                writer.writeArithmetic(parser.arg1())

            elif command_type == "C_PUSH":
                writer.writePush(
                    parser.arg1(),
                    parser.arg2()
                )

            elif command_type == "C_POP":
                writer.writePop(
                    parser.arg1(),
                    parser.arg2()
                )

    finally:
        writer.close()

    print(f"Tradução concluída: {output_path}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m main.main caminho/arquivo.vm")
        sys.exit(1)

    try:
        translate_file(sys.argv[1])
    except (FileNotFoundError, ValueError) as error:
        print(f"Erro: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()