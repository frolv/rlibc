// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_STDIO_PRINTF_H
#define RLIBC_STDIO_PRINTF_H

#include <stdarg.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

typedef size_t (*printf_callback)(void *ctx, const char *str, size_t size);

int rc_callback_printf(printf_callback callback,
                       void *context,
                       const char *__restrict format,
                       va_list ap);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_STDIO_PRINTF_H
