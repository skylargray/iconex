cmake_minimum_required(VERSION 3.16)
project(iconex_224xl_harness CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Default to Release for single-config generators (Ninja/Make); no-op on MSVC multi-config.
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

if(MSVC)
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
endif()

# Repo root is three levels up from this file (tools/harness/224xl).
get_filename_component(REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../.." ABSOLUTE)
set(SGDSP_INCLUDE "${REPO_ROOT}/libs/sgdsp/include")

# RTL-parity flow (plan 024 F1d): goldens come from tools/export_golden_224xl_rtl.py
# (the Python RTL22 reference) into golden_rtl/.
#
# booth_vectors_test replaces the obsolete mult_vectors_test (pre-0022 value-domain
# primitives; the source stays on disk for the record but no longer builds).
add_executable(booth_vectors_test booth_vectors_test.cpp)
target_include_directories(booth_vectors_test PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")

add_executable(diff_harness diff_harness.cpp)
target_include_directories(diff_harness PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")

add_executable(wav_ir_tool wav_ir_tool.cpp)
target_include_directories(wav_ir_tool PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")

enable_testing()
add_test(NAME booth_vectors COMMAND booth_vectors_test "${CMAKE_CURRENT_SOURCE_DIR}/golden_rtl/booth_vectors.bin")
add_test(NAME diff_rtl COMMAND diff_harness "${CMAKE_CURRENT_SOURCE_DIR}/golden_rtl")
