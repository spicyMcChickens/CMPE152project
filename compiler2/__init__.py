# compiler/__init__.py

# Expose key classes at the package level
from .lexer import Lexer
from .parser1 import Parser
from .ast1 import (
    Num, Var, BinOp, Assign, Compound, If, While, For, FunctionDef,
    FunctionCall, Return, Block
)
from .generator import CodeGen
from .interpreter import Interpreter

# Optionally: define what gets imported if someone does "from compiler import *"
__all__ = [
    'Lexer',
    'Parser',
    'Num', 'Var', 'BinOp', 'Assign', 'Compound', 'If', 'While', 'For', 
    'FunctionDef', 'FunctionCall', 'Return', 'Block',
    'CodeGenerator',
    'Interpreter',
]
