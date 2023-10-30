<img alt="Version" src="https://img.shields.io/badge/version-0.1.0--alpha-blue.svg?cacheSeconds=604800" />
<a href="https://github.com/Gato-X/python-LinkedTuple/blob/main/LICENSE" target="_blank"><img alt="License:BSD" src="https://img.shields.io/badge/License-BSD-yellow.svg" /></a>

# cwriter

# Project Description
The package facilitates the creation of C (.h) files from Python. It's not designed to generate every possible C file or cover the entire C syntax. Rather, its primary focus is to generate files that contain elements like arrays or strings as well as constants, defines, and typedefs that can be used or imported from other sources.

# Example

This code

```python

	f = CFile("example.h")

	f.openGuard()
	f.define("THIS",0)
	f.newLine()
	an = {5:"This is a message", 30:("Another message, but with single=True",True)}
	f.varDefinition("const int[]","values", numbers, to_str_fn=paddedHex(2), annotations=an)
	f.newLine(2)
	f.comment("This is a test comment")
	f.varDeclaration("const int[]","values")

	f.comment(["Now a multilne","comment","here"])
	f.varDefinition("const char[]","other",[1,2,3,4,5])
	f.varDefinition(["const", "char[]"],
					"var_name","this is a string",
					extra_attribs="__attribute__ ((aligned (16)))")

	f.closeGuard()

	f.print()
	f.write()

```


Prints and generates this file
```c
#ifndef EXAMPLE_H_GUARD
#define EXAMPLE_H_GUARD

#define THIS 0

const int values[] = {
    0x00, 0x01, 0x02, 0x03, 0x04,
    // This is a message
    0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14,
    0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d,
    // Another message, but with single=True
    0x1e,
    0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e,
    0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e,
    0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e,
    0x4f, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e,
    0x5f, 0x60, 0x61, 0x62, 0x63
    };



// This is a test comment
extern const int values[];
/*
 * Now a multilne
 * comment
 * here
 */
const char other[] = {1, 2, 3, 4, 5};

const char var_name[] __attribute__ ((aligned (16))) = "this is a string";


#endif /* EXAMPLE_H_GUARD */
```

NOTE: The generated code is only and example, and doesn't intend to show what should be placed in an .h file.
  

# Licensing and Copyright 

BSD 2-Clause License

Copyright © 2023, Guillermo Romero (Gato)





