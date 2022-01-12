// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/util.h>

#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "printf.h"

struct vsnprintf_context {
    char *buffer;
    size_t remaining_size;
};

size_t callback(void *ctx, const char *string, size_t size)
{
    struct vsnprintf_context *context = ctx;
    size_t to_write = min(size, context->remaining_size);

    if (to_write > 0) {
        memcpy(context->buffer, string, to_write);
        context->buffer += to_write;
        context->remaining_size -= to_write;
    }

    // snprintf() should return the number of characters that would have been
    // written if the buffer were large enough, regardless of the actual written
    // size. While this is generally considered a poor design choice and has led
    // to many bugs, a standard is a standard.
    return size;
}

int vsnprintf(char *__restrict str,
              size_t size,
              const char *__restrict format,
              va_list ap)
{
    struct vsnprintf_context ctx = {.buffer = str,
                                    .remaining_size = size > 0 ? size - 1 : 0};

    int ret = rc_callback_printf(callback, &ctx, format, ap);

    if (size > 0) {
        *ctx.buffer = '\0';
    }

    return ret;
}
