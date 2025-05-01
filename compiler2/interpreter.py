from .ast1 import *
class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = {}  # Store variables and their values

    def visit(self, node):
        if isinstance(node, Block):
            print("Visiting Block:")
            print(f"Block body: {node.body}")
            for stmt in node.body:
                print(f"Visiting statement: {stmt}")
                result = self.visit(stmt)
                # If a return value is encountered, propagate it up
                if result is not None:
                    return result

        elif isinstance(node, FunctionDef):
            print(f"Visiting FunctionDef: {node.name}")
            self.symbol_table[node.name] = node  # Store the function definition in the symbol table

        elif isinstance(node, Assign):
            print(f"Visiting Assign: target={node.target}, value={node.value}")
            value = self.visit(node.value)  # Evaluate the value being assigned
            self.symbol_table[node.target] = value  # Store the value in the symbol table

        elif isinstance(node, FunctionCall):
            print(f"Visiting FunctionCall: {node.name} with args {node.args}")
            # Handle the built-in `range` function
            if node.name == "range":
                if len(node.args) == 2:
                    start = self.visit(node.args[0])
                    end = self.visit(node.args[1])
                    return list(range(start, end))
                else:
                    raise Exception(f"range() expects 2 arguments, got {len(node.args)}")
            
            # Handle the built-in `print` function
            if node.name == "print":
                values = [self.visit(arg) for arg in node.args]
                print(*values)  # Use Python's built-in print function
                return None
            
            # Look up the function definition
            func = self.symbol_table.get(node.name)
            if not func or not isinstance(func, FunctionDef):
                raise Exception(f"Function {node.name} is not defined")
            
            # Evaluate arguments
            arg_values = [self.visit(arg) for arg in node.args]
            print(f"Evaluated arguments: {arg_values}")

            # Create a new symbol table for the function scope
            local_symbol_table = {}
            for param, arg in zip(func.params, arg_values):
                local_symbol_table[param] = arg

            # Save the current symbol table and switch to the function's symbol table
            previous_symbol_table = self.symbol_table
            self.symbol_table = local_symbol_table

            # Execute the function body
            try:
                return self.visit(func.body)  # Return the result of the function body
            finally:
                # Restore the previous symbol table
                self.symbol_table = previous_symbol_table

        elif isinstance(node, Return):
            print(f"Visiting Return: value={node.value}")
            return self.visit(node.value)  # Evaluate and return the value

        elif isinstance(node, If):
            print("Visiting If statement")
            condition = self.visit(node.condition)
            if condition:
                return self.visit(node.body)

        elif isinstance(node, For):
            print("Visiting For loop")
            iterable = self.visit(node.iterable)
            for value in iterable:
                self.symbol_table[node.var] = value
                result = self.visit(node.body)
                # If a return value is encountered, propagate it up
                if result is not None:
                    return result

        elif isinstance(node, Num):
            return node.value

        elif isinstance(node, Var):
            return self.symbol_table.get(node.name, None)

        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if node.op == 'PLUS':
                return left + right
            elif node.op == 'MINUS':
                return left - right
            elif node.op == 'MUL':
                return left * right
            elif node.op == 'DIV':
                return left // right

        else:
            raise Exception(f"Unknown node type: {type(node)}")
