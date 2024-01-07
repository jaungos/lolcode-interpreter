"""
    This file is used to define and implement the interpreter for the LOLCode language.
    Holds the respective functions that would call the lexical analyzer, syntax analyzer, and semantic analyzer.
"""

# Import the needed modules
from lolcode.lexical_analyzer import LexicalAnalyzer
from lolcode.syntax_analyzer import SyntaxAnalyzer
from lolcode.semantic_analyzer import SemanticAnalyzer

class Interpreter:
    def __init__(self):
        self.source_code = ""
        self.tokens = []
        self.parse_tree = []

        self.lexer = None
        self.parser = None
        self.semantic_analyzer = None

    """
        TODO:
            - error messages and delete the print statements
    """
    def isTokenListEmpty(self):
        return len(self.tokens) == 0
    
    def read_file(self, file_path):
        self.source_code = file_path

    def checkIfFileExists(self):
        # TODO: improve error prompting
        if self.source_code == "":
            raise Exception("No file path passed. Please pass a file path.")
        
        # Check if the file is a .lol file
        if self.source_code[-4:] != ".lol":
            raise Exception("File is not a .lol file. Please pass a valid .lol file.")

        # Check if the file exists
        try:
            file = open(self.source_code, "r")
        except FileNotFoundError:
            raise Exception("File not found. Please pass a valid file path.")
        
        # Check if the file is empty
        if file.read() == "":
            raise Exception("File is empty. No source code to interpret.")
        
        # Close the file
        file.close()

    def run_lexer(self):
        # Check for the validity of the file path
        self.checkIfFileExists()

        print("Running the lexical analyzer...")

        # Instantiate the lexical analyzer
        self.lexer = LexicalAnalyzer(self.source_code)

        self.tokens = self.lexer.run_lexical_analyzer()
        self.lexer.print_tokens()

    def run_parser(self):
        print("\n\nRunning the syntax analyzer...")

        # TODO: improve error prompting
        if self.isTokenListEmpty():
            raise Exception("No tokens to parse.")

        # Instantiate the syntax analyzer
        self.parser = SyntaxAnalyzer(self.tokens)

        self.parser.run_syntax_analyzer()

        self.parse_tree = self.parser.parse_tree

        self.parser.print_parse_tree()

    def run_interpreter(self):
        print("\n\nRunning the semantic analyzer...")

        # TODO: improve error prompting
        if self.parse_tree is None:
            raise Exception("No parse tree to analyze.")

        # Instantiate the semantic analyzer
        self.semantic_analyzer = SemanticAnalyzer(self.parse_tree)

        self.semantic_analyzer.run_semantic_analyzer()

        self.semantic_analyzer.print_symbol_table()

