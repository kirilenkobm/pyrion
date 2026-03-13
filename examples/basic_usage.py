#!/usr/bin/env python3
"""Basic Pyrion usage: intervals, sequences, and BED I/O."""

import numpy as np
from pyrion import GenomicInterval, NucleotideSequence, Strand
from pyrion.ops import merge_intervals, intersect_intervals

# --- Intervals ---

iv1 = GenomicInterval("chr1", 1000, 2000, Strand.PLUS, id="region_A")
iv2 = GenomicInterval("chr1", 1500, 2500, Strand.PLUS, id="region_B")
iv3 = GenomicInterval.from_string("chr1:3000-4000:+")

print(f"iv1 length: {iv1.length()}")
print(f"iv1 intersects iv2: {iv1.intersects(iv2)}")
print(f"Overlap: {iv1.overlap(iv2)} bp")
print(f"iv1 contains iv2: {iv1.contains(iv2)}")

union = iv1.union(iv2)
print(f"Union: {union.chrom}:{union.start}-{union.end}")

# --- Merge and intersect numpy arrays ---

intervals = np.array([[100, 200], [150, 300], [500, 600]])
merged = merge_intervals(intervals)
print(f"Merged: {merged}")

a = np.array([[100, 300], [500, 700]])
b = np.array([[200, 600]])
isect = intersect_intervals(a, b)
print(f"Intersection: {isect}")

# --- Nucleotide sequences ---

seq = NucleotideSequence.from_string("ATGCGATCGATCGA")
print(f"Sequence: {seq.to_string()}")
print(f"RevComp:  {seq.reverse_complement().to_string()}")
print(f"Slice:    {seq.slice(0, 6).to_string()}")
