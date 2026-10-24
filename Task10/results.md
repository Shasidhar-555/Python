# Task 10 — Benchmark Results

## Objective

Compare the execution time of floating-point (`float`) and decimal (`Decimal`) arithmetic when accumulating milk payments.

## Environment

- Language: Python 3.12
- Operating system: Windows
- Method: `time.perf_counter()`
- Payment amount per iteration: Rs. 33.40

## Results

| Number of payments | Float total (Rs.) | Decimal total (Rs.) | Float time (seconds) | Decimal time (seconds) |
|---:|---:|---:|---:|---:|
| 300 | 10,020.00 | 10,020.00 | 0.000073 | 0.000064 |
| 6,000 | 200,400.00 | 200,400.00 | 0.001391 | 0.000903 |
| 150,000 | 5,010,000.00 | 5,010,000.00 | 0.036913 | 0.019850 |

## Observations

1. Both methods produced the same displayed totals for these test cases.
2. In this benchmark run, Decimal was faster than float for all three payment counts.
3. Execution time increased as the number of payments increased.
4. Benchmark timings can vary depending on system load and other environmental factors. These results represent one run on this computer.

## Conclusion

The benchmark compares the execution times of float and Decimal arithmetic. For financial calculations, Decimal is generally preferred because it supports decimal arithmetic with explicit precision and rounding, making it more suitable for representing currency amounts reliably. Performance should be measured over repeated runs before drawing a general conclusion about speed.
