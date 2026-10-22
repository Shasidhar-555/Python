
# Task 9 - Implementation and Testing

The calculator is implemented using separate functions for
conversion, validation, rate calculation and payment calculation.

## Test cases

| Test | Input or condition | Expected result |
|---|---|---|
| Standard | 10 L, fat 3.5, SNF 8.5 | Rs 300.00 |
| Above standard | 8.5 L, fat 4.2, SNF 8.7 | Rs 283.90 |
| Below standard | 12 L, fat 3.1, SNF 8.3 | Rs 333.60 |
| Minimum fat | 2.0% fat | Accepted |
| Maximum fat | 7.0% fat | Accepted |
| Negative litres | -1 L | Rejected |
| Fat too high | 7.1% fat | Rejected |
| Invalid number | "eight" | Rejected |
| Invalid shift | "night" | Rejected |

The expected total for the three normal examples is Rs 917.50.

The automated tests use assert-style checks through unittest.
They can be rerun consistently after each code change.
Manual testing requires repeated data entry and is more likely
to miss a boundary or regression case.

For m tests, the suite's time complexity is O(m), excluding
the constant setup overhead of the testing framework.
```

## 15. Task 10 — Compare expectations with execution

### `Task10/benchmark.py`

<CodeBlock language="python" editable>
"""Benchmark float and Decimal accumulation at three data sizes."""

from decimal import Decimal
from time import perf_counter


def benchmark(n):
    """Measure totals and execution times for n payments."""
    text_amount = "33.40"

    start = perf_counter()
    float_total = 0.0

    for _ in range(n):
        float_total += float(text_amount)

    float_time = perf_counter() - start

    start = perf_counter()
    decimal_total = Decimal("0.00")
    amount = Decimal(text_amount)

    for _ in range(n):
        decimal_total += amount

    decimal_time = perf_counter() - start

    difference = abs(
        Decimal(str(float_total)) - decimal_total
    )

    print(f"\nNumber of payments: {n:,}")
    print(f"Float total:   {float_total:.12f}")
    print(f"Decimal total: {decimal_total:.2f}")
    print(f"Difference:    {difference}")
    print(f"Float time:    {float_time:.6f} seconds")
    print(f"Decimal time:  {decimal_time:.6f} seconds")


if __name__ == "__main__":
    for count in (300, 6000, 150000):
        benchmark(count)
