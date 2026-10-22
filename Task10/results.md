
# Task 10 - Expected vs Execution

## Experiment

The benchmark compares float and Decimal accumulation for
300, 6,000 and 150,000 payments of Rs 33.40.

## Expected observations

Float arithmetic may accumulate binary representation errors.
Decimal arithmetic constructed from decimal strings preserves
the intended decimal amounts in this experiment.

Both loops take O(n) time and O(1) additional space.

Decimal operations are often slower than float operations, but
their financial correctness is more important for this application.

## Rounding policy

The program rounds the rate per litre to two decimal places,
then rounds each delivery payment to two decimal places.
The ten-day total adds the rounded payments.

Rounding each payment and rounding only the grand total can
produce different results. The co-operative must specify which
policy matches its accounting and bank reconciliation rules.

## My actual measurements

Python version: TODO
Computer/operating system: TODO

| Payments | Float time | Decimal time | Observed difference |
|---:|---:|---:|---:|
| 300 | TODO | TODO | TODO |
| 6,000 | TODO | TODO | TODO |
| 150,000 | TODO | TODO | TODO |

Run `python Task10/benchmark.py` and replace every TODO with
the actual values printed by your computer.
Do not invent benchmark results.
