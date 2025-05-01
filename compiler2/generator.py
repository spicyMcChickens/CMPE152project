from .ast1 import*
class CodeGen:
    def __init__(self):
        self.asm_code = []
        self.data_section = []

    def generate(self, node):
        if isinstance(node, Num):
            self.asm_code.append(f"    mov eax, {node.value}")
        elif isinstance(node, Var):
            self.asm_code.append(f"    mov eax, [ebp - {4 * node.name}]")
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
                self.asm_code.append("    div ebx")

        elif isinstance(node, FunctionCall):
            self.asm_code.append(f"    call {node.name}")
        
        elif isinstance(node, FunctionDef):
            self.asm_code.append(f"{node.name}:")
            for stmt in node.body:
                self.generate(stmt)
            self.asm_code.append("    ret")

        elif isinstance(node, Return):
            self.asm_code.append(f"    mov eax, {node.expr.value}")
            self.asm_code.append("    ret")
