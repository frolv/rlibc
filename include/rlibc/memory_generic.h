// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_MEMORY_GENERIC_H
#define RLIBC_RLIBC_MEMORY_GENERIC_H

// This file defines generic implementations of memory copying and filling
// operations. Targets may chose to provide their own optimized implementations
// instead.
//
// By default, no functions are defined when this header is included, allowing
// targets to pull in only those they require.

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

#if defined(__RLIBC_GENERIC_COPY_BYTES_FWD)
#define __RLIBC_HAS_COPY_BYTES_FWD 1

// Copies n bytes from src to dst in ascending order.
static inline void __rc_copy_bytes_fwd(uint8_t *dst,
                                       const uint8_t *src,
                                       size_t n)
{
    while (n > 0) {
        *dst++ = *src++;
        --n;
    }
}

#endif  // defined(__RLIBC_GENERIC_COPY_BYTES_FWD)

#if defined(__RLIBC_GENERIC_SET_BYTES)
#define __RLIBC_HAS_SET_BYTES 1

// Sets n bytes starting from dst to the value c.
static inline void __rc_set_bytes(uint8_t *dst, uint8_t c, size_t n)
{
    while (n > 0) {
        *dst++ = c;
        --n;
    }
}

#endif  // defined(__RLIBC_GENERIC_SET_BYTES)

#if defined(__RLIBC_GENERIC_SCAN_BYTE)
#define __RLIBC_HAS_SCAN_BYTE 1

// Finds the first occurrence of c within n bytes of ptr, if any.
static inline const uint8_t *__rc_scan_byte(const uint8_t *ptr,
                                            uint8_t c,
                                            size_t n)
{
    for (size_t i = 0; i < n; ++i) {
        if (ptr[i] == c) {
            return ptr + i;
        }
    }
    return NULL;
}

#endif  // defined(__RLIBC_GENERIC_SCAN_BYTE)

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_RLIBC_MEMORY_GENERIC_H
