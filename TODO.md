# Tier 1 – Core completeness & stability (v0.2–v0.3)

[x] CodonSequence:

len - # codons, not # nucleotides
slice and inteding - for codons too

[x] SequencesCollectionClass with "is_aligned" field.

[ ] add ambiguous nucleotide codes

[x] support gz-ed inputs

[ ] support gz-ed inputs, but this time good

[x] gtf parsing - need at least a small sample

[ ] better gtf parsing test - compare with actual kent tools output

[ ] gff3 reading

[ ] tests for gff3 vs kenttools output

[ ] Maf reader + respective Genome-Alignment-precursor structure (?)

[ ] verbosity and logging system

[ ] revise metadata (what is helpful to add? Some API to work with metadata)

# Tier 2 – “Batteries included” operations (v0.4–v0.6)

[ ] AlignerStrategy: SequencesCollection, AlignerName -> SequencesCollection.is_aligned

Detect installed aligners (mafft/muscle/minimap2/etc.)

Run & parse output, manage temp files, allow custom strategy injection

Provide one basic built-in pairwise aligner (Needleman–Wunsch or Smith–Waterman, pure-Python+numba) for small jobs

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

[ ]Performance policy (pre-1.0)
Audit codebase for “avoid unnecessary computations” principle
Check zero-copy where possible (views instead of copies)
Document invariants (coordinate system, strand semantics, array dtypes)

For instance, attaching data for TranscriptsCollection is an operation that changes Transcripts.
