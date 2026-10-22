
# Task 12 - Re-evaluate and Adapt the Design

## A. Impact Analysis

The new requirements introduce two-decimal analyser readings,
a seasonal base rate of Rs 32.00, a seasonal fat-step value of
Rs 0.45, and a ten-day volume bonus.

The original calculation functions remain useful, but the rate
card must now depend on the selected season. The ten-day total
must also consider the farmer's total litres.

The implementation uses Decimal to avoid binary floating-point
errors in decimal analyser readings and money.

The step rule rounds each 0.1 percentage-point step count to
the nearest whole step using ROUND_HALF_UP. This is an explicit
assumption that must be approved by the co-operative.

## B. Evaluation of the Original Design

The original module and named constants remain appropriate
for reusable calculation logic.

However, fixed global rate values alone cannot represent
multiple seasonal rate cards cleanly. A RateCard data class
allows the program to select rates based on a season argument.

A separate bonus function prevents the farmer-level bonus
from being confused with the milk's base price per litre.

## C. Adaptation

The revised program provides:

- RateCard: stores the seasonal rates.
- select_rate_card(): selects a rate configuration.
- rate_per_litre(): calculates the price for a selected season.
- payout(): calculates a delivery payment.
- bonus_for_ten_day_volume(): applies the volume bonus.
- ten_day_total(): calculates the subtotal, bonus and final total.

## D. Evidence-Based Defence

Run:

python Task12/seasonal_calculator.py

python -m unittest discover -s Task12 -p "test_*.py"

The tests cover the regular rate card, April-June rate card,
two-decimal readings, a 500-litre boundary and a 501-litre
bonus case.

The example reading fat=4.23 and SNF=8.67 produces:
- Regular rate: Rs 33.40 per litre.
- April-June rate: Rs 35.75 per litre.

The bonus is zero at exactly 500 litres and Rs 250.50 at
501 litres under the stated assumption that all litres qualify
once the threshold is exceeded.

Screenshots and actual test results should be captured from
the student's own computer.
