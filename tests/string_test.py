#!/usr/bin/env python3
# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.
"""Tests rlibc's implementation of <string.h> functions."""

import ctypes
import functools
import unittest

from rlibc_test import RlibcTest


class MemcmpTest(RlibcTest):
    """Tests the memcmp() function."""

    def test_equal(self):
        self.assertEqual(self._rlibc.memcmp(b'\xef', b'\xef', 1), 0)
        self.assertEqual(self._rlibc.memcmp(b'abcdefgh', b'abcdefgh', 4), 0)
        self.assertEqual(self._rlibc.memcmp(b'abcdefgh', b'abcdefgh', 8), 0)
        self.assertEqual(self._rlibc.memcmp(b'0' * 1024, b'0' * 1024, 1024), 0)
        self.assertEqual(
            self._rlibc.memcmp(b'\x00\x00\x00\x00\x00',
                               b'\x00\x00\x00\x00\x01', 4), 0)

    def test_less_than(self):
        self.assertLess(self._rlibc.memcmp(b'1', b'2', 1), 0)
        self.assertLess(
            self._rlibc.memcmp(b'\x00\x00\x00\x00\x00',
                               b'\x00\x00\x00\x00\x01', 5), 0)

    def test_greater_than(self):
        self.assertGreater(self._rlibc.memcmp(b'\xff', b'\x30'), 0)
        self.assertGreater(
            self._rlibc.memcmp(b'\x00\x00\x00\x00\x01',
                               b'\x00\x00\x00\x00\x00', 5), 0)

    def test_zero(self):
        self.assertEqual(self._rlibc.memcmp(b'', b'', 0), 0)
        self.assertEqual(
            self._rlibc.memcmp(b'\x01\x02\x03', b'\x01\x02\x03', 0), 0)


class MemcpyTest(RlibcTest):
    """Tests the memcpy() function."""

    def test_full_copy(self):
        src = ctypes.create_string_buffer(b'0123456789')
        dst = ctypes.create_string_buffer(b'\xff' * 8, 8)
        self._rlibc.memcpy(dst, src, len(dst))
        self.assertEqual(dst.value, b'01234567')

    def test_partial_copy(self):
        src = ctypes.create_string_buffer(b'0123456789')
        dst = ctypes.create_string_buffer(b'\xff' * 8, 8)
        self._rlibc.memcpy(dst, src, 4)
        self.assertEqual(dst.value, b'0123\xff\xff\xff\xff')

    def test_zero_copy(self):
        src = ctypes.create_string_buffer(b'0123456789')
        dst = ctypes.create_string_buffer(b'\xff' * 8, 8)
        self._rlibc.memcpy(dst, src, 0)
        self.assertEqual(dst.value, b'\xff\xff\xff\xff\xff\xff\xff\xff')

    def test_large_copy(self):
        large_size = 2**22  # 4 MiB
        src = ctypes.create_string_buffer(b'\xaa' * large_size)
        dst = ctypes.create_string_buffer(b'\xff' * large_size)
        self._rlibc.memcpy(dst, src, large_size)
        self.assertEqual(dst.value, src.value)


class MemsetTest(RlibcTest):
    """Tests the memset() function."""

    def test_small(self):
        buffer = ctypes.create_string_buffer(
            b'\xff\xff\xff\xff\xff\xff\xff\xff', 8)
        self._rlibc.memset(buffer, 0, len(buffer))
        self.assertEqual(buffer.raw, b'\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_large(self):
        large_size = 2**22  # 4 MiB
        buffer = ctypes.create_string_buffer(b'\xff' * large_size, large_size)
        self._rlibc.memset(buffer, 0, len(buffer))
        self.assertEqual(buffer.raw, b'\x00' * large_size)

    def test_partial(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 128, 128)
        start = ctypes.c_void_p(ctypes.addressof(buffer) + 32)
        self._rlibc.memset(start, 0xaa, 64)
        self.assertEqual(buffer.raw,
                         b'\xff' * 32 + b'\xaa' * 64 + b'\xff' * 32)

    def test_unaligned(self):
        # Start setting from a non word-aligned offset in the buffer.
        buffer = ctypes.create_string_buffer(b'\xff' * 128, 128)
        start = ctypes.c_void_p(ctypes.addressof(buffer) + 5)
        self._rlibc.memset(start, 0, len(buffer) - 5)
        self.assertEqual(buffer.raw, b'\xff' * 5 + b'\x00' * 123)


class StrcmpTest(RlibcTest):
    """Tests the strcmp() function."""

    def test_equal(self):
        self.assertEqual(self._rlibc.strcmp(b'', b''), 0)
        self.assertEqual(self._rlibc.strcmp(b'!', b'!'), 0)
        self.assertEqual(self._rlibc.strcmp(b'strcmp', b'strcmp'), 0)
        self.assertEqual(self._rlibc.strcmp(b'0' * 1024, b'0' * 1024), 0)

    def test_less_than(self):
        self.assertLess(self._rlibc.strcmp(b'', b'\x01'), 0)
        self.assertLess(self._rlibc.strcmp(b'a', b'b'), 0)
        self.assertLess(self._rlibc.strcmp(b'mike', b'oscar'), 0)
        self.assertLess(self._rlibc.strcmp(b'11111110', b'11111111'), 0)

    def test_greater_than(self):
        self.assertGreater(self._rlibc.strcmp(b' ', b''), 0)
        self.assertGreater(self._rlibc.strcmp(b'8', b'7'), 0)
        self.assertGreater(self._rlibc.strcmp(b'somebody', b'once'), 0)

    def test_sort(self):
        names = ['Bob', 'Dave', 'Alice', 'Eve', 'Bob', 'Carol']
        key = functools.cmp_to_key(lambda a, b: self._rlibc.strcmp(a, b))
        self.assertEqual(sorted(names, key=key),
                         ['Alice', 'Bob', 'Bob', 'Carol', 'Dave', 'Eve'])


class StrlenTest(RlibcTest):
    """Tests the strlen() function."""

    def test_short(self):
        self.assertEqual(self._rlibc.strlen(b'hello'), 5)
        self.assertEqual(self._rlibc.strlen(b', world'), 7)
        self.assertEqual(self._rlibc.strlen(b'hello, world'), 12)

    def test_long(self):
        self.assertEqual(self._rlibc.strlen(b'a' * 1024), 1024)
        self.assertEqual(self._rlibc.strlen(b'b' * 8192), 8192)

    def test_empty(self):
        self.assertEqual(self._rlibc.strlen(b''), 0)


class StrnlenTest(RlibcTest):
    """Tests the strnlen() function."""

    def test_terminated(self):
        self.assertEqual(self._rlibc.strnlen(b'rlibc', 10), 5)
        self.assertEqual(self._rlibc.strnlen(b'b' * 128, 256), 128)

    def test_limited(self):
        self.assertEqual(self._rlibc.strnlen(b'rlibc', 2), 2)
        self.assertEqual(self._rlibc.strnlen(b'c' * 128, 42), 42)
        self.assertEqual(self._rlibc.strnlen(b'strnlen', 6), 6)

    def test_exact_limit(self):
        self.assertEqual(self._rlibc.strnlen(b'hello', 5), 5)  # Without NUL
        self.assertEqual(self._rlibc.strnlen(b'hello', 6), 5)  # With NUL

    def test_empty(self):
        self.assertEqual(self._rlibc.strnlen(b'', 10), 0)

    def test_unterminated_string(self):
        string = ctypes.create_string_buffer(b'a' * 128, 128)
        self.assertEqual(self._rlibc.strnlen(string.raw, 100), 100)

    def test_zero_limit(self):
        self.assertEqual(self._rlibc.strnlen(b'a string', 0), 0)
        self.assertEqual(self._rlibc.strnlen(b'', 0), 0)


if __name__ == '__main__':
    unittest.main()
