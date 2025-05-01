import re

TOKEN_TYPES = {
    'STRING': 'STRING',
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
    'IN':'IN',
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
        self.indent_level = 0  # Track the current level of indentation

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
                break
            self.advance()

    def get_next_token(self):
        self.skip_whitespace()

        if self.current_char is None:
            # Finalize tokens by generating all remaining DEDENT tokens
            if not hasattr(self, 'finalized_tokens'):
                self.finalized_tokens = []
                while self.indent_level > 0:
                    self.indent_level -= 1
                    dedent_token = Token(TOKEN_TYPES['DEDENT'], None, self.line)
                    print(f"Generated DEDENT Token: {dedent_token}")  # Debugging
                    self.finalized_tokens.append(dedent_token)

                # Generate EOF token
                eof_token = Token(TOKEN_TYPES['EOF'], None, self.line)
                print(f"Generated EOF Token: {eof_token}")  # Debugging
                self.finalized_tokens.append(eof_token)

            # Return tokens from the finalized list
            if self.finalized_tokens:
                return self.finalized_tokens.pop(0)

        # Handle '\n' (newline)
        if self.current_char == '\n':
            self.advance()
            self.line += 1
            newline_token = Token(TOKEN_TYPES['NEWLINE'], '\n', self.line)
            print(f"Generated NEWLINE Token: {newline_token}")  # Debugging
            # Check for indentation changes
            current_indent = self.get_indent_level()
            indent_dedent_tokens = self.handle_indentation(current_indent)
            if indent_dedent_tokens:
                return indent_dedent_tokens.pop(0)  # Return the first token
            return newline_token

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
        elif id_str == 'in':
            return Token(TOKEN_TYPES['IN'], id_str, self.line)
        elif id_str == 'def':
            return Token(TOKEN_TYPES['DEF'], id_str, self.line)
        elif id_str == 'return':
            return Token(TOKEN_TYPES['RETURN'], id_str, self.line)
        return Token(TOKEN_TYPES['IDENTIFIER'], id_str, self.line)

    def get_indent_level(self):
        count = 0
        while self.current_char == ' ':
            count += 1
            self.advance()
        print(f"Current Indent Level: {count}, Previous Indent Level: {self.indent_level}")  # Debugging
        return count

    def handle_indentation(self, current_indent):
        tokens = []
        if current_indent > self.indent_level:
            self.indent_level = current_indent
            indent_token = Token(TOKEN_TYPES['INDENT'], None, self.line)
            print(f"Generated INDENT Token: {indent_token}")  # Debugging
            tokens.append(indent_token)
        elif current_indent < self.indent_level:
            while self.indent_level > current_indent:
                self.indent_level -= 1
                dedent_token = Token(TOKEN_TYPES['DEDENT'], None, self.line)
                print(f"Generated DEDENT Token: {dedent_token}")  # Debugging
                tokens.append(dedent_token)
        return tokens

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line})"
