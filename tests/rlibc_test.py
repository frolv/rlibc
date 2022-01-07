# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.
"""Unit test helpers for rlibc."""

import ctypes
from pathlib import Path
import subprocess
import unittest


class RlibcTest(unittest.TestCase):
    """Base class for rlibc test cases"""

    # Path to the test rlibc binary from the rlibc repository root.
    RLIBC_TEST_SO: Path = Path('build') / 'test_rlibc.so'

    @classmethod
    def setUpClass(cls):
        root = subprocess.check_output(
            ('git', 'rev-parse', '--show-toplevel')).decode('utf-8').strip()

        lib = Path(root) / cls.RLIBC_TEST_SO

        if not lib.exists():
            raise RuntimeError('No rlibc library found at %s' % lib)

        cls._rlibc = ctypes.cdll.LoadLibrary(lib)
