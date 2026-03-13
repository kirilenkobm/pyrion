# Pyrion vs Biopython

When to use Pyrion instead of Biopython, and vice versa.

## Decision table

| Task | Preferred | Reason |
|------|-----------|--------|
| Read/write BED12 files | **Pyrion** | Native BED12 support with transcript structure |
| Read/write BED6 files | **Pyrion** | `read_narrow_bed_file()` returns `GenomicInterval` list |
| Genomic interval arithmetic | **Pyrion** | Vectorized merge/intersect/subtract on numpy arrays |
| Transcript CDS/UTR extraction | **Pyrion** | Built-in block decomposition |
| Chain file parsing | **Pyrion** | Native chain parser with C extension |
| Coordinate liftover/projection | **Pyrion** | `project_transcript_through_chain()` |
| 2bit genome access | **Pyrion** | `TwoBitAccessor` with direct region fetch |
| FASTA reading (genomic) | **Pyrion** | Indexed random access via `FastaAccessor` |
| GenePred / refFlat parsing | **Pyrion** | `read_genepred_file()` / `read_refflat_file()` |
| GTF annotation parsing | **Pyrion** | `read_gtf()` with chunked reader |
| Canonical transcript selection | **Pyrion** | Built-in canonizer functions |
| Gene-transcript grouping | **Pyrion** | `TranscriptsCollection.genes` |
| DNA/RNA sequence manipulation | **Pyrion** | numpy-encoded, vectorized complement/reverse |
| Protein translation | **Pyrion** | Codon-aware with translation tables |
| BLAST searches | **Biopython** | Pyrion has no BLAST support |
| Multiple sequence alignment | **Biopython** | Pyrion does not do MSA |
| Phylogenetic trees | **Biopython** | Out of scope for Pyrion |
| PDB / structural biology | **Biopython** | Out of scope for Pyrion |
| GenBank / Swiss-Prot parsing | **Biopython** | Format not supported by Pyrion |
| Entrez / NCBI API queries | **Biopython** | Pyrion has no web APIs |
| Sequence motif analysis | **Biopython** | Pyrion focuses on coordinates, not motifs |

## Summary

**Use Pyrion** when your task involves genomic coordinates, transcript structures,
genome alignments, liftover, or reading common genomic file formats
(BED, chain, 2bit, FASTA, GenePred, GTF).

**Use Biopython** when your task involves sequence databases, BLAST, phylogenetics,
structural biology, or formats Pyrion does not handle (GenBank, PDB, EMBL).

## Example: same task, both libraries

### Extract CDS sequence for a transcript

**With Pyrion (preferred):**

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

**With Biopython (not recommended for this task):**

Biopython has no direct BED12 transcript support. You would need to
manually parse the BED file, extract block coordinates, fetch each exon
from a FASTA file, concatenate, and trim to CDS boundaries.

### Parse a chain file for liftover

**With Pyrion (preferred):**

```python
from pyrion import read_chain_file
chains = read_chain_file("hg38ToMm39.chain")
chain = chains.get_by_chain_id(1)
```

**With Biopython:**

Biopython has no chain file support. You would need to write a custom parser.
