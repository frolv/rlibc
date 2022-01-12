#!/usr/bin/env python3
# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.
"""Tests rlibc's implementation of <stdio.h> functions."""

import ctypes
import unittest

from rlibc_test import RlibcTest


class SnprintfTest(RlibcTest):
    """Tests the snprintf() function."""

    def test_empty_format_string(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(self._rlibc.snprintf(buffer, len(buffer), b''), 0)
        self.assertEqual(buffer.raw, b'\0' + b'\xff' * 15)

    def test_no_format_sequence_fits(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'hello world'), 11)
        self.assertEqual(buffer.raw, b'hello world\0\xff\xff\xff\xff')

    def test_no_format_sequence_exceeds(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer),
                                 b'this is a long string'), 21)
        self.assertEqual(buffer.raw, b'this is a long \0')

    def test_zero_size(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(self._rlibc.snprintf(buffer, 0, b'hello world'), 11)
        self.assertEqual(buffer.raw, b'\xff' * 16)

    def test_format_char_single(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'%cello', ord('j')), 5)
        self.assertEqual(buffer.raw, b'jello\0' + b'\xff' * 10)

    def test_format_char_multiple(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'%c%c%c%c%c%c%c%c',
                                 ord('s'), ord('n'), ord('p'), ord('r'),
                                 ord('i'), ord('n'), ord('t'), ord('f')), 8)
        self.assertEqual(buffer.raw, b'snprintf\0' + b'\xff' * 7)

    def test_format_char_width(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'number:%4c', ord('9')),
            11)
        self.assertEqual(buffer.raw, b'number:   9\0\xff\xff\xff\xff')

    def test_format_char_width_ladjust(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'number:%-4c',
                                 ord('9')), 11)
        self.assertEqual(buffer.raw, b'number:9   \0\xff\xff\xff\xff')

    def test_format_char_width_long(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 256, 256)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'%250c', ord('!')), 250)
        self.assertEqual(buffer.raw, b' ' * 249 + b'!\0\xff\xff\xff\xff\xff')

    def test_format_string(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'hello %s', b'world'),
            11)
        self.assertEqual(buffer.raw, b'hello world\0\xff\xff\xff\xff')

    def test_format_string_width(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'%15s', b'radix libc'),
            15)
        self.assertEqual(buffer.raw, b'     radix libc\0')

    def test_format_string_width_ladjust(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'%-15s', b'radix libc'),
            15)
        self.assertEqual(buffer.raw, b'radix libc     \0')

    def test_format_string_precision(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'%.5s', b'precision'),
            5)
        self.assertEqual(buffer.raw, b'preci\0' + b'\xff' * 10)

    def test_format_string_precision_zero(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'zero %.s',
                                 b'precision'), 5)
        self.assertEqual(buffer.raw, b'zero \0' + b'\xff' * 10)

    def test_format_string_null(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'str is %s',
                                 ctypes.c_char_p(None)), 13)
        self.assertEqual(buffer.raw, b'str is (null)\0\xff\xff')

    def test_format_percent(self):
        buffer = ctypes.create_string_buffer(b'\xff' * 16, 16)
        self.assertEqual(
            self._rlibc.snprintf(buffer, len(buffer), b'loading: 10%%!',
                                 ctypes.c_char_p(None)), 13)
        self.assertEqual(buffer.raw, b'loading: 10%!\0\xff\xff')


if __name__ == '__main__':
    unittest.main()
