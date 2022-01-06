#!/usr/bin/env python3
# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.
"""Tests rlibc's implmentation of <string.h> functions."""

import ctypes
import unittest

from rlibc_test import RlibcTest


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
