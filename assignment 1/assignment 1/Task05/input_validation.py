
"""Read numeric values safely and format the output."""

from decimal import Decimal, InvalidOperation


def read_decimal(prompt):
    """Read a decimal value, retrying when input is invalid."""
    while True:
        text = input(prompt).strip()

        try:
            return Decimal(text)
        except InvalidOperation:
            print(
                "Invalid number. Use a decimal point, "
                "for example 8.5."
            )


def main():
    """Read sample milk values and display aligned output."""
    litres = read_decimal("Litres: ")
    fat = read_decimal("Fat percentage: ")
    snf = read_decimal("SNF percentage: ")

    print(f"Litres: {litres:>8}")
    print(f"Fat:    {fat:>8}%")
    print(f"SNF:    {snf:>8}%")


if __name__ == "__main__":
    main()
