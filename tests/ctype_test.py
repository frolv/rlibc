#!/usr/bin/env python3
# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.
"""Tests rlibc's implementation of <ctype.h> functions."""

import ctypes
import string
from typing import Set
import unittest

from rlibc_test import RlibcTest


def _exclude_chars(exclude: str) -> Set[int]:
    return set(range(0, 256)) - set(ord(c) for c in exclude)


class IsalnumTest(RlibcTest):
    """Tests the isalnum() function."""

    def test_alnum(self):
        for c in string.ascii_letters + string.digits:
            self.assertTrue(bool(self._rlibc.isalnum(ord(c))))

    def test_nonalnum(self):
        for c in _exclude_chars(string.ascii_letters + string.digits):
            self.assertFalse(bool(self._rlibc.isalnum(c)))


class IsalphaTest(RlibcTest):
    """Tests the isalpha() function."""

    def test_alpha(self):
        for c in string.ascii_letters:
            self.assertTrue(bool(self._rlibc.isalpha(ord(c))))

    def test_nonalpha(self):
        for c in _exclude_chars(string.ascii_letters):
            self.assertFalse(bool(self._rlibc.isalpha(c)))


class IsdigitTest(RlibcTest):
    """Tests the isdigit() function."""

    def test_digit(self):
        for c in string.digits:
            self.assertTrue(bool(self._rlibc.isdigit(ord(c))))

    def test_nondigit(self):
        for c in _exclude_chars(string.digits):
            self.assertFalse(bool(self._rlibc.isdigit(c)))


class IslowerTest(RlibcTest):
    """Tests the islower() function."""

    def test_upper(self):
        for c in string.ascii_lowercase:
            self.assertTrue(bool(self._rlibc.islower(ord(c))))

    def test_nonupper(self):
        for c in _exclude_chars(string.ascii_lowercase):
            self.assertFalse(bool(self._rlibc.islower(c)))


class IsupperTest(RlibcTest):
    """Tests the isupper() function."""

    def test_lower(self):
        for c in string.ascii_uppercase:
            self.assertTrue(bool(self._rlibc.isupper(ord(c))))

    def test_nonlower(self):
        for c in _exclude_chars(string.ascii_uppercase):
            self.assertFalse(bool(self._rlibc.isupper(c)))


if __name__ == '__main__':
    unittest.main()
