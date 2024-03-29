"""

    This file is used to define and implement the semantic analyzer of the interpreter for the LOLCode language.
    Evaluates the passed parse tree and checks for semantic errors.
"""

from Classes.lol_symbol_table import Lol_Symbol_Table
from Classes.lol_symbol import SymbolEntity

class SemanticAnalyzer:
    def __init__(self, parse_tree, input_callback):
        self.parse_tree = parse_tree
        self.final_symbol_table = Lol_Symbol_Table()
        self.input_callback = input_callback
        self.suppress_newline_print = False
        self.print_statements = []

    def run_semantic_analyzer(self):
        self.evaluate()

    def print_symbol_table(self):
        self.final_symbol_table.get_symbols()
        symbol_table = []
        for symbol in self.final_symbol_table.symbols:
            symbol_table.append((symbol, self.final_symbol_table.symbols[symbol].symbolValue))
        return symbol_table

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
                raise Exception(f"Error in line {symbol.line_number + 1}: Cannot cast {symbol.symbolValue} to NUMBR or NUMBAR")

    def type_cast_to_troof(self, symbol : SymbolEntity):
        # Returns a SymbolEntity with the same symbolClassification but with a symbolValue of type TROOF
        if symbol.symbolClassification == "NUMBR" or symbol.symbolClassification == "NUMBAR":
            if symbol.symbolValue == 0 or symbol.symbolValue == 0.0:
                return SymbolEntity("TROOF", "FAIL")
            else:
                return SymbolEntity("TROOF", "WIN")
        elif symbol.symbolClassification == "YARN":
            if symbol.symbolValue == "":
                return SymbolEntity("TROOF", "FAIL")
            else:
                return SymbolEntity("TROOF", "WIN")
        else:
            raise Exception(f"Error in line {symbol.line_number + 1}: Cannot cast {symbol.symbolValue} to TROOF")

    def troof_to_boolean(self, symbol : SymbolEntity):
        # Returns a boolean value of the symbolValue
        if symbol.symbolValue == "WIN":
            return True
        else:
            return False

    def evaluate(self):
        # Add the IT in the symbol table
        self.final_symbol_table.add_symbol("IT", SymbolEntity("NOOB", "NOOB"))

        # Evaluate the parse tree
        for node in self.parse_tree.children:
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
                raise Exception(f"Error in line {node.line_number + 1}: Expected variable declaration or code block but got {node.value}\n")

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
        elif literal_value.value == "<noob-literal>":
            return SymbolEntity("NOOB", "NOOB")

    def evaluate_another_variable_value(self, variable_value):
        if not self.final_symbol_table.check_if_symbol_exists(variable_value.value):
            raise Exception(f"Error in line {variable_value.line_number + 1}: Variable {variable_value.value} has not been declared")
        else:
            return self.final_symbol_table.get_symbol(variable_value.value)

    def evaluate_arithmetic_expression(self, arithmetic_expression):
        # Get the two operands before performing the respective prefix arithmetic operation
        operand1 = self.evaluate_var_value(arithmetic_expression.children[1].children[0])
        operand2 = self.evaluate_var_value(arithmetic_expression.children[1].children[2])

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
        elif arithmetic_expression.value == "<subtraction-operator>":
            symbol_value = operand1.symbolValue - operand2.symbolValue

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)
        elif arithmetic_expression.value == "<multiplication-operator>":
            symbol_value = operand1.symbolValue * operand2.symbolValue

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)
        elif arithmetic_expression.value == "<division-operator>":
            symbol_value = operand1.symbolValue / operand2.symbolValue

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)
        elif arithmetic_expression.value == "<modulo-operator>":
            symbol_value = operand1.symbolValue % operand2.symbolValue

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)
        elif arithmetic_expression.value == "<max-operator>":
            symbol_value = max(operand1.symbolValue, operand2.symbolValue)

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)
        elif arithmetic_expression.value == "<min-operator>":
            symbol_value = min(operand1.symbolValue, operand2.symbolValue)

            if type(symbol_value) == int:
                return SymbolEntity("NUMBR", symbol_value)
            else:
                return SymbolEntity("NUMBAR", symbol_value)

    def evaluate_boolean_operand(self, boolean_operand):
        if boolean_operand.value == "<not-operator>":
            operand = self.evaluate_var_value(boolean_operand.children[1])
        else:
            operand = self.evaluate_var_value(boolean_operand)

        # Typecast operand to TROOF if it is not
        if operand.symbolClassification != "TROOF":
            operand = self.type_cast_to_troof(operand)

        if boolean_operand.value == "<not-operator>":
            if self.troof_to_boolean(operand):
                return SymbolEntity("TROOF", "FAIL")
            else:
                return SymbolEntity("TROOF", "WIN")
        else:
            return operand

    def evaluate_boolean_operations(self, boolean_expression):
        if boolean_expression.value == "<boolean-value-operands>":
            return self.evaluate_boolean_operand(boolean_expression.children[0])

        operand1 = self.evaluate_boolean_operand(boolean_expression.children[1].children[0])
        operand2 = self.evaluate_boolean_operand(boolean_expression.children[1].children[2])

        if boolean_expression.value == "<and-operator>":
            if self.troof_to_boolean(operand1) and self.troof_to_boolean(operand2):
                return SymbolEntity("TROOF", "WIN")
            else:
                return SymbolEntity("TROOF", "FAIL")
        elif boolean_expression.value == "<or-operator>":
            if self.troof_to_boolean(operand1) or self.troof_to_boolean(operand2):
                return SymbolEntity("TROOF", "WIN")
            else:
                return SymbolEntity("TROOF", "FAIL")
        elif boolean_expression.value == "<xor-operator>":
            if self.troof_to_boolean(operand1) and self.troof_to_boolean(operand2) == False:
                return SymbolEntity("TROOF", "WIN")
            elif self.troof_to_boolean(operand1) == False and self.troof_to_boolean(operand2):
                return SymbolEntity("TROOF", "WIN")
            else:
                return SymbolEntity("TROOF", "FAIL")

    def evaluate_boolean_expression(self, boolean_expression):
        if boolean_expression.value == "<infinite-arity-and-operator>":
            boolean_value = True

            for boolean_information in boolean_expression.children:
                if boolean_information.value == "<boolean-operations>":
                    boolean_value = boolean_value and self.troof_to_boolean(self.evaluate_boolean_operations(boolean_information.children[0]))
                    
            return SymbolEntity("TROOF", "WIN" if boolean_value else "FAIL")
        elif boolean_expression.value == "<infinite-arity-or-operator>":
            boolean_value = False

            for boolean_information in boolean_expression.children:
                if boolean_information.value == "<boolean-operations>":
                    boolean_value = boolean_value or self.troof_to_boolean(self.evaluate_boolean_operations(boolean_information.children[0]))
                    
            return SymbolEntity("TROOF", "WIN" if boolean_value else "FAIL")
        else:
            return self.evaluate_boolean_operations(boolean_expression.children[0])
        
    def evaluate_comparison_expression(self, comparison_expression):
        operand1 = self.evaluate_var_value(comparison_expression.children[1].children[0])
        operand2 = self.evaluate_var_value(comparison_expression.children[1].children[2])

        if operand1.symbolClassification == "NUMBAR" or operand2.symbolClassification == "NUMBAR":
            operand1 = self.type_cast_to_numbr_or_numbar(operand1)
            operand2 = self.type_cast_to_numbr_or_numbar(operand2)

        # If numbr/numbar compared to yarn/troof/noob and vice versa, it should always be false
        if operand1.symbolClassification == "NUMBR" or operand1.symbolClassification == "NUMBAR":
            if operand2.symbolClassification == "YARN" or operand2.symbolClassification == "TROOF" or operand2.symbolClassification == "NOOB":
                return SymbolEntity("TROOF", "FAIL")
        elif operand2.symbolClassification == "NUMBR" or operand2.symbolClassification == "NUMBAR":
            if operand1.symbolClassification == "YARN" or operand1.symbolClassification == "TROOF" or operand1.symbolClassification == "NOOB":
                return SymbolEntity("TROOF", "FAIL")
            
        if comparison_expression.value == "<equal-operator>":
            if operand1.symbolValue == operand2.symbolValue:
                return SymbolEntity("TROOF", "WIN")
            else:
                return SymbolEntity("TROOF", "FAIL")
        elif comparison_expression.value == "<not-equal-operator>":
            if operand1.symbolValue != operand2.symbolValue:
                return SymbolEntity("TROOF", "WIN")
            else:
                return SymbolEntity("TROOF", "FAIL")

    def evaluate_concatenation_expression(self, concatenation_expression):
        concatenated_string = ""

        for concatenation_information in concatenation_expression.children:
            if concatenation_information.value == "<var-value>":
                concatenated_string = ''.join([concatenated_string, str(self.evaluate_var_value(concatenation_information).symbolValue)])
            elif concatenation_information.value == "<concat-loop>":
                concatenated_string = ''.join([concatenated_string, str(self.evaluate_concatenation_expression(concatenation_information).symbolValue)])

        return SymbolEntity("YARN", concatenated_string)

    def evaluate_expression_value(self, expression_value):
        result = None

        if expression_value.value == "<arithmetic-expression>":
            result = self.evaluate_arithmetic_expression(expression_value.children[0])
        elif expression_value.value == "<boolean-expression>":
            result = self.evaluate_boolean_expression(expression_value.children[0])
        elif expression_value.value == "<comparison-expression>":
            result = self.evaluate_comparison_expression(expression_value.children[0])
        elif expression_value.value == "<concatenation-expression>":
            result = self.evaluate_concatenation_expression(expression_value.children[1])

        if result is None:
            raise Exception(f"Error in line {expression_value.line_number + 1}: Expected arithmetic, boolean, comparison, or concatenation expression but got {expression_value.value}\n")
        
        # Update the IT
        self.final_symbol_table.update_symbol("IT", result)
        
        return result

    def evaluate_var_value_type(self, variable_type):
        if variable_type.value == "<literal-value>":
            literal_result = self.evaluate_literal_value(variable_type.children[0])
            self.final_symbol_table.update_symbol("IT", literal_result) # Update the IT
            return literal_result
        elif variable_type.value == "<variable-value>":
            variable_result = self.evaluate_another_variable_value(variable_type.children[0])
            self.final_symbol_table.update_symbol("IT", variable_result) # Update the IT
            return variable_result
        elif variable_type.value == "<expression-value>":
            expression_result = self.evaluate_expression_value(variable_type.children[0])
            self.final_symbol_table.update_symbol("IT", expression_result) # Update the IT
            return expression_result

    def evaluate_var_value(self, variable_value):
        return self.evaluate_var_value_type(variable_value.children[0]) # Pass the <literal-value> | <variable-value> | <expression-value> node

    def evaluate_var(self, variable_declaration_block):
        symbol_identifier = None
        symbol_value = SymbolEntity("NOOB", "NOOB") # Initialize a new SymbolEntity

        for variable_information in variable_declaration_block.children:
            if variable_information.value == "<identifier>":
                symbol_identifier = variable_information.children[0].value
                
                # Check if the variable is already declared
                if self.final_symbol_table.check_if_symbol_exists(symbol_identifier):
                    raise Exception(f"Error in line {variable_information.line_number + 1}: Variable {symbol_identifier} has already been declared")

            elif variable_information.value == "<var-initialization>":
                symbol_value = self.evaluate_var_value(variable_information.children[1]) # Pass the <var-value> node
            
        if symbol_identifier is None:
            symbol_identifier = "IT"
            
        self.final_symbol_table.add_symbol(symbol_identifier, symbol_value)

    def evaluate_variable_declaration(self, variable_declaration_section):
        for variable_declaration_node in variable_declaration_section.children:
            if variable_declaration_node.value == "<variable-declaration-start-delimiter>" or variable_declaration_node.value == "<variable-declaration-end-delimiter>":
                continue
            elif variable_declaration_node.value == "<var>":
                self.evaluate_var(variable_declaration_node) # Pass the <var> node
            else:
                raise Exception(f"Error in line {variable_declaration_node.line_number + 1}: Expected variable but got {variable_declaration_node.value}\n")

    def evaluate_print_loop(self, print_loop):
        string_to_print = ""

        for print_information in print_loop.children:
            if print_information.value == "<var-value>":
                string_to_print = ''.join([string_to_print, str(self.evaluate_var_value(print_information).symbolValue)])
            elif print_information.value == "<print-loop>":
                string_to_print = ''.join([string_to_print, str(self.evaluate_print_loop(print_information).symbolValue)])

        return SymbolEntity("YARN", string_to_print)
    
    # Function for getting print statements
    def get_print_statements(self):
        return self.print_statements

    def evaluate_print(self, print_statement):
        string_symbol_entity = None
        for print_information in print_statement.children:
            if print_information.value == "<suppress-newline-delimiter>":
                self.suppress_newline_print = True
            elif print_information.value == "<print-loop>":
                string_symbol_entity = self.evaluate_print_loop(print_information)

        if string_symbol_entity is None:
            raise Exception(f"Error in line {print_statement.line_number + 1}: Expected <print-loop> but got {print_statement.children[1].value}")
    
        
        if self.suppress_newline_print:
            self.suppress_newline_print = False
            to_print = (string_symbol_entity.symbolValue) 
        else:

            to_print = (string_symbol_entity.symbolValue + '\n')

        # Update the IT
        self.final_symbol_table.update_symbol("IT", string_symbol_entity)
        
        # Append to print statements
        self.print_statements.append(to_print)

        return to_print
    
    def trigger_callback(self, symbol_name):
        user_input = self.input_callback(symbol_name)
        return user_input

    def evaluate_input(self, input_statement):
        user_input = None
        for input_information in input_statement.children:
            if input_information.value == "<input-operator>":
                pass
            elif input_information.value == "<identifier>":
                symbol_name = input_information.children[0].value
                if not self.final_symbol_table.check_if_symbol_exists(symbol_name):
                    raise Exception(f"Error in line {input_statement.line_number + 1}: Variable {symbol_name} has not been declared")
                # Pass the symbol name to the callback function
                user_input = self.trigger_callback(symbol_name)
        self.final_symbol_table.update_symbol(symbol_name, SymbolEntity("YARN", user_input))

    def evaluate_assignment(self, assignment_statement):
        symbol_name = None
        symbol_value = None

        for assignment_information in assignment_statement.children:
            if assignment_information.value == "<identifier>":
                symbol_name = assignment_information.children[0].value
                
                if not self.final_symbol_table.check_if_symbol_exists(symbol_name):
                    raise Exception(f"Error in line {assignment_statement.line_number + 1}: Variable {symbol_name} does not exist")

                symbol_value = self.final_symbol_table.get_symbol(symbol_name)
                
                self.final_symbol_table.update_symbol("IT", symbol_value) # Update the IT
            elif assignment_information.value == "<var-value>":
                symbol_value = self.evaluate_var_value(assignment_information)
            elif assignment_information.value == "<type-casting-assignment-operator>":
                symbol_value = self.evaluate_casting(self.final_symbol_table.get_symbol(symbol_name), self.evaluate_data_type(assignment_information.children[1]))
            elif assignment_information.value == "<casting>":
                # Check if the keyword A is present
                if assignment_information.children[2].value == "<type-casting-reassignment-operator>":
                    symbol_value = self.evaluate_casting(self.evaluate_var_value(assignment_information.children[1]), self.evaluate_data_type(assignment_information.children[3]))
                else:
                    symbol_value = self.evaluate_casting(self.evaluate_var_value(assignment_information.children[1]), self.evaluate_data_type(assignment_information.children[2]))

        if symbol_name is None or symbol_value is None:
            raise Exception(f"Error in line {assignment_statement.line_number + 1}: Expected <identifier> or <var-value> but got {assignment_statement.children[1].value}")

        self.final_symbol_table.update_symbol(symbol_name, symbol_value)

    def evaluate_data_type(self, data_type):
        return data_type.children[0].children[0].value

    def evaluate_casting(self, symbol_to_cast, new_data_type):
        if new_data_type == "NUMBR":
            if symbol_to_cast.symbolClassification == "TROOF":
                if symbol_to_cast.symbolValue == "WIN":
                    return SymbolEntity("NUMBR", 1)
                else:
                    return SymbolEntity("NUMBR", 0)
            elif symbol_to_cast.symbolClassification == "NOOB":
                return SymbolEntity("NUMBR", 0)
            else:
                try:
                    return SymbolEntity("NUMBR", int(symbol_to_cast.symbolValue))
                except:
                    raise Exception(f"Error in line {symbol_to_cast.line_number + 1}: Cannot cast {symbol_to_cast.symbolValue} to NUMBR")
        elif new_data_type == "NUMBAR":
            if symbol_to_cast.symbolClassification == "TROOF":
                if symbol_to_cast.symbolValue == "WIN":
                    return SymbolEntity("NUMBAR", 1.0)
                else:
                    return SymbolEntity("NUMBAR", 0.0)
            elif symbol_to_cast.symbolClassification == "NOOB":
                return SymbolEntity("NUMBAR", 0.0)
            else:
                try:
                    return SymbolEntity("NUMBAR", float(symbol_to_cast.symbolValue))
                except:
                    raise Exception(f"Error in line {symbol_to_cast.line_number + 1}: Cannot cast {symbol_to_cast.symbolValue} to NUMBAR")
        elif new_data_type == "YARN":
            if symbol_to_cast.symbolClassification == "NOOB":
                return SymbolEntity("YARN", "")
            
            if symbol_to_cast.symbolClassification == "NUMBAR":
                return SymbolEntity("YARN", f'{symbol_to_cast.symbolValue:.2f}') # Truncate up to 2 decimal places
            return SymbolEntity("YARN", str(symbol_to_cast.symbolValue))
        elif new_data_type == "TROOF":
            if symbol_to_cast.symbolClassification == "NOOB":
                return SymbolEntity("TROOF", "FAIL")

            if symbol_to_cast.symbolClassification == "NUMBR" and symbol_to_cast.symbolValue == 0:
                return SymbolEntity("TROOF", "FAIL")

            if symbol_to_cast.symbolClassification == "NUMBAR" and symbol_to_cast.symbolValue == 0.0:
                return SymbolEntity("TROOF", "FAIL")

            if symbol_to_cast.symbolClassification == "YARN" and symbol_to_cast.symbolValue == "":
                return SymbolEntity("TROOF", "FAIL")

            return SymbolEntity("TROOF", "WIN")
        elif new_data_type == "NOOB":
            return SymbolEntity("NOOB", "NOOB")
        else:
            raise Exception(f"Error in line {symbol_to_cast.line_number + 1}: Invalid data type {new_data_type}")

    def evaluate_true_switch_statement(self, index, true_switch_statement, switch_statements):
        self.evaluate_code_block(true_switch_statement.children[2])
        
        if true_switch_statement.children[-1].value == "<switch-statement-break-delimiter>":
            return

        if index + 1 == len(switch_statements.children):
            return
        
        if switch_statements.children[index + 1].value == "<default-loop>":
            return
        
        self.evaluate_true_switch_statement(index + 1, switch_statements.children[index + 1], switch_statements)

    def evaluate_switch_statements(self, switch_conditional_statements):
        for index, switch_conditional_statement in enumerate(switch_conditional_statements.children):
            if switch_conditional_statement.value == "<omg-loop>":
                if str(self.final_symbol_table.get_symbol("IT").symbolValue) == str(self.evaluate_literal_value(switch_conditional_statement.children[1].children[0]).symbolValue):
                    self.evaluate_true_switch_statement(index, switch_conditional_statement, switch_conditional_statements)

                    break
            if switch_conditional_statement.value == "<default-loop>":
                self.evaluate_code_block(switch_conditional_statement.children[1])
                
                break

    def evaluate_switch_case(self, switch_statement):
        for switch_information in switch_statement.children:
            if switch_information.value == "<switch-delimiter>":
                self.evaluate_switch_statements(switch_information)

    def evaluate_conditional_statements(self, conditional_statements):
        # Typecast the IT to TROOF if it is not
        if self.final_symbol_table.get_symbol("IT").symbolClassification != "TROOF":
            self.final_symbol_table.update_symbol("IT", self.type_cast_to_troof(self.final_symbol_table.get_symbol("IT")))

        for conditional_statement in conditional_statements.children:
            if str(self.final_symbol_table.get_symbol("IT").symbolValue) == "WIN" : # if true, go to true's codeblock
                if conditional_statement.value == "<if-statement>":
                    self.evaluate_code_block(conditional_statement.children[1])

                    break
            else:
                if conditional_statement.value == "<mebbe-loop>":
                    self.evaluate_expression_value(conditional_statement.children[1].children[0])

                    if str(self.final_symbol_table.get_symbol("IT").symbolValue) == "WIN":
                        self.evaluate_code_block(conditional_statement.children[2])

                        break
                elif conditional_statement.value == "<else-statement>":
                    self.evaluate_code_block(conditional_statement.children[1])

                    break

    def evaluate_conditional_case(self, conditional_statement):
        self.evaluate_conditional_statements(conditional_statement)

    def evaluate_loop_statements(self, loop_statements):
        # flag for loop operation; True for increment, False for decrement
        isIncrement = None

        # flag for loop condition; True for TIL, False for WILE
        isTILLoop = None

        for loop_statement in loop_statements.children:

            if loop_statement.value == "<loop-operation>":
                if loop_statement.children[0].value == "UPPIN":
                    # change flag to increment
                    isIncrement = True
                elif loop_statement.children[0].value == "NERFIN":
                    isIncrement = False
                else:
                    raise Exception(f"Error in line {loop_statement.line_number + 1}: Expected UPPIN or NERFIN but got {loop_statement.children[0].value}")
            elif loop_statement.value == "<variable-name>":
                # Check if the variable is already declared
                identifier = loop_statement.children[0].children[0].value
                if not self.final_symbol_table.check_if_symbol_exists(identifier):
                    raise Exception(f"CHECKER: Error in line {loop_statement.line_number + 1}: Variable {identifier} has not been declared")

                # Typecast the variable to NUMBR or NUMBAR if it is not
                if self.final_symbol_table.get_symbol(identifier).symbolClassification != "NUMBR" and self.final_symbol_table.get_symbol(identifier).symbolClassification != "NUMBAR":
                    self.final_symbol_table.update_symbol(identifier, self.type_cast_to_numbr_or_numbar(self.final_symbol_table.get_symbol(identifier)))

            # get if TIL or WILE
            elif loop_statement.value == "<loop-condition-keyword>":
                if loop_statement.children[0].value == "TIL":
                    isTILLoop = True
                elif loop_statement.children[0].value == "WILE":
                    isTILLoop = False
                else:
                    raise Exception(f"Error in line {loop_statement.line_number + 1}: Expected TIL or WILE but got {loop_statement.children[0].value}")
            # Get the value of the loop condition
            elif loop_statement.value == "<loop-condition-expression>":
                # Store the loop condition
                loop_condition = loop_statement.children[0]

                # Get the value of the loop condition
                self.evaluate_expression_value(loop_condition)

                if isTILLoop:
                    if str(self.final_symbol_table.get_symbol("IT").symbolValue) == "WIN":
                        break # Break the loop as the condition is already true
                elif isTILLoop == False:
                    if str(self.final_symbol_table.get_symbol("IT").symbolValue) == "FAIL":
                        break # Break the loop as the condition is already false
            elif loop_statement.value == "<code-block-statement>":
                if isTILLoop == True:
                    # Execute loop as long as condition is False
                    while str(self.final_symbol_table.get_symbol("IT").symbolValue) == "FAIL":
                        if isIncrement == True:
                            # Run the code block
                            self.evaluate_code_block(loop_statement)

                            # Increment
                            if self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBR", self.final_symbol_table.get_symbol(identifier).symbolValue + 1))
                            elif self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBAR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBAR", self.final_symbol_table.get_symbol(identifier).symbolValue + 1.00))

                            # Check if loop condition is still False
                            self.evaluate_expression_value(loop_condition)
                        else:
                            # Run the code block
                            self.evaluate_code_block(loop_statement)

                            # Decrement
                            if self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBR", self.final_symbol_table.get_symbol(identifier).symbolValue - 1))
                            elif self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBAR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBAR", self.final_symbol_table.get_symbol(identifier).symbolValue - 1.00))

                            # Check if loop condition is still true
                            self.evaluate_expression_value(loop_condition)

                        # Check if a break statement is present
                        if loop_statements.children[-3].value == "<loop-statement-break-delimiter>":
                            break # Break the loop as a GTFO keyword is present
                else:
                    while str(self.final_symbol_table.get_symbol("IT").symbolValue) == "WIN": #While it is WIN, run
                        if isIncrement == True:
                            # Run the code block
                            self.evaluate_code_block(loop_statement)

                            # Increment
                            if self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBR", self.final_symbol_table.get_symbol(identifier).symbolValue + 1))
                            elif self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBAR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBAR", self.final_symbol_table.get_symbol(identifier).symbolValue + 1.00))

                            # Check if loop condition is still False
                            self.evaluate_expression_value(loop_condition)
                        else:
                            # Run the code block
                            self.evaluate_code_block(loop_statement)

                            # Decrement
                            if self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBR", self.final_symbol_table.get_symbol(identifier).symbolValue - 1))
                            elif self.final_symbol_table.get_symbol(identifier).symbolClassification == "NUMBAR":
                                self.final_symbol_table.update_symbol(identifier, SymbolEntity("NUMBAR", self.final_symbol_table.get_symbol(identifier).symbolValue - 1.00))

                            # Check if loop condition is still true
                            self.evaluate_expression_value(loop_condition)

                        # Check if a break statement is present
                        if loop_statements.children[-3].value == "<loop-statement-break-delimiter>":
                            break # Break the loop as a GTFO keyword is present

    def evaluate_loop(self, loop_statement):
        self.evaluate_loop_statements(loop_statement)

    def evaluate_code_block(self, code_block):
        for statement in code_block.children:
            if statement.value == "<print>":
                self.evaluate_print(statement)
            elif statement.value == "<input>":
                self.evaluate_input(statement)
            elif statement.value == "<assignment>":
                self.evaluate_assignment(statement)
            elif statement.value ==  "<var-value>":
                self.evaluate_var_value(statement)
            elif statement.value in ["<arithmetic-expression>", "<boolean-expression>", "<comparison-expression>", "<concatenation-expression>"]:
                self.evaluate_expression_value(statement)
            elif statement.value == "<casting>":
                symbol_value = None

                # Check if the keyword A is present
                if statement.children[2].value == "<type-casting-reassignment-operator>":
                    symbol_value = self.evaluate_casting(self.final_symbol_table.evaluate_var_value(statement.children[1]), self.evaluate_data_type(statement.children[3]))
                else:
                    symbol_value = self.evaluate_casting(self.final_symbol_table.evaluate_var_value(statement.children[1]), self.evaluate_data_type(statement.children[2]))

                self.final_symbol_table.update_symbol("IT", symbol_value)
            elif statement.value == "<switch>":
                self.evaluate_switch_case(statement)
            elif statement.value == "<conditional-statement>":
                self.evaluate_conditional_case(statement)
            elif statement.value == "<loop-statement>":
                self.evaluate_loop(statement)
