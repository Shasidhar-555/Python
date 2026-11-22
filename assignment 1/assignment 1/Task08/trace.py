
"""Trace three example payments and the running total."""

from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP = Decimal("0.40")
SNF_STEP = Decimal("0.30")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP = Decimal("0.1")
CENT = Decimal("0.01")


def payment(litres, fat, snf):
    """Return the rounded rate and payment for one entry."""
    litres = Decimal(str(litres))
    fat = Decimal(str(fat))
    snf = Decimal(str(snf))

    fat_steps = ((fat - STANDARD_FAT) / STEP).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    snf_steps = ((snf - STANDARD_SNF) / STEP).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )

    rate = (
        BASE_RATE + fat_steps * FAT_STEP
        + snf_steps * SNF_STEP
    ).quantize(CENT, rounding=ROUND_HALF_UP)

    amount = (litres * rate).quantize(
        CENT, rounding=ROUND_HALF_UP
    )

    return rate, amount


entries = [
    ("A", "10", "3.5", "8.5"),
    ("B", "8.5", "4.2", "8.7"),
    ("C", "12", "3.1", "8.3"),
]

total = Decimal("0.00")

for farmer, litres, fat, snf in entries:
    rate, amount = payment(litres, fat, snf)
    total += amount

    print(
        f"{farmer}: rate={rate:.2f}, "
        f"payment={amount:.2f}, total={total:.2f}"
    )

print(f"Ten-day total: Rs {total:.2f}")
