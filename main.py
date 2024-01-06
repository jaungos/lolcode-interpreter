"""
    This file is the main file of the project. It is the one responsible for running the interpreter.
"""

from lolcode.interpreter import Interpreter

# Initialize the lexical analyzer
interpreter = Interpreter()

interpreter.read_file("testcases_natin/gimmeh_duplicate.lol")
# interpreter.read_file("project-testcases/01_variables.lol")

interpreter.run_lexer() # Run the lexical analyzer

interpreter.run_parser() # Run the syntax analyzer

interpreter.run_interpreter() # Run the semantic analyzer