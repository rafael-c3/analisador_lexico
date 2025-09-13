# token_class.py

from token_type import TokenType

class Token:
    def __init__(self, type: TokenType, text: str):
        self.type = type
        self.text = text

    def __str__(self) -> str:
        # Formato de impressão idêntico ao do Java: "Token [type=..., text=...]"
        return f"Token [type={self.type.name}, text={self.text}]"