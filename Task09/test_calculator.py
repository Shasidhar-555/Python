
"""Automated tests for the milk payment calculator."""

import os
import sys
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.dirname(__file__))

from milk_calculator import (
    rate_per_litre,
    payout,
    validate_entry,
    decimal_value,
)


class MilkCalculatorTests(unittest.TestCase):
    """Test payment calculations and invalid inputs."""

    def test_standard_rate(self):
        self.assertEqual(
            rate_per_litre(Decimal("3.5"), Decimal("8.5")),
            Decimal("30.00"),
        )

    def test_above_standard(self):
        self.assertEqual(
            rate_per_litre(Decimal("4.2"), Decimal("8.7")),
            Decimal("33.40"),
        )

    def test_below_standard(self):
        self.assertEqual(
            rate_per_litre(Decimal("3.1"), Decimal("8.3")),
            Decimal("27.80"),
        )

    def test_payment(self):
        self.assertEqual(
            payout(
                Decimal("8.5"),
                Decimal("4.2"),
                Decimal("8.7"),
            ),
            Decimal("283.90"),
        )

    def test_fat_boundaries(self):
        validate_entry(
            "F1", "AM", Decimal("1"),
            Decimal("2.0"), Decimal("8.5")
        )
        validate_entry(
            "F1", "PM", Decimal("1"),
            Decimal("7.0"), Decimal("8.5")
        )

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            validate_entry(
                "F1", "AM", Decimal("-1"),
                Decimal("3.5"), Decimal("8.5")
            )

    def test_fat_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_entry(
                "F1", "AM", Decimal("1"),
                Decimal("7.1"), Decimal("8.5")
            )

    def test_invalid_text(self):
        with self.assertRaises(ValueError):
            decimal_value("eight", "Litres")

    def test_invalid_shift(self):
        with self.assertRaises(ValueError):
            validate_entry(
                "F1", "night", Decimal("1"),
                Decimal("3.5"), Decimal("8.5")
            )


if __name__ == "__main__":
    unittest.main()
