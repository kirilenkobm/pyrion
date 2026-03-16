# Pyrion API Reference

**Generated:** 2026-03-16 15:50:13

Complete API reference with full docstrings and signatures.

## Table of Contents

- [pyrion](#pyrion)
  - [cite](#cite)
  - [get_version](#get_version)
  - [get_version_info](#get_version_info)
  - [quick_start](#quick_start)
- [pyrion._bed12parser](#pyrion_bed12parser)
- [pyrion._chainparser](#pyrion_chainparser)
- [pyrion._faiparser](#pyrion_faiparser)
- [pyrion._fastaparser](#pyrion_fastaparser)
- [pyrion._gtfparser](#pyrion_gtfparser)
- [pyrion._narrowbedparser](#pyrion_narrowbedparser)
- [pyrion._version](#pyrion_version)
- [pyrion.config](#pyrionconfig)
  - [PyrionConfig](#pyrionconfig)

---

# pyrion

Pyrion: A Fast and Efficient Bioinformatics Library for Genomic Data Processing


## Functions

### cite

**Signature:** `()`

Get citation information.


### get_version

**Signature:** `()`

Get pyrion version.


### get_version_info

**Signature:** `()`

Get pyrion version as tuple.


### quick_start

**Signature:** `()`


---

# pyrion._bed12parser


---

# pyrion._chainparser


---

# pyrion._faiparser

Fast FASTA indexer for generating FAI entries - Production optimized


---

# pyrion._fastaparser

Fast FASTA file parser with numpy integration - Production optimized


---

# pyrion._gtfparser

High-performance GTF parser


---

# pyrion._narrowbedparser


---

# pyrion._version

Version information for pyrion.


---

# pyrion.config

Global configuration for pyrion library.


## Classes

### PyrionConfig

Global configuration for pyrion library.

Manages parallelization settings and other global options.

**Signature:** `(self)`

#### Methods

**__init__**

*Signature:* `(self)`

Initialize self.  See help(type(self)) for accurate signature.


**disable_parallel**

*Signature:* `(self) -> None`

Disable all parallel processing by setting max_cores to 0.


**enable_parallel**

*Signature:* `(self, max_cores: Optional[int] = None) -> None`

Enable parallel processing.


**set_log_level**

*Signature:* `(self, level: Union[str, int]) -> None`

Configure logging for the pyrion package.

Args:
    level: Logging level as string ("DEBUG", "INFO", "WARNING", "ERROR") 
          or int (logging.DEBUG, logging.INFO, etc.)


**summary**

*Signature:* `(self) -> dict`

Get a summary of current configuration.


#### Properties

**available_cores** -> `int`

Get the number of available CPU cores (read-only).


**max_cores** -> `int`

Get the maximum number of cores to use for parallel processing.


**min_items_for_parallel** -> `int`

Get the minimum number of items required to use parallel processing.


**multiprocessing_available** -> `bool`

Check if multiprocessing is available (read-only).



## Functions

### disable_parallel

**Signature:** `() -> None`

Disable all parallel processing.


### enable_parallel

**Signature:** `(max_cores: Optional[int] = None) -> None`

Enable parallel processing with optional core limit.


### get_available_cores

**Signature:** `() -> int`

Get the number of available CPU cores.


### get_config_summary

**Signature:** `() -> dict`

Get a summary of current configuration.


### get_max_cores

**Signature:** `() -> int`

Get the current maximum number of cores for parallel processing.


### get_min_items_for_parallel

**Signature:** `() -> int`

Get the minimum number of items required for parallel processing.


### is_multiprocessing_available

**Signature:** `() -> bool`

Check if multiprocessing is available.


### set_loglevel

**Signature:** `(level: Union[str, int]) -> None`

Set logging level for the pyrion package.

Examples:
    >>> import pyrion
    >>> pyrion.set_loglevel("INFO")     # Enable info-level logging
    >>> pyrion.set_loglevel("DEBUG")    # Enable debug-level logging  
    >>> pyrion.set_loglevel("WARNING")  # Enable warning+ only


### set_max_cores

**Signature:** `(cores: int) -> None`

Set the maximum number of cores to use for parallel processing.


### set_min_items_for_parallel

**Signature:** `(items: int) -> None`

Set the minimum number of items required for parallel processing.


---

# pyrion.constants


---

# pyrion.core

Core genomics data structures and types.


---

# pyrion.core.amino_acid_auxiliary

Auxiliary functions for amino acid sequence objects.


## Functions

### calculate_molecular_weight

**Signature:** `(sequence) -> float`

Calculate approximate molecular weight in Daltons.


### count_amino_acids_in_sequence

**Signature:** `(sequence) -> Dict[str, int]`

Count occurrences of each amino acid type (ignoring masking).


### get_amino_acid_composition

**Signature:** `(sequence) -> Dict[str, float]`


---

# pyrion.core.amino_acid_sequences

Amino acid sequence representations and storage.


## Classes

### AminoAcidSequence

AminoAcidSequence(data: 'np.ndarray', metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None)

**Signature:** `(self, data: 'np.ndarray', metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None) -> None`

#### Methods

**__init__**

*Signature:* `(self, data: 'np.ndarray', metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> 'str'`

Return repr(self).


**__str__**

*Signature:* `(self) -> 'str'`

Return str(self).


**apply_masking**

*Signature:* `(self) -> "'AminoAcidSequence'"`


**count_amino_acids**

*Signature:* `(self) -> 'dict'`

Count occurrences of each amino acid type (ignoring masking) using vectorized operations.


**find_stop_codons**

*Signature:* `(self) -> 'np.ndarray'`

Find positions of stop codons in the sequence.


**from_string**

*Signature:* `(sequence: 'str', metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None) -> "'AminoAcidSequence'"`


**get_amino_acid_content**

*Signature:* `(self) -> 'dict'`

Get amino acid composition as percentages.


**get_gap_positions**

*Signature:* `(self) -> 'np.ndarray'`

Get boolean array indicating which positions are gaps.


**get_masked_positions**

*Signature:* `(self) -> 'np.ndarray'`

Get boolean array indicating which positions are masked.


**get_stop_positions**

*Signature:* `(self) -> 'np.ndarray'`

Get boolean array indicating which positions are stop codons.


**molecular_weight**

*Signature:* `(self) -> 'float'`

Calculate approximate molecular weight in Daltons.


**remove_gaps**

*Signature:* `(self) -> "'AminoAcidSequence'"`


**remove_masking**

*Signature:* `(self) -> "'AminoAcidSequence'"`


**reverse**

*Signature:* `(self) -> "'AminoAcidSequence'"`


**slice**

*Signature:* `(self, start: 'int', end: 'int') -> "'AminoAcidSequence'"`


**to_fasta_string**

*Signature:* `(self, width: 'int' = 80, header: 'Optional[str]' = None) -> 'str'`


**to_string**

*Signature:* `(self) -> 'str'`



---

# pyrion.core.assembly

Genome assembly representation with optional sequence accessor.


## Classes

### Assembly

A genome assembly: named chromosome sizes with optional sequence accessor.

Assembly is a mutable context object (not a frozen data record).
Two assemblies are equal if they have the same name and chrom_sizes.

Parameters
----------
name : str
    Primary identifier, e.g. "hg38".
chrom_sizes : dict
    Mapping of chromosome name to size in bp.
aliases : tuple of str, optional
    Alternative names, e.g. ("GRCh38", "GCA_000001405.15").
species : str, optional
    Species name, e.g. "Homo sapiens".
metadata : dict, optional
    Arbitrary extra information.

**Signature:** `(self, name: 'str', chrom_sizes: 'Dict[str, int]', aliases: 'Tuple[str, ...]' = (), species: 'Optional[str]' = None, metadata: 'Optional[Dict[str, Any]]' = None)`

#### Methods

**__init__**

*Signature:* `(self, name: 'str', chrom_sizes: 'Dict[str, int]', aliases: 'Tuple[str, ...]' = (), species: 'Optional[str]' = None, metadata: 'Optional[Dict[str, Any]]' = None)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> 'str'`

Return repr(self).


**all_names**

*Signature:* `(self) -> 'Tuple[str, ...]'`

Return (name,) + aliases.


**fetch**

*Signature:* `(self, chrom: 'str', start: 'Optional[int]' = None, end: 'Optional[int]' = None, strand: 'Strand' = <Strand.PLUS: 1>) -> 'NucleotideSequence'`

Fetch sequence via the attached accessor.


**fetch_interval**

*Signature:* `(self, interval: 'GenomicInterval') -> 'NucleotideSequence'`

Fetch sequence for a GenomicInterval via the attached accessor.


**find_chrom**

*Signature:* `(self, chrom: 'str') -> 'Optional[str]'`

Fuzzy-match a chromosome name, handling chr prefix differences.

Returns the matching chrom name from this assembly, or None.


**from_2bit**

*Signature:* `(path_or_accessor, name: 'str', aliases: 'Tuple[str, ...]' = (), species: 'Optional[str]' = None, metadata: 'Optional[Dict[str, Any]]' = None) -> 'Assembly'`

Create an Assembly from a 2bit file or an open TwoBitAccessor.

The accessor is attached automatically.


**from_chrom_sizes_file**

*Signature:* `(path: 'Union[str, Path]', name: 'str', aliases: 'Tuple[str, ...]' = (), species: 'Optional[str]' = None, metadata: 'Optional[Dict[str, Any]]' = None) -> 'Assembly'`

Create an Assembly from a .chrom.sizes file (two-column TSV).


**from_dict**

*Signature:* `(d: 'Dict[str, Any]') -> 'Assembly'`


**from_fasta_index**

*Signature:* `(path_or_accessor, name: 'str', aliases: 'Tuple[str, ...]' = (), species: 'Optional[str]' = None, metadata: 'Optional[Dict[str, Any]]' = None) -> 'Assembly'`

Create an Assembly from a FastaAccessor (or path to indexed FASTA).

The accessor is attached automatically.


**get_chrom_size**

*Signature:* `(self, chrom: 'str') -> 'int'`


**has_chrom**

*Signature:* `(self, chrom: 'str') -> 'bool'`


**matches_name**

*Signature:* `(self, name: 'str') -> 'bool'`

Check if `name` matches this assembly's name or any alias (case-insensitive).


**save_chrom_sizes**

*Signature:* `(self, path: 'Union[str, Path]') -> 'None'`

Write chrom sizes to a two-column TSV file.


**set_accessor**

*Signature:* `(self, accessor) -> 'None'`

Attach a TwoBitAccessor or FastaAccessor for sequence retrieval.


**to_dict**

*Signature:* `(self) -> 'Dict[str, Any]'`


**validate_collection**

*Signature:* `(self, collection) -> 'List[str]'`

Validate a TranscriptsCollection against this assembly.

Returns a list of issue descriptions (empty = all valid).


**validate_interval**

*Signature:* `(self, interval: 'GenomicInterval') -> 'bool'`

Check if a GenomicInterval fits within this assembly.


**validate_transcript**

*Signature:* `(self, transcript) -> 'bool'`

Check if a Transcript fits within this assembly.


#### Properties

**accessor** -> `Any`

Return the attached sequence accessor, or raise if none is set.


**chrom_names** -> `List[str]`


**has_accessor** -> `bool`


**num_chroms** -> `int`


**total_size** -> `int`


**uses_chr_prefix** -> `bool`

Whether this assembly uses 'chr' prefixed chromosome names.



---

# pyrion.core.canonizer

Canonizer functions for selecting canonical transcripts from transcript lists.


## Functions

### DEFAULT_CANONIZER

**Signature:** `(transcripts: List, **kwargs) -> Optional[str]`

Default canonizer that selects the transcript with the longest total exonic length.


### first_transcript_canonizer

**Signature:** `(transcripts: List, **kwargs) -> Optional[str]`


### longest_cds_canonizer

**Signature:** `(transcripts: List, **kwargs) -> Optional[str]`


### longest_isoform_canonizer

**Signature:** `(transcripts: List, **kwargs) -> Optional[str]`

Default canonizer that selects the transcript with the longest total exonic length.


### longest_transcript_span_canonizer

**Signature:** `(transcripts: List, **kwargs) -> Optional[str]`


### most_exons_canonizer

**Signature:** `(transcripts: List, **kwargs) -> Optional[str]`


---

# pyrion.core.codons

Codon and codon sequence representations for genomic analysis.


## Classes

### Codon

Codon representation holding 1-3 non-gap symbols (incomplete codons allowed).

**Signature:** `(self, symbols: numpy.ndarray, is_rna: bool = False) -> None`

#### Methods

**__init__**

*Signature:* `(self, symbols: numpy.ndarray, is_rna: bool = False) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**__str__**

*Signature:* `(self) -> str`

Return str(self).


**is_complete**

*Signature:* `(self) -> bool`

Check if codon has exactly 3 non-gap symbols.


**to_string**

*Signature:* `(self) -> str`


**translate**

*Signature:* `(self, translation_table=None) -> str`



### CodonSequence

Codon sequence wrapper around NucleotideSequence with codon-wise operations.

**Signature:** `(self, nucleotide_sequence, id: Optional[str] = None)`

#### Methods

**__init__**

*Signature:* `(self, nucleotide_sequence, id: Optional[str] = None)`

Initialize from a NucleotideSequence object.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**__str__**

*Signature:* `(self) -> str`

Return str(self).


**get_codons**

*Signature:* `(self, preserve_gaps: bool = False) -> List[pyrion.core.codons.Codon]`


**get_frameshift_positions**

*Signature:* `(self) -> List[Tuple[int, int]]`


**insert_frameshift**

*Signature:* `(self, position: int) -> None`

Insert frameshift after the Nth valid nucleotide (atgcnATGCN) (0-based).


**remove_frameshift**

*Signature:* `(self, position: int) -> None`

Remove frameshift after the Nth valid nucleotide (atgcnATGCN).


**remove_gaps**

*Signature:* `(self) -> None`


**to_fasta_string**

*Signature:* `(self, width: int = 80, header: Optional[str] = None) -> str`


**translate**

*Signature:* `(self, translation_table=None)`


#### Properties

**data** -> `ndarray`

Access to underlying data array.



---

# pyrion.core.fai

FASTA index (FAI) functionality for efficient random access to large FASTA files.


## Classes

### FaiEntry

FASTA index entry for a single sequence.

**Signature:** `(self, name: 'str', length: 'int', offset: 'int', line_bases: 'int', line_bytes: 'int') -> None`

#### Methods

**__init__**

*Signature:* `(self, name: 'str', length: 'int', offset: 'int', line_bases: 'int', line_bytes: 'int') -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> 'str'`

Return repr(self).


**__str__**

*Signature:* `(self) -> 'str'`

Format as FAI file line.


**from_fai_line**

*Signature:* `(line: 'str') -> "'FaiEntry'"`


**get_sequence_end_offset**

*Signature:* `(self) -> 'int'`



### FaiStore

Container for FASTA index entries with dict interface.

**Signature:** `(self, entries: 'Optional[Dict[str, FaiEntry]]' = None)`

#### Methods

**__init__**

*Signature:* `(self, entries: 'Optional[Dict[str, FaiEntry]]' = None)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> 'str'`

Return repr(self).


**get_total_bases**

*Signature:* `(self) -> 'int'`


**load_from_file**

*Signature:* `(filename: 'Union[str, Path]') -> "'FaiStore'"`


**save_to_file**

*Signature:* `(self, filename: 'Union[str, Path]') -> 'None'`



---

# pyrion.core.gene_data

Gene data storage with multiple mappings.


## Classes

### GeneData

Gene data container with optional mappings for gene-transcript relationships, biotypes, and names.

**Signature:** `(self, source_file: Optional[str] = None)`

#### Methods

**__init__**

*Signature:* `(self, source_file: Optional[str] = None)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**add_gene_name**

*Signature:* `(self, gene_id: str, gene_name: str) -> None`


**add_gene_transcript_mapping**

*Signature:* `(self, gene_id: str, transcript_id: str) -> None`


**add_transcript_biotype**

*Signature:* `(self, transcript_id: str, biotype: str) -> None`


**get_biotype_count**

*Signature:* `(self) -> int`


**get_gene**

*Signature:* `(self, transcript_id: str) -> Optional[str]`


**get_gene_name**

*Signature:* `(self, gene_id: str) -> Optional[str]`


**get_gene_name_count**

*Signature:* `(self) -> int`


**get_gene_transcript_count**

*Signature:* `(self) -> int`


**get_genes_by_name**

*Signature:* `(self, gene_name: str) -> Set[str]`


**get_transcript_biotype**

*Signature:* `(self, transcript_id: str) -> Optional[str]`


**get_transcripts**

*Signature:* `(self, gene_id: str) -> Set[str]`


**has_biotype_mapping**

*Signature:* `(self) -> bool`


**has_gene**

*Signature:* `(self, gene_id: str) -> bool`


**has_gene_name_mapping**

*Signature:* `(self) -> bool`


**has_gene_transcript_mapping**

*Signature:* `(self) -> bool`


**has_transcript**

*Signature:* `(self, transcript_id: str) -> bool`


**subset**

*Signature:* `(self, transcript_ids: Set[str]) -> 'GeneData'`

Return a new GeneData containing only entries relevant to the given transcript IDs.


**summary**

*Signature:* `(self) -> str`


#### Properties

**gene_ids** -> `Set`


**transcript_ids** -> `Set`



---

# pyrion.core.genes

Gene and transcript representations.


## Classes

### Gene

Gene containing multiple transcripts with computed genomic bounds.

**Signature:** `(self, gene_id: str, transcripts: List[pyrion.core.genes.Transcript], gene_name: Optional[str] = None)`

#### Methods

**__init__**

*Signature:* `(self, gene_id: str, transcripts: List[pyrion.core.genes.Transcript], gene_name: Optional[str] = None)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**apply_canonizer**

*Signature:* `(self, canonizer_func: Optional[Callable] = None, **kwargs) -> None`

Set the canonical transcript using a canonizer function.

Args:
    canonizer_func: Function that takes transcripts list and returns canonical transcript ID.
                  If None, uses the default longest_isoform_canonizer.
    **kwargs: Additional arguments passed to the canonizer function.


**clear_canonical_transcript**

*Signature:* `(self) -> None`


**get_transcript**

*Signature:* `(self, transcript_id: str) -> Optional[pyrion.core.genes.Transcript]`


**has_transcript**

*Signature:* `(self, transcript_id: str) -> bool`


**set_canonical_transcript**

*Signature:* `(self, transcript_id: str) -> None`


**to_union_transcript**

*Signature:* `(self, transcript_id: Optional[str] = None, id_prefix: str = 'U_') -> pyrion.core.genes.Transcript`

Merge all isoforms into a single union transcript.

For coding genes: merges CDS and UTR blocks separately, then combines.
CDS boundaries are derived from the union of all CDS blocks.
For non-coding genes: merges all exon blocks.

Args:
    transcript_id: Explicit ID for the union transcript.
        If None, uses ``id_prefix + gene_id``.
    id_prefix: Prefix prepended to gene_id when transcript_id is None.


#### Properties

**canonical_transcript** -> `Optional`


**canonical_transcript_id** -> `Optional`


**chrom** -> `str`


**has_canonical_transcript** -> `bool`


**is_coding** -> `bool`

Check if gene has any coding transcripts.


**length** -> `int`


**strand** -> `Strand`


**transcript_ids** -> `Set`


**transcripts** -> `List`



### Transcript

Transcript(blocks: numpy.ndarray, strand: pyrion.core.strand.Strand, chrom: str, id: str, cds_start: Optional[int] = None, cds_end: Optional[int] = None, biotype: Optional[str] = None)

**Signature:** `(self, blocks: numpy.ndarray, strand: pyrion.core.strand.Strand, chrom: str, id: str, cds_start: Optional[int] = None, cds_end: Optional[int] = None, biotype: Optional[str] = None) -> None`

#### Methods

**__init__**

*Signature:* `(self, blocks: numpy.ndarray, strand: pyrion.core.strand.Strand, chrom: str, id: str, cds_start: Optional[int] = None, cds_end: Optional[int] = None, biotype: Optional[str] = None) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**__str__**

*Signature:* `(self) -> str`

Return str(self).


**compute_flanks**

*Signature:* `(self, flank_size: int, chrom_sizes: Dict[str, int]) -> Tuple[Optional[pyrion.core.intervals.GenomicInterval], Optional[pyrion.core.intervals.GenomicInterval]]`


**contains_interval**

*Signature:* `(self, interval: pyrion.core.intervals.GenomicInterval) -> bool`


**exons**

*Signature:* `(self) -> numpy.ndarray`


**from_intervals_collection**

*Signature:* `(collection: pyrion.core.intervals.GenomicIntervalsCollection, transcript_id: str, cds_start: Optional[int] = None, cds_end: Optional[int] = None, biotype: Optional[str] = None) -> 'Transcript'`

Create a Transcript from a GenomicIntervalsCollection.

The collection already guarantees same chrom, same strand, and
sorted-by-start blocks. This method additionally validates that
blocks do not overlap.


**get_annotated_regions**

*Signature:* `(self, chrom_sizes: dict, flank_size: int = 5000) -> pyrion.core.intervals.AnnotatedIntervalSet`


**get_introns**

*Signature:* `(self, use_numba: bool = True) -> numpy.ndarray`


**splice_junctions**

*Signature:* `(self)`

Generator yielding splice junction coordinates (donor, acceptor) for transcript.


**with_fields**

*Signature:* `(self, **kwargs) -> 'Transcript'`

Return a copy with arbitrary fields replaced.

Example:
    t.with_fields(id="new_id", biotype="lncRNA")


**with_id**

*Signature:* `(self, new_id: str) -> 'Transcript'`

Return a copy of this transcript with a different ID.


#### Properties

**is_coding** -> `bool`



### TranscriptsCollection

Container for many transcripts.

**Signature:** `(self, transcripts: Optional[List[pyrion.core.genes.Transcript]] = None, source_file: Optional[str] = None)`

#### Methods

**__init__**

*Signature:* `(self, transcripts: Optional[List[pyrion.core.genes.Transcript]] = None, source_file: Optional[str] = None)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**__str__**

*Signature:* `(self) -> str`

Return str(self).


**append**

*Signature:* `(self, transcript: pyrion.core.genes.Transcript) -> None`

Append a single transcript to the collection.


**apply_gene_canonical_mapping**

*Signature:* `(self, gene_to_canonical: Dict[str, str]) -> None`

gene_to_canonical: Dictionary mapping gene IDs to canonical transcript IDs


**bind_gene_data**

*Signature:* `(self, gene_data: 'GeneData') -> None`


**canonize_transcripts**

*Signature:* `(self, canonizer_func: Optional[Callable] = None, **kwargs) -> None`


**copy_with_remapped_ids**

*Signature:* `(self, id_mapping: Union[Dict[str, str], Callable[[str], str]], source_file: Optional[str] = None) -> 'TranscriptsCollection'`

Return a new collection with the same transcripts but different IDs.

IDs are immutable on Transcript, so this creates new Transcript copies
with the requested IDs. See pyrion.ops.transformations.remap_transcript_ids.


**extend**

*Signature:* `(self, other: Union[List[pyrion.core.genes.Transcript], ForwardRef('TranscriptsCollection')]) -> None`

Extend this collection with transcripts from a list or another collection.


**filter_by_biotype**

*Signature:* `(self, biotype: Union[str, List[str], Set[str]]) -> 'TranscriptsCollection'`

Return a new collection containing only transcripts with the given biotype(s).

Accepts a single biotype string or a collection of biotype strings.
Uses bound GeneData for biotype when transcript.biotype is not set.


**filter_by_chroms**

*Signature:* `(self, chroms: Union[str, List[str], Set[str]]) -> 'TranscriptsCollection'`

Return a new subcollection containing only transcripts on the given chromosome(s).

Carries over bound GeneData and source_file from the parent collection.


**from_json**

*Signature:* `(file_path: Union[str, pathlib.Path]) -> 'TranscriptsCollection'`


**get_all_chromosomes**

*Signature:* `(self) -> List[str]`


**get_by_biotype**

*Signature:* `(self, biotype: Union[str, List[str], Set[str]]) -> 'TranscriptsCollection'`

Alias for filter_by_biotype.


**get_by_chrom**

*Signature:* `(self, chrom: str) -> List[pyrion.core.genes.Transcript]`


**get_by_gene_name**

*Signature:* `(self, gene_name: str) -> List[pyrion.core.genes.Gene]`

Get Gene objects by gene name. Multiple genes can have the same name.


**get_by_id**

*Signature:* `(self, transcript_id: str) -> Optional[pyrion.core.genes.Transcript]`


**get_canonical_transcripts**

*Signature:* `(self) -> 'TranscriptsCollection'`


**get_gene_by_id**

*Signature:* `(self, gene_id: str) -> Optional[pyrion.core.genes.Gene]`


**get_gene_by_transcript_id**

*Signature:* `(self, transcript_id: str) -> Optional[pyrion.core.genes.Gene]`


**get_genes_without_canonical_transcript**

*Signature:* `(self) -> List[pyrion.core.genes.Gene]`


**get_transcript_ids_by_chrom**

*Signature:* `(self, chrom: str) -> List[str]`


**get_transcripts_in_interval**

*Signature:* `(self, interval: pyrion.core.intervals.GenomicInterval, include_partial: bool = True) -> 'TranscriptsCollection'`


**get_trimmed_gene_data**

*Signature:* `(self) -> 'GeneData'`

Return a copy of bound GeneData containing only entries for transcripts in this collection.


**save_biodata**

*Signature:* `(self, tsv_path: Union[str, pathlib.Path], include_gene_transcript: bool = True, include_transcript_biotype: bool = True, include_gene_name: bool = True, separator: str = '\t', trim: bool = True) -> None`


**save_to_bed12**

*Signature:* `(self, file_path: Union[str, pathlib.Path]) -> None`


**save_to_json**

*Signature:* `(self, file_path: Union[str, pathlib.Path]) -> None`


**sort**

*Signature:* `(self, by: Union[str, List[str]] = 'position', reverse: bool = False) -> 'TranscriptsCollection'`

Sort transcripts in-place and return self for chaining.

Args:
    by: Sort key(s). A single string or list of strings.
        Predefined presets:
            "position" — sort by (chrom, start, end)  [default]
            "id"       — sort by transcript ID
        Individual keys: "chrom", "start", "end", "id", "strand".
        Multiple keys: ["chrom", "start"] sorts by chrom first, then start.
    reverse: If True, sort in descending order.

Returns:
    self (for chaining, e.g. ``collection.sort().save_to_bed12(path)``)


**summary**

*Signature:* `(self) -> str`


**to_bed12_string**

*Signature:* `(self) -> str`


#### Properties

**applied_biotypes** -> `bool`


**applied_gene_names** -> `bool`


**available_data_mappings** -> `List`


**gene_data** -> `Optional`

Bound GeneData object, or None if no gene data has been bound.


**gene_ids** -> `Set`


**genes** -> `List`


**has_gene_mapping** -> `bool`



---

# pyrion.core.genes_auxiliary

Auxiliary functions for gene and transcript objects.


## Functions

### build_annotated_regions

**Signature:** `(transcript, chrom_sizes: dict, flank_size: int = 5000) -> pyrion.core.intervals.AnnotatedIntervalSet`


### compute_flanks

**Signature:** `(transcript, flank_size: int, chrom_sizes: Dict[str, int]) -> Tuple[Optional[pyrion.core.intervals.GenomicInterval], Optional[pyrion.core.intervals.GenomicInterval]]`

Get flanking regions of specified size around a transcript.


### filter_transcripts_by_biotype

**Signature:** `(transcripts_collection, biotypes)`

Return a new TranscriptsCollection with only transcripts matching the given biotype(s).

Args:
    biotypes: A set of biotype strings to keep.


### filter_transcripts_in_interval

**Signature:** `(transcripts_collection, interval: pyrion.core.intervals.GenomicInterval, include_partial: bool = True)`

Filter transcripts that are within or intersect with a genomic interval.


### get_canonical_transcripts_from_collection

**Signature:** `(transcripts_collection, canonizer_func: Optional[Callable] = None, **kwargs)`

Get a new collection containing only canonical transcripts.


### get_canonical_transcripts_only_from_collection

**Signature:** `(transcripts_collection)`

Get a new collection containing only already-set canonical transcripts.


### get_cds_blocks

**Signature:** `(transcript) -> numpy.ndarray`

Get CDS blocks from transcript using slice operations.


### get_genes_with_canonical_transcripts_from_collection

**Signature:** `(transcripts_collection) -> List`

Get all genes that have canonical transcripts set.


### get_left_utr_blocks

**Signature:** `(transcript) -> numpy.ndarray`

Get UTR blocks to the left of CDS (chromosomally before CDS start).


### get_right_utr_blocks

**Signature:** `(transcript) -> numpy.ndarray`

Get UTR blocks to the right of CDS (chromosomally after CDS end).


### get_transcript_cds_interval

**Signature:** `(transcript) -> Optional[pyrion.core.intervals.GenomicInterval]`

Get genomic interval spanning the CDS region.


### get_transcript_interval

**Signature:** `(transcript) -> pyrion.core.intervals.GenomicInterval`

Get genomic interval spanning the entire transcript.


### get_utr3_blocks

**Signature:** `(transcript) -> numpy.ndarray`


### get_utr5_blocks

**Signature:** `(transcript) -> numpy.ndarray`


### set_canonical_transcripts_for_collection

**Signature:** `(transcripts_collection, canonizer_func: Optional[Callable] = None, **kwargs) -> None`

Set canonical transcripts for all genes in a collection using a canonizer function.


---

# pyrion.core.genome_alignment


## Classes

### GenomeAlignment

GenomeAlignment(chain_id: int, score: int, t_chrom: str, t_strand: int, t_size: int, q_chrom: str, q_strand: int, q_size: int, blocks: numpy.ndarray, child_id: Optional[int] = None)

**Signature:** `(self, chain_id: int, score: int, t_chrom: str, t_strand: int, t_size: int, q_chrom: str, q_strand: int, q_size: int, blocks: numpy.ndarray, child_id: Optional[int] = None) -> None`

#### Methods

**__init__**

*Signature:* `(self, chain_id: int, score: int, t_chrom: str, t_strand: int, t_size: int, q_chrom: str, q_strand: int, q_size: int, blocks: numpy.ndarray, child_id: Optional[int] = None) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**aligned_length**

*Signature:* `(self) -> int`


**blocks_in_query**

*Signature:* `(self) -> numpy.ndarray`


**blocks_in_target**

*Signature:* `(self) -> numpy.ndarray`


**q_length**

*Signature:* `(self) -> int`


**t_length**

*Signature:* `(self) -> int`



### GenomeAlignmentsCollection

Container for many genome alignments.

**Signature:** `(self, alignments: Optional[List[pyrion.core.genome_alignment.GenomeAlignment]] = None, source_file: Optional[str] = None)`

#### Methods

**__init__**

*Signature:* `(self, alignments: Optional[List[pyrion.core.genome_alignment.GenomeAlignment]] = None, source_file: Optional[str] = None)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**__str__**

*Signature:* `(self) -> str`

String representation with summary.


**filter**

*Signature:* `(self, t_chrom: Union[str, List[str], NoneType] = None, q_chrom: Union[str, List[str], NoneType] = None, min_score: Optional[int] = None, max_score: Optional[int] = None, min_aligned_length: Optional[int] = None) -> 'GenomeAlignmentsCollection'`

Filter alignments by target/query chromosomes, score, and aligned length.

All criteria are combined with AND logic. None means no filter on that field.
Chromosome arguments accept a single string or a list/set of strings.

Equivalent to UCSC chainFilter:
    chainFilter -t=chr11,chrX -q=chr19,chr7 -minScore=15000 in.chain
becomes:
    collection.filter(t_chrom=["chr11", "chrX"],
                      q_chrom=["chr19", "chr7"],
                      min_score=15000)


**from_json**

*Signature:* `(file_path: Union[str, pathlib.Path]) -> 'GenomeAlignmentsCollection'`


**get_alignments_fully_contained**

*Signature:* `(self, interval: 'GenomicInterval') -> List[pyrion.core.genome_alignment.GenomeAlignment]`


**get_alignments_in_interval**

*Signature:* `(self, interval: 'GenomicInterval', include_partial: bool = True) -> List[pyrion.core.genome_alignment.GenomeAlignment]`


**get_alignments_overlapping_query_interval**

*Signature:* `(self, interval: 'GenomicInterval', include_partial: bool = True) -> List[pyrion.core.genome_alignment.GenomeAlignment]`


**get_alignments_overlapping_target_interval**

*Signature:* `(self, interval: 'GenomicInterval', include_partial: bool = True) -> List[pyrion.core.genome_alignment.GenomeAlignment]`


**get_by_chain_id**

*Signature:* `(self, chain_id: int) -> Optional[pyrion.core.genome_alignment.GenomeAlignment]`


**get_by_query_chrom**

*Signature:* `(self, chrom: str) -> List[pyrion.core.genome_alignment.GenomeAlignment]`


**get_by_target_chrom**

*Signature:* `(self, chrom: str) -> List[pyrion.core.genome_alignment.GenomeAlignment]`


**get_chain_ids_by_query_chrom**

*Signature:* `(self, chrom: str) -> List[int]`


**get_chain_ids_by_target_chrom**

*Signature:* `(self, chrom: str) -> List[int]`


**get_query_chromosomes**

*Signature:* `(self) -> List[str]`


**get_reference_chromosomes**

*Signature:* `(self) -> List[str]`


**save_to_chain**

*Signature:* `(self, file_path: Union[str, pathlib.Path]) -> None`


**save_to_json**

*Signature:* `(self, file_path: Union[str, pathlib.Path]) -> None`


**sort**

*Signature:* `(self, by: Union[str, List[str]] = 'score', reverse: bool = False) -> 'GenomeAlignmentsCollection'`

Sort alignments in-place and return self for chaining.

Args:
    by: Sort key(s). A single string or list of strings.
        Predefined presets:
            "score"    — sort by alignment score  [default]
            "position" — sort by (t_chrom, t_start)
        Individual keys: "score", "chain_id", "t_chrom", "t_start",
            "q_chrom", "q_start", "aligned_length".
        Multiple keys: ["t_chrom", "t_start"] sorts by target chrom
            first, then target start.
    reverse: If True, sort in descending order.
        Tip: use ``reverse=True`` with ``by="score"`` for highest-first.

Returns:
    self (for chaining, e.g. ``collection.sort("score", reverse=True).save_to_chain(path)``)


**sort_by_score**

*Signature:* `(self, max_elems: Optional[int] = None) -> List[Tuple[int, int]]`


**summary**

*Signature:* `(self) -> str`



---

# pyrion.core.genome_alignment_auxiliary

Auxiliary functions for genome alignment objects.


## Functions

### sort_alignments_by_score

**Signature:** `(alignments_collection, max_elems: Optional[int] = None) -> List[Tuple[int, int]]`


---

# pyrion.core.intervals

Genomic interval representations.


## Classes

### AnnotatedIntervalSet

AnnotatedIntervalSet(intervals: numpy.ndarray, region_types: numpy.ndarray)

**Signature:** `(self, intervals: numpy.ndarray, region_types: numpy.ndarray) -> None`

#### Methods

**__init__**

*Signature:* `(self, intervals: numpy.ndarray, region_types: numpy.ndarray) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).



### GenomicInterval

Single genomic interval with strand information and optional ID.

**Signature:** `(self, chrom: str, start: int, end: int, strand: pyrion.core.strand.Strand = <Strand.UNKNOWN: 0>, id: Optional[str] = None) -> None`

#### Methods

**__init__**

*Signature:* `(self, chrom: str, start: int, end: int, strand: pyrion.core.strand.Strand = <Strand.UNKNOWN: 0>, id: Optional[str] = None) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Detailed representation for debugging.


**__str__**

*Signature:* `(self) -> str`

Return str(self).


**contains**

*Signature:* `(self, pos: int) -> bool`


**flip_strand**

*Signature:* `(self) -> 'GenomicInterval'`


**from_string**

*Signature:* `(interval_string: str, id: Optional[str] = None) -> 'GenomicInterval'`

Create GenomicInterval from string representation.

Supported formats:
- "chr1:100-200" (no strand)
- "chr1:100-200:+" (plus strand)  
- "chr1:100-200:-" (minus strand)
- "chr1:1,000,000-2,000,000" (commas in numbers supported)
- "chr11:118,300,000-118,400,000:+" (full example with commas)


**intersects**

*Signature:* `(self, other: 'GenomicInterval') -> bool`


**length**

*Signature:* `(self) -> int`


**overlap**

*Signature:* `(self, other: 'GenomicInterval') -> int`


**to_bed6_string**

*Signature:* `(self, score: int = 1000) -> str`

Convert to BED6 format string.


**union**

*Signature:* `(self, other: 'GenomicInterval') -> Optional[ForwardRef('GenomicInterval')]`



### GenomicIntervalsCollection

GenomicIntervalsCollection(chrom: str, strand: pyrion.core.strand.Strand, array: numpy.ndarray, ids: numpy.ndarray)

**Signature:** `(self, chrom: str, strand: pyrion.core.strand.Strand, array: numpy.ndarray, ids: numpy.ndarray) -> None`

#### Methods

**__init__**

*Signature:* `(self, chrom: str, strand: pyrion.core.strand.Strand, array: numpy.ndarray, ids: numpy.ndarray) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**__str__**

*Signature:* `(self) -> str`

Return str(self).


**filter_by**

*Signature:* `(self, predicate: Callable[[pyrion.core.intervals.GenomicInterval], bool]) -> 'GenomicIntervalsCollection'`


**from_array**

*Signature:* `(array: numpy.ndarray, chrom: str, strand: Optional[pyrion.core.strand.Strand] = None, ids: Optional[List[str]] = None) -> 'GenomicIntervalsCollection'`

Create collection from numpy array.


**from_intervals**

*Signature:* `(intervals: List[pyrion.core.intervals.GenomicInterval]) -> 'GenomicIntervalsCollection'`

Create collection from list of GenomicInterval objects.


**from_strings**

*Signature:* `(interval_strings, ids: Optional[List[str]] = None) -> Dict[Tuple[str, pyrion.core.strand.Strand], ForwardRef('GenomicIntervalsCollection')]`


**group_by_proximity**

*Signature:* `(self, max_gap: int) -> List[ForwardRef('GenomicIntervalsCollection')]`


**intersect**

*Signature:* `(self, other: Union[ForwardRef('GenomicIntervalsCollection'), pyrion.core.intervals.GenomicInterval]) -> 'GenomicIntervalsCollection'`


**is_empty**

*Signature:* `(self) -> bool`


**merge_close**

*Signature:* `(self, max_gap: int = 0) -> 'GenomicIntervalsCollection'`


**split_on_gaps**

*Signature:* `(self, min_gap: int) -> List[ForwardRef('GenomicIntervalsCollection')]`


**to_bed6_string**

*Signature:* `(self, score: int = 1000) -> str`


**to_intervals_list**

*Signature:* `(self) -> List[pyrion.core.intervals.GenomicInterval]`



### RegionType

Enum where members are also (and must be) ints

**Signature:** `(self, *args, **kwds)`

#### Methods

**__init__**

*Signature:* `(self, *args, **kwds)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self)`

Return repr(self).



---

# pyrion.core.intervals_auxiliary

Auxiliary functions for interval objects.


## Functions

### create_intervals_collections_from_strings

**Signature:** `(interval_strings, ids: Optional[List[str]] = None) -> Dict[Tuple[str, pyrion.core.strand.Strand], pyrion.core.intervals.GenomicIntervalsCollection]`

Create collections from iterable of string representations, grouped by chromosome and strand.


---

# pyrion.core.nucleotide_sequences

Sequence representations and storage.


## Classes

### NucleotideSequence

NucleotideSequence(data: 'np.ndarray', is_rna: 'bool' = False, metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None)

**Signature:** `(self, data: 'np.ndarray', is_rna: 'bool' = False, metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None) -> None`

#### Methods

**__init__**

*Signature:* `(self, data: 'np.ndarray', is_rna: 'bool' = False, metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> 'str'`

Return repr(self).


**__str__**

*Signature:* `(self) -> 'str'`

Return str(self).


**complement**

*Signature:* `(self) -> "'NucleotideSequence'"`


**from_string**

*Signature:* `(sequence: 'str', is_rna: 'bool' = False, metadata: 'Optional[Metadata]' = None, id: 'Optional[str]' = None) -> "'NucleotideSequence'"`


**get_masked_positions**

*Signature:* `(self) -> 'np.ndarray'`


**get_unmasked_positions**

*Signature:* `(self) -> 'np.ndarray'`


**is_position_masked**

*Signature:* `(self, position: 'int') -> 'bool'`


**mask**

*Signature:* `(self, start: 'Optional[int]' = None, end: 'Optional[int]' = None) -> "'NucleotideSequence'"`


**merge**

*Signature:* `(self, other: "'NucleotideSequence'") -> "'NucleotideSequence'"`


**nucleotide_composition**

*Signature:* `(self, consider_masking: 'bool' = False) -> 'dict[str, int]'`


**remove_gaps**

*Signature:* `(self) -> "'NucleotideSequence'"`


**reverse**

*Signature:* `(self) -> "'NucleotideSequence'"`


**reverse_complement**

*Signature:* `(self) -> "'NucleotideSequence'"`


**slice**

*Signature:* `(self, start: 'int', end: 'int') -> "'NucleotideSequence'"`


**to_amino_acids**

*Signature:* `(self, translation_table=None)`


**to_codons**

*Signature:* `(self)`


**to_fasta_string**

*Signature:* `(self, width: 'int' = 80, header: 'Optional[str]' = None) -> 'str'`


**to_string**

*Signature:* `(self) -> 'str'`


**toggle_type**

*Signature:* `(self) -> "'NucleotideSequence'"`

Toggle between DNA and RNA (T <-> U).


**unmask**

*Signature:* `(self, start: 'Optional[int]' = None, end: 'Optional[int]' = None) -> "'NucleotideSequence'"`


#### Properties

**masked_fraction** -> `float`



### SequenceType

Sequence type detection.

Uses integer values for efficient C function calls while maintaining
string compatibility through the string_value property.

**Signature:** `(self, *args, **kwds)`

#### Methods

**__init__**

*Signature:* `(self, *args, **kwds)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self)`

Return repr(self).



---

# pyrion.core.sequences_auxiliary

Auxiliary functions for sequences objects.


## Functions

### get_nucleotide_composition

**Signature:** `(sequence, consider_masking: bool = False) -> Dict[str, int]`


### mask_nucleotide_sequence_slice

**Signature:** `(sequence, start: Optional[int] = None, end: Optional[int] = None)`


### merge_nucleotide_sequences

**Signature:** `(sequence1, sequence2)`


### unmask_nucleotide_sequence_slice

**Signature:** `(sequence, start: Optional[int] = None, end: Optional[int] = None)`


---

# pyrion.core.sequences_collection

SequencesCollection: a clean wrapper over a mapping of sequences.


## Classes

### SequencesCollection

A MutableMapping is a generic container for associating
key/value pairs.

This class provides concrete generic implementations of all
methods except for __getitem__, __setitem__, __delitem__,
__iter__, and __len__.

**Signature:** `(self, data: 'Optional[Mapping[str, SequenceLike]]' = None)`

#### Methods

**__init__**

*Signature:* `(self, data: 'Optional[Mapping[str, SequenceLike]]' = None)`

Initialize self.  See help(type(self)) for accurate signature.


**add**

*Signature:* `(self, key: 'str', value: 'SequenceLike', *, force: 'bool' = False) -> 'None'`

Add a sequence. If key exists and force=False, raise; if force=True, overwrite.


**as_alignment**

*Signature:* `(self, *, inplace: 'bool' = False) -> "'SequencesCollection'"`

Validate equal lengths and mark as alignment.

If `inplace` is False (default), returns a new aligned collection.
If `inplace` is True, sets the alignment flag on this instance and returns self.


**clear**

*Signature:* `(self)`

D.clear() -> None.  Remove all items from D.


**delete**

*Signature:* `(self, key: 'str') -> 'None'`

Remove a sequence by key.


**from_dict**

*Signature:* `(data: 'Mapping[str, SequenceLike]') -> "'SequencesCollection'"`


**from_list**

*Signature:* `(sequences: 'Iterable[SequenceLike]') -> "'SequencesCollection'"`


**get**

*Signature:* `(self, key, default=None)`

D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.


**ids**

*Signature:* `(self) -> 'List[str]'`


**items**

*Signature:* `(self)`

D.items() -> a set-like object providing a view on D's items


**keys**

*Signature:* `(self)`

D.keys() -> a set-like object providing a view on D's keys


**pop**

*Signature:* `(self, key, default=<object object at 0x10479c1d0>)`

D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
If key is not found, d is returned if given, otherwise KeyError is raised.


**popitem**

*Signature:* `(self)`

D.popitem() -> (k, v), remove and return some (key, value) pair
as a 2-tuple; but raise KeyError if D is empty.


**sequences**

*Signature:* `(self) -> 'List[SequenceLike]'`


**setdefault**

*Signature:* `(self, key, default=None)`

D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D


**slice**

*Signature:* `(self, start: 'int', end: 'int') -> "'SequencesCollection'"`

Slice all sequences consistently. Requires aligned collection.


**update**

*Signature:* `(self, other=(), /, **kwds)`

D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
If E present and has a .keys() method, does:     for k in E.keys(): D[k] = E[k]
If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
In either case, this is followed by: for k, v in F.items(): D[k] = v


**values**

*Signature:* `(self)`

D.values() -> an object providing a view on D's values


#### Properties

**is_alignment** -> `bool`


**sequence_type** -> `Optional[SequenceType]`



---

# pyrion.core.strand


## Classes

### Strand

Enum where members are also (and must be) ints

**Signature:** `(self, *args, **kwds)`

#### Methods

**__init__**

*Signature:* `(self, *args, **kwds)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self)`

Return repr(self).


**__str__**

*Signature:* `(self) -> 'str'`

Return repr(self).



---

# pyrion.core.translation

Translation tables for genetic code.


## Classes

### TranslationTable

TranslationTable(table_id: int, name: str, codon_table: Dict[tuple, int], start_codons: set[tuple], stop_codons: set[tuple])

**Signature:** `(self, table_id: int, name: str, codon_table: Dict[tuple, int], start_codons: set[tuple], stop_codons: set[tuple]) -> None`

#### Methods

**__init__**

*Signature:* `(self, table_id: int, name: str, codon_table: Dict[tuple, int], start_codons: set[tuple], stop_codons: set[tuple]) -> None`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**is_start_codon**

*Signature:* `(self, codon_codes: Tuple[int, int, int]) -> bool`


**is_stop_codon**

*Signature:* `(self, codon_codes: Tuple[int, int, int]) -> bool`


**mitochondrial**

*Signature:* `() -> 'TranslationTable'`

Mitochondrial genetic code (NCBI table 2).


**standard**

*Signature:* `() -> 'TranslationTable'`

Standard genetic code (NCBI table 1).


**translate_codon**

*Signature:* `(self, codon_codes: Tuple[int, int, int]) -> int`



---

# pyrion.core_types

Shared types, enums, and protocols for pyrion.


## Classes

### ExonType

Enumeration for exon types in genomic annotations.

**Signature:** `(self, *args, **kwds)`


---

# pyrion.io

I/O modules for various genomic file formats.


---

# pyrion.io.bed

BED format I/O support.


## Functions

### read_bed12_file

**Signature:** `(file_path: Union[str, pathlib.Path]) -> pyrion.core.genes.TranscriptsCollection`

Read BED12 file and return TranscriptsCollection.


### read_narrow_bed_file

**Signature:** `(file_path: Union[str, pathlib.Path]) -> List[pyrion.core.intervals.GenomicInterval]`

Read a narrow BED file with 3-9 fields and return a list of GenomicInterval objects.


---

# pyrion.io.chain

Chain format I/O support.

This reader streams large chain files and parses them in batches to avoid
exceeding the C-extension limit on number of chunks per call and to reduce
peak memory usage. The public API remains unchanged.


## Functions

### read_chain_file

**Signature:** `(file_path: Union[str, pathlib.Path], min_score: Optional[int] = None) -> pyrion.core.genome_alignment.GenomeAlignmentsCollection`

Read a .chain or .chain.gz file and return parsed alignments.

Internally parses in batches (<= 1_000_000 chunks per call) to satisfy the
C-extension limit and to keep memory bounded for very large files.


---

# pyrion.io.chrom_sizes

Read and write .chrom.sizes files (two-column TSV: chrom_name   size).


## Functions

### read_chrom_sizes

**Signature:** `(path: Union[str, pathlib.Path]) -> Dict[str, int]`

Read a chrom.sizes file into a dict.

Format: tab-separated, one chromosome per line.
Lines starting with '#' are skipped.


### write_chrom_sizes

**Signature:** `(chrom_sizes: Dict[str, int], path: Union[str, pathlib.Path]) -> None`

Write a chrom_sizes dict to a two-column TSV file.


---

# pyrion.io.fai

FASTA indexing functionality using fast C extension.


## Functions

### create_fasta_index

**Signature:** `(fasta_file: 'Union[str, Path]', fai_file: 'Optional[Union[str, Path]]' = None) -> 'FaiStore'`


### get_or_create_fasta_index

**Signature:** `(fasta_file: 'Union[str, Path]', force_recreate: 'bool' = False) -> 'FaiStore'`


### load_fasta_index

**Signature:** `(fai_file: 'Union[str, Path]') -> 'FaiStore'`


---

# pyrion.io.fasta

FASTA I/O operations.


## Classes

### FastaAccessor

**Signature:** `(self, fasta_file: 'Union[str, Path]', fai_store: 'FaiStore')`

#### Methods

**__init__**

*Signature:* `(self, fasta_file: 'Union[str, Path]', fai_store: 'FaiStore')`

Initialize FastaAccessor with FASTA file and index.


**__repr__**

*Signature:* `(self) -> 'str'`

Return repr(self).


**get_multiple_sequences**

*Signature:* `(self, regions: 'List[GenomicInterval]', is_rna: 'bool' = False) -> 'Dict[str, NucleotideSequence]'`


**get_sequence**

*Signature:* `(self, region: 'GenomicInterval', is_rna: 'bool' = False) -> 'NucleotideSequence'`


**get_sequence_length**

*Signature:* `(self, sequence_name: 'str') -> 'int'`


**get_sequence_names**

*Signature:* `(self) -> 'List[str]'`


**has_sequence**

*Signature:* `(self, sequence_name: 'str') -> 'bool'`



## Functions

### read_dna_fasta

**Signature:** `(filename: 'Union[str, Path]', **kwargs) -> 'SequencesCollection'`


### read_fasta

**Signature:** `(filename: 'Union[str, Path]', sequence_type: 'SequenceType', return_dict: 'bool' = True) -> 'Union[SequencesCollection, List[Union[NucleotideSequence, AminoAcidSequence]]]'`


### read_protein_fasta

**Signature:** `(filename: 'Union[str, Path]', **kwargs) -> 'SequencesCollection'`

Read protein sequences from FASTA file.


### read_rna_fasta

**Signature:** `(filename: 'Union[str, Path]', **kwargs) -> 'SequencesCollection'`


### write_fasta

**Signature:** `(sequences: 'Union[Mapping[str, NucleotideSequence], List[NucleotideSequence]]', filename: 'Union[str, Path]', line_width: 'int' = 80) -> 'None'`


---

# pyrion.io.gene_data

Gene data I/O support.


## Functions

### read_gene_data

**Signature:** `(file_path: Union[str, pathlib.Path], gene_column: Union[int, str, NoneType] = None, transcript_id_column: Union[int, str, NoneType] = None, gene_name_column: Union[int, str, NoneType] = None, transcript_type_column: Union[int, str, NoneType] = None, separator: str = '\t', has_header: bool = True) -> pyrion.core.gene_data.GeneData`

Read gene data from TSV/CSV file and build mappings.


### resolve_index

**Signature:** `(column_idx: Union[int, str], header: List[str]) -> int | None`


### write_gene_data_tsv

**Signature:** `(gene_data: pyrion.core.gene_data.GeneData, file_path: Union[str, pathlib.Path], include_gene_transcript: bool = True, include_transcript_biotype: bool = True, include_gene_name: bool = True, separator: str = '\t') -> None`


---

# pyrion.io.genepred

GenePred format I/O support.


## Functions

### read_genepred_file

**Signature:** `(file_path: Union[str, pathlib.Path], has_header: bool = False, extended: bool = False) -> pyrion.core.genes.TranscriptsCollection`

Read genePred file and return TranscriptsCollection.


### read_refflat_file

**Signature:** `(file_path: Union[str, pathlib.Path], has_header: bool = False) -> pyrion.core.genes.TranscriptsCollection`

Read refFlat file and return TranscriptsCollection.

refFlat format is like genePred but with an additional first column for gene name:
geneName name chrom strand txStart txEnd cdsStart cdsEnd exonCount exonStarts exonEnds.


---

# pyrion.io.gtf

High-performance GTF format I/O support using C extension.


## Classes

### GTFChunkReader

**Signature:** `(self, file_path: Union[str, pathlib.Path], chunk_size_mb: int = 512)`

#### Methods

**__init__**

*Signature:* `(self, file_path: Union[str, pathlib.Path], chunk_size_mb: int = 512)`

Initialize self.  See help(type(self)) for accurate signature.


**read_gene_chunks**

*Signature:* `(self) -> Iterator[List[str]]`



## Functions

### read_gtf

**Signature:** `(file_path: Union[str, pathlib.Path], chunk_size_mb: int = 512) -> pyrion.core.genes.TranscriptsCollection`


---

# pyrion.io.twobit

2bit file format support.


## Classes

### TwoBitAccessor

Access sequences from 2bit files using py2bit.

**Signature:** `(self, file_path: str)`

#### Methods

**__init__**

*Signature:* `(self, file_path: str)`

Initialize self.  See help(type(self)) for accurate signature.


**__repr__**

*Signature:* `(self) -> str`

Return repr(self).


**chrom_names**

*Signature:* `(self) -> List[str]`


**chrom_sizes**

*Signature:* `(self) -> Dict[str, int]`


**close**

*Signature:* `(self)`


**fetch**

*Signature:* `(self, chrom: str, start: Optional[int] = None, end: Optional[int] = None, strand: pyrion.core.strand.Strand = <Strand.PLUS: 1>) -> pyrion.core.nucleotide_sequences.NucleotideSequence`


**fetch_interval**

*Signature:* `(self, interval: pyrion.core.intervals.GenomicInterval) -> pyrion.core.nucleotide_sequences.NucleotideSequence`


**list_chromosomes**

*Signature:* `(self) -> None`


**validate_interval**

*Signature:* `(self, chrom: str, start: int, end: int) -> bool`



---

# pyrion.ops

Pyrion operations module.


---

# pyrion.ops.chain_serialization

Genome alignment serialization operations for chain format and JSON.


## Functions

### genome_alignment_from_dict

**Signature:** `(data: Dict[str, Any]) -> pyrion.core.genome_alignment.GenomeAlignment`


### genome_alignment_to_chain_string

**Signature:** `(alignment: pyrion.core.genome_alignment.GenomeAlignment) -> str`

Convert a single GenomeAlignment to chain format string.

Chain format:
chain {score} {t_chrom} {t_size} {t_strand} {t_start} {t_end} {q_chrom} {q_size} {q_strand} {q_start} {q_end} {chain_id}
{block_size} {dt} {dq}
...
{final_block_size}


### genome_alignment_to_dict

**Signature:** `(alignment: pyrion.core.genome_alignment.GenomeAlignment) -> Dict[str, Any]`


### genome_alignments_collection_from_dict

**Signature:** `(data: Dict[str, Any]) -> pyrion.core.genome_alignment.GenomeAlignmentsCollection`


### genome_alignments_collection_summary_string

**Signature:** `(collection: pyrion.core.genome_alignment.GenomeAlignmentsCollection) -> str`


### genome_alignments_collection_to_chain_string

**Signature:** `(collection: pyrion.core.genome_alignment.GenomeAlignmentsCollection) -> str`


### genome_alignments_collection_to_dict

**Signature:** `(collection: pyrion.core.genome_alignment.GenomeAlignmentsCollection) -> Dict[str, Any]`


### load_genome_alignments_collection_from_json

**Signature:** `(file_path: Union[str, pathlib.Path]) -> pyrion.core.genome_alignment.GenomeAlignmentsCollection`


### save_genome_alignments_collection_to_chain

**Signature:** `(collection: pyrion.core.genome_alignment.GenomeAlignmentsCollection, file_path: Union[str, pathlib.Path]) -> None`


### save_genome_alignments_collection_to_json

**Signature:** `(collection: pyrion.core.genome_alignment.GenomeAlignmentsCollection, file_path: Union[str, pathlib.Path]) -> None`


---

# pyrion.ops.chain_slicing

Chain slicing operations with proper Q strand handling.


## Functions

### remove_chain_region_target_space

**Signature:** `(chain: pyrion.core.genome_alignment.GenomeAlignment, start: int, end: int, use_numba: bool = True) -> pyrion.core.genome_alignment.GenomeAlignment`


### slice_chain_query_space

**Signature:** `(chain: pyrion.core.genome_alignment.GenomeAlignment, start: int, end: int, use_numba: bool = True) -> pyrion.core.genome_alignment.GenomeAlignment`


### slice_chain_target_space

**Signature:** `(chain: pyrion.core.genome_alignment.GenomeAlignment, start: int, end: int, use_numba: bool = True) -> pyrion.core.genome_alignment.GenomeAlignment`


---

# pyrion.ops.chains

Chain alignment operations for projecting genomic intervals.


## Functions

### get_chain_q_end

**Signature:** `(genome_alignment) -> int`


### get_chain_q_start

**Signature:** `(genome_alignment) -> int`


### get_chain_query_interval

**Signature:** `(genome_alignment) -> pyrion.core.intervals.GenomicInterval`


### get_chain_t_end

**Signature:** `(genome_alignment) -> int`


### get_chain_t_start

**Signature:** `(genome_alignment) -> int`


### get_chain_target_interval

**Signature:** `(genome_alignment) -> pyrion.core.intervals.GenomicInterval`


### project_intervals_through_chain

**Signature:** `(intervals: numpy.ndarray, chain_blocks: numpy.ndarray, q_strand: int = 1) -> List[numpy.ndarray]`


### project_intervals_through_chain_strict

**Signature:** `(intervals: numpy.ndarray, chain_blocks: numpy.ndarray, q_strand: int = 1) -> List[numpy.ndarray]`

Stricter projection that respects alignment structure and deletions.

Logic:
1. If interval overlaps aligned blocks:
   - For each terminus (start/end):
     * If in aligned block: project directly
     * If in misaligned region: extend from nearest internal block, BUT limited by
       actual query sequence length between blocks (handles deletions)
     * If in deletion: don't extend, use closest internal block boundary

2. If interval is fully within deletion: return [[0, 0]]

3. If interval has no overlapping blocks (complete misalignment):
   - Find flanking blocks (before and after)
   - If query distance between flanks <= target interval length: return that query interval
   - Otherwise: return [[0, 0]]

Args:
    intervals: Array of intervals to project, shape (N, 2)
    chain_blocks: Chain alignment blocks, shape (M, 4) with [t_start, t_end, q_start, q_end]
    q_strand: Query strand (1 for plus, -1 for minus). For minus-strand chains,
        within-block projection direction is reversed (anti-parallel alignment).

Returns:
    List of projected intervals. Returns [[0, 0]] if interval can't be reliably projected.


### project_intervals_through_genome_alignment

**Signature:** `(intervals: numpy.ndarray, genome_alignment) -> List[numpy.ndarray]`

Convenience function to project intervals through a GenomeAlignment object.


### project_intervals_through_genome_alignment_to_intervals

**Signature:** `(intervals: numpy.ndarray, genome_alignment, target_chrom: Optional[str] = None, target_strand: Optional[pyrion.core.strand.Strand] = None) -> List[pyrion.core.intervals.GenomicInterval]`

Project intervals through genome alignment and convert to GenomicInterval objects.

Args:
    intervals: Array of intervals to project, shape (N, 2)
    genome_alignment: GenomeAlignment object to project through
    target_chrom: Target chromosome name (auto-detected if None)
    target_strand: Target strand (auto-detected if None)


### project_transcript_through_chain

**Signature:** `(transcript: pyrion.core.genes.Transcript, chain: pyrion.core.genome_alignment.GenomeAlignment, only_cds=False) -> Optional[pyrion.core.intervals.GenomicInterval]`


### split_genome_alignment

**Signature:** `(chain: pyrion.core.genome_alignment.GenomeAlignment, intersected_transcripts: List[pyrion.core.genes.Transcript], window_size: int = 1000000, intergenic_margin: int = 10000) -> Tuple[List[pyrion.core.genome_alignment.GenomeAlignment], Dict[int, List[str]]]`


---

# pyrion.ops.data_consistency

Data consistency checking utilities.


## Functions

### check_data_consistency

**Signature:** `(transcripts_collection: pyrion.core.genes.TranscriptsCollection, detailed: bool = False) -> str`

Check data consistency in a transcripts collection.

Analyzes the consistency of applied gene data mappings and reports issues:
- Transcripts without gene IDs (if gene-transcript mapping was applied)
- Transcripts without biotypes (if biotype mapping was applied)
- Genes without names (if gene names were applied)


---

# pyrion.ops.entity_ops

Entity-specific operations for Transcripts and GenomeAlignments using low-level interval operations.


## Functions

### find_alignment_gaps

**Signature:** `(alignment: pyrion.core.genome_alignment.GenomeAlignment, space: str = 'target', use_numba: bool = True) -> numpy.ndarray`

Find gaps in a genome alignment.

Args:
    alignment: GenomeAlignment object
    space: "target" or "query" - which coordinate space to find gaps in
    use_numba: Whether to use numba-optimized operations
    
Returns:
    Array of gap intervals


### find_transcript_overlaps

**Signature:** `(transcript1: pyrion.core.genes.Transcript, transcript2: pyrion.core.genes.Transcript, region_type: str = 'exon', use_numba: bool = True) -> numpy.ndarray`

Find overlaps between specific regions of two transcripts.


### get_transcript_cds_in_range

**Signature:** `(transcript: pyrion.core.genes.Transcript, start: int, end: int, use_numba: bool = True) -> numpy.ndarray`

Get CDS blocks within a specific genomic range using slice operations.


### get_transcript_introns_in_range

**Signature:** `(transcript: pyrion.core.genes.Transcript, start: int, end: int, use_numba: bool = True) -> numpy.ndarray`

Get intron blocks within a specific genomic range.


### get_transcript_utrs_in_range

**Signature:** `(transcript: pyrion.core.genes.Transcript, start: int, end: int, utr_type: str = 'both', use_numba: bool = True) -> numpy.ndarray`

Get UTR blocks within a specific genomic range.


### intersect_alignment_with_intervals

**Signature:** `(alignment: pyrion.core.genome_alignment.GenomeAlignment, intervals: numpy.ndarray, space: str = 'target', use_numba: bool = True) -> numpy.ndarray`

Find intersections between alignment blocks and given intervals.

Args:
    alignment: GenomeAlignment object
    intervals: Array of intervals to intersect with, shape (N, 2)
    space: "target" or "query" - which coordinate space to use
    use_numba: Whether to use numba-optimized operations
    
Returns:
    Array of intersection intervals


### merge_genome_alignments

**Signature:** `(alignments: List[pyrion.core.genome_alignment.GenomeAlignment], space: str = 'target', use_numba: bool = True) -> numpy.ndarray`

Merge blocks from multiple genome alignments.


### merge_transcript_cds

**Signature:** `(transcripts: List[pyrion.core.genes.Transcript], use_numba: bool = True) -> numpy.ndarray`

Merge CDS blocks from multiple transcripts.


### merge_transcript_utrs

**Signature:** `(transcripts: List[pyrion.core.genes.Transcript], utr_type: str = 'both', use_numba: bool = True) -> numpy.ndarray`

Merge UTR blocks from multiple transcripts.


### subtract_transcript_regions

**Signature:** `(transcript: pyrion.core.genes.Transcript, subtract_regions: numpy.ndarray, region_type: str = 'exon', use_numba: bool = True) -> numpy.ndarray`

Subtract regions from specific parts of a transcript.


---

# pyrion.ops.genes

Gene and transcript operations.


## Classes

### SequenceAccessor

Protocol for sequence accessors (TwoBitAccessor, FastaAccessor).

**Signature:** `(self, *args, **kwargs)`

#### Methods

**__init__**

*Signature:* `(self, *args, **kwargs)`


**fetch**

*Signature:* `(self, chrom: str, start: int, end: int, strand: pyrion.core.strand.Strand) -> pyrion.core.nucleotide_sequences.NucleotideSequence`

Fetch sequence from chrom:start-end.



## Functions

### extract_cds_sequence

**Signature:** `(transcript: pyrion.core.genes.Transcript, accessor: pyrion.ops.genes.SequenceAccessor) -> pyrion.core.nucleotide_sequences.NucleotideSequence`


### extract_exon_sequence

**Signature:** `(transcript: pyrion.core.genes.Transcript, accessor: pyrion.ops.genes.SequenceAccessor) -> pyrion.core.nucleotide_sequences.NucleotideSequence`


### extract_intron_sequence

**Signature:** `(transcript: pyrion.core.genes.Transcript, accessor: pyrion.ops.genes.SequenceAccessor) -> pyrion.core.nucleotide_sequences.NucleotideSequence`

Extract concatenated intron sequences from a transcript.


### extract_utr3_sequence

**Signature:** `(transcript: pyrion.core.genes.Transcript, accessor: pyrion.ops.genes.SequenceAccessor) -> pyrion.core.nucleotide_sequences.NucleotideSequence`


### extract_utr5_sequence

**Signature:** `(transcript: pyrion.core.genes.Transcript, accessor: pyrion.ops.genes.SequenceAccessor) -> pyrion.core.nucleotide_sequences.NucleotideSequence`


### merge_transcript_intervals

**Signature:** `(transcripts: List[pyrion.core.genes.Transcript], cds_only: bool = False, use_numba: bool = True) -> List[pyrion.core.intervals.GenomicInterval]`

Merge overlapping or adjacent intervals from multiple transcripts.


---

# pyrion.ops.interval_collection_ops

Bulk operations for GenomicIntervalsCollection using vectorized numpy operations.


## Functions

### create_collections_from_mixed_intervals

**Signature:** `(intervals: List[pyrion.core.intervals.GenomicInterval], consider_strand: bool = False) -> List[pyrion.core.intervals.GenomicIntervalsCollection]`


### filter_collection

**Signature:** `(collection: pyrion.core.intervals.GenomicIntervalsCollection, predicate: Callable[[pyrion.core.intervals.GenomicInterval], bool]) -> pyrion.core.intervals.GenomicIntervalsCollection`


### group_intervals_by_proximity

**Signature:** `(collection: pyrion.core.intervals.GenomicIntervalsCollection, max_gap: int) -> List[pyrion.core.intervals.GenomicIntervalsCollection]`


### intersect_collections

**Signature:** `(collection: pyrion.core.intervals.GenomicIntervalsCollection, other: Union[pyrion.core.intervals.GenomicIntervalsCollection, pyrion.core.intervals.GenomicInterval]) -> pyrion.core.intervals.GenomicIntervalsCollection`


### merge_close_intervals

**Signature:** `(collection: pyrion.core.intervals.GenomicIntervalsCollection, max_gap: int = 0) -> pyrion.core.intervals.GenomicIntervalsCollection`


### split_intervals_on_gaps

**Signature:** `(collection: pyrion.core.intervals.GenomicIntervalsCollection, min_gap: int) -> List[pyrion.core.intervals.GenomicIntervalsCollection]`


---

# pyrion.ops.interval_ops

Additional low-level interval operations for merge, intersection, etc.


## Functions

### intersect_intervals

**Signature:** `(intervals1: numpy.ndarray, intervals2: numpy.ndarray, use_numba: bool = True) -> numpy.ndarray`


### intervals_union

**Signature:** `(intervals_list: List[numpy.ndarray], use_numba: bool = True) -> numpy.ndarray`


### merge_intervals

**Signature:** `(intervals: numpy.ndarray, use_numba: bool = None) -> numpy.ndarray`


### subtract_intervals

**Signature:** `(intervals1: numpy.ndarray, intervals2: numpy.ndarray, use_numba: bool = True) -> numpy.ndarray`


---

# pyrion.ops.interval_serialization

Genomic interval serialization operations for BED6 format.


## Functions

### genomic_interval_to_bed6_string

**Signature:** `(interval: pyrion.core.intervals.GenomicInterval, score: int = 1000) -> str`

Convert a single GenomicInterval to BED6 format string.


### genomic_intervals_to_bed6_string

**Signature:** `(intervals: List[pyrion.core.intervals.GenomicInterval], score: int = 1000) -> str`


### save_genomic_intervals_to_bed6

**Signature:** `(intervals: List[pyrion.core.intervals.GenomicInterval], file_path: Union[str, pathlib.Path], score: int = 1000) -> None`


---

# pyrion.ops.interval_slicing

Low-level interval slicing and manipulation operations.


## Functions

### invert_intervals

**Signature:** `(intervals: numpy.ndarray, span_start: int, span_end: int, use_numba: bool = None) -> numpy.ndarray`

Get the inverse (gaps) of intervals within a given span.
    
Example:
    exons = [[100, 150], [200, 210], [400, 600]]
    invert_intervals(exons, 50, 700) -> [[50, 100], [150, 200], [210, 400], [600, 700]]


### remove_intervals

**Signature:** `(intervals: numpy.ndarray, remove_start: int, remove_end: int, use_numba: bool = None) -> numpy.ndarray`

Remove a region from intervals, potentially splitting them.
    
Example:
    blocks = [[10, 100], [150, 300]]
    remove_intervals(blocks, 50, 200) -> [[10, 50], [200, 300]]


### slice_intervals

**Signature:** `(intervals: numpy.ndarray, slice_start: int, slice_end: int, use_numba: bool = None) -> numpy.ndarray`

Slice intervals to get only parts that intersect with [slice_start, slice_end).

Example:
    blocks = [[10, 30], [100, 150], [200, 210], [400, 600]]
    slice_intervals(blocks, 40, 450) -> [[100, 150], [200, 210], [400, 450]]


---

# pyrion.ops.intervals

Interval operations for pyrion.


## Functions

### array_to_intervals

**Signature:** `(array: numpy.ndarray, chrom: str) -> List`

Convert 2D numpy array of [start, end] pairs to list of GenomicInterval objects.


### chains_to_arrays

**Signature:** `(chains: List, for_q: bool = False) -> Tuple[numpy.ndarray, numpy.ndarray]`


### compute_overlap_size

**Signature:** `(start1: int, end1: int, start2: int, end2: int) -> int`


### find_intersections

**Signature:** `(arr1: numpy.ndarray, arr2: numpy.ndarray, ids1: Optional[List] = None, ids2: Optional[List] = None) -> Dict[Any, List]`

Find intersections between two arrays of intervals.


### intervals_to_array

**Signature:** `(intervals: List) -> numpy.ndarray`

Convert list of GenomicInterval objects to 2D numpy array of [start, end] pairs.


### projected_intervals_to_genomic_intervals

**Signature:** `(projected_arrays: List[numpy.ndarray], target_chrom: str, target_strand: pyrion.core.strand.Strand = <Strand.UNKNOWN: 0>, ids: Optional[List[str]] = None) -> List[List[pyrion.core.intervals.GenomicInterval]]`

Convert projected interval arrays to GenomicInterval objects.

Convenience function to convert the output of project_intervals_through_genome_alignment
into GenomicInterval objects.


### transcripts_to_arrays

**Signature:** `(transcripts: List) -> Tuple[numpy.ndarray, numpy.ndarray]`


---

# pyrion.ops.sequence_serialization

Sequence serialization operations for FASTA format.


## Functions

### amino_acid_sequence_to_fasta_string

**Signature:** `(sequence: pyrion.core.amino_acid_sequences.AminoAcidSequence, width: int = 80, header: Optional[str] = None) -> str`


### codon_sequence_to_fasta_string

**Signature:** `(sequence: pyrion.core.codons.CodonSequence, width: int = 80, header: Optional[str] = None) -> str`


### format_fasta_sequence

**Signature:** `(sequence_string: str, width: int = 80) -> str`

Format sequence string with specified line width.


### get_sequence_header

**Signature:** `(sequence: Any, index: Optional[int] = None) -> str`

Extract or generate FASTA header for a sequence object.


### nucleotide_sequence_to_fasta_string

**Signature:** `(sequence: pyrion.core.nucleotide_sequences.NucleotideSequence, width: int = 80, header: Optional[str] = None) -> str`


### save_amino_acid_sequence_to_fasta

**Signature:** `(sequence: pyrion.core.amino_acid_sequences.AminoAcidSequence, file_path: Union[str, pathlib.Path], width: int = 80, header: Optional[str] = None) -> None`

Save a single AminoAcidSequence to a FASTA file.


### save_nucleotide_sequence_to_fasta

**Signature:** `(sequence: pyrion.core.nucleotide_sequences.NucleotideSequence, file_path: Union[str, pathlib.Path], width: int = 80, header: Optional[str] = None) -> None`

Save a single NucleotideSequence to a FASTA file.


### save_sequences_to_fasta

**Signature:** `(sequences: List[Any], file_path: Union[str, pathlib.Path], width: int = 80) -> None`


### sequence_to_fasta_string

**Signature:** `(sequence: Any, width: int = 80, header: Optional[str] = None) -> str`


### sequences_to_fasta_string

**Signature:** `(sequences: List[Any], width: int = 80) -> str`


---

# pyrion.ops.transcript_serialization

Transcript serialization operations for BED12 and JSON formats.


## Functions

### load_transcripts_collection_from_json

**Signature:** `(file_path: Union[str, pathlib.Path]) -> pyrion.core.genes.TranscriptsCollection`


### save_transcripts_collection_to_bed12

**Signature:** `(collection: pyrion.core.genes.TranscriptsCollection, file_path: Union[str, pathlib.Path]) -> None`


### save_transcripts_collection_to_json

**Signature:** `(collection: pyrion.core.genes.TranscriptsCollection, file_path: Union[str, pathlib.Path]) -> None`


### transcript_from_dict

**Signature:** `(data: Dict[str, Any]) -> pyrion.core.genes.Transcript`


### transcript_to_bed12_string

**Signature:** `(transcript: pyrion.core.genes.Transcript) -> str`


### transcript_to_dict

**Signature:** `(transcript: pyrion.core.genes.Transcript) -> Dict[str, Any]`


### transcripts_collection_from_dict

**Signature:** `(data: Dict[str, Any]) -> pyrion.core.genes.TranscriptsCollection`


### transcripts_collection_summary_string

**Signature:** `(collection: pyrion.core.genes.TranscriptsCollection) -> str`


### transcripts_collection_to_bed12_string

**Signature:** `(collection: pyrion.core.genes.TranscriptsCollection) -> str`


### transcripts_collection_to_dict

**Signature:** `(collection: pyrion.core.genes.TranscriptsCollection) -> Dict[str, Any]`


---

# pyrion.ops.transcript_slicing

Transcript slicing operations.


## Functions

### get_transcript_introns

**Signature:** `(transcript: pyrion.core.genes.Transcript, use_numba: bool = True) -> numpy.ndarray`

Get intron blocks (gaps between exons) within transcript span.


### remove_transcript_region

**Signature:** `(transcript: pyrion.core.genes.Transcript, start: int, end: int, use_numba: bool = True) -> pyrion.core.genes.Transcript`

Remove a region from transcript, potentially splitting blocks.

Args:
    transcript: Transcript object
    start: Start position to remove (inclusive)
    end: End position to remove (exclusive)
    use_numba: Whether to use numba-optimized operations

Returns:
    New Transcript with region removed


### slice_transcript

**Signature:** `(transcript: pyrion.core.genes.Transcript, start: int, end: int, use_numba: bool = True) -> pyrion.core.genes.Transcript`

Slice transcript to get only blocks that intersect with [start, end).


---

# pyrion.ops.transformations

Data transformation utilities for converting between different genomic data types.


## Functions

### bed_to_transcripts

**Signature:** `(bed_file_path: str) -> pyrion.core.genes.TranscriptsCollection`


### intervals_to_transcripts

**Signature:** `(intervals: List[pyrion.core.intervals.GenomicInterval], source_file: Optional[str] = None) -> pyrion.core.genes.TranscriptsCollection`

Convert a list of GenomicInterval objects to a TranscriptsCollection.

May be helpful if bed-6 formatted data is needed as is was bed-12.


### remap_transcript_ids

**Signature:** `(collection: pyrion.core.genes.TranscriptsCollection, id_mapping: Union[Dict[str, str], Callable[[str], str]], source_file: Optional[str] = None) -> pyrion.core.genes.TranscriptsCollection`

Build a new TranscriptsCollection with the same transcripts but new IDs.

Transcript IDs are immutable (Transcript is a frozen dataclass), so this
creates new Transcript instances that are copies except for the id field,
and returns a new collection containing them.

Args:
    collection: The source TranscriptsCollection.
    id_mapping: Either a dict (old_id -> new_id) or a callable that takes
        the old transcript id and returns the new one.
    source_file: Optional source_file for the new collection. If None,
        the original collection's source_file is not carried over.

Returns:
    A new TranscriptsCollection with the same transcripts and remapped IDs.

Example:
    # Prefix every ID
    new_coll = remap_transcript_ids(coll, lambda tid: f"custom_{tid}")

    # Explicit mapping
    new_coll = remap_transcript_ids(coll, {"ENST1": "my_ENST1", "ENST2": "my_ENST2"})


---

# pyrion.utils

Utility modules for pyrion.


---

# pyrion.utils.amino_acid_encoding

Amino acid encoding utilities using prime-based multiplicative semantics.


## Functions

### apply_masking_aa

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Apply masking using multiplicative semantics (multiply by -1, gaps stay 0).


### decode_amino_acids

**Signature:** `(encoded: numpy.ndarray) -> str`

Decode int8 array to amino acid sequence using prime-based multiplicative semantics.


### encode_amino_acids

**Signature:** `(sequence: str) -> numpy.ndarray`

Encode amino acid sequence to int8 array using prime-based multiplicative semantics.


### get_masking_status_aa

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Get boolean array indicating which positions are masked.


### is_gap

**Signature:** `(code: int) -> bool`

Check if code represents a gap.


### is_masked

**Signature:** `(code: int) -> bool`

Check if amino acid is masked (negative and not 0).


### is_stop

**Signature:** `(code: int) -> bool`

Check if code represents a stop codon.


### is_unknown

**Signature:** `(code: int) -> bool`

Check if code represents an unknown amino acid.


### mask

**Signature:** `(code: int) -> int`

Apply masking by multiplying by -1.


### remove_masking_aa

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Remove masking using multiplicative semantics (take absolute value).


### unmask

**Signature:** `(code: int) -> int`

Remove masking by taking absolute value.


---

# pyrion.utils.encoding

Encoding utilities for nucleotides using multiplicative semantics.


## Functions

### apply_complement

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Apply complement using multiplicative semantics (multiply by -1).


### apply_masking

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Apply masking using multiplicative semantics (multiply by 5, gaps stay 0).


### complement

**Signature:** `(code: int) -> int`

Get complement by multiplying by -1.


### decode_nucleotides

**Signature:** `(encoded: numpy.ndarray, is_rna: bool = False) -> str`

Decode int8 array to nucleotide sequence using multiplicative semantics.


### encode_nucleotides

**Signature:** `(sequence: str) -> numpy.ndarray`

Encode nucleotide sequence to int8 array using multiplicative semantics.


### get_masking_status

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Get boolean array indicating which positions are masked.


### is_frameshift

**Signature:** `(code: int) -> bool`

Check if code represents a frameshift.


### is_gap

**Signature:** `(code: int) -> bool`

Check if code represents a gap.


### is_masked

**Signature:** `(code: int) -> bool`

Check if nucleotide is masked using multiplicative test.


### mask

**Signature:** `(code: int) -> int`

Apply masking by multiplying by 5.


### remove_masking

**Signature:** `(encoded: numpy.ndarray) -> numpy.ndarray`

Remove masking using multiplicative semantics.


### unmask

**Signature:** `(code: int) -> int`

Remove masking by dividing by 5.


---

# pyrion.utils.numpy_utils


---

# pyrion.visualization

The visualization module was quickly prototyped in Cursor without thorough design.

A cleaner architecture and improved visuals are planned for a future release.


## Classes

### AlignmentFeature

Wrapper for GenomeAlignment.

**Signature:** `(self, alignment: pyrion.core.genome_alignment.GenomeAlignment)`

#### Methods

**__init__**

*Signature:* `(self, alignment: pyrion.core.genome_alignment.GenomeAlignment)`

Initialize self.  See help(type(self)) for accurate signature.


#### Properties

**end** -> `int`


**length** -> `int`


**start** -> `int`



### Band

Holds non-overlapping features placed in same vertical band.

**Signature:** `(self, index: int)`

#### Methods

**__init__**

*Signature:* `(self, index: int)`

Initialize self.  See help(type(self)) for accurate signature.


**add_feature**

*Signature:* `(self, feature: pyrion.visualization.GenomicFeature)`

Add feature to this band.


**can_add_feature**

*Signature:* `(self, feature: pyrion.visualization.GenomicFeature) -> bool`

Check if feature can be added without overlap.



### GenomicFeature

Abstract base class for genomic features with start/end coordinates.

**Signature:** `(self, /, *args, **kwargs)`

#### Properties

**end** -> `int`


**length** -> `int`


**start** -> `int`



### GenomicRuler

Renders genomic coordinate ruler with fixed height.

**Signature:** `(self, interval: pyrion.core.intervals.GenomicInterval, tick_count: int = 10, inverted: bool = False, height: float = 0.15)`

#### Methods

**__init__**

*Signature:* `(self, interval: pyrion.core.intervals.GenomicInterval, tick_count: int = 10, inverted: bool = False, height: float = 0.15)`

Initialize self.  See help(type(self)) for accurate signature.


**draw**

*Signature:* `(self, ax, y: float = 0.0)`

Draw ruler at specified y position.



### IntervalFeature

Wrapper for GenomicInterval.

**Signature:** `(self, interval: pyrion.core.intervals.GenomicInterval)`

#### Methods

**__init__**

*Signature:* `(self, interval: pyrion.core.intervals.GenomicInterval)`

Initialize self.  See help(type(self)) for accurate signature.


#### Properties

**end** -> `int`


**length** -> `int`


**start** -> `int`



### LayoutManager

Assigns tracks to levels and produces packed band layout.

**Signature:** `(self)`

#### Methods

**__init__**

*Signature:* `(self)`

Initialize self.  See help(type(self)) for accurate signature.


**add_track**

*Signature:* `(self, track: 'Track')`

Assign track to correct level based on type.


**compute_layout**

*Signature:* `(self)`

Run layout logic for all levels.


**get_total_bands**

*Signature:* `(self) -> int`

Get total number of bands across all levels.



### Level

Contains features of one type, produces non-overlapping bands.

**Signature:** `(self)`

#### Methods

**__init__**

*Signature:* `(self)`

Initialize self.  See help(type(self)) for accurate signature.


**add_features**

*Signature:* `(self, features: List[pyrion.visualization.GenomicFeature])`

Add features to this level.


**compute_bands**

*Signature:* `(self)`

Greedy algorithm to assign features to non-overlapping bands.



### Track

Logical unit of data belonging to one category.

**Signature:** `(self, name: str, features: List[pyrion.visualization.GenomicFeature], track_type: pyrion.visualization.TrackType)`

#### Methods

**__init__**

*Signature:* `(self, name: str, features: List[pyrion.visualization.GenomicFeature], track_type: pyrion.visualization.TrackType)`

Initialize self.  See help(type(self)) for accurate signature.



### TrackType

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.

**Signature:** `(self, *args, **kwds)`


### TranscriptFeature

Wrapper for Transcript.

**Signature:** `(self, transcript: pyrion.core.genes.Transcript)`

#### Methods

**__init__**

*Signature:* `(self, transcript: pyrion.core.genes.Transcript)`

Initialize self.  See help(type(self)) for accurate signature.


#### Properties

**end** -> `int`


**length** -> `int`


**start** -> `int`



### VisualizationWindow

Entry point for rendering genomic data visualization.

**Signature:** `(self, interval: pyrion.core.intervals.GenomicInterval, height: Optional[float] = None, band_height: float = 0.35, band_spacing: float = 0.05, level_spacing: float = 0.2, ruler_height: float = 0.4, label_height: float = 0.15, show_labels: bool = True, left_padding_width: int = 15000, show_feature_labels: bool = True)`

#### Methods

**__init__**

*Signature:* `(self, interval: pyrion.core.intervals.GenomicInterval, height: Optional[float] = None, band_height: float = 0.35, band_spacing: float = 0.05, level_spacing: float = 0.2, ruler_height: float = 0.4, label_height: float = 0.15, show_labels: bool = True, left_padding_width: int = 15000, show_feature_labels: bool = True)`

Initialize self.  See help(type(self)) for accurate signature.


**add_track**

*Signature:* `(self, track: pyrion.visualization.Track)`

Add a track to the window.


**show**

*Signature:* `(self, figsize: tuple = (12, 6))`

Trigger layout and rendering.



## Functions

### create_alignment_track

**Signature:** `(name: str, alignments: List[pyrion.core.genome_alignment.GenomeAlignment]) -> pyrion.visualization.Track`

Create an alignment track from a list of GenomeAlignment objects.


### create_interval_track

**Signature:** `(name: str, intervals: List[pyrion.core.intervals.GenomicInterval]) -> pyrion.visualization.Track`

Create an interval track from a list of GenomicInterval objects.


### create_transcript_track

**Signature:** `(name: str, transcripts: List[pyrion.core.genes.Transcript]) -> pyrion.visualization.Track`

Create a transcript track from a list of Transcript objects.


### create_window_for_region

**Signature:** `(chrom: str, start: int, end: int, **kwargs) -> pyrion.visualization.VisualizationWindow`

Create a VisualizationWindow for a specific genomic region.


### visualize_alignments

**Signature:** `(alignments: List[pyrion.core.genome_alignment.GenomeAlignment], window_interval: pyrion.core.intervals.GenomicInterval = None, track_name: str = 'Alignments', band_height: float = 0.35, **kwargs)`

Quick function to visualize a list of alignments.


### visualize_intervals

**Signature:** `(intervals: List[pyrion.core.intervals.GenomicInterval], window_interval: pyrion.core.intervals.GenomicInterval = None, track_name: str = 'Intervals', band_height: float = 0.35, **kwargs)`

Quick function to visualize a list of intervals.


### visualize_transcripts

**Signature:** `(transcripts: List[pyrion.core.genes.Transcript], window_interval: pyrion.core.intervals.GenomicInterval = None, track_name: str = 'Transcripts', band_height: float = 0.35, **kwargs)`

Quick function to visualize a list of transcripts.


---

