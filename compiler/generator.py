import os
from string import Template
from dataclasses import dataclass
from typing import List

@dataclass
class FieldInfo:
    name: str
    c_type: str

@dataclass
class CStruct:
    name: str
    fields: List[FieldInfo]

# Replace with your parser template
PARSER_TEMPLATE = Template("""
#include "$Header"

void print_${StructName}(${StructName} data) {
% for field in Fields:
    printf("${field.name}: %s\\n", data.${field.name});
% endfor
}
""")

def generate_c_code(c_struct: CStruct) -> str:
    header = generate_c_header(c_struct)

    # Template data
    template_data = {
        'Header': f"{c_struct.name}.h",
        'StructName': c_struct.name,
        'Fields': c_struct.fields
    }

    # Render parser code using Template
    parser_code = render_parser_template(PARSER_TEMPLATE, template_data)

    return f"{header}\n{parser_code}"

def generate_c_header(c_struct: CStruct) -> str:
    header_lines = [
        f"#ifndef {c_struct.name}_H",
        f"#define {c_struct.name}_H\n",
        "#include <stdint.h>",
        "#include <stdbool.h>\n",
        f"typedef struct {{"
    ]
    for field in c_struct.fields:
        header_lines.append(f"    {field.c_type} {field.name};")
    header_lines.append(f"}} {c_struct.name};\n")
    header_lines.append(f"#endif // {c_struct.name}_H")

    return "\n".join(header_lines)

def render_parser_template(tmpl: Template, data: dict) -> str:
    # Basic rendering; you could use Jinja2 for better templating features
    # Manual loop substitution for now
    field_lines = "\n".join(
        f'    printf("{field.name}: %s\\n", data.{field.name});'
        for field in data['Fields']
    )
    result = tmpl.safe_substitute(
        Header=data['Header'],
        StructName=data['StructName']
    )
    return result.replace("% for field in Fields:\n", "").replace("% endfor", field_lines)

# Example usage:
if __name__ == "__main__":
    example_struct = CStruct(
        name="Person",
        fields=[
            FieldInfo(name="age", c_type="int"),
            FieldInfo(name="name", c_type="char*")
        ]
    )

    code = generate_c_code(example_struct)
    print(code)
