// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT - style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>

size_t strlcpy(char *__restrict dst, const char *__restrict src, size_t n)
{
    size_t size = 0;

    if (n > 0) {
        for (; size < n - 1 && src[size] != '\0'; ++size) {
            dst[size] = src[size];
        }
        dst[size] = '\0';
    }

    if (src[size] != '\0') {
        size += strlen(&src[size]);
    }

    return size;
}
