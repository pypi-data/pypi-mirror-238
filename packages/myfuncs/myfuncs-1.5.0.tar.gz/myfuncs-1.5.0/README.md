# myfuncs

`myfuncs` is a Python package that provides a set of utility functions designed to streamline your code and enhance efficiency across various projects and platforms.

## Installation

You can install `myfuncs` using pip:

```bash
pip install myfuncs
```

### Functions Overview

1. **`nlprint`**: Enhanced print function.

2. **`is_jwt`**: Checks if a given string or bytes is a valid JWT (JSON Web Token).

3. **`ranstr`**: Generates a random string of specified length and character set.

4. **`runcmd`**: Executes a shell command and optionally returns its output.

5. **`get_terminal_width`**: Retrieves the terminal width, defaulting to 80 if undetectable.

6. **`print_middle`**: Displays a string centered amidst a specified character.

7. **`print_columns`**: Prints list items in columns based on terminal width.

8. **`objinfo`**: Presents detailed information about an object, its attributes, methods, and documentation.

9. **`default_repr`**: Provides a standardized string representation of an object.

10. **`typed_evar`**: Fetches an environment variable with inferred or specified type.

For more detailed descriptions and usage examples, please refer to the module's source code.


## Running Tests

The `myfuncs` package includes a test suite to verify the operation of its functions. To run the tests:

```bash
python -m unittest tests/test_myfuncs.py
```

The other tests file exists for legacy purposes for legacy code in `funcs.py` (no longer used but kept for backwards compatibility).


## Contributing

Contributions to `myfuncs` are welcomed. If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/cc-d/myfuncs).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/cc-d/myfuncs/blob/main/LICENSE) file for more details.