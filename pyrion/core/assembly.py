"""Genome assembly representation with optional sequence accessor."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Tuple, Union

from ..core_types import Strand
from .nucleotide_sequences import NucleotideSequence
from .intervals import GenomicInterval


class _SequenceAccessorProtocol(Protocol):
    """Minimal protocol for sequence accessors (TwoBitAccessor, FastaAccessor)."""
    def fetch(self, chrom: str, start: int, end: int, strand: Strand) -> NucleotideSequence: ...
    def chrom_sizes(self) -> Dict[str, int]: ...


class Assembly:
    """A genome assembly: named chromosome sizes with optional sequence accessor.

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
    """

    def __init__(
        self,
        name: str,
        chrom_sizes: Dict[str, int],
        aliases: Tuple[str, ...] = (),
        species: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if not name:
            raise ValueError("Assembly name must not be empty")
        if not chrom_sizes:
            raise ValueError("chrom_sizes must not be empty")

        self.name: str = name
        self.chrom_sizes: Dict[str, int] = dict(chrom_sizes)
        self.aliases: Tuple[str, ...] = tuple(aliases)
        self.species: Optional[str] = species
        self.metadata: Optional[Dict[str, Any]] = metadata
        self._accessor: Optional[Any] = None

        self._chr_prefix: Optional[bool] = None
        self._chrom_lookup: Optional[Dict[str, str]] = None

    # ── Constructors ──────────────────────────────────────────────────────

    @classmethod
    def from_2bit(
        cls,
        path_or_accessor,
        name: str,
        aliases: Tuple[str, ...] = (),
        species: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Assembly:
        """Create an Assembly from a 2bit file or an open TwoBitAccessor.

        The accessor is attached automatically.
        """
        from ..io.twobit import TwoBitAccessor

        if isinstance(path_or_accessor, (str, Path)):
            accessor = TwoBitAccessor(str(path_or_accessor))
        else:
            accessor = path_or_accessor

        assembly = cls(
            name=name,
            chrom_sizes=accessor.chrom_sizes(),
            aliases=aliases,
            species=species,
            metadata=metadata,
        )
        assembly._accessor = accessor
        return assembly

    @classmethod
    def from_chrom_sizes_file(
        cls,
        path: Union[str, Path],
        name: str,
        aliases: Tuple[str, ...] = (),
        species: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Assembly:
        """Create an Assembly from a .chrom.sizes file (two-column TSV)."""
        from ..io.chrom_sizes import read_chrom_sizes

        chrom_sizes = read_chrom_sizes(path)
        return cls(
            name=name,
            chrom_sizes=chrom_sizes,
            aliases=aliases,
            species=species,
            metadata=metadata,
        )

    @classmethod
    def from_fasta_index(
        cls,
        path_or_accessor,
        name: str,
        aliases: Tuple[str, ...] = (),
        species: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Assembly:
        """Create an Assembly from a FastaAccessor (or path to indexed FASTA).

        The accessor is attached automatically.
        """
        from ..io.fasta import FastaAccessor

        if isinstance(path_or_accessor, (str, Path)):
            accessor = FastaAccessor(str(path_or_accessor))
        else:
            accessor = path_or_accessor

        chrom_sizes = {
            seq_name: accessor.get_sequence_length(seq_name)
            for seq_name in accessor.get_sequence_names()
        }
        assembly = cls(
            name=name,
            chrom_sizes=chrom_sizes,
            aliases=aliases,
            species=species,
            metadata=metadata,
        )
        assembly._accessor = accessor
        return assembly

    # ── Accessor link ─────────────────────────────────────────────────────

    @property
    def accessor(self):
        """Return the attached sequence accessor, or raise if none is set."""
        if self._accessor is None:
            raise RuntimeError(
                f"Assembly '{self.name}' has no sequence accessor. "
                "Use set_accessor() or construct with from_2bit() / from_fasta_index()."
            )
        return self._accessor

    def set_accessor(self, accessor) -> None:
        """Attach a TwoBitAccessor or FastaAccessor for sequence retrieval."""
        self._accessor = accessor

    @property
    def has_accessor(self) -> bool:
        return self._accessor is not None

    def fetch(
        self,
        chrom: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        strand: Strand = Strand.PLUS,
    ) -> NucleotideSequence:
        """Fetch sequence via the attached accessor."""
        return self.accessor.fetch(chrom, start, end, strand)

    def fetch_interval(self, interval: GenomicInterval) -> NucleotideSequence:
        """Fetch sequence for a GenomicInterval via the attached accessor."""
        return self.accessor.fetch(interval.chrom, interval.start, interval.end, interval.strand)

    # ── Chromosome queries ────────────────────────────────────────────────

    def has_chrom(self, chrom: str) -> bool:
        return chrom in self.chrom_sizes

    def get_chrom_size(self, chrom: str) -> int:
        if chrom not in self.chrom_sizes:
            raise KeyError(f"Chromosome '{chrom}' not found in assembly '{self.name}'")
        return self.chrom_sizes[chrom]

    def find_chrom(self, chrom: str) -> Optional[str]:
        """Fuzzy-match a chromosome name, handling chr prefix differences.

        Returns the matching chrom name from this assembly, or None.
        """
        if chrom in self.chrom_sizes:
            return chrom

        if self._chrom_lookup is None:
            self._build_chrom_lookup()

        return self._chrom_lookup.get(chrom.lower())

    def _build_chrom_lookup(self) -> None:
        """Build a case-insensitive lookup table with chr-prefix variants."""
        lookup: Dict[str, str] = {}
        for name in self.chrom_sizes:
            lower = name.lower()
            lookup[lower] = name

            if lower.startswith("chr"):
                stripped = lower[3:]
                if stripped not in lookup:
                    lookup[stripped] = name
            else:
                prefixed = "chr" + lower
                if prefixed not in lookup:
                    lookup[prefixed] = name

            # MT ↔ M
            if lower == "chrm" or lower == "m":
                lookup["chrmt"] = name
                lookup["mt"] = name
            elif lower == "chrmt" or lower == "mt":
                lookup["chrm"] = name
                lookup["m"] = name

        self._chrom_lookup = lookup

    @property
    def uses_chr_prefix(self) -> bool:
        """Whether this assembly uses 'chr' prefixed chromosome names."""
        if self._chr_prefix is None:
            chroms = list(self.chrom_sizes.keys())
            chr_count = sum(1 for c in chroms if c.startswith("chr"))
            self._chr_prefix = chr_count > len(chroms) / 2
        return self._chr_prefix

    @property
    def num_chroms(self) -> int:
        return len(self.chrom_sizes)

    @property
    def total_size(self) -> int:
        return sum(self.chrom_sizes.values())

    @property
    def chrom_names(self) -> List[str]:
        return list(self.chrom_sizes.keys())

    # ── Validation ────────────────────────────────────────────────────────

    def validate_interval(self, interval: GenomicInterval) -> bool:
        """Check if a GenomicInterval fits within this assembly."""
        if interval.chrom not in self.chrom_sizes:
            return False
        return 0 <= interval.start < interval.end <= self.chrom_sizes[interval.chrom]

    def validate_transcript(self, transcript) -> bool:
        """Check if a Transcript fits within this assembly."""
        if transcript.chrom not in self.chrom_sizes:
            return False
        chrom_size = self.chrom_sizes[transcript.chrom]
        return 0 <= transcript.start and transcript.end <= chrom_size

    def validate_collection(self, collection) -> List[str]:
        """Validate a TranscriptsCollection against this assembly.

        Returns a list of issue descriptions (empty = all valid).
        """
        issues = []
        known_chroms = set(self.chrom_sizes.keys())
        collection_chroms = set()

        for t in collection:
            collection_chroms.add(t.chrom)
            if t.chrom not in known_chroms:
                continue
            chrom_size = self.chrom_sizes[t.chrom]
            if t.end > chrom_size:
                issues.append(
                    f"Transcript '{t.id}' ends at {t.end} but "
                    f"{t.chrom} size is {chrom_size}"
                )

        unknown = collection_chroms - known_chroms
        if unknown:
            issues.insert(
                0,
                f"Unknown chromosomes: {sorted(unknown)}"
            )

        return issues

    # ── Identity ──────────────────────────────────────────────────────────

    def matches_name(self, name: str) -> bool:
        """Check if `name` matches this assembly's name or any alias (case-insensitive)."""
        lower = name.lower()
        if self.name.lower() == lower:
            return True
        return any(a.lower() == lower for a in self.aliases)

    def all_names(self) -> Tuple[str, ...]:
        """Return (name,) + aliases."""
        return (self.name,) + self.aliases

    # ── Serialization ─────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "name": self.name,
            "chrom_sizes": self.chrom_sizes,
        }
        if self.aliases:
            d["aliases"] = list(self.aliases)
        if self.species is not None:
            d["species"] = self.species
        if self.metadata is not None:
            d["metadata"] = self.metadata
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Assembly:
        return cls(
            name=d["name"],
            chrom_sizes=d["chrom_sizes"],
            aliases=tuple(d.get("aliases", ())),
            species=d.get("species"),
            metadata=d.get("metadata"),
        )

    def save_chrom_sizes(self, path: Union[str, Path]) -> None:
        """Write chrom sizes to a two-column TSV file."""
        path = Path(path)
        with path.open("w") as f:
            for chrom in sorted(self.chrom_sizes.keys()):
                f.write(f"{chrom}\t{self.chrom_sizes[chrom]}\n")

    # ── Dunder ────────────────────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Assembly):
            return NotImplemented
        return self.name == other.name and self.chrom_sizes == other.chrom_sizes

    def __hash__(self) -> int:
        return hash(self.name)

    def __contains__(self, chrom: str) -> bool:
        """Allow `'chr1' in assembly` syntax."""
        return chrom in self.chrom_sizes

    def __len__(self) -> int:
        return len(self.chrom_sizes)

    def __repr__(self) -> str:
        total = self.total_size
        if total >= 1_000_000_000:
            size_str = f"{total / 1_000_000_000:.1f}Gb"
        elif total >= 1_000_000:
            size_str = f"{total / 1_000_000:.1f}Mb"
        elif total >= 1_000:
            size_str = f"{total / 1_000:.1f}kb"
        else:
            size_str = f"{total}bp"

        parts = [f"'{self.name}'", f"{self.num_chroms} chromosomes", size_str]
        if self.species:
            parts.insert(1, self.species)
        if self.has_accessor:
            parts.append("accessor=yes")

        return f"Assembly({', '.join(parts)})"
