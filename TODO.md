# Tier 1 – Core completeness & stability (v0.2–v0.3)

[x] TranscriptsCollection method to save not only bed, but also GeneData to tsv

[x] Add nullable ID field for NucleotideSequence

[x] write fasta - if width = 0 - just one line - one seq

[x] where is to_rna() method?

[x] NucleotideSequence - some convenience method like nucleotide: count

[x] SequencesCollectionClass with "is_aligned" field.

[x] support gz-ed inputs

[x] gtf parsing - need at least a small sample

[x] gtf parsing - add biodata and geneName extraction 

[x] better gtf parsing test - compare with actual kent tools output

[x] add logger

[x] GeneData binding optimisation - compute anything only on request, lazy attachments

[ ] logging: add where necessary

(a) I/O (open/closed file, format, # entries)
(b) parsing (# valid / skipped lines)
(c) heavy ops (timings, cache-hits)
(d) Warnings about questionable things.


[ ] gff3 reading

strict+lenient modes
ID/Parent, many-parents, order‑independence, ##sequence-region, ##FASTA,;=%&.
Multi-lines features tests

[ ] tests for gff3 vs kenttools output

[ ] Maf reader + respective Genome-Alignment-precursor structure (?)

AlignmentBlocks{seqid, start, end, strand, srcSize, text} -> project(interval) -> list[ProjectedInterval]?

[ ] support gz-ed inputs, but this time good

Shared open_auto(path_or_buf, mode) supporting .gz, .bgz, file‑like, Path, stdin/stdout.
Use everywhere.

[ ] add ambiguous nucleotide codes

[ ] revise metadata (what is helpful to add? Some API to work with metadata)

 Metadata as Mapping[str, Any] + namespaces (sample:…, aligner:…). JSON sidecar.

# Tier 2 – “Batteries included” operations (v0.4–v0.6)

[ ] AlignerStrategy: SequencesCollection, AlignerName -> SequencesCollection.is_aligned

run(collection, *, tool: Literal["mafft","muscle","minimap2"]|Callable, params: dict) -> collection_aligned.
Detect installed aligners (mafft/muscle/minimap2/etc.)
Run & parse output, manage temp files, allow custom strategy injection
Provide one basic built-in pairwise aligner (Needleman–Wunsch or Smith–Waterman, pure-Python+numba) for small jobs

[ ] Simple bundled NW-aligner.

[ ] Transcripts tokenizer

[ ] Isoform graphs

[ ] Vcf support

a thin parser + projection through chains is enough for 80% of needs

# Tier 3 – Visualization & CLI UX (v0.7–v0.9)

[ ] Better visuals

[ ] visualization for sequences - showali-style interactive?

[ ] If need be - CLI wrapper for some very common operations

[ ] low prio: networks wrapper for trees

[ ] execution layer (extendable, strategy pattern, slurm/nextflow/etc)

[ ] Performance policy (pre-1.0)

Audit codebase for “avoid unnecessary computations” principle
Check zero-copy where possible (views instead of copies)
Document invariants (coordinate system, strand semantics, array dtypes)
For instance, attaching data for TranscriptsCollection is an operation that changes Transcripts.
