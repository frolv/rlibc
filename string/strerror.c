// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/compiler.h>

#include <errno.h>
#include <stdlib.h>
#include <string.h>

struct errno_descriptor {
    int value;
    const char *name;
    char *description;
};

#define ERRNO_DESC(errnum, description) \
    {                                   \
        errnum, #errnum, description,   \
    }

// Store the names, values, and descriptions of every errno constant in a table
// which can be read by external programs.
__RC_SECTION(".rlibc_errno_table") const
    struct errno_descriptor __rlibc_errno_descriptors[ERRNO_MAX + 1] = {
        {0, "OK", "Success"},
        ERRNO_DESC(EPERM, "Operation not permitted"),
        ERRNO_DESC(ENOENT, "No such file or directory"),
        ERRNO_DESC(ESRCH, "No such process"),
        ERRNO_DESC(EINTR, "Operation interrupted"),
        ERRNO_DESC(EIO, "I/O error"),
        ERRNO_DESC(ENXIO, "No such device or address"),
        ERRNO_DESC(E2BIG, "Argument list too long"),
        ERRNO_DESC(ENOEXEC, "Executable format error"),
        ERRNO_DESC(EBADF, "Bad file"),
        ERRNO_DESC(ECHILD, "No child processes"),
        ERRNO_DESC(EAGAIN, "Try again"),
        ERRNO_DESC(ENOMEM, "Out of memory"),
        ERRNO_DESC(EACCES, "Permission denied"),
        ERRNO_DESC(EFAULT, "Bad address"),
        ERRNO_DESC(ENOTBLK, "Not a block device"),
        ERRNO_DESC(EBUSY, "Device or resource busy"),
        ERRNO_DESC(EEXIST, "File already exists"),
        ERRNO_DESC(EXDEV, "Cross-device link"),
        ERRNO_DESC(ENODEV, "No such device"),
        ERRNO_DESC(ENOTDIR, "Not a directory"),
        ERRNO_DESC(EISDIR, "Is a directory"),
        ERRNO_DESC(EINVAL, "Invalid argument"),
        ERRNO_DESC(ENFILE, "File table overflow"),
        ERRNO_DESC(EMFILE, "Too many open files"),
        ERRNO_DESC(ENOTTY, "Not a TTY"),
        ERRNO_DESC(ETXTBSY, "Text file busy"),
        ERRNO_DESC(EFBIG, "File too large"),
        ERRNO_DESC(ENOSPC, "No space left on device"),
        ERRNO_DESC(ESPIPE, "Illegal seek"),
        ERRNO_DESC(EROFS, "Read-only file system"),
};

const size_t __rlibc_errno_descriptors_size =
    sizeof __rlibc_errno_descriptors / sizeof __rlibc_errno_descriptors[0];

char *strerror(int errnum)
{
    if (errnum > ERRNO_MAX) {
        return "Unknown error";
    }

    return __rlibc_errno_descriptors[errnum].description;
}
