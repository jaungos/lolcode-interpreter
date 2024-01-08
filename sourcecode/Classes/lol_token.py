"""
    This file is used to define the token class for the compiler.
"""

class Token:
    def __init__(self, identified_lexeme, identified_token_type, read_in_line_number):
        self.lexeme = identified_lexeme
        self.token_type = identified_token_type
        self.line_number = read_in_line_number

    def get_lexeme(self):
        return self.lexeme

    def get_token_type(self):
        return self.token_type