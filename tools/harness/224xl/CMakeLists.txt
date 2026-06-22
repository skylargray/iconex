cmake_minimum_required(VERSION 3.16)
project(iconex_224xl_harness CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Default to Release for single-config generators (Ninja/Make); no-op on MSVC multi-config.
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Repo root is three levels up from this file (tools/harness/224xl).
get_filename_component(REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../.." ABSOLUTE)
set(SGDSP_INCLUDE "${REPO_ROOT}/libs/sgdsp/include")

# Desktop build: portable headers only, no platform config, no CMSIS/STM.
add_executable(mult_vectors_test mult_vectors_test.cpp)
target_include_directories(mult_vectors_test PRIVATE "${SGDSP_INCLUDE}")

# --- Re-enabled in Task 6 (diff_harness) and Task 7 (wav_ir_tool) ---
# add_executable(diff_harness diff_harness.cpp)
# target_include_directories(diff_harness PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")
#
# add_executable(wav_ir_tool wav_ir_tool.cpp)
# target_include_directories(wav_ir_tool PRIVATE "${SGDSP_INCLUDE}" "${CMAKE_CURRENT_SOURCE_DIR}")

enable_testing()
add_test(NAME mult_vectors COMMAND mult_vectors_test)
# add_test(NAME diff_concert COMMAND diff_harness "${CMAKE_CURRENT_SOURCE_DIR}/golden" 01)
