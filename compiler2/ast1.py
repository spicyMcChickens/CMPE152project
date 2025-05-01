class ASTNode:
    pass

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return(ASTNode):
    def __init__(self, value):
        self.value = value  # The value being returned


class Assign:
    def __init__(self, target, value):
        self.target = target
        self.value = value

class Compound:
    def __init__(self, statements):
        self.statements = statements

class If:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class For:
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body

class Block:
    def __init__(self, statements):
        self.body = statements  # Store the list of statements in the block

    def __repr__(self):
        return f"Block({self.body})"

    def debug(self):
        print("Block Debug:")
        print(f"Body: {self.body}")

class Str(ASTNode):
    def __init__(self, value):
        self.value = value