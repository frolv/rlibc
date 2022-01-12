// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <string.h>

char *strrev(char *s)
{
    char *start = s;
    char *t = s + strlen(s) - 1;

    while (s < t) {
        char tmp = *s;
        *s = *t;
        *t = tmp;

        ++s;
        --t;
    }

    return start;
}
