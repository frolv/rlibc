#!/usr/bin/env python3
# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.
"""Tests rlibc's implementation of <stdio.h> functions."""

import ctypes
from typing import Tuple
import unittest

from rlibc_test import RlibcTest


def c_int_limits(ctype) -> Tuple[int, int]:
    """Returns the minimum and maximum values of a C integer type."""
    is_signed = ctype(-1).value < ctype(0).value
    bits = ctypes.sizeof(ctype) * 8

    if is_signed:
        bits -= 1
        return (-(2**bits), 2**bits - 1)

    return (0, 2**bits - 1)


class SnprintfTest(RlibcTest):
    """Tests the snprintf() function."""

    def _format(self,
                string: str,
                *args,
                bufsize: int = 64) -> Tuple[int, str]:
        buffer = ctypes.create_string_buffer(b'\xff' * bufsize, bufsize)
        count = self._rlibc.snprintf(buffer, len(buffer),
                                     string.encode('utf-8'), *args)
        return (count, buffer.value.decode('utf-8'))

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

    def test_format_int_positive(self):
        self.assertEqual(self._format('%d', 0), (1, '0'))
        self.assertEqual(self._format('%d', 7), (1, '7'))
        self.assertEqual(self._format('%d', 1234567), (7, '1234567'))
        self.assertEqual(self._format('%d + %d = %d', 11, 27, 11 + 27),
                         (12, '11 + 27 = 38'))

    def test_format_int_negative(self):
        self.assertEqual(self._format('%d', -1), (2, '-1'))
        self.assertEqual(self._format('%d', -3), (2, '-3'))
        self.assertEqual(self._format('%d', -987654), (7, '-987654'))

    def test_format_int_space(self):
        self.assertEqual(self._format('% d', 0), (2, ' 0'))
        self.assertEqual(self._format('% d', 144), (4, ' 144'))
        self.assertEqual(self._format('% d', -144), (4, '-144'))

    def test_format_int_sign(self):
        self.assertEqual(self._format('%+d', 0), (2, '+0'))
        self.assertEqual(self._format('%+d', 144), (4, '+144'))
        self.assertEqual(self._format('%+d', -144), (4, '-144'))

    def test_format_int_space_sign_precedence(self):
        # The sign flag should always override the space flag.
        self.assertEqual(self._format('% +d', 0), (2, '+0'))
        self.assertEqual(self._format('% +d', 144), (4, '+144'))
        self.assertEqual(self._format('% +d', -144), (4, '-144'))
        self.assertEqual(self._format('%+ d', 0), (2, '+0'))
        self.assertEqual(self._format('%+ d', 144), (4, '+144'))
        self.assertEqual(self._format('%+ d', -144), (4, '-144'))

    def test_format_int_precision(self):
        self.assertEqual(self._format('%.d', 8675309), (7, '8675309'))
        self.assertEqual(self._format('%.4d', 8675309), (7, '8675309'))
        self.assertEqual(self._format('%.10d', 8675309), (10, '0008675309'))
        self.assertEqual(self._format('%.1d', -27), (3, '-27'))
        self.assertEqual(self._format('%.2d', -27), (3, '-27'))
        self.assertEqual(self._format('%.6d', -27), (7, '-000027'))
        self.assertEqual(self._format('%.d', 0), (1, '0'))
        self.assertEqual(self._format('%.1d', 0), (1, '0'))
        self.assertEqual(self._format('%.2d', 0), (2, '00'))
        self.assertEqual(self._format('%.1024d', 13, bufsize=2048),
                         (1024, '0' * 1022 + '13'))

    def test_format_int_precision_flags(self):
        self.assertEqual(self._format('%+.d', 616), (4, '+616'))
        self.assertEqual(self._format('%+.3d', 616), (4, '+616'))
        self.assertEqual(self._format('%+.6d', 616), (7, '+000616'))
        self.assertEqual(self._format('%+.d', -333), (4, '-333'))
        self.assertEqual(self._format('%+.3d', -333), (4, '-333'))
        self.assertEqual(self._format('%+.6d', -333), (7, '-000333'))
        self.assertEqual(self._format('% .d', 616), (4, ' 616'))
        self.assertEqual(self._format('% .3d', 616), (4, ' 616'))
        self.assertEqual(self._format('% .6d', 616), (7, ' 000616'))
        self.assertEqual(self._format('% .d', -333), (4, '-333'))
        self.assertEqual(self._format('% .3d', -333), (4, '-333'))
        self.assertEqual(self._format('% .6d', -333), (7, '-000333'))

    def test_format_int_width(self):
        self.assertEqual(self._format('%2d', 4), (2, ' 4'))
        self.assertEqual(self._format('%2d', -4), (2, '-4'))
        self.assertEqual(self._format('%3d', -4), (3, ' -4'))
        self.assertEqual(self._format('%8.d', 22), (8, '      22'))
        self.assertEqual(self._format('%8.4d', 22), (8, '    0022'))
        self.assertEqual(self._format('%8.d', -22), (8, '     -22'))
        self.assertEqual(self._format('%8.4d', -22), (8, '   -0022'))
        self.assertEqual(self._format('%+8.d', 123), (8, '    +123'))
        self.assertEqual(self._format('%+8.4d', 123), (8, '   +0123'))
        self.assertEqual(self._format('%+8.d', -123), (8, '    -123'))
        self.assertEqual(self._format('%+8.4d', -123), (8, '   -0123'))
        self.assertEqual(self._format('% 8.d', 2022), (8, '    2022'))
        self.assertEqual(self._format('% 8.5d', 2022), (8, '   02022'))
        self.assertEqual(self._format('% 8.d', -2022), (8, '   -2022'))
        self.assertEqual(self._format('% 8.5d', -2022), (8, '  -02022'))
        self.assertEqual(self._format('%+1024.8d', 123456, bufsize=2048),
                         (1024, ' ' * 1015 + '+00123456'))

    def test_format_int_width_ladjust(self):
        self.assertEqual(self._format('%-2d', 4), (2, '4 '))
        self.assertEqual(self._format('%-2d', -4), (2, '-4'))
        self.assertEqual(self._format('%-3d', -4), (3, '-4 '))
        self.assertEqual(self._format('%-8.d', 22), (8, '22      '))
        self.assertEqual(self._format('%-8.4d', 22), (8, '0022    '))
        self.assertEqual(self._format('%-8.d', -22), (8, '-22     '))
        self.assertEqual(self._format('%-8.4d', -22), (8, '-0022   '))
        self.assertEqual(self._format('%-+8.d', 123), (8, '+123    '))
        self.assertEqual(self._format('%-+8.4d', 123), (8, '+0123   '))
        self.assertEqual(self._format('%-+8.d', -123), (8, '-123    '))
        self.assertEqual(self._format('%-+8.4d', -123), (8, '-0123   '))
        self.assertEqual(self._format('%- 8.d', 2022), (8, ' 2022   '))
        self.assertEqual(self._format('%- 8.5d', 2022), (8, ' 02022  '))
        self.assertEqual(self._format('%- 8.d', -2022), (8, '-2022   '))
        self.assertEqual(self._format('%- 8.5d', -2022), (8, '-02022  '))
        self.assertEqual(self._format('%-+1024.8d', 123456, bufsize=2048),
                         (1024, '+00123456' + ' ' * 1015))

    def test_format_int_width_zero(self):
        self.assertEqual(self._format('%02d', 4), (2, '04'))
        self.assertEqual(self._format('%02d', -4), (2, '-4'))
        self.assertEqual(self._format('%03d', -4), (3, '-04'))
        self.assertEqual(self._format('%06d', 11), (6, '000011'))
        self.assertEqual(self._format('%+06d', 11), (6, '+00011'))
        self.assertEqual(self._format('%+06d', -11), (6, '-00011'))
        self.assertEqual(self._format('%08.d', 42), (8, '00000042'))
        self.assertEqual(self._format('%08.d', -42), (8, '-0000042'))
        self.assertEqual(self._format('%08.8d', 42), (8, '00000042'))
        self.assertEqual(self._format('%08.8d', -42), (9, '-00000042'))
        self.assertEqual(self._format('%08.10d', 42), (10, '0000000042'))
        self.assertEqual(self._format('%08.10d', -42), (11, '-0000000042'))
        self.assertEqual(self._format('%+08.8d', 42), (9, '+00000042'))
        self.assertEqual(self._format('%+08.8d', -42), (9, '-00000042'))
        self.assertEqual(self._format('%+08.10d', 42), (11, '+0000000042'))
        self.assertEqual(self._format('%+08.10d', -42), (11, '-0000000042'))
        self.assertEqual(self._format('% 08.8d', 42), (9, ' 00000042'))
        self.assertEqual(self._format('% 08.8d', -42), (9, '-00000042'))
        self.assertEqual(self._format('% 08.10d', 42), (11, ' 0000000042'))
        self.assertEqual(self._format('% 08.10d', -42), (11, '-0000000042'))
        self.assertEqual(self._format('%+01024.8d', 123456, bufsize=2048),
                         (1024, f'+{"0" * 1015}00123456'))

    def test_format_int_width_zero_ladjust(self):
        # Left adjust takes precedence over the zero pad flag.
        self.assertEqual(self._format('%-02d', 4), (2, '4 '))
        self.assertEqual(self._format('%-02d', -4), (2, '-4'))
        self.assertEqual(self._format('%-03d', -4), (3, '-4 '))
        self.assertEqual(self._format('%-06d', 11), (6, '11    '))
        self.assertEqual(self._format('%-+06d', 11), (6, '+11   '))
        self.assertEqual(self._format('%-+06d', -11), (6, '-11   '))
        self.assertEqual(self._format('%-08.d', 42), (8, '42      '))
        self.assertEqual(self._format('%-08.d', -42), (8, '-42     '))
        self.assertEqual(self._format('%-08.8d', 42), (8, '00000042'))
        self.assertEqual(self._format('%-08.8d', -42), (9, '-00000042'))
        self.assertEqual(self._format('%-08.10d', 42), (10, '0000000042'))
        self.assertEqual(self._format('%-08.10d', -42), (11, '-0000000042'))
        self.assertEqual(self._format('%-+010.8d', 42), (10, '+00000042 '))
        self.assertEqual(self._format('%-+010.8d', -42), (10, '-00000042 '))
        self.assertEqual(self._format('%-+010.10d', 42), (11, '+0000000042'))
        self.assertEqual(self._format('%-+010.10d', -42), (11, '-0000000042'))
        self.assertEqual(self._format('%- 010.8d', 42), (10, ' 00000042 '))
        self.assertEqual(self._format('%- 010.8d', -42), (10, '-00000042 '))
        self.assertEqual(self._format('%- 010.10d', 42), (11, ' 0000000042'))
        self.assertEqual(self._format('%- 010.10d', -42), (11, '-0000000042'))
        self.assertEqual(self._format('%-+01024.8d', 123456, bufsize=2048),
                         (1024, '+00123456' + ' ' * 1015))

    def test_format_unsigned(self):
        self.assertEqual(self._format('%u', 0), (1, '0'))
        self.assertEqual(self._format('%u', 7), (1, '7'))
        self.assertEqual(self._format('%u', 1234567), (7, '1234567'))
        self.assertEqual(self._format('%u', 2**28), (9, '268435456'))
        self.assertEqual(self._format('%u + %u = %u', 11, 27, 11 + 27),
                         (12, '11 + 27 = 38'))

    def test_format_unsigned_flags(self):
        # Space and sign flags have no effect on unsigned values.
        self.assertEqual(self._format('% u', 0), (1, '0'))
        self.assertEqual(self._format('% u', 144), (3, '144'))
        self.assertEqual(self._format('%+u', 0), (1, '0'))
        self.assertEqual(self._format('%+u', 144), (3, '144'))
        self.assertEqual(self._format('% +u', 0), (1, '0'))
        self.assertEqual(self._format('% +u', 144), (3, '144'))

    def test_format_unsigned_precision(self):
        self.assertEqual(self._format('%.u', 8675309), (7, '8675309'))
        self.assertEqual(self._format('%.4u', 8675309), (7, '8675309'))
        self.assertEqual(self._format('%.10u', 8675309), (10, '0008675309'))
        self.assertEqual(self._format('%.u', 0), (1, '0'))
        self.assertEqual(self._format('%.1u', 0), (1, '0'))
        self.assertEqual(self._format('%.2u', 0), (2, '00'))
        self.assertEqual(self._format('%.1024u', 13, bufsize=2048),
                         (1024, '0' * 1022 + '13'))

    def test_format_unsigned_width(self):
        self.assertEqual(self._format('%2u', 4), (2, ' 4'))
        self.assertEqual(self._format('%8.u', 22), (8, '      22'))
        self.assertEqual(self._format('%8.4u', 22), (8, '    0022'))
        self.assertEqual(self._format('%1024.8u', 123456, bufsize=2048),
                         (1024, ' ' * 1016 + '00123456'))

    def test_format_unsigned_width_ladjust(self):
        self.assertEqual(self._format('%-2u', 4), (2, '4 '))
        self.assertEqual(self._format('%-8.u', 22), (8, '22      '))
        self.assertEqual(self._format('%-8.4u', 22), (8, '0022    '))
        self.assertEqual(self._format('%-1024.8u', 123456, bufsize=2048),
                         (1024, '00123456' + ' ' * 1016))

    def test_format_unsigned_width_zero(self):
        self.assertEqual(self._format('%02u', 4), (2, '04'))
        self.assertEqual(self._format('%06u', 11), (6, '000011'))
        self.assertEqual(self._format('%08.u', 42), (8, '00000042'))
        self.assertEqual(self._format('%08.8u', 42), (8, '00000042'))
        self.assertEqual(self._format('%08.10u', 42), (10, '0000000042'))
        self.assertEqual(self._format('%01024.8u', 123456, bufsize=2048),
                         (1024, '0' * 1016 + '00123456'))

    def test_format_octal(self):
        self.assertEqual(self._format('%o', 0), (1, '0'))
        self.assertEqual(self._format('%o', 12), (2, '14'))
        self.assertEqual(self._format('%o', 1234567), (7, '4553207'))
        self.assertEqual(self._format('%o', 2**28), (10, '2000000000'))
        self.assertEqual(self._format('...because dec %d = oct %o', 25, 25),
                         (26, '...because dec 25 = oct 31'))

    def test_format_octal_special(self):
        self.assertEqual(self._format('%#o', 0), (1, '0'))
        self.assertEqual(self._format('%#o', 12), (3, '014'))
        self.assertEqual(self._format('%#o', 1234567), (8, '04553207'))
        self.assertEqual(self._format('%#o', 2**28), (11, '02000000000'))

    def test_format_octal_precision(self):
        self.assertEqual(self._format('%.o', 0), (1, '0'))
        self.assertEqual(self._format('%.4o', 0), (4, '0000'))
        self.assertEqual(self._format('%.4o', 8), (4, '0010'))
        self.assertEqual(self._format('%.2o', 17), (2, '21'))
        self.assertEqual(self._format('%#.2o', 17), (3, '021'))

    def test_format_octal_width(self):
        self.assertEqual(self._format('%8o', 0), (8, '       0'))
        self.assertEqual(self._format('%8o', 8), (8, '      10'))
        self.assertEqual(self._format('%2o', 17), (2, '21'))
        self.assertEqual(self._format('%8.3o', 0), (8, '     000'))
        self.assertEqual(self._format('%8.3o', 8), (8, '     010'))
        self.assertEqual(self._format('%2.3o', 17), (3, '021'))
        self.assertEqual(self._format('%#8.3o', 0), (8, '     000'))
        self.assertEqual(self._format('%#8.3o', 8), (8, '     010'))
        self.assertEqual(self._format('%#2.3o', 17), (3, '021'))

    def test_format_octal_width_ladjust(self):
        self.assertEqual(self._format('%-8o', 0), (8, '0       '))
        self.assertEqual(self._format('%-8o', 8), (8, '10      '))
        self.assertEqual(self._format('%-2o', 17), (2, '21'))
        self.assertEqual(self._format('%-8.3o', 0), (8, '000     '))
        self.assertEqual(self._format('%-8.3o', 8), (8, '010     '))
        self.assertEqual(self._format('%-2.3o', 17), (3, '021'))
        self.assertEqual(self._format('%#-8.3o', 0), (8, '000     '))
        self.assertEqual(self._format('%#-8.3o', 8), (8, '010     '))
        self.assertEqual(self._format('%#-2.3o', 17), (3, '021'))

    def test_format_octal_width_zero(self):
        self.assertEqual(self._format('%08o', 0), (8, '00000000'))
        self.assertEqual(self._format('%08o', 8), (8, '00000010'))
        self.assertEqual(self._format('%02o', 17), (2, '21'))
        self.assertEqual(self._format('%08.3o', 0), (8, '00000000'))
        self.assertEqual(self._format('%08.3o', 8), (8, '00000010'))
        self.assertEqual(self._format('%02.3o', 17), (3, '021'))
        self.assertEqual(self._format('%#08.3o', 0), (8, '00000000'))
        self.assertEqual(self._format('%#08.3o', 8), (8, '00000010'))
        self.assertEqual(self._format('%#02.3o', 17), (3, '021'))

    def test_format_hex(self):
        self.assertEqual(self._format('%x', 0), (1, '0'))
        self.assertEqual(self._format('%x', 14), (1, 'e'))
        self.assertEqual(self._format('%x', 16), (2, '10'))
        self.assertEqual(self._format('%x', 0xdeadbeef), (8, 'deadbeef'))
        self.assertEqual(self._format('%x', 2**16 - 1), (4, 'ffff'))

    def test_format_hex_upper(self):
        self.assertEqual(self._format('%X', 0), (1, '0'))
        self.assertEqual(self._format('%X', 14), (1, 'E'))
        self.assertEqual(self._format('%X', 16), (2, '10'))
        self.assertEqual(self._format('%X', 0xdeadbeef), (8, 'DEADBEEF'))
        self.assertEqual(self._format('%X', 2**16 - 1), (4, 'FFFF'))

    def test_format_hex_special(self):
        self.assertEqual(self._format('%#x', 0), (1, '0'))
        self.assertEqual(self._format('%#x', 14), (3, '0xe'))
        self.assertEqual(self._format('%#x', 16), (4, '0x10'))
        self.assertEqual(self._format('%#x', 0xdeadbeef), (10, '0xdeadbeef'))
        self.assertEqual(self._format('%#X', 14), (3, '0XE'))
        self.assertEqual(self._format('%#X', 16), (4, '0X10'))
        self.assertEqual(self._format('%#X', 0xdeadbeef), (10, '0XDEADBEEF'))

    def test_format_hex_width(self):
        self.assertEqual(self._format('%4x', 0), (4, '   0'))
        self.assertEqual(self._format('%4x', 14), (4, '   e'))
        self.assertEqual(self._format('%4x', 16), (4, '  10'))
        self.assertEqual(self._format('%4x', 0xdeadbeef), (8, 'deadbeef'))
        self.assertEqual(self._format('%12x', 0xdeadbeef),
                         (12, '    deadbeef'))
        self.assertEqual(self._format('%#4x', 0), (4, '   0'))
        self.assertEqual(self._format('%#4x', 14), (4, ' 0xe'))
        self.assertEqual(self._format('%#4x', 16), (4, '0x10'))
        self.assertEqual(self._format('%#4x', 0xdeadbeef), (10, '0xdeadbeef'))
        self.assertEqual(self._format('%#12x', 0xdeadbeef),
                         (12, '  0xdeadbeef'))
        self.assertEqual(self._format('%#4X', 14), (4, ' 0XE'))
        self.assertEqual(self._format('%#4X', 16), (4, '0X10'))
        self.assertEqual(self._format('%#4X', 0xdeadbeef), (10, '0XDEADBEEF'))
        self.assertEqual(self._format('%#12X', 0xdeadbeef),
                         (12, '  0XDEADBEEF'))

    def test_format_hex_width_ladjust(self):
        self.assertEqual(self._format('%-4x', 0), (4, '0   '))
        self.assertEqual(self._format('%-4x', 14), (4, 'e   '))
        self.assertEqual(self._format('%-4x', 16), (4, '10  '))
        self.assertEqual(self._format('%-4x', 0xdeadbeef), (8, 'deadbeef'))
        self.assertEqual(self._format('%-12x', 0xdeadbeef),
                         (12, 'deadbeef    '))
        self.assertEqual(self._format('%#-4x', 0), (4, '0   '))
        self.assertEqual(self._format('%#-4x', 14), (4, '0xe '))
        self.assertEqual(self._format('%#-4x', 16), (4, '0x10'))
        self.assertEqual(self._format('%#-4x', 0xdeadbeef), (10, '0xdeadbeef'))
        self.assertEqual(self._format('%#-12x', 0xdeadbeef),
                         (12, '0xdeadbeef  '))
        self.assertEqual(self._format('%#-4X', 14), (4, '0XE '))
        self.assertEqual(self._format('%#-4X', 16), (4, '0X10'))
        self.assertEqual(self._format('%#-4X', 0xdeadbeef), (10, '0XDEADBEEF'))
        self.assertEqual(self._format('%#-12X', 0xdeadbeef),
                         (12, '0XDEADBEEF  '))

    def test_format_hex_width_zero(self):
        self.assertEqual(self._format('%04x', 0), (4, '0000'))
        self.assertEqual(self._format('%04x', 14), (4, '000e'))
        self.assertEqual(self._format('%04x', 16), (4, '0010'))
        self.assertEqual(self._format('%04x', 0xdeadbeef), (8, 'deadbeef'))
        self.assertEqual(self._format('%012x', 0xdeadbeef),
                         (12, '0000deadbeef'))
        self.assertEqual(self._format('%#04x', 0), (4, '0000'))
        self.assertEqual(self._format('%#04x', 14), (4, '0x0e'))
        self.assertEqual(self._format('%#04x', 16), (4, '0x10'))
        self.assertEqual(self._format('%#04x', 0xdeadbeef), (10, '0xdeadbeef'))
        self.assertEqual(self._format('%#012x', 0xdeadbeef),
                         (12, '0x00deadbeef'))
        self.assertEqual(self._format('%#04X', 14), (4, '0X0E'))
        self.assertEqual(self._format('%#04X', 16), (4, '0X10'))
        self.assertEqual(self._format('%#04X', 0xdeadbeef), (10, '0XDEADBEEF'))
        self.assertEqual(self._format('%#012X', 0xdeadbeef),
                         (12, '0X00DEADBEEF'))

    def test_format_pointer(self):
        self.assertEqual(self._format('%p', ctypes.c_void_p(0)), (1, '0'))
        self.assertEqual(self._format('%p', ctypes.c_void_p(0xcff02340)),
                         (10, '0xcff02340'))
        self.assertEqual(
            self._format('&foo is %p', ctypes.c_void_p(0x084083f0)),
            (17, '&foo is 0x84083f0'))

    def test_format_short_limits(self):
        short_min, short_max = c_int_limits(ctypes.c_short)
        min_str, max_str = str(short_min), str(short_max)
        self.assertEqual(self._format('%hd', short_min),
                         (len(min_str), min_str))
        self.assertEqual(self._format('%hd', short_max),
                         (len(max_str), max_str))

    def test_format_unsigned_short_limits(self):
        short_min, short_max = c_int_limits(ctypes.c_ushort)

        min_str, max_str = str(short_min), str(short_max)
        self.assertEqual(self._format('%hu', short_min),
                         (len(min_str), min_str))
        self.assertEqual(self._format('%hu', short_max),
                         (len(max_str), max_str))

        max_hex = hex(short_max)
        self.assertEqual(self._format('%#hx', short_min), (1, '0'))
        self.assertEqual(self._format('%#hx', short_max),
                         (len(max_hex), max_hex))

    def test_format_int_limits(self):
        int_min, int_max = c_int_limits(ctypes.c_int)
        min_str, max_str = str(int_min), str(int_max)
        self.assertEqual(self._format('%d', int_min), (len(min_str), min_str))
        self.assertEqual(self._format('%d', int_max), (len(max_str), max_str))

    def test_format_unsigned_int_limits(self):
        int_min, int_max = c_int_limits(ctypes.c_uint)

        min_str, max_str = str(int_min), str(int_max)
        self.assertEqual(self._format('%u', int_min), (len(min_str), min_str))
        self.assertEqual(self._format('%u', int_max), (len(max_str), max_str))

        max_hex = hex(int_max)
        self.assertEqual(self._format('%#x', int_min), (1, '0'))
        self.assertEqual(self._format('%#x', int_max), (len(max_hex), max_hex))

    def test_format_long_limits(self):
        long_min, long_max = c_int_limits(ctypes.c_long)
        min_str, max_str = str(long_min), str(long_max)
        self.assertEqual(self._format('%ld', ctypes.c_long(long_min)),
                         (len(min_str), min_str))
        self.assertEqual(self._format('%ld', ctypes.c_long(long_max)),
                         (len(max_str), max_str))

    def test_format_unsigned_long_limits(self):
        long_min, long_max = c_int_limits(ctypes.c_ulong)

        min_str, max_str = str(long_min), str(long_max)
        self.assertEqual(self._format('%lu', ctypes.c_ulong(long_min)),
                         (len(min_str), min_str))
        self.assertEqual(self._format('%lu', ctypes.c_ulong(long_max)),
                         (len(max_str), max_str))

        max_hex = hex(long_max)
        self.assertEqual(self._format('%#lx', ctypes.c_ulong(long_min)),
                         (1, '0'))
        self.assertEqual(self._format('%#lx', ctypes.c_ulong(long_max)),
                         (len(max_hex), max_hex))

    def test_format_long_long_limits(self):
        long_long_min, long_long_max = c_int_limits(ctypes.c_longlong)
        min_str, max_str = str(long_long_min), str(long_long_max)
        self.assertEqual(
            self._format('%lld', ctypes.c_longlong(long_long_min)),
            (len(min_str), min_str))
        self.assertEqual(
            self._format('%lld', ctypes.c_longlong(long_long_max)),
            (len(max_str), max_str))

    def test_format_unsigned_long_long_limits(self):
        long_long_min, long_long_max = c_int_limits(ctypes.c_ulonglong)

        min_str, max_str = str(long_long_min), str(long_long_max)
        self.assertEqual(
            self._format('%llu', ctypes.c_ulonglong(long_long_min)),
            (len(min_str), min_str))
        self.assertEqual(
            self._format('%llu', ctypes.c_ulonglong(long_long_max)),
            (len(max_str), max_str))

        max_hex = hex(long_long_max)
        self.assertEqual(
            self._format('%#lx', ctypes.c_ulonglong(long_long_min)), (1, '0'))
        self.assertEqual(
            self._format('%#lx', ctypes.c_ulonglong(long_long_max)),
            (len(max_hex), max_hex))

    def test_format_percent(self):
        self.assertEqual(self._format('loading: 10%%!'), (13, 'loading: 10%!'))

    def test_invalid_format_sequence(self):
        with self.assertErrno(22):
            self.assertEqual(self._format('%')[0], -1)
        with self.assertErrno(22):
            self.assertEqual(self._format('%0')[0], -1)
        with self.assertErrno(22):
            self.assertEqual(self._format('%%%.')[0], -1)
        with self.assertErrno(22):
            self.assertEqual(
                self._format('foo: %#08.4ll bar: %#08.4llx')[0], -1)


if __name__ == '__main__':
    unittest.main()
