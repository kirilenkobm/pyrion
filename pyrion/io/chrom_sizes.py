"""Read and write .chrom.sizes files (two-column TSV: chrom_name\tsize)."""

from pathlib import Path
from typing import Dict, Union


def read_chrom_sizes(path: Union[str, Path]) -> Dict[str, int]:
    """Read a chrom.sizes file into a dict.

    Format: tab-separated, one chromosome per line.
    Lines starting with '#' are skipped.
    """
    path = Path(path)
    chrom_sizes: Dict[str, int] = {}

    with path.open() as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                raise ValueError(
                    f"{path}:{line_num}: expected tab-separated chrom and size, "
                    f"got: {line!r}"
                )
            chrom = parts[0]
            try:
                size = int(parts[1])
            except ValueError:
                raise ValueError(
                    f"{path}:{line_num}: invalid size value: {parts[1]!r}"
                )
            if size <= 0:
                raise ValueError(
                    f"{path}:{line_num}: chromosome size must be positive, "
                    f"got {size} for '{chrom}'"
                )
            if chrom in chrom_sizes:
                raise ValueError(
                    f"{path}:{line_num}: duplicate chromosome '{chrom}'"
                )
            chrom_sizes[chrom] = size

    if not chrom_sizes:
        raise ValueError(f"{path}: no chromosomes found")

    return chrom_sizes


def write_chrom_sizes(chrom_sizes: Dict[str, int], path: Union[str, Path]) -> None:
    """Write a chrom_sizes dict to a two-column TSV file."""
    path = Path(path)
    with path.open("w") as f:
        for chrom in sorted(chrom_sizes.keys()):
            f.write(f"{chrom}\t{chrom_sizes[chrom]}\n")
