"""Shared pytest configuration and fixtures."""

import pytest
from pathlib import Path


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "io: mark test as requiring file I/O operations")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    return Path("test_data")


@pytest.fixture(scope="session")
def chain_files(test_data_dir):
    """Available chain files for testing."""
    return {
        "large": test_data_dir / "chains" / "hg38.chr9.mm39.chr4.chain",
        "sample": test_data_dir / "sample_toga_input" / "hg38.chr21.mm39.chr16.chain",
        "chromM": test_data_dir / "chromM" / "hg38.chrM.mm39.chrM.chain"
    }


@pytest.fixture(scope="session", autouse=True)
def check_test_data(test_data_dir):
    """Verify test data availability at session start."""
    if not test_data_dir.exists():
        pytest.skip("Test data directory not found")
    
    required_files = [
        "chains/hg38.chr9.mm39.chr4.chain",
        "sample_toga_input/hg38.chr21.mm39.chr16.chain"
    ]
    
    for file_path in required_files:
        if not (test_data_dir / file_path).exists():
            pytest.skip(f"Required test file not found: {file_path}")