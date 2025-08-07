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
        "compressed": test_data_dir / "chains" / "hg38.chr9.mm39.chr4.chain.gz"
    }


@pytest.fixture(scope="session", autouse=True)  
def check_test_data(test_data_dir):
    """Verify test data availability at session start."""
    if not test_data_dir.exists():
        pytest.skip("Test data directory not found")
    
    # Check for at least one chain file
    chain_files = [
        "chains/hg38.chr9.mm39.chr4.chain",
        "chains/hg38.chr9.mm39.chr4.chain.gz"
    ]
    
    if not any((test_data_dir / file_path).exists() for file_path in chain_files):
        pytest.skip("No chain files found for testing")