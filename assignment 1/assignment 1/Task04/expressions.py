
"""Explore expressions, rounding and operator behaviour."""

import math


def main():
    """Print examples of floating-point and rounding behaviour."""
    print("(4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)

    print(
        "Rounded step count:",
        round((4.2 - 3.5) / 0.1)
    )

    print("0.1 + 0.2 =", 0.1 + 0.2)
    print("round(2.675, 2) =", round(2.675, 2))

    print("round(-1.5) =", round(-1.5))
    print("int(-1.5) =", int(-1.5))
    print("floor(-1.5) =", math.floor(-1.5))

    print("-2 ** 2 =", -2 ** 2)
    print("(-2) ** 2 =", (-2) ** 2)

    fat = 4.2
    print("Fat valid:", 2.0 <= fat <= 7.0)

    for fat in (4.2, 3.1):
        raw = (fat - 3.5) / 0.1

        print(
            f"fat={fat}, raw={raw}, "
            f"round={round(raw)}, int={int(raw)}, "
            f"floor={math.floor(raw)}"
        )


if __name__ == "__main__":
    main()
