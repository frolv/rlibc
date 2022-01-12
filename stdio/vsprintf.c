// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <stdint.h>
#include <stdio.h>

int vsprintf(char *__restrict str, const char *__restrict format, va_list ap)
{
    return vsnprintf(str, SIZE_MAX, format, ap);
}
