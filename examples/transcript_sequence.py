#!/usr/bin/env python3
"""Load transcripts from BED12, extract CDS sequences, translate to protein.

Requires:
  - A BED12 file with transcript annotations
  - A 2bit genome file

Usage:
  python transcript_sequence.py annotations.bed hg38.2bit ENST00000456328
"""

import sys
from pyrion import read_bed12_file, TwoBitAccessor
from pyrion.ops import extract_cds_sequence, extract_exon_sequence


def main():
    if len(sys.argv) < 4:
        print("Usage: python transcript_sequence.py <bed12> <2bit> <transcript_id>")
        sys.exit(1)

    bed_path, twobit_path, transcript_id = sys.argv[1], sys.argv[2], sys.argv[3]

    transcripts = read_bed12_file(bed_path)
    genome = TwoBitAccessor(twobit_path)

    t = transcripts.get_by_id(transcript_id)
    if t is None:
        print(f"Transcript {transcript_id} not found")
        sys.exit(1)

    print(f"Transcript: {t.id}")
    print(f"  Chrom:  {t.chrom}")
    print(f"  Strand: {t.strand.to_char()}")
    print(f"  Span:   {t.start}-{t.end}")
    print(f"  Exons:  {len(t.exons())}")
    print(f"  Coding: {t.is_coding}")

    exon_seq = extract_exon_sequence(t, genome)
    print(f"\nExon sequence length: {len(exon_seq.to_string())} nt")

    if t.is_coding:
        cds_seq = extract_cds_sequence(t, genome)
        print(f"CDS sequence length:  {len(cds_seq.to_string())} nt")

        protein = cds_seq.to_amino_acids()
        print(f"Protein length:       {len(protein.to_string())} aa")
        print(f"Protein (first 50):   {protein.to_string()[:50]}")

    genome.close()


if __name__ == "__main__":
    main()
