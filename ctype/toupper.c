// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <ctype.h>

int toupper(int c) { return islower(c) ? c ^ 32 : c; }
