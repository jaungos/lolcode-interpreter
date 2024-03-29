"""
    This file is used to define the node class of a parse tree for the compiler. 
"""

class ParseTreeNode:
    def __init__(self, value, parent, line_number):
        self.value = value
        self.parent = parent
        self.children = []
        self.line_number = line_number

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level):
        print("   " * level + '- ' + str(self.value))
        for child in self.children:
            child.print_tree(level + 1)