// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>

#include <string.h>

size_t strnlen(const char *s, size_t maxlen)
{
    if (s == NULL) {
        return 0;
    }

    const char *nul =
        (const char *)__rc_scan_byte((const uint8_t *)s, '\0', maxlen);
    return nul ? (size_t)(nul - s) : maxlen;
}
