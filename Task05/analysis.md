
# Task 5 - Read Input and Convert Types

The input() function returns a string, even when the user types
digits. int() converts whole-number text, while float() converts
floating-point text. Decimal() can be used for exact decimal
representations when it is constructed directly from text.

The input "eight" is invalid numeric text. The input "8,5" is
also rejected by this program because it expects a dot as the
decimal separator. Surrounding whitespace is removed with strip().

A try/except block is preferable to checking characters manually
because valid numbers may contain signs or exponent notation.

For example:

try:
    value = float(text)
except ValueError:
    print("Invalid number")

An f-string such as f"{amount:8.2f}" prints a value in a field
eight characters wide with two digits after the decimal point.

Parsing and validating one input takes O(1) time for ordinary
bounded-length inputs and O(1) additional space.
