// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_UTIL_H
#define RLIBC_RLIBC_UTIL_H

#define min(a, b)                              \
    ({                                         \
        __typeof(a) __min_a = a;               \
        __typeof(b) __min_b = b;               \
        __min_a < __min_b ? __min_a : __min_b; \
    })

#define max(a, b)                              \
    ({                                         \
        __typeof(a) __max_a = a;               \
        __typeof(b) __max_b = b;               \
        __max_a > __max_b ? __max_a : __max_b; \
    })

#endif  // RLIBC_RLIBC_UTIL_H
