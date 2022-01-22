// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>

#include <stdint.h>
#include <string.h>

size_t strlen(const char *s)
{
    if (s == NULL) {
        return 0;
    }
    return (const char *)__rc_scan_byte((const uint8_t *)s, '\0', SIZE_MAX) - s;
}
