#!/usr/bin/env python3
"""Liftover transcripts between assemblies using chain files.

Requires:
  - A BED12 file with transcript annotations
  - A chain file (e.g. hg38ToMm39.over.chain)

Usage:
  python liftover_example.py annotations.bed hg38ToMm39.chain ENST00000456328
"""

import sys
from pyrion import read_bed12_file, read_chain_file
from pyrion.ops import project_transcript_through_chain


def main():
    if len(sys.argv) < 4:
        print("Usage: python liftover_example.py <bed12> <chain> <transcript_id>")
        sys.exit(1)

    bed_path, chain_path, transcript_id = sys.argv[1], sys.argv[2], sys.argv[3]

    transcripts = read_bed12_file(bed_path)
    chains = read_chain_file(chain_path)

    t = transcripts.get_by_id(transcript_id)
    if t is None:
        print(f"Transcript {transcript_id} not found")
        sys.exit(1)

    print(f"Source transcript: {t.id}")
    print(f"  {t.chrom}:{t.start}-{t.end} ({t.strand.to_char()})")
    print(f"  Exons: {len(t.exons())}")

    region = t.transcript_interval
    overlapping = chains.get_alignments_overlapping_target_interval(region)
    print(f"\nFound {len(overlapping)} overlapping chains")

    for chain in overlapping[:3]:
        print(f"\n  Chain {chain.chain_id} (score={chain.score})")
        print(f"    Target: {chain.t_chrom}, Query: {chain.q_chrom}")
        print(f"    Aligned bases: {chain.aligned_length()}")

        projected = project_transcript_through_chain(t, chain)
        if projected:
            print(f"    Projected to: {projected.chrom}:{projected.start}-{projected.end}")
        else:
            print("    Projection failed (no overlap with chain blocks)")


if __name__ == "__main__":
    main()
