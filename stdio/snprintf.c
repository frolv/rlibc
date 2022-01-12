// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <stdint.h>
#include <stdio.h>

int snprintf(char *__restrict str,
             size_t size,
             const char *__restrict format,
             ...)
{
    va_list ap;

    va_start(ap, format);
    int ret = vsnprintf(str, size, format, ap);
    va_end(ap);

    return ret;
}
