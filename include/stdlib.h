// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_STDLIB_H
#define RLIBC_STDLIB_H

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

#endif  // RLIBC_STDLIB_H
