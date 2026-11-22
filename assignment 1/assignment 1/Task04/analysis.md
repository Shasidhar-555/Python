
# Task 4 - Correct Expressions

Fat steps:
round((fat - STANDARD_FAT) / STEP_SIZE)

SNF steps:
round((snf - STANDARD_SNF) / STEP_SIZE)

Rate:
BASE_RATE + fat_steps * FAT_STEP_VALUE
           + snf_steps * SNF_STEP_VALUE

The rate should then be rounded to two decimal places.

Unexpected results include:

1. (4.2 - 3.5) / 0.1 can produce a value slightly different
   from 7 because binary floats approximate decimal fractions.
2. 0.1 + 0.2 is not exactly equal to 0.3.
3. round(2.675, 2) can return 2.67 because the stored float
   is not exactly 2.675.
4. -2 ** 2 is -4, while (-2) ** 2 is 4.

round() rounds to the nearest integer, with ties handled using
ties-to-even for Python's built-in numeric rounding in these cases.
int() truncates toward zero. math.floor() rounds downward.

For fat = 4.2, the mathematical step count is 7.
For fat = 3.1, the mathematical step count is -4.

Using int() or floor() on the raw floating-point expression can
give different results near a boundary. The rate calculation
should use the documented step rule and an appropriate numeric type.

All three step-count methods take O(1) time and O(1) extra space.
