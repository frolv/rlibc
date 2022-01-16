// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n)
{
    while (n > 0) {
        if (*s1 != *s2) {
            return *s1 - *s2;
        }

        if (*s1 == '\0') {
            return 0;
        }

        --n;
        ++s1;
        ++s2;
    }

    return 0;
}
