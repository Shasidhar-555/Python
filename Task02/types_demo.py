
"""Explore Python data types and arithmetic operators."""

from decimal import Decimal

values = [10, 10.0, "10", True, [10, 8.5]]

for value in values:
    print(repr(value), "->", type(value))

print("7 / 2 =", 7 / 2)
print("7 // 2 =", 7 // 2)
print("7 % 2 =", 7 % 2)
print("-7 // 2 =", -7 // 2)

print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)

print(
    'Decimal("0.1") + Decimal("0.2") == Decimal("0.3"):',
    Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
)
