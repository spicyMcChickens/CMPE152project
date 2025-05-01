from compiler2.lexer import Lexer, TOKEN_TYPES
from compiler2.parser1 import Parser
from compiler2.generator import CodeGen
from compiler2.interpreter import Interpreter
from compiler2.ast1 import *

def print_ast(node, indent=0):
    prefix = " " * indent
    if isinstance(node, Block):
        print(f"{prefix}Block:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    elif isinstance(node, FunctionDef):
        print(f"{prefix}FunctionDef(name={node.name}, params={node.params}):")
        print_ast(node.body, indent + 2)
    elif isinstance(node, Assign):
        print(f"{prefix}Assign(target={node.target}, value=):")
        print_ast(node.value, indent + 2)
    elif isinstance(node, If):
        print(f"{prefix}If(condition=):")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}Body:")
        print_ast(node.body, indent + 2)
    elif isinstance(node, For):
        print(f"{prefix}For(var={node.var}, iterable=):")
        print_ast(node.iterable, indent + 2)
        print(f"{prefix}Body:")
        print_ast(node.body, indent + 2)
    elif isinstance(node, FunctionCall):
        print(f"{prefix}FunctionCall(name={node.name}, args=):")
        for arg in node.args:
            print_ast(arg, indent + 2)
    elif isinstance(node, Return):
        print(f"{prefix}Return(value=):")
        print_ast(node.value, indent + 2)
    elif isinstance(node, BinOp):
        print(f"{prefix}BinOp(op={node.op}):")
        print(f"{prefix}  Left:")
        print_ast(node.left, indent + 4)
        print(f"{prefix}  Right:")
        print_ast(node.right, indent + 4)
    elif isinstance(node, Num):
        print(f"{prefix}Num(value={node.value})")
    elif isinstance(node, Var):
        print(f"{prefix}Var(name={node.name})")
    else:
        print(f"{prefix}Unknown node type: {type(node)}")

def main():
    code = """
def add(a, b):
    return a + b

x = add(5, 10)

if x > 5:
    print(x)

for i in range(0, 5):
    print(i)
    if i == 2:
        print(i + 100)
"""
    
    lexer = Lexer(code)
    tokens = []
    while True:
        token = lexer.get_next_token()
        print(f"Token: {token}")
        tokens.append(token)
        if token.type == TOKEN_TYPES['EOF']:  # Stop when EOF token is reached
            break
    parser = Parser(tokens)
    interpreter = Interpreter(parser)
    codegen = CodeGen()
    
    try:
        ast = parser.parse()  # Start parsing the code

        print_ast(ast)
        print("\n--- Python Code Execution Output ---")
        try:
            exec(code)  # Execute the code string directly
        except Exception as e:
            print(f"Error during execution: {e}")
        
        print("Program output:", interpreter.symbol_table)
        
        # Generate the x86 code for the functions and expressions
        if isinstance(ast, Block):  # Ensure the AST is a Block
           # print(f"Block body: {ast.body}")  # Debugging output
            codegen.generate(ast)  # Pass the entire Block to the CodeGen
        
        print("\n--- Generated x86 Assembly ---")
        print("\n".join(codegen.asm_code))
        
        print("\n--- AST Structure ---")
        print_ast(ast)  # Print the AST structure
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
