# Membros:
# Rafael Lucas Carlos Gonçalves
# João Victor Queiroz
# José Vieira Stable

from scanner import Scanner
from parser import Parser

def main():
    try:
        sc = Scanner("programa.mc")
        parser = Parser(sc)

        parser.parse_programa()

    except Exception as e:
        
        print(f"Erro de Compilação: {e}")

if __name__ == "__main__":
    main()