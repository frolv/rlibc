// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <stdio.h>

#include "printf.h"

static size_t callback(void *ctx, const char *string, size_t size)
{
    FILE *stream = ctx;
    return stream->write(stream, string, size);
}

int vfprintf(FILE *stream, const char *__restrict format, va_list ap)
{
    return rc_callback_printf(callback, stream, format, ap);
}
