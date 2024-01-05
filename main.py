"""
    Developed by:   BONZA, Jhorge Anne B.
                    SOLIVERES, Angelo E.
                    UNGOS, Jerico Luis A.
"""

"""
    TODO:
        - create a ReadMe file
"""


from lolcode.interpreter import Interpreter

# Initialize the lexical analyzer
interpreter = Interpreter()

interpreter.read_file("testcases_natin/gimmeh.lol")
# interpreter.read_file("testcases_natin/05_bool.lol")

interpreter.run_lexer() # Run the lexical analyzer

interpreter.run_parser() # Run the syntax analyzer

# interpreter.run_interpreter() # Run the semantic analyzer