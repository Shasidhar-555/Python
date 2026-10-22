
"""Interactive milk payment calculator with input validation."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STEP_SIZE = Decimal("0.1")
CENT = Decimal("0.01")

MIN_FAT = Decimal("2.0")
MAX_FAT = Decimal("7.0")

# Demonstration assumption; confirm the allowed SNF range.
MIN_SNF = Decimal("0.0")
MAX_SNF = Decimal("15.0")


def money(value):
    """Round a monetary amount to the nearest paisa."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def decimal_value(text, field):
    """Convert text to Decimal or raise a helpful validation error."""
    try:
        value = Decimal(text.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError(
            f"{field} must be a valid decimal number."
        ) from None

    if not value.is_finite():
        raise ValueError(f"{field} must be a finite number.")

    return value


def validate_entry(farmer_id, shift, litres, fat, snf):
    """Check identity, shift, quantity and milk composition."""
    if not farmer_id.strip():
        raise ValueError("Farmer ID cannot be blank.")

    if shift.upper() not in {"AM", "PM"}:
        raise ValueError("Shift must be AM or PM.")

    if litres <= 0:
        raise ValueError("Litres must be greater than zero.")

    if not MIN_FAT <= fat <= MAX_FAT:
        raise ValueError("Fat must be between 2.0 and 7.0.")

    if not MIN_SNF <= snf <= MAX_SNF:
        raise ValueError("SNF must be between 0.0 and 15.0.")


def rate_per_litre(fat, snf):
    """Calculate the price per litre."""
    fat_steps = ((fat - STANDARD_FAT) / STEP_SIZE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )

    snf_steps = ((snf - STANDARD_SNF) / STEP_SIZE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )

    rate = (
        BASE_RATE
        + fat_steps * FAT_STEP_VALUE
        + snf_steps * SNF_STEP_VALUE
    )

    return money(rate)


def payout(litres, fat, snf):
    """Calculate one delivery's payment rounded to paisa."""
    return money(litres * rate_per_litre(fat, snf))


def ten_day_total(payments):
    """Return the total of already-rounded payment amounts."""
    return money(
        sum((money(value) for value in payments), Decimal("0.00"))
    )


def main():
    """Read entries until the clerk enters a blank farmer ID."""
    total = Decimal("0.00")
    print("Enter a blank farmer ID to finish.")

    while True:
        farmer_id = input("Farmer ID: ").strip()

        if not farmer_id:
            break

        try:
            shift = input("Shift (AM/PM): ").strip().upper()
            litres = decimal_value(input("Litres: "), "Litres")
            fat = decimal_value(input("Fat %: "), "Fat")
            snf = decimal_value(input("SNF %: "), "SNF")

            validate_entry(farmer_id, shift, litres, fat, snf)

            rate = rate_per_litre(fat, snf)
            amount = payout(litres, fat, snf)
            total += amount

            print(
                f"{farmer_id:>12} {shift:>2} "
                f"{litres:>8} L  rate Rs {rate:6.2f} "
                f"pay Rs {amount:8.2f} total Rs {total:9.2f}"
            )

        except ValueError as error:
            print("Invalid entry:", error)

    print(f"Ten-day total: Rs {total:.2f}")


if __name__ == "__main__":
    main()
