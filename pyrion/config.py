"""Global configuration for pyrion library."""

import logging
import multiprocessing as mp
import os
from typing import Optional, Union


class PyrionConfig:
    """Global configuration for pyrion library.
    
    Manages parallelization settings and other global options.
    """
    
    def __init__(self):
        # Detect available cores at initialization
        self._available_cores = self._detect_available_cores()
        self._max_cores = min(self._available_cores, 8)
        self._min_items_for_parallel = 100
        self._multiprocessing_available = self._test_multiprocessing()
        
        # Logging configuration
        self._logger_configured = False
        self._setup_default_logging()
    
    def _detect_available_cores(self) -> int:
        """Detect the number of available CPU cores."""
        try:
            return max(1, mp.cpu_count())
        except Exception:
            return 1
    
    def _test_multiprocessing(self) -> bool:
        """Test if multiprocessing is available and safe to use."""
        try:
            mp.cpu_count()  # Simple check if multiprocessing works
            return True
        except Exception:
            return False
    
    @property
    def available_cores(self) -> int:
        """Get the number of available CPU cores (read-only)."""
        return self._available_cores
    
    @property
    def max_cores(self) -> int:
        """Get the maximum number of cores to use for parallel processing."""
        return self._max_cores
    
    @max_cores.setter
    def max_cores(self, value: int) -> None:
        """Set the maximum number of cores to use for parallel processing."""
        if value < 0:
            raise ValueError("max_cores must be non-negative")
        if value > self._available_cores:
            raise ValueError(f"max_cores ({value}) cannot exceed available cores ({self._available_cores})")
        self._max_cores = value
    
    @property
    def min_items_for_parallel(self) -> int:
        """Get the minimum number of items required to use parallel processing."""
        return self._min_items_for_parallel
    
    @min_items_for_parallel.setter
    def min_items_for_parallel(self, value: int) -> None:
        """Set the minimum number of items required to use parallel processing."""
        if value < 0:
            raise ValueError("min_items_for_parallel must be non-negative")
        self._min_items_for_parallel = value
    
    @property
    def multiprocessing_available(self) -> bool:
        """Check if multiprocessing is available (read-only)."""
        return self._multiprocessing_available
    
    def disable_parallel(self) -> None:
        """Disable all parallel processing by setting max_cores to 0."""
        self._max_cores = 0
    
    def enable_parallel(self, max_cores: Optional[int] = None) -> None:
        """Enable parallel processing."""
        if max_cores is None:
            self._max_cores = min(self._available_cores, 8)
        else:
            self.max_cores = max_cores
    
    def _setup_default_logging(self) -> None:
        """Set up default logging to silence all pyrion logs by default."""
        pyrion_logger = logging.getLogger("pyrion")
        if not pyrion_logger.handlers:
            # Add NullHandler to silence logs by default
            pyrion_logger.addHandler(logging.NullHandler())
            pyrion_logger.setLevel(logging.DEBUG)  # Allow all levels, handler controls output
    
    def set_log_level(self, level: Union[str, int]) -> None:
        """Configure logging for the pyrion package.
        
        Args:
            level: Logging level as string ("DEBUG", "INFO", "WARNING", "ERROR") 
                  or int (logging.DEBUG, logging.INFO, etc.)
        """
        # Convert string levels to int
        if isinstance(level, str):
            level = level.upper()
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL
            }
            if level not in level_map:
                raise ValueError(f"Invalid log level: {level}. Must be one of {list(level_map.keys())}")
            level = level_map[level]
        
        pyrion_logger = logging.getLogger("pyrion")
        
        # Remove existing handlers except NullHandler
        for handler in pyrion_logger.handlers[:]:
            if not isinstance(handler, logging.NullHandler):
                pyrion_logger.removeHandler(handler)
        
        # If not already configured, add a StreamHandler
        if not self._logger_configured:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            pyrion_logger.addHandler(handler)
            self._logger_configured = True
        
        # Set level on all handlers
        pyrion_logger.setLevel(level)
        for handler in pyrion_logger.handlers:
            if not isinstance(handler, logging.NullHandler):
                handler.setLevel(level)

    def summary(self) -> dict:
        """Get a summary of current configuration."""
        return {
            "available_cores": self._available_cores,
            "max_cores": self._max_cores,
            "min_items_for_parallel": self._min_items_for_parallel,
            "multiprocessing_available": self._multiprocessing_available,
            "parallel_enabled": self._max_cores > 0,
            "logging_configured": self._logger_configured
        }


# Global configuration instance
_config = PyrionConfig()

def get_available_cores() -> int:
    """Get the number of available CPU cores."""
    return _config.available_cores


def get_max_cores() -> int:
    """Get the current maximum number of cores for parallel processing."""
    return _config.max_cores


def set_max_cores(cores: int) -> None:
    """Set the maximum number of cores to use for parallel processing."""
    _config.max_cores = cores


def get_min_items_for_parallel() -> int:
    """Get the minimum number of items required for parallel processing."""
    return _config.min_items_for_parallel


def set_min_items_for_parallel(items: int) -> None:
    """Set the minimum number of items required for parallel processing."""
    _config.min_items_for_parallel = items


def disable_parallel() -> None:
    """Disable all parallel processing."""
    _config.disable_parallel()


def enable_parallel(max_cores: Optional[int] = None) -> None:
    """Enable parallel processing with optional core limit."""
    _config.enable_parallel(max_cores)


def is_multiprocessing_available() -> bool:
    """Check if multiprocessing is available."""
    return _config.multiprocessing_available


def get_config_summary() -> dict:
    """Get a summary of current configuration."""
    return _config.summary()


def set_loglevel(level: Union[str, int]) -> None:
    """Set logging level for the pyrion package.
    
    Examples:
        >>> import pyrion
        >>> pyrion.set_loglevel("INFO")     # Enable info-level logging
        >>> pyrion.set_loglevel("DEBUG")    # Enable debug-level logging  
        >>> pyrion.set_loglevel("WARNING")  # Enable warning+ only
    """
    _config.set_log_level(level)
