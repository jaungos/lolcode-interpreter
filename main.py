"""
    This file is the main file of the project. 
    This is an interpreter for the LOLCode programming language created using Python.
"""

from lolcode.interpreter import Interpreter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter")

        # File explorer
        self.file_explorer = tk.Button(root, text="Open File", command=self.open_file)
        self.file_explorer.pack(pady=10)

        # Frame for Text Editor and Tables
        self.editor_tables_frame = tk.Frame(root)
        self.editor_tables_frame.pack(pady=10)

        # Text editor
        self.text_editor = tk.Text(self.editor_tables_frame, height=20, width=50)
        self.text_editor.grid(row=0, column=0, padx=5, sticky="nsew")

        # Frame for List of Tokens and Symbol Table
        self.tables_frame = tk.Frame(self.editor_tables_frame)
        self.tables_frame.grid(row=0, column=1, padx=5, sticky="nsew")

        # List of Tokens
        self.tokens_label = tk.Label(self.tables_frame, text="Lexemes")
        self.tokens_label.grid(row=0, column=0, pady=(0, 5))

        self.tokens_treeview = ttk.Treeview(self.tables_frame, height=20, columns=('Lexeme', 'Classification'), show='headings')
        self.tokens_treeview.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

        self.tokens_treeview.heading('Lexeme', text='Lexeme')
        self.tokens_treeview.heading('Classification', text='Classification')

        # Symbol Table
        self.symbol_table_label = tk.Label(self.tables_frame, text="Symbol Table")
        self.symbol_table_label.grid(row=0, column=1, pady=(0, 5))

        self.symbol_treeview = ttk.Treeview(self.tables_frame, height=20, columns=('Identifier', 'Value'), show='headings')
        self.symbol_treeview.grid(row=1, column=1, pady=(0, 10), sticky="nsew")

        self.symbol_treeview.heading('Identifier', text='Identifier')
        self.symbol_treeview.heading('Value', text='Value')

        # Execute/Run button
        self.run_button = tk.Button(root, text="Execute", command=self.run_code)
        self.run_button.pack(pady=10)

        # Console
        self.console_text = tk.Text(root, height=20, width=150, state=tk.DISABLED)
        self.console_text.pack()

        # Configure row and column weights for resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    # Function to open a file
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("lol files", "*.lol"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, code)
        self.file_path = file_path

    # Function to run the code
    def run_code(self):
        # Get the code from the text editor
        code = self.text_editor.get(1.0, tk.END)

        # Initialize the lexical analyzer
        interpreter = Interpreter()
        interpreter.read_file(self.file_path)  # Read the file
        tokens = interpreter.run_lexer() # Run the lexical analyzer and get the tokens
        interpreter.run_parser() # Run the syntax analyzer
        symbol_table = interpreter.run_interpreter() # Run the semantic analyzer
    
        # Update List of Tokens
        self.tokens_treeview.delete(*self.tokens_treeview.get_children())
        for token, value in tokens:
            self.tokens_treeview.insert("", "end", values=(token, value))
            
        # Update Symbol Table
        # TODO: connect backend
        self.symbol_treeview.delete(*self.symbol_treeview.get_children())
        for variable, value in symbol_table:
            self.symbol_treeview.insert("", "end", values=(variable, value))

        # Update Console (replace with your own console output)
        # TODO: integrate console and inputs
        console_output = "Program executed successfully!\n"
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, console_output)
        self.console_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x768")  # Set an initial size
    app = GUI(root)
    root.mainloop()
