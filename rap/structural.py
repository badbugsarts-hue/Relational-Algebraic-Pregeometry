"""Exact finite combinatorics only. No empirical constants, networking, or target loading.

H1: at least two distinct positive parts in descending order.
H2: successive gaps are at most one. These are declared predicates, not physical laws.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt
from typing import Iterator


def require_n(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('n must be a positive integer, not bool or a float')
    return n


def partitions(n: int, maximum: int | None = None) -> Iterator[tuple[int, ...]]:
    """Generate every descending positive integer partition exactly once."""
    require_n(n)
    if maximum is not None and (isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 1):
        raise ValueError('maximum must be a positive integer')
    def rec(total: int, bound: int):
        if total == 0:
            yield ()
            return
        for head in range(min(total, bound), 0, -1):
            for tail in rec(total - head, head):
                yield (head,) + tail
    yield from rec(n, n if maximum is None else maximum)


def valid_partition(parts: tuple[int, ...] | list[int], n: int | None = None) -> bool:
    if not isinstance(parts, (tuple, list)) or not parts or any(isinstance(x, bool) or not isinstance(x, int) or x < 1 for x in parts):
        return False
    return all(a >= b for a, b in zip(parts, parts[1:])) and (n is None or sum(parts) == n)


def admissible(parts: tuple[int, ...] | list[int]) -> bool:
    return (valid_partition(parts) and len(parts) >= 2 and len(set(parts)) == len(parts)
            and all(a - b <= 1 for a, b in zip(parts, parts[1:])))


def interval_solutions(n: int) -> list[tuple[int, ...]]:
    """Solve n = k*m + k*(k-1)/2 with m>=1, k>=2; no finite scan over m."""
    require_n(n)
    result = []
    kmax = (isqrt(8 * n + 1) - 1) // 2
    for k in range(2, kmax + 1):
        numerator = n - k * (k - 1) // 2
        m, remainder = divmod(numerator, k)
        if remainder == 0 and m >= 1:
            result.append(tuple(range(m + k - 1, m - 1, -1)))
    return sorted(result, reverse=True)


def interval_certificate(parts: tuple[int, ...] | list[int]) -> dict:
    if not admissible(parts):
        raise ValueError('certificate requires an admissible partition')
    k, m, n = len(parts), parts[-1], sum(parts)
    return {'n': n, 'k': k, 'm': m, 'parts': list(parts),
            'sum_formula_rhs': k*m + k*(k-1)//2,
            'scope': 'exact integer identity under declared H1/H2'}


def verify_interval_certificate(c: dict) -> bool:
    """Check all advertised fields, not merely the list of parts."""
    if not isinstance(c, dict) or set(c) != {'n','k','m','parts','sum_formula_rhs','scope'}:
        return False
    if any(isinstance(c.get(x), bool) or not isinstance(c.get(x), int) for x in ['n','k','m','sum_formula_rhs']):
        return False
    p = c.get('parts')
    if not isinstance(p, list) or not admissible(p):
        return False
    n,k,m=c['n'],c['k'],c['m']
    return (k >= 2 and m >= 1 and k == len(p) and m == p[-1] and n == sum(p)
            and p == list(range(m+k-1,m-1,-1))
            and c['sum_formula_rhs'] == n == k*m+k*(k-1)//2
            and c['scope'] == 'exact integer identity under declared H1/H2')


def algebra_signature(parts: tuple[int, ...] | list[int]) -> dict:
    if not valid_partition(parts):
        raise ValueError('descending positive parts required')
    return {'base_field': 'complex', 'block_sizes': list(parts),
            'matrix_size_sum': sum(parts), 'complex_algebra_dimension': sum(x*x for x in parts),
            'centre_dimension': len(parts), 'off_diagonal_count': sum(x*(x-1) for x in parts),
            'physical_representation_supplied': False, 'real_structure_supplied': False,
            'spectral_triple_constructed': False,
            'warning': 'a direct-sum signature is not a physical spectral triple or a gauge derivation'}


def equal_block_action_ratio(n: int, k: int) -> Fraction:
    require_n(n); require_n(k)
    if n <= 1 or n % k:
        raise ValueError('require n>1 and k dividing n')
    block = n // k
    return Fraction(block*block-1, n*n-1)
