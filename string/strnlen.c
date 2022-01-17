// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>

size_t strnlen(const char *s, size_t maxlen)
{
    size_t len = 0;
    if (s == NULL) {
        return len;
    }

    while (maxlen > 0 && *s) {
        ++len;
        ++s;
        --maxlen;
    }
    return len;
}
