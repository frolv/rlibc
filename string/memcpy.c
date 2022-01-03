// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>

#include <string.h>

void *memcpy(void *restrict dst, const void *restrict src, size_t n)
{
    __rc_copy_bytes_fwd(dst, src, n);
    return dst;
}
