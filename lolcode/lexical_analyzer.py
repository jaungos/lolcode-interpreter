"""
    This file is used to define the lexical analyzer for the lolcode language.
    TODO: add brief description of what a lexer does in this lolcode compiler
"""

# Importing the needed libraries
import re as lexicalanalyzer

# Importing the needed modules
from Classes.lol_token import Token
from Classes.lol_symbol_table import Lol_Symbol_Table
from Classifiers.lexeme_types import classify_passed_lexeme
from Classifiers.lexeme_identifiers import get_all_lexeme_regex_patterns

"""
    TODO:
        - improve error printing for all errors
            - should always include the type of error, line number, and the token that caused the error
            - for lexical errors, print if the it the token is caused by an invalid lexeme or the paired delimiters are not found (e.g. OBTW-TLDR, string delimiters)
"""

class LexicalAnalyzer:
    def __init__(self, code_file_to_analyze):
        self.code_file_to_analyze = code_file_to_analyze
        self.symbol_table = Lol_Symbol_Table()

        self.total_file_lines = 0
        self.line_number = 0
        self.character_position = 0
        self.comment_literal = ""
        self.currently_reading_multi_line_comment = False

    def run_lexical_analyzer(self):
        self.analyze()
        return self.symbol_table.get_tokens()

    def read_one_whitespace(self):
        self.character_position += 1

    def analyze(self):
        with open(self.code_file_to_analyze, "r") as code_file:
            self.total_file_lines = len(code_file.readlines())
            code_file.seek(0) # Reset the file pointer to the start of the file

            # Read the file line by line
            for line in code_file:
                # Remove the newline character at both the start and end of the line
                line = line.strip()

                line = line + '\n' # Add a newline character at the end of the line

                self.character_position = 0 # The current character being read in the line

                lexeme_regex_identifiers = get_all_lexeme_regex_patterns()

                while self.character_position < len(line):
                    # print(f'Currently reading the character: {line[self.character_position]} in line {self.line_number}')

                    # Check if opening multiline comment delimiter token is found
                    match = lexicalanalyzer.match(lexeme_regex_identifiers['OBTW'], line[self.character_position:])
                    if match:
                        # Add the token to the symbol table
                        self.symbol_table.add_token(Token(match.group(), classify_passed_lexeme('OBTW'), self.line_number))
                        self.character_position += len(match.group())

                        self.read_one_whitespace()

                        self.currently_reading_multi_line_comment = True # Set the flag to true to indicate that we are currently reading a multiline comment

                        continue

                    # Check if still reading multiline comment
                    if self.currently_reading_multi_line_comment:
                        # Check if closing multiline comment delimiter token is found
                        match = lexicalanalyzer.match(lexeme_regex_identifiers['TLDR'], line[self.character_position:])
                        if match:
                            # Add the multiline comment literal token to the symbol table
                            self.symbol_table.add_token(Token(self.comment_literal, classify_passed_lexeme('COMMENT'), self.line_number))

                            # Add the closing multiline comment delimiter token to the symbol table
                            self.symbol_table.add_token(Token(match.group(), classify_passed_lexeme('TLDR'), self.line_number))
                            self.character_position += len(match.group())
                            self.read_one_whitespace()

                            self.comment_literal = ""
                            self.currently_reading_multi_line_comment = False # Set the flag to false to indicate that we are no longer reading a multiline comment

                            continue

                        # Otherwise, continue appending the current line to the multiline comment
                        self.comment_literal = " ".join([self.comment_literal, line[self.character_position:-1]])
                        self.character_position += len(line[self.character_position:-1])
                        break

                    # Check if single line comment is found
                    match = lexicalanalyzer.match(lexeme_regex_identifiers['BTW'], line[self.character_position:])
                    if match:
                        # Add the single line comment delimiter token to the symbol table
                        self.symbol_table.add_token(Token(match.group(), classify_passed_lexeme('BTW'), self.line_number))
                        self.character_position += len(match.group())
                        self.read_one_whitespace()

                        # Read the rest of the line as a comment up until before the newline character
                        self.symbol_table.add_token(Token(line[self.character_position:-1], classify_passed_lexeme('COMMENT'), self.line_number))
                        self.character_position += len(line[self.character_position:-1])
                        break

                    for pattern in lexeme_regex_identifiers:
                        # Check if match is found
                        match = lexicalanalyzer.match(lexeme_regex_identifiers[pattern], line[self.character_position:])
                        if match:
                            # Check if the match is a YARN
                            if pattern == "YARN":
                                YARN_position = 0
                                # Add the opening YARN delimiter token to the symbol table
                                self.symbol_table.add_token(Token(match.group()[YARN_position], classify_passed_lexeme("\""), self.line_number))
                                YARN_position += 1

                                # Add the YARN literal up until before the closing YARN delimiter token to the symbol table
                                string_literal = ""
                                while match.group()[YARN_position] != "\"":
                                    string_literal = "".join([string_literal, match.group()[YARN_position]])
                                    YARN_position += 1

                                self.symbol_table.add_token(Token(string_literal, classify_passed_lexeme("STRING"), self.line_number))

                                # Add the closing YARN delimiter token to the symbol table
                                self.symbol_table.add_token(Token(match.group()[YARN_position], classify_passed_lexeme("\""), self.line_number))
                                YARN_position += 1

                                self.character_position += len(match.group())
                                break

                            # Add the token to the symbol table
                            self.symbol_table.add_token(Token(match.group(), classify_passed_lexeme(pattern), self.line_number)) 
                            self.character_position += len(match.group())
                            break

                    self.read_one_whitespace()

                # Add the newline character to the symbol table if it is not currently reading a multiline comment
                if not self.currently_reading_multi_line_comment:
                    self.symbol_table.add_token(Token('\n', classify_passed_lexeme('NEWLINE'), self.line_number))

                self.line_number += 1 # Increment the line number as we move to the next lin

                # Check if it is still reading a multiline comment but the end of the file has already been reached
                if self.currently_reading_multi_line_comment and self.line_number == self.total_file_lines:
                    raise Exception(f'ERROR: Missing TLDR for multi-line comments. Line {self.line_number}')

    def print_tokens(self):
        print("Tokens:")
        for token in self.symbol_table.get_tokens():
            print(f'\t{token.get_token_type()}: {token.get_lexeme()} in line {token.line_number + 1}')