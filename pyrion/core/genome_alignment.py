from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional, Dict, Union, Tuple
import numpy as np
from pathlib import Path

from pyrion.core.strand import Strand


@dataclass(frozen=True)
class GenomeAlignment:
    chain_id: int
    score: int
    t_chrom: str
    t_strand: int
    t_size: int
    q_chrom: str
    q_strand: int
    q_size: int
    blocks: np.ndarray             # Shape (N, 4) -- [[t_start, t_end, q_start, q_end], ...]
    child_id: Optional[int] = None  # For sub-chains (None for original chains)

    @cached_property
    def t_span(self) -> np.ndarray:
        return np.array([self.blocks[0][0], self.blocks[-1][1]], dtype=np.int32)

    @cached_property
    def q_span(self) -> np.ndarray:
        if self.q_strand == -1:
            # For negative strand, coordinates are reversed: first block has highest, last block has lowest
            return np.array([self.blocks[-1][2], self.blocks[0][3]], dtype=np.int32)
        else:
            # For positive strand, use first block start and last block end as before
            return np.array([self.blocks[0][2], self.blocks[-1][3]], dtype=np.int32)

    def __repr__(self) -> str:
        t_strand_str = Strand.from_int(self.t_strand).to_char()
        q_strand_str = Strand.from_int(self.q_strand).to_char()
        
        # Get target and query spans
        t_start, t_end = self.t_span
        q_start, q_end = self.q_span
        
        return (f"GenomeAlignment(id={self.chain_id}, score={self.score:,}, "
                f"T={self.t_chrom}:{t_start:,}-{t_end:,}:{t_strand_str} -> "
                f"Q={self.q_chrom}:{q_start:,}-{q_end:,}:{q_strand_str}, "
                f"{len(self.blocks)} blocks)")

    def aligned_length(self) -> int:
        if len(self.blocks) == 0:
            return 0
        return int(np.sum(self.blocks[:, 1] - self.blocks[:, 0]))

    def t_length(self) -> int:
        return int(self.t_span[1] - self.t_span[0])

    def q_length(self) -> int:
        return int(self.q_span[1] - self.q_span[0])

    def blocks_in_target(self) -> np.ndarray:
        return self.blocks[:, :2]

    def blocks_in_query(self) -> np.ndarray:
        return self.blocks[:, 2:]

    def __hash__(self):
        return hash((self.chain_id, self.t_chrom, self.t_strand, self.q_chrom, self.q_strand))


class GenomeAlignmentsCollection:
    """Container for many genome alignments."""
    def __init__(
        self,
        alignments: Optional[List[GenomeAlignment]] = None,
        source_file: Optional[str] = None
    ):
        self.alignments: List[GenomeAlignment] = alignments or []
        self.source_file: Optional[str] = source_file

        self._id_index: Optional[Dict[int, int]] = None  # chain_id → index
        self._chrom_index: Optional[Dict[str, List[int]]] = None  # target chrom → indices
        self._query_chrom_index: Optional[Dict[str, List[int]]] = None  # query chrom → indices

    def __len__(self):
        return len(self.alignments)

    def __getitem__(self, idx: int) -> GenomeAlignment:
        return self.alignments[idx]

    def get_by_chain_id(self, chain_id: int) -> Optional[GenomeAlignment]:
        if self._id_index is None:
            self._build_id_index()
        idx = self._id_index.get(chain_id)
        return self.alignments[idx] if idx is not None else None

    def get_by_target_chrom(self, chrom: str) -> List[GenomeAlignment]:
        if self._chrom_index is None:
            self._build_chrom_index()
        indices = self._chrom_index.get(chrom, [])
        return [self.alignments[i] for i in indices]

    def get_by_query_chrom(self, chrom: str) -> List[GenomeAlignment]:
        if self._query_chrom_index is None:
            self._build_query_chrom_index()
        indices = self._query_chrom_index.get(chrom, [])
        return [self.alignments[i] for i in indices]

    def get_reference_chromosomes(self) -> List[str]:
        if self._chrom_index is None:
            self._build_chrom_index()
        return list(self._chrom_index.keys())

    def get_query_chromosomes(self) -> List[str]:
        if self._query_chrom_index is None:
            self._build_query_chrom_index()
        return list(self._query_chrom_index.keys())

    def get_chain_ids_by_target_chrom(self, chrom: str) -> List[int]:
        if self._chrom_index is None:
            self._build_chrom_index()
        indices = self._chrom_index.get(chrom, [])
        return [self.alignments[i].chain_id for i in indices]

    def get_chain_ids_by_query_chrom(self, chrom: str) -> List[int]:
        if self._query_chrom_index is None:
            self._build_query_chrom_index()
        indices = self._query_chrom_index.get(chrom, [])
        return [self.alignments[i].chain_id for i in indices]

    def get_alignments_overlapping_target_interval(self, interval: 'GenomicInterval', include_partial: bool = True) -> List[GenomeAlignment]:
        target_chrom_alignments = self.get_by_target_chrom(interval.chrom)
        
        if not target_chrom_alignments:
            return []
        
        matching = []
        for alignment in target_chrom_alignments:
            # Get target span: [start, end]
            t_start, t_end = alignment.t_span
            
            if include_partial:
                if not (t_end <= interval.start or interval.end <= t_start):
                    matching.append(alignment)
            else:
                if t_start >= interval.start and t_end <= interval.end:
                    matching.append(alignment)
        
        return matching

    def get_alignments_overlapping_query_interval(self, interval: 'GenomicInterval', include_partial: bool = True) -> List[GenomeAlignment]:
        query_chrom_alignments = self.get_by_query_chrom(interval.chrom)
        
        if not query_chrom_alignments:
            return []
        
        # Check overlap on query coordinates
        matching = []
        for alignment in query_chrom_alignments:
            # Get query span: [start, end]  
            q_start, q_end = alignment.q_span
            
            if include_partial:
                # Include if alignment intersects (overlaps) the target interval - even 1nt
                if not (q_end <= interval.start or interval.end <= q_start):
                    matching.append(alignment)
            else:
                # Include only if alignment is fully contained within the target interval
                if q_start >= interval.start and q_end <= interval.end:
                    matching.append(alignment)
        
        return matching

    # Convenience methods with shorter names
    def get_alignments_in_interval(self, interval: 'GenomicInterval', include_partial: bool = True) -> List[GenomeAlignment]:
        return self.get_alignments_overlapping_target_interval(interval, include_partial)
    
    def get_alignments_fully_contained(self, interval: 'GenomicInterval') -> List[GenomeAlignment]:
        return self.get_alignments_overlapping_target_interval(interval, include_partial=False)

    def _build_id_index(self):
        self._id_index = {ga.chain_id: i for i, ga in enumerate(self.alignments)}

    def _build_chrom_index(self):
        from collections import defaultdict
        chrom_index = defaultdict(list)
        for i, ga in enumerate(self.alignments):
            chrom_index[ga.t_chrom].append(i)
        self._chrom_index = dict(chrom_index)

    def _build_query_chrom_index(self):
        from collections import defaultdict
        query_chrom_index = defaultdict(list)
        for i, ga in enumerate(self.alignments):
            query_chrom_index[ga.q_chrom].append(i)
        self._query_chrom_index = dict(query_chrom_index)

    def filter(
        self,
        t_chrom: Optional[Union[str, List[str]]] = None,
        q_chrom: Optional[Union[str, List[str]]] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
        min_aligned_length: Optional[int] = None,
    ) -> 'GenomeAlignmentsCollection':
        """Filter alignments by target/query chromosomes, score, and aligned length.

        All criteria are combined with AND logic. None means no filter on that field.
        Chromosome arguments accept a single string or a list/set of strings.

        Equivalent to UCSC chainFilter:
            chainFilter -t=chr11,chrX -q=chr19,chr7 -minScore=15000 in.chain
        becomes:
            collection.filter(t_chrom=["chr11", "chrX"],
                              q_chrom=["chr19", "chr7"],
                              min_score=15000)
        """
        t_set = None
        if t_chrom is not None:
            t_set = {t_chrom} if isinstance(t_chrom, str) else set(t_chrom)

        q_set = None
        if q_chrom is not None:
            q_set = {q_chrom} if isinstance(q_chrom, str) else set(q_chrom)

        filtered = []
        for a in self.alignments:
            if t_set is not None and a.t_chrom not in t_set:
                continue
            if q_set is not None and a.q_chrom not in q_set:
                continue
            if min_score is not None and a.score < min_score:
                continue
            if max_score is not None and a.score > max_score:
                continue
            if min_aligned_length is not None and a.aligned_length() < min_aligned_length:
                continue
            filtered.append(a)

        return GenomeAlignmentsCollection(
            alignments=filtered,
            source_file=self.source_file,
        )

    _SORT_KEYS = {
        "score": lambda a: a.score,
        "chain_id": lambda a: a.chain_id,
        "t_chrom": lambda a: a.t_chrom,
        "t_start": lambda a: int(a.t_span[0]),
        "q_chrom": lambda a: a.q_chrom,
        "q_start": lambda a: int(a.q_span[0]),
        "aligned_length": lambda a: a.aligned_length(),
    }

    def sort(
        self,
        by: Union[str, List[str]] = "score",
        reverse: bool = False,
    ) -> 'GenomeAlignmentsCollection':
        """Sort alignments in-place and return self for chaining.

        Args:
            by: Sort key(s). A single string or list of strings.
                Predefined presets:
                    "score"    — sort by alignment score  [default]
                    "position" — sort by (t_chrom, t_start)
                Individual keys: "score", "chain_id", "t_chrom", "t_start",
                    "q_chrom", "q_start", "aligned_length".
                Multiple keys: ["t_chrom", "t_start"] sorts by target chrom
                    first, then target start.
            reverse: If True, sort in descending order.
                Tip: use ``reverse=True`` with ``by="score"`` for highest-first.

        Returns:
            self (for chaining, e.g. ``collection.sort("score", reverse=True).save_to_chain(path)``)
        """
        if isinstance(by, str):
            if by == "position":
                keys = ["t_chrom", "t_start"]
            elif by in self._SORT_KEYS:
                keys = [by]
            else:
                raise ValueError(
                    f"Unknown sort key '{by}'. "
                    f"Use one of: {', '.join(sorted(self._SORT_KEYS))} or 'position'."
                )
        else:
            keys = list(by)
            for k in keys:
                if k not in self._SORT_KEYS:
                    raise ValueError(
                        f"Unknown sort key '{k}'. "
                        f"Use one of: {', '.join(sorted(self._SORT_KEYS))}."
                    )

        extractors = [self._SORT_KEYS[k] for k in keys]
        self.alignments.sort(
            key=lambda a: tuple(fn(a) for fn in extractors),
            reverse=reverse,
        )
        self._invalidate_indices()
        return self

    def _invalidate_indices(self):
        self._id_index = None
        self._chrom_index = None
        self._query_chrom_index = None

    def sort_by_score(self, max_elems: Optional[int] = None) -> List[Tuple[int, int]]:
        from .genome_alignment_auxiliary import sort_alignments_by_score
        return sort_alignments_by_score(self, max_elems)

    def summary(self) -> str:
        return f"{len(self.alignments):,} genome alignments from {self.source_file or 'unknown source'}"

    def __str__(self) -> str:
        """String representation with summary."""
        from ..ops.chain_serialization import genome_alignments_collection_summary_string
        return genome_alignments_collection_summary_string(self)

    def __repr__(self) -> str:
        return f"<GenomeAlignmentsCollection: {self.summary()}>"

    def save_to_chain(self, file_path: Union[str, Path]) -> None:
        from ..ops.chain_serialization import save_genome_alignments_collection_to_chain
        save_genome_alignments_collection_to_chain(self, file_path)

    def save_to_json(self, file_path: Union[str, Path]) -> None:
        from ..ops.chain_serialization import save_genome_alignments_collection_to_json
        save_genome_alignments_collection_to_json(self, file_path)

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> 'GenomeAlignmentsCollection':
        from ..ops.chain_serialization import load_genome_alignments_collection_from_json
        return load_genome_alignments_collection_from_json(file_path)
