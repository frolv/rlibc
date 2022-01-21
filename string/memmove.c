// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>

#include <string.h>

void *memmove(void *dst, const void *src, size_t n)
{
    if (dst > src && (uintptr_t)dst < (uintptr_t)src + n) {
        // If the memory regions overlap, and dst is higher, the bytes must be
        // copied backwards to avoid clobbering data.
        __rc_copy_bytes_bwd(dst, src, n);
    } else if (dst != src) {
        // Otherwise, run a forwards copy, as this is generally more efficient
        // on most architectures.
        __rc_copy_bytes_fwd(dst, src, n);
    }
    return dst;
}
