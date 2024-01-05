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
        
    def evaluate(self):
        # Add the IT in the symbol table
        self.final_symbol_table.add_symbol("IT", SymbolEntity("NOOB", None))

        # Evaluate the parse tree
        for node in self.parse_tree.children:
            # TODO: Remove this for debugging purposes ONLY
            print(f'Current node: {node.value}')
            
            # TODO: add function before HAI and after KTHXBYE and make it the if for this control flow statement
            if node.value == "<program-start-delimiter>":
                print(f'Program start delimiter: {node.children[0].value} at line {node.children[0].line_number + 1}')
                if node.children[0].value == "HAI" and len(node.children) == 1:
                    continue
            elif node.value == "<variable-declaration>":
                self.evaluate_variable_declaration(node)
            elif node.value == "<code-block>":
                self.evaluate_code_block(node)
            elif node.value == "KTHXBYE":
                continue
            else:
                raise Exception(f"Invalid syntax {node.value}")
        
        # TODO: remove this for debugging purposes ONLY
        print(f'Finished evaluating the parse tree\n')

    def evaluate_var(self, variableDeclared):
        symbolValue = SymbolEntity("NOOB", None) # Initialize a new SymbolEntity

        for variable_information in variableDeclared.children:
            if variable_information.value == "<varident>":
                symbolName = variable_information.children[0].value
                
                # Check if the variable is already declared
                if self.final_symbol_table.check_if_symbol_exists(symbolName):
                    raise Exception(f"Variable {symbolName} already declared")

            elif variable_information.value == "<var-initialization>":
                symbolValue = self.evaluate_var_value(variable_information) # Pass the <var-initialization> node
            
        self.final_symbol_table.add_symbol(symbolName, symbolValue)
    
    def evaluate_var_value(self, variable_value):
        for value in variable_value.children:
            if value.value == "<var-value>":
                return self.evaluate_var_value_type(value.children[0]) # Pass the <literal-value> node

    def evaluate_var_value_type(self, variable_type):
        variable_classification = variable_type.children[0].value
        if variable_classification == "<yarn-literal>":
            variable_classification = "YARN"
        elif variable_classification == "<numbr-literal>":
            variable_classification = "NUMBR"
        elif variable_classification == "<numbar-literal>":
            variable_classification = "NUMBAR"
        elif variable_classification == "<troof-literal>":
            variable_classification = "TROOF"
            
        variable_value = variable_type.children[0].children[0].value

        return SymbolEntity(variable_classification, variable_value)

    def evaluate_variable_declaration(self, variable_declarations):
        for variable_declared in variable_declarations.children:
            if variable_declared.value == "<var>":
                self.evaluate_var(variable_declared) # Pass the <var> node

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