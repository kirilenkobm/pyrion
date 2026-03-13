# Pyrion LLM Coding Patterns

30 copy-pasteable patterns for common genomics tasks.

---

## 1. Read BED12 transcripts

```python
from pyrion import read_bed12_file

transcripts = read_bed12_file("annotations.bed")
print(f"Loaded {len(transcripts)} transcripts")
```

## 2. Read BED6 intervals

```python
from pyrion import read_narrow_bed_file

intervals = read_narrow_bed_file("regions.bed")
for iv in intervals[:5]:
    print(iv.chrom, iv.start, iv.end)
```

## 3. Get a transcript by ID

```python
t = transcripts.get_by_id("ENST00000456328")
print(t.chrom, t.strand, t.start, t.end)
```

## 4. List exon blocks

```python
exons = t.exons()  # np.ndarray shape (N, 2)
for start, end in exons:
    print(f"  exon: {start}-{end}")
```

## 5. Get CDS, UTR5, UTR3 blocks

```python
if t.is_coding:
    cds = t.cds_blocks
    utr5 = t.utr5_blocks
    utr3 = t.utr3_blocks
    print(f"CDS blocks: {len(cds)}, UTR5: {len(utr5)}, UTR3: {len(utr3)}")
```

## 6. Get introns

```python
introns = t.get_introns()
for start, end in introns:
    print(f"  intron: {start}-{end}, length={end - start}")
```

## 7. Get splice junctions

```python
for donor, acceptor in t.splice_junctions():
    print(f"  junction: {donor} -> {acceptor}")
```

## 8. Open a 2bit genome

```python
from pyrion import TwoBitAccessor

genome = TwoBitAccessor("hg38.2bit")
print(genome.chrom_names()[:5])
print(genome.chrom_sizes()["chr1"])
```

## 9. Fetch a genomic sequence

```python
from pyrion import TwoBitAccessor, Strand

genome = TwoBitAccessor("hg38.2bit")
seq = genome.fetch("chr1", 100000, 100100, strand=Strand.PLUS)
print(seq.to_string())
genome.close()
```

## 10. Fetch sequence for an interval

```python
from pyrion import GenomicInterval, TwoBitAccessor, Strand

iv = GenomicInterval("chr1", 100000, 100100, Strand.PLUS)
genome = TwoBitAccessor("hg38.2bit")
seq = genome.fetch_interval(iv)
print(seq.to_string())
genome.close()
```

## 11. Extract CDS sequence from a transcript

```python
from pyrion import read_bed12_file, TwoBitAccessor
from pyrion.ops import extract_cds_sequence

transcripts = read_bed12_file("annotations.bed")
genome = TwoBitAccessor("hg38.2bit")
t = transcripts.get_by_id("ENST00000456328")

cds_seq = extract_cds_sequence(t, genome)
print(cds_seq.to_string()[:60])
genome.close()
```

## 12. Translate CDS to protein

```python
from pyrion.ops import extract_cds_sequence

cds_seq = extract_cds_sequence(t, genome)
protein = cds_seq.to_amino_acids()
print(protein.to_string())
```

## 13. Reverse complement a sequence

```python
from pyrion import NucleotideSequence

seq = NucleotideSequence.from_string("ATGCGATCGA")
rc = seq.reverse_complement()
print(rc.to_string())  # TCGATCGCAT
```

## 14. Create an interval from a string

```python
from pyrion import GenomicInterval

iv = GenomicInterval.from_string("chr1:1000-2000:+")
print(iv.chrom, iv.start, iv.end, iv.strand)
```

## 15. Check interval overlap

```python
from pyrion import GenomicInterval, Strand

a = GenomicInterval("chr1", 1000, 2000, Strand.PLUS)
b = GenomicInterval("chr1", 1500, 2500, Strand.PLUS)
print(a.intersects(b))  # True
print(a.overlap(b))     # 500
print(a.contains(b))    # False
```

## 16. Merge overlapping intervals

```python
from pyrion.ops import merge_intervals
import numpy as np

intervals = np.array([[100, 200], [150, 300], [500, 600]])
merged = merge_intervals(intervals)
print(merged)  # [[100, 300], [500, 600]]
```

## 17. Intersect two interval arrays

```python
from pyrion.ops import intersect_intervals
import numpy as np

a = np.array([[100, 300], [500, 700]])
b = np.array([[200, 600]])
result = intersect_intervals(a, b)
print(result)  # [[200, 300], [500, 600]]
```

## 18. Read a chain file

```python
from pyrion import read_chain_file

chains = read_chain_file("hg38ToMm39.chain")
print(f"Loaded {len(chains)} chains")
```

## 19. Get a chain by ID

```python
chain = chains.get_by_chain_id(1)
print(chain.t_chrom, chain.q_chrom, chain.score)
print(f"Aligned length: {chain.aligned_length()}")
```

## 20. Find chains overlapping a region

```python
from pyrion import GenomicInterval, Strand

region = GenomicInterval("chr1", 1000000, 2000000, Strand.PLUS)
overlapping = chains.get_alignments_overlapping_target_interval(region)
print(f"Found {len(overlapping)} overlapping chains")
```

## 21. Liftover a transcript

```python
from pyrion.ops import project_transcript_through_chain

projected = project_transcript_through_chain(t, chain)
if projected:
    print(f"Projected to: {projected.chrom}:{projected.start}-{projected.end}")
```

## 22. Project intervals through a chain

```python
from pyrion.ops import project_intervals_through_chain
import numpy as np

intervals = np.array([[1000, 2000], [3000, 4000]])
projected = project_intervals_through_chain(intervals, chain.blocks)
for p in projected:
    print(p)  # projected coordinate arrays
```

## 23. Filter transcripts by chromosome

```python
chr1_transcripts = transcripts.filter_by_chroms("chr1")
multi = transcripts.filter_by_chroms(["chr1", "chr2", "chr3"])
```

## 24. Filter transcripts by biotype

```python
gene_data = read_gene_data("gene_data.tsv")
transcripts.bind_gene_data(gene_data)
coding = transcripts.filter_by_biotype("protein_coding")
```

## 25. Find transcripts in a region

```python
from pyrion import GenomicInterval, Strand

region = GenomicInterval("chr1", 1000000, 2000000, Strand.PLUS)
hits = transcripts.get_transcripts_in_interval(region)
for t in hits:
    print(t.id, t.start, t.end)
```

## 26. Select canonical transcripts

```python
from pyrion import read_gene_data
from pyrion.core import longest_cds_canonizer

gene_data = read_gene_data("gene_data.tsv")
transcripts.bind_gene_data(gene_data)
transcripts.canonize_transcripts(longest_cds_canonizer)
canonical = transcripts.get_canonical_transcripts()
```

## 27. Get Gene objects from collection

```python
from pyrion import read_gene_data

gene_data = read_gene_data("gene_data.tsv")
transcripts.bind_gene_data(gene_data)
genes = transcripts.genes
for gene in genes[:3]:
    print(gene.gene_id, len(gene.transcripts), gene.is_coding)
```

## 28. Slice a transcript to a region

```python
from pyrion.ops import slice_transcript

sliced = slice_transcript(t, start=1500, end=3000)
print(f"Sliced exons: {len(sliced.exons())}")
```

## 29. Convert transcript to BED12

```python
from pyrion.ops import transcript_to_bed12_string

bed_line = transcript_to_bed12_string(t)
print(bed_line)
```

## 30. Sort transcripts by genomic position

```python
transcripts.sort(by="position")

# or equivalently
transcripts.sort(by=["chrom", "start"])

# sort and save in one line
transcripts.sort(by="position").save_to_bed12("sorted.bed")
```

## 31. Sort chains by score (highest first)

```python
chains.sort(by="score", reverse=True)
chains.save_to_chain("sorted_by_score.chain")

# sort by target position instead
chains.sort(by="position").save_to_chain("positional.chain")
```

## 32. Save transcripts to BED12

```python
transcripts.save_to_bed12("output.bed")
```

## 33. Read GTF annotations

```python
from pyrion import read_gtf

transcripts = read_gtf("annotations.gtf")
print(f"Loaded {len(transcripts)} transcripts from GTF")
```

## 34. Read FASTA sequences

```python
from pyrion import read_fasta, read_dna_fasta

sequences = read_dna_fasta("sequences.fa")
for seq_id, seq in sequences.items():
    print(seq_id, len(seq.to_string()))
```

## 35. Create a copy of a transcript with new ID

```python
t_copy = t.with_id("my_custom_id")
t_modified = t.with_fields(id="new_id", biotype="lncRNA")
```

## 36. Filter chains by score and chromosomes

```python
filtered = chains.filter(
    t_chrom=["chr1", "chr2"],
    q_chrom="chr1",
    min_score=50000,
)
```

## 37. Read FASTA with indexed random access

```python
from pyrion import FastaAccessor, Strand

fa = FastaAccessor("genome.fa")
seq = fa.fetch("chr1", 0, 1000, Strand.PLUS)
print(seq.to_string()[:50])
```

## 38. Compute flanking regions

```python
genome = TwoBitAccessor("hg38.2bit")
chrom_sizes = genome.chrom_sizes()
left_flank, right_flank = t.compute_flanks(flank_size=5000, chrom_sizes=chrom_sizes)
```

## 39. Union of intervals from multiple arrays

```python
from pyrion.ops import intervals_union

combined = intervals_union([arr1, arr2, arr3])
```

## 40. Get annotated regions (CDS, UTR, flanks)

```python
genome = TwoBitAccessor("hg38.2bit")
chrom_sizes = genome.chrom_sizes()
annotated = t.get_annotated_regions(chrom_sizes, flank_size=5000)
```

## 41. Remap transcript IDs

```python
from pyrion.ops import remap_transcript_ids

new_coll = remap_transcript_ids(transcripts, lambda tid: f"custom_{tid}")
```

## 42. Save and load from JSON

```python
transcripts.save_to_json("transcripts.json")
from pyrion import TranscriptsCollection
loaded = TranscriptsCollection.from_json("transcripts.json")
```
