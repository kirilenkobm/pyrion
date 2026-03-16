"""Test that every symbol documented in CLAUDE.md, AGENTS.md, and __all__ is actually importable.

This test exists to catch drift between documentation and the real public API.
If it fails, either fix the import or update the docs — never leave a phantom export.
"""

import importlib
import pytest


# ── pyrion top-level ──────────────────────────────────────────────────────────

PYRION_ALL_SYMBOLS = [
    "__version__", "__version_info__", "__author__", "__github__",
    "Strand", "ExonType", "GenomicInterval", "Metadata", "BlockArray", "ChainBlockArray",
    "NucleotideSequence", "SequenceType",
    "FaiEntry", "FaiStore",
    "Transcript", "TranscriptsCollection", "Gene", "GeneData",
    "GenomeAlignment", "GenomeAlignmentsCollection",
    "read_bed12_file", "read_narrow_bed_file",
    "read_chain_file",
    "read_gtf",
    "read_gene_data",
    "TwoBitAccessor",
    "read_fasta", "write_fasta", "read_dna_fasta", "read_rna_fasta", "FastaAccessor",
    "create_fasta_index", "load_fasta_index", "get_or_create_fasta_index",
    "TranslationTable",
    "get_available_cores", "get_max_cores", "set_max_cores",
    "get_min_items_for_parallel", "set_min_items_for_parallel",
    "disable_parallel", "enable_parallel", "is_multiprocessing_available",
    "get_config_summary", "set_loglevel",
    "quick_start", "get_version", "get_version_info",
]

PYRION_DOCUMENTED_EXTRAS = [
    "AminoAcidSequence",
    "GenomicIntervalsCollection",
    "Assembly",
    "read_chrom_sizes",
    "write_chrom_sizes",
]


@pytest.mark.parametrize("symbol", PYRION_ALL_SYMBOLS + PYRION_DOCUMENTED_EXTRAS)
def test_pyrion_top_level_importable(symbol):
    """Every symbol in pyrion.__all__ and docs must be importable from pyrion."""
    mod = importlib.import_module("pyrion")
    assert hasattr(mod, symbol), f"pyrion.{symbol} is not importable"


def test_pyrion_all_is_consistent():
    """pyrion.__all__ must not list symbols that aren't actually importable."""
    import pyrion
    for symbol in pyrion.__all__:
        assert hasattr(pyrion, symbol), (
            f"pyrion.__all__ lists '{symbol}' but it is not importable from pyrion"
        )


# ── pyrion.ops ────────────────────────────────────────────────────────────────

PYRION_OPS_ALL_SYMBOLS = [
    "find_intersections", "compute_overlap_size",
    "intervals_to_array", "array_to_intervals",
    "chains_to_arrays", "transcripts_to_arrays",
    "projected_intervals_to_genomic_intervals",
    "project_intervals_through_chain",
    "project_intervals_through_genome_alignment",
    "project_intervals_through_genome_alignment_to_intervals",
    "project_transcript_through_chain",
    "get_chain_target_interval", "get_chain_query_interval",
    "get_chain_t_start", "get_chain_t_end",
    "get_chain_q_start", "get_chain_q_end",
    "split_genome_alignment",
    "merge_transcript_intervals",
    "slice_intervals", "remove_intervals", "invert_intervals",
    "merge_intervals", "intersect_intervals", "subtract_intervals", "intervals_union",
    "merge_close_intervals", "group_intervals_by_proximity", "split_intervals_on_gaps",
    "intersect_collections", "filter_collection", "create_collections_from_mixed_intervals",
    "get_transcript_cds_in_range", "get_transcript_utrs_in_range",
    "get_transcript_introns_in_range",
    "merge_transcript_cds", "merge_transcript_utrs",
    "find_transcript_overlaps", "subtract_transcript_regions",
    "merge_genome_alignments", "find_alignment_gaps", "intersect_alignment_with_intervals",
    "slice_transcript", "get_transcript_introns", "remove_transcript_region",
    "slice_chain_target_space", "slice_chain_query_space", "remove_chain_region_target_space",
    "transcript_to_bed12_string", "transcripts_collection_to_bed12_string",
    "save_transcripts_collection_to_bed12",
    "transcript_to_dict", "transcript_from_dict",
    "transcripts_collection_to_dict", "transcripts_collection_from_dict",
    "save_transcripts_collection_to_json", "load_transcripts_collection_from_json",
    "transcripts_collection_summary_string",
    "genome_alignment_to_chain_string",
    "genome_alignments_collection_to_chain_string",
    "save_genome_alignments_collection_to_chain",
    "genome_alignment_to_dict", "genome_alignment_from_dict",
    "genome_alignments_collection_to_dict", "genome_alignments_collection_from_dict",
    "save_genome_alignments_collection_to_json",
    "load_genome_alignments_collection_from_json",
    "genome_alignments_collection_summary_string",
    "genomic_interval_to_bed6_string", "genomic_intervals_to_bed6_string",
    "save_genomic_intervals_to_bed6",
    "sequence_to_fasta_string",
    "nucleotide_sequence_to_fasta_string",
    "amino_acid_sequence_to_fasta_string",
    "save_nucleotide_sequence_to_fasta",
    "save_amino_acid_sequence_to_fasta",
    "check_data_consistency",
    "intervals_to_transcripts", "bed_to_transcripts", "remap_transcript_ids",
]

PYRION_OPS_DOCUMENTED_EXTRAS = [
    "extract_cds_sequence",
    "extract_exon_sequence",
    "extract_intron_sequence",
]


@pytest.mark.parametrize("symbol", PYRION_OPS_ALL_SYMBOLS + PYRION_OPS_DOCUMENTED_EXTRAS)
def test_pyrion_ops_importable(symbol):
    """Every symbol in pyrion.ops.__all__ and docs must be importable from pyrion.ops."""
    mod = importlib.import_module("pyrion.ops")
    assert hasattr(mod, symbol), f"pyrion.ops.{symbol} is not importable"


def test_pyrion_ops_all_is_consistent():
    """pyrion.ops.__all__ must not list symbols that aren't actually importable."""
    import pyrion.ops
    for symbol in pyrion.ops.__all__:
        assert hasattr(pyrion.ops, symbol), (
            f"pyrion.ops.__all__ lists '{symbol}' but it is not importable from pyrion.ops"
        )


# ── CLAUDE.md documented imports ──────────────────────────────────────────────

CLAUDE_MD_PYRION_IMPORTS = [
    "GenomicInterval", "GenomicIntervalsCollection", "Transcript",
    "TranscriptsCollection", "Gene", "GeneData", "GenomeAlignment",
    "GenomeAlignmentsCollection", "NucleotideSequence", "AminoAcidSequence",
    "Strand", "TwoBitAccessor", "FastaAccessor", "read_bed12_file",
    "read_chain_file", "read_gene_data", "read_fasta", "write_fasta",
]

CLAUDE_MD_OPS_IMPORTS = [
    "project_transcript_through_chain",
    "project_intervals_through_genome_alignment",
    "extract_cds_sequence", "extract_exon_sequence",
    "merge_intervals", "intersect_intervals", "subtract_intervals",
    "slice_transcript", "transcript_to_bed12_string",
    "save_transcripts_collection_to_bed12",
]


@pytest.mark.parametrize("symbol", CLAUDE_MD_PYRION_IMPORTS)
def test_claude_md_pyrion_imports(symbol):
    """All imports shown in CLAUDE.md 'from pyrion import ...' must work."""
    mod = importlib.import_module("pyrion")
    assert hasattr(mod, symbol), f"CLAUDE.md documents 'from pyrion import {symbol}' but it fails"


@pytest.mark.parametrize("symbol", CLAUDE_MD_OPS_IMPORTS)
def test_claude_md_ops_imports(symbol):
    """All imports shown in CLAUDE.md 'from pyrion.ops import ...' must work."""
    mod = importlib.import_module("pyrion.ops")
    assert hasattr(mod, symbol), f"CLAUDE.md documents 'from pyrion.ops import {symbol}' but it fails"


# ── AGENTS.md documented imports ──────────────────────────────────────────────

AGENTS_MD_PYRION_IMPORTS = [
    "FastaAccessor", "Gene", "GeneData", "GenomeAlignment",
    "GenomeAlignmentsCollection", "GenomicInterval", "NucleotideSequence",
    "Strand", "Transcript", "TranscriptsCollection", "TwoBitAccessor",
    "create_fasta_index", "get_or_create_fasta_index", "load_fasta_index",
    "read_bed12_file", "read_chain_file", "read_dna_fasta", "read_fasta",
    "read_gene_data", "read_gtf", "read_narrow_bed_file", "read_rna_fasta",
    "write_fasta",
]

AGENTS_MD_OPS_IMPORTS = [
    "amino_acid_sequence_to_fasta_string", "array_to_intervals",
    "bed_to_transcripts", "chains_to_arrays", "check_data_consistency",
    "compute_overlap_size", "create_collections_from_mixed_intervals",
    "filter_collection", "find_alignment_gaps", "find_intersections",
    "find_transcript_overlaps", "genome_alignment_from_dict",
    "genome_alignment_to_chain_string", "genome_alignment_to_dict",
    "genome_alignments_collection_from_dict",
    "genome_alignments_collection_summary_string",
    "genome_alignments_collection_to_chain_string",
    "genome_alignments_collection_to_dict", "genomic_interval_to_bed6_string",
    "genomic_intervals_to_bed6_string", "get_chain_q_end", "get_chain_q_start",
    "get_chain_query_interval", "get_chain_t_end", "get_chain_t_start",
    "get_chain_target_interval", "get_transcript_cds_in_range",
    "get_transcript_introns", "get_transcript_introns_in_range",
    "get_transcript_utrs_in_range", "group_intervals_by_proximity",
    "intersect_alignment_with_intervals", "intersect_collections",
    "intersect_intervals", "intervals_to_array", "intervals_to_transcripts",
    "intervals_union", "invert_intervals",
    "load_genome_alignments_collection_from_json",
    "load_transcripts_collection_from_json", "merge_close_intervals",
    "merge_genome_alignments", "merge_intervals", "merge_transcript_cds",
    "merge_transcript_intervals", "merge_transcript_utrs",
    "nucleotide_sequence_to_fasta_string", "project_intervals_through_chain",
    "project_intervals_through_genome_alignment",
    "project_intervals_through_genome_alignment_to_intervals",
    "project_transcript_through_chain",
    "projected_intervals_to_genomic_intervals", "remap_transcript_ids",
    "remove_chain_region_target_space", "remove_intervals",
    "remove_transcript_region", "save_amino_acid_sequence_to_fasta",
    "save_genome_alignments_collection_to_chain",
    "save_genome_alignments_collection_to_json",
    "save_genomic_intervals_to_bed6", "save_nucleotide_sequence_to_fasta",
    "save_transcripts_collection_to_bed12",
    "save_transcripts_collection_to_json", "sequence_to_fasta_string",
    "slice_chain_query_space", "slice_chain_target_space", "slice_intervals",
    "slice_transcript", "split_genome_alignment", "split_intervals_on_gaps",
    "subtract_intervals", "subtract_transcript_regions", "transcript_from_dict",
    "transcript_to_bed12_string", "transcript_to_dict",
    "transcripts_collection_from_dict",
    "transcripts_collection_summary_string",
    "transcripts_collection_to_bed12_string",
    "transcripts_collection_to_dict", "transcripts_to_arrays",
]


@pytest.mark.parametrize("symbol", AGENTS_MD_PYRION_IMPORTS)
def test_agents_md_pyrion_imports(symbol):
    """All imports shown in AGENTS.md 'from pyrion import ...' must work."""
    mod = importlib.import_module("pyrion")
    assert hasattr(mod, symbol), f"AGENTS.md documents 'from pyrion import {symbol}' but it fails"


@pytest.mark.parametrize("symbol", AGENTS_MD_OPS_IMPORTS)
def test_agents_md_ops_imports(symbol):
    """All imports shown in AGENTS.md 'from pyrion.ops import ...' must work."""
    mod = importlib.import_module("pyrion.ops")
    assert hasattr(mod, symbol), f"AGENTS.md documents 'from pyrion.ops import {symbol}' but it fails"


# ── Callable checks ──────────────────────────────────────────────────────────

EXPECTED_CALLABLES_PYRION = [
    "read_bed12_file", "read_narrow_bed_file", "read_chain_file",
    "read_gtf", "read_gene_data", "read_fasta", "write_fasta",
    "read_dna_fasta", "read_rna_fasta",
    "create_fasta_index", "load_fasta_index", "get_or_create_fasta_index",
    "get_version", "get_version_info", "quick_start",
]

EXPECTED_CLASSES_PYRION = [
    "GenomicInterval", "Transcript", "Gene", "GeneData",
    "NucleotideSequence", "AminoAcidSequence",
    "GenomeAlignment", "GenomeAlignmentsCollection",
    "TwoBitAccessor", "FastaAccessor",
    "TranslationTable",
]


@pytest.mark.parametrize("symbol", EXPECTED_CALLABLES_PYRION + EXPECTED_CLASSES_PYRION)
def test_pyrion_symbols_are_callable(symbol):
    """Key public symbols must be callable (functions or classes)."""
    mod = importlib.import_module("pyrion")
    obj = getattr(mod, symbol)
    assert callable(obj), f"pyrion.{symbol} exists but is not callable"
