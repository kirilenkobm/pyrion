"""Unit tests for strict chain projection."""

import pytest
import numpy as np

from pyrion.ops.chains import project_intervals_through_chain_strict


class TestStrictProjection:
    """Tests for project_intervals_through_chain_strict function."""

    def test_scenario_1_perfect_alignment(self):
        """Scenario 1: Interval overlaps aligned blocks with same coordinates."""
        # Interval: [1000, 2000]
        # Blocks: [500-1200] -> [500-1200], [1800-2200] -> [1800-2200]
        intervals = np.array([[1000, 2000]], dtype=np.int64)
        blocks = np.array([
            [500, 1200, 500, 1200],
            [1800, 2200, 1800, 2200]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        assert result[0].shape == (1, 2)
        # Should project start from first block, end from last block
        assert result[0][0, 0] == 1000  # Start
        assert result[0][0, 1] == 2000  # End

    def test_scenario_2_single_overlapping_block(self):
        """Scenario 2: Only one block overlaps, misaligned regions on both sides."""
        # Interval: [1000, 2000]
        # Blocks: [0-100], [1500-1600], [3000-3500] (same in query)
        intervals = np.array([[1000, 2000]], dtype=np.int64)
        blocks = np.array([
            [0, 100, 0, 100],
            [1500, 1600, 1500, 1600],
            [3000, 3500, 3000, 3500]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        # Should extrapolate but limit by available query space
        # Start: interval_start=1000, first_block_start=1500, extension_needed=500
        # Available space before: 1500 - 100 = 1400, so extension = min(500, 1400) = 500
        # q_start = 1500 - 500 = 1000
        # End: interval_end=2000, last_block_end=1600, extension_needed=400
        # Available space after: 3000 - 1600 = 1400, so extension = min(400, 1400) = 400
        # q_end = 1600 + 400 = 2000
        assert result[0][0, 0] == 1000
        assert result[0][0, 1] == 2000

    def test_scenario_3_deletion_in_query(self):
        """Scenario 3: Deletion in query - limited extension."""
        # Interval: [1000, 2000]
        # Blocks: [0-100] -> [0-100], [1500-1600] -> [200-300], [3000-3500] -> [400-900]
        intervals = np.array([[1000, 2000]], dtype=np.int64)
        blocks = np.array([
            [0, 100, 0, 100],
            [1500, 1600, 200, 300],
            [3000, 3500, 400, 900]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        # Start: extension_needed=500, but available_query_space = 200-100 = 100
        # q_start = 200 - 100 = 100
        # End: extension_needed=400, but available_query_space = 400-300 = 100
        # q_end = 300 + 100 = 400
        assert result[0][0, 0] == 100
        assert result[0][0, 1] == 400

    def test_scenario_4_chain_does_not_propagate(self):
        """Scenario 4: Block in middle, chain doesn't propagate to termini."""
        # Interval: [100, 2000]
        # Block: [1000-1100] -> [1000-1100] (only one in middle)
        intervals = np.array([[100, 2000]], dtype=np.int64)
        blocks = np.array([
            [1000, 1100, 1000, 1100]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        # No block before 100, no block after 2000
        # Should use block boundaries without extension
        assert result[0][0, 0] == 1000  # Block start
        assert result[0][0, 1] == 1100  # Block end

    def test_complete_misalignment_acceptable(self):
        """Complete misalignment with flanks - query distance <= interval length."""
        # Interval: [1000, 2000] (length 1000)
        # Blocks: [0-500] -> [0-500], [2500-3000] -> [600-1100]
        # Query gap: 600-500 = 100 <= 1000, should return
        intervals = np.array([[1000, 2000]], dtype=np.int64)
        blocks = np.array([
            [0, 500, 0, 500],
            [2500, 3000, 600, 1100]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        assert result[0][0, 0] == 500   # Left flank end
        assert result[0][0, 1] == 600   # Right flank start

    def test_complete_misalignment_too_large(self):
        """Complete misalignment - query distance > interval length, reject."""
        # Interval: [1000, 2000] (length 1000)
        # Blocks: [0-500] -> [0-500], [2500-3000] -> [2000-2500]
        # Query gap: 2000-500 = 1500 > 1000, should reject
        intervals = np.array([[1000, 2000]], dtype=np.int64)
        blocks = np.array([
            [0, 500, 0, 500],
            [2500, 3000, 2000, 2500]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        assert result[0][0, 0] == 0
        assert result[0][0, 1] == 0

    def test_no_flanking_blocks(self):
        """Complete misalignment but missing flanks."""
        # Interval: [1000, 2000]
        # Block: [3000-4000] (only after interval)
        intervals = np.array([[1000, 2000]], dtype=np.int64)
        blocks = np.array([
            [3000, 4000, 3000, 4000]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        assert result[0][0, 0] == 0
        assert result[0][0, 1] == 0

    def test_interval_inside_block(self):
        """Interval completely inside one aligned block."""
        # Interval: [1500, 1800]
        # Block: [1000-2000] -> [500-1500]
        intervals = np.array([[1500, 1800]], dtype=np.int64)
        blocks = np.array([
            [1000, 2000, 500, 1500]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        # Direct projection with scaling
        # Start: (1500-1000)/(2000-1000) * (1500-500) + 500 = 0.5 * 1000 + 500 = 1000
        # End: (1800-1000)/(2000-1000) * (1500-500) + 500 = 0.8 * 1000 + 500 = 1300
        assert result[0][0, 0] == 1000
        assert result[0][0, 1] == 1300

    def test_multiple_intervals(self):
        """Test multiple intervals at once."""
        intervals = np.array([
            [1000, 1500],
            [2000, 2500],
            [5000, 6000]
        ], dtype=np.int64)
        blocks = np.array([
            [900, 1600, 900, 1600],
            [1800, 2600, 1800, 2600],
            [10000, 11000, 10000, 11000]
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 3
        # First interval overlaps first block
        assert result[0][0, 0] == 1000
        assert result[0][0, 1] == 1500
        # Second interval overlaps second block
        assert result[1][0, 0] == 2000
        assert result[1][0, 1] == 2500
        # Third interval - no overlap, check flanks
        # Left flank: block 2 ends at 2600, right flank: block 3 starts at 10000
        # Query distance: 10000-2600 = 7400 > interval length 1000, reject
        assert result[2][0, 0] == 0
        assert result[2][0, 1] == 0

    def test_reverse_strand_overlapping_blocks(self):
        """Reverse-strand chain: query coords decrease as target coords increase."""
        # Interval overlaps two blocks whose query coords are in reverse order
        intervals = np.array([[1000, 4000]], dtype=np.int64)
        blocks = np.array([
            [500, 2000, 7000, 8500],
            [3000, 4500, 4000, 5500],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        projected_start = result[0][0, 0]
        projected_end = result[0][0, 1]
        assert projected_start < projected_end, (
            f"Expected start < end, got ({projected_start}, {projected_end})"
        )

    def test_reverse_strand_single_block(self):
        """Reverse-strand chain: interval fully inside one block, coords must normalize."""
        # Block maps t=[0,100000] -> q=[200000,100000] (reverse strand, q_start > q_end
        # is actually represented as q_start=200000, q_end=100000 in chain)
        intervals = np.array([[20000, 80000]], dtype=np.int64)
        blocks = np.array([
            [0, 100000, 200000, 100000],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        projected_start = result[0][0, 0]
        projected_end = result[0][0, 1]
        assert projected_start < projected_end, (
            f"Expected start < end, got ({projected_start}, {projected_end})"
        )

    def test_reverse_strand_flanking_blocks_acceptable(self):
        """Reverse-strand chain: flanking blocks with reversed query coords."""
        # Interval: [2000, 3000] (length 1000)
        # Blocks have decreasing query coords (reverse strand)
        # Left flank q_end=7000, right flank q_start=6200 -> abs gap=800 <= 1000 -> accept
        intervals = np.array([[2000, 3000]], dtype=np.int64)
        blocks = np.array([
            [0, 1000, 6500, 7000],
            [4000, 5000, 6200, 6400],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        projected_start = result[0][0, 0]
        projected_end = result[0][0, 1]
        assert projected_start < projected_end, (
            f"Expected start < end, got ({projected_start}, {projected_end})"
        )
        assert projected_start == 6200
        assert projected_end == 7000

    def test_reverse_strand_flanking_blocks_too_large(self):
        """Reverse-strand chain: flanking blocks gap too large, should reject."""
        # Interval: [2000, 3000] (length 1000)
        # Left flank q_end=9000, right flank q_start=5000 -> abs gap=4000 > 1000 -> reject
        intervals = np.array([[2000, 3000]], dtype=np.int64)
        blocks = np.array([
            [0, 1000, 8000, 9000],
            [4000, 5000, 5000, 6000],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks)

        assert len(result) == 1
        assert result[0][0, 0] == 0
        assert result[0][0, 1] == 0

    def test_minus_strand_single_block_inside(self):
        """Minus-strand chain: within-block projection reverses direction."""
        # Block: T=[1000, 1100], Q=[2000, 2100] (100 bp each, genomic + coords)
        # Interval [1010, 1030] at offset 10-30 from t_start
        # Plus strand would give: [2010, 2030]
        # Minus strand should give: [2070, 2090] (q_end - offset)
        intervals = np.array([[1010, 1030]], dtype=np.int64)
        blocks = np.array([[1000, 1100, 2000, 2100]], dtype=np.int64)

        result_plus = project_intervals_through_chain_strict(intervals, blocks, q_strand=1)
        result_minus = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)

        assert result_plus[0][0, 0] == 2010
        assert result_plus[0][0, 1] == 2030
        assert result_minus[0][0, 0] == 2070
        assert result_minus[0][0, 1] == 2090

    def test_minus_strand_single_block_scaled(self):
        """Minus-strand chain: proportional projection with different t_len/q_len."""
        # Block: T=[0, 200], Q=[0, 100], ratio=0.5
        # Interval [40, 160] → offset [40, 160]
        # Plus: q_s + int((40/200)*100)=20, q_s + int((160/200)*100)=80 → [20, 80]
        # Minus: q_e - int((40/200)*100)=80, q_e - int((160/200)*100)=20 → [20, 80]
        # (symmetric interval → same result either way)
        # Asymmetric: Interval [20, 60]
        # Plus: 0 + int((20/200)*100)=10, 0 + int((60/200)*100)=30 → [10, 30]
        # Minus: 100 - 10=90, 100 - 30=70 → [70, 90]
        intervals = np.array([[20, 60]], dtype=np.int64)
        blocks = np.array([[0, 200, 0, 100]], dtype=np.int64)

        result_plus = project_intervals_through_chain_strict(intervals, blocks, q_strand=1)
        result_minus = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)

        assert result_plus[0][0, 0] == 10
        assert result_plus[0][0, 1] == 30
        assert result_minus[0][0, 0] == 70
        assert result_minus[0][0, 1] == 90

    def test_minus_strand_two_blocks_spanning(self):
        """Minus-strand chain: interval spans two blocks with decreasing q."""
        # Simulates minus-strand parsed blocks (q decreases across blocks)
        # Block 0: T=[0, 200], Q=[800, 1000] (t_len=200, q_len=200, higher q)
        # Block 1: T=[300, 500], Q=[400, 600] (t_len=200, q_len=200, lower q)
        # Interval: [50, 350]
        #   Start in block 0, offset=50: minus → 1000 - int((50/200)*200) = 1000-50 = 950
        #   End in block 1, offset=50: minus → 600 - int((50/200)*200) = 600-50 = 550
        #   After swap: [550, 950]
        intervals = np.array([[50, 350]], dtype=np.int64)
        blocks = np.array([
            [0, 200, 800, 1000],
            [300, 500, 400, 600],
        ], dtype=np.int64)

        result_minus = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)
        assert result_minus[0][0, 0] == 550
        assert result_minus[0][0, 1] == 950

    def test_minus_strand_extension_before_block(self):
        """Minus-strand: extension into misaligned region before first overlapping block."""
        # Block 0: T=[0, 100], Q=[800, 900] (higher q, previous block)
        # Block 1: T=[200, 300], Q=[500, 600] (lower q, overlapping block)
        # Interval: [150, 250] → start is before block 1, end is inside block 1
        # Minus strand:
        #   Start extension: needed=200-150=50
        #     Available: q_starts[block0] - q_ends[block1] = 800 - 600 = 200
        #     Extension = min(50, 200) = 50
        #     q_start = q_ends[block1] + 50 = 600 + 50 = 650
        #   End projection: offset=250-200=50, q_end = q_ends[1] - int((50/100)*100) = 600-50 = 550
        #   After swap: [550, 650]
        intervals = np.array([[150, 250]], dtype=np.int64)
        blocks = np.array([
            [0, 100, 800, 900],
            [200, 300, 500, 600],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)
        assert result[0][0, 0] == 550
        assert result[0][0, 1] == 650

    def test_minus_strand_extension_after_block(self):
        """Minus-strand: extension into misaligned region after last overlapping block."""
        # Block 0: T=[0, 100], Q=[800, 900] (higher q, overlapping block)
        # Block 1: T=[200, 300], Q=[500, 600] (lower q, next block)
        # Interval: [50, 150] → start is inside block 0, end is after block 0
        # Minus strand:
        #   Start projection: offset=50-0=50, q_start = q_ends[0] - int((50/100)*100) = 900-50 = 850
        #   End extension: needed=150-100=50
        #     Available: q_starts[block0] - q_ends[block1] = 800 - 600 = 200
        #     Extension = min(50, 200) = 50
        #     q_end = q_starts[block0] - 50 = 800 - 50 = 750
        #   After swap: [750, 850]
        intervals = np.array([[50, 150]], dtype=np.int64)
        blocks = np.array([
            [0, 100, 800, 900],
            [200, 300, 500, 600],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)
        assert result[0][0, 0] == 750
        assert result[0][0, 1] == 850

    def test_minus_strand_flanking_blocks(self):
        """Minus-strand: interval entirely in gap, flanking blocks provide boundaries."""
        # Block 0: T=[0, 100], Q=[800, 900] (left flank, higher q)
        # Block 1: T=[400, 500], Q=[500, 600] (right flank, lower q)
        # Interval: [200, 300] (length 100)
        # Minus strand flanking:
        #   q_flank_start = q_ends[right] = 600
        #   q_flank_end = q_starts[left] = 800
        #   distance = 200, interval_length = 100 → 200 > 100 → reject
        intervals = np.array([[200, 300]], dtype=np.int64)
        blocks = np.array([
            [0, 100, 800, 900],
            [400, 500, 500, 600],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)
        assert result[0][0, 0] == 0
        assert result[0][0, 1] == 0

    def test_minus_strand_flanking_blocks_acceptable(self):
        """Minus-strand: flanking gap within acceptable distance."""
        # Block 0: T=[0, 100], Q=[850, 900] (left flank)
        # Block 1: T=[400, 500], Q=[800, 830] (right flank)
        # Interval: [200, 300] (length 100)
        # Minus strand:
        #   q_flank_start = q_ends[right] = 830
        #   q_flank_end = q_starts[left] = 850
        #   distance = 20, interval_length = 100 → 20 <= 100 → accept
        #   After normalize: [830, 850]
        intervals = np.array([[200, 300]], dtype=np.int64)
        blocks = np.array([
            [0, 100, 850, 900],
            [400, 500, 800, 830],
        ], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)
        assert result[0][0, 0] == 830
        assert result[0][0, 1] == 850

    def test_minus_strand_no_propagation_before(self):
        """Minus-strand: no previous block, can't extend before first block."""
        # Single block: T=[100, 200], Q=[500, 600]
        # Interval: [50, 150] → start before block, end inside block
        # No previous block → q_start = q_ends[0] = 600 (for minus strand)
        # End: offset=150-100=50, q_end = 600 - 50 = 550
        # After swap: [550, 600]
        intervals = np.array([[50, 150]], dtype=np.int64)
        blocks = np.array([[100, 200, 500, 600]], dtype=np.int64)

        result = project_intervals_through_chain_strict(intervals, blocks, q_strand=-1)
        assert result[0][0, 0] == 550
        assert result[0][0, 1] == 600

    def test_empty_inputs(self):
        """Test edge cases with empty inputs."""
        # Empty intervals
        result = project_intervals_through_chain_strict(
            np.array([], dtype=np.int64).reshape(0, 2),
            np.array([[0, 100, 0, 100]], dtype=np.int64)
        )
        assert len(result) == 0

        # Empty blocks
        result = project_intervals_through_chain_strict(
            np.array([[100, 200]], dtype=np.int64),
            np.array([], dtype=np.int64).reshape(0, 4)
        )
        assert len(result) == 1
        assert result[0][0, 0] == 0
        assert result[0][0, 1] == 0
