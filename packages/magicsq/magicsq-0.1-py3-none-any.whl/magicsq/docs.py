import os
import ast
"""
docs module

A utility module for the magicsq package to extract and format docstrings from 
the package modules for documentation purposes.

Functions:
- extract_function_docstrings(): Extract function-level docstrings from all Python files in a directory.
"""


def extract_function_docstrings(directory="."):
    """Extract function-level docstrings from all Python files in a directory."""
    docs = {}
    
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            with open(filename, 'r') as f:
                content = f.read()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_name = node.name
                        docstring = ast.get_docstring(node)
                        
                        if docstring:
                            docs[f"{filename}.{function_name}"] = docstring

    return docs

# Extract the docstrings
docstrings = extract_function_docstrings()

# Display the docstrings
for func, doc in docstrings.items():
    print(f"Function: {func}\n")
    print(doc)
    print('-' * 50)
