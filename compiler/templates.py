from dataclasses import dataclass, field
from typing import Optional
import json

# Replace this with dynamically generated class using FieldInfo, etc.
@dataclass
class ExampleStruct:
    name: Optional[str] = None
    age: Optional[int] = None
    active: Optional[bool] = None

def parse_json(input_str: str, StructClass):
    try:
        data = json.loads(input_str)
        obj = StructClass()
        for field_name in StructClass.__annotations__:
            if field_name in data:
                setattr(obj, field_name, data[field_name])
        return obj, 0
    except Exception:
        return None, -1

def parse_and_serialize_json(input_str: str, StructClass):
    obj, result = parse_json(input_str, StructClass)
    if result != 0 or obj is None:
        return None

    fields = []
    for field_name in StructClass.__annotations__:
        val = getattr(obj, field_name)
        if isinstance(val, bool):
            fields.append("true" if val else "false")
        elif val is None:
            fields.append("")
        else:
            fields.append(str(val))

    serialized = "SUCCESS|" + "|".join(fields)
    return serialized

# Example usage:
if __name__ == "__main__":
    input_json = '{"name": "Alice", "age": 30, "active": true}'
    result = parse_and_serialize_json(input_json, ExampleStruct)
    print(result)
