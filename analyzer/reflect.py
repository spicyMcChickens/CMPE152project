from dataclasses import is_dataclass, fields
from .types import StructType, StructField

'''breaks struct or classes into their fields and types for compilation'''
def breakdown_struct(cls):
    if not is_dataclass(cls):
        raise TypeError(f"{cls.name} is not a dataclass")
    
    struct_name= cls.__name__
    struct_fields = fields(cls)

    return StructType(name=struct_name,fields=struct_fields)
