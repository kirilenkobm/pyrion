"""Chain alignment operations for projecting genomic intervals."""

from typing import List, Optional, Tuple, Dict
import numpy as np

from .. import GenomeAlignment, Transcript
from ..config import HAS_NUMBA, njit
from ..core.intervals import GenomicInterval
from ..core.strand import Strand


def project_intervals_through_chain(
    intervals: np.ndarray,
    chain_blocks: np.ndarray,
    q_strand: int = 1,
) -> List[np.ndarray]:
    if len(intervals) == 0:
        return []
    if len(chain_blocks) == 0:
        return [np.array([[0, 0]], dtype=np.int64) for _ in range(len(intervals))]
    return _project_intervals_vectorized(intervals, chain_blocks, q_strand)


def project_intervals_through_chain_strict(
    intervals: np.ndarray,
    chain_blocks: np.ndarray,
    q_strand: int = 1,
    max_gap_ratio: float = 1.0,
) -> List[np.ndarray]:
    """Stricter projection that respects alignment structure and deletions.

    Logic:
    1. If interval overlaps aligned blocks:
       - For each terminus (start/end):
         * If in aligned block: project directly
         * If in misaligned region: extend from nearest internal block, BUT limited by
           actual query sequence length between blocks (handles deletions)
         * If in deletion: don't extend, use closest internal block boundary

    2. If interval is fully within deletion: return [[0, 0]]

    3. If interval has no overlapping blocks (complete misalignment):
       - Find flanking blocks (before and after)
       - If query distance between flanks <= max_gap_ratio * target interval length:
         return that query interval
       - Otherwise: return [[0, 0]]

    Args:
        intervals: Array of intervals to project, shape (N, 2)
        chain_blocks: Chain alignment blocks, shape (M, 4) with [t_start, t_end, q_start, q_end]
        q_strand: Query strand (1 for plus, -1 for minus). For minus-strand chains,
            within-block projection direction is reversed (anti-parallel alignment).
        max_gap_ratio: When an interval falls entirely in a misaligned gap, accept it
            if query_distance <= max_gap_ratio * interval_length. Default 1.0 (strict:
            query gap must not exceed reference interval). Use higher values (e.g. 25.0)
            for liftover of flanked regions where query expansion is expected.

    Returns:
        List of projected intervals. Returns [[0, 0]] if interval can't be reliably projected.
    """
    if len(intervals) == 0:
        return []
    if len(chain_blocks) == 0:
        return [np.array([[0, 0]], dtype=np.int64) for _ in range(len(intervals))]

    if HAS_NUMBA:
        return _project_intervals_strict_numba(intervals, chain_blocks, q_strand, max_gap_ratio)
    else:
        return _project_intervals_strict_numpy(intervals, chain_blocks, q_strand, max_gap_ratio)


def _project_intervals_vectorized(intervals: np.ndarray, chain_blocks: np.ndarray, q_strand: int = 1) -> List[np.ndarray]:
    if HAS_NUMBA:
        return _project_intervals_numba(intervals, chain_blocks, q_strand)
    else:
        return _project_intervals_numpy(intervals, chain_blocks, q_strand)


@njit
def _project_intervals_numba(intervals: np.ndarray, chain_blocks: np.ndarray, q_strand: int = 1) -> List[np.ndarray]:
    results = []
    is_minus = (q_strand == -1)
    
    t_starts = chain_blocks[:, 0]
    t_ends = chain_blocks[:, 1]
    q_starts = chain_blocks[:, 2] 
    q_ends = chain_blocks[:, 3]
    
    chain_q_start = q_starts.min()
    chain_q_end = q_ends.max()
    
    for i in range(len(intervals)):
        interval_start, interval_end = intervals[i, 0], intervals[i, 1]
        first_possible_idx = np.searchsorted(t_ends, interval_start, side='right')
        last_possible_idx = np.searchsorted(t_starts, interval_end, side='right') - 1
        
        first_overlap_idx = -1
        last_overlap_idx = -1
        
        for block_idx in range(max(0, first_possible_idx), min(len(chain_blocks), last_possible_idx + 1)):
            t_start, t_end = t_starts[block_idx], t_ends[block_idx]
            
            if t_end > interval_start and t_start < interval_end:
                if first_overlap_idx == -1:
                    first_overlap_idx = block_idx
                last_overlap_idx = block_idx
        
        if first_overlap_idx != -1:
            if is_minus:
                projected_start = q_ends[first_overlap_idx] - (interval_start - t_starts[first_overlap_idx])
                projected_end = q_ends[last_overlap_idx] - (interval_end - t_starts[last_overlap_idx])
            else:
                projected_start = q_starts[first_overlap_idx] + (interval_start - t_starts[first_overlap_idx])
                projected_end = q_starts[last_overlap_idx] + (interval_end - t_starts[last_overlap_idx])

            projected_start = max(chain_q_start, min(chain_q_end, projected_start))
            projected_end = max(chain_q_start, min(chain_q_end, projected_end))

            if projected_start > projected_end:
                projected_start, projected_end = projected_end, projected_start
            
            results.append(np.array([[projected_start, projected_end]], dtype=np.int64))
        else:
            if first_possible_idx > 0 and first_possible_idx < len(chain_blocks):
                if is_minus:
                    gap_lo = q_ends[first_possible_idx]
                    gap_hi = q_starts[first_possible_idx - 1]
                    if gap_lo > gap_hi:
                        gap_lo, gap_hi = gap_hi, gap_lo
                    results.append(np.array([[gap_lo, gap_hi]], dtype=np.int64))
                else:
                    prev_q_end = q_ends[first_possible_idx - 1]
                    next_q_start = q_starts[first_possible_idx]
                    results.append(np.array([[prev_q_end, next_q_start]], dtype=np.int64))
            else:
                results.append(np.array([[0, 0]], dtype=np.int64))
    
    return results


def _project_intervals_numpy(intervals: np.ndarray, chain_blocks: np.ndarray, q_strand: int = 1) -> List[np.ndarray]:
    """NumPy fallback implementation when numba is not available."""
    results = []
    is_minus = (q_strand == -1)
    
    t_starts = chain_blocks[:, 0]
    t_ends = chain_blocks[:, 1]
    q_starts = chain_blocks[:, 2] 
    q_ends = chain_blocks[:, 3]
    
    chain_q_start = q_starts.min()
    chain_q_end = q_ends.max()
    
    for interval_start, interval_end in intervals:
        first_possible_idx = np.searchsorted(t_ends, interval_start, side='right')
        last_possible_idx = np.searchsorted(t_starts, interval_end, side='right') - 1
        
        first_overlap_idx = None
        last_overlap_idx = None
        
        for block_idx in range(max(0, first_possible_idx), min(len(chain_blocks), last_possible_idx + 1)):
            t_start, t_end = chain_blocks[block_idx, 0], chain_blocks[block_idx, 1]
            
            if t_end > interval_start and t_start < interval_end:
                if first_overlap_idx is None:
                    first_overlap_idx = block_idx
                last_overlap_idx = block_idx
        
        if first_overlap_idx is not None:
            if is_minus:
                projected_start = int(q_ends[first_overlap_idx]) - (interval_start - int(t_starts[first_overlap_idx]))
                projected_end = int(q_ends[last_overlap_idx]) - (interval_end - int(t_starts[last_overlap_idx]))
            else:
                projected_start = int(q_starts[first_overlap_idx]) + (interval_start - int(t_starts[first_overlap_idx]))
                projected_end = int(q_starts[last_overlap_idx]) + (interval_end - int(t_starts[last_overlap_idx]))
            
            projected_start = max(chain_q_start, min(chain_q_end, projected_start))
            projected_end = max(chain_q_start, min(chain_q_end, projected_end))
            
            if projected_start > projected_end:
                projected_start, projected_end = projected_end, projected_start
            
            results.append(np.array([[projected_start, projected_end]], dtype=np.int64))
        else:
            if first_possible_idx > 0 and first_possible_idx < len(chain_blocks):
                if is_minus:
                    gap_lo = int(q_ends[first_possible_idx])
                    gap_hi = int(q_starts[first_possible_idx - 1])
                    if gap_lo > gap_hi:
                        gap_lo, gap_hi = gap_hi, gap_lo
                    results.append(np.array([[gap_lo, gap_hi]], dtype=np.int64))
                else:
                    prev_q_end = q_ends[first_possible_idx - 1]
                    next_q_start = q_starts[first_possible_idx]
                    results.append(np.array([[prev_q_end, next_q_start]], dtype=np.int64))
            else:
                results.append(np.array([[0, 0]], dtype=np.int64))
    
    return results


@njit
def _project_intervals_strict_numba(
    intervals: np.ndarray,
    chain_blocks: np.ndarray,
    q_strand: int = 1,
    max_gap_ratio: float = 1.0,
) -> List[np.ndarray]:
    """Strict projection respecting alignment structure and query strand."""
    results = []
    is_minus = (q_strand == -1)

    t_starts = chain_blocks[:, 0]
    t_ends = chain_blocks[:, 1]
    q_starts = chain_blocks[:, 2]
    q_ends = chain_blocks[:, 3]

    for i in range(len(intervals)):
        interval_start, interval_end = intervals[i, 0], intervals[i, 1]
        interval_length = interval_end - interval_start

        overlapping_idxs = []
        for block_idx in range(len(chain_blocks)):
            if t_ends[block_idx] > interval_start and t_starts[block_idx] < interval_end:
                overlapping_idxs.append(block_idx)

        if len(overlapping_idxs) > 0:
            first_block_idx = overlapping_idxs[0]
            last_block_idx = overlapping_idxs[-1]

            # --- Project start coordinate ---
            if interval_start >= t_starts[first_block_idx] and interval_start < t_ends[first_block_idx]:
                t_offset = interval_start - t_starts[first_block_idx]
                t_len = t_ends[first_block_idx] - t_starts[first_block_idx]
                q_len = q_ends[first_block_idx] - q_starts[first_block_idx]
                if is_minus:
                    q_start = q_ends[first_block_idx] - int((t_offset / t_len) * q_len)
                else:
                    q_start = q_starts[first_block_idx] + int((t_offset / t_len) * q_len)
            else:
                extension_needed = t_starts[first_block_idx] - interval_start
                if is_minus:
                    # Minus strand: t_start of block maps to q_end; extend upward from q_end
                    if first_block_idx > 0:
                        available_query_space = q_starts[first_block_idx - 1] - q_ends[first_block_idx]
                        if available_query_space < 0:
                            available_query_space = 0
                        extension = min(extension_needed, available_query_space)
                        q_start = q_ends[first_block_idx] + extension
                    else:
                        q_start = q_ends[first_block_idx]
                else:
                    if first_block_idx > 0:
                        available_query_space = q_starts[first_block_idx] - q_ends[first_block_idx - 1]
                        extension = min(extension_needed, available_query_space)
                        q_start = q_starts[first_block_idx] - extension
                    else:
                        q_start = q_starts[first_block_idx]

            # --- Project end coordinate ---
            if interval_end > t_starts[last_block_idx] and interval_end <= t_ends[last_block_idx]:
                t_offset = interval_end - t_starts[last_block_idx]
                t_len = t_ends[last_block_idx] - t_starts[last_block_idx]
                q_len = q_ends[last_block_idx] - q_starts[last_block_idx]
                if is_minus:
                    q_end = q_ends[last_block_idx] - int((t_offset / t_len) * q_len)
                else:
                    q_end = q_starts[last_block_idx] + int((t_offset / t_len) * q_len)
            else:
                extension_needed = interval_end - t_ends[last_block_idx]
                if is_minus:
                    # Minus strand: t_end of block maps to q_start; extend downward from q_start
                    if last_block_idx < len(chain_blocks) - 1:
                        available_query_space = q_starts[last_block_idx] - q_ends[last_block_idx + 1]
                        if available_query_space < 0:
                            available_query_space = 0
                        extension = min(extension_needed, available_query_space)
                        q_end = q_starts[last_block_idx] - extension
                    else:
                        q_end = q_starts[last_block_idx]
                else:
                    if last_block_idx < len(chain_blocks) - 1:
                        available_query_space = q_starts[last_block_idx + 1] - q_ends[last_block_idx]
                        extension = min(extension_needed, available_query_space)
                        q_end = q_ends[last_block_idx] + extension
                    else:
                        q_end = q_ends[last_block_idx]

            if q_start > q_end:
                q_start, q_end = q_end, q_start
            results.append(np.array([[q_start, q_end]], dtype=np.int64))

        else:
            left_block_idx = -1
            right_block_idx = -1

            for block_idx in range(len(chain_blocks)):
                if t_ends[block_idx] <= interval_start:
                    left_block_idx = block_idx
                if t_starts[block_idx] >= interval_end and right_block_idx == -1:
                    right_block_idx = block_idx
                    break

            if left_block_idx >= 0 and right_block_idx >= 0:
                if is_minus:
                    # Minus strand: left block (lower t) has higher q; right block has lower q
                    q_flank_start = q_ends[right_block_idx]
                    q_flank_end = q_starts[left_block_idx]
                else:
                    q_flank_start = q_ends[left_block_idx]
                    q_flank_end = q_starts[right_block_idx]
                query_distance = abs(q_flank_end - q_flank_start)

                if query_distance <= interval_length * max_gap_ratio:
                    if q_flank_start > q_flank_end:
                        q_flank_start, q_flank_end = q_flank_end, q_flank_start
                    results.append(np.array([[q_flank_start, q_flank_end]], dtype=np.int64))
                else:
                    results.append(np.array([[0, 0]], dtype=np.int64))
            else:
                results.append(np.array([[0, 0]], dtype=np.int64))

    return results


def _project_intervals_strict_numpy(
    intervals: np.ndarray,
    chain_blocks: np.ndarray,
    q_strand: int = 1,
    max_gap_ratio: float = 1.0,
) -> List[np.ndarray]:
    """NumPy fallback for strict projection."""
    results = []
    is_minus = (q_strand == -1)

    t_starts = chain_blocks[:, 0]
    t_ends = chain_blocks[:, 1]
    q_starts = chain_blocks[:, 2]
    q_ends = chain_blocks[:, 3]

    for interval_start, interval_end in intervals:
        interval_length = interval_end - interval_start

        overlapping_idxs = []
        for block_idx in range(len(chain_blocks)):
            if t_ends[block_idx] > interval_start and t_starts[block_idx] < interval_end:
                overlapping_idxs.append(block_idx)

        if len(overlapping_idxs) > 0:
            first_block_idx = overlapping_idxs[0]
            last_block_idx = overlapping_idxs[-1]

            # --- Project start coordinate ---
            if interval_start >= t_starts[first_block_idx] and interval_start < t_ends[first_block_idx]:
                t_offset = interval_start - t_starts[first_block_idx]
                t_len = t_ends[first_block_idx] - t_starts[first_block_idx]
                q_len = q_ends[first_block_idx] - q_starts[first_block_idx]
                if is_minus:
                    q_start = int(q_ends[first_block_idx]) - int((t_offset / t_len) * q_len)
                else:
                    q_start = int(q_starts[first_block_idx]) + int((t_offset / t_len) * q_len)
            else:
                extension_needed = int(t_starts[first_block_idx]) - interval_start
                if is_minus:
                    if first_block_idx > 0:
                        available_query_space = int(q_starts[first_block_idx - 1]) - int(q_ends[first_block_idx])
                        if available_query_space < 0:
                            available_query_space = 0
                        extension = min(extension_needed, available_query_space)
                        q_start = int(q_ends[first_block_idx]) + extension
                    else:
                        q_start = int(q_ends[first_block_idx])
                else:
                    if first_block_idx > 0:
                        available_query_space = int(q_starts[first_block_idx]) - int(q_ends[first_block_idx - 1])
                        extension = min(extension_needed, available_query_space)
                        q_start = int(q_starts[first_block_idx]) - extension
                    else:
                        q_start = int(q_starts[first_block_idx])

            # --- Project end coordinate ---
            if interval_end > t_starts[last_block_idx] and interval_end <= t_ends[last_block_idx]:
                t_offset = interval_end - t_starts[last_block_idx]
                t_len = t_ends[last_block_idx] - t_starts[last_block_idx]
                q_len = q_ends[last_block_idx] - q_starts[last_block_idx]
                if is_minus:
                    q_end = int(q_ends[last_block_idx]) - int((t_offset / t_len) * q_len)
                else:
                    q_end = int(q_starts[last_block_idx]) + int((t_offset / t_len) * q_len)
            else:
                extension_needed = interval_end - int(t_ends[last_block_idx])
                if is_minus:
                    if last_block_idx < len(chain_blocks) - 1:
                        available_query_space = int(q_starts[last_block_idx]) - int(q_ends[last_block_idx + 1])
                        if available_query_space < 0:
                            available_query_space = 0
                        extension = min(extension_needed, available_query_space)
                        q_end = int(q_starts[last_block_idx]) - extension
                    else:
                        q_end = int(q_starts[last_block_idx])
                else:
                    if last_block_idx < len(chain_blocks) - 1:
                        available_query_space = int(q_starts[last_block_idx + 1]) - int(q_ends[last_block_idx])
                        extension = min(extension_needed, available_query_space)
                        q_end = int(q_ends[last_block_idx]) + extension
                    else:
                        q_end = int(q_ends[last_block_idx])

            if q_start > q_end:
                q_start, q_end = q_end, q_start
            results.append(np.array([[q_start, q_end]], dtype=np.int64))

        else:
            left_block_idx = -1
            right_block_idx = -1

            for block_idx in range(len(chain_blocks)):
                if t_ends[block_idx] <= interval_start:
                    left_block_idx = block_idx
                if t_starts[block_idx] >= interval_end and right_block_idx == -1:
                    right_block_idx = block_idx
                    break

            if left_block_idx >= 0 and right_block_idx >= 0:
                if is_minus:
                    q_flank_start = int(q_ends[right_block_idx])
                    q_flank_end = int(q_starts[left_block_idx])
                else:
                    q_flank_start = int(q_ends[left_block_idx])
                    q_flank_end = int(q_starts[right_block_idx])
                query_distance = abs(q_flank_end - q_flank_start)

                if query_distance <= interval_length * max_gap_ratio:
                    if q_flank_start > q_flank_end:
                        q_flank_start, q_flank_end = q_flank_end, q_flank_start
                    results.append(np.array([[q_flank_start, q_flank_end]], dtype=np.int64))
                else:
                    results.append(np.array([[0, 0]], dtype=np.int64))
            else:
                results.append(np.array([[0, 0]], dtype=np.int64))

    return results


def project_intervals_through_genome_alignment(
    intervals: np.ndarray,
    genome_alignment
) -> List[np.ndarray]:
    """Convenience function to project intervals through a GenomeAlignment object."""
    return project_intervals_through_chain(
        intervals=intervals,
        chain_blocks=genome_alignment.blocks,
        q_strand=genome_alignment.q_strand,
    )


def project_intervals_through_genome_alignment_to_intervals(
    intervals: np.ndarray,
    genome_alignment,
    target_chrom: Optional[str] = None,
    target_strand: Optional[Strand] = None
) -> List[GenomicInterval]:
    """Project intervals through genome alignment and convert to GenomicInterval objects.
    
    Args:
        intervals: Array of intervals to project, shape (N, 2)
        genome_alignment: GenomeAlignment object to project through
        target_chrom: Target chromosome name (auto-detected if None)
        target_strand: Target strand (auto-detected if None)

    """
    if target_chrom is None:
        target_chrom = genome_alignment.q_chrom
    if target_strand is None:
        target_strand = Strand.from_int(genome_alignment.q_strand)
    
    projected_arrays = project_intervals_through_genome_alignment(intervals, genome_alignment)
    
    return [
        GenomicInterval(target_chrom, int(array[0][0]), int(array[0][1]), target_strand)
        for array in projected_arrays 
        if len(array) > 0 and not (array[0][0] == 0 and array[0][1] == 0)
    ]


def project_transcript_through_chain(transcript: Transcript, chain: GenomeAlignment, only_cds=False) -> Optional[GenomicInterval]:
    if only_cds:
        arr = np.array([[transcript.cds_start, transcript.cds_end]])
    else:
        arr = np.array([transcript.transcript_span])
    projection = project_intervals_through_genome_alignment(arr, chain)
    if len(projection) == 0:
        return None
    else:
        return GenomicInterval(
            chrom=chain.q_chrom,
            start=int(projection[0][0][0]),
            end=int(projection[0][0][1]),
            strand=Strand.from_int(chain.t_strand),
            id=f"chain_{chain.chain_id}_transcript_{transcript.id}"
        )

def get_chain_target_interval(genome_alignment) -> GenomicInterval:
    if genome_alignment is None:
        raise ValueError("get_chain_target_interval: for some reason, provided genome_alignment object is None")

    if len(genome_alignment.blocks) == 0:
        raise ValueError("Chain has no blocks")
    
    start = int(genome_alignment.blocks[0, 0])
    end = int(genome_alignment.blocks[-1, 1])
    
    strand = Strand.from_int(genome_alignment.t_strand)
    chrom = genome_alignment.t_chrom
    if isinstance(chrom, bytes):
        chrom = chrom.decode('utf-8')
    
    return GenomicInterval(
        chrom=chrom,
        start=start,
        end=end,
        strand=strand,
        id=f"chain_{genome_alignment.chain_id}_target"
    )


def get_chain_query_interval(genome_alignment) -> GenomicInterval:
    if len(genome_alignment.blocks) == 0:
        raise ValueError("Chain has no blocks")
    
    start = int(genome_alignment.blocks[0, 2])
    end = int(genome_alignment.blocks[-1, 3])
    
    strand = Strand.from_int(genome_alignment.q_strand)
    return GenomicInterval(
        chrom=genome_alignment.q_chrom,
        start=start,
        end=end,
        strand=strand,
        id=f"chain_{genome_alignment.chain_id}_query"
    )


def get_chain_t_start(genome_alignment) -> int:
    if len(genome_alignment.blocks) == 0:
        raise ValueError("Chain has no blocks")
    
    return int(genome_alignment.blocks[0, 0])


def get_chain_t_end(genome_alignment) -> int:
    if len(genome_alignment.blocks) == 0:
        raise ValueError("Chain has no blocks")
    
    return int(genome_alignment.blocks[-1, 1])


def get_chain_q_start(genome_alignment) -> int:
    if len(genome_alignment.blocks) == 0:
        raise ValueError("Chain has no blocks")
    
    return int(genome_alignment.blocks[0, 2])


def get_chain_q_end(genome_alignment) -> int:
    if len(genome_alignment.blocks) == 0:
        raise ValueError("Chain has no blocks")
    
    return int(genome_alignment.blocks[-1, 3])


def split_genome_alignment(
    chain: GenomeAlignment,
    intersected_transcripts: List[Transcript],
    window_size: int = 1_000_000,
    intergenic_margin: int = 10_000,
) -> Tuple[List[GenomeAlignment], Dict[int, List[str]]]:

    t_start, t_end = chain.blocks[:, 0].min(), chain.blocks[:, 1].max()
    chain_length = t_end - t_start

    if chain_length < window_size * 1.5:
        return [GenomeAlignment(**{**chain.__dict__, "child_id": 0})], {0: [t.id for t in intersected_transcripts]}

    transcript_spans = np.array([
        [tr.blocks[0, 0], tr.blocks[-1, 1]]
        for tr in intersected_transcripts if tr.blocks.size > 0
    ], dtype=int)

    if transcript_spans.size == 0:
        cut_points = list(range(t_start + window_size, t_end, window_size))
    else:
        transcript_spans = transcript_spans[np.argsort(transcript_spans[:, 0])]
        gaps = []
        for i in range(len(transcript_spans) - 1):
            gap_start, gap_end = transcript_spans[i, 1], transcript_spans[i + 1, 0]
            if gap_end - gap_start >= intergenic_margin:
                gaps.append((gap_start + gap_end) // 2)

        cut_points = []
        current = t_start
        while current + window_size < t_end:
            target = current + window_size
            nearby = [g for g in gaps if abs(g - target) < window_size // 2]
            if nearby:
                best = min(nearby, key=lambda g: abs(g - target))
                cut_points.append(best)
                current = best
            else:
                cut_points.append(target)
                current = target

    boundaries = [t_start] + cut_points + [t_end]
    subchains = []
    transcript_mapping = {}

    for i, (start, end) in enumerate(zip(boundaries[:-1], boundaries[1:])):
        block_mask = (chain.blocks[:, 1] > start) & (chain.blocks[:, 0] < end)
        block_idxs = np.where(block_mask)[0]
        if len(block_idxs) == 0:
            continue

        new_blocks = chain.blocks[block_idxs].copy()
        new_blocks[:, 0] = np.clip(new_blocks[:, 0], start, end)
        new_blocks[:, 1] = np.clip(new_blocks[:, 1], start, end)

        for j, orig_idx in enumerate(block_idxs):
            t0, t1, q0, q1 = chain.blocks[orig_idx]
            t_start_new, t_end_new = new_blocks[j, 0], new_blocks[j, 1]
            if t1 > t0:
                ratio_start = (t_start_new - t0) / (t1 - t0)
                ratio_end = (t_end_new - t0) / (t1 - t0)
                q_len = q1 - q0
                new_blocks[j, 2] = q0 + int(ratio_start * q_len)
                new_blocks[j, 3] = q0 + int(ratio_end * q_len)

        subchains.append(GenomeAlignment(
            chain_id=chain.chain_id,
            score=-1,
            t_chrom=chain.t_chrom,
            t_strand=chain.t_strand,
            q_chrom=chain.q_chrom,
            q_strand=chain.q_strand,
            blocks=new_blocks,
            child_id=i,
            t_size=chain.t_size,
            q_size=chain.q_size,
        ))

        overlapping_transcripts = [
            tr.id for tr in intersected_transcripts
            if tr.blocks.size > 0 and not (tr.blocks[-1, 1] <= start or tr.blocks[0, 0] >= end)
        ]
        transcript_mapping[i] = overlapping_transcripts

    return subchains, transcript_mapping
