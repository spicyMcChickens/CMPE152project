# CMPE152project

## Description
Implementation Overview
The project consists of three main components:

Struct Analysis - Analyzes python structs
Code Generation - Generates code for parsing
Compilation - Compiles and loads the generated parser

## Features
- Key feature 1: Struct Analysis
-         add to later heehee
- Key feature 2: Code Generation
-         add to later nehehehehe
- Key feature 3: Parser Complilation
-         yk the drill by now 

## Type Support
- Integers (`int`)
- Booleans (`bool`)
- Strings (`char*` as pseudo-support)

## Validation
- Basic Python syntax checking
- Type correctness for supported primitives
- Variable declaration and scope validation

## Error Handling
- Informative compile-time error messages
- Detection of unsupported Python constructs
- Feedback on type or syntax mismatches

## Testing
Comprehensive tests included for:
- Tokenization and lexical analysis
- Basic parsing and AST generation
- MIPS instruction emission
- Sample Python code translation

---

## Limitations

Currently supports:
- Simple scalar types (`int`, `bool`, limited `char*`)
- Flat code blocks (no nested functions or classes)
- Basic control flow: `if`, `while`, and `print`

Not yet supported:
- Lists, dictionaries, or sets
- Function calls or recursion
- File I/O or libraries
- Object-oriented constructs

## Future Improvements

- Full support for:
  - Nested control structures
  - Functions and parameters
  - Lists and iteration

- Performance optimizations:
  - Register allocation improvements
  - Peephole MIPS optimizations

- Enhanced features:
  - Interactive REPL mode
  - Step-through debug output
  - Support for more Python data types


## Learning Motivation

This project was inspired by various minimalist compiler tools and transpilers encountered in open-source communities. It's meant as an educational exploration of how high-level languages can be translated into low-level representations.


## Key Learning Areas

## Compiler Construction Basics
- Tokenizing Python source
- Generating intermediate representations
- Emitting MIPS assembly from an abstract syntax tree

## Systems-Level Concepts
- Stack management and calling conventions
- Manual memory layout
- Instruction selection and branching

