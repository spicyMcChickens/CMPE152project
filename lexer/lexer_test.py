import unittest
from .lexer import tokenize

class TestLexer(unittest.TestCase):
    def test_tokenize(self):
        code = '''
        int main() {
            // This is a comment
            int x = 10;
            float y = 20.5;
            string name = "Hello, World!";
            if (x > y) {
                x = y + 1;
            } else {
                x = y - 1;
            }
        }
        '''
        tokens=tokenize(code)
        expected_tokens = [
            ('Identifier', 'int'),
            ('Identifier', 'main'),
            ('Punctuation', '('),
            ('Punctuation', ')'),
            ('Punctuation', '{'),
            ('Comment', '// This is a comment'),
            ('Identifier', 'int'),
            ('Identifier', 'x'),
            ('Operator', '='),
            ('Number', '10'),
            ('Punctuation', ';'),
            ('Identifier', 'float'),
            ('Identifier', 'y'),
            ('Operator', '='),
            ('Number', '20.5'),
            ('Punctuation', ';'),
            ('Identifier', 'string'),
            ('Identifier', 'name'),
            ('Operator', '='),
            ('String', '"Hello, World!"'),
            ('Punctuation', ';'),
            ('Identifier', 'if'),
            ('Punctuation', '('),
            ('Identifier', 'x'),
            ('Operator', '>'),
            ('Identifier', 'y'),
            ('Punctuation', ')'),
            ('Punctuation', '{'),
            ('Identifier', 'x'),
            ('Operator', '='),
            ('Identifier', 'y'),
            ('Operator', '+'),
            ('Number', '1'),
            ('Punctuation', ';'),
            ('Punctuation', '}'),
            ('Identifier', 'else'),
            ('Punctuation', '{'),
            ('Identifier', 'x'),
            ('Operator', '='),
            ('Identifier', 'y'),
            ('Operator', '-'),
            ('Number', '1'),
            ('Punctuation', ';'),
            ('Punctuation', '}'),
            ('Punctuation', '}')
            ]
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_with_mismatched(self):
        with self.assertRaises(ValueError):
            tokenize("int x = 10; @")

if __name__=="__main__":
    unittest.main()