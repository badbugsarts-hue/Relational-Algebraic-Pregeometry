"""Spectral graph diagnostics for PR-2.

Scientific status: [D] (Software graph diagnostic only).
Physical interpretation is strictly forbidden.
"""

from mpmath import mp, matrix, eig, log
from typing import List
from verification.pregeometry.primitives import RelationalState

PRECISION_DECIMAL_DIGITS = 80

def _get_adjacency_matrix(state: RelationalState) -> matrix:
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        n = state.distinction_count()
        adjacency = matrix(n, n)
        for relation in state.relations:
            i = relation.source.value
            j = relation.target.value
            adjacency[i, j] = mp.fadd(adjacency[i, j], mp.mpf(1), exact=True)
            if not relation.directed:
                adjacency[j, i] = mp.fadd(adjacency[j, i], mp.mpf(1), exact=True)
        return adjacency

def _get_degree_matrix(state: RelationalState, adjacency: matrix) -> matrix:
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        n = state.distinction_count()
        degree = matrix(n, n)
        for i in range(n):
            degree[i, i] = mp.fsum(adjacency[i, j] for j in range(n))
        return degree


def _matrix_difference(left: matrix, right: matrix) -> matrix:
    result = matrix(left.rows, left.cols)
    for i in range(left.rows):
        for j in range(left.cols):
            result[i, j] = mp.fsub(left[i, j], right[i, j], exact=True)
    return result


def _matrix_product(left: matrix, right: matrix) -> matrix:
    result = matrix(left.rows, right.cols)
    for i in range(left.rows):
        for j in range(right.cols):
            result[i, j] = mp.fdot(
                (left[i, k], right[k, j])
                for k in range(left.cols)
            )
    return result

def combinatorial_laplacian_spectrum(state: RelationalState) -> List[mp.mpf]:
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        if state.distinction_count() == 0:
            return []
        adjacency = _get_adjacency_matrix(state)
        degree = _get_degree_matrix(state, adjacency)
        laplacian = _matrix_difference(degree, adjacency)
        eigenvalues, _ = eig(laplacian)
        return sorted(mp.re(value) for value in eigenvalues)

def compute_laplacian_lambda_2(eigenvalues: List[mp.mpf]) -> mp.mpf:
    """Return the algebraic connectivity (Fiedler value) as a purely structural diagnostic."""
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        for value in eigenvalues:
            if value > mp.mpf("1e-14"):
                return value
        return mp.mpf(0)

def random_walk_return_probabilities(state: RelationalState, max_steps: int) -> List[mp.mpf]:
    """Compute the return probability trace for random walks."""
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        n = state.distinction_count()
        if n == 0:
            return []
        adjacency = _get_adjacency_matrix(state)
        degree = _get_degree_matrix(state, adjacency)

        transition = matrix(n, n)
        for i in range(n):
            node_degree = degree[i, i]
            if node_degree > 0:
                for j in range(n):
                    transition[i, j] = mp.fdiv(adjacency[i, j], node_degree)

        probabilities = []
        transition_power = matrix(n, n)
        for i in range(n):
            transition_power[i, i] = mp.mpf(1)

        for _ in range(1, max_steps + 1):
            transition_power = _matrix_product(transition_power, transition)
            trace = mp.fsum(transition_power[i, i] for i in range(n))
            probabilities.append(mp.fdiv(trace, mp.mpf(n)))
        return probabilities

def log_slope_diagnostic(return_probs: List[mp.mpf], window_start: int, window_end: int) -> mp.mpf:
    """Compute the log-log slope of the return probability trace."""
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        if window_end >= len(return_probs):
            window_end = len(return_probs) - 1
        if window_start >= window_end or window_start < 0:
            return mp.mpf(0)

        x1 = mp.mpf(window_start + 1)
        x2 = mp.mpf(window_end + 1)
        y1 = return_probs[window_start]
        y2 = return_probs[window_end]

        if y1 <= 0 or y2 <= 0:
            return mp.mpf(0)

        numerator = mp.fsub(log(y2), log(y1))
        denominator = mp.fsub(log(x2), log(x1))
        return mp.fdiv(numerator, denominator)
