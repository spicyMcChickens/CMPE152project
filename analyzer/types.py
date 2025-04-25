from dataclasses import dataclass
from typing import List

@dataclass
class StructField:
    name: str
    type: str

@dataclass
class StructType:
    name: str
    fields: List[StructField]