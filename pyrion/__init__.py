"""
Pyrion: A Fast and Efficient Bioinformatics Library for Genomic Data Processing
"""

# Import version from the single source of truth
from ._version import __version__, __version_info__, __author__, __github__, __license__, __copyright__

# Configuration system
from .config import (
    get_available_cores, get_max_cores, set_max_cores,
    get_min_items_for_parallel, set_min_items_for_parallel,
    disable_parallel, enable_parallel, is_multiprocessing_available,
    get_config_summary, set_loglevel
)

# Core data structures
from .core import (
    GenomicInterval, GenomicIntervalsCollection,
    Transcript, TranscriptsCollection, Gene, GeneData,
    NucleotideSequence, AminoAcidSequence,
    GenomeAlignment, GenomeAlignmentsCollection,
)

# Type system
from .core_types import Strand, ExonType, ChainBlockArray, BlockArray, Metadata

# Sequence types and translation
from .core.nucleotide_sequences import SequenceType
from .core.fai import FaiEntry, FaiStore
from .core.translation import TranslationTable

# I/O operations
from .io import (
    # BED format
    read_bed12_file, read_narrow_bed_file,
    # Chain format
    read_chain_file,
    # GTF format
    read_gtf,
    # 2bit format  
    TwoBitAccessor,
    # Gene data
    read_gene_data,
    # FASTA format
    read_fasta, write_fasta, read_dna_fasta, read_rna_fasta, FastaAccessor,
    # FASTA indexing
    create_fasta_index, load_fasta_index, get_or_create_fasta_index
)

# Visualization is now imported on-demand:
# from pyrion.visualization import VisualizationWindow, visualize_intervals, etc.

# Operations
# from .ops import (
#
# )

__all__ = [
    # Version info
    "__version__", "__version_info__", "__author__", "__github__",
    
    # Core types
    "Strand", "ExonType", "GenomicInterval", "Metadata", "BlockArray", "ChainBlockArray",
    
    # Sequences
    "NucleotideSequence", "SequenceType",
    
    # FASTA indexing
    "FaiEntry", "FaiStore",
    
    # Genes and annotations
    "Transcript", "TranscriptsCollection", "Gene", "GeneData",
    
    # Alignment chains
    "GenomeAlignment", "GenomeAlignmentsCollection",
    
    # I/O functions
    "read_bed12_file", "read_narrow_bed_file",
    "read_chain_file",
    "read_gtf",
    "read_gene_data",
    "TwoBitAccessor",
    "read_fasta", "write_fasta", "read_dna_fasta", "read_rna_fasta", "FastaAccessor",
    "create_fasta_index", "load_fasta_index", "get_or_create_fasta_index",

    # Operations
    
    # Translation
    "TranslationTable",
    
    # Configuration
    "get_available_cores", "get_max_cores", "set_max_cores",
    "get_min_items_for_parallel", "set_min_items_for_parallel", 
    "disable_parallel", "enable_parallel", "is_multiprocessing_available",
    "get_config_summary", "set_loglevel",
    
    # Utilities
    "quick_start", "get_version", "get_version_info"
]


def get_version():
    """Get pyrion version."""
    return __version__


def get_version_info():
    """Get pyrion version as tuple."""
    return __version_info__


def cite():
    """Get citation information."""
    return {
        "software": "Pyrion",
        "version": __version__,
        "description": "A fast and efficient bioinformatics library for genomic data processing",
        "author": __author__,
        "license": __license__,
        "design_principles": [
            "Memory-efficient numpy-based storage",
            "Lazy evaluation and caching", 
            "Separation of data and operations",
            "Minimal dependencies",
            "Zero-cost abstractions"
        ]
    }


def quick_start():
    guide = f"""
    Pyrion Quick Start Guide (v{__version__})
    =======================================

    # Import main components
    from pyrion import (
        GenomicInterval, Strand, NucleotideSequence,
        TwoBitAccessor, read_bed12_file, read_chain_file,
    )
    from pyrion.ops import (
        merge_intervals, intersect_intervals,
        extract_cds_sequence, project_transcript_through_chain,
    )

    # Read transcripts from BED12
    transcripts = read_bed12_file("annotations.bed")
    t = transcripts.get_by_id("ENST00000456328")

    # Work with sequences
    seq = NucleotideSequence.from_string("ATGAAATAG")
    rc = seq.reverse_complement()
    protein = seq.to_amino_acids()

    # Genomic intervals
    iv = GenomicInterval("chr1", 1000, 2000, Strand.PLUS)
    iv2 = GenomicInterval("chr1", 1500, 2500, Strand.PLUS)
    print(iv.intersects(iv2))  # True
    print(iv.overlap(iv2))     # 500

    # Access genome sequences
    genome = TwoBitAccessor("genome.2bit")
    region_seq = genome.fetch("chr1", 1000, 2000)
    genome.close()

    # Extract CDS sequence from a transcript
    cds_seq = extract_cds_sequence(t, genome)

    # Liftover via chain
    chains = read_chain_file("hg38ToMm39.chain")
    chain = chains.get_by_chain_id(1)
    projected = project_transcript_through_chain(t, chain)

    For detailed documentation, see docs/quickstart.md
    """
    print(guide)
