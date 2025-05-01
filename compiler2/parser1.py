# compiler/parser.py

from .lexer import TOKEN_TYPES
from .ast1 import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise SyntaxError(f"Expected {token_type} but got {self.current_token.type}")

    def parse(self):
        statements = []
        while self.current_token.type != TOKEN_TYPES['EOF']:
            if self.current_token.type == TOKEN_TYPES['NEWLINE']:
                self.eat(TOKEN_TYPES['NEWLINE'])
            else:
                statements.append(self.parse_statement())
        return ast.Block(statements)

    def parse_statement(self):
        if self.current_token.type == TOKEN_TYPES['DEF']:
            return self.parse_function_definition()
        elif self.current_token.type == TOKEN_TYPES['IF']:
            return self.parse_if_statement()
        elif self.current_token.type == TOKEN_TYPES['FOR']:
            return self.parse_for_loop()
        elif self.current_token.type == TOKEN_TYPES['RETURN']:
            return self.parse_return_statement()
        else:
            expr = self.parse_expression()
            if self.current_token.type == TOKEN_TYPES['ASSIGN']:
                return self.parse_assignment(expr)
            return expr

    def parse_function_definition(self):
        self.eat(TOKEN_TYPES['DEF'])
        name = self.current_token.value
        self.eat(TOKEN_TYPES['IDENTIFIER'])
        self.eat(TOKEN_TYPES['LPAREN'])
        params = self.parse_parameter_list()
        self.eat(TOKEN_TYPES['RPAREN'])
        self.eat(TOKEN_TYPES['COLON'])
        self.eat(TOKEN_TYPES['NEWLINE'])
        self.eat(TOKEN_TYPES['INDENT'])

        body = self.parse_block()

        self.eat(TOKEN_TYPES['DEDENT'])

        return ast.FunctionDef(name, params, body)

    def parse_parameter_list(self):
        params = []
        if self.current_token.type == TOKEN_TYPES['IDENTIFIER']:
            params.append(self.current_token.value)
            self.eat(TOKEN_TYPES['IDENTIFIER'])
            while self.current_token.type == TOKEN_TYPES['COMMA']:
                self.eat(TOKEN_TYPES['COMMA'])
                params.append(self.current_token.value)
                self.eat(TOKEN_TYPES['IDENTIFIER'])
        return params

    def parse_block(self):
        statements = []
        while self.current_token.type not in (TOKEN_TYPES['DEDENT'], TOKEN_TYPES['EOF']):
            print(f"Parsing block, current token: {self.current_token}")  # Debugging
            if self.current_token.type == TOKEN_TYPES['NEWLINE']:
                self.eat(TOKEN_TYPES['NEWLINE'])
                continue
            statements.append(self.parse_statement())
        return ast.Block(statements)

    def parse_if_statement(self):
        self.eat(TOKEN_TYPES['IF'])
        condition = self.parse_expression()
        self.eat(TOKEN_TYPES['COLON'])
        self.eat(TOKEN_TYPES['NEWLINE'])
        self.eat(TOKEN_TYPES['INDENT'])
        body = self.parse_block()
        self.eat(TOKEN_TYPES['DEDENT'])
        return ast.If(condition, body)

    def parse_for_loop(self):
        self.eat(TOKEN_TYPES['FOR'])
        var_name = self.current_token.value
        self.eat(TOKEN_TYPES['IDENTIFIER'])
        self.eat(TOKEN_TYPES['IN'])
        iterable = self.parse_expression()
        self.eat(TOKEN_TYPES['COLON'])
        self.eat(TOKEN_TYPES['NEWLINE'])
        self.eat(TOKEN_TYPES['INDENT'])
        body = self.parse_block()
        self.eat(TOKEN_TYPES['DEDENT'])
        return ast.For(var_name, iterable, body)

    def parse_return_statement(self):
        self.eat(TOKEN_TYPES['RETURN'])
        expr = self.parse_expression()
        return ast.Return(expr)

    def parse_assignment(self, left):
        if not isinstance(left, ast.Variable):
            raise SyntaxError("Cannot assign to non-variable.")
        self.eat(TOKEN_TYPES['ASSIGN'])
        value = self.parse_expression()
        return ast.Assign(left.name, value)

    def parse_expression(self):
        return self.parse_binary_operation()

    def parse_binary_operation(self, precedence=0):
        left = self.parse_primary()

        while True:
            op = self.current_token
            op_prec = self.get_operator_precedence(op)
            if op_prec < precedence:
                break

            self.eat(op.type)
            right = self.parse_binary_operation(op_prec + 1)
            left = ast.BinOp(left, op.type, right)

        return left

    def get_operator_precedence(self, token):
        if token.type in (TOKEN_TYPES['PLUS'], TOKEN_TYPES['MINUS']):
            return 10
        if token.type in (TOKEN_TYPES['STAR'], TOKEN_TYPES['SLASH']):
            return 20
        if token.type == TOKEN_TYPES['GT']:
            return 5
        return -1

    def parse_primary(self):
        token = self.current_token

        if token.type == TOKEN_TYPES['NUMBER']:
            self.eat(TOKEN_TYPES['NUMBER'])
            return ast.Num(token.value)

        if token.type == TOKEN_TYPES['STRING']:
            self.eat(TOKEN_TYPES['STRING'])
            return ast.Str(token.value)

        if token.type == TOKEN_TYPES['IDENTIFIER']:
            name = token.value
            self.eat(TOKEN_TYPES['IDENTIFIER'])

            if self.current_token.type == TOKEN_TYPES['LPAREN']:
                self.eat(TOKEN_TYPES['LPAREN'])
                args = self.parse_argument_list()
                self.eat(TOKEN_TYPES['RPAREN'])
                return ast.FunctionCall(name, args)

            return ast.Variable(name)

        if token.type == TOKEN_TYPES['LPAREN']:
            self.eat(TOKEN_TYPES['LPAREN'])
            expr = self.parse_expression()
            self.eat(TOKEN_TYPES['RPAREN'])
            return expr

        raise SyntaxError(f"Unexpected token: {token}")

    def parse_argument_list(self):
        args = []
        if self.current_token.type not in (TOKEN_TYPES['RPAREN'],):
            args.append(self.parse_expression())
            while self.current_token.type == TOKEN_TYPES['COMMA']:
                self.eat(TOKEN_TYPES['COMMA'])
                args.append(self.parse_expression())
        return args
