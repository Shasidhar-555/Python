
# Task 6 - Functions and Scope

rate_per_litre(fat, snf) returns the calculated price per litre.

payout(litres, fat, snf) returns the payment for one delivery.

ten_day_total(payments) returns the sum of payment amounts.

Returning values makes functions easier to reuse and test.
Printing only displays information and does not provide a result
that other calculations can directly use.

Parameters and local variables belong to a function call.
Rate constants can be read from the module scope, but functions
should not modify them.

Docstrings explain the purpose of each function.

A single long script duplicates logic and is harder to test.
Lambda expressions are useful for short functions but are not a
good replacement for multi-step validation and financial logic.

For n entries, processing takes O(n) time. The running total
uses O(1) additional space if individual records are not retained.
Function-call overhead exists but is generally small compared
with input/output and other work.
