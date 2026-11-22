
"""Demonstrate named constants, dynamic typing and swapping."""

BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STEP_SIZE = 0.1


def main():
    """Display constants and demonstrate Python assignments."""
    print("Base rate:", BASE_RATE)
    print("Fat step value:", FAT_STEP_VALUE)
    print("SNF step value:", SNF_STEP_VALUE)

    value = 10
    print(value, type(value))

    value = "ten"
    print(value, type(value))

    a, b = "AM", "PM"
    a, b = b, a
    print("Swapped:", a, b)


if __name__ == "__main__":
    main()
