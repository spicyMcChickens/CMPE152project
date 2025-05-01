from compiler2.lexer import Lexer, TOKEN_TYPES
from compiler2.parser1 import Parser
from compiler2.generator import CodeGen
from compiler2.interpreter import Interpreter
from compiler2.ast1 import Block

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
        print(f"AST: {ast}")  # Debugging output
        if isinstance(ast, Block):
            print(f"Block body: {ast.body}")  # Debugging output

        interpreter.visit(ast)  # Interpret the code (run the program)
        print("Program output:", interpreter.symbol_table)
        
        # Generate the x86 code for the functions and expressions
        if isinstance(ast, Block):  # Ensure the AST is a Block
            print(f"Block body: {ast.body}")  # Debugging output
            codegen.generate(ast)  # Pass the entire Block to the CodeGen
        
        print("\nGenerated x86 Assembly:")
        print("\n".join(codegen.asm_code))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
