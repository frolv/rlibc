// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <stdio.h>

int printf(const char *__restrict format, ...)
{
    va_list ap;

    va_start(ap, format);
    int ret = vfprintf(stdout, format, ap);
    va_end(ap);

    return ret;
}
