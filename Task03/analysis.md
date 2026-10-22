
# Task 3 - Variables and Constants

Python uses snake_case for ordinary variable and function names.
Constants are conventionally written in UPPER_CASE.

Python does not enforce constants. A name such as BASE_RATE can
still be reassigned, but the uppercase convention communicates that
the value should not normally change during program execution.

Python is dynamically typed. A variable can refer to an integer
and later refer to a string. The type belongs to the object, not
permanently to the variable name.

Multiple assignment allows concise swapping:

a, b = b, a

If a rate value is written as a magic number in k separate places,
all k places may need revision. A named constant requires one edit.
A dictionary rate card also centralizes values and can support
multiple rate schedules.

Both constant lookup and dictionary lookup are O(1) for a fixed
rate card. The dictionary uses a small amount of additional memory.
Neither design meaningfully changes the overall O(n) processing
time for n farmer entries.
