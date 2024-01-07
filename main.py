"""
    This file is the main file of the project. 
    This is an interpreter for the LOLCode programming language created using Python.
"""

from lolcode.interpreter import Interpreter

def main():
    # Initialize the lexical analyzer
    interpreter = Interpreter()

    interpreter.read_file("testcases_natin/if_else.lol")
    # interpreter.read_file("project-testcases/01_variables.lol")

    interpreter.run_lexer() # Run the lexical analyzer

    interpreter.run_parser() # Run the syntax analyzer

    interpreter.run_interpreter() # Run the semantic analyzer

# Run the program
if __name__ == "__main__":
    main()