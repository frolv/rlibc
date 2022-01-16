// Copyright 2022 Alexei Frolov
//
// Use of this source code is governed by an MIT-style license
// that can be found in the LICENSE file in the repository root.

#include <rlibc/util.h>

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "printf.h"

enum format_type {
    FORMAT_NONE,
    FORMAT_CHAR,
    FORMAT_STRING,
    FORMAT_INT,
    FORMAT_UINT,
    FORMAT_POINTER,
    FORMAT_PERCENT,
};

#define FLAGS_ZERO      (1 << 0)  // Zero-pad a formatted number.
#define FLAGS_SPECIAL   (1 << 1)  // Add special characters.
#define FLAGS_LADJUST   (1 << 2)  // Left-adjust a padded value.
#define FLAGS_SPACE     (1 << 3)  // Leave a space before a nonnegative number.
#define FLAGS_SIGN      (1 << 4)  // Always place a sign before a number.
#define FLAGS_LOWER     (1 << 5)  // Use lowercase hex formatting.
#define FLAGS_SHORT     (1 << 6)  // Format a short int.
#define FLAGS_LONG      (1 << 7)  // Format a long int.
#define FLAGS_LONG_LONG (1 << 8)  // Format a long long int.

struct printf_format {
    enum format_type type;
    uint32_t flags;
    uint32_t base;
    int32_t precision;
    int32_t width;
};

// Reads a positive base 10 integer from a string, advancing the string pointer
// past the read number.
static int atoi_skip(const char **format)
{
    int value = 0;

    while (isdigit(**format)) {
        value = value * 10 + (**format - '0');
        ++*format;
    }

    return value;
}

// Parses a printf format sequence from a string. The string passed to this
// function should point to the first character following the initial '%' of the
// format sequence.
//
// Returns the length of the parsed sequence on success, or -1 if the sequence
// is invalid.
static int parse_format_sequence(const char *format, struct printf_format *p)
{
    const char *start = format;

    p->type = FORMAT_NONE;
    p->flags = 0;
    p->base = 10;
    p->width = -1;
    p->precision = -1;

    // The literal percent format specifier is "%%", without any modifiers.
    if (*format == '%') {
        p->type = FORMAT_PERCENT;
        return 1;
    }

    // First, parse any special flag characters from the format sequence.
    while (true) {
        if (*format == '\0') {
            return -1;
        }

        if (*format == '0') {
            p->flags |= FLAGS_ZERO;
        } else if (*format == '#') {
            p->flags |= FLAGS_SPECIAL;
        } else if (*format == '-') {
            p->flags |= FLAGS_LADJUST;
        } else if (*format == ' ') {
            p->flags |= FLAGS_SPACE;
        } else if (*format == '+') {
            p->flags |= FLAGS_SIGN;
        } else {
            break;
        }

        ++format;
    }

    // Following flags is the optional padded width of the field.
    if (isdigit(*format)) {
        p->width = atoi_skip(&format);
    }

    // After the width, the precision may be specified prepended by a period.
    if (*format == '.') {
        ++format;
        p->precision = atoi_skip(&format);
    }

    // Next are optional length modifiers.
    switch (*format) {
    case 'h':
        p->flags |= FLAGS_SHORT;
        ++format;
        break;

    case 'l':
        p->flags |= FLAGS_LONG;
        ++format;
        if (*format == 'l') {
            p->flags |= FLAGS_LONG_LONG;
            ++format;
        }
        break;

    default:
        break;
    }

    switch (*format) {
    case 'c':
        p->type = FORMAT_CHAR;
        break;
    case 'd':
    case 'i':
        p->type = FORMAT_INT;
        break;
    case 'o':
        p->type = FORMAT_UINT;
        p->base = 8;
        break;
    case 'p':
        p->type = FORMAT_POINTER;
        p->base = 16;
        p->flags |= FLAGS_SPECIAL | FLAGS_LOWER;
        break;
    case 's':
        p->type = FORMAT_STRING;
        break;
    case 'u':
        p->type = FORMAT_UINT;
        break;
    case 'x':
        p->flags |= FLAGS_LOWER;
        // Fallthrough.
    case 'X':
        p->type = FORMAT_UINT;
        p->base = 16;
        break;
    default:
        return -1;
    }

    ++format;
    return format - start;
}

static size_t pad_chars(printf_callback callback,
                        void *context,
                        char c,
                        size_t amount)
{
    char buffer[128];
    size_t total_size = 0;

    while (amount > 0) {
        size_t curr_size = min(amount, sizeof buffer);
        memset(buffer, c, curr_size);
        total_size += callback(context, buffer, curr_size);
        amount -= curr_size;
    }

    return total_size;
}

static int format_char(printf_callback callback,
                       void *context,
                       char c,
                       const struct printf_format *p)
{
    size_t size = 0;

    if (p->flags & FLAGS_LADJUST) {
        size += callback(context, &c, 1);
    }

    if (p->width > 1) {
        size += pad_chars(callback, context, ' ', p->width - 1);
    }

    if (!(p->flags & FLAGS_LADJUST)) {
        size += callback(context, &c, 1);
    }

    return size;
}

static int format_string(printf_callback callback,
                         void *context,
                         const char *string,
                         const struct printf_format *p)
{
    if (!string) {
        string = "(null)";
    }

    size_t len = strlen(string);
    if (p->precision >= 0 && (size_t)p->precision < len) {
        len = p->precision;
    }

    size_t size = 0;

    if (p->flags & FLAGS_LADJUST) {
        size += callback(context, string, len);
    }

    if (p->width > (int)len) {
        size += pad_chars(callback, context, ' ', p->width - len);
    }

    if (!(p->flags & FLAGS_LADJUST)) {
        size += callback(context, string, len);
    }

    return size;
}

static size_t print_number(printf_callback callback,
                           void *context,
                           const char *prefix,
                           int zeros,
                           const char *number_buffer,
                           size_t number_length)
{
    size_t size = 0;

    if (prefix) {
        size += callback(context, prefix, strlen(prefix));
    }

    if (zeros > 0) {
        size += pad_chars(callback, context, '0', zeros);
    }

    size += callback(context, number_buffer, number_length);
    return size;
}

static int format_number(printf_callback callback,
                         void *context,
                         const char *prefix,
                         uint64_t value,
                         const struct printf_format *p)
{
    char buffer[32];
    char *pos = buffer;

    const char *digits = "0123456789ABCDEF";
    do {
        char c = digits[value % p->base];
        *pos++ = (p->flags & FLAGS_LOWER) ? tolower(c) : c;
        value /= p->base;
    } while (value > 0);

    *pos = '\0';
    strrev(buffer);

    size_t value_size = pos - buffer;
    size_t zeros_to_pad =
        p->precision > (int)value_size ? p->precision - value_size : 0;

    if (p->base == 8 && prefix != NULL && zeros_to_pad > 0) {
        // Octal prefix is "0", which counts towards the total amount of zeros.
        --zeros_to_pad;
    }

    size_t total_size = value_size + zeros_to_pad;
    if (prefix != NULL) {
        total_size += strlen(prefix);
    }

    // If both '0' and '-' flags are provided, left-adjust takes precedence.
    if ((p->flags & (FLAGS_ZERO | FLAGS_LADJUST)) == FLAGS_ZERO) {
        // If the width is to be zero-padded, a prefix must come before all of
        // the zeros (precision and width).
        if ((int)total_size < p->width) {
            zeros_to_pad += p->width - total_size;
        }

        return print_number(
            callback, context, prefix, zeros_to_pad, buffer, value_size);
    }

    size_t size = 0;

    if (p->flags & FLAGS_LADJUST) {
        size += print_number(
            callback, context, prefix, zeros_to_pad, buffer, value_size);
    }

    if (p->width > (int)total_size) {
        size += pad_chars(callback, context, ' ', p->width - total_size);
    }

    if (!(p->flags & FLAGS_LADJUST)) {
        size += print_number(
            callback, context, prefix, zeros_to_pad, buffer, value_size);
    }

    return size;
}

static int format_signed(printf_callback callback,
                         void *context,
                         int64_t value,
                         const struct printf_format *p)
{
    const char *prefix = NULL;
    if (value < 0) {
        prefix = "-";
        if (value != INT64_MIN) {
            value = -value;
        }
    } else if (p->flags & FLAGS_SIGN) {
        prefix = "+";
    } else if (p->flags & FLAGS_SPACE) {
        prefix = " ";
    }

    return format_number(callback, context, prefix, value, p);
}

static int format_unsigned(printf_callback callback,
                           void *context,
                           uint64_t value,
                           const struct printf_format *p)
{
    const char *prefix = NULL;
    if (p->flags & FLAGS_SPECIAL && value != 0) {
        if (p->base == 8) {
            prefix = "0";
        } else if (p->base == 16) {
            prefix = (p->flags & FLAGS_LOWER) ? "0x" : "0X";
        }
    }

    return format_number(callback, context, prefix, value, p);
}

#define VA_SIGNED_INT(ap, printf)                                    \
    ({                                                               \
        ((printf)->flags & FLAGS_LONG_LONG) ? va_arg(ap, long long)  \
        : ((printf)->flags & FLAGS_LONG)    ? va_arg(ap, long)       \
        : ((printf)->flags & FLAGS_SHORT)   ? (short)va_arg(ap, int) \
                                            : va_arg(ap, int);         \
    })

#define VA_UNSIGNED_INT(ap, printf)                                          \
    ({                                                                       \
        ((printf)->flags & FLAGS_LONG_LONG) ? va_arg(ap, unsigned long long) \
        : ((printf)->flags & FLAGS_LONG)    ? va_arg(ap, unsigned long)      \
        : ((printf)->flags & FLAGS_SHORT)                                    \
            ? (unsigned short)va_arg(ap, unsigned int)                       \
            : va_arg(ap, unsigned int);                                      \
    })

int rc_callback_printf(printf_callback callback,
                       void *context,
                       const char *__restrict format,
                       va_list ap)
{
    const char *start = format;
    int n = 0;

    while (*format != '\0') {
        if (*format != '%') {
            ++format;
            continue;
        }

        if (format != start) {
            n += callback(context, start, format - start);
        }

        // Skip the percent sign.
        ++format;

        struct printf_format p;
        int format_size = parse_format_sequence(format, &p);
        if (format_size == -1) {
            // errno = EINVAL;
            return -1;
        }

        switch (p.type) {
        case FORMAT_CHAR:
            n += format_char(callback, context, va_arg(ap, int), &p);
            break;

        case FORMAT_STRING:
            n += format_string(callback, context, va_arg(ap, const char *), &p);
            break;

        case FORMAT_INT:
            n += format_signed(callback, context, VA_SIGNED_INT(ap, &p), &p);
            break;

        case FORMAT_UINT:
            n +=
                format_unsigned(callback, context, VA_UNSIGNED_INT(ap, &p), &p);
            break;

        case FORMAT_POINTER:
            n += format_unsigned(
                callback, context, (uintptr_t)va_arg(ap, const void *), &p);
            break;

        case FORMAT_PERCENT: {
            const char percent = '%';
            n += callback(context, &percent, 1);
            break;
        }

        case FORMAT_NONE:
            // errno = EINVAL;
            return -1;
        }

        format += format_size;
        start = format;
    }

    if (format != start) {
        n += callback(context, start, format - start);
    }

    return n;
}
