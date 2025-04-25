import os
import tempfile
import unittest
from compiler import compile_parser, parse_json
from templates import CStruct, FieldInfo


class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.test_struct = CStruct(
            name="Person",
            fields=[
                FieldInfo(name="name", ctype="char*"),
                FieldInfo(name="age", ctype="int"),
                FieldInfo(name="is_student", ctype="bool")
            ]
        )
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_compile_parser_creates_files(self):
        output_dir = self.temp_dir.name
        compile_parser(self.test_struct, output_dir)

        header_path = os.path.join(output_dir, "Person.h")
        source_path = os.path.join(output_dir, "Person.c")

        self.assertTrue(os.path.exists(header_path))
        self.assertTrue(os.path.exists(source_path))

        with open(header_path, 'r') as f:
            content = f.read()
            for expected in [
                "#ifndef Person_H",
                "#define Person_H",
                "typedef struct {",
                "char* name;",
                "int age;",
                "bool is_student;",
                "} Person;"
            ]:
                self.assertIn(expected, content)

        with open(source_path, 'r') as f:
            content = f.read()
            for expected in [
                "int parse_json(const char* input, Person* out)",
                "strcmp(field, \"name\")",
                "strcmp(field, \"age\")",
                "strcmp(field, \"is_student\")",
                "parse_and_serialize_json"
            ]:
                self.assertIn(expected, content)

    def test_parse_json_various_cases(self):
        parser = compile_parser(self.test_struct)

        valid_cases = [
            ('{"name": "John Doe", "age": 25, "is_student": true}', {
                "name": "John Doe", "age": "25", "is_student": True
            }),
            ('{"name": "John Doe"}', {
                "name": "John Doe", "age": "0", "is_student": False
            }),
            ('{"name": "John \\"Johnny\\" Doe", "age": 25, "is_student": true}', {
                "name": 'John "Johnny" Doe', "age": "25", "is_student": True
            }),
            ("""
                {
                    "name": "John Doe",
                    "age": 25,
                    "is_student": true
                }
            """, {
                "name": "John Doe", "age": "25", "is_student": True
            })
        ]

        for json_str, expected in valid_cases:
            with self.subTest(json=json_str):
                result = parser.parse(json_str)
                self.assertEqual(result, expected)

        invalid_cases = [
            '"name": "John Doe", "age": 25}',
            '{"name": "John Doe", "age": 25',
            '{name: "John Doe"}',
            '{"name": John Doe}',
            '{"is_student": maybe}',
            '{"age": twenty}',
        ]

        for json_str in invalid_cases:
            with self.subTest(json=json_str):
                with self.assertRaises(ValueError):
                    parser.parse(json_str)

    def test_compile_parser_errors(self):
        error_cases = [
            (CStruct(name="", fields=[FieldInfo("name", "char*")]), "empty struct name"),
            (CStruct(name="Person", fields=[]), "struct has no fields"),
            (CStruct(name="Person", fields=[FieldInfo("", "char*")]), "empty field name"),
            (CStruct(name="Person", fields=[
                FieldInfo("name", "char*"),
                FieldInfo("name", "int")
            ]), "duplicate field name"),
            (CStruct(name="Person", fields=[FieldInfo("name", "float")]), "unsupported C type"),
            (CStruct(name="Person", fields=[FieldInfo("name", "")]), "empty C type"),
            (CStruct(name="Person", fields=None), "struct has no fields"),
            (CStruct(name="Person!@#", fields=[FieldInfo("name", "char*")]), "invalid struct name"),
            (CStruct(name="Person", fields=[FieldInfo("name!@#", "char*")]), "invalid field name"),
        ]

        for cstruct, err_msg in error_cases:
            with self.subTest(error=err_msg):
                with self.assertRaises(ValueError):
                    compile_parser(cstruct, self.temp_dir.name)

        # Invalid output directory
        bad_dir = "/nonexistent/directory"
        with self.assertRaises(OSError):
            compile_parser(self.test_struct, bad_dir)


if __name__ == "__main__":
    unittest.main()
