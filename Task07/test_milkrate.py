
"""Test the milk-rate module from another script."""

from milkrate import payout, rate_per_litre


def main():
    """Demonstrate importing and calling the calculation functions."""
    print("Module imported successfully.")
    print("Rate:", rate_per_litre("4.2", "8.7"))
    print("Payment:", payout("8.5", "4.2", "8.7"))


if __name__ == "__main__":
    main()
