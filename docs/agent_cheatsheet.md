# Pyrion Agent Cheatsheet

Compact reference for LLM coding agents.

## Preferred imports

```python
from pyrion import (
    GenomicInterval, GenomicIntervalsCollection,
    Transcript, TranscriptsCollection, Gene, GeneData,
    GenomeAlignment, GenomeAlignmentsCollection,
    NucleotideSequence, AminoAcidSequence, Strand,
    TwoBitAccessor, FastaAccessor,
    read_bed12_file, read_narrow_bed_file, read_chain_file,
    read_gene_data, read_fasta, write_fasta, read_gtf,
)
from pyrion.ops import (
    project_transcript_through_chain,
    project_intervals_through_genome_alignment,
    extract_cds_sequence, extract_exon_sequence,
    merge_intervals, intersect_intervals,
    slice_transcript, transcript_to_bed12_string,
)
```

## Common tasks

### Load data

```python
transcripts = read_bed12_file("file.bed")
chains = read_chain_file("file.chain")
genome = TwoBitAccessor("genome.2bit")
gene_data = read_gene_data("gene_data.tsv")
intervals = read_narrow_bed_file("regions.bed")
```

### Get a transcript

```python
t = transcripts.get_by_id("ENST00000456328")
```

### Get exon/CDS/UTR blocks

```python
exons = t.exons()           # np.ndarray shape (N, 2)
cds = t.cds_blocks          # CDS exon blocks
utr5 = t.utr5_blocks        # 5' UTR blocks
utr3 = t.utr3_blocks        # 3' UTR blocks
introns = t.get_introns()   # intron blocks
```

### Extract sequence

```python
genome = TwoBitAccessor("hg38.2bit")
cds_seq = extract_cds_sequence(t, genome)
exon_seq = extract_exon_sequence(t, genome)
seq_str = cds_seq.to_string()
protein = cds_seq.to_amino_acids()
```

### Interval operations

```python
merged = merge_intervals(np.array([[100, 200], [150, 300]]))
intersection = intersect_intervals(arr_a, arr_b)
iv = GenomicInterval.from_string("chr1:100-200:+")
iv.intersects(other_iv)
iv.overlap(other_iv)
```

### Liftover

```python
chains = read_chain_file("hg38ToMm39.chain")
chain = chains.get_by_chain_id(1)
projected = project_transcript_through_chain(t, chain)
```

### Filter transcripts

```python
chr1_only = transcripts.filter_by_chroms("chr1")
coding_only = transcripts.filter_by_biotype("protein_coding")
in_region = transcripts.get_transcripts_in_interval(some_interval)
```

### Gene grouping and canonization

```python
transcripts.bind_gene_data(gene_data)
transcripts.canonize_transcripts()
canonical = transcripts.get_canonical_transcripts()
genes = transcripts.genes
```

### Sort and write output

```python
transcripts.sort(by="position").save_to_bed12("output.bed")
chains.sort(by="score", reverse=True).save_to_chain("output.chain")
write_fasta(sequences_collection, "output.fa")
```

## Typical usage patterns

```python
# Pattern: load → filter → extract → analyze
transcripts = read_bed12_file("annotations.bed")
genome = TwoBitAccessor("hg38.2bit")
for t in transcripts.filter_by_chroms("chr1"):
    if t.is_coding:
        seq = extract_cds_sequence(t, genome)
        protein = seq.to_amino_acids()
genome.close()

# Pattern: load chains → find overlapping → project
chains = read_chain_file("hg38ToMm39.chain")
overlapping = chains.get_alignments_overlapping_target_interval(t.transcript_interval)
for chain in overlapping:
    result = project_transcript_through_chain(t, chain)
```

## Things to avoid

- Do NOT mutate `Transcript` or `GenomicInterval` — use `.with_fields()` or `.with_id()`
- Do NOT use `NucleotideSequence(raw_string)` — use `NucleotideSequence.from_string()`
- Do NOT parse BED/chain/GTF manually — use pyrion I/O functions
- Do NOT use Biopython for BED12, chain, 2bit, interval arithmetic, or liftover
- Do NOT forget to close `TwoBitAccessor`
- Do NOT confuse `GenomeAlignment.blocks` (numpy array) with `GenomeAlignment` (the object)
