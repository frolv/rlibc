// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_STRING_H
#define RLIBC_STRING_H

#include <rlibc.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

void *memcpy(void *__restrict dst, const void *__restrict src, size_t n);
void *memset(void *dst, int c, size_t n);
int memcmp(const void *s1, const void *s2, size_t n);

int strcmp(const char *s1, const char *s2);
int strncmp(const char *s1, const char *s2, size_t n);

char *strcpy(char *__restrict dst, const char *__restrict src);
char *strncpy(char *__restrict dst, const char *__restrict src, size_t n);
size_t strlcpy(char *__restrict dst, const char *__restrict src, size_t n);

size_t strlen(const char *s);
size_t strnlen(const char *s, size_t maxlen);

char *strrev(char *s);

char *strerror(int errnum);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_STRING_H
