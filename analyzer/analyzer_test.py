import unittest
from dataclasses import dataclass
from .reflect import breakdown_struct
from .types import StructType, StructField

@dataclass
class testStruct:
    id: int
    name: str

@dataclass
class TestAnalyzer(unittest.TestCase):
    def test_breakdown_struct(self):
        result = breakdown_struct(testStruct)
        expected = StructType(
            name='testStruct',
            fields=[
                StructField(name='id', type='int'),
                StructField(name='name', type='str')
            ]
        )
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()