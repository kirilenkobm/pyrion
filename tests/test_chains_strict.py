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
