// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>

#include <string.h>

void *memchr(const void *s, int c, size_t n)
{
    return (void *)__rc_scan_byte(s, c, n);
}
