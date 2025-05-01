from .ast1 import *

class CodeGen:
    def __init__(self):
        self.asm_code = []  # List to store generated assembly code

    def generate(self, node):
        if isinstance(node, Block):
            print("Generating code for Block:")
            #print(f"Block body: {node.body}")  # Debugging output
            for stmt in node.body:  # Iterate over the body of the block
                self.generate(stmt)

        elif isinstance(node, FunctionDef):
            print(f"Generating code for FunctionDef: {node.name}")
            self.asm_code.append(f"{node.name}:")
            self.asm_code.append("    push ebp")
            self.asm_code.append("    mov ebp, esp")
            self.generate(node.body)  # Generate code for the function body
            self.asm_code.append("    pop ebp")
            self.asm_code.append("    ret")

        elif isinstance(node, Return):
            print(f"Generating code for Return: {node.value}")
            self.generate(node.value)  # Generate code for the return value
            self.asm_code.append("    mov esp, ebp")  # Restore the stack pointer
            self.asm_code.append("    pop ebp")       # Restore the base pointer
            self.asm_code.append("    ret")           # Return from the function

        elif isinstance(node, Assign):
            print(f"Generating code for Assign: {node.target}")
            self.generate(node.value)
            self.asm_code.append(f"    mov [ebp - {4 * hash(node.target)}], eax")

        elif isinstance(node, If):
            print("Generating code for If statement")
            self.generate(node.condition)
            self.asm_code.append("    cmp eax, 0")
            self.asm_code.append("    je .endif")
            self.generate(node.body)
            self.asm_code.append(".endif:")

        elif isinstance(node, For):
            print("Generating code for For loop")
            self.asm_code.append(f"{node.var}_start:")
            self.generate(node.iterable)
            self.asm_code.append("    cmp eax, 0")
            self.asm_code.append("    je .endfor")
            self.generate(node.body)
            self.asm_code.append("    jmp {node.var}_start")
            self.asm_code.append(".endfor:")

        elif isinstance(node, FunctionCall):
            print(f"Generating code for FunctionCall: {node.name} with args {node.args}")
            # Push arguments onto the stack in reverse order
            for arg in reversed(node.args):
                self.generate(arg)
                self.asm_code.append("    push eax")
            # Call the function
            self.asm_code.append(f"    call {node.name}")
            # Clean up the stack after the call
            self.asm_code.append(f"    add esp, {4 * len(node.args)}")

        elif isinstance(node, Num):
            self.asm_code.append(f"    mov eax, {node.value}")

        elif isinstance(node, Var):
            self.asm_code.append(f"    mov eax, [ebp - {4 * hash(node.name)}]")

        elif isinstance(node, BinOp):
            self.generate(node.left)
            self.asm_code.append("    push eax")
            self.generate(node.right)
            self.asm_code.append("    pop ebx")
            if node.op == 'PLUS':
                self.asm_code.append("    add eax, ebx")
            elif node.op == 'MINUS':
                self.asm_code.append("    sub eax, ebx")
            elif node.op == 'MUL':
                self.asm_code.append("    imul eax, ebx")
            elif node.op == 'DIV':
                self.asm_code.append("    xor edx, edx")
                self.asm_code.append("    idiv ebx")

        else:
            raise Exception(f"Unknown node type: {type(node)}")
