// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_COMPILER_H
#define RLIBC_RLIBC_COMPILER_H

#if defined(__GNUC__) || defined(__clang__)

#define __rc_printf(format_index, arg_index) \
    __attribute__((format(printf, format_index, arg_index)))

#define __rc_section(section_name) __attribute__((section(section_name)))

#define __rc_unused __attribute__((unused))

#else  // defined(__GNUC__) || defined(__clang__)

#define __rc_printf(format_index, arg_index)
#define __rc_section(section_name)
#define __rc_unused

#endif  // defined(__GNUC__) || defined(__clang__)

#endif  // RLIBC_RLIBC_COMPILER_H
