#!/bin/bash
# Convenient test runner script for pyrion chains module

set -e  # Exit on error

echo "🚀 Pyrion Chains Test Suite Runner"
echo "=================================="

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    echo "📦 Activating .venv virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found at .venv/"
    echo "💡 Run 'python setup.py build_ext --inplace' to build C extensions"
    exit 1
fi

# Check command line arguments
case "${1:-fast}" in
    "fast"|"quick"|"f")
        echo "⚡ Running fast test suite..."
        python test_runner.py fast
        ;;
    "comprehensive"|"full"|"c")
        echo "🔬 Running comprehensive test suite with benchmarks..."
        python test_runner.py comprehensive
        ;;
    "high-priority"|"priority"|"hp")
        echo "🎯 Running high-priority modules test suite..."
        python test_runner.py high-priority
        ;;
    "coverage"|"cov")
        echo "📊 Running tests with coverage analysis..."
        python test_runner.py coverage
        ;;
    "help"|"--help"|"-h")
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  fast, quick, f     - Run fast test suite (default)"
        echo "  comprehensive, c   - Run comprehensive tests with benchmarks"
        echo "  high-priority, hp  - Run high-priority modules (34 functions)"
        echo "  coverage, cov      - Run tests with coverage analysis"
        echo "  help              - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                 # Fast tests"
        echo "  $0 comprehensive   # Full test suite"
        echo "  $0 high-priority   # High-priority modules"
        echo "  $0 coverage       # Coverage analysis"
        exit 0
        ;;
    *)
        echo "❌ Unknown option: $1"
        echo "💡 Use '$0 help' for usage information"
        exit 1
        ;;
esac