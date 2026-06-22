#pragma once
// =============================================================================
// sgdsp - Platform Detection and Configuration
// =============================================================================

// =============================================================================
// Platform Detection (auto-detect if not defined)
// =============================================================================

// ARM Cortex-M7 (Daisy Seed 2 DFM, i.MX RT1060, etc.)
#if defined(__ARM_ARCH_7EM__) && !defined(SGDSP_PLATFORM_M7)
    #define SGDSP_PLATFORM_M7
#endif

// ARM Cortex-M85 with Helium MVE
#if defined(__ARM_FEATURE_MVE) && !defined(SGDSP_PLATFORM_M85)
    #define SGDSP_PLATFORM_M85
#endif

// =============================================================================
// CMSIS-DSP Configuration
// =============================================================================
#if defined(SGDSP_USE_CMSIS) && SGDSP_USE_CMSIS
    #if __has_include(<arm_math.h>)
        #include <arm_math.h>
        #define SGDSP_HAS_CMSIS 1
    #else
        #define SGDSP_HAS_CMSIS 0
        #warning "SGDSP_USE_CMSIS enabled but arm_math.h not found"
    #endif
#else
    #define SGDSP_HAS_CMSIS 0
#endif

// =============================================================================
// Data Alignment
// =============================================================================
#if defined(SGDSP_PLATFORM_M85) || defined(__ARM_FEATURE_MVE)
    // MVE optimal alignment: 8 bytes for 128-bit vectors
    constexpr inline std::size_t kDataAlignment = 8;
#else
    // M7 and generic ARM: 4 bytes
    constexpr inline std::size_t kDataAlignment = 4;
#endif

#ifdef _MSC_VER
    #define SGDSP_ALIGNED __declspec(align(8))
#else
    #define SGDSP_ALIGNED __attribute__((aligned(kDataAlignment)))
#endif

// =============================================================================
// Debug Assertions
// =============================================================================
#ifndef SGDSP_ASSERT
    #if defined(SGDSP_DEBUG) && SGDSP_DEBUG
        #if defined(__arm__) || defined(__ARM_ARCH)
            #define SGDSP_ASSERT(x) do { if (!(x)) __BKPT(0); } while(0)
        #else
            #include <cassert>
            #define SGDSP_ASSERT(x) assert(x)
        #endif
    #else
        #define SGDSP_ASSERT(x) ((void)0)
    #endif
#endif

// =============================================================================
// Inline Hints
// =============================================================================
#ifdef _MSC_VER
    #define SGDSP_INLINE __forceinline
    #define SGDSP_NOINLINE __declspec(noinline)
#else
    #define SGDSP_INLINE inline __attribute__((always_inline))
    #define SGDSP_NOINLINE __attribute__((noinline))
#endif

// =============================================================================
// DSP Intrinsics Availability
// =============================================================================
#if defined(__ARM_FEATURE_DSP)
    #define SGDSP_HAS_DSP_INTRINSICS 1
#else
    #define SGDSP_HAS_DSP_INTRINSICS 0
#endif

#if defined(__ARM_FEATURE_MVE)
    #define SGDSP_HAS_MVE 1
    #if __has_include(<arm_mve.h>)
        #include <arm_mve.h>
    #endif
#else
    #define SGDSP_HAS_MVE 0
#endif

// =============================================================================
// Memory Placement Macros (defaults - override in platform config)
// =============================================================================
// These macros allow placing data in specific memory regions for performance.
// On platforms without special memory regions, they expand to nothing.
// Include your platform config (e.g., sgdsp_daisy_seed2.hpp) BEFORE sgdsp.hpp
// to define platform-specific placements.

// DTCM - Tightly Coupled Memory (fastest, 0-wait state)
// Use for: filter states, coefficients, hot data accessed every sample
#ifndef SGDSP_DTCM
    #define SGDSP_DTCM
#endif

// SDRAM - External RAM (slower, but large capacity)
// Use for: large delay lines, reverb buffers, sample storage (>10KB)
#ifndef SGDSP_SDRAM
    #define SGDSP_SDRAM
#endif

// AXI RAM - Internal RAM (moderate speed, general purpose)
#ifndef SGDSP_AXI_RAM
    #define SGDSP_AXI_RAM
#endif

// Combined helper for hot-path data
#ifndef SGDSP_HOT_DATA
    #define SGDSP_HOT_DATA SGDSP_DTCM
#endif

// ITCM - Instruction Tightly Coupled Memory (zero-wait-state code execution)
// Use for: audio callbacks, inner DSP loops, any function on the audio IRQ path
#ifndef SGDSP_ITCM
    #define SGDSP_ITCM
#endif

// =============================================================================
// Profiling Timestamp (DWT cycle counter on ARM, no-op elsewhere)
// =============================================================================
// Enable with -DSGDSP_PROFILE in firmware build.
// DWT->CYCCNT must be enabled by the application before use.
#if defined(SGDSP_PROFILE) && defined(SGDSP_PLATFORM_M7)
    #define SGDSP_TIMESTAMP() DWT->CYCCNT
#else
    #define SGDSP_TIMESTAMP() 0u
#endif

// Interrupt disable/enable for atomic profiling snapshots.
// CMSIS core headers (which provide __disable_irq/__enable_irq) are already
// in scope when SGDSP_PLATFORM_M7 is defined (same dependency as DWT->CYCCNT).
#if defined(SGDSP_PROFILE) && defined(SGDSP_PLATFORM_M7)
    #define SGDSP_DISABLE_IRQ() __disable_irq()
    #define SGDSP_ENABLE_IRQ()  __enable_irq()
#else
    #define SGDSP_DISABLE_IRQ() ((void)0)
    #define SGDSP_ENABLE_IRQ()  ((void)0)
#endif
