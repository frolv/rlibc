// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_TARGET_MEMORY_H
#define RLIBC_RLIBC_TARGET_MEMORY_H

#define __RLIBC_WORDSIZE 32

#define __RLIBC_GENERIC_COPY_BYTES_BWD
#define __RLIBC_GENERIC_SCAN_BYTE
#include <rlibc/memory_generic.h>

#define __RLIBC_HAS_COPY_BYTES_FWD 1
static inline void __rc_copy_bytes_fwd(uint8_t *dst,
                                       const uint8_t *src,
                                       size_t n)
{
    int a, b, c;

    if (n > 0) {
        __asm__ volatile("rep movsb"
                         : "=&c"(a), "=&D"(b), "=&S"(c)
                         : "0"(n), "1"(dst), "2"(src)
                         : "memory");
    }
}

#define __RLIBC_HAS_SET_BYTES 1
static inline void __rc_set_bytes(uint8_t *dst, uint8_t c, size_t n)
{
    int a, b;

    if (n > 0) {
        __asm__ volatile("rep stosb"
                         : "=&c"(a), "=&D"(b)
                         : "a"(c), "1"(dst), "0"(n)
                         : "memory");
    }
}

#endif  // RLIBC_RLIBC_TARGET_MEMORY_H
