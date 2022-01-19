// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT - style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>

char *strncpy(char *__restrict dst, const char *__restrict src, size_t n)
{
    size_t i = 0;

    for (; i < n && src[i] != '\0'; ++i) {
        dst[i] = src[i];
    }
    for (; i < n; ++i) {
        dst[i] = '\0';
    }

    return dst;
}
