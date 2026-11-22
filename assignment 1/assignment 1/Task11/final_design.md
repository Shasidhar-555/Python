
# Task 11 - Recommend and Defend the Final Design

## Recommendation

I recommend retaining the modular architecture while modifying
the numeric representation, validation and rate configuration.

Decimal should be used for financial calculations because it
represents decimal amounts accurately when constructed from
strings. Monetary values should be rounded to two decimal places
using an explicitly selected rounding rule.

The program should use named constants, reusable functions,
input validation and automated tests.

## Rate revision

The rate card should be maintained in one module or configuration
file. A rate revision should be followed by automated tests and
a review of expected outputs.

## Limitations

The demonstration calculator does not include a production
database, user authentication, audit logs, backup procedures,
or bank reconciliation.

The SNF validation range is an assumption and must be confirmed
with the co-operative.

The program uses a simple nearest-step rule. The co-operative
must approve this rule for readings with two decimal places.

## District-union scale

The algorithm processes n entries in O(n) time. A running total
requires O(1) additional space, while storing all records takes
O(n) space.

Processing 150,000 entries is practical for a simple calculation,
but a real district union also requires persistent records,
auditing, duplicate-entry prevention and transaction controls.

## Alternative rate configuration

A JSON file can store t configuration values. Reading it takes
O(t) time and O(t) memory. This allows seasonal rates to be
revised without editing Python source code.

The configuration must be validated when loaded. An invalid or
missing file must not silently result in incorrect payments.

## Evidence

Use the actual test results from Tasks 9, 10 and 12 to support
this recommendation. Record the measured timings and describe
the observed float-versus-Decimal difference.
