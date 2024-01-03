"""

    This file is used to define the interpreter for the lolcode language.
    TODO: add brief description of what an interpreter does in this lolcode compiler
"""

# Import the needed modules
from lolcode.lexical_analyzer import LexicalAnalyzer
from lolcode.syntax_analyzer import SyntaxAnalyzer
from lolcode.semantic_analyzer import SemanticAnalyzer

class Interpreter:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.parse_tree = []

        self.lexer = None
        self.parser = None
        self.semantic_analyzer = None

    """
        TODO:
            - Check if the file passed is a .lol file
            - Check if there is a file passed a non-empty string
                - set the initial self.source_code to an empty string
                - update it once a method for reading the file is created
                    - the method is just to check the 2 above conditions
    """

    def run_lexer(self):
        print("Running the lexical analyzer...")

        # Instantiate the lexical analyzer
        self.lexer = LexicalAnalyzer(self.source_code)

        self.tokens = self.lexer.run_lexical_analyzer()
        self.lexer.print_tokens()

    def run_parser(self):
        print("\n\nRunning the syntax analyzer...")

        # Instantiate the syntax analyzer
        self.parser = SyntaxAnalyzer(self.tokens)

        self.parser.run_syntax_analyzer()

        self.parse_tree = self.parser.parse_tree

        self.parser.print_parse_tree()

    def run_interpreter(self):
        print("\n\nRunning the semantic analyzer...")

        # Instantiate the semantic analyzer
        self.semantic_analyzer = SemanticAnalyzer(self.parse_tree)

        self.semantic_analyzer.run_semantic_analyzer()

        self.semantic_analyzer.print_symbol_table()

