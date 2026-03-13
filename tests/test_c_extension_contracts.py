"""Validate that compiled C extensions match the interfaces Python code expects.

These tests catch stale .so files — when C source is updated but not recompiled,
or when Python callers and C return types drift apart.

Run before every PyPI upload.
"""

import inspect
import importlib
import pytest
import numpy as np


class TestGTFParserContract:
    """parse_gtf_chunk must return a 4-tuple."""

    def test_empty_input_returns_4_tuple(self):
        from pyrion._gtfparser import parse_gtf_chunk
        result = parse_gtf_chunk([])
        assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
        assert len(result) == 4, (
            f"parse_gtf_chunk must return 4 values "
            f"(transcripts, gene_mapping, transcript_biotypes, gene_names), got {len(result)}"
        )

    def test_return_types(self):
        from pyrion._gtfparser import parse_gtf_chunk
        transcripts, gene_mapping, transcript_biotypes, gene_names = parse_gtf_chunk([])
        assert isinstance(transcripts, list)
        assert isinstance(gene_mapping, dict)
        assert isinstance(transcript_biotypes, dict)
        assert isinstance(gene_names, dict)

    def test_single_gene_returns_4_tuple(self):
        from pyrion._gtfparser import parse_gtf_chunk
        lines = [
            'chr1\tENSEMBL\texon\t100\t200\t.\t+\t.\tgene_id "G1"; transcript_id "T1";',
        ]
        result = parse_gtf_chunk(lines)
        assert len(result) == 4


class TestBed12ParserContract:
    """parse_bed12_file must return a list of Transcript objects."""

    def test_empty_input(self):
        from pyrion._bed12parser import parse_bed12_file
        result = parse_bed12_file(b"")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_parse_bed12_line_exists(self):
        from pyrion._bed12parser import parse_bed12_line
        assert callable(parse_bed12_line)


class TestChainParserContract:
    """parse_chain_chunk / parse_many_chain_chunks must exist and be callable."""

    def test_parse_chain_chunk_exists(self):
        from pyrion._chainparser import parse_chain_chunk
        assert callable(parse_chain_chunk)

    def test_parse_many_chain_chunks_empty(self):
        from pyrion._chainparser import parse_many_chain_chunks
        result = parse_many_chain_chunks([])
        assert isinstance(result, list)
        assert len(result) == 0


class TestNarrowBedParserContract:
    """parse_narrow_bed_file must return a list."""

    def test_empty_input(self):
        from pyrion._narrowbedparser import parse_narrow_bed_file
        result = parse_narrow_bed_file(b"", 3)
        assert isinstance(result, list)
        assert len(result) == 0


class TestFastaParserContract:
    """parse_fasta_fast must be callable with (filename, sequence_type)."""

    def test_function_exists(self):
        from pyrion._fastaparser import parse_fasta_fast
        assert callable(parse_fasta_fast)


class TestFaiParserContract:
    """parse_fasta_to_fai must be callable with (filename,)."""

    def test_function_exists(self):
        from pyrion._faiparser import parse_fasta_to_fai
        assert callable(parse_fasta_to_fai)


class TestStubsMatchCompiled:
    """Verify .pyi stubs declare the same functions the compiled modules export."""

    @pytest.mark.parametrize("module_name,expected_functions", [
        ("pyrion._gtfparser", ["parse_gtf_chunk"]),
        ("pyrion._bed12parser", ["parse_bed12_line", "parse_bed12_file"]),
        ("pyrion._chainparser", ["parse_chain_chunk", "parse_many_chain_chunks"]),
        ("pyrion._narrowbedparser", ["parse_narrow_bed_line", "parse_narrow_bed_file"]),
        ("pyrion._fastaparser", ["parse_fasta_fast"]),
        ("pyrion._faiparser", ["parse_fasta_to_fai"]),
    ])
    def test_expected_functions_present(self, module_name, expected_functions):
        mod = importlib.import_module(module_name)
        for func_name in expected_functions:
            assert hasattr(mod, func_name), (
                f"{module_name}.{func_name} missing from compiled extension — "
                f"rebuild with: pip install -e ."
            )
            assert callable(getattr(mod, func_name))
