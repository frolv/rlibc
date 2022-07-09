// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/compiler.h>

#include <stdio.h>

#if defined(__radix_kernel__)

#include <radix/tty.h>

static size_t stderr_write(__RC_UNUSED FILE *stream,
                           const char *data,
                           size_t size)
{
    tty_write(data, size);
    return size;
}

#else  // defined(__radix_kernel__)

static size_t stderr_write(__RC_UNUSED FILE *stream,
                           __RC_UNUSED const char *data,
                           __RC_UNUSED size_t size)
{
    // TODO(frolv): Implement userspace write.
    return 0;
}

#endif  // defined(__radix_kernel__)

static FILE stderr_file = {
    .write = stderr_write,
};

FILE *const stderr = &stderr_file;
