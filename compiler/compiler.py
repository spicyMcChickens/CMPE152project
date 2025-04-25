import os
import subprocess
import re
import logging
from typing import List, Dict

# Regular expression to validate valid identifiers (for struct names and field names)
valid_identifier_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


class FieldInfo:
    def __init__(self, name: str, ctype: str):
        self.name = name
        self.ctype = ctype


class CStruct:
    def __init__(self, name: str, fields: List[FieldInfo]):
        self.name = name
        self.fields = fields


# Validate CStruct
def validate_struct(cstruct: CStruct) -> None:
    # Check struct name
    if not cstruct.name:
        raise ValueError("Empty struct name")
    if not valid_identifier_regex.match(cstruct.name):
        raise ValueError(f"Invalid struct name: must be a valid C identifier")

    # Check fields
    if not cstruct.fields:
        raise ValueError("Struct has no fields")

    field_names = set()
    for field in cstruct.fields:
        if not field.name:
            raise ValueError("Empty field name")
        if not valid_identifier_regex.match(field.name):
            raise ValueError(f"Invalid field name: {field.name} (must be a valid C identifier)")
        if field.name in field_names:
            raise ValueError(f"Duplicate field name: {field.name}")
        field_names.add(field.name)

        # Validate CType
        if field.ctype not in ["char*", "int", "bool"]:
            raise ValueError(f"Unsupported C type: {field.ctype}")


# Generate C code for the struct
def generate_c_code(cstruct: CStruct) -> str:
    header_template = f"""
#ifndef {cstruct.name.upper()}_H
#define {cstruct.name.upper()}_H

typedef struct {{
"""
    body = ""
    for field in cstruct.fields:
        body += f"    {field.ctype} {field.name};\n"

    footer = f"""
}} {cstruct.name};

#endif // {cstruct.name.upper()}_H
"""

    return header_template + body + footer


# Compile the struct and generate C code files
def compile_parser(cstruct: CStruct, output_dir: str) -> None:
    # Validate struct
    validate_struct(cstruct)

    # Generate C code
    c_code = generate_c_code(cstruct)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Write the C code to header and implementation files
    header_file = os.path.join(output_dir, f"{cstruct.name}.h")
    c_file = os.path.join(output_dir, f"{cstruct.name}.c")

    # Write header and implementation
    with open(header_file, "w") as f:
        f.write(c_code.split("}\n")[0] + "}\n")
    with open(c_file, "w") as f:
        f.write(c_code.split("}\n")[1])


# Compile and build the parser
def compile_and_build(cstruct: CStruct) -> Dict:
    output_dir = "c_output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate and write C code
    compile_parser(cstruct, output_dir)

    # Create main C file
    main_file = os.path.join(output_dir, f"main_{cstruct.name}.c")
    main_code = f"""
#include <stdio.h>
#include <stdlib.h>
#include "{cstruct.name}.h"

extern char* parse_and_serialize_json(const char* input);
extern void free_serialized(char* str);

int main(int argc, char *argv[]) {{
    if (argc != 2) {{
        fprintf(stderr, "Usage: %%s <json_string>\\n", argv[0]);
        return 1;
    }}

    char* result = parse_and_serialize_json(argv[1]);
    if (result == NULL) {{
        printf("ERROR|Failed to parse JSON\\n");
        return 1;
    }}

    printf("%%s", result);  // No newline in output
    free_serialized(result);
    return 0;
}}
"""
    with open(main_file, "w") as f:
        f.write(main_code)

    # Compile the program
    out_path = os.path.join(output_dir, f"parser_{cstruct.name}")
    cmd = ["gcc", "-o", out_path, main_file, os.path.join(output_dir, f"{cstruct.name}.c")]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Compilation failed: {result.stderr}")

    # Return the compiled parser information
    return {
        "exec_path": out_path,
        "cleanup": lambda: cleanup_files(main_file, output_dir, cstruct.name, out_path)
    }


def cleanup_files(main_file: str, output_dir: str, struct_name: str, out_path: str):
    # Remove generated files
    logging.info(f"Removing File: {main_file}")
    os.remove(main_file)
    logging.info(f"Removing File: {os.path.join(output_dir, f'{struct_name}.c')}")
    os.remove(os.path.join(output_dir, f"{struct_name}.c"))
    logging.info(f"Removing File: {os.path.join(output_dir, f'{struct_name}.h')}")
    os.remove(os.path.join(output_dir, f"{struct_name}.h"))
    logging.info(f"Removing File: {out_path}")
    os.remove(out_path)


# Parse a JSON string using the compiled parser
def parse_with_compiled_parser(exec_path: str, json_str: str) -> Dict:
    result = subprocess.run([exec_path, json_str], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Parser execution failed: {result.stderr}")

    output = result.stdout.strip()
    parts = output.split("|")

    if parts[0] != "SUCCESS":
        raise ValueError(f"Parsing failed: {output}")

    # Convert to map based on field information (placeholder for actual field handling)
    parsed_result = {f"field_{i+1}": part.strip() for i, part in enumerate(parts[1:])}
    return parsed_result


# Example usage
if __name__ == "__main__":
    # Create a struct and compile it
    fields = [FieldInfo(name="field1", ctype="int"), FieldInfo(name="field2", ctype="char*")]
    cstruct = CStruct(name="ExampleStruct", fields=fields)

    # Compile and build
    parser_info = compile_and_build(cstruct)

    # Use the compiled parser to parse a JSON string
    try:
        parsed_data = parse_with_compiled_parser(parser_info["exec_path"], '{"field1": 123, "field2": "abc"}')
        print(parsed_data)
    finally:
        # Clean up generated files
        parser_info["cleanup"]()
