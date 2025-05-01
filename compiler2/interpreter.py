from .ast1 import *

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = {}

    def visit(self, node):
        if isinstance(node, Block):
            for stmt in node.body:
                result = self.visit(stmt)
                if result is not None:  # Handle return values
                    return result

        elif isinstance(node, FunctionDef):
            self.symbol_table[node.name] = node

        elif isinstance(node, Assign):
            self.symbol_table[node.target] = self.visit(node.value)

        elif isinstance(node, If):
            if self.visit(node.condition):
                return self.visit(node.body)

        elif isinstance(node, For):
            iterable = self.visit(node.iterable)  # Evaluate the iterable (e.g., range)
            for value in iterable:
                self.symbol_table[node.var.name] = value  # Use the variable's name as the key
                result = self.visit(node.body)  # Visit the loop body
                if result is not None:  # Handle return values inside loops
                    return result

        elif isinstance(node, FunctionCall):
            if node.name == "print":
                # Evaluate all arguments before printing
                values = [self.visit(arg) for arg in node.args]
                print(*values)  # Use Python's built-in print function
                return None
            elif node.name == "range":
                # Handle the built-in `range` function
                if len(node.args) == 2:
                    start = self.visit(node.args[0])
                    end = self.visit(node.args[1])
                    return list(range(start, end))
                else:
                    raise Exception(f"range() expects 2 arguments, got {len(node.args)}")
            else:
                # Handle user-defined functions
                func = self.symbol_table.get(node.name)
                if not func:
                    raise Exception(f"Function {node.name} is not defined")
                arg_values = [self.visit(arg) for arg in node.args]
                local_symbol_table = {}
                for param, arg in zip(func.params, arg_values):
                    local_symbol_table[param] = arg
                previous_symbol_table = self.symbol_table
                self.symbol_table = local_symbol_table
                try:
                    result = self.visit(func.body)
                    return result
                finally:
                    self.symbol_table = previous_symbol_table

        elif isinstance(node, Return):
            return self.visit(node.value)

        elif isinstance(node, Num):
            return node.value

        elif isinstance(node, Var):
            value = self.symbol_table.get(node.name, 0)  # Retrieve the value using the variable's name
            print(f"Var: {node.name} = {value}")  # Debugging output
            return value

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
