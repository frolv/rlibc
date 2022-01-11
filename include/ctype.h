// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#ifndef RLIBC_CTYPE_H
#define RLIBC_CTYPE_H

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

int isalnum(int c);
int isalpha(int c);
int isdigit(int c);

int islower(int c);
int isupper(int c);

#ifdef __cplusplus
}
#endif  // __cplusplus

#endif  // RLIBC_CTYPE_H
