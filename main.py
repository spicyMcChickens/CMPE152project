import json
from typing import Dict, Any

# Define the Student class with annotations, similar to the Go struct
class Student:
    def __init__(self, first_name: str, last_name: str, student_id: int, currently_enrolled: bool):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.currently_enrolled = currently_enrolled


# Assuming these are the same as in Go (you would need to implement these)
class Analyzer:
    @staticmethod
    def analyze_struct(cls) -> Dict[str, Any]:
        # Mimicking the field analysis (reflection in Go)
        # This function returns the structure of the class
        field_info = []
        for field in cls.__annotations__:
            field_info.append({
                "name": field,
                "type": cls.__annotations__[field]
            })
        return field_info


class Compiler:
    @staticmethod
    def compile_and_build(c_struct: Dict[str, Any]):
        # Mimic compilation and build in Python (can be a mock here)
        return Parser(c_struct)

class Parser:
    def __init__(self, c_struct):
        self.c_struct = c_struct

    def parse(self, json_data: str):
        # Parse the JSON data into a dictionary
        data = json.loads(json_data)
        result = {}
        for field in self.c_struct['Fields']:
            field_name = field["name"]
            result[field_name] = data.get(field_name, None)
        return result


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

    # 1. Analyze the struct using reflection (in Python, we use class annotations)
    field_infos = Analyzer.analyze_struct(Student)
    
    # 2. Create CStruct representation
    c_struct = {
        "Name": "Student",
        "Fields": field_infos
    }

    # 3. Compile the parser
    parser = Compiler.compile_and_build(c_struct)

    # 4. Parse the JSON data
    result = parser.parse(json_data)

    # 5. Print the results
    print("Parsed Student Information:")
    print(f"First Name: {result['first_name']}")
    print(f"Last Name: {result['last_name']}")
    print(f"Student ID: {result['student_id']}")
    print(f"Currently Enrolled: {result['currently_enrolled']}")


if __name__ == "__main__":
    main()

