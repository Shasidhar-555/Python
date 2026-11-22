
# Task 1 - Understand the Problem and Identify the Data

## 1. Inputs and Outputs

The calculator accepts the following inputs:

- Farmer ID: a string because an ID may contain letters or leading zeroes.
- Litres: a positive decimal quantity because a farmer may supply fractional litres.
- Fat percentage: a decimal value between 2.0% and 7.0%, inclusive, according to the assignment.
- SNF percentage: a decimal value. A permitted SNF range must be confirmed by the co-operative.
- Shift: a string representing AM or PM.

The outputs are the rate per litre, the payment for each delivery and the farmer's ten-day total.

## 2. Named Constants

The following values should be named constants:

- BASE_RATE = Rs 30.00
- STANDARD_FAT = 3.5
- STANDARD_SNF = 8.5
- FAT_STEP_VALUE = Rs 0.40
- SNF_STEP_VALUE = Rs 0.30
- STEP_SIZE = 0.1

Named constants prevent a rate revision from being applied inconsistently in several expressions.

## 3. Data Types

Strings are appropriate for farmer IDs and shifts. Integers are useful for record counts. Decimal values represent litres, percentages, rates and payments. Boolean values represent validation results. Lists can store multiple entries.

Decimal is preferred for financial calculations because many decimal fractions cannot be represented exactly as binary floating-point numbers.

## 4. Validation Rules

1. Farmer ID must not be blank.
2. Shift must be AM or PM.
3. Litres must be greater than zero.
4. Fat must be between 2.0% and 7.0%, inclusive.
5. SNF must satisfy the range approved by the co-operative.
6. Invalid numeric input must be rejected.
7. The rate and delivery payment must follow an explicitly defined rounding rule.

Assumption: this implementation uses an SNF range of 0.0% to 15.0% for demonstration. The co-operative must confirm the actual range before production use.

## 5. Alternative Concept and Complexity

If every farmer had separate variables such as litres1, fat1 and snf1, then 300 farmers would require 900 individual data variables. Repeated code would make the program difficult to maintain.

A list of records allows the same loop to process any number of farmers.

For n records:
- Processing time: O(n)
- Storage for all records: O(n)
- Running-total approach with no stored records: O(1) extra space

The list-based design is easier to extend to 6,000 or 150,000 farmers.
