"""Auxiliary functions for genome alignment objects."""

from typing import List, Tuple, Optional


def sort_alignments_by_score(alignments_collection, max_elems: Optional[int] = None) -> List[Tuple[int, int]]:
    # Create list of (chain_id, score) tuples
    score_tuples = [(alignment.chain_id, alignment.score) for alignment in alignments_collection.alignments]
    
    # Sort by score in descending order (highest scores first)
    sorted_tuples = sorted(score_tuples, key=lambda x: x[1], reverse=True)
    
    # Trim to max_elems if specified
    if max_elems is not None:
        sorted_tuples = sorted_tuples[:max_elems]
    
    return sorted_tuples
