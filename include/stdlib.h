// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_STDLIB_H
#define RLIBC_STDLIB_H

#include <rlibc/compiler.h>

#include <rlibc.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

#if !defined(__radix_kernel__)

void *malloc(size_t size);
void free(void *ptr);

#endif  // !defined(__radix_kernel__)

#if defined(__radix_kernel__)

#include <radix/slab.h>

static inline void *malloc(size_t size) { return kmalloc(size); }
static inline void free(void *ptr) { return kfree(ptr); }

#endif  // defined(__radix_kernel__)

#ifdef __cplusplus
}
#endif  // __cplusplus

// These function prototypes are required to build gcc, but are yet
// unimplemented.
__rc_noreturn void exit(int status);
__rc_noreturn void abort(void);
int abs(int j);
int atoi(const char *nptr);
void *calloc(size_t nmemb, size_t size);
char *getenv(const char *name);

#endif  // RLIBC_STDLIB_H
