"""
    Developed by:   BONZA, Jhorge Anne B.
                    SOLIVERES, Angelo E.
                    UNGOS, Jerico Luis A.
"""

# Importing the needed libraries
import re as lexicalanalyzer

# Importing the needed modules
from Classes.lol_token import Token
from Classes.lol_symbol_table import Lol_Symbol_Table
from Classes.lexeme_types import classify_passed_lexeme

# ==================== LEXICAL ANALYZER ==================== #
class LexicalAnalyzer:
    def __init__(self, code_file_to_analyze):
        self.code_file_to_analyze = code_file_to_analyze
        self.symbol_table = Lol_Symbol_Table()

    def check_if_valid_identifier(self, lexeme):
        # Check if the lexeme is a valid identifier
        return True if lexicalanalyzer.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', lexeme) else False

    def check_if_valid_numbr_literal(self, lexeme):
        # Check if the lexeme is a valid numbr literal
        return True if lexicalanalyzer.match(r'(^-?[1-9][0-9]*$)|(^0$)', lexeme) else False

    def check_if_valid_numbar_literal(self, lexeme):
        # Check if the lexeme is a valid numbar literal
        return True if lexicalanalyzer.match(r'^-?[0-9]+\.[0-9]+$', lexeme) else False

    def check_if_valid_yarn_literal(self, lexeme):
        # Check if the lexeme is a valid yarn literal (incl. ~ )
        return True if lexicalanalyzer.match(r'^\"(.*?)(?<!~)\"$', lexeme) else False

    def check_if_valid_troof_literal(self, lexeme):
        return True if lexicalanalyzer.match(r'^(WIN|FAIL)', lexeme) else False

    def check_if_valid_type_literal(self, lexeme):
        # Check if the lexeme is valid type literal
        return True if lexicalanalyzer.match(r'^(NOOB|TROOF|NUMBAR|NUMBR|YARN)', lexeme) else False

    def check_if_valid_starting_point(self, line):
        # Check if the line is a valid starting point of the LOLCODE program
        if line.startswith("HAI"):
            # If so, add it to the symbol table as a keyword
            self.symbol_table.add_token(Token(line, "OPENING_PROGRAM_DELIMITER"))
            return True
        
        return False

    def check_if_valid_ending_point(self, line):
        # Check if the line is a valid ending point of the LOLCODE program
        if line.startswith("KTHXBYE"):
            # If so, add it to the symbol table as a keyword
            self.symbol_table.add_token(Token(line, "CLOSING_PROGRAM_DELIMITER"))
            return True
        
        return False

    def check_if_empty_line(self, line):
        return True if line == "" else False

    def check_if_invalid_starting_multiline_comment(self, line):
        # Check if OBTW is detected in the middle of a statement
        error_match = lexicalanalyzer.match(r'(.+)\s+OBTW', line)
        return True if error_match else False

    def check_if_invalid_closing_multiline_comment(self, line):
        # Check if TLDR is followed by any other characters
        return True if len(line) > 4 else False
            
    def check_if_valid_comment(self, line, code_file_being_read):
        # Check if the line is an invalid starting point of a multi-line comment
        if self.check_if_invalid_starting_multiline_comment(line):
            raise Exception("Invalid multi-line comment (opening delimiter)")

        # Check if the line is a standalone single-line comment
        # Reference: https://www.geeksforgeeks.org/python-string-startswith/
        if line.startswith("BTW"):
            # If so add it to the symbol table as a comment
            self.symbol_table.add_comment(Token(line, "COMMENT LITERAL"))
            return True

        # Check if the line is a co-existing single-line comment with another statement
        coexisting_comment_matched = lexicalanalyzer.match(r'(.*?)\s+BTW\s+(.*?)$', line)
        if coexisting_comment_matched:
            # get the comment text (after BTW)
            comment_text = " ".join(['BTW', coexisting_comment_matched.group(2)]) 
            self.symbol_table.add_comment(Token(comment_text, "COMMENT LITERAL"))

            return True
        
        # Check if the line is a multi-line comment
        if line.startswith("OBTW"):
            # Store the entire multi-line comment in a string
            comment_line = line.strip()

            line = code_file_being_read.readline() # Proceed to checking from the next line

            # Read next lines until it finds a TLDR
            while True:
                line = line.strip()

                # Append the line to a string
                # Reference: https://www.geeksforgeeks.org/python-string-concatenation/
                comment_line = " ".join([comment_line, line])

                if line.startswith("TLDR"):
                    # Check if the line is an invalid ending point of the multi-line comment
                    if self.check_if_invalid_closing_multiline_comment(line):
                        # If so, raise an exception
                        # Reference: https://www.geeksforgeeks.org/python-raise-keyword/
                        raise Exception("Invalid multi-line comment (closing delimiter)")
                    
                    # If not, add it to the symbol table as a comment
                    self.symbol_table.add_comment(Token(comment_line, "COMMENT LITERAL"))
                    return True
                
                line = code_file_being_read.readline()

        return False

    def analyze(self):
        with open(self.code_file_to_analyze, "r") as code_file:
            # Read the file line by line
            for line in code_file:
                # Remove the newline character
                line = line.strip()

                # Skip the line if it is empty
                if self.check_if_empty_line(line):
                    continue
                
                # Check if the line is a valid comment
                # Reference: https://www.geeksforgeeks.org/python-string-startswith/
                if self.check_if_valid_comment(line, code_file):
                    continue

                # Check if the line is the valid starting point of the LOLCODE program
                if self.check_if_valid_starting_point(line):
                    continue
                
                # Check if the line is a valid ending point of the LOLCODE program
                if self.check_if_valid_ending_point(line):
                    continue
                


                print(line)
        

    def print_tokens(self):
        print("Tokens:")
        for token in self.symbol_table.get_tokens():
            print(f'\t{token.get_token_type()}: {token.get_lexeme()}')

    def print_comments(self):
        print("Comments:")
        for comment in self.symbol_table.get_comments():
            print(f'\t{comment.get_token_type()}: {comment.get_lexeme()}')

# ==================== MAIN ==================== #
# Initialize the lexical analyzer
lexical_analyzer = LexicalAnalyzer("testcases/11_btws.lol")

# Analyze the file
lexical_analyzer.analyze()

lexical_analyzer.check_if_valid_identifier("aAA___")
lexical_analyzer.print_tokens()
lexical_analyzer.print_comments()

