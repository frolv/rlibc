// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>
#include <stdint.h>

int memcmp(const void *s1, const void *s2, size_t n)
{
    const uint8_t *s = s1;
    const uint8_t *t = s2;

    while (n > 0) {
        if (*s != *t) {
            return *s - *t;
        }

        --n;
        ++s;
        ++t;
    }

    return 0;
}
