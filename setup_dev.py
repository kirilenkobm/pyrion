from setuptools import setup, Extension
import numpy as np

# Common optimization flags for all extensions
common_flags = ["-O3", "-DNDEBUG"]

# Additional flags for faiparser to handle large files
faiparser_flags = common_flags + [
    "-D_FILE_OFFSET_BITS=64",  # Enable large file support
    "-D_GNU_SOURCE",           # Enable GNU extensions (strndup, etc.)
    "-funroll-loops",          # Unroll loops for better performance
    "-finline-functions",      # Inline small functions
]

ext_modules = [
    Extension(
        "pyrion._chainparser",
        sources=["csrc/chainparser.c"],
        include_dirs=[np.get_include()],
        extra_compile_args=common_flags,
    ),
    Extension(
        "pyrion._bed12parser",
        sources=["csrc/bed12parser.c"],
        include_dirs=[np.get_include()],
        extra_compile_args=common_flags,
    ),
    Extension(
        "pyrion._fastaparser",
        sources=["csrc/fastaparser.c"],
        include_dirs=[np.get_include()],
        extra_compile_args=common_flags,
    ),
    Extension(
        "pyrion._narrowbedparser",
        sources=["csrc/narrowbedparser.c"],
        include_dirs=[np.get_include()],
        extra_compile_args=common_flags,
    ),
    Extension(
        "pyrion._faiparser",
        sources=["csrc/faiparser.c"],
        extra_compile_args=faiparser_flags,
    ),
    Extension(
        "pyrion._gtfparser",
        sources=["csrc/gtfparser.c"],
        include_dirs=[np.get_include()],
        extra_compile_args=common_flags,
    )
]

setup(
    name="pyrion",
    ext_modules=ext_modules
)