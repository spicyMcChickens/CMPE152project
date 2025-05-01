class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = {}

    def visit(self, node):
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, Var):
            if node.name in self.symbol_table:
                return self.symbol_table[node.name]
            raise Exception(f"Variable '{node.name}' not defined")
        elif isinstance(node, BinOp):
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            if node.op == 'PLUS':
                return left_val + right_val
            elif node.op == 'MINUS':
                return left_val - right_val
            elif node.op == 'MUL':
                return left_val * right_val
            elif node.op == 'DIV':
                return left_val / right_val
        elif isinstance(node, FunctionDef):
            self.symbol_table[node.name] = node
        elif isinstance(node, FunctionCall):
            func = self.symbol_table.get(node.name)
            if not func:
                raise Exception(f"Function '{node.name}' is not defined.")
            return self.call_function(func, node.args)
        elif isinstance(node, Return):
            return self.visit(node.expr)

    def call_function(self, func, args):
        if len(args) != len(func.params):
            raise Exception(f"Function '{func.name}' expects {len(func.params)} arguments, got {len(args)}.")
        local_scope = {func.params[i]: self.visit(arg) for i, arg in enumerate(args)}
        return_val = None
        for stmt in func.body:
            return_val = self.visit(stmt)
        return return_val
