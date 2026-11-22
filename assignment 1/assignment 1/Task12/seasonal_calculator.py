
"""Seasonal milk rates and a ten-day volume bonus."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
STEP = Decimal("0.1")

STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")

SNF_STEP_VALUE = Decimal("0.30")
BONUS_THRESHOLD = Decimal("500")
BONUS_PER_LITRE = Decimal("0.50")


@dataclass(frozen=True)
class RateCard:
    """Hold the rate values applicable to one season."""

    base_rate: Decimal
    fat_step_value: Decimal
    snf_step_value: Decimal = SNF_STEP_VALUE


RATE_CARDS = {
    "regular": RateCard(
        Decimal("30.00"),
        Decimal("0.40"),
    ),
    "apr_jun": RateCard(
        Decimal("32.00"),
        Decimal("0.45"),
    ),
}


def money(value):
    """Round a monetary value to paisa using half-up rounding."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def select_rate_card(season):
    """Return the rate card for the requested season."""
    try:
        return RATE_CARDS[season]
    except KeyError:
        raise ValueError(
            "Season must be 'regular' or 'apr_jun'."
        ) from None


def rate_per_litre(fat, snf, season="regular"):
    """Calculate the rate using the selected seasonal rate card."""
    fat = Decimal(str(fat))
    snf = Decimal(str(snf))
    card = select_rate_card(season)

    fat_steps = (
        (fat - STANDARD_FAT) / STEP
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    snf_steps = (
        (snf - STANDARD_SNF) / STEP
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    rate = (
        card.base_rate
        + fat_steps * card.fat_step_value
        + snf_steps * card.snf_step_value
    )

    return money(rate)


def payout(litres, fat, snf, season="regular"):
    """Calculate one delivery payment rounded to paisa."""
    litres = Decimal(str(litres))

    if not litres.is_finite() or litres <= 0:
        raise ValueError("Litres must be a positive finite number.")

    return money(
        litres * rate_per_litre(fat, snf, season)
    )


def bonus_for_ten_day_volume(total_litres):
    """Apply the bonus if ten-day volume exceeds 500 litres."""
    total_litres = Decimal(str(total_litres))

    if total_litres > BONUS_THRESHOLD:
        return money(total_litres * BONUS_PER_LITRE)

    return Decimal("0.00")


def ten_day_total(deliveries, season="regular"):
    """Return delivery subtotal, bonus and final total.

    Each delivery is a (litres, fat, snf) tuple.
    """
    subtotal = Decimal("0.00")
    total_litres = Decimal("0.00")

    for litres, fat, snf in deliveries:
        litres = Decimal(str(litres))

        subtotal += payout(
            litres, fat, snf, season
        )
        total_litres += litres

    subtotal = money(subtotal)
    bonus = bonus_for_ten_day_volume(total_litres)
    final_total = money(subtotal + bonus)

    return subtotal, bonus, final_total


def main():
    """Display sample rates and bonus boundary examples."""
    for season in ("regular", "apr_jun"):
        rate = rate_per_litre("4.23", "8.67", season)
        amount = payout("100.00", "4.23", "8.67", season)

        print(
            f"{season:8} rate={rate:.2f} Rs/L, "
            f"100 L payment=Rs {amount:.2f}"
        )

    for litres in ("500", "501"):
        bonus = bonus_for_ten_day_volume(litres)
        print(f"Volume={litres} L, bonus=Rs {bonus:.2f}")


if __name__ == "__main__":
    main()
