
"""Rate card and payment functions for the milk co-operative."""

from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")

STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")
CENT = Decimal("0.01")


def rate_per_litre(fat, snf):
    """Return the rate per litre rounded to two decimal places."""
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

    return rate.quantize(CENT, rounding=ROUND_HALF_UP)


def payout(litres, fat, snf):
    """Return the delivery payment rounded to two decimal places."""
    litres = Decimal(str(litres))
    rate = rate_per_litre(fat, snf)

    return (litres * rate).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


if __name__ == "__main__":
    entries = [
        (10, 3.5, 8.5),
        (8.5, 4.2, 8.7),
        (12, 3.1, 8.3),
    ]

    for litres, fat, snf in entries:
        rate = rate_per_litre(fat, snf)
        amount = payout(litres, fat, snf)

        print(
            f"{litres:5} L  fat {fat}  snf {snf}  "
            f"rate {rate:6.2f}  pay {amount:8.2f}"
        )
