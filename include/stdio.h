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

#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

typedef struct rlibc_file {
    size_t (*write)(struct rlibc_file *, const char *, size_t);
} FILE;

extern FILE *const stdout;
extern FILE *const stderr;

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

// These function prototypes are required to build gcc, but are yet
// unimplemented.
FILE *fopen(const char *__restrict pathname, const char *__restrict mode);
int fclose(FILE *stream);
size_t fread(void *__restrict ptr,
             size_t size,
             size_t nmemb,
             FILE *__restrict stream);
size_t fwrite(const void *__restrict ptr,
              size_t size,
              size_t nmemb,
              FILE *__restrict stream);
int fseek(FILE *stream, long offset, int whence);
long ftell(FILE *stream);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_STDIO_H
