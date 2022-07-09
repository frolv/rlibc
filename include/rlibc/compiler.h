// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_RLIBC_COMPILER_H
#define RLIBC_RLIBC_COMPILER_H

#define __RC_STRINGIFY_EXPAND(x) #x
#define __RC_STRINGIFY(x) __RC_STRINGIFY_EXPAND(x)

#if defined(__GNUC__) || defined(__clang__)

#define __RC_PRINTF(format_index, arg_index) \
    __attribute__((format(printf, format_index, arg_index)))

#define __RC_SECTION(section_name) __attribute__((section(section_name)))

#define __RC_NORETURN __attribute__((noreturn))
#define __RC_UNUSED   __attribute__((unused))

#else  // defined(__GNUC__) || defined(__clang__)

#define __RC_PRINTF(format_index, arg_index)
#define __RC_SECTION(section_name)
#define __RC_NORETURN
#define __RC_UNUSED

#endif  // defined(__GNUC__) || defined(__clang__)

#endif  // RLIBC_RLIBC_COMPILER_H
