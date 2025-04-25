import re
from typing import List, Tuple

Token=Tuple[str, str]

Token_Specs=[
    ('Number', r'\d+(\.\d+)?'),  # Integer or decimal number
    ('String', r'\".*?\"'),  # String enclosed in double quotes
    ('Identifier', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifier (variable names, function names, etc.)
    ('Operator', r'[\+\-\*/=<>!&|]+'),  # Operators
    ('Punctuation', r'[.,;:(){}[\]]'),  # Punctuation marks
    ('Whitespace', r'\s+'),  # Whitespace (spaces, tabs, newlines)
    ('Comment', r'//.*'),  # Single-line comment
    ('MultiLineComment', r'/\*.*?\*/'),  # Multi-line comment
    ('Newline', r'\n'),  # Newline character
    ('Tab', r'\t'),  # Tab character
    ('Mismatched', r'.'),  # Mismatched token (catch-all for any other character)
]

token_regex= '|'.join(f'(?P<{name}>{pattern})' for name, pattern in Token_Specs)
token_compile=re.compile(token_regex)

def tokenize(code:str)->List[Token]:
    tokens = []
    for match in token_compile.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'Whitespace' or kind == 'Comment' or kind == 'MultiLineComment' or kind == 'Newline' or kind == 'Tab':
            continue  # Ignore whitespace and comments
        elif kind == 'Mismatched':
            raise ValueError(f"Unexpected character: {value}")
        tokens.append((kind, value.strip("").strip("'")if kind == 'String' else value))
    return tokens
