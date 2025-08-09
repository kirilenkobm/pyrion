import os
from pathlib import Path

import pytest

from pyrion.io.gtf import read_gtf
from pyrion.io.bed import read_bed12_file


@pytest.mark.integration
def test_gtf_vs_bed12_equivalence_if_available():
    # Use pinned files; the project promises these files exist and remain stable
    gtf_path = Path("test_data/gtf/sample_gencode.gtf")
    bed_path = Path("test_data/hg38.v48.comprehensive.bed")

    if not (gtf_path.exists() and bed_path.exists()):
        pytest.skip("Pinned GTF/BED files not available; skipping")

    gtf_tx = read_gtf(gtf_path)
    bed_tx = read_bed12_file(bed_path)

    # Define equivalence: intersect transcript IDs and compare exon structures
    gtf_ids = {t.id for t in gtf_tx.transcripts}
    bed_ids = {t.id for t in bed_tx.transcripts}

    common = gtf_ids & bed_ids
    # Require at least some overlap
    assert len(common) > 0

    checked = 0
    for tx_id in sorted(common):
        gtf_t = gtf_tx.get_by_id(tx_id)
        bed_t = bed_tx.get_by_id(tx_id)
        assert gtf_t is not None and bed_t is not None

        # Same chrom and strand
        assert gtf_t.chrom == bed_t.chrom
        assert gtf_t.strand == bed_t.strand

        # Same exon count and coordinates (compare sorted by start)
        gtf_exons = sorted((int(s), int(e)) for s, e in gtf_t.blocks)
        bed_exons = sorted((int(s), int(e)) for s, e in bed_t.blocks)
        assert gtf_exons == bed_exons
        checked += 1

    assert checked > 0

