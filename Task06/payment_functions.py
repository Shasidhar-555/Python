
"""Calculate milk rates and payments using reusable functions."""

from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STEP_SIZE = Decimal("0.1")
CENT = Decimal("0.01")


def round_money(value):
    """Round a monetary value to the nearest paisa."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def rate_per_litre(fat, snf):
    """Calculate the rate per litre from fat and SNF values."""
    fat = Decimal(str(fat))
    snf = Decimal(str(snf))

    fat_steps = (
        (fat - STANDARD_FAT) / STEP_SIZE
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    snf_steps = (
        (snf - STANDARD_SNF) / STEP_SIZE
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    rate = (
        BASE_RATE
        + fat_steps * FAT_STEP_VALUE
        + snf_steps * SNF_STEP_VALUE
    )

    return round_money(rate)


def payout(litres, fat, snf):
    """Calculate one delivery payment, rounded to paisa."""
    litres = Decimal(str(litres))
    return round_money(litres * rate_per_litre(fat, snf))


def ten_day_total(payments):
    """Return the sum of already-calculated delivery payments."""
    total = sum(
        (round_money(Decimal(str(p))) for p in payments),
        Decimal("0.00")
    )

    return round_money(total)


if __name__ == "__main__":
    print("Rate:", rate_per_litre("4.2", "8.7"))
    print("Payment:", payout("8.5", "4.2", "8.7"))

    print(
        "Ten-day total:",
        ten_day_total(["283.90", "300.00"])
    )
