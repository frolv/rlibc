// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/memory.h>

#include <stdlib.h>
#include <string.h>

char *strdup(const char *s)
{
    size_t len = strlen(s);

    char *t = malloc(len + 1);
    if (t != NULL) {
        __rc_copy_bytes_fwd((void *)t, (const void *)s, len);
        t[len] = '\0';
    }

    return t;
}
