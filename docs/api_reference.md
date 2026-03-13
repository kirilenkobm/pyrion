# Pyrion API Reference

Structured overview of the public API. For full generated docs see `API_REFERENCE.md`.

---

## GenomicInterval

Single genomic region with strand and optional ID.

```python
from pyrion import GenomicInterval, Strand

iv = GenomicInterval(chrom="chr1", start=1000, end=2000, strand=Strand.PLUS, id="my_interval")
iv = GenomicInterval.from_string("chr1:1000-2000:+")
```

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `length()` | `int` | End minus start |
| `intersects(other)` | `bool` | Whether intervals overlap |
| `overlap(other)` | `int` | Number of overlapping bases |
| `contains(other)` | `bool` | Whether self fully contains other |
| `union(other)` | `GenomicInterval` | Merged interval |
| `flip_strand()` | `GenomicInterval` | Copy with flipped strand |
| `to_bed6_string()` | `str` | BED6 format line |

---

## GenomicIntervalsCollection

Set of intervals on the same chromosome and strand.

```python
from pyrion import GenomicIntervalsCollection, GenomicInterval

coll = GenomicIntervalsCollection.from_intervals([iv1, iv2, iv3])
coll = GenomicIntervalsCollection.from_strings(["chr1:100-200:+", "chr1:300-400:+"])
```

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `to_intervals_list()` | `list[GenomicInterval]` | Convert to list of intervals |
| `merge_close(max_gap)` | `GenomicIntervalsCollection` | Merge nearby intervals |
| `intersect(other)` | `GenomicIntervalsCollection` | Intersect with another collection or interval |
| `filter_by(predicate)` | `GenomicIntervalsCollection` | Filter intervals by function |
| `split_on_gaps(min_gap)` | `list[GenomicIntervalsCollection]` | Split on large gaps |
| `to_bed6_string()` | `str` | BED6 format |

---

## Transcript

Frozen dataclass representing a gene transcript with exon blocks and CDS boundaries.

```python
from pyrion import Transcript, Strand
import numpy as np

t = Transcript(
    blocks=np.array([[1000, 1200], [2000, 2300], [3000, 3500]]),
    strand=Strand.PLUS,
    chrom="chr1",
    id="ENST00000456328",
    cds_start=1100,
    cds_end=3400,
)
```

**Key properties:**

| Property | Type | Description |
|----------|------|-------------|
| `is_coding` | `bool` | Has CDS boundaries |
| `start` | `int` | Transcript start |
| `end` | `int` | Transcript end |
| `transcript_interval` | `GenomicInterval` | Span as interval |
| `cds_blocks` | `np.ndarray` | CDS exon blocks |
| `utr5_blocks` | `np.ndarray` | 5' UTR blocks |
| `utr3_blocks` | `np.ndarray` | 3' UTR blocks |

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `exons()` | `np.ndarray` | Exon block array (N, 2) |
| `get_introns()` | `np.ndarray` | Intron blocks |
| `splice_junctions()` | generator | Donor/acceptor coordinates |
| `with_id(new_id)` | `Transcript` | Copy with new ID |
| `with_fields(**kwargs)` | `Transcript` | Copy with changed fields |
| `contains_interval(iv)` | `bool` | Check containment |

---

## Gene

Gene containing multiple transcript isoforms.

```python
from pyrion import Gene

gene = Gene(gene_id="ENSG00000123456", transcripts=[t1, t2, t3])
```

**Key properties/methods:**

| Member | Type | Description |
|--------|------|-------------|
| `transcripts` | `list[Transcript]` | All isoforms |
| `canonical_transcript` | `Transcript` | Canonical isoform (after canonization) |
| `is_coding` | `bool` | Has any coding transcript |
| `get_transcript(id)` | `Transcript` | Get by ID |
| `apply_canonizer(func)` | `None` | Set canonical transcript |
| `to_union_transcript()` | `Transcript` | Merge all isoforms |

---

## TranscriptsCollection

Container for many transcripts. Supports filtering, gene grouping, and serialization.

```python
from pyrion import read_bed12_file

tc = read_bed12_file("annotations.bed")
```

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get_by_id(id)` | `Transcript` | Lookup by transcript ID |
| `get_by_chrom(chrom)` | `list[Transcript]` | All transcripts on chromosome |
| `filter_by_chroms(chroms)` | `TranscriptsCollection` | Filter by chromosome(s) |
| `filter_by_biotype(biotype)` | `TranscriptsCollection` | Filter by biotype |
| `get_transcripts_in_interval(iv)` | `TranscriptsCollection` | Transcripts overlapping interval |
| `bind_gene_data(gd)` | `None` | Attach gene-transcript mappings |
| `canonize_transcripts(func)` | `None` | Set canonical transcripts |
| `get_genes()` | `list[Gene]` | Group into Gene objects |
| `sort(by, reverse)` | `self` | Sort in-place (chainable); see below |
| `save_to_bed12(path)` | `None` | Write to BED12 file |
| `save_to_json(path)` | `None` | Write to JSON |

---

## GenomeAlignment

Single pairwise genome alignment (chain).

```python
from pyrion import read_chain_file

chains = read_chain_file("hg38ToMm39.chain")
chain = chains.get_by_chain_id(1)

print(chain.t_chrom, chain.q_chrom)
print(chain.aligned_length())
```

**Key fields:** `chain_id`, `score`, `t_chrom`, `t_size`, `q_chrom`, `q_size`, `blocks`

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `aligned_length()` | `int` | Total aligned bases |
| `t_length()` | `int` | Target span length |
| `q_length()` | `int` | Query span length |
| `blocks_in_target()` | `np.ndarray` | Target-space blocks |
| `blocks_in_query()` | `np.ndarray` | Query-space blocks |

---

## GenomeAlignmentsCollection

Container for many chain alignments.

```python
from pyrion import read_chain_file

chains = read_chain_file("hg38ToMm39.chain")
```

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get_by_chain_id(id)` | `GenomeAlignment` | Lookup by chain ID |
| `get_by_target_chrom(chrom)` | `list` | Chains on target chrom |
| `get_alignments_overlapping_target_interval(iv)` | `list` | Chains overlapping target interval |
| `filter(t_chrom, q_chrom, min_score)` | `GenomeAlignmentsCollection` | Filter chains |
| `save_to_chain(path)` | `None` | Write chain file |
| `sort(by, reverse)` | `self` | Sort in-place (chainable); see below |
| `sort_by_score()` | `list[tuple]` | Sorted (chain_id, score) tuples |

---

## NucleotideSequence

DNA/RNA sequence stored as numpy int8 array.

```python
from pyrion import NucleotideSequence

seq = NucleotideSequence.from_string("ATGCGATCGA")
print(seq.to_string())
print(seq.reverse_complement().to_string())
```

**Key methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `to_string()` | `str` | Decode to string |
| `reverse_complement()` | `NucleotideSequence` | Reverse complement |
| `complement()` | `NucleotideSequence` | Complement only |
| `reverse()` | `NucleotideSequence` | Reverse only |
| `slice(start, end)` | `NucleotideSequence` | Subsequence |
| `to_amino_acids()` | `AminoAcidSequence` | Translate |
| `to_codons()` | `CodonSequence` | Split into codons |
| `remove_gaps()` | `NucleotideSequence` | Remove gap characters |

---

## AminoAcidSequence

Protein sequence stored as numpy int8 array.

```python
from pyrion import AminoAcidSequence

aa = AminoAcidSequence.from_string("MVLSPADKTNVKAAWGKVG")
print(aa.to_string())
print(aa.molecular_weight())
```

**Key methods:** `to_string()`, `slice(start, end)`, `reverse()`, `to_fasta_string()`,
`find_stop_codons()`, `count_amino_acids()`, `molecular_weight()`

---

## TwoBitAccessor

Random access to 2bit genome files.

```python
from pyrion import TwoBitAccessor, Strand

genome = TwoBitAccessor("hg38.2bit")
seq = genome.fetch("chr1", 100000, 100500, strand=Strand.PLUS)
seq2 = genome.fetch_interval(some_interval)
sizes = genome.chrom_sizes()
genome.close()
```

---

## FastaAccessor

Random access to indexed FASTA files.

```python
from pyrion import FastaAccessor

fa = FastaAccessor("genome.fa")
seq = fa.fetch("chr1", 100000, 100500, strand=Strand.PLUS)
```

---

## I/O Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `read_bed12_file(path)` | `TranscriptsCollection` | Read BED12 transcripts |
| `read_narrow_bed_file(path)` | `list[GenomicInterval]` | Read BED6 intervals |
| `read_chain_file(path)` | `GenomeAlignmentsCollection` | Read chain alignments |
| `read_gene_data(path)` | `GeneData` | Read gene-transcript mappings |
| `read_gtf(path)` | `TranscriptsCollection` | Read GTF annotations |
| `read_fasta(path)` | `SequencesCollection` | Read FASTA sequences |
| `read_dna_fasta(path)` | `SequencesCollection` | Read DNA FASTA |
| `write_fasta(seqs, path)` | `None` | Write FASTA file |
| `create_fasta_index(path)` | `FaiStore` | Create .fai index |

---

## Operations (pyrion.ops)

| Function | Description |
|----------|-------------|
| `project_transcript_through_chain(t, chain)` | Liftover a transcript |
| `project_intervals_through_chain(intervals, blocks)` | Project interval arrays through chain blocks |
| `project_intervals_through_genome_alignment(intervals, alignment)` | Convenience wrapper |
| `extract_cds_sequence(t, accessor)` | Get CDS nucleotide sequence |
| `extract_exon_sequence(t, accessor)` | Get spliced exon sequence |
| `extract_utr5_sequence(t, accessor)` | Get 5' UTR sequence |
| `extract_utr3_sequence(t, accessor)` | Get 3' UTR sequence |
| `merge_intervals(arr)` | Merge overlapping intervals |
| `intersect_intervals(a, b)` | Intersect two interval arrays |
| `slice_transcript(t, start, end)` | Slice transcript to region |
| `transcript_to_bed12_string(t)` | Convert transcript to BED12 |
| `save_transcripts_collection_to_bed12(coll, path)` | Save collection to BED12 |

---

## Sorting Collections

Both `TranscriptsCollection` and `GenomeAlignmentsCollection` support in-place sorting
via `.sort()`. The method returns `self` so you can chain it with save calls.

### TranscriptsCollection.sort()

```python
# Sort by genomic position (chrom, start, end) — default
transcripts.sort()
transcripts.sort(by="position")

# Sort by transcript ID
transcripts.sort(by="id")

# Sort by multiple keys
transcripts.sort(by=["chrom", "start"])

# Descending order
transcripts.sort(by="start", reverse=True)

# Chain with save
transcripts.sort(by="position").save_to_bed12("sorted.bed")
```

Available keys: `"chrom"`, `"start"`, `"end"`, `"id"`, `"strand"`.
Preset: `"position"` = `["chrom", "start", "end"]`.

### GenomeAlignmentsCollection.sort()

```python
# Sort by score (default)
chains.sort()

# Highest score first
chains.sort(by="score", reverse=True)

# Sort by target genomic position
chains.sort(by="position")

# Sort by multiple keys
chains.sort(by=["t_chrom", "t_start"])

# Chain with save
chains.sort(by="score", reverse=True).save_to_chain("sorted.chain")
```

Available keys: `"score"`, `"chain_id"`, `"t_chrom"`, `"t_start"`,
`"q_chrom"`, `"q_start"`, `"aligned_length"`.
Preset: `"position"` = `["t_chrom", "t_start"]`.

---

## Canonizers

```python
from pyrion.core import longest_isoform_canonizer, longest_cds_canonizer

tc.canonize_transcripts(longest_cds_canonizer)
canonical = tc.get_canonical_transcripts()
```

Available: `longest_isoform_canonizer`, `longest_cds_canonizer`,
`longest_transcript_span_canonizer`, `most_exons_canonizer`, `first_transcript_canonizer`

---

## Strand

```python
from pyrion import Strand

Strand.PLUS    # 1
Strand.MINUS   # -1
Strand.UNKNOWN # 0

s = Strand.from_char("+")
s.to_char()  # "+"
s.flip()     # Strand.MINUS
```
