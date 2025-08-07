#!/usr/bin/env python3
"""
Test Runner for Pyrion - pytest wrapper
=======================================

This project now uses pytest for all testing.

Usage:
    uv run pytest                    # Run all tests
    uv run pytest -v                 # Verbose output  
    uv run pytest tests/test_*.py    # Run specific test files
    uv run pytest -m "not slow"      # Skip slow tests
    uv run pytest --cov=pyrion       # Run with coverage

Test Categories:
    pytest -m io              # Tests requiring test data files
    pytest -m integration     # Integration tests  
    pytest -m slow            # Performance/benchmark tests

Examples:
    uv run pytest tests/test_chains.py -v
    uv run pytest tests/test_high_priority_modules.py
    uv run pytest --cov=pyrion --cov-report=html
"""

import sys
import subprocess
import argparse


def main():
    """Main entry point that delegates to pytest."""
    
    parser = argparse.ArgumentParser(
        description="Pyrion Test Runner - pytest wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This project now uses pytest. Available test modes:

Fast tests (default):
  uv run pytest -m "not slow"

All tests including slow ones:
  uv run pytest

With coverage:
  uv run pytest --cov=pyrion

Specific modules:
  uv run pytest tests/test_chains.py
  uv run pytest tests/test_high_priority_modules.py
  uv run pytest tests/test_sequences.py
        """
    )
    
    parser.add_argument(
        'mode', 
        nargs='?', 
        default='fast',
        choices=['fast', 'comprehensive', 'high-priority', 'coverage', 'all'],
        help='Test mode to run (default: fast)'
    )
    
    args = parser.parse_args()
    
    print("🚀 Pyrion Test Runner (pytest wrapper)")
    print("=" * 50)
    
    # Build pytest command based on mode
    pytest_args = ["uv", "run", "pytest", "-v"]
    
    if args.mode == 'fast':
        print("⚡ Running fast tests (excluding slow tests)")
        pytest_args.extend(["-m", "not slow"])
        
    elif args.mode == 'comprehensive':
        print("🔬 Running comprehensive tests (including slow tests)")
        pytest_args.append("tests/test_chains_comprehensive.py")
        
    elif args.mode == 'high-priority':
        print("🎯 Running high-priority module tests")
        pytest_args.append("tests/test_high_priority_modules.py")
        
    elif args.mode == 'coverage':
        print("📊 Running tests with coverage analysis")
        pytest_args.extend(["--cov=pyrion", "--cov-report=html", "--cov-report=term"])
        
    elif args.mode == 'all':
        print("🌟 Running all tests")
        # No additional filters
        
    # Add tests directory if no specific file
    if not any(arg.startswith("tests/") for arg in pytest_args[2:]):  # Skip "uv run" 
        pytest_args.append("tests/")
    
    print(f"Executing: {' '.join(pytest_args)}")
    print()
    
    # Run pytest
    try:
        result = subprocess.run(pytest_args, check=False)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("❌ uv not found. Please install uv first.")
        print("   Or run directly: python -m pytest")
        sys.exit(1)


if __name__ == "__main__":
    main()