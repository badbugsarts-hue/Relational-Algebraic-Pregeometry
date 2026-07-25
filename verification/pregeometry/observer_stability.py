"""Observer stability tests for PR-2 diagnostics.

Status: [D] purely for software verification.
"""

from mpmath import mp
import random
from typing import List
from verification.pregeometry.primitives import DistinctionID, Relation, RelationalState
from verification.pregeometry.spectral_diagnostics import combinatorial_laplacian_spectrum

def _permute_state(state: RelationalState, seed: int) -> RelationalState:
    """Relabel nodes using a random permutation to verify ordering invariance."""
    n = state.distinction_count()
    if n == 0:
        return state
        
    rng = random.Random(seed)
    labels = list(range(n))
    rng.shuffle(labels)
    
    relations = tuple(
        Relation(
            DistinctionID(labels[relation.source.value]),
            DistinctionID(labels[relation.target.value]),
            directed=relation.directed,
            weight=relation.weight,
        )
        for relation in state.relations
    )
    return RelationalState(
        distinctions=tuple(DistinctionID(index) for index in range(n)),
        relations=relations,
    )

def verify_relabeling_invariance(state: RelationalState, seed: int = 42) -> bool:
    """Verify that spectral graph diagnostics are invariant under node relabeling."""
    with mp.workdps(80):
        base_spectrum = combinatorial_laplacian_spectrum(state)
        permuted_state = _permute_state(state, seed)
        permuted_spectrum = combinatorial_laplacian_spectrum(permuted_state)

        if len(base_spectrum) != len(permuted_spectrum):
            return False

        for base, permuted in zip(base_spectrum, permuted_spectrum):
            residual = mp.fabs(mp.fsub(base, permuted))
            if residual > mp.mpf("1e-14"):
                return False

        return True
