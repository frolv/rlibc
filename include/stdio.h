// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_STDIO_H
#define RLIBC_STDIO_H

#include <rlibc/compiler.h>

#include <rlibc.h>
#include <stdarg.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

#define EOF (-1)

typedef struct rlibc_file {
} FILE;

extern FILE *const stdout;

int printf(const char *__restrict format, ...) __rc_printf(1, 2);
int fprintf(FILE *stream, const char *__restrict format, ...) __rc_printf(2, 3);
int sprintf(char *__restrict str, const char *__restrict format, ...)
    __rc_printf(2, 3);
int snprintf(char *__restrict str,
             size_t size,
             const char *__restrict format,
             ...) __rc_printf(3, 4);

int vprintf(const char *__restrict format, va_list ap) __rc_printf(1, 0);
int vfprintf(FILE *stream, const char *__restrict format, va_list ap)
    __rc_printf(2, 0);
int vsprintf(char *__restrict str, const char *__restrict format, va_list ap)
    __rc_printf(2, 0);
int vsnprintf(char *__restrict str,
              size_t size,
              const char *__restrict format,
              va_list ap) __rc_printf(3, 0);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_STDIO_H
