from token_type import TokenType

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance() # Inicia o first token

    def advance(self):
        """ Pega o próximo token do scanner """
        self.current_token = self.scanner.next_token()
        # Pula tokens ilegais (se o léxico os reportar)
        while self.current_token and self.current_token.type == TokenType.ILLEGAL:
            print(f"AVISO LÉXICO (ignorado): Token ilegal '{self.current_token.text}'")
            self.current_token = self.scanner.next_token()

    def consume(self, expected_type):
        """ Consome o token atual se for do tipo esperado """
        if self.current_token and self.current_token.type == expected_type:
            self.advance()
        else:
            # Erro Sintático!
            raise Exception(f"Erro Sintático: Esperado {expected_type}, mas encontrou {self.current_token.type if self.current_token else 'EOF'}")

    def parse_programa(self):
        self.consume(TokenType.FUNCTION)
        self.consume(TokenType.MAIN)
        self.consume(TokenType.LPAREN)
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)
        self.parse_corpo() # Chama a função da próxima regra
        self.consume(TokenType.RBRACE)
        if self.current_token.type != TokenType.EOF:
            raise Exception(f"Erro Sintático: Lixo encontrado após o '}}' final: {self.current_token.type}")
        print("Parse concluído com sucesso!")

    def parse_corpo(self):
        self.parse_declaracoes()
        self.parse_comandos()

    def parse_declaracoes(self):
        while self.current_token and self.current_token.type in [TokenType.LET, TokenType.CONST]:
            self.parse_declaracao()
            
    def parse_declaracao(self):
        if self.current_token.type == TokenType.LET:
            self.consume(TokenType.LET)
        elif self.current_token.type == TokenType.CONST:
            self.consume(TokenType.CONST)
        
        self.consume(TokenType.ID)
        self.consume(TokenType.COLON)
        self.parse_tipo() # Chama a função para 'tipo'
        self.consume(TokenType.SEMICOLON)

    def parse_tipo(self):
        if self.current_token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
        elif self.current_token.type == TokenType.FLOAT:
            self.consume(TokenType.FLOAT)
        else:
            raise Exception(f"Erro Sintático: Tipo desconhecido '{self.current_token.text}'")

    def parse_expressaoAritmetica(self):
        self.parse_termo()
        self.parse_expressaoAritmetica_linha()
        
    def parse_expressaoAritmetica_linha(self):
        if self.current_token and self.current_token.type == TokenType.PLUS:
            self.consume(TokenType.PLUS)
            self.parse_termo()
            self.parse_expressaoAritmetica_linha() # Chamada recursiva
        elif self.current_token and self.current_token.type == TokenType.MINUS:
            self.consume(TokenType.MINUS)
            self.parse_termo()
            self.parse_expressaoAritmetica_linha() # Chamada recursiva
        else:
            pass # Caso Vazio (ε)

    def parse_comandos(self):
        tokens_de_inicio = [
            TokenType.ID, 
            TokenType.READ, 
            TokenType.CONSOLE_LOG,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.LBRACE
        ]
        
        while self.current_token and self.current_token.type in tokens_de_inicio:
            self.parse_comando()

    def parse_comando(self):
        token_type = self.current_token.type
        
        if token_type == TokenType.ID:
            self.parse_atribuicao()
        elif token_type == TokenType.READ:
            self.parse_leitura()
        elif token_type == TokenType.CONSOLE_LOG:
            self.parse_escrita()
        elif token_type == TokenType.IF:
            self.parse_condicional()
        elif token_type == TokenType.WHILE:
            self.parse_repeticao()
        elif token_type == TokenType.LBRACE:
            self.parse_blocoInterno()
        else:
            raise Exception(f"Erro Sintático: Comando inesperado iniciado com {token_type}")

    def parse_atribuicao(self):
        print("Parse: Atribuição") # (Temporário para debug)
        self.consume(TokenType.ID)
        self.consume(TokenType.ASSIGN)
        self.parse_expressaoAritmetica()
        self.consume(TokenType.SEMICOLON)

    def parse_leitura(self):
        print("Parse: Leitura") # (Temporário para debug)
        self.consume(TokenType.READ)
        self.consume(TokenType.LPAREN)
        self.consume(TokenType.ID)
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.SEMICOLON)

    def parse_escrita(self):
        print("Parse: Escrita") # (Temporário para debug)
        self.consume(TokenType.CONSOLE_LOG)
        self.consume(TokenType.LPAREN)
        
        if self.current_token.type not in [TokenType.ID, TokenType.CADEIA]:
             raise Exception(f"Erro Sintático: Esperado ID ou CADEIA no console.log, encontrou {self.current_token.type}")
        self.advance()
        
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.SEMICOLON)

    def parse_condicional(self):
        print("Parse: Condicional") # (Temporário para debug)
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        self.parse_expressaoRelacional()
        self.consume(TokenType.RPAREN)
        self.parse_blocoInterno()
        
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.consume(TokenType.ELSE)
            self.parse_blocoInterno()

    def parse_repeticao(self):
        print("Parse: Repetição (While)") # (Temporário para debug)
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        self.parse_expressaoRelacional()
        self.consume(TokenType.RPAREN)
        self.parse_blocoInterno()

    def parse_blocoInterno(self):
        print("Parse: Bloco Interno") # (Temporário para debug)
        self.consume(TokenType.LBRACE)
        self.parse_comandos()
        self.consume(TokenType.RBRACE)

    def parse_termo(self):
        self.parse_fator()
        self.parse_termo_linha()

    def parse_termo_linha(self):
        if self.current_token and self.current_token.type == TokenType.ASTERISK:
            self.consume(TokenType.ASTERISK)
            self.parse_fator()
            self.parse_termo_linha()
        elif self.current_token and self.current_token.type == TokenType.SLASH:
            self.consume(TokenType.SLASH)
            self.parse_fator()
            self.parse_termo_linha()
        elif self.current_token and self.current_token.type == TokenType.MODULO:
            self.consume(TokenType.MODULO)
            self.parse_fator()
            self.parse_termo_linha()
        else:
            pass # Caso Vazio (ε)

    def parse_fator(self):
        if self.current_token.type == TokenType.NUMINT:
            self.consume(TokenType.NUMINT)
        elif self.current_token.type == TokenType.NUMREAL:
            self.consume(TokenType.NUMREAL)
        elif self.current_token.type == TokenType.ID:
            self.consume(TokenType.ID)
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            self.parse_expressaoRelacional() 
            self.consume(TokenType.RPAREN)
        else:
            raise Exception(f"Erro Sintático: Fator inválido, encontrou {self.current_token.type}")

    def parse_expressaoRelacional(self):
        self.parse_termoRelacional()
        self.parse_expressaoRelacional_linha()

    def parse_expressaoRelacional_linha(self):
        if self.current_token and self.current_token.type == TokenType.OP_LOGICO:
            self.consume(TokenType.OP_LOGICO)
            self.parse_termoRelacional()
            self.parse_expressaoRelacional_linha()
        else:
            pass # Caso Vazio (ε)

    def parse_termoRelacional(self):
        self.parse_expressaoAritmetica()
        if self.current_token and self.current_token.type == TokenType.OP_REL:
            self.consume(TokenType.OP_REL)
            self.parse_expressaoAritmetica()