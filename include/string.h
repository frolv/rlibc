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

void *memcpy(void *restrict dst, const void *restrict src, size_t n);

int strcmp(const char *s1, const char *s2);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_STRING_H
