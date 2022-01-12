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
    FORMAT_PERCENT,
};

#define FLAGS_LOWER     (1 << 0)  // Use lowercase hex formatting.
#define FLAGS_SHORT     (1 << 1)  // Format a short int.
#define FLAGS_LONG      (1 << 2)  // Format a long int.
#define FLAGS_LONG_LONG (1 << 3)  // Format a long long int.
#define FLAGS_ZERO      (1 << 4)  // Zero-pad a formatted number.
#define FLAGS_SPECIAL   (1 << 5)  // Add special characters.
#define FLAGS_LADJUST   (1 << 6)  // Left-adjust a padded value.
#define FLAGS_SPACE     (1 << 7)  // Leave a space before a positive number.
#define FLAGS_SIGN      (1 << 8)  // Always place a sign before a number.

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

    switch (*format) {
    case 'c':
        p->type = FORMAT_CHAR;
        break;
    case 's':
        p->type = FORMAT_STRING;
        break;
    default:
        return -1;
    }

    ++format;
    return format - start;
}

static size_t pad_spaces(printf_callback callback, void *context, size_t amount)
{
    char buffer[128];
    size_t total_size = 0;

    while (amount > 0) {
        size_t curr_size = min(amount, sizeof buffer);
        memset(buffer, ' ', curr_size);
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
        size += pad_spaces(callback, context, p->width - 1);
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
        size += pad_spaces(callback, context, p->width - len);
    }

    if (!(p->flags & FLAGS_LADJUST)) {
        size += callback(context, string, len);
    }

    return size;
}

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
        case FORMAT_UINT:
            break;

        case FORMAT_PERCENT: {
            char percent = '%';
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
