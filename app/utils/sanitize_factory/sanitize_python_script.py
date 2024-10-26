import ast

class PythonSanitizer(ast.NodeVisitor):
    """
    This class visits each node in the Abstract Syntax Tree (AST) of the Python code
    and checks for potentially unsafe nodes or expressions.
    """

    SAFE_FUNCTIONS = {'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple'}
    UNSAFE_NODES = (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal)
    UNSAFE_FUNCTIONS = {'eval', 'exec', 'open', 'input', '__import__'}

    def __init__(self):
        self.errors = []

    def visit_Call(self, node):
        # Check for unsafe function calls like eval, exec, open, input
        if isinstance(node.func, ast.Name) and node.func.id in self.UNSAFE_FUNCTIONS:
            self.errors.append(f"Unsafe function '{node.func.id}' is not allowed.")
        self.generic_visit(node)

    def visit(self, node):
        # Check for unsafe nodes like imports or other specified nodes
        if isinstance(node, self.UNSAFE_NODES):
            node_type = type(node).__name__
            self.errors.append(f"Unsafe node '{node_type}' is not allowed.")
        else:
            self.generic_visit(node)

    def is_safe(self):
        return len(self.errors) == 0

def sanitize_python_code(code):
    """
    Sanitizes Python code by parsing it into an AST and detecting unsafe nodes or expressions.
    
    Parameters:
    - code (str): The Python code to sanitize.
    
    Returns:
    - bool: True if code is safe, False otherwise.
    - list: List of error messages if unsafe code is detected.
    """
    try:
        # Parse code into an AST
        tree = ast.parse(code)
        
        # Initialize the sanitizer
        sanitizer = PythonSanitizer()
        
        # Visit each node
        sanitizer.visit(tree)
        
        # Return results
        return sanitizer.is_safe(), sanitizer.errors
    except SyntaxError as e:
        return False, [f"SyntaxError: {e}"]

# Example usage:
unsafe_code = """
import os
def my_function():
    print("Hello, World!")
    eval("print('This is unsafe!')")
"""

safe_code = """
def my_function():
    print("Hello, World!")
    x = len("safe code")
"""

# Test with unsafe code
is_safe, errors = sanitize_python_code(unsafe_code)
print("Is the code safe?", is_safe)
print("Errors:", errors)

# Test with safe code
is_safe, errors = sanitize_python_code(safe_code)
print("Is the code safe?", is_safe)
print("Errors:", errors)
