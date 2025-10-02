from token_type import TokenType
from token_class import Token

# A "Tabela de Palavras Reservadas" exigida no projeto.
# Usamos um dicionário Python para mapear a string da palavra-chave
# para o seu tipo de token correspondente (TokenType)
KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
}

class Scanner:
    # A classe Scanner, também conhecida como Analisador Léxico, é responsável por
    # ler um arquivo de código-fonte caractere por caractere e convertê-lo em uma
    # sequência de tokens.

    def __init__(self, filename: str):
        # O construtor da classe. Ele abre e lê o arquivo de código-fonte,
        # e inicializa as variáveis de estado do analisador.
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.source_code = content
            self.pos = 0  # Posição atual no `source_code` (índice do próximo caractere a ser lido)
            
            # Contadores para rastrear a posição do erro para o usuário.
            self.line = 1
            self.column = 1
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado.")
            self.source_code = ""
            self.pos = 0
            self.line = 1
            self.column = 1

    def peek_char(self) -> str | None:
        # 'Espia' o próximo caractere no código-fonte sem avançar a posição (o cursor).
        # É essencial para decidir entre operadores de um ou dois caracteres (ex: '>' vs '>=').
        if self.pos >= len(self.source_code):
            return None
        return self.source_code[self.pos]

    def lexical_error(self, char: str) -> Token:
        # Função chamada quando um caractere inválido é encontrado.
        # Ela imprime uma mensagem de erro formatada com a linha e coluna
        # e retorna um token do tipo ILEGAL.
        msg = f"Erro Léxico: Caractere inesperado '{char}' na linha {self.line}, coluna {self.column}."
        print(msg)
        return Token(TokenType.ILLEGAL, char)

    def next_token(self) -> Token | None:
        # O método principal do analisador. A cada chamada, ele lê o código-fonte
        # e retorna o próximo token válido que encontrar, ignorando espaços e comentários.
        # Loop principal: continua procurando tokens até o fim do arquivo.
        while not self.is_eof():
            current_char = self.next_char()

            # --- 1. Ignorar caracteres não relevantes ---
            # Se for espaço em branco, simplesmente ignora e começa a próxima iteração do loop.
            if current_char in [' ', '\t', '\n', '\r']:
                continue

            # Se for o início de um comentário de linha única ('#'), chama a função para pular o resto da linha.
            if current_char == '#':
                self.skip_single_line_comment()
                continue # Volta ao início do loop para buscar o próximo token.

            # Se for o início de um comentário de múltiplas linhas ('/*'), chama a função para pular o bloco.
            if current_char == '/':
                if self.peek_char() == '*':
                    self.skip_multi_line_comment()
                    continue # Volta ao início do loop.
                else:
                    # Se for apenas '/', é o operador de divisão.
                    return Token(TokenType.MATH_OPERATOR, "/")

            # --- 2. Reconhecimento de Tokens ---
            # Se for uma letra ou underscore, é o início de um identificador ou palavra-chave.
            if self.is_letter(current_char):
                self.back() # Devolve o caractere para que `read_identifier` possa lê-lo.
                literal = self.read_identifier() # Lê a palavra completa.
                # Verifica na tabela se a palavra é reservada; se não, é um identificador comum.
                token_type = KEYWORDS.get(literal, TokenType.IDENTIFIER)
                return Token(token_type, literal)
            
            # Se for um dígito ou um ponto seguido de dígito, é um número.
            if self.is_digit(current_char) or (current_char == '.' and self.is_digit(self.peek_char())):
                self.back() # Devolve para que `read_number` processe o número completo.
                literal = self.read_number()
                return Token(TokenType.NUMBER, literal)

            # Lógica para operadores de atribuição e relacionais.
            # O padrão é: verificar o caractere e usar `peek_char()` para ver se é um operador duplo.
            if current_char == '=':
                if self.peek_char() == '=': # Verifica se é '=='
                    self.next_char() # Consome o segundo '='
                    return Token(TokenType.EQUAL, "==")
                else: # Se não, é apenas '='
                    return Token(TokenType.ASSIGN, "=")
            elif current_char == '>':
                if self.peek_char() == '=': # Verifica se é '>='
                    self.next_char()
                    return Token(TokenType.GTE, ">=")
                else: # Se não, é apenas '>'
                    return Token(TokenType.GT, ">")
            elif current_char == '<':
                if self.peek_char() == '=': # Verifica se é '<='
                    self.next_char()
                    return Token(TokenType.LTE, "<=")
                else: # Se não, é apenas '<'
                    return Token(TokenType.LT, "<")
            elif current_char == '!':
                if self.peek_char() == '=': # Verifica se é '!='
                    self.next_char()
                    return Token(TokenType.NOT_EQUAL, "!=")
                else: # '!' sozinho é um caractere ilegal nesta linguagem.
                    return self.lexical_error(current_char)
            
            # Operadores matemáticos simples de um caractere.
            elif current_char in ['+', '-', '*']:
                return Token(TokenType.MATH_OPERATOR, current_char)
            
            # Delimitadores (parênteses).
            elif current_char == '(':
                return Token(TokenType.LPAREN, "(")
            elif current_char == ')':
                return Token(TokenType.RPAREN, ")")
            
            # --- 3. Tratamento de Erro ---
            # Se o caractere não se encaixou em nenhuma regra acima, é um erro léxico.
            else:
                return self.lexical_error(current_char)

        # Se o loop terminar (fim do arquivo), retorna None para sinalizar o fim.
        return None

    def skip_single_line_comment(self):
        # Avança o cursor até encontrar uma quebra de linha, ignorando o comentário.
        while self.peek_char() not in ['\n', '\r', None]:
            self.next_char()

    def skip_multi_line_comment(self):
        # Avança o cursor até encontrar o delimitador '*/', ignorando o bloco de comentário.
        self.next_char() # Consome o '*' inicial do '/*'.
        while True:
            if self.is_eof(): # Previne loop infinito se o comentário não for fechado.
                break
            if self.peek_char() == '*':
                self.next_char() # Consome o '*'
                if self.peek_char() == '/':
                    self.next_char() # Consome o '/' final do '*/'
                    break
            else:
                self.next_char()
    
    def read_number(self) -> str:
        # Lê uma sequência de caracteres que formam um número (inteiro ou decimal).
        start_pos = self.pos
        # Lê a parte inteira do número.
        while self.is_digit(self.peek_char()):
            self.next_char()
        # Se encontrar um ponto, verifica se ele é seguido por um dígito para ser um decimal válido.
        if self.peek_char() == '.':
            next_pos = self.pos + 1 # Posição do caractere após o ponto.
            if next_pos < len(self.source_code) and self.is_digit(self.source_code[next_pos]):
                self.next_char() # Consome o ponto.
                # Lê a parte fracionária do número.
                while self.is_digit(self.peek_char()):
                    self.next_char()
        # Retorna a string completa do número que foi lido.
        return self.source_code[start_pos:self.pos]

    def read_identifier(self) -> str:
        # Lê uma sequência de caracteres que formam um identificador ou palavra-chave.
        start_pos = self.pos
        # Continua lendo enquanto o próximo caractere for válido para um identificador.
        while self.is_letter(self.peek_char()) or self.is_digit(self.peek_char()):
            self.next_char()
        # Retorna a string completa do identificador.
        return self.source_code[start_pos:self.pos]

    # --- Funções Auxiliares de Verificação ---
    def is_letter(self, c: str | None) -> bool:
        # Verifica se um caractere é uma letra ou underscore.
        if c is None: return False
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def is_digit(self, c: str | None) -> bool:
        # Verifica se um caractere é um dígito numérico.
        if c is None: return False
        return '0' <= c <= '9'

    def next_char(self) -> str:
        # Consome e retorna o próximo caractere do código-fonte e ATUALIZA os contadores de linha/coluna.
        if self.is_eof(): return '\0'
        
        char = self.source_code[self.pos]
        self.pos += 1

        # Atualiza a linha e a coluna para o relatório de erros.
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char

    def back(self):
        # Retrocede a posição em um caractere. Útil quando lemos um caractere a mais.
        self.pos -= 1
        # A coluna não é decrementada aqui para simplificar, pois `back` é usado
        # antes de uma leitura, e a posição do erro (que vem de `next_char`) será a correta.

    def is_eof(self) -> bool:
        # Verifica se o analisador chegou ao final do arquivo.
        return self.pos >= len(self.source_code)