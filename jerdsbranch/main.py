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
interpreter = Interpreter("project-testcases/02_gimmeh.lol")

interpreter.run_lexer() # Run the lexical analyzer

interpreter.run_parser() # Run the syntax analyzer

# interpreter.run_interpreter() # Run the semantic analyzer