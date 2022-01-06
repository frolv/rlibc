# radix libc

The C standard library implementation used by
[radix](https://github.com/frolv/radix).

## Testing

Unit tests for rlibc are run through Python. The code is compiled to a shared
library for the host system (e.g. Linux), which is then loaded and tested using
Python's `ctypes` module.

To compile the test library, run

```
$ make test-lib
```

Following this, individual test scripts can be run:

```
$ python tests/string_test.py
```
