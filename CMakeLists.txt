cmake_minimum_required(VERSION 4.0)
project(pyrion C)

set(CMAKE_C_STANDARD 11)

include_directories(csrc)

add_executable(pyrion
        csrc/bed12parser.c
        csrc/chainparser.c
        csrc/faiparser.c
        csrc/fastaparser.c
        csrc/gtfparser.c
        csrc/narrowbedparser.c)

execute_process(
        COMMAND python3 -c "from sysconfig import get_paths; print(get_paths()['include'])"
        OUTPUT_VARIABLE PYTHON_INCLUDE
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
        COMMAND python3 -c "import numpy; print(numpy.get_include())"
        OUTPUT_VARIABLE NUMPY_INCLUDE
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

include_directories(${PYTHON_INCLUDE})
include_directories(${NUMPY_INCLUDE})
