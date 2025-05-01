import re

TOKEN_TYPES = {
    'NUMBER': 'NUMBER',
    'IDENTIFIER': 'IDENTIFIER',
    'PLUS': 'PLUS',
    'MINUS': 'MINUS',
    'MUL': 'MUL',
    'DIV': 'DIV',
    'MOD': 'MOD',
    'OR': 'OR',
    'AND': 'AND',
    'XOR': 'XOR',
    'EQUAL': 'EQUAL',
    'EQEQ': 'EQEQ',
    'GT': 'GT',
    'LT': 'LT',
    'GTE': 'GTE',
    'LTE': 'LTE',
    'LPAREN': 'LPAREN',
    'RPAREN': 'RPAREN',
    'COLON': 'COLON',
    'PRINT': 'PRINT',
    'IF': 'IF',
    'WHILE': 'WHILE',
    'FOR': 'FOR',
    'DEF': 'DEF',
    'RETURN': 'RETURN',
    'COMMA': 'COMMA',
    'INDENT': 'INDENT',
    'DEDENT': 'DEDENT',
    'NEWLINE': 'NEWLINE',
    'EOF': 'EOF',
    'UNKNOWN': 'UNKNOWN'
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.indent_level = 0

    def error(self, message):
        raise Exception(f"Lexer Error: {message}")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def get_next_token(self):
        self.skip_whitespace()

        if self.current_char is None:
            eof_token = Token(TOKEN_TYPES['EOF'], None, self.line)
            print(f"Generated EOF Token: {eof_token}")  # Debugging
            return eof_token

        # Handle '=' and '=='
        if self.current_char == '=':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(TOKEN_TYPES['EQEQ'], '==', self.line)
            return Token(TOKEN_TYPES['EQUAL'], '=', self.line)

        # Handle '>' and '>='
        if self.current_char == '>':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(TOKEN_TYPES['GTE'], '>=', self.line)
            return Token(TOKEN_TYPES['GT'], '>', self.line)

        # Handle '<' and '<='
        if self.current_char == '<':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(TOKEN_TYPES['LTE'], '<=', self.line)
            return Token(TOKEN_TYPES['LT'], '<', self.line)

        # Handle '+' (addition)
        if self.current_char == '+':
            self.advance()
            return Token(TOKEN_TYPES['PLUS'], '+', self.line)

        # Handle '-' (subtraction)
        if self.current_char == '-':
            self.advance()
            return Token(TOKEN_TYPES['MINUS'], '-', self.line)

        # Handle '*' (multiplication)
        if self.current_char == '*':
            self.advance()
            return Token(TOKEN_TYPES['MUL'], '*', self.line)

        # Handle '/' (division)
        if self.current_char == '/':
            self.advance()
            return Token(TOKEN_TYPES['DIV'], '/', self.line)

        # Handle '%' (modulus)
        if self.current_char == '%':
            self.advance()
            return Token(TOKEN_TYPES['MOD'], '%', self.line)

        # Handle '|' (bitwise OR)
        if self.current_char == '|':
            self.advance()
            return Token(TOKEN_TYPES['OR'], '|', self.line)

        # Handle '&' (bitwise AND)
        if self.current_char == '&':
            self.advance()
            return Token(TOKEN_TYPES['AND'], '&', self.line)

        # Handle '^' (bitwise XOR)
        if self.current_char == '^':
            self.advance()
            return Token(TOKEN_TYPES['XOR'], '^', self.line)

        # Handle ':' (colon)
        if self.current_char == ':':
            self.advance()
            return Token(TOKEN_TYPES['COLON'], ':', self.line)

        # Handle ',' (comma)
        if self.current_char == ',':
            self.advance()
            return Token(TOKEN_TYPES['COMMA'], ',', self.line)

        # Handle '(' (left parenthesis)
        if self.current_char == '(':
            self.advance()
            return Token(TOKEN_TYPES['LPAREN'], '(', self.line)

        # Handle ')' (right parenthesis)
        if self.current_char == ')':
            self.advance()
            return Token(TOKEN_TYPES['RPAREN'], ')', self.line)

        # Handle '\n' (newline)
        if self.current_char == '\n':
            self.advance()
            return Token(TOKEN_TYPES['NEWLINE'], '\n', self.line)

        # Handle numbers
        if self.current_char.isdigit():
            return self.number()

        # Handle identifiers and keywords
        if self.current_char.isalpha() or self.current_char == '_':
            return self.identifier()

        # Raise an error for unexpected characters
        self.error(f"Unexpected character: {self.current_char}")

    def number(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TOKEN_TYPES['NUMBER'], int(num_str), self.line)

    def identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str == 'if':
            return Token(TOKEN_TYPES['IF'], id_str, self.line)
        elif id_str == 'while':
            return Token(TOKEN_TYPES['WHILE'], id_str, self.line)
        elif id_str == 'for':
            return Token(TOKEN_TYPES['FOR'], id_str, self.line)
        elif id_str == 'def':
            return Token(TOKEN_TYPES['DEF'], id_str, self.line)
        elif id_str == 'return':
            return Token(TOKEN_TYPES['RETURN'], id_str, self.line)
        return Token(TOKEN_TYPES['IDENTIFIER'], id_str, self.line)

    def get_indent_level(self):
        leading_spaces = len(self.text[self.pos:]) - len(self.text[self.pos:].lstrip())
        return leading_spaces // 4  # Assuming 4 spaces for indentation

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line})"
