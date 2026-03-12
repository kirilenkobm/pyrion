"""Data transformation utilities for converting between different genomic data types."""

from dataclasses import replace
from typing import Callable, Dict, List, Optional, Union

import numpy as np

from ..core.intervals import GenomicInterval
from ..core.genes import Transcript, TranscriptsCollection


def intervals_to_transcripts(
    intervals: List[GenomicInterval], 
    source_file: Optional[str] = None
) -> TranscriptsCollection:
    """Convert a list of GenomicInterval objects to a TranscriptsCollection.

    May be helpful if bed-6 formatted data is needed as is was bed-12.
    """
    transcripts = []
    
    for i, interval in enumerate(intervals):
        # Use interval ID if available, otherwise generate one
        transcript_id = interval.id if interval.id is not None else f"interval_{i+1}"
        blocks = np.array([[interval.start, interval.end]], dtype=np.int32)
        
        transcript = Transcript(
            id=transcript_id,
            chrom=interval.chrom,
            strand=interval.strand,
            blocks=blocks,
            cds_start=interval.start,
            cds_end=interval.end
        )
        
        transcripts.append(transcript)
    
    return TranscriptsCollection(transcripts=transcripts, source_file=source_file)


def bed_to_transcripts(bed_file_path: str) -> TranscriptsCollection:
    from ..io import read_narrow_bed_file
    
    intervals = read_narrow_bed_file(bed_file_path)
    return intervals_to_transcripts(intervals, source_file=bed_file_path)


def remap_transcript_ids(
    collection: TranscriptsCollection,
    id_mapping: Union[Dict[str, str], Callable[[str], str]],
    source_file: Optional[str] = None,
) -> TranscriptsCollection:
    """Build a new TranscriptsCollection with the same transcripts but new IDs.

    Transcript IDs are immutable (Transcript is a frozen dataclass), so this
    creates new Transcript instances that are copies except for the id field,
    and returns a new collection containing them.

    Args:
        collection: The source TranscriptsCollection.
        id_mapping: Either a dict (old_id -> new_id) or a callable that takes
            the old transcript id and returns the new one.
        source_file: Optional source_file for the new collection. If None,
            the original collection's source_file is not carried over.

    Returns:
        A new TranscriptsCollection with the same transcripts and remapped IDs.

    Example:
        # Prefix every ID
        new_coll = remap_transcript_ids(coll, lambda tid: f"custom_{tid}")

        # Explicit mapping
        new_coll = remap_transcript_ids(coll, {"ENST1": "my_ENST1", "ENST2": "my_ENST2"})
    """
    if callable(id_mapping):
        new_transcripts = [
            replace(t, id=id_mapping(t.id)) for t in collection.transcripts
        ]
    else:
        new_transcripts = [
            replace(t, id=id_mapping.get(t.id, t.id)) for t in collection.transcripts
        ]
    out_source = source_file if source_file is not None else collection.source_file
    return TranscriptsCollection(transcripts=new_transcripts, source_file=out_source)
