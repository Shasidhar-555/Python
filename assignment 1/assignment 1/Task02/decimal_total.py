
from decimal import Decimal

payments = ["33.40"] * 1000 + ["0.10"] * 3


def total_float(items):
    """Calculate the total using binary floating-point values."""
    total = 0.0

    for amount in items:
        total += float(amount)

    return total


def total_decimal(items):
    """Calculate the total accurately from decimal strings."""
    total = Decimal("0.00")

    for amount in items:
        total += Decimal(amount)

    return total


def total_decimal_from_float(items):
    """Show the effect of converting an already approximated float."""
    total = Decimal("0.00")

    for amount in items:
        total += Decimal(float(amount))

    return total


print("float  :", total_float(payments))
print("Decimal:", total_decimal(payments))

print(
    0.1 + 0.2 == 0.3,
    Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
)

print("Decimal(float(...)):", total_decimal_from_float(payments))
