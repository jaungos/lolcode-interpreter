"""
    This file is used to define the symbol class of a symbol table for the compiler. 
"""

class SymbolEntity:
    def __init__(self, symbolClassification, symbolValue):
        self.symbolClassification = symbolClassification
        self.symbolValue = symbolValue