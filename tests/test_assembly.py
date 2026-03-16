"""Tests for Assembly class and chrom_sizes I/O."""

import json
import pytest
import numpy as np
from pathlib import Path

from pyrion import Assembly, GenomicInterval, Strand, read_chrom_sizes, write_chrom_sizes


HUMAN_CHROMS = {
    "chr1": 248956422,
    "chr2": 242193529,
    "chr3": 198295559,
    "chrX": 156040895,
    "chrY": 57227415,
    "chrM": 16569,
}


@pytest.fixture
def hg38():
    return Assembly(
        name="hg38",
        chrom_sizes=HUMAN_CHROMS,
        aliases=("GRCh38", "GCA_000001405.15"),
        species="Homo sapiens",
    )


@pytest.fixture
def chrom_sizes_file(tmp_path):
    p = tmp_path / "test.chrom.sizes"
    lines = [f"{c}\t{s}\n" for c, s in sorted(HUMAN_CHROMS.items())]
    p.write_text("".join(lines))
    return p


# ── Construction ──────────────────────────────────────────────────────────


class TestConstruction:
    def test_basic(self, hg38):
        assert hg38.name == "hg38"
        assert hg38.num_chroms == 6
        assert hg38.species == "Homo sapiens"
        assert hg38.aliases == ("GRCh38", "GCA_000001405.15")

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            Assembly(name="", chrom_sizes={"chr1": 100})

    def test_empty_chrom_sizes_raises(self):
        with pytest.raises(ValueError, match="chrom_sizes must not be empty"):
            Assembly(name="test", chrom_sizes={})

    def test_from_chrom_sizes_file(self, chrom_sizes_file):
        assembly = Assembly.from_chrom_sizes_file(chrom_sizes_file, name="hg38")
        assert assembly.name == "hg38"
        assert assembly.chrom_sizes == HUMAN_CHROMS

    def test_from_dict_round_trip(self, hg38):
        d = hg38.to_dict()
        restored = Assembly.from_dict(d)
        assert restored == hg38
        assert restored.aliases == hg38.aliases
        assert restored.species == hg38.species

    def test_minimal_from_dict(self):
        d = {"name": "test", "chrom_sizes": {"chr1": 1000}}
        assembly = Assembly.from_dict(d)
        assert assembly.name == "test"
        assert assembly.aliases == ()
        assert assembly.species is None

    def test_metadata(self):
        assembly = Assembly(
            name="test",
            chrom_sizes={"chr1": 1000},
            metadata={"source": "UCSC", "date": "2024-01"},
        )
        assert assembly.metadata["source"] == "UCSC"


# ── Chromosome queries ───────────────────────────────────────────────────


class TestChromQueries:
    def test_has_chrom(self, hg38):
        assert hg38.has_chrom("chr1")
        assert not hg38.has_chrom("chr99")

    def test_contains_syntax(self, hg38):
        assert "chr1" in hg38
        assert "chr99" not in hg38

    def test_get_chrom_size(self, hg38):
        assert hg38.get_chrom_size("chr1") == 248956422

    def test_get_chrom_size_missing(self, hg38):
        with pytest.raises(KeyError):
            hg38.get_chrom_size("chr99")

    def test_uses_chr_prefix(self, hg38):
        assert hg38.uses_chr_prefix is True

    def test_no_chr_prefix(self):
        assembly = Assembly(name="test", chrom_sizes={"1": 100, "2": 200, "X": 300})
        assert assembly.uses_chr_prefix is False

    def test_total_size(self, hg38):
        assert hg38.total_size == sum(HUMAN_CHROMS.values())

    def test_len(self, hg38):
        assert len(hg38) == 6

    def test_chrom_names(self, hg38):
        assert set(hg38.chrom_names) == set(HUMAN_CHROMS.keys())


# ── Fuzzy chrom matching ─────────────────────────────────────────────────


class TestFindChrom:
    def test_exact_match(self, hg38):
        assert hg38.find_chrom("chr1") == "chr1"

    def test_strip_chr_prefix(self, hg38):
        assert hg38.find_chrom("1") == "chr1"

    def test_add_chr_prefix(self):
        assembly = Assembly(name="test", chrom_sizes={"1": 100, "X": 300})
        assert assembly.find_chrom("chr1") == "1"
        assert assembly.find_chrom("chrX") == "X"

    def test_case_insensitive(self, hg38):
        assert hg38.find_chrom("CHR1") == "chr1"
        assert hg38.find_chrom("ChrX") == "chrX"

    def test_mt_m_equivalence(self, hg38):
        assert hg38.find_chrom("chrMT") == "chrM"
        assert hg38.find_chrom("MT") == "chrM"

    def test_no_match(self, hg38):
        assert hg38.find_chrom("chr99") is None


# ── Name matching ────────────────────────────────────────────────────────


class TestNameMatching:
    def test_matches_primary(self, hg38):
        assert hg38.matches_name("hg38")

    def test_matches_alias(self, hg38):
        assert hg38.matches_name("GRCh38")
        assert hg38.matches_name("GCA_000001405.15")

    def test_case_insensitive(self, hg38):
        assert hg38.matches_name("HG38")
        assert hg38.matches_name("grch38")

    def test_no_match(self, hg38):
        assert not hg38.matches_name("mm39")

    def test_all_names(self, hg38):
        assert hg38.all_names() == ("hg38", "GRCh38", "GCA_000001405.15")


# ── Validation ───────────────────────────────────────────────────────────


class TestValidation:
    def test_valid_interval(self, hg38):
        iv = GenomicInterval("chr1", 1000, 2000, Strand.PLUS)
        assert hg38.validate_interval(iv)

    def test_interval_unknown_chrom(self, hg38):
        iv = GenomicInterval("chr99", 0, 100, Strand.PLUS)
        assert not hg38.validate_interval(iv)

    def test_interval_out_of_bounds(self, hg38):
        iv = GenomicInterval("chrM", 0, 99999, Strand.PLUS)
        assert not hg38.validate_interval(iv)

    def test_interval_at_boundary(self, hg38):
        iv = GenomicInterval("chrM", 0, 16569, Strand.PLUS)
        assert hg38.validate_interval(iv)

    def test_valid_transcript(self, hg38):
        from pyrion import Transcript
        t = Transcript(
            blocks=np.array([[1000, 2000], [3000, 4000]], dtype=np.int32),
            strand=Strand.PLUS,
            chrom="chr1",
            id="test_tx",
        )
        assert hg38.validate_transcript(t)

    def test_transcript_unknown_chrom(self, hg38):
        from pyrion import Transcript
        t = Transcript(
            blocks=np.array([[0, 100]], dtype=np.int32),
            strand=Strand.PLUS,
            chrom="chr99",
            id="bad_tx",
        )
        assert not hg38.validate_transcript(t)

    def test_validate_collection(self, hg38):
        from pyrion import Transcript, TranscriptsCollection
        good = Transcript(
            blocks=np.array([[1000, 2000]], dtype=np.int32),
            strand=Strand.PLUS, chrom="chr1", id="good",
        )
        bad_chrom = Transcript(
            blocks=np.array([[0, 100]], dtype=np.int32),
            strand=Strand.PLUS, chrom="chr99", id="bad_chrom",
        )
        bad_bounds = Transcript(
            blocks=np.array([[0, 999999]], dtype=np.int32),
            strand=Strand.PLUS, chrom="chrM", id="bad_bounds",
        )
        tc = TranscriptsCollection(transcripts=[good, bad_chrom, bad_bounds])
        issues = hg38.validate_collection(tc)
        assert len(issues) == 2
        assert any("chr99" in i for i in issues)
        assert any("bad_bounds" in i for i in issues)


# ── Accessor link ────────────────────────────────────────────────────────


class TestAccessor:
    def test_no_accessor_raises(self, hg38):
        assert hg38.has_accessor is False
        with pytest.raises(RuntimeError, match="no sequence accessor"):
            hg38.accessor

    def test_set_accessor(self, hg38):
        class FakeAccessor:
            def fetch(self, chrom, start, end, strand):
                return f"{chrom}:{start}-{end}"

        hg38.set_accessor(FakeAccessor())
        assert hg38.has_accessor is True
        assert hg38.fetch("chr1", 100, 200) == "chr1:100-200"

    def test_fetch_interval(self, hg38):
        class FakeAccessor:
            def fetch(self, chrom, start, end, strand):
                return f"{chrom}:{start}-{end}:{strand}"

        hg38.set_accessor(FakeAccessor())
        iv = GenomicInterval("chr1", 500, 600, Strand.PLUS)
        result = hg38.fetch_interval(iv)
        assert "chr1" in str(result)


# ── Equality and repr ────────────────────────────────────────────────────


class TestIdentity:
    def test_equal(self):
        a = Assembly(name="hg38", chrom_sizes={"chr1": 100})
        b = Assembly(name="hg38", chrom_sizes={"chr1": 100})
        assert a == b

    def test_not_equal_name(self):
        a = Assembly(name="hg38", chrom_sizes={"chr1": 100})
        b = Assembly(name="mm39", chrom_sizes={"chr1": 100})
        assert a != b

    def test_not_equal_chroms(self):
        a = Assembly(name="hg38", chrom_sizes={"chr1": 100})
        b = Assembly(name="hg38", chrom_sizes={"chr1": 200})
        assert a != b

    def test_hash_by_name(self):
        a = Assembly(name="hg38", chrom_sizes={"chr1": 100})
        b = Assembly(name="hg38", chrom_sizes={"chr1": 200})
        assert hash(a) == hash(b)

    def test_repr(self, hg38):
        r = repr(hg38)
        assert "hg38" in r
        assert "6 chromosomes" in r
        assert "Homo sapiens" in r

    def test_repr_with_accessor(self, hg38):
        hg38.set_accessor(object())
        assert "accessor=yes" in repr(hg38)


# ── Chrom sizes I/O ──────────────────────────────────────────────────────


class TestChromSizesIO:
    def test_read_chrom_sizes(self, chrom_sizes_file):
        sizes = read_chrom_sizes(chrom_sizes_file)
        assert sizes == HUMAN_CHROMS

    def test_write_and_read_round_trip(self, tmp_path):
        out = tmp_path / "out.sizes"
        write_chrom_sizes(HUMAN_CHROMS, out)
        sizes = read_chrom_sizes(out)
        assert sizes == HUMAN_CHROMS

    def test_read_with_comments(self, tmp_path):
        p = tmp_path / "commented.sizes"
        p.write_text("# header comment\nchr1\t100\n# another\nchr2\t200\n")
        sizes = read_chrom_sizes(p)
        assert sizes == {"chr1": 100, "chr2": 200}

    def test_read_empty_raises(self, tmp_path):
        p = tmp_path / "empty.sizes"
        p.write_text("")
        with pytest.raises(ValueError, match="no chromosomes found"):
            read_chrom_sizes(p)

    def test_read_bad_size_raises(self, tmp_path):
        p = tmp_path / "bad.sizes"
        p.write_text("chr1\tnot_a_number\n")
        with pytest.raises(ValueError, match="invalid size"):
            read_chrom_sizes(p)

    def test_read_negative_size_raises(self, tmp_path):
        p = tmp_path / "neg.sizes"
        p.write_text("chr1\t-100\n")
        with pytest.raises(ValueError, match="must be positive"):
            read_chrom_sizes(p)

    def test_read_duplicate_raises(self, tmp_path):
        p = tmp_path / "dup.sizes"
        p.write_text("chr1\t100\nchr1\t200\n")
        with pytest.raises(ValueError, match="duplicate"):
            read_chrom_sizes(p)

    def test_save_chrom_sizes_method(self, hg38, tmp_path):
        out = tmp_path / "assembly.sizes"
        hg38.save_chrom_sizes(out)
        sizes = read_chrom_sizes(out)
        assert sizes == HUMAN_CHROMS
