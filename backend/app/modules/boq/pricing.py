"""Deterministic Decimal pricing (BR-03). Pure functions, no I/O, never floats.

TODO(C2): write the unit tests first (VAT on/off, ROUND_HALF_UP edge cases, null vs zero),
then implement. Only approved lines count towards totals; the LLM never computes totals.
"""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def round_money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)
