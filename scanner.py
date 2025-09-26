from token_type import TokenType
from token_class import Token

KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
}

class Scanner:
    def __init__(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.source_code = content
            self.pos = 0
            self.line = 1
            self.column = 1
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado.")
            self.source_code = ""
            self.pos = 0
            self.line = 1
            self.column = 1

    def peek_char(self) -> str | None:
        if self.pos >= len(self.source_code):
            return None
        return self.source_code[self.pos]

    def lexical_error(self, char: str) -> Token:
        """Imprime uma mensagem de erro formatada e retorna um token ILEGAL."""
        msg = f"Erro Léxico: Caractere inesperado '{char}' na linha {self.line}, coluna {self.column}."
        print(msg)
        return Token(TokenType.ILLEGAL, char)

    def next_token(self) -> Token | None:
        while not self.is_eof():
            current_char = self.next_char()

            if current_char in [' ', '\t', '\n', '\r']:
                continue

            if current_char == '#':
                self.skip_single_line_comment()
                continue

            if current_char == '/':
                if self.peek_char() == '*':
                    self.skip_multi_line_comment()
                    continue
                else:
                    return Token(TokenType.MATH_OPERATOR, "/")

            if self.is_letter(current_char):
                self.back()
                literal = self.read_identifier()
                token_type = KEYWORDS.get(literal, TokenType.IDENTIFIER)
                return Token(token_type, literal)
            
            if self.is_digit(current_char) or (current_char == '.' and self.is_digit(self.peek_char())):
                self.back()
                literal = self.read_number()
                return Token(TokenType.NUMBER, literal)

            if current_char == '=':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.EQUAL, "==")
                else:
                    return Token(TokenType.ASSIGN, "=")
            elif current_char == '>':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.GTE, ">=")
                else:
                    return Token(TokenType.GT, ">")
            elif current_char == '<':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.LTE, "<=")
                else:
                    return Token(TokenType.LT, "<")
            elif current_char == '!':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.NOT_EQUAL, "!=")
                else:
                    # --- CHAMANDO A FUNÇÃO DE ERRO ---
                    return self.lexical_error(current_char)
            elif current_char in ['+', '-', '*']:
                return Token(TokenType.MATH_OPERATOR, current_char)
            elif current_char == '(':
                return Token(TokenType.LPAREN, "(")
            elif current_char == ')':
                return Token(TokenType.RPAREN, ")")
            else:
                # --- CHAMANDO A FUNÇÃO DE ERRO PARA QUALQUER OUTRO CARACTERE ---
                return self.lexical_error(current_char)

        return None

    def skip_single_line_comment(self):
        while self.peek_char() not in ['\n', '\r', None]:
            self.next_char()

    def skip_multi_line_comment(self):
        self.next_char()
        while True:
            if self.is_eof():
                break
            if self.peek_char() == '*':
                self.next_char()
                if self.peek_char() == '/':
                    self.next_char()
                    break
            else:
                self.next_char()
    
    def read_number(self) -> str:
        start_pos = self.pos
        while self.is_digit(self.peek_char()):
            self.next_char()
        if self.peek_char() == '.':
            next_pos = self.pos + 1
            if next_pos < len(self.source_code) and self.is_digit(self.source_code[next_pos]):
                self.next_char()
                while self.is_digit(self.peek_char()):
                    self.next_char()
        return self.source_code[start_pos:self.pos]

    def read_identifier(self) -> str:
        start_pos = self.pos
        while self.is_letter(self.peek_char()) or self.is_digit(self.peek_char()):
            self.next_char()
        return self.source_code[start_pos:self.pos]

    def is_letter(self, c: str | None) -> bool:
        if c is None: return False
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def is_digit(self, c: str | None) -> bool:
        if c is None: return False
        return '0' <= c <= '9'
    
    def is_math_operator(self, c: str) -> bool:
        return c in ['+', '-', '*', '/']

    def next_char(self) -> str:
        if self.is_eof(): return '\0'
        
        char = self.source_code[self.pos]
        self.pos += 1

        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char

    def back(self):
        # Esta função é mais complexa de ajustar com linhas/colunas,
        # mas como a usamos antes de ler, a posição do erro ainda será correta.
        self.pos -= 1
        # Simplificação: não voltamos a coluna/linha aqui para evitar complexidade.
        # A posição do erro será a do caractere *após* o token.

    def is_eof(self) -> bool:
        return self.pos >= len(self.source_code)