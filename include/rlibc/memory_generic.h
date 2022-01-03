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
static inline void __rc_copy_bytes_fwd(uint8_t *dst, const uint8_t *src, size_t n)
{
    while (n > 0) {
        *dst++ = *src++;
        --n;
    }
}

#endif  // defined(__RLIBC_GENERIC_COPY_BYTES_FWD)

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_RLIBC_MEMORY_GENERIC_H
