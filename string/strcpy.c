// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT - style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>

char *strcpy(char *__restrict dst, const char *__restrict src)
{
    char *start = dst;

    while ((*dst++ = *src++)) {}

    return start;
}
