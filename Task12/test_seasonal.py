
"""Automated tests for seasonal rates and volume bonuses."""

import os
import sys
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.dirname(__file__))

from seasonal_calculator import (
    rate_per_litre,
    payout,
    bonus_for_ten_day_volume,
    ten_day_total,
)


class SeasonalCalculatorTests(unittest.TestCase):
    """Test the seasonal calculation rules."""

    def test_regular_base_rate(self):
        self.assertEqual(
            rate_per_litre("3.50", "8.50", "regular"),
            Decimal("30.00"),
        )

    def test_april_june_base_rate(self):
        self.assertEqual(
            rate_per_litre("3.50", "8.50", "apr_jun"),
            Decimal("32.00"),
        )

    def test_two_decimal_readings_regular(self):
        self.assertEqual(
            rate_per_litre("4.23", "8.67", "regular"),
            Decimal("33.40"),
        )

    def test_two_decimal_readings_seasonal(self):
        self.assertEqual(
            rate_per_litre("4.23", "8.67", "apr_jun"),
            Decimal("35.75"),
        )

    def test_regular_payment(self):
        self.assertEqual(
            payout("100", "4.23", "8.67", "regular"),
            Decimal("3340.00"),
        )

    def test_bonus_at_exact_threshold(self):
        self.assertEqual(
            bonus_for_ten_day_volume("500"),
            Decimal("0.00"),
        )

    def test_bonus_above_threshold(self):
        self.assertEqual(
            bonus_for_ten_day_volume("501"),
            Decimal("250.50"),
        )

    def test_ten_day_total_with_bonus(self):
        subtotal, bonus, total = ten_day_total(
            [("501", "3.5", "8.5")],
            "apr_jun",
        )

        self.assertEqual(subtotal, Decimal("16032.00"))
        self.assertEqual(bonus, Decimal("250.50"))
        self.assertEqual(total, Decimal("16282.50"))

    def test_invalid_season(self):
        with self.assertRaises(ValueError):
            rate_per_litre("3.5", "8.5", "winter")


if __name__ == "__main__":
    unittest.main()
