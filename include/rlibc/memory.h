// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_MEMORY_H
#define RLIBC_RLIBC_MEMORY_H

// Memory manipulation functions.
//
// Many of the macros and functions in this file are to be defined by targets
// within the header <rlibc/target/memory.h>. This header provides descriptions
// of the required target definitions, as well as simple checks to validate that
// they exist and have suitable values.

#include <rlibc/target/memory.h>

#include <limits.h>

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

//
// Target preprocessor constants.
//

// __RLIBC_WORDSIZE
//
// Targets should define __RLIBC_WORDSIZE to the number of bits within a word
// (e.g. 32 or 64).
#ifndef __RLIBC_WORDSIZE
#error Target must define __RLIBC_WORDSIZE to the number of bits in a word.
#endif  // __RLIBC_WORDSIZE

#if __RLIBC_WORDSIZE < CHAR_BIT || __RLIBC_WORDSIZE > 128
#error Invalid value for __RLIBC_WORDSIZE.
#endif  // __RLIBC_WORDSIZE < CHAR_BIT || __RLIBC_WORDSIZE > 128

//
// Target functions.
//
// Each target must provide an implementation for the functions below. This may
// be an optimized implementation for the architecture. Alternatively, a target
// can choose to use a generic implementation of any of these functions by
// defining the appropriate macro and including <rlibc/memory_generic.h>.
//

// void __rc_copy_bytes_fwd(uint8_t *dst, const uint8_t *src, size_t n);
//
// Copies n bytes from src to dst in ascending order (i.e. from src[0] to
// src[n - 1]).
//
// A generic implementation can be pulled from <rlibc/memory_generic.h> by
// defining the macro __RLIBC_GENERIC_COPY_BYTES_FWD.
#ifndef __RLIBC_HAS_COPY_BYTES_FWD
#error Target must implement __rc_copy_bytes_fwd.
#endif  // __RLIBC_HAS_COPY_BYTES_FWD

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_RLIBC_MEMORY_H
