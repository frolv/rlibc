# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.

BUILD_DIR := build
INCLUDE_DIR := include

TARGET ?= i686-elf

CC := $(TARGET)-gcc
AR := $(TARGET)-ar

RM := rm -f

OPT_LEVEL ?= -O2

_FLAGS := -Wall -Wextra -Werror -Wimplicit-fallthrough -ffreestanding \
          $(OPT_LEVEL)
CPPFLAGS := -I$(INCLUDE_DIR)
CFLAGS := $(_FLAGS) -std=c11 -Wstrict-prototypes

# Source directories for libc.
LIBC_DIRS := string

LIBC_SRCS := $(foreach dir,$(LIBC_DIRS),$(wildcard $(dir)/*.c))
LIBC_OBJS := $(patsubst %.c,$(BUILD_DIR)/%.o,$(LIBC_SRCS))
LIBC_BUILD_DIRS := $(addprefix $(BUILD_DIR)/,$(LIBC_DIRS))

# The final binary files to produce.
BINS := libc.a

BINS := $(addprefix $(BUILD_DIR)/,$(BINS))

all: libs

clean: clean-libs

libs: $(BINS)

build_dirs: $(BUILD_DIR) $(LIBC_BUILD_DIRS)

$(BUILD_DIR)/libc.a: $(LIBC_OBJS)
	$(AR) rcs $@ $^

$(BUILD_DIR):
	mkdir -p $@

$(LIBC_BUILD_DIRS):
	mkdir -p $@

$(BUILD_DIR)/%.o: %.c build_dirs
	$(CC) -c $< -o $@ $(CPPFLAGS) $(CFLAGS)

clean-libs:
	$(RM) $(LIBC_OBJS) $(LIBC_DEPS)
	$(RM) $(BINS)
