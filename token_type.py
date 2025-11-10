from enum import Enum

class TokenType(Enum):
    # Palavras-chave da Gramática
    FUNCTION = "FUNCTION"
    MAIN = "MAIN"
    LET = "LET"
    CONST = "CONST"
    NUMBER = "NUMBER"     # Keyword 'number'
    FLOAT = "FLOAT"       # Keyword 'float'
    READ = "READ"
    CONSOLE_LOG = "CONSOLE.LOG"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"

    # Literais e Identificadores
    ID = "ID"             # Identificador (ex: x, minha_var)
    CADEIA = "CADEIA"     # Literal de string (ex: "ola")
    NUMINT = "NUMINT"     # Literal de número inteiro (ex: 123)
    NUMREAL = "NUMREAL"   # Literal de número real (ex: 12.34, .5)

    # Operadores
    ASSIGN = "="          # Atribuição
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    MODULO = "%"          # Novo operador Módulo
    OP_REL = "OP_REL"     # Relacionais (>, <, >=, <=, ==, !=)
    OP_LOGICO = "OP_LOGICO" # Logicos (&&, ||)

    # Delimitadores
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"
    COLON = ":"           # Dois pontos

    # Especiais
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"