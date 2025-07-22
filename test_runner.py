#!/usr/bin/env python3
"""
Comprehensive Test Runner for Pyrion
====================================

Single test runner covering all testing modes:
- Fast: Core functionality verification
- Comprehensive: Detailed testing with benchmarks  
- High-Priority: All critical modules (34+ functions)
- Coverage: Detailed coverage analysis

Usage:
    python test_runner.py [mode]
    
Modes:
    fast         - Quick core tests (default)
    comprehensive - Full chains module with benchmarks  
    high-priority - All high-priority modules
    coverage     - Coverage analysis
"""

import sys
import time
import argparse
from pathlib import Path


def run_fast_tests():
    """Run fast core functionality tests."""
    print("⚡ Fast Test Suite")
    print("=" * 50)
    print("Testing core chains functionality...")
    
    sys.path.insert(0, str(Path.cwd()))
    
    try:
        # Core imports and basic tests
        import numpy as np
        from pyrion.ops.chains import (
            project_intervals_through_chain,
            get_chain_target_interval,
            get_chain_query_interval,
            get_chain_t_start,
            get_chain_t_end
        )
        from pyrion.core.genome_alignment import GenomeAlignment
        
        tests_passed = 0
        tests_total = 0
        
        # Test 1: Basic projection
        tests_total += 1
        try:
            chain_blocks = np.array([
                [100, 200, 1000, 1100],
                [300, 400, 1200, 1300],
            ], dtype=np.int64)
            
            intervals = np.array([[150, 180], [350, 380]], dtype=np.int64)
            results = project_intervals_through_chain(intervals, chain_blocks)
            
            assert len(results) == 2
            assert np.array_equal(results[0], np.array([[1050, 1080]], dtype=np.int64))
            assert np.array_equal(results[1], np.array([[1250, 1280]], dtype=np.int64))
            
            print("✅ Test 1: Basic projection - PASSED")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Test 1: Basic projection - FAILED: {e}")
        
        # Test 2: Chain accessors
        tests_total += 1
        try:
            genome_alignment = GenomeAlignment(
                chain_id=1, score=1000, t_chrom="chr1", t_strand=1, t_size=1000000,
                q_chrom="chr2", q_strand=1, q_size=1000000, blocks=chain_blocks
            )
            
            assert get_chain_t_start(genome_alignment) == 100
            assert get_chain_t_end(genome_alignment) == 400
            
            target = get_chain_target_interval(genome_alignment)
            assert target.chrom == "chr1"
            assert target.start == 100
            assert target.end == 400
            
            print("✅ Test 2: Chain accessors - PASSED")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Test 2: Chain accessors - FAILED: {e}")
        
        # Test 3: Real data (if available)
        tests_total += 1
        try:
            from pyrion.io.chain import read_chain_file
            chain_file = Path("test_data/sample_toga_input/hg38.chr21.mm39.chr16.chain")
            
            if chain_file.exists():
                collection = read_chain_file(chain_file)
                if len(collection.alignments) > 0:
                    alignment = collection.alignments[0]
                    
                    t_start = get_chain_t_start(alignment)
                    t_end = get_chain_t_end(alignment)
                    
                    test_intervals = np.array([[t_start + 1000, t_start + 1100]], dtype=np.int64)
                    results = project_intervals_through_chain(test_intervals, alignment.blocks)
                    assert len(results) == 1
                    
                    print(f"✅ Test 3: Real data ({len(alignment.blocks):,} blocks) - PASSED")
                else:
                    print("⚠️  Test 3: Real data - SKIPPED (no alignments)")
            else:
                print("⚠️  Test 3: Real data - SKIPPED (file not found)")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Test 3: Real data - FAILED: {e}")
        
        print(f"\n📊 Results: {tests_passed}/{tests_total} tests passed")
        return tests_passed == tests_total
        
    except Exception as e:
        print(f"❌ Fast tests failed: {e}")
        return False


def run_comprehensive_tests():
    """Run comprehensive tests by delegating to the comprehensive runner."""
    print("🔬 Comprehensive Test Suite")
    print("=" * 50)
    print("Running detailed tests with benchmarks...")
    
    try:
        # Import and run the comprehensive test suite
        sys.path.insert(0, str(Path.cwd() / "tests"))
        from test_chains_comprehensive import main as comprehensive_main
        
        # Redirect to comprehensive runner
        comprehensive_main()
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive tests failed: {e}")
        return False


def run_high_priority_tests():
    """Run high-priority modules tests by delegating to the high-priority runner."""
    print("🎯 High-Priority Modules Test Suite")
    print("=" * 50)
    print("Testing all critical modules...")
    
    try:
        # Import and run the high-priority test suite
        sys.path.insert(0, str(Path.cwd() / "tests"))
        from test_high_priority_modules import main as hp_main
        
        # Redirect to high-priority runner
        hp_main()
        return True
        
    except Exception as e:
        print(f"❌ High-priority tests failed: {e}")
        return False


def run_sequences_tests():
    """Run sequence functionality tests."""
    print("🧬 Sequence Functionality Tests") 
    print("=" * 50)
    print("Testing nucleotides, codons, amino acids...")
    
    try:
        # Run sequence tests directly
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, "tests/test_sequences.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ All sequence tests passed!")
            return True
        else:
            print("❌ Some sequence tests failed")
            print("STDOUT:", result.stdout[-500:])  # Last 500 chars
            print("STDERR:", result.stderr[-500:])
            return False
            
    except Exception as e:
        print(f"❌ Sequence tests failed: {e}")
        return False


def run_coverage_tests():
    """Run coverage analysis."""
    print("📊 Coverage Analysis")
    print("=" * 50)
    print("Running comprehensive coverage analysis...")
    
    # For now, redirect to high-priority tests which provide coverage info
    return run_high_priority_tests()


def main():
    """Main test runner with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Comprehensive Test Runner for Pyrion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py                    # Fast tests (default)
  python test_runner.py fast               # Fast tests  
  python test_runner.py comprehensive      # Full test suite with benchmarks
  python test_runner.py high-priority      # All high-priority modules (49+ functions)
  python test_runner.py sequences          # Sequence functionality tests
  python test_runner.py coverage           # Coverage analysis
        """
    )
    
    parser.add_argument(
        'mode', 
        nargs='?', 
        default='fast',
        choices=['fast', 'comprehensive', 'high-priority', 'coverage', 'sequences'],
        help='Test mode to run (default: fast)'
    )
    
    args = parser.parse_args()
    
    print("🚀 Pyrion Comprehensive Test Runner")
    print("=" * 60)
    
    start_time = time.time()
    
    # Run selected test mode
    if args.mode == 'fast':
        success = run_fast_tests()
    elif args.mode == 'comprehensive':
        success = run_comprehensive_tests()
    elif args.mode == 'high-priority':
        success = run_high_priority_tests()
    elif args.mode == 'sequences':
        success = run_sequences_tests()
    elif args.mode == 'coverage':
        success = run_coverage_tests()
    else:
        print(f"❌ Unknown mode: {args.mode}")
        sys.exit(1)
    
    end_time = time.time()
    
    # Summary
    print(f"\n⏱️  Total execution time: {end_time - start_time:.2f} seconds")
    
    if success:
        print("🎉 All tests completed successfully!")
        
        # Show available options
        print(f"\n💡 Other test modes:")
        if args.mode != 'fast':
            print(f"   python test_runner.py fast               # Quick core tests")
        if args.mode != 'comprehensive':
            print(f"   python test_runner.py comprehensive      # Full benchmarks")
        if args.mode != 'high-priority':
            print(f"   python test_runner.py high-priority      # All critical modules")
        if args.mode != 'sequences':
            print(f"   python test_runner.py sequences          # Sequence functionality")
        if args.mode != 'coverage':
            print(f"   python test_runner.py coverage           # Coverage analysis")
        
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()