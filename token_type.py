from enum import Enum

class TokenType(Enum):
    # Tipos Especiais
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Operadores
    ASSIGN = "ASSIGN"
    MATH_OPERATOR = "MATH_OPERATOR"
    GT = "GT"
    GTE = "GTE"
    LT = "LT"
    LTE = "LTE"
    NOT_EQUAL = "NOT_EQUAL"
    EQUAL = "EQUAL"

    # Delimitadores
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )

    # Palavras-chave
    INT = "INT"
    FLOAT = "FLOAT"
    PRINT = "PRINT"
    IF = "IF"
    ELSE = "ELSE"