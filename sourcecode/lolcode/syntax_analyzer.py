"""
    This file is used to define the syntax analyzer for the lolcode language.
"""

from Classes.lol_node import ParseTreeNode

class SyntaxAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.parse_tree = None

        self.current_token = symbol_table[0]
        self.previous_token = None

        self.current_number_of_nested_arithmetic_operand_operations = 0
        self.current_number_of_nested_boolean_operand_operations = 0
        self.current_number_of_nested_comparison_operand_operations = 0
        self.currently_reading_infinite_arity_boolean_operator = False
        self.currently_inside_variable_declaration_section = False
        self.isReadingBinaryBooleanOperation = False

    def run_syntax_analyzer(self):
        self.analyze()
        
    def check_if_symbol_table_is_empty(self):
        if len(self.symbol_table) == 0:
            return True
        else:
            return False
        
    def check_if_program_delimiters_are_present(self):
        # Check if the program start and end delimiters are present anywhere in the symbol table
        if "program_start_delimiter" in [token.get_token_type() for token in self.symbol_table] and "program_end_delimiter" in [token.get_token_type() for token in self.symbol_table]:
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
            return
        else:
            self.current_token = self.symbol_table[0]

    def addParseTreeNode(self, node_parent):
        node = ParseTreeNode(self.current_token.get_lexeme(), node_parent, self.current_token.line_number)
        node_parent.add_child(node)
        return node

    def analyze(self):
        # Remove all comments and linebreak delimiters
        self.check_if_comments_are_valid()
        self.remove_all_comments()
        self.remove_linebreak_delimiters()

        # Update the current token if there are still tokens left
        if self.check_if_symbol_table_is_empty():
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Empty file")
        else:
            self.current_token = self.symbol_table[0]

        # Check if the program delimiters are present
        if not self.check_if_program_delimiters_are_present():
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Missing program start and/or end delimiters")

        # Create the root node of the parse tree
        self.parse_tree = ParseTreeNode("<program>", None, None)
        self.program() # Start the parsing from the <program> grammar rule

    def print_parse_tree(self):
        self.parse_tree.print_tree(0)
    
    # ===================== Functions for the Grammar Rules =====================
    # <data-type> ::= NUMBR | NUMBAR | YARN | TROOF | NOOB
    def data_type(self, node_parent):
        if self.current_token.get_lexeme() == "NUMBR":
            integer_type_node = ParseTreeNode("<integer-data-type>", node_parent, self.current_token.line_number)
            node_parent.add_child(integer_type_node)

            self.addParseTreeNode(integer_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "NUMBAR":
            float_type_node = ParseTreeNode("<float-data-type>", node_parent, self.current_token.line_number)
            node_parent.add_child(float_type_node)
            
            self.addParseTreeNode(float_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "YARN":
            string_type_node = ParseTreeNode("<string-data-type>", node_parent, self.current_token.line_number)
            node_parent.add_child(string_type_node)
            
            self.addParseTreeNode(string_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "TROOF":
            boolean_type_node = ParseTreeNode("<boolean-data-type>", node_parent, self.current_token.line_number)
            node_parent.add_child(boolean_type_node)

            self.addParseTreeNode(boolean_type_node)
            self.consume_current_token()
        elif self.current_token.get_lexeme() == "NOOB":
            null_type_node = ParseTreeNode("<null-data-type>", node_parent, self.current_token.line_number)
            node_parent.add_child(null_type_node)

            self.addParseTreeNode(null_type_node)
            self.consume_current_token()
        else:
            # Error handling for invalid data type
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected data type but got {self.current_token.token_type}")
    
    # <valid-type> ::= <data-type>
    def valid_type(self, node_parent):
        if self.check_if_token_matches_expected_token_types("type_literal"):
            valid_type_node = ParseTreeNode("<valid-data-type>", node_parent, self.current_token.line_number)
            node_parent.add_child(valid_type_node)
            self.data_type(valid_type_node) # Add the data type node as a child of the valid type node
        else:
            # Error handling for invalid type
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected valid type but got {self.current_token.token_type}")

    # <literal-value> ::= numbr_literal | numbar_literal | yarn_literal | troof_literal
    def literal_value(self, node_parent):
        if self.current_token.get_token_type() == "string_delimiter":
            yarn_literal_node = ParseTreeNode("<yarn-literal>", node_parent, self.current_token.line_number)
            node_parent.add_child(yarn_literal_node)

            self.consume_current_token() # Skip the string delimiter
            self.addParseTreeNode(yarn_literal_node)
            self.consume_current_token()
            self.consume_current_token() # Skip the string delimiter
        elif self.current_token.get_token_type() == "numbr_literal":
            numbr_literal_node = ParseTreeNode("<numbr-literal>", node_parent, self.current_token.line_number)
            node_parent.add_child(numbr_literal_node)

            self.addParseTreeNode(numbr_literal_node)
            self.consume_current_token()
        elif self.current_token.get_token_type() == "numbar_literal":
            numbar_literal_node = ParseTreeNode("<numbar-literal>", node_parent, self.current_token.line_number)
            node_parent.add_child(numbar_literal_node)

            self.addParseTreeNode(numbar_literal_node)
            self.consume_current_token()
        elif self.current_token.get_token_type() == "troof_literal":
            troof_literal_node = ParseTreeNode("<troof-literal>", node_parent, self.current_token.line_number)
            node_parent.add_child(troof_literal_node)

            self.addParseTreeNode(troof_literal_node)
            self.consume_current_token()
        else:
            # Error handling for invalid literal value
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected literal value but got {self.current_token.token_type}")
    
    # <arithmetic-value-operands> ::= <var-value> AN <var-value>
    def arithmetic_value_operands(self, node_parent):
        arithmetic_value_operand_node = ParseTreeNode("<arithmetic-value-operands>", node_parent, self.current_token.line_number)
        node_parent.add_child(arithmetic_value_operand_node)

        self.var_value(arithmetic_value_operand_node)

        # Check for the AN keyword
        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", arithmetic_value_operand_node, self.current_token.line_number)
            arithmetic_value_operand_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.var_value(arithmetic_value_operand_node)

            self.current_number_of_nested_arithmetic_operand_operations -= 1
        else:
            # Error handling for invalid arithmetic value operand
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected another arithmetic value operand but got {self.current_token.token_type}")

    # <arithmetic-expression> ::= SUM OF <arithmetic-value-operands> | DIFF OF <arithmetic-value-operands> | PRODUKT OF <arithmetic-value-operands> | QUOSHUNT OF <arithmetic-value-operands> | MOD OF <arithmetic-value-operands> | BIGGR OF <arithmetic-value-operands> | SMALLR OF <arithmetic-value-operands> 
    def arithmetic_expression(self, node_parent):
        arith_statement_node = ParseTreeNode("<arithmetic-expression>", node_parent, self.current_token.line_number)
        node_parent.add_child(arith_statement_node)
        self.current_number_of_nested_arithmetic_operand_operations += 1

        if self.current_token.get_lexeme() == "SUM OF":
            sum_operator_node = ParseTreeNode("<addition-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(sum_operator_node)
            self.addParseTreeNode(sum_operator_node) # Add the SUM OF node as a child of the arithmetic statement node
            self.consume_current_token() # Update the current token to the next token
            
            self.arithmetic_value_operands(sum_operator_node) # Add the arithmetic expression node as a child of the arithmetic statement node
        elif self.current_token.get_lexeme() == "DIFF OF":
            difference_operator_node = ParseTreeNode("<subtraction-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(difference_operator_node)
            self.addParseTreeNode(difference_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(difference_operator_node)
        elif self.current_token.get_lexeme() == "PRODUKT OF":
            product_operator_node = ParseTreeNode("<multiplication-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(product_operator_node)
            self.addParseTreeNode(product_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(product_operator_node)
        elif self.current_token.get_lexeme() == "QUOSHUNT OF":
            quotient_operator_node = ParseTreeNode("<division-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(quotient_operator_node)
            self.addParseTreeNode(quotient_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(quotient_operator_node)
        elif self.current_token.get_lexeme() == "MOD OF":
            modulo_operator_node = ParseTreeNode("<modulo-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(modulo_operator_node)
            self.addParseTreeNode(modulo_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(modulo_operator_node)
        elif self.current_token.get_lexeme() == "BIGGR OF":
            max_operator_node = ParseTreeNode("<max-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(max_operator_node)
            self.addParseTreeNode(max_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(max_operator_node)
        elif self.current_token.get_lexeme() == "SMALLR OF":
            min_operator_node = ParseTreeNode("<min-operator>", arith_statement_node, self.current_token.line_number)
            arith_statement_node.add_child(min_operator_node)
            self.addParseTreeNode(min_operator_node)
            self.consume_current_token()

            self.arithmetic_value_operands(min_operator_node)
        else:
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected arithmetic operator but got {self.current_token.token_type}")

        if self.current_number_of_nested_arithmetic_operand_operations == 0 and self.current_number_of_nested_boolean_operand_operations == 0 and self.current_number_of_nested_comparison_operand_operations == 0 and self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Arithmetic operations are only binary")

    # <boolean-value-operands> ::= <var-value> AN <var-value> | NOT <var-value> AN <var-value> | <var-value> AN NOT <var-value> | NOT <var-value> AN <var-value> | NOT <var-value>
    def boolean_value_operands(self, node_parent):
        boolean_value_operand_node = ParseTreeNode("<boolean-value-operands>", node_parent, self.current_token.line_number)
        node_parent.add_child(boolean_value_operand_node)

        if self.current_token.get_lexeme() == "NOT":
            not_operator_node = ParseTreeNode("<not-operator>", boolean_value_operand_node, self.current_token.line_number)
            boolean_value_operand_node.add_child(not_operator_node)
            self.addParseTreeNode(not_operator_node)
            self.consume_current_token()

            if self.isReadingBinaryBooleanOperation == False and self.currently_reading_infinite_arity_boolean_operator == True:
                self.var_value(not_operator_node)
                return
            
            self.var_value(not_operator_node)
        else:
            if self.isReadingBinaryBooleanOperation == False and self.currently_reading_infinite_arity_boolean_operator == True:
                self.var_value(boolean_value_operand_node)
                return
            
            self.var_value(boolean_value_operand_node)

        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", boolean_value_operand_node, self.current_token.line_number)
            boolean_value_operand_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            if self.current_token.get_lexeme() == "NOT":
                not_operator_node = ParseTreeNode("<not-operator>", boolean_value_operand_node, self.current_token.line_number)
                boolean_value_operand_node.add_child(not_operator_node)
                self.addParseTreeNode(not_operator_node)
                self.consume_current_token()

                self.var_value(not_operator_node)
            else:
                self.var_value(boolean_value_operand_node)

            self.current_number_of_nested_boolean_operand_operations -= 1
            self.isReadingBinaryBooleanOperation = False
        elif self.current_number_of_nested_boolean_operand_operations > 0 and not self.check_if_token_matches_expected_token_types("operand_separator_keyword") and self.currently_reading_infinite_arity_boolean_operator == False:
            # Error handling for invalid logical value operand
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected another boolean value operand but got {self.current_token.token_type}")

    # <boolean-operations> ::= BOTH OF <boolean-value-operands> | EITHER OF <boolean-value-operands> | WON OF <boolean-value-operands> | <boolean-value-operands>
    def boolean_operations(self, node_parent):
        boolean_operation_node = ParseTreeNode("<boolean-operations>", node_parent, self.current_token.line_number)
        node_parent.add_child(boolean_operation_node)

        if self.current_token.get_lexeme() in ["BOTH OF", "EITHER OF", "WON OF"]:
            self.current_number_of_nested_boolean_operand_operations += 1
            self.isReadingBinaryBooleanOperation = True

        if self.current_token.get_lexeme() == "BOTH OF":
            and_operator_node = ParseTreeNode("<and-operator>", boolean_operation_node, self.current_token.line_number)
            boolean_operation_node.add_child(and_operator_node)
            self.addParseTreeNode(and_operator_node)
            self.consume_current_token()

            self.boolean_value_operands(and_operator_node)
        elif self.current_token.get_lexeme() == "EITHER OF":
            or_operator_node = ParseTreeNode("<or-operator>", boolean_operation_node, self.current_token.line_number)
            boolean_operation_node.add_child(or_operator_node)
            self.addParseTreeNode(or_operator_node)
            self.consume_current_token()

            self.boolean_value_operands(or_operator_node)
        elif self.current_token.get_lexeme() == "WON OF":
            xor_operator_node = ParseTreeNode("<xor-operator>", boolean_operation_node, self.current_token.line_number)
            boolean_operation_node.add_child(xor_operator_node)
            self.addParseTreeNode(xor_operator_node)
            self.consume_current_token()

            self.boolean_value_operands(xor_operator_node)
        else:
            self.boolean_value_operands(boolean_operation_node)

        if self.current_number_of_nested_arithmetic_operand_operations == 0 and self.current_number_of_nested_boolean_operand_operations == 0 and self.current_number_of_nested_comparison_operand_operations == 0 and self.check_if_token_matches_expected_token_types("operand_separator_keyword") and self.currently_reading_infinite_arity_boolean_operator == False:
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Boolean operations are only binary")

    # <boolean-expression> ::= ALL OF <boolean-operations> MKAY | ANY OF <boolean-operations> MKAY
    def boolean_expression(self, node_parent):
        boolean_statement_node = ParseTreeNode("<boolean-expression>", node_parent, self.current_token.line_number)
        node_parent.add_child(boolean_statement_node)

        if self.current_token.get_lexeme() == "ALL OF":
            if self.currently_reading_infinite_arity_boolean_operator == True:
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Infinite arity boolean operators cannot be nested with each other and themselves")

            infinite_and_operator_node = ParseTreeNode("<infinite-arity-and-operator>", boolean_statement_node, self.current_token.line_number)
            boolean_statement_node.add_child(infinite_and_operator_node)
            self.addParseTreeNode(infinite_and_operator_node)
            self.consume_current_token()
            self.currently_reading_infinite_arity_boolean_operator = True

            self.boolean_operations(infinite_and_operator_node)

            if self.currently_reading_infinite_arity_boolean_operator == True:
                while self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
                    operator_separator_node = ParseTreeNode("<operator-separator-operator>", infinite_and_operator_node, self.current_token.line_number)
                    infinite_and_operator_node.add_child(operator_separator_node)
                    self.addParseTreeNode(operator_separator_node)
                    self.consume_current_token()

                    self.boolean_operations(infinite_and_operator_node)

                if self.check_if_token_matches_expected_token_types("multi_operator_closing_delimiter"):
                    infinite_and_operator_end_delimiter_node = ParseTreeNode("<multiple-operator-closing-delimiter>", infinite_and_operator_node, self.current_token.line_number)
                    infinite_and_operator_node.add_child(infinite_and_operator_end_delimiter_node)
                    self.addParseTreeNode(infinite_and_operator_end_delimiter_node)
                    self.consume_current_token()
                    self.currently_reading_infinite_arity_boolean_operator = False
        elif self.current_token.get_lexeme() == "ANY OF":
            if self.currently_reading_infinite_arity_boolean_operator == True:
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Infinite arity boolean operators cannot be nested with each other and themselves")

            infinite_or_operator_node = ParseTreeNode("<infinite-arity-or-operator>", boolean_statement_node, self.current_token.line_number)
            boolean_statement_node.add_child(infinite_or_operator_node)
            self.addParseTreeNode(infinite_or_operator_node)
            self.consume_current_token()
            self.currently_reading_infinite_arity_boolean_operator = True

            self.boolean_operations(infinite_or_operator_node)

            if self.currently_reading_infinite_arity_boolean_operator == True:
                while self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
                    operator_separator_node = ParseTreeNode("<operator-separator-operator>", infinite_or_operator_node, self.current_token.line_number)
                    infinite_or_operator_node.add_child(operator_separator_node)
                    self.addParseTreeNode(operator_separator_node)
                    self.consume_current_token()

                    self.boolean_operations(infinite_or_operator_node)
                
                if self.check_if_token_matches_expected_token_types("multi_operator_closing_delimiter"):
                    infinite_or_operator_end_delimiter_node = ParseTreeNode("<multiple-operator-closing-delimiter>", infinite_or_operator_node, self.current_token.line_number)
                    infinite_or_operator_node.add_child(infinite_or_operator_end_delimiter_node)
                    self.addParseTreeNode(infinite_or_operator_end_delimiter_node)
                    self.consume_current_token()
                    self.currently_reading_infinite_arity_boolean_operator = False
        else:
            self.boolean_operations(boolean_statement_node)

    # <comparison-value-operands> ::= <var-value> AN <var-value> | <var-value> AN BIGGR OF <var-value> | <var-value> AN SMALLR OF <var-value>
    def comparison_value_operands(self, node_parent):
        comparison_value_operand_node = ParseTreeNode("<comparison-value-operands>", node_parent, self.current_token.line_number)
        node_parent.add_child(comparison_value_operand_node)

        self.var_value(comparison_value_operand_node)

        # Check for the AN keyword
        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", comparison_value_operand_node, self.current_token.line_number)
            comparison_value_operand_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.var_value(comparison_value_operand_node)

            self.current_number_of_nested_comparison_operand_operations -= 1
        else:
            # Error handling for invalid comparison value operand
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected another comparison value operand but got {self.current_token.token_type}")

    # <comparison-expression> ::= BOTH SAEM <comparison-value-operands> | DIFFRINT <comparison-value-operands>
    def comparison_expression(self, node_parent):
        comparison_statement_node = ParseTreeNode("<comparison-expression>", node_parent, self.current_token.line_number)
        node_parent.add_child(comparison_statement_node)
        self.current_number_of_nested_comparison_operand_operations += 1

        if self.current_token.lexeme == "BOTH SAEM":
            equal_operator_node = ParseTreeNode("<equal-operator>", comparison_statement_node, self.current_token.line_number)
            comparison_statement_node.add_child(equal_operator_node)
            self.addParseTreeNode(equal_operator_node)
            self.consume_current_token()

            self.comparison_value_operands(equal_operator_node)
        elif self.current_token.lexeme == "DIFFRINT":
            not_equal_operator_node = ParseTreeNode("<not-equal-operator>", comparison_statement_node, self.current_token.line_number)
            comparison_statement_node.add_child(not_equal_operator_node)
            self.addParseTreeNode(not_equal_operator_node)
            self.consume_current_token()

            self.comparison_value_operands(not_equal_operator_node)
        else:
            # Error handling for invalid comparison operator
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected comparison operator but got {self.current_token.token_type}")

        if self.current_number_of_nested_arithmetic_operand_operations == 0 and self.current_number_of_nested_boolean_operand_operations == 0 and self.current_number_of_nested_comparison_operand_operations == 0 and self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Comparison operations are only binary")

    # <concat-loop> ::= <var-value> | <var-value> AN <concat-loop>
    def concat_loop(self, node_parent):
        concat_loop_node = ParseTreeNode("<concat-loop>", node_parent, self.current_token.line_number)
        node_parent.add_child(concat_loop_node)

        self.var_value(concat_loop_node)

        if self.check_if_token_matches_expected_token_types("operand_separator_keyword"):
            operand_separator_node = ParseTreeNode("<operand-separator-operator>", concat_loop_node, self.current_token.line_number)
            concat_loop_node.add_child(operand_separator_node)
            self.addParseTreeNode(operand_separator_node)
            self.consume_current_token()

            self.concat_loop(concat_loop_node)

    # <concatenation-expression> ::= SMOOSH <concat-loop> | SMOOSH <concat-loop> MKAY
    def concatenation_expression(self, node_parent):
        concat_statement_node = ParseTreeNode("<concatenation-expression>", node_parent, self.current_token.line_number)
        node_parent.add_child(concat_statement_node)

        concatenation_start_delimiter_node = ParseTreeNode("<concatenation-start-delimiter>", concat_statement_node, self.current_token.line_number)
        concat_statement_node.add_child(concatenation_start_delimiter_node)
        self.addParseTreeNode(concatenation_start_delimiter_node) # Add the SMOOSH node as a child of the concat statement node
        self.consume_current_token() # Update the current token to the next token

        self.concat_loop(concat_statement_node) # Add the concat loop node as a child of the concat statement node

        if self.check_if_token_matches_expected_token_types("multi_operator_closing_delimiter"):
            concatenation_end_delimiter_node = ParseTreeNode("<multiple-operator-closing-delimiter>", concat_statement_node, self.current_token.line_number)
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
        else:
            # Error handling for invalid expression
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected expression but got {self.current_token.token_type}")

        # Check if the current token is an opening conditional statement delimiter
        if self.check_if_token_matches_expected_token_types("opening_conditional_statement_delimiter"):
            self.if_then_statement(node_parent) # Add the if then statement node as a child of the conditional statement node

    # <var-value> ::= literal | varident | <expression>
    def var_value(self, node_parent):
        var_value_node = ParseTreeNode("<var-value>", node_parent, self.current_token.line_number)
        node_parent.add_child(var_value_node)

        # If the value is a literal
        if self.current_token.token_type in ["numbr_literal", "numbar_literal", "string_delimiter", "troof_literal"]:
            literal_value_node = ParseTreeNode("<literal-value>", var_value_node, self.current_token.line_number)
            var_value_node.add_child(literal_value_node)

            self.literal_value(literal_value_node) # Add the literal value node as a child of the var value node
        # If the value is a variable identifier
        elif self.current_token.token_type == "identifiers":
            variable_value_node = ParseTreeNode("<variable-value>", var_value_node, self.current_token.line_number)
            var_value_node.add_child(variable_value_node)

            self.addParseTreeNode(variable_value_node)
            self.consume_current_token()
        # If the value is an expression
        elif self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
            expression_value_node = ParseTreeNode("<expression-value>", var_value_node, self.current_token.line_number)
            var_value_node.add_child(expression_value_node)

            self.expression(expression_value_node) # Add the expression node as a child of the var value node
        else:
            # Error handling for invalid var value
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected literal, variable identifier, or expression but got {self.current_token.token_type}")

    # <varident> ::= identifier | identifier ITZ <var-value>
    def varident(self, node_parent):
        if self.check_if_token_matches_expected_token_types("identifiers"):
            identifier_node = ParseTreeNode("<identifier>", node_parent, self.current_token.line_number)
            node_parent.add_child(identifier_node)
            self.addParseTreeNode(identifier_node)
            self.consume_current_token()

            if self.check_if_token_matches_expected_token_types("variable_initialization_keyword"):
                if self.currently_inside_variable_declaration_section == False:
                    raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Variable initialization keyword cannot be used outside variable declaration section of the program")

                var_node_initialization = ParseTreeNode("<var-initialization>", node_parent, self.current_token.line_number)
                node_parent.add_child(var_node_initialization)
                
                var_initialization_keyword = ParseTreeNode("<variable-initialization-keyword>", var_node_initialization, self.current_token.line_number)
                var_node_initialization.add_child(var_initialization_keyword)
                self.addParseTreeNode(var_initialization_keyword) # Add the ITZ node as a child of the var initialization keyword
                self.consume_current_token() # Update the current token to the next token

                self.var_value(var_node_initialization) # Add the var value node as a child of the var node initialization
        else:
            # Error handling for invalid variable identifier
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected identifier but got {self.current_token.token_type}")

    # <var> ::= I HAS A <varident> | I HAS A <varident> ITZ <var-value>
    def var(self, node_parent):
        var_node = ParseTreeNode("<var>", node_parent, self.current_token.line_number)
        node_parent.add_child(var_node)

        var_declaration_keyword_node = ParseTreeNode("<var-declaration-keyword>", var_node, self.current_token.line_number)
        var_node.add_child(var_declaration_keyword_node)
        self.addParseTreeNode(var_declaration_keyword_node) # Add the I HAS A node as a child of the var node
        self.consume_current_token() # Update the current token to the next token
        
        self.varident(var_node) # Add the varident node as a child of the var node

        # Check if the current token is still a variable declaration start delimiter
        if self.check_if_token_matches_expected_token_types("variable_declaration_keyword"):
            self.var(node_parent)

    # <variable-declaration> ::= WAZZUP <var> BUHBYE
    def variable_declaration(self, node_parent):
        variable_declaration_start_delimiter_node = ParseTreeNode("<variable-declaration-start-delimiter>", node_parent, self.current_token.line_number)
        node_parent.add_child(variable_declaration_start_delimiter_node)
        self.addParseTreeNode(variable_declaration_start_delimiter_node) # Add the WAZZUP node as a child of the variable declaration node
        self.consume_current_token() # Update the current token to the next token

        if self.check_if_token_matches_expected_token_types("variable_declaration_keyword"):
            self.var(node_parent) # Add the var node as a child of the variable declaration node

        if self.check_if_token_matches_expected_token_types("variable_declaration_end_delimiter"):
            variable_declaration_end_delimiter_node = ParseTreeNode("<variable-declaration-end-delimiter>", node_parent, self.current_token.line_number)
            node_parent.add_child(variable_declaration_end_delimiter_node)
            self.addParseTreeNode(variable_declaration_end_delimiter_node) # Add the BUHBYE node as a child of the variable declaration node
            self.consume_current_token() # Update the current token to the next token

            self.currently_inside_variable_declaration_section = False
        else:
            # Error handling for missing BUHBYE keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected variable declaration end delimiter but got {self.current_token.token_type}")
    
    # <print-loop> ::= <var-value> | <var-value> + <print-loop>
    def print_loop(self, node_parent):
        print_loop_node = ParseTreeNode("<print-loop>", node_parent, self.current_token.line_number)
        node_parent.add_child(print_loop_node)

        self.var_value(print_loop_node)

        if self.check_if_token_matches_expected_token_types("visible_concatenate_operator"):
            visible_concatenate_operator = ParseTreeNode("<visible-concatenate-operator>", print_loop_node, self.current_token.line_number)
            print_loop_node.add_child(visible_concatenate_operator)
            self.addParseTreeNode(visible_concatenate_operator)
            self.consume_current_token()

            self.print_loop(print_loop_node)

    # <print> ::= VISIBLE <print-loop> | VISIBLE <print-loop> ! 
    def print_statement(self, node_parent):
        print_statement_node = ParseTreeNode("<print>", node_parent, self.current_token.line_number)
        node_parent.add_child(print_statement_node)

        visible_operator = ParseTreeNode("<visible-operator>", print_statement_node, self.current_token.line_number)
        print_statement_node.add_child(visible_operator)
        self.addParseTreeNode(visible_operator) # Add the VISIBLE node as a child of the print statement node
        self.consume_current_token() # Update the current token to the next token

        self.print_loop(print_statement_node) # Add the var value node as a child of the print statement node

        if self.check_if_token_matches_expected_token_types("suppress_newline_delimiter"):
            suppress_newline_delimiter_node = ParseTreeNode("<suppress-newline-delimiter>", print_statement_node, self.current_token.line_number)
            print_statement_node.add_child(suppress_newline_delimiter_node)
            self.addParseTreeNode(suppress_newline_delimiter_node)
            self.consume_current_token() # Update the current token to the next token

    # <assignment> ::= <varident> R <var-value> | <varident> R <casting> | <varident> IS NOW A <valid-type>
    def assignment_statement(self, node_parent):
        assignment_statement_node = ParseTreeNode("<assignment>", node_parent, self.current_token.line_number)
        node_parent.add_child(assignment_statement_node)

        self.varident(assignment_statement_node)

        if self.check_if_token_matches_expected_token_types("variable_assignment_keyword"):
            variable_assignment_node = ParseTreeNode("<variable-assignment-operator>", assignment_statement_node, self.current_token.line_number)
            assignment_statement_node.add_child(variable_assignment_node)
            self.addParseTreeNode(variable_assignment_node)
            self.consume_current_token()

            # Check if it is a type casting assignment or a value assignment
            if self.check_if_token_matches_expected_token_types("type_casting_delimiter"):
                self.casting_statement(assignment_statement_node)
            else:
                self.var_value(assignment_statement_node)
        elif self.check_if_token_matches_expected_token_types("type_casting_assignment_operator"):
            type_casting_assignment_node = ParseTreeNode("<type-casting-assignment-operator>", assignment_statement_node, self.current_token.line_number)
            assignment_statement_node.add_child(type_casting_assignment_node)
            self.addParseTreeNode(type_casting_assignment_node)
            self.consume_current_token()

            self.valid_type(type_casting_assignment_node)

    # <input> ::= GIMMEH <varident>
    def input_statement(self, node_parent):
        input_statement_node = ParseTreeNode("<input>", node_parent, self.current_token.line_number)
        node_parent.add_child(input_statement_node)

        input_operator = ParseTreeNode("<input-operator>", input_statement_node, self.current_token.line_number)
        input_statement_node.add_child(input_operator)
        self.addParseTreeNode(input_operator) # Add the GIMMEH node as a child of the input statement node
        self.consume_current_token() # Update the current token to the next token

        self.varident(input_statement_node)

    # <casting> ::= MAEK <var-value> A <valid-type> | MAEK <var-value> <valid-type> 
    def casting_statement(self, node_parent):
        casting_node = ParseTreeNode("<casting>", node_parent, self.current_token.line_number)
        node_parent.add_child(casting_node)

        type_casting_operator = ParseTreeNode("<type-casting-operator>", casting_node, self.current_token.line_number)
        casting_node.add_child(type_casting_operator)
        self.addParseTreeNode(type_casting_operator) # Add the MAEK node as a child of the casting node
        self.consume_current_token() # Update the current token to the next token

        self.var_value(casting_node) # Add the varident node as a child of the casting node

        if self.check_if_token_matches_expected_token_types("type_casting_reassignment_operator"):
            type_casting_reassignment_node = ParseTreeNode("<type-casting-reassignment-operator>", casting_node, self.current_token.line_number)
            casting_node.add_child(type_casting_reassignment_node)
            self.addParseTreeNode(type_casting_reassignment_node)
            self.consume_current_token()

            self.valid_type(casting_node)
        else:
            self.valid_type(casting_node)
        
    # Specialized codeblock for control flow statements
    def flow_control_codeblock(self, node_parent):
        # Check if the current token is the print keyword
        if self.check_if_token_matches_expected_token_types("print_keyword"):
            self.print_statement(node_parent)

        # FOR IF-ELSE STATEMENTS
        # Check if the current token is the if keyword
        if self.check_if_token_matches_expected_token_types("opening_conditional_statement_delimiter"):
            self.if_then_statement(node_parent)

        # Check if the current token is the loop keyword
        if self.check_if_token_matches_expected_token_types("loop_keyword"):
            self.loop_statement(node_parent)

        # Check if the current token is an identifier for the assignment keyword/typecasting assignment keyword
        if self.check_if_token_matches_expected_token_types("identifiers"):
            self.assignment_statement(node_parent)

        # Check if the current token is a literal value
        if self.current_token.token_type in ["numbr_literal", "numbar_literal", "string_delimiter", "troof_literal"]:
            self.var_value(node_parent)

        # Check if the current token is the input keyword
        if self.check_if_token_matches_expected_token_types("input_keyword"):
            self.input_statement(node_parent)

        # Check if the current token is the switch keyword
        if self.check_if_token_matches_expected_token_types("opening_switch_statement_delimiter"):
            self.switch_statement(node_parent)

        # Check if the current token is the type casting keyword
        if self.check_if_token_matches_expected_token_types("type_casting_delimiter"):
            self.casting_statement(node_parent)

        # Check if the current token is one of the keywords under expressions
        if self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
            self.expression(node_parent)

        # Check if the current token is the break keyword for switch statements
        if self.check_if_token_matches_expected_token_types("switch_statement_break_delimiter"):
            return # Return to the switch statement function

        # Check if the current token is still not a switch statement delimiter and is still not a conditional statement delimiter
        if not self.check_if_token_matches_expected_token_types("switch_statement_delimiter") and not self.check_if_token_matches_expected_token_types("alternative_switch_statement_delimiter") and not self.check_if_token_matches_expected_token_types("closing_conditional_statement_delimiter") \
            and not self.check_if_token_matches_expected_token_types("alternative_conditional_statement_delimiter") and not self.check_if_token_matches_expected_token_types("else_conditional_statement_delimiter") and not self.check_if_token_matches_expected_token_types("closing_conditional_statement_delimiter"):
            self.flow_control_codeblock(node_parent)

    # <mebbe-loop> :== <mebbe-loop> | <mebbe-loop> <mebbe-loop>
    def mebbe_loop(self, node_parent):
        mebbe_loop_node = ParseTreeNode("<mebbe-loop>", node_parent, self.current_token.line_number)
        node_parent.add_child(mebbe_loop_node)
        
        mebbe_statement_delimiter = ParseTreeNode("<mebbe-statement-delimiter>", mebbe_loop_node, self.current_token.line_number)
        mebbe_loop_node.add_child(mebbe_statement_delimiter)
        self.addParseTreeNode(mebbe_statement_delimiter)
        self.consume_current_token()
    
        expression_statement_node = ParseTreeNode("<expression-statement>", mebbe_loop_node, self.current_token.line_number)
        mebbe_loop_node.add_child(expression_statement_node)

        self.expression(expression_statement_node)    

        codeblock_statement_node = ParseTreeNode("<code-block-statement>", mebbe_loop_node, self.current_token.line_number)
        mebbe_loop_node.add_child(codeblock_statement_node)

        self.flow_control_codeblock(codeblock_statement_node)

        # Check if the current token is another MEBBE
        if self.check_if_token_matches_expected_token_types("alternative_conditional_statement_delimiter"):
            self.mebbe_loop(node_parent)

    # <if_then> ::= <conditional-statement> O RLY? YA RLY <if-else-code-block> NO WAI <else-code-block> OIC
    def if_then_statement(self, node_parent):
        if_then_statement_node = ParseTreeNode("<conditional-statement>", node_parent, self.current_token.line_number)
        node_parent.add_child(if_then_statement_node)

        conditional_statement_start_delimiter_node = ParseTreeNode("<conditional-statement-start-delimiter>", if_then_statement_node, self.current_token.line_number)
        if_then_statement_node.add_child(conditional_statement_start_delimiter_node)
        self.addParseTreeNode(conditional_statement_start_delimiter_node)
        self.consume_current_token()

        # Get the YA RLY keyword
        if self.check_if_token_matches_expected_token_types("if_conditional_statement_delimiter"):
            if_statement_node = ParseTreeNode("<if-statement>", if_then_statement_node, self.current_token.line_number)
            if_then_statement_node.add_child(if_statement_node)

            if_conditional_statement_delimiter = ParseTreeNode("<if-delimiter>", if_statement_node, self.current_token.line_number)
            if_statement_node.add_child(if_conditional_statement_delimiter)
            self.addParseTreeNode(if_conditional_statement_delimiter)
            self.consume_current_token()

            codeblock_statement_node = ParseTreeNode("<code-block-statement>", if_statement_node, self.current_token.line_number)
            if_statement_node.add_child(codeblock_statement_node)

            self.flow_control_codeblock(codeblock_statement_node)

            # Check if the current token is MEBBE
            if self.check_if_token_matches_expected_token_types("alternative_conditional_statement_delimiter"):
                self.mebbe_loop(if_then_statement_node)

            # Check if the current token is the NO WAI keyword
            if self.check_if_token_matches_expected_token_types("else_conditional_statement_delimiter"):
                else_statement_node = ParseTreeNode("<else-statement>", if_then_statement_node, self.current_token.line_number)
                if_then_statement_node.add_child(else_statement_node)
                
                else_conditional_statement_delimiter = ParseTreeNode("<else-delimiter>", else_statement_node, self.current_token.line_number)
                else_statement_node.add_child(else_conditional_statement_delimiter)
                self.addParseTreeNode(else_conditional_statement_delimiter)
                self.consume_current_token()

                # add NO WAI's code block
                codeblock_statement_node = ParseTreeNode("<code-block-statement>", else_statement_node, self.current_token.line_number)
                else_statement_node.add_child(codeblock_statement_node)

                self.flow_control_codeblock(codeblock_statement_node)
            
            # Check if the current token is the OIC keyword
            if self.check_if_token_matches_expected_token_types("closing_conditional_statement_delimiter"):
                conditional_statement_end_delimiter = ParseTreeNode("<closing-conditional-statement-delimiter>", if_then_statement_node, self.current_token.line_number)
                if_then_statement_node.add_child(conditional_statement_end_delimiter)
                self.addParseTreeNode(conditional_statement_end_delimiter)
                self.consume_current_token()
            else:
                # Error handling for missing OIC keyword
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected conditional statement end delimiter but got {self.current_token.token_type}")
        else:
            # Error handling for missing YA RLY keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected if conditional statement start delimiter but got {self.current_token.token_type}")

    # <omg-loop> :== OMG <literal-value> <code-block> <omg-loop> | OMG <literal-value> <code-block> OMGWTF <code-block>
    def omg_loop(self, node_parent):
        omg_loop_node = ParseTreeNode("<omg-loop>", node_parent, self.current_token.line_number)
        node_parent.add_child(omg_loop_node)

        if self.check_if_token_matches_expected_token_types("switch_statement_delimiter"):
            switch_statement_delimiter_node = ParseTreeNode("<switch-statement-delimiter>", omg_loop_node, self.current_token.line_number)
            omg_loop_node.add_child(switch_statement_delimiter_node)
            self.addParseTreeNode(switch_statement_delimiter_node)
            self.consume_current_token()

            if self.current_token.token_type in ["numbr_literal", "numbar_literal", "string_delimiter", "troof_literal"]:
                literal_value_node = ParseTreeNode("<literal-value>", omg_loop_node, self.current_token.line_number)
                omg_loop_node.add_child(literal_value_node)

                self.literal_value(literal_value_node) # Add the literal value node as a child of the var value node
            else:
                # Error handling for invalid var value
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected literal but got {self.current_token.token_type}")

            codeblock_statement_node = ParseTreeNode("<code-block-statement>", omg_loop_node, self.current_token.line_number)
            omg_loop_node.add_child(codeblock_statement_node)

            self.flow_control_codeblock(codeblock_statement_node)

            if self.check_if_token_matches_expected_token_types("switch_statement_break_delimiter"):
                switch_statement_break_delimiter_node = ParseTreeNode("<switch-statement-break-delimiter>", omg_loop_node, self.current_token.line_number)
                omg_loop_node.add_child(switch_statement_break_delimiter_node)
                self.addParseTreeNode(switch_statement_break_delimiter_node)
                self.consume_current_token()

            if self.check_if_token_matches_expected_token_types("switch_statement_delimiter"):
                self.omg_loop(node_parent)
            elif self.check_if_token_matches_expected_token_types("alternative_switch_statement_delimiter"):
                default_loop_node = ParseTreeNode("<default-loop>", node_parent, self.current_token.line_number)
                node_parent.add_child(default_loop_node)

                alternative_switch_statement_delimiter_node = ParseTreeNode("<alternative-switch-statement-delimiter>", default_loop_node, self.current_token.line_number)
                default_loop_node.add_child(alternative_switch_statement_delimiter_node)
                self.addParseTreeNode(alternative_switch_statement_delimiter_node)
                self.consume_current_token()
                
                codeblock_statement_node = ParseTreeNode("<code-block-statement>", default_loop_node, self.current_token.line_number)
                default_loop_node.add_child(codeblock_statement_node)

                self.flow_control_codeblock(codeblock_statement_node)

                if self.check_if_token_matches_expected_token_types("switch_statement_break_delimiter"):
                    switch_statement_break_delimiter_node = ParseTreeNode("<switch-statement-break-delimiter>", default_loop_node, self.current_token.line_number)
                    default_loop_node.add_child(switch_statement_break_delimiter_node)
                    self.addParseTreeNode(switch_statement_break_delimiter_node)
                    self.consume_current_token()

    def loop_codeblock(self, node_parent):
        # Check if the current token is the print keyword
        if self.check_if_token_matches_expected_token_types("print_keyword"):
            self.print_statement(node_parent)

        # FOR IF-ELSE STATEMENTS
        # Check if the current token is the if keyword
        if self.check_if_token_matches_expected_token_types("opening_conditional_statement_delimiter"):
            self.if_then_statement(node_parent)

        # Check if the current token is the loop keyword
        if self.check_if_token_matches_expected_token_types("loop_keyword"):
            self.loop_statement(node_parent)

        # Check if the current token is an identifier for the assignment keyword/typecasting assignment keyword
        if self.check_if_token_matches_expected_token_types("identifiers"):
            self.assignment_statement(node_parent)

        # Check if the current token is a literal value
        if self.current_token.token_type in ["numbr_literal", "numbar_literal", "string_delimiter", "troof_literal"]:
            self.var_value(node_parent)

        # Check if the current token is the input keyword
        if self.check_if_token_matches_expected_token_types("input_keyword"):
            self.input_statement(node_parent)

        # Check if the current token is the switch keyword
        if self.check_if_token_matches_expected_token_types("opening_switch_statement_delimiter"):
            self.switch_statement(node_parent)

        # Check if the current token is the type casting keyword
        if self.check_if_token_matches_expected_token_types("type_casting_delimiter"):
            self.casting_statement(node_parent)

        # Check if the current token is one of the keywords under expressions
        if self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
            self.expression(node_parent)

        # Check if the current token is the break keyword for switch statements
        if not self.check_if_token_matches_expected_token_types("loop_exit_keyword") and not self.check_if_token_matches_expected_token_types("switch_statement_break_delimiter"):
            self.loop_codeblock(node_parent)
    
    def loop_statement(self, node_parent):
        loop_statement_node = ParseTreeNode("<loop-statement>", node_parent, self.current_token.line_number)
        node_parent.add_child(loop_statement_node)

        loop_delimiter_node = ParseTreeNode("<loop-opening-delimiter>", loop_statement_node, self.current_token.line_number)
        loop_statement_node.add_child(loop_delimiter_node)
        self.addParseTreeNode(loop_delimiter_node)
        self.consume_current_token()

        # Get label
        if self.check_if_token_matches_expected_token_types("identifiers"):
            label_node = ParseTreeNode("<loop-label>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(label_node)   # add the label node as a child of the parse tree node
            self.varident(label_node)   # add the varident node as a child of the label node
        else:
            # Error handling for missing label
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected label but got {self.current_token.token_type}")

        # Get the loop operator
        if self.check_if_token_matches_expected_token_types("loop_operator"):
            loop_operator_node = ParseTreeNode("<loop-operation>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(loop_operator_node)
            self.addParseTreeNode(loop_operator_node)
            self.consume_current_token()
        else:
            # Error handling for invalid loop operator
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected loop operator but got {self.current_token.token_type}")

        # Get YR
        if self.check_if_token_matches_expected_token_types("yr_keyword"):
            yr_operator_node = ParseTreeNode("<loop-yr-operator>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(yr_operator_node)
            self.addParseTreeNode(yr_operator_node)
            self.consume_current_token()
        else:
            # Error handling for invalid YR operator
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected YR operator but got {self.current_token.token_type}")

        # Get the variable
        if self.check_if_token_matches_expected_token_types("identifiers"):
            variable_value_node = ParseTreeNode("<variable-name>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(variable_value_node)
            
            self.varident(variable_value_node)

        else:
            # Error handling for invalid variable
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected variable but got {self.current_token.token_type}")

        # Get condition loop keyword
        if self.check_if_token_matches_expected_token_types("condition_loop_keyword"):
            condition_loop_keyword = ParseTreeNode("<loop-condition-keyword>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(condition_loop_keyword)
            self.addParseTreeNode(condition_loop_keyword)
            self.consume_current_token()
        else:
            # Error handling for invalid loop keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t condition loop keyword but got {self.current_token.token_type}")

        # Get the expression
        if self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
            loop_expression_node = ParseTreeNode("<loop-condition-expression>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(loop_expression_node)
            
            self.expression(loop_expression_node)

        else:
            # Error handling for invalid loop expression
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected loop expression but got {self.current_token.token_type}")

        # Get the code block
        codeblock_statement_node = ParseTreeNode("<code-block-statement>", loop_statement_node, self.current_token.line_number)
        loop_statement_node.add_child(codeblock_statement_node)

        self.loop_codeblock(codeblock_statement_node)
        
        # Check for optional GTFO keyword
        if self.check_if_token_matches_expected_token_types("switch_statement_break_delimiter"):
            loop_statement_break_delimiter_node = ParseTreeNode("<loop-statement-break-delimiter>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(loop_statement_break_delimiter_node)
            self.addParseTreeNode(loop_statement_break_delimiter_node)
            self.consume_current_token()

        # Get IM OUTTA YR
        if self.check_if_token_matches_expected_token_types("loop_exit_keyword"):
            loop_exit_node = ParseTreeNode("<loop-closing-delimiter>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(loop_exit_node)
            self.addParseTreeNode(loop_exit_node)
            self.consume_current_token()
        else:
            # Error handling for invalid loop exit keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected loop exit keyword but got {self.current_token.token_type}")
        
        # Get the loop label
        if self.check_if_token_matches_expected_token_types("identifiers"):
            loop_label_node = ParseTreeNode("<loop-label>", loop_statement_node, self.current_token.line_number)
            loop_statement_node.add_child(loop_label_node)

            self.varident(loop_label_node)
        else:
            # Error handling for invalid loop label
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected loop label but got {self.current_token.token_type}")

    # <switch> ::= WTF? <omg-loop> OIC
    def switch_statement(self, node_parent):
        switch_statement_node = ParseTreeNode("<switch>", node_parent, self.current_token.line_number)
        node_parent.add_child(switch_statement_node)

        switch_delimiter_node = ParseTreeNode("<switch-delimiter>", switch_statement_node, self.current_token.line_number)
        switch_statement_node.add_child(switch_delimiter_node)
        self.addParseTreeNode(switch_delimiter_node)
        self.consume_current_token()

        self.omg_loop(switch_delimiter_node)

        # Check if the current token is the OIC keyword
        if self.check_if_token_matches_expected_token_types("closing_conditional_statement_delimiter"):
            conditional_statement_end_delimiter = ParseTreeNode("<closing-conditional-statement-delimiter>", switch_statement_node, self.current_token.line_number)
            switch_statement_node.add_child(conditional_statement_end_delimiter)
            self.addParseTreeNode(conditional_statement_end_delimiter)
            self.consume_current_token()
        else:
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected switch statement end delimiter but got {self.current_token.token_type}")

    # <code-block> ::= <print> | <if-then> | <loop-opt> | <assignment> | <input> | <function-call> | <switch> | <casting> | <concat> | <expression> | <code-block>
    def codeblock(self, node_parent):
        # Check if the current token is the print keyword
        if self.check_if_token_matches_expected_token_types("print_keyword"):
            self.print_statement(node_parent)

        # FOR IF-ELSE STATEMENTS
        # Check if the current token is the if keyword
        if self.check_if_token_matches_expected_token_types("opening_conditional_statement_delimiter"):
            self.if_then_statement(node_parent)

        # Check if the current token is the loop keyword
        if self.check_if_token_matches_expected_token_types("loop_keyword"):
            self.loop_statement(node_parent)

        # Check if the current token is an identifier for the assignment keyword/typecasting assignment keyword
        if self.check_if_token_matches_expected_token_types("identifiers"):
            self.assignment_statement(node_parent)

        # Check if the current token is a literal value
        if self.current_token.token_type in ["numbr_literal", "numbar_literal", "string_delimiter", "troof_literal"]:
            self.var_value(node_parent)

        # Check if the current token is the input keyword
        if self.check_if_token_matches_expected_token_types("input_keyword"):
            self.input_statement(node_parent)

        # Check if the current token is the switch keyword
        if self.check_if_token_matches_expected_token_types("opening_switch_statement_delimiter"):
            self.switch_statement(node_parent)

        # Check if the current token is the type casting keyword
        if self.check_if_token_matches_expected_token_types("type_casting_delimiter"):
            self.casting_statement(node_parent)

        # Check if the current token is one of the keywords under expressions
        if self.current_token.token_type in ["arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
            self.expression(node_parent)

        # Check if the current token is still not the program end delimiter
        if not self.check_if_token_matches_expected_token_types("program_end_delimiter"):
            if self.current_token.token_type not in ["loop_keyword","opening_switch_statement_delimiter", "print_keyword", "opening_conditional_statement_delimiter", "identifiers", "numbr_literal", "numbar_literal", "string_delimiter", "troof_literal", "input_keyword", "type_casting_delimiter", "arithmetic_operator", "logical_operator", "comparison_operator", "concatenation_operator"]:
                # Error handling for invalid code block
                raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected code block but got {self.current_token.token_type}")

            self.codeblock(node_parent)

    # <program> ::= <function> HAI <variable-declaration> <code-block> KTHXBYE <function>
    def program(self):
        # Check if the current token is the HAI keyword
        if self.check_if_token_matches_expected_token_types("program_start_delimiter"):
            start_delimiter_node = ParseTreeNode("<program-start-delimiter>", self.parse_tree, self.current_token.line_number)
            self.parse_tree.add_child(start_delimiter_node)
            self.addParseTreeNode(start_delimiter_node) # Add the HAI node as a child of the root node
            self.consume_current_token() # Update the current token to the next token
        else:
            # Error handling for missing HAI keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected program start delimiter but got {self.current_token.token_type}")

        # Check if the current token is the variable declaration start delimiter
        if self.check_if_token_matches_expected_token_types("variable_declaration_start_delimiter"):
            self.currently_inside_variable_declaration_section = True

            variable_declaration_node = ParseTreeNode("<variable-declaration>", self.parse_tree, self.current_token.line_number)
            self.parse_tree.add_child(variable_declaration_node)
            self.variable_declaration(variable_declaration_node) # Call the variable declaration grammar rule

        # Check if the current token is already the statement start delimiter
        if not self.check_if_token_matches_expected_token_types("variable_declaration_start_delimiter"):
            codeblock_node = ParseTreeNode("<code-block>", self.parse_tree, self.current_token.line_number)
            self.parse_tree.add_child(codeblock_node)
            self.codeblock(codeblock_node)

        # Check if the current token is the KTHXBYE keyword
        if self.check_if_token_matches_expected_token_types("program_end_delimiter"):
            end_delimiter_node = ParseTreeNode("<program-end-delimiter>", self.parse_tree, self.current_token.line_number)
            self.parse_tree.add_child(end_delimiter_node)
            self.addParseTreeNode(end_delimiter_node)
            self.consume_current_token() # Update the current token to the next token
        else:
            # Error handling for missing KTHXBYE keyword
            raise Exception(f"Syntax Error: Line {self.current_token.line_number + 1}\n\t Expected program end delimiter but got {self.current_token.token_type}")
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

            # Remove all linebreaks that are next to a
            if token.token_type in ["opening_multi-line_comment_delimiter", "closing_multi-line_comment_delimiter"]:
                if self.symbol_table[index + 1].token_type == "linebreak_delimiter":
                    self.symbol_table.pop(index + 1)

        # Update the symbol table
        self.symbol_table = symbol_table_without_comments    
    # ==========================================================================================