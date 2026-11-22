
"""Compare float and Decimal accumulation times."""

from decimal import Decimal
from time import perf_counter


def benchmark_float(count):
    total = 0.0
    start = perf_counter()

    for _ in range(count):
        total += float("33.40")

    elapsed = perf_counter() - start
    return total, elapsed


def benchmark_decimal(count):
    amount = Decimal("33.40")
    total = Decimal("0.00")
    start = perf_counter()

    for _ in range(count):
        total += amount

    elapsed = perf_counter() - start
    return total, elapsed


def main():
    for count in (300, 6000, 150000):
        float_total, float_time = benchmark_float(count)
        decimal_total, decimal_time = benchmark_decimal(count)

        print(f"\nPayments: {count}")
        print(f"Float total:   {float_total:.2f}")
        print(f"Decimal total: {decimal_total:.2f}")
        print(f"Float time:    {float_time:.6f} seconds")
        print(f"Decimal time:  {decimal_time:.6f} seconds")


if __name__ == "__main__":
    main()
