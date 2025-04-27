import json
from dataclasses import dataclass, field
from analyzer.types import StructField, StructType
from analyzer.reflect import breakdown_struct
from compiler.compiler import *
from lexer.lexer import *
from typing import  Dict, Any

@dataclass
class Student:
    first_name: str
    last_name: str
    student_id: int
    currently_enrolled: bool

    def __init__(self, first_name: str, last_name: str, student_id: int, currently_enrolled: bool):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.currently_enrolled = currently_enrolled

# Function to map Python types to C types
def map_python_type_to_c_type(python_type: str) -> str:
    type_mapping = {
        "str": "char*",
        "int": "int",
        "bool": "bool"
    }
    return type_mapping.get(python_type, None)

def main():
    # Example JSON data for testing
    json_data = '''
    {
        "first_name": "John",
        "last_name": "Doe",
        "student_id": 12345,
        "currently_enrolled": true
    }
    '''

    # 1. Analyze the struct using the Analyzer package
    field_infos = breakdown_struct(Student)

    # Convert field information into StructField objects
    struct_fields = [StructField(name=field.name,  type=field.type) for field in field_infos.fields]

    # 2. Create a StructType representation
    c_struct = StructType(name="Student", fields=struct_fields)

    # 3. Convert StructType to CStruct for compilation
    c_fields = []
    for field in struct_fields:
        c_type = map_python_type_to_c_type(field.type.__name__)
        if c_type is None:
            raise ValueError(f"Unsupported Python type: {field.type}")
        c_fields.append(FieldInfo(name=field.name, ctype=c_type))
    cstruct = CStruct(name="Student", fields=c_fields)

    # 4. Compile the parser using the Compiler package
    parser = compile_and_build(cstruct)

    # 5. Parse the JSON data using the Lexer package
    result = tokenize(json_data)

    # 6. Print the results
    print("Parsed Student Information:")
    print(f"First Name: {result['first_name']}")
    print(f"Last Name: {result['last_name']}")
    print(f"Student ID: {result['student_id']}")
    print(f"Currently Enrolled: {result['currently_enrolled']}")


if __name__ == "__main__":
    main()