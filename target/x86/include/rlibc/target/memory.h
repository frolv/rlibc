// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_TARGET_MEMORY_H
#define RLIBC_RLIBC_TARGET_MEMORY_H

#define __RLIBC_WORDSIZE 32

// The compiler optimizes byte copying operations well on x86, so there's no
// need to override them.
#define __RLIBC_GENERIC_COPY_BYTES_FWD
#define __RLIBC_GENERIC_COPY_BYTES_BWD

#define __RLIBC_GENERIC_SET_BYTES
#define __RLIBC_GENERIC_SCAN_BYTE
#include <rlibc/memory_generic.h>

#endif  // RLIBC_RLIBC_TARGET_MEMORY_H
