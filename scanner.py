import re
from token_type import TokenType
from token_class import Token

KEYWORDS = {
    "function": TokenType.FUNCTION,
    "main": TokenType.MAIN,
    "let": TokenType.LET,
    "const": TokenType.CONST,
    "number": TokenType.NUMBER,
    "float": TokenType.FLOAT,
    "read": TokenType.READ,
    "console.log": TokenType.CONSOLE_LOG,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
}

VALID_NUMBER_REGEX = re.compile(r"^(\d+(\.\d+)?|\.\d+)$")

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

    def lexical_error(self, char_or_msg: str, is_char: bool = True) -> Token:
        """Imprime uma mensagem de erro formatada e retorna um token ILEGAL."""
        if is_char:
            msg = f"Erro Léxico: Caractere inesperado '{char_or_msg}' na linha {self.line}, coluna {self.column}."
            print(msg)
            return Token(TokenType.ILLEGAL, char_or_msg)
        else:
            msg = f"Erro Léxico: {char_or_msg} na linha {self.line}."
            print(msg)
            return Token(TokenType.ILLEGAL, char_or_msg)

    def next_token(self) -> Token | None:
        """O cérebro do scanner. Lê o código e retorna o PRÓXIMO token."""
        
        while not self.is_eof():
            current_char = self.next_char()

            # --- Ignorar Espaços e Comentários ---
            if current_char in [' ', '\t', '\n', '\r']:
                continue
            if current_char == '#':
                self.skip_single_line_comment()
                continue
            
            # --- CORREÇÃO: Adicionado suporte para comentários // ---
            if current_char == '/':
                if self.peek_char() == '*':      # Se for /*
                    self.skip_multi_line_comment()
                    continue
                elif self.peek_char() == '/':    # Se for //
                    self.skip_single_line_comment()
                    continue
                else:                            # Se for apenas /
                    return Token(TokenType.SLASH, "/") # Operador de divisão

            # --- 3. RECONHECIMENTO DE TOKENS DA GRAMÁTICA ---

            # Identificadores e Palavras-chave
            if self.is_letter(current_char):
                self.back()
                return self.read_identifier() 

            # Números (Inteiros ou Reais)
            if self.is_digit(current_char) or (current_char == '.' and self.is_digit(self.peek_char())):
                self.back()
                return self.read_number() 

            # Cadeias (Strings)
            if current_char == '"':
                return self.read_string() 

            # Operadores Relacionais e Atribuição
            if current_char == '=':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.OP_REL, "==")
                else:
                    return Token(TokenType.ASSIGN, "=")
            elif current_char == '>':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.OP_REL, ">=")
                else:
                    return Token(TokenType.OP_REL, ">")
            elif current_char == '<':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.OP_REL, "<=")
                else:
                    return Token(TokenType.OP_REL, "<")
            elif current_char == '!':
                if self.peek_char() == '=':
                    self.next_char()
                    return Token(TokenType.OP_REL, "!=")
                else:
                    return self.lexical_error(current_char)

            # Operadores Lógicos
            elif current_char == '&':
                if self.peek_char() == '&':
                    self.next_char()
                    return Token(TokenType.OP_LOGICO, "&&")
                else:
                    return self.lexical_error(current_char)
            elif current_char == '|':
                if self.peek_char() == '|':
                    self.next_char()
                    return Token(TokenType.OP_LOGICO, "||")
                else:
                    return self.lexical_error(current_char)

            # --- CORREÇÃO: Operadores Matemáticos separados ---
            elif current_char == '+':
                return Token(TokenType.PLUS, "+")
            elif current_char == '-':
                return Token(TokenType.MINUS, "-")
            elif current_char == '*':
                return Token(TokenType.ASTERISK, "*")
            
            # --- NOVO: Adicionado o operador Módulo (%) ---
            elif current_char == '%':
                return Token(TokenType.MODULO, "%")

            # Delimitadores
            elif current_char == '(':
                return Token(TokenType.LPAREN, "(")
            elif current_char == ')':
                return Token(TokenType.RPAREN, ")")
            elif current_char == '{':
                return Token(TokenType.LBRACE, "{")
            elif current_char == '}':
                return Token(TokenType.RBRACE, "}")
            elif current_char == ';':
                return Token(TokenType.SEMICOLON, ";")
            elif current_char == ':':
                return Token(TokenType.COLON, ":")

            # Se não for nada disso, é um erro
            else:
                return self.lexical_error(current_char)

        return Token(TokenType.EOF, "") # Fim do arquivo

    # --- Funções de Leitura Especializada ---

    def read_identifier(self) -> Token:
        """Lê um identificador completo e decide se é uma ID ou Palavra-chave."""
        start_pos = self.pos
        while self.is_letter(self.peek_char()) or self.is_digit(self.peek_char()):
            self.next_char()
        
        literal = self.source_code[start_pos:self.pos]
        
        # Lógica especial para 'console.log'
        if literal == "console" and self.peek_char() == '.':
            self.next_char() # Consome o '.'
            if self.source_code[self.pos:self.pos+3] == "log":
                self.pos += 3
                literal = "console.log"
        
        token_type = KEYWORDS.get(literal, TokenType.ID)
        return Token(token_type, literal)

    def read_number(self) -> Token:
        """
        Lê um número (inteiro ou float) de forma "gananciosa" e o valida.
        Correção para o bug '1.1.1.1'.
        """
        start_pos = self.pos
        
        while self.is_digit(self.peek_char()) or self.peek_char() == '.':
            self.next_char()
            
        literal = self.source_code[start_pos:self.pos]
        
        if VALID_NUMBER_REGEX.match(literal):
            if '.' in literal:
                return Token(TokenType.NUMREAL, literal)
            else:
                return Token(TokenType.NUMINT, literal)
        else:
            col = self.column - len(literal)
            print(f"Erro Léxico: Constante numérica malformada '{literal}' na linha {self.line}, coluna {col}.")
            return Token(TokenType.ILLEGAL, literal)

    def read_string(self) -> Token:
        """Lê uma cadeia de caracteres (string) entre aspas."""
        start_pos = self.pos # Posição *depois* do " de abertura
        
        while self.peek_char() != '"' and not self.is_eof():
            self.next_char()
            
        if self.is_eof():
            return self.lexical_error("String não fechada", is_char=False)
            
        literal = self.source_code[start_pos:self.pos]
        
        self.next_char() # Consome o " de fechamento
        return Token(TokenType.CADEIA, literal)

    # --- Funções Auxiliares (sem mudanças) ---

    def skip_single_line_comment(self):
        while self.peek_char() not in ['\n', '\r', None]:
            self.next_char()

    def skip_multi_line_comment(self):
        self.next_char() # consome o '*'
        while True:
            if self.is_eof():
                self.lexical_error("Comentário de múltiplas linhas não fechado", is_char=False)
                break
            if self.peek_char() == '*':
                self.next_char()
                if self.peek_char() == '/':
                    self.next_char()
                    break
            else:
                self.next_char()

    def is_letter(self, c: str | None) -> bool:
        if c is None: return False
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def is_digit(self, c: str | None) -> bool:
        if c is None: return False
        return '0' <= c <= '9'

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
        """Retrocede a posição."""
        if self.pos > 0:
            self.pos -= 1
            if self.column > 1:
                self.column -= 1

    def is_eof(self) -> bool:
        return self.pos >= len(self.source_code)