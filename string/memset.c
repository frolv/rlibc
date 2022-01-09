// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>
#include <rlibc/util.h>

#include <limits.h>
#include <string.h>

void *memset(void *dst, int c, size_t n)
{
    size_t count = n;
    const uint8_t byte = c;
    uint8_t *ptr = dst;

#if defined(__RLIBC_GENERIC_SET_BYTES)
#if CHAR_BIT == 8 && (__RLIBC_WORDSIZE == 32 || __RLIBC_WORDSIZE == 64)
    // With a 4- or 8-byte word, optimize by setting one word at a time instead
    // of one byte.

    // First, align the destination pointer to the word size in case the system
    // requires aligned memory access.
    const size_t align = __RLIBC_WORDSIZE / CHAR_BIT;
    const size_t bytes_to_align = align - ((uintptr_t)ptr % align);
    const size_t small_bytes = min(bytes_to_align, count);
    __rc_set_small(ptr, byte, small_bytes);
    count -= small_bytes;
    ptr += small_bytes;

    if (count == 0) {
        return dst;
    }

#if __RLIBC_WORDSIZE == 32
    uint32_t *word_ptr = (uint32_t *)ptr;
    const uint32_t word = byte * 0x01010101;
#elif __RLIBC_WORDSIZE == 64
    uint64_t *word_ptr = (uint64_t *)ptr;
    const uint64_t word = byte * 0x0101010101010101;
#endif

    size_t word_count = count / sizeof word;
    for (size_t i = 0; i < word_count; ++i) {
        word_ptr[i] = word;
    }
    count -= word_count * sizeof word;
    ptr += word_count * sizeof word;

#endif  // CHAR_BIT == 8 && (__RLIBC_WORDSIZE == 32 || __RLIBC_WORDSIZE == 64)
#endif  // defined(__RLIBC_GENERIC_SET_BYTES)

    __rc_set_bytes(ptr, byte, count);
    return dst;
}
