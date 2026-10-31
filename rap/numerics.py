"""Isolated mpmath diagnostics on mathematical identities, not physical fitting.

Finite precision residuals below a threshold are observations, not rigorous error bounds.
No calibrated reference values are imported here.
"""
from __future__ import annotations
from fractions import Fraction
import mpmath


def precision_diagnostics(dps: int = 80) -> dict:
    if isinstance(dps, bool) or not isinstance(dps, int) or dps < 80:
        raise ValueError('use at least 80 decimal digits')
    before = mpmath.mp.dps
    ctx = mpmath.mp.clone()
    ctx.dps = dps
    threshold_digits = 40 if dps < 100 else 60
    tolerance = ctx.mpf(10) ** (-threshold_digits)
    # Same log identity in two evaluation orders; no mass-gap model or target value.
    integers = tuple(range(2, 10))
    product = 1
    for x in integers:
        product *= x
    left = ctx.log(ctx.mpf(product))
    right = ctx.fsum(ctx.log(ctx.mpf(x)) for x in integers)
    residual = abs(left - right)
    # An exact rational identity is established independently, not by rounded cancellation.
    rational = Fraction(1, 7) + Fraction(2, 7) - Fraction(3, 7)
    rational_residual = abs(ctx.mpf(1)/7 + ctx.mpf(2)/7 - ctx.mpf(3)/7)
    # Demonstrate why zero residual alone is not a universal exactness certificate.
    huge = ctx.mpf(10) ** (dps + 20)
    cancellation = (huge + 1) - huge
    unchanged = mpmath.mp.dps == before
    return {'working_decimal_digits': dps, 'context': 'mp.clone; independent context per invocation',
            'global_context_unchanged': unchanged, 'mpmath_version': mpmath.__version__,
            'log_identity': {'residual': ctx.nstr(residual, dps),
                'criterion': 'absolute observed residual < 10^(-threshold_digits)',
                'threshold_digits': threshold_digits, 'observed_consistency': bool(residual < tolerance)},
            'rational_control': {'exact_fraction_residual': str(rational),
                'observed_mpmath_residual': ctx.nstr(rational_residual, dps),
                'observed_consistency': bool(rational_residual < tolerance)},
            'rounding_counterexample': {'expression': '(10^(dps+20)+1)-10^(dps+20)',
                'rounded_result': ctx.nstr(cancellation, 8), 'exact_integer_result': 1,
                'shows_loss_of_exactness': bool(cancellation != 1)},
            'certified_error_bound': None, 'physical_validation': False,
            'scope': 'numerical self-consistency diagnostics, not a Yang-Mills or RAP existence proof'}
