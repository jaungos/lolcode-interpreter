"""

    This file is used to define the semantic analyzer for the lolcode language.
    TODO: add brief description of what an interpreter does in this lolcode compiler
"""

from Classes.lol_symbol_table import Lol_Symbol_Table
from Classes.lol_symbol import SymbolEntity

suppress_newline_print = False

class SemanticAnalyzer:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.final_symbol_table = Lol_Symbol_Table()

    def run_semantic_analyzer(self):
        self.evaluate()

    def print_symbol_table(self):
        self.final_symbol_table.get_symbols()
        print("Symbol Table:")
        for symbol in self.final_symbol_table.symbols:
            print(f'\t{symbol}: {self.final_symbol_table.symbols[symbol].symbolClassification} - {self.final_symbol_table.symbols[symbol].symbolValue}')
    
    def type_cast_to_numbr_or_numbar(self, symbol : SymbolEntity):
        # Returns a SymbolEntity with the same symbolClassification but with a symbolValue of type NUMBR or NUMBAR
        if symbol.symbolClassification == "TROOF":
            if symbol.symbolValue == "WIN":
                return SymbolEntity("NUMBR", 1)
            else:
                return SymbolEntity("NUMBR", 0)
        else:
            try:
                if '.' in str(symbol.symbolValue):
                    return SymbolEntity("NUMBAR", float(symbol.symbolValue))
                else:
                    return SymbolEntity("NUMBR", int(symbol.symbolValue))
            except:
                raise Exception(f"Cannot cast {symbol.symbolValue} to NUMBR or NUMBAR")
        
    def evaluate(self):
        # Add the IT in the symbol table
        self.final_symbol_table.add_symbol("IT", SymbolEntity("NOOB", None))

        # Evaluate the parse tree
        for node in self.parse_tree.children:
            # TODO: Remove this for debugging purposes ONLY
            print(f'Current node: {node.value}')
            
            # TODO: add function before HAI and after KTHXBYE and make it the if for this control flow statement
            if node.value == "<program-start-delimiter>":
                if node.children[0].value == "HAI" and len(node.children) == 1:
                    continue
            elif node.value == "<variable-declaration>":
                self.evaluate_variable_declaration(node)
            elif node.value == "<code-block>":
                self.evaluate_code_block(node)
            elif node.value == "<program-end-delimiter>":
                if node.children[0].value == "KTHXBYE" and len(node.children) == 1:
                    continue
            else:
                raise Exception(f"Syntax Error: Line {node.line_number + 1}\n")
        
        # TODO: remove this for debugging purposes ONLY
        print(f'Finished evaluating the parse tree\n')

    def evaluate_literal_value(self, literal_value):
        if literal_value.value == "<yarn-literal>":
            return SymbolEntity("YARN", literal_value.children[0].value)
        elif literal_value.value == "<numbr-literal>":
            return SymbolEntity("NUMBR", int(literal_value.children[0].value))
        elif literal_value.value == "<numbar-literal>":
            return SymbolEntity("NUMBAR", float(literal_value.children[0].value))
        elif literal_value.value == "<troof-literal>":
            if literal_value.children[0].value == "WIN":
                return SymbolEntity("TROOF", "WIN")
            else:
                return SymbolEntity("TROOF", "FAIL")
            
    def evaluate_another_variable_value(self, variable_value):
        if not self.final_symbol_table.check_if_symbol_exists(variable_value.value):
            raise Exception(f"Variable {variable_value.value} has not been declared")
        else:
            return self.final_symbol_table.get_symbol(variable_value.value)
        
    def evaluate_arithmetic_expression(self, arithmetic_expression):
        # TODO: remove this for debugging purposes ONLY
        print(f'The number of children: {len(arithmetic_expression.children[1].children)}')
        for child in arithmetic_expression.children[1].children:
            print(f'\t\t\t\t{child.value}')

        # Get the two operands before performing the respective prefix arithmetic operation
        operand1 = self.evaluate_var_value(arithmetic_expression.children[1].children[0])
        operand2 = self.evaluate_var_value(arithmetic_expression.children[1].children[2])

        # TODO: remove this for debugging purposes ONLY
        print(f'\t\t\t\tOperand 1: {operand1.symbolValue} - {operand1.symbolClassification} | Operand 2: {operand2.symbolValue} - {operand2.symbolClassification}')

        # Typecast the operands to NUMBR or NUMBAR if they are not and it is possible
        if operand1.symbolClassification != "NUMBR" and operand1.symbolClassification != "NUMBAR":
            operand1 = self.type_cast_to_numbr_or_numbar(operand1)
        if operand2.symbolClassification != "NUMBR" and operand2.symbolClassification != "NUMBAR":
            operand2 = self.type_cast_to_numbr_or_numbar(operand2)

        if arithmetic_expression.value == "<addition-operator>":
            symbol_value = operand1.symbolValue + operand2.symbolValue

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)
            
        #     # return self.evaluate_addition_expression(arithmetic_expression.children[0])
        # elif arithmetic_expression.value == "<subtraction-operator>":
        #     pass
        #     # return self.evaluate_subtraction_expression(arithmetic_expression.children[0])
        # elif arithmetic_expression.value == "<multiplication-operator>":
        #     pass
        #     # return self.evaluate_multiplication_expression(arithmetic_expression.children[0])
        # elif arithmetic_expression.value == "<division-operator>":
        #     pass
        #     # return self.evaluate_division_expression(arithmetic_expression.children[0])
        # elif arithmetic_expression.value == "<modulo-operator>":
        #     pass
        #     # return self.evaluate_modulo_expression(arithmetic_expression.children[0])
        # elif arithmetic_expression.value == "<max-operator>":
        #     pass
        #     # return self.evaluate_max_expression(arithmetic_expression.children[0])
        # elif arithmetic_expression.value == "<min-operator>":
        #     pass
        #     # return self.evaluate_min_expression(arithmetic_expression.children[0])

    def evaluate_expression_value(self, expression_value):
        if expression_value.value == "<arithmetic-expression>":
            print(f'\t\t\t\tArith: {expression_value.children[0].value}')
            return self.evaluate_arithmetic_expression(expression_value.children[0])
        elif expression_value.value == "<boolean-expression>":
            print(f'\t\t\t\tBoolean: {expression_value.children[0].value}')
        elif expression_value.value == "<comparison-expression>":
            print(f'\t\t\t\tComparison: {expression_value.children[0].value}')
        elif expression_value.value == "<concatenation-expression>":
            print(f'\t\t\t\tConcat: {expression_value.children[0].value}')

        return SymbolEntity("YARN", "TEST")

    def evaluate_var_value_type(self, variable_type):
        print(f'\t\t{variable_type.value}')
        
        if variable_type.value == "<literal-value>":
            return self.evaluate_literal_value(variable_type.children[0])
        elif variable_type.value == "<variable-value>":
            return self.evaluate_another_variable_value(variable_type.children[0])
        elif variable_type.value == "<expression-value>":
            print(f'\t\t\tNext child: {variable_type.children[0].value}')
            return self.evaluate_expression_value(variable_type.children[0])

        # return SymbolEntity("YARN", "TEST")
    
    def evaluate_var_value(self, variable_value):
        print(f'\tCurrent node: {variable_value.value}')
        if variable_value.value == "<var-value>":
            return self.evaluate_var_value_type(variable_value.children[0]) # Pass the <literal-value> | <variable-value> | <expression-value> node

    def evaluate_var(self, variable_declaration_block):
        symbol_value = SymbolEntity("NOOB", None) # Initialize a new SymbolEntity

        for variable_information in variable_declaration_block.children:
            print(f'Current node: {variable_information.value}')
            if variable_information.value == "<identifier>":
                symbol_identifier = variable_information.children[0].value
                
                # Check if the variable is already declared
                if self.final_symbol_table.check_if_symbol_exists(symbol_identifier):
                    raise Exception(f"Variable {symbol_identifier} has already been declared")

            elif variable_information.value == "<var-initialization>":
                symbol_value = self.evaluate_var_value(variable_information.children[1]) # Pass the <var-value> node
            
        self.final_symbol_table.add_symbol(symbol_identifier, symbol_value)

    def evaluate_variable_declaration(self, variable_declaration_section):
        for variable_declaration_node in variable_declaration_section.children:
            print(f'{variable_declaration_node.value}')
            if variable_declaration_node.value == "<variable-declaration-start-delimiter>" or variable_declaration_node.value == "<variable-declaration-end-delimiter>":
                continue
            elif variable_declaration_node.value == "<var>":
                self.evaluate_var(variable_declaration_node) # Pass the <var> node
            else:
                # TODO: improve error prompting
                raise Exception(f"Syntax error: Line {variable_declaration_node.line_number}\n")

    def evaluate_print_loop(self, print_loop):
        string_to_print = ""

        for print_information in print_loop.children:
            if print_information.value == "<var-value>":
                string_value = self.evaluate_print_var_value(print_information.children[0])
                string_to_print = ''.join([string_to_print, string_value])
            elif print_information.value == "+":
                string_to_print = ''.join([string_to_print, self.evaluate_print_loop(print_information.children[0])])

        return string_to_print

    def evaluate_print_var_value(self, variable_value):
        return str(variable_value.children[0].children[0].value)

    def evaluate_print(self, print_statement):
        global suppress_newline_print
        for print_information in print_statement.children:
            # Checks if there is a suppress new line delimiter at the end
            if print_statement.children[len(print_statement.children) - 1].value == "!":
                suppress_newline_print = True

            if print_information.value == "<print-loop>":
                string_to_print = self.evaluate_print_loop(print_information)
            
        if suppress_newline_print:
            print(f'Resulting String: {string_to_print}', end='')
            suppress_newline_print = False
        else:
            print(f'Resulting String: {string_to_print}')

    def evaluate_input(self, input_statement):
        # Get input from the user
        user_input = input()

        for input_information in input_statement.children:
            if input_information.value == "<varident>":
                symbolName = input_information.children[0].value
                if not self.final_symbol_table.check_if_symbol_exists(symbolName):
                    raise Exception(f"Variable {symbolName} does not exist")
                
        self.final_symbol_table.update_symbol(symbolName, SymbolEntity("YARN", user_input))

    def evaluate_assignment(self, assignment_statement):
        for assignment_information in assignment_statement.children:
            if assignment_information.value == "<varident>":
                symbolName = assignment_information.children[0].value
                if not self.final_symbol_table.check_if_symbol_exists(symbolName):
                    raise Exception(f"Variable {symbolName} does not exist")
            elif assignment_information.value == "<var-value>":
                symbolValue = self.evaluate_var_value_type(assignment_information.children[0])
                
        self.final_symbol_table.update_symbol(symbolName, symbolValue)

    def evaluate_data_type(self, data_type):
        if data_type.value == "<integer-data-type>":
            return "NUMBR"
        elif data_type.value == "<float-data-type>":
            return "NUMBAR"
        elif data_type.value == "<string-data-type>":
            return "YARN"
        elif data_type.value == "<boolean-data-type>":
            return "TROOF"
        elif data_type.value == "<null-data-type>":
            return "NOOB"

    def evaluate_casting(self, casting_statement):
        for casting_information in casting_statement.children:
            if casting_information.value == "<varident>":
                symbolName = casting_information.children[0].value
                if not self.final_symbol_table.check_if_symbol_exists(symbolName):
                    raise Exception(f"Variable {symbolName} does not exist")
            elif casting_information.value == "<valid-data-type>":
                # Get the current symbol value
                oldSymbolValue = self.final_symbol_table.get_symbol(symbolName)
                # Get the new symbol classification
                newSymbolClassification = self.evaluate_data_type(casting_information.children[0])
                print(newSymbolClassification)

                if newSymbolClassification == "NUMBR":
                    if oldSymbolValue.symbolClassification == "TROOF":
                        if oldSymbolValue.symbolValue == "WIN":
                            newSymbolValue = 1
                        else:
                            newSymbolValue = 0
                    else:
                        try:
                            newSymbolValue = int(oldSymbolValue.symbolValue)
                        except:
                            raise Exception(f"Cannot cast {oldSymbolValue.symbolValue} to NUMBR")
                elif newSymbolClassification == "NUMBAR":
                    if oldSymbolValue.symbolClassification == "TROOF":
                        if oldSymbolValue.symbolValue == "WIN":
                            newSymbolValue = 1.0
                        else:
                            newSymbolValue = 0.0
                    else:
                        try:
                            newSymbolValue = float(oldSymbolValue.symbolValue)
                        except:
                            raise Exception(f"Cannot cast {oldSymbolValue.symbolValue} to NUMBAR")
                elif newSymbolClassification == "YARN":
                    newSymbolValue = str(oldSymbolValue.symbolValue)
                elif newSymbolClassification == "TROOF":
                    if oldSymbolValue.symbolClassification == "NOOB":
                        newSymbolValue = "FAIL"
                    else:
                        if oldSymbolValue.symbolClassification == "NUMBR" or oldSymbolValue.symbolClassification == "NUMBAR":
                            if oldSymbolValue.symbolValue == 0:
                                newSymbolValue = "FAIL"
                        newSymbolValue = "WIN"
                elif newSymbolClassification == "NOOB":
                    newSymbolValue = None
                else:
                    raise Exception(f"Invalid data type {newSymbolClassification}")
                
        self.final_symbol_table.update_symbol(symbolName, SymbolEntity(newSymbolClassification, newSymbolValue))

    def evaluate_code_block(self, code_block):
        for statement in code_block.children:
            print(f'\n\t{statement.value}\n')
            # TODO: complete all the possible statements
            if statement.value == "<print>":
                self.evaluate_print(statement)
            elif statement.value == "<input>":
                self.evaluate_input(statement)
            elif statement.value == "<assignment>":
                self.evaluate_assignment(statement)
            elif statement.value == "<casting>":
                self.evaluate_casting(statement)