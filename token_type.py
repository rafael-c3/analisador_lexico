# token_type.py

from enum import Enum

class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    REL_OPERATOR = "REL_OPERATOR"
    MATH_OPERATOR = "MATH_OPERATOR"
    ASSIGNMENT = "ASSIGNMENT"