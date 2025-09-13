# scanner.py

from token_type import TokenType
from token_class import Token

class Scanner:
    def __init__(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            # Em Python, é mais fácil trabalhar com a string diretamente
            self.source_code = content
            self.pos = 0
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado.")
            self.source_code = ""
            self.pos = 0

    def next_token(self) -> Token | None:
        """
        Esta função replica a máquina de estados do código Java original.
        OBS: O código original do professor SÓ reconhece identificadores e
        ignora todos os outros caracteres (números, operadores, espaços).
        """
        content = ""
        state = 0
        
        while True:
            if self.is_eof():
                # Se chegamos ao fim do arquivo e ainda estamos em um estado
                # intermediário (como lendo um identificador), precisamos finalizá-lo.
                if state == 1: # Estava lendo um identificador
                    return Token(TokenType.IDENTIFIER, content)
                return None # Fim do arquivo

            current_char = self.next_char()
            
            # A estrutura switch-case do Java é substituída por if/elif/else
            if state == 0:
                if self.is_letter(current_char):
                    content += current_char
                    state = 1
                # IMPORTANTE: O código original não trata espaços, números, etc.
                # Ele simplesmente os ignora, continuando no estado 0.
                
            elif state == 1:
                if self.is_letter(current_char) or self.is_digit(current_char):
                    content += current_char
                    # Permanece no estado 1
                else:
                    # Encontrou um caractere que não pertence ao identificador
                    state = 2
            
            elif state == 2:
                self.back() # Devolve o último caractere lido para o buffer
                return Token(TokenType.IDENTIFIER, content)

    def is_letter(self, c: str) -> bool:
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z'

    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'
    
    # (Não usadas no código original para identificadores, mas traduzidas para referência)
    def is_math_operator(self, c: str) -> bool:
        return c in ['+', '-', '*', '/']

    def is_rel_operator(self, c: str) -> bool:
        return c in ['>', '<', '=', '!']

    def next_char(self) -> str:
        char = self.source_code[self.pos]
        self.pos += 1
        return char

    def back(self):
        self.pos -= 1

    def is_eof(self) -> bool:
        return self.pos >= len(self.source_code)