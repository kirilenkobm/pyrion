# Pyrion Quick Start

## Installation

```bash
pip install pyrion
```

Dependencies: `numpy>=1.21.0`, `py2bit>=0.3.0`, `numba>=0.56.0`

## Minimal working example

```python
from pyrion import read_bed12_file, TwoBitAccessor
from pyrion.ops import extract_cds_sequence

transcripts = read_bed12_file("annotations.bed")
genome = TwoBitAccessor("hg38.2bit")

t = transcripts.get_by_id("ENST00000456328")
cds = extract_cds_sequence(t, genome)
print(cds.to_string())

genome.close()
```

## Common tasks

### 1. Load a genome and fetch a sequence

```python
from pyrion import TwoBitAccessor, Strand

genome = TwoBitAccessor("hg38.2bit")

# Fetch a region
seq = genome.fetch("chr1", 100000, 100500, strand=Strand.PLUS)
print(seq.to_string())

# Get chromosome sizes
chrom_sizes = genome.chrom_sizes()
print(chrom_sizes["chr1"])

genome.close()
```

### 2. Read transcripts from BED12

```python
from pyrion import read_bed12_file

transcripts = read_bed12_file("annotations.bed")

# Get a specific transcript
t = transcripts.get_by_id("ENST00000456328")
print(f"Chrom: {t.chrom}, Strand: {t.strand}, Exons: {len(t.exons())}")
print(f"Is coding: {t.is_coding}")

# Filter by chromosome
chr1_transcripts = transcripts.filter_by_chroms("chr1")

# List all transcript IDs on chr1
for tid in transcripts.get_transcript_ids_by_chrom("chr1"):
    print(tid)
```

### 3. Extract transcript sequences

```python
from pyrion import read_bed12_file, TwoBitAccessor
from pyrion.ops import extract_cds_sequence, extract_exon_sequence

transcripts = read_bed12_file("annotations.bed")
genome = TwoBitAccessor("hg38.2bit")

t = transcripts.get_by_id("ENST00000456328")

# Full exonic sequence (spliced)
exon_seq = extract_exon_sequence(t, genome)
print(exon_seq.to_string()[:60])

# CDS only
if t.is_coding:
    cds_seq = extract_cds_sequence(t, genome)
    protein = cds_seq.to_amino_acids()
    print(protein.to_string()[:40])

genome.close()
```

### 4. Interval operations

```python
from pyrion import GenomicInterval, Strand
from pyrion.ops import merge_intervals, intersect_intervals
import numpy as np

# Create intervals
iv1 = GenomicInterval("chr1", 1000, 2000, Strand.PLUS)
iv2 = GenomicInterval("chr1", 1500, 2500, Strand.PLUS)

# Check overlap
print(iv1.intersects(iv2))  # True
print(iv1.overlap(iv2))     # 500

# Parse from string
iv3 = GenomicInterval.from_string("chr1:3000-4000:+")

# Merge interval arrays
intervals = np.array([[100, 200], [150, 300], [500, 600]])
merged = merge_intervals(intervals)
# Result: [[100, 300], [500, 600]]

# Intersect two interval arrays
a = np.array([[100, 300], [500, 700]])
b = np.array([[200, 600]])
result = intersect_intervals(a, b)
# Result: [[200, 300], [500, 600]]
```

### 5. Liftover (coordinate projection)

```python
from pyrion import read_bed12_file, read_chain_file
from pyrion.ops import project_transcript_through_chain

transcripts = read_bed12_file("hg38_annotations.bed")
chains = read_chain_file("hg38ToMm39.chain")

t = transcripts.get_by_id("ENST00000456328")

# Find chains overlapping the transcript's region
overlapping = chains.get_alignments_overlapping_target_interval(
    t.transcript_interval
)

# Project through the best chain
if overlapping:
    chain = overlapping[0]
    projected_interval = project_transcript_through_chain(t, chain)
    if projected_interval:
        print(f"Projected to: {projected_interval}")
```
