"""
    This file is used to define the symbol table class for the compiler.
"""

class Lol_Symbol_Table:
    def __init__(self):
        self.tokens = []
        self.symbols = {}

    def add_token(self, token):
        self.tokens.append(token)

    def get_tokens(self):
        return self.tokens

    def add_symbol(self, lexeme, symbol):
        self.symbols.update({lexeme: symbol})

    def get_symbol(self, lexeme):
        return self.symbols[lexeme]

    def get_symbols(self):
        return self.symbols
    
    def check_if_symbol_exists(self, symbol):
        return symbol in self.symbols
    
    def update_symbol(self, lexeme, symbol):
        self.symbols[lexeme] = symbol
    