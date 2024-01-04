"""
    This file is used to define the syntax analyzer for the lolcode language.
    TODO: add brief description of what a parser does in this lolcode compiler
"""

"""
    TODO:
        - improve error printing for all errors
            - should always include the type of error, line number, and the token that caused the error
            - for syntax errors, should also include the expected token type and the actual token type
        - improve printing when parsing is finished due to no more tokens left
        - double check and fix naming conventions
"""

# TODO: Remove after milestone presentation
from Classes.lol_node import ParseTreeNode

class SyntaxAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.parse_tree = None

        self.current_token = symbol_table[0]
        self.previous_token = None

        self.currently_reading_infinite_arity_boolean_operator = False

    def run_syntax_analyzer(self):
        self.analyze()
        
    def check_if_symbol_table_is_empty(self):
        if len(self.symbol_table) == 0:
            return True
        else:
            return False
        
    def check_if_program_delimiters_are_present(self):
        if "program_start_delimiter" in self.symbol_table[0].token_type and "program_end_delimiter" in self.symbol_table[-1].token_type:
            return True
        else:
            return False

    def check_if_token_matches_expected_token_types(self, expected_token_type):
        if expected_token_type == self.current_token.get_token_type():
            return True
        else:
            return False
            
    def consume_current_token(self):
        # Remove the token from the list and proceed to check the next token
        self.previous_token = self.symbol_table.pop(0) 

        # Update the current token if there are still tokens left
        if self.check_if_symbol_table_is_empty() == True:
            print("Finished parsing...")
            return
        else:
            self.current_token = self.symbol_table[0]

    def addParseTreeNode(self, node_parent):
        node = ParseTreeNode(self.current_token.lexeme, node_parent)
        node_parent.add_child(node)
        return node
    
    def analyze(self):
        # Remove all comments and linebreak delimiters
        self.check_if_comments_are_valid()    
        self.remove_all_comments()
        self.remove_linebreak_delimiters()

        # Update the current token if there are still tokens left 
        if self.check_if_symbol_table_is_empty():
            # TODO: Improve the error printing for empty file
            print("File is empty...")
            return
        else:
            self.current_token = self.symbol_table[0]

        # Check if the program delimiters are present
        if not self.check_if_program_delimiters_are_present():
            # TODO: Improve the error printing for missing program delimiters
            raise Exception("Syntax Error: Missing program delimiters")

        # Create the root node of the parse tree
        self.parse_tree = ParseTreeNode("<program>", None)
        self.program() # Start the parsing from the <program> grammar rule

    # TODO: remove. ONLY FOR ERROR CHECKING
    def print_parse_tree(self):
        self.parse_tree.print_tree(0)
    
    # ===================== Functions for the Grammar Rules =====================
    # <data-type> ::= NUMBR | NUMBAR | YARN | TROOF | NOOB
    def data_type(self, node_parent):
        if self.current_token.get_lexeme() == "NUMBR":
            integer_type_node = ParseTreeNode("<integer-data-type>", node_parent)
            node_parent.add_child(integer_type_node)

            self.addParseTreeNode(integer_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "NUMBAR":
            float_type_node = ParseTreeNode("<float-data-type>", node_parent)
            node_parent.add_child(float_type_node)
            
            self.addParseTreeNode(float_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "YARN":
            string_type_node = ParseTreeNode("<string-data-type>", node_parent)
            node_parent.add_child(string_type_node)
            
            self.addParseTreeNode(string_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "TROOF":
            boolean_type_node = ParseTreeNode("<boolean-data-type>", node_parent)
            node_parent.add_child(boolean_type_node)

            self.addParseTreeNode(boolean_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "NOOB":
            null_type_node = ParseTreeNode("<null-data-type>", node_parent)
            node_parent.add_child(null_type_node)

            self.addParseTreeNode(null_type_node)
            self.consume_current_token()
        else:
            # Error handling for invalid data type
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected data type but got {self.current_token.token_type}")
    
    # <valid-type> ::= <data-type>
    def valid_type(self, node_parent):
        if self.check_if_token_matches_expected_token_types("type_literal"):
            valid_type_node = ParseTreeNode("<valid-data-type>", node_parent)
            node_parent.add_child(valid_type_node)
            self.data_type(valid_type_node) # Add the data type node as a child of the valid type node
        else:
            # Error handling for invalid type
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected valid type but got {self.current_token.token_type}")

    # <literal-value> ::= numbr_literal | numbar_literal | yarn_literal | troof_literal
    def literal_value(self, node_parent):
        if self.current_token.token_type == "string_delimiter":
            yarn_literal_node = ParseTreeNode("<yarn-literal>", node_parent)
            node_parent.add_child(yarn_literal_node)

            self.consume_current_token() # Skip the string delimiter
            self.addParseTreeNode(yarn_literal_node)
            self.consume_current_token()
            self.consume_current_token() # Skip the string delimiter
        elif self.current_token.token_type == "numbr_literal":
            numbr_literal_node = ParseTreeNode("<numbr-literal>", node_parent)
            node_parent.add_child(numbr_literal_node)

            self.addParseTreeNode(numbr_literal_node)
            self.consume_current_token()
        elif self.current_token.token_type == "numbar_literal":
            numbar_literal_node = ParseTreeNode("<numbar-literal>", node_parent)
            node_parent.add_child(numbar_literal_node)

            self.addParseTreeNode(numbar_literal_node)
            self.consume_current_token()
        elif self.current_token.token_type == "troof_literal":
            troof_literal_node = ParseTreeNode("<troof-literal>", node_parent)
            node_parent.add_child(troof_literal_node)

            self.addParseTreeNode(troof_literal_node)
            self.consume_current_token()
        else:
            # Error handling for invalid literal value
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected literal value but got {self.current_token.token_type}")
    
    # <arithmetic-value-operands> ::= <var-value> AN <var-value>
    def arithmetic_value_operands(self, node_parent):
        arithmetic_value_operand_node = ParseTreeNode("<arithmetic-value-operands>", node_parent)
        node_parent.add_child(arithmetic_value_operand_node)

        self.var_value(arithmetic_value_operand_node)

        # Check for the AN keyword
        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", arithmetic_value_operand_node)
            arithmetic_value_operand_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.var_value(arithmetic_value_operand_node)
        else:
            # Error handling for invalid arithmetic value operand
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected another arithmetic value operand but got {self.current_token.token_type}")

    # <arithmetic-expression> ::= SUM OF <arithmetic-value-operands> | DIFF OF <arithmetic-value-operands> | PRODUKT OF <arithmetic-value-operands> | QUOSHUNT OF <arithmetic-value-operands> | MOD OF <arithmetic-value-operands> | BIGGR OF <arithmetic-value-operands> | SMALLR OF <arithmetic-value-operands> 
    def arithmetic_expression(self, node_parent):
        arith_statement_node = ParseTreeNode("<arithmetic-expression>", node_parent)
        node_parent.add_child(arith_statement_node)

        if self.current_token.lexeme == "SUM OF":
            sum_operator_node = ParseTreeNode("<addition-operator>", arith_statement_node)
            arith_statement_node.add_child(sum_operator_node)
            self.addParseTreeNode(sum_operator_node) # Add the SUM OF node as a child of the arithmetic statement node
            self.consume_current_token() # Update the current token to the next token

            self.arithmetic_value_operands(sum_operator_node) # Add the arithmetic expression node as a child of the arithmetic statement node
        elif self.current_token.lexeme == "DIFF OF":
            difference_operator_node = ParseTreeNode("<subtraction-operator>", arith_statement_node)
            arith_statement_node.add_child(difference_operator_node)
            self.addParseTreeNode(difference_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(difference_operator_node)
        elif self.current_token.lexeme == "PRODUKT OF":
            product_operator_node = ParseTreeNode("<multiplication-operator>", arith_statement_node)
            arith_statement_node.add_child(product_operator_node)
            self.addParseTreeNode(product_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(product_operator_node)
        elif self.current_token.lexeme == "QUOSHUNT OF":
            quotient_operator_node = ParseTreeNode("<division-operator>", arith_statement_node)
            arith_statement_node.add_child(quotient_operator_node)
            self.addParseTreeNode(quotient_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(quotient_operator_node)
        elif self.current_token.lexeme == "MOD OF":
            modulo_operator_node = ParseTreeNode("<modulo-operator>", arith_statement_node)
            arith_statement_node.add_child(modulo_operator_node)
            self.addParseTreeNode(modulo_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(modulo_operator_node)
        elif self.current_token.lexeme == "BIGGR OF":
            max_operator_node = ParseTreeNode("<max-operator>", arith_statement_node)
            arith_statement_node.add_child(max_operator_node)
            self.addParseTreeNode(max_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(max_operator_node)
        elif self.current_token.lexeme == "SMALLR OF":
            min_operator_node = ParseTreeNode("<min-operator>", arith_statement_node)
            arith_statement_node.add_child(min_operator_node)
            self.addParseTreeNode(min_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(min_operator_node)
        else:
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected arithmetic operator but got {self.current_token.token_type}")

    # <boolean-value-operands> ::= <var-value> AN <var-value>
    def boolean_value_operands(self, node_parent):
        boolean_value_operand_node = ParseTreeNode("<boolean-value-operands>", node_parent)
        node_parent.add_child(boolean_value_operand_node)

        self.var_value(boolean_value_operand_node)

        # Check for the AN keyword
        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", boolean_value_operand_node)
            boolean_value_operand_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.var_value(boolean_value_operand_node)

            while self.currently_reading_infinite_arity_boolean_operator == True and self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
                operand_separator_node = ParseTreeNode("<operand-separator-operator>", boolean_value_operand_node)
                boolean_value_operand_node.add_child(operand_separator_node)
                self.addParseTreeNode(operand_separator_node)
                self.consume_current_token()

                self.var_value(boolean_value_operand_node)
        else:
            # Error handling for invalid logical value operand
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected another boolean value operand but got {self.current_token.token_type}")

    # <boolean-operations> ::= BOTH OF <boolean-value-operands> | EITHER OF <boolean-value-operands> | WON OF <boolean-value-operands> | NOT <var-value> 
    def boolean_operations(self, node_parent):
        boolean_operation_node = ParseTreeNode("<boolean-operations>", node_parent)
        node_parent.add_child(boolean_operation_node)

        if self.current_token.lexeme == "BOTH OF":
            and_operator_node = ParseTreeNode("<and-operator>", boolean_operation_node)
            boolean_operation_node.add_child(and_operator_node)
            self.addParseTreeNode(and_operator_node)
            self.consume_current_token()

            self.boolean_value_operands(and_operator_node)
        elif self.current_token.lexeme == "EITHER OF":
            or_operator_node = ParseTreeNode("<or-operator>", boolean_operation_node)
            boolean_operation_node.add_child(or_operator_node)
            self.addParseTreeNode(or_operator_node)
            self.consume_current_token()

            self.boolean_value_operands(or_operator_node)
        elif self.current_token.lexeme == "WON OF":
            xor_operator_node = ParseTreeNode("<xor-operator>", boolean_operation_node)
            boolean_operation_node.add_child(xor_operator_node)
            self.addParseTreeNode(xor_operator_node)
            self.consume_current_token()

            self.boolean_value_operands(xor_operator_node)
        elif self.current_token.lexeme == "NOT":
            not_operator_node = ParseTreeNode("<not-operator>", boolean_operation_node)
            boolean_operation_node.add_child(not_operator_node)
            self.addParseTreeNode(not_operator_node)
            self.consume_current_token()

            self.var_value(not_operator_node)
        else:
            self.boolean_value_operands(boolean_operation_node)

    # <boolean-expression> ::= ALL OF <boolean-operations> MKAY | ANY OF <boolean-operations> MKAY
    def boolean_expression(self, node_parent):
        boolean_statement_node = ParseTreeNode("<boolean-expression>", node_parent)
        node_parent.add_child(boolean_statement_node)

        if self.current_token.lexeme == "ALL OF":
            if self.currently_reading_infinite_arity_boolean_operator == True:
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected a non-infinite arity boolean operator but got {self.current_token.token_type}")

            infinite_and_operator_node = ParseTreeNode("<infinite-arity-and-operator>", boolean_statement_node)
            boolean_statement_node.add_child(infinite_and_operator_node)
            self.addParseTreeNode(infinite_and_operator_node)
            self.consume_current_token()
            self.currently_reading_infinite_arity_boolean_operator = True

            self.boolean_operations(infinite_and_operator_node)

            if self.currently_reading_infinite_arity_boolean_operator == True and self.check_if_token_matches_expected_token_types("multi_operator_closing_delimiter"):
                infinite_and_operator_end_delimiter_node = ParseTreeNode("<multiple-operator-closing-delimiter>", infinite_and_operator_node)
                infinite_and_operator_node.add_child(infinite_and_operator_end_delimiter_node)
                self.addParseTreeNode(infinite_and_operator_end_delimiter_node)
                self.consume_current_token()
                self.currently_reading_infinite_arity_boolean_operator = False
        elif self.current_token.lexeme == "ANY OF":
            if self.currently_reading_infinite_arity_boolean_operator == True:
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected a non-infinite arity boolean operator but got {self.current_token.token_type}")

            infinite_or_operator_node = ParseTreeNode("<infinite-arity-or-operator>", boolean_statement_node)
            boolean_statement_node.add_child(infinite_or_operator_node)
            self.addParseTreeNode(infinite_or_operator_node)
            self.consume_current_token()
            self.currently_reading_infinite_arity_boolean_operator = True

            self.boolean_operations(infinite_or_operator_node)

            if self.currently_reading_infinite_arity_boolean_operator == True and self.check_if_token_matches_expected_token_types("multi_operator_closing_delimiter"):
                infinite_or_operator_end_delimiter_node = ParseTreeNode("<multiple-operator-closing-delimiter>", infinite_or_operator_node)
                infinite_or_operator_node.add_child(infinite_or_operator_end_delimiter_node)
                self.addParseTreeNode(infinite_or_operator_end_delimiter_node)
                self.consume_current_token()
                self.currently_reading_infinite_arity_boolean_operator = False
        else:
            self.boolean_operations(boolean_statement_node)

    # <comparison-value-operands> ::= <var-value> AN <var-value> | <var-value> AN BIGGR OF <var-value> | <var-value> AN SMALLR OF <var-value>
    def comparison_value_operands(self, node_parent):
        print(f'Current token: {self.current_token.lexeme} at line {self.current_token.line_number}')
        comparison_value_operand_node = ParseTreeNode("<comparison-value-operands>", node_parent)
        node_parent.add_child(comparison_value_operand_node)

        self.var_value(comparison_value_operand_node)

        # Check for the AN keyword
        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", comparison_value_operand_node)
            comparison_value_operand_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.var_value(comparison_value_operand_node)
        else:
            # Error handling for invalid comparison value operand
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected another comparison value operand but got {self.current_token.token_type}")

    # <comparison-expression> ::= BOTH SAEM <comparison-value-operands> | DIFFRINT <comparison-value-operands>
    def comparison_expression(self, node_parent):
        print(f'Current token: {self.current_token.lexeme} at line {self.current_token.line_number}')
        comparison_statement_node = ParseTreeNode("<comparison-expression>", node_parent)
        node_parent.add_child(comparison_statement_node)

        if self.current_token.lexeme == "BOTH SAEM":
            equal_operator_node = ParseTreeNode("<equal-operator>", comparison_statement_node)
            comparison_statement_node.add_child(equal_operator_node)
            self.addParseTreeNode(equal_operator_node)
            self.consume_current_token()

            self.comparison_value_operands(equal_operator_node)
        elif self.current_token.lexeme == "DIFFRINT":
            not_equal_operator_node = ParseTreeNode("<not-equal-operator>", comparison_statement_node)
            comparison_statement_node.add_child(not_equal_operator_node)
            self.addParseTreeNode(not_equal_operator_node)
            self.consume_current_token()

            self.comparison_value_operands(not_equal_operator_node)
        else:
            # Error handling for invalid comparison operator
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected comparison operator but got {self.current_token.token_type}")

    # <concat-loop> ::= <var-value> | <var-value> AN <concat-loop>
    def concat_loop(self, node_parent):
        concat_loop_node = ParseTreeNode("<concat-loop>", node_parent)
        node_parent.add_child(concat_loop_node)

        self.var_value(concat_loop_node)

        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", concat_loop_node)
            concat_loop_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.concat_loop(concat_loop_node)

    # <concatenation-expression> ::= SMOOSH <concat-loop> | SMOOSH <concat-loop> MKAY
    def concatenation_expression(self, node_parent):
        concat_statement_node = ParseTreeNode("<concatenation-expression>", node_parent)
        node_parent.add_child(concat_statement_node)

        self.addParseTreeNode(concat_statement_node) # Add the SMOOSH node as a child of the concat statement node
        self.consume_current_token() # Update the current token to the next token

        self.concat_loop(concat_statement_node) # Add the concat loop node as a child of the concat statement node

        if self.check_if_token_matches_expected_token_types("multi_operator_closing_delimiter"):
            concatenation_end_delimiter_node = ParseTreeNode("<multiple-operator-closing-delimiter>", concat_statement_node)
            concat_statement_node.add_child(concatenation_end_delimiter_node)
            self.addParseTreeNode(concatenation_end_delimiter_node)
            self.consume_current_token()

    # <expression> ::= <arithmetic-expression> | <logical-expression> | <comparison-expression> | <concatenation-expression>
    def expression(self, node_parent):
        if self.current_token.token_type == "arithmetic_operator":
            self.arithmetic_expression(node_parent)
        elif self.current_token.token_type == "logical_operator":
            self.boolean_expression(node_parent)
        elif self.current_token.token_type == "comparison_operator":
            self.comparison_expression(node_parent)
        elif self.current_token.token_type == "concatenation_operator":
            self.concatenation_expression(node_parent)
        # TODO: double check if pwede rin typecasting
        else:
            # Error handling for invalid expression
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected expression but got {self.current_token.token_type}")

    # <var-value> ::= literal | varident | <expression>
    def var_value(self, node_parent):
        var_value_node = ParseTreeNode("<var-value>", node_parent)
        node_parent.add_child(var_value_node)

        # If the value is a literal
        if self.current_token.token_type in ["numbr_literal", "numbar_literal", "string_delimiter", "troof_literal"]:
            literal_value_node = ParseTreeNode("<literal-value>", var_value_node)
            var_value_node.add_child(literal_value_node)
            
            self.literal_value(literal_value_node) # Add the literal value node as a child of the var value node
        # If the value is a variable identifier
        elif self.current_token.token_type == "identifiers":
            variable_value_node = ParseTreeNode("<variable-value>", var_value_node)
            var_value_node.add_child(variable_value_node)

            self.addParseTreeNode(variable_value_node)
            self.consume_current_token()
        # If the value is an expression
        # TODO: ask if typecasting is also an expression
        elif self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator", ]:
            expression_value_node = ParseTreeNode("<expression-value>", var_value_node)
            var_value_node.add_child(expression_value_node)

            self.expression(expression_value_node) # Add the expression node as a child of the var value node
        else:
            # Error handling for invalid var value
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected literal, variable identifier, or expression but got {self.current_token.token_type}")

    # <varident> ::= identifier | ITZ <var-value>
    def varident(self, node_parent):
        varident_node = ParseTreeNode("<varident>", node_parent)
        node_parent.add_child(varident_node)

        if self.check_if_token_matches_expected_token_types("identifiers"):
            # TODO: add additional check if the identifier is a keyword or reserved keyword (make an array of keywords para IN <array-name> na check na lang)
            # if self.current_token IN keywords:
            self.addParseTreeNode(varident_node)
            self.consume_current_token()

            if self.check_if_token_matches_expected_token_types("variable_initialization_keyword"):
                var_node_initialization = ParseTreeNode("<var-initialization>", node_parent)
                node_parent.add_child(var_node_initialization)
                self.addParseTreeNode(var_node_initialization) # Add the ITZ node as a child of the var node initialization
                self.consume_current_token() # Update the current token to the next token

                self.var_value(var_node_initialization) # Add the var value node as a child of the var node initialization
        else:
            # Error handling for invalid variable identifier
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected variable identifier but got {self.current_token.token_type}")

    # <var> ::= I HAS A <varident> | I HAS A <varident> ITZ <var-value>
    def var(self, node_parent):
        var_node = ParseTreeNode("<var>", node_parent)
        node_parent.add_child(var_node)

        var_declaration_keyword_node = ParseTreeNode("<var-declaration-keyword>", var_node)
        var_node.add_child(var_declaration_keyword_node)
        self.addParseTreeNode(var_declaration_keyword_node) # Add the I HAS A node as a child of the var node
        self.consume_current_token() # Update the current token to the next token
        
        self.varident(var_node) # Add the varident node as a child of the var node

        # Check if the current token is still a variable declaration start delimiter
        if self.check_if_token_matches_expected_token_types("variable_declaration_keyword"):
            self.var(node_parent)

    # <variable-declaration> ::= WAZZUP <var> BUHBYE
    # TODO: implement I HAS A and ITZ keywords outside of variable declaration
    def variable_declaration(self):
        variable_declaration_node = ParseTreeNode("<variable-declaration>", self.parse_tree)
        self.parse_tree.add_child(variable_declaration_node)

        variable_declaration_start_delimiter_node = ParseTreeNode("<variable-declaration-start-delimiter>", variable_declaration_node)
        variable_declaration_node.add_child(variable_declaration_start_delimiter_node)
        self.addParseTreeNode(variable_declaration_start_delimiter_node) # Add the WAZZUP node as a child of the variable declaration node
        self.consume_current_token() # Update the current token to the next token

        if self.check_if_token_matches_expected_token_types("variable_declaration_keyword"):
            self.var(variable_declaration_node) # Add the var node as a child of the variable declaration node

        if self.check_if_token_matches_expected_token_types("variable_declaration_end_delimiter"):
            variable_declaration_end_delimiter_node = ParseTreeNode("<variable-declaration-end-delimiter>", variable_declaration_node)
            variable_declaration_node.add_child(variable_declaration_end_delimiter_node)
            self.addParseTreeNode(variable_declaration_end_delimiter_node) # Add the BUHBYE node as a child of the variable declaration node
            self.consume_current_token() # Update the current token to the next token
        else:
            # Error handling for missing BUHBYE keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected variable declaration end delimiter but got {self.current_token.token_type}")
    
    # <print-loop> ::= <var-value> | <var-value> + <print-loop>
    # TODO: remove only for testing smoosh
    def print_loop(self, node_parent):
        print_loop_node = ParseTreeNode("<print-loop>", node_parent)
        node_parent.add_child(print_loop_node)

        self.var_value(print_loop_node)

        if self.check_if_token_matches_expected_token_types("visible_concatenate_operator"):
            visible_concatenate_operator = ParseTreeNode("<visible-concatenate-operator>", print_loop_node)
            print_loop_node.add_child(visible_concatenate_operator)
            self.addParseTreeNode(visible_concatenate_operator)
            self.consume_current_token()

            self.print_loop(print_loop_node)

    # <print> ::= VISIBLE <print-loop> | VISIBLE <print-loop> ! 
    def print_statement(self, node_parent):
        print_statement_node = ParseTreeNode("<print>", node_parent)
        node_parent.add_child(print_statement_node)

        self.addParseTreeNode(print_statement_node) # Add the VISIBLE node as a child of the print statement node
        self.consume_current_token() # Update the current token to the next token

        self.print_loop(print_statement_node) # Add the var value node as a child of the print statement node

        if self.check_if_token_matches_expected_token_types("suppress_newline_delimiter"):
            suppress_newline_delimiter_node = ParseTreeNode("<suppress-newline-delimiter>", print_statement_node)
            print_statement_node.add_child(suppress_newline_delimiter_node)
            self.addParseTreeNode(suppress_newline_delimiter_node)
            self.consume_current_token() # Update the current token to the next token

    # <assignment> ::= <varident> R <var-value>
    def assignment_statement(self, node_parent):
        assignment_statement_node = ParseTreeNode("<assignment>", node_parent)
        node_parent.add_child(assignment_statement_node)

        self.varident(assignment_statement_node)

        if self.check_if_token_matches_expected_token_types("variable_assignment_keyword"):
            self.addParseTreeNode(assignment_statement_node)
            self.consume_current_token()

            self.var_value(assignment_statement_node)
        else:
            # Error handling for missing assignment operator
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected assignment operator but got {self.current_token.token_type}")

    # <input> ::= GIMMEH <var>
    def input_statement(self, node_parent):
        input_statement_node = ParseTreeNode("<input>", node_parent)
        node_parent.add_child(input_statement_node)

        self.addParseTreeNode(input_statement_node) # Add the GIMMEH node as a child of the input statement node
        self.consume_current_token() # Update the current token to the next token

        self.varident(input_statement_node)

    # <casting> ::= MAEK <valid-casting> A <valid-type> | varident IS NOW A <valid-type>
    def casting_statement(self, node_parent):
        casting_node = ParseTreeNode("<casting>", node_parent)
        node_parent.add_child(casting_node)

        # TODO: implement IS NOW A

        self.addParseTreeNode(casting_node) # Add the MAEK node as a child of the casting node
        self.consume_current_token() # Update the current token to the next token

        self.varident(casting_node) # Add the varident node as a child of the casting node

        if self.check_if_token_matches_expected_token_types("type_casting_reassignment_operator"):
            self.addParseTreeNode(casting_node)
            self.consume_current_token()

            self.valid_type(casting_node)
        else:
            # Error handling for missing assignment operator
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected typecast reassignment operator but got {self.current_token.token_type}")

    # <code-block> ::= <print> | <expression> | <operator> | <if-then> | <loop-opt> | <assignment> | <input> | <function-call> | <switch> | <casting> | <concat> | <code-block>
    def codeblock(self, node_parent):
        # Check if the current token is the print keyword
        if self.check_if_token_matches_expected_token_types("print_keyword"):
            self.print_statement(node_parent)

        # Check if the current token is the assignment keyword
        if self.check_if_token_matches_expected_token_types("identifiers"):
            self.assignment_statement(node_parent)

        # Check if the current token is the input keyword
        if self.check_if_token_matches_expected_token_types("input_keyword"):
            self.input_statement(node_parent)

        # Check if the current token is the type casting keyword
        if self.check_if_token_matches_expected_token_types("type_casting_maek_delimiter"):
            self.casting_statement(node_parent)

        # Check if the current token is one of the keywords under expressions
        if self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
            self.expression(node_parent)

        # Check if the current token is still not the program end delimiter
        if not self.check_if_token_matches_expected_token_types("program_end_delimiter"):
            self.codeblock(node_parent)

    # <program> ::= <function> HAI <variable-declaration> <code-block> KTHXBYE <function>
    def program(self):
        # TODO: Check if the current token is the function declaration start delimiter
        # if self.current_token.token_type == "function_declaration_start_delimiter":

        # Check if the current token is the HAI keyword
        if self.check_if_token_matches_expected_token_types("program_start_delimiter"):
            start_delimiter_node = ParseTreeNode("<program-start-delimiter>", self.parse_tree)
            self.parse_tree.add_child(start_delimiter_node)
            self.addParseTreeNode(start_delimiter_node) # Add the HAI node as a child of the root node
            self.consume_current_token() # Update the current token to the next token

        # Check if the current token is the variable declaration start delimiter
        if self.check_if_token_matches_expected_token_types("variable_declaration_start_delimiter"):
            self.variable_declaration() # Call the variable declaration grammar rule

        # Check if the current token is already the statement start delimiter
        if not self.check_if_token_matches_expected_token_types("variable_declaration_start_delimiter"):
            codeblock_node = ParseTreeNode("<code-block>", self.parse_tree)
            self.parse_tree.add_child(codeblock_node)
            self.codeblock(codeblock_node)
        
        # Check if the current token is the KTHXBYE keyword
        if self.check_if_token_matches_expected_token_types("program_end_delimiter"):
            end_delimiter_node = ParseTreeNode("<program-end-delimiter>", self.parse_tree)
            self.parse_tree.add_child(end_delimiter_node)
            self.addParseTreeNode(end_delimiter_node)
            self.consume_current_token() # Update the current token to the next token

        # TODO: Check if the current token is the function declaration start delimiter

    # ===================== Functions for Removing Linebreak Delimiters =====================
    def remove_linebreak_delimiters(self):
        symbol_table_without_linebreaks = []

        for token in self.symbol_table:
            if token.token_type != "linebreak_delimiter":
                symbol_table_without_linebreaks.append(token)

        # Update the symbol table
        self.symbol_table = symbol_table_without_linebreaks
    # ======================================================================================

    # ===================== Functions for Validating and Removing Comments =====================
    def check_if_invalid_starting_multiline_comment(self, current_index):
        # Check if the multi-line comment has their own lines
        if self.symbol_table[current_index].line_number == self.symbol_table[current_index - 1].line_number:
            return True
        
        return False
    
    def check_if_invalid_closing_multiline_comment(self, current_index):
        # Check if the multi-line comment has their own lines
        if self.symbol_table[current_index].line_number == self.symbol_table[current_index + 1].line_number:
            if self.symbol_table[current_index + 1].token_type != "linebreak_delimiter":
                return True
        
        return False

    def check_if_comments_are_valid(self):
        for index, token in enumerate(self.symbol_table):
            if token.token_type == "opening_multi-line_comment_delimiter":
                if self.check_if_invalid_starting_multiline_comment(index) == True:
                    # Raise an error
                    raise Exception(f'Syntax Error in Line {token.line_number} \n\t Multi-line comments must have their own lines.')
            
            if token.token_type == "closing_multi-line_comment_delimiter":
                if self.check_if_invalid_closing_multiline_comment(index) == True:
                    # Raise an error
                    raise Exception(f'Syntax Error in Line {token.line_number} \n\t Multi-line comments must have their own lines.')

    def remove_all_comments(self):
        symbol_table_without_comments = []

        for index, token in enumerate(self.symbol_table):
            if token.token_type not in ["single-line_comment_delimiter", "opening_multi-line_comment_delimiter", "closing_multi-line_comment_delimiter", "comment_literal"]:
                symbol_table_without_comments.append(token)
            
            # Remove all linebreaks that are next to a single-line comment that has their own line
            if token.token_type == "single-line_comment_delimiter" and token.line_number != self.symbol_table[index - 1].line_number:
                # Empty single-line comment
                if self.symbol_table[index + 1].token_type == "linebreak_delimiter":
                    self.symbol_table.pop(index + 1)

                # Single-line comment with text
                if self.symbol_table[index + 1].token_type == "comment_literal":
                    self.symbol_table.pop(index + 2)

            # Remove all linebreaks that are next to a multi-line comment
            if token.token_type in ["opening_multi-line_comment_delimiter", "closing_multi-line_comment_delimiter"]:
                if self.symbol_table[index + 1].token_type == "linebreak_delimiter":
                    self.symbol_table.pop(index + 1)

        # Update the symbol table
        self.symbol_table = symbol_table_without_comments    
    # ==========================================================================================