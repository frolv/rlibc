# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.

TARGET ?= x86

ifeq ($(TARGET), x86)
	TOOLCHAIN_PREFIX := i686-elf
endif

CC := $(TOOLCHAIN_PREFIX)-gcc
AR := $(TOOLCHAIN_PREFIX)-ar

RM := rm -f

BUILD_DIR := build
INCLUDE_DIR := include
TARGET_INCLUDE_DIR := target/$(TARGET)/include

OPT_LEVEL ?= -O2

_FLAGS := -Wall -Wextra -Werror -Wimplicit-fallthrough -Wundef \
          -ffreestanding $(OPT_LEVEL)
CPPFLAGS := -I$(INCLUDE_DIR) -I$(TARGET_INCLUDE_DIR)
CFLAGS := $(_FLAGS) -std=c11 -Wstrict-prototypes

RADIX_FLAGS ?=
LIBK_FLAGS := -D__radix_kernel__ $(RADIX_FLAGS)

# Source directories for libc.
LIBC_DIRS := string

LIBC_SRCS := $(foreach dir,$(LIBC_DIRS),$(wildcard $(dir)/*.c))
LIBC_OBJS := $(patsubst %.c,$(BUILD_DIR)/%.o,$(LIBC_SRCS))
LIBC_BUILD_DIRS := $(addprefix $(BUILD_DIR)/,$(LIBC_DIRS))

LIBK_OBJS := $(patsubst %.c,$(BUILD_DIR)/%.k.o,$(LIBC_SRCS))
LIBK_BIN := $(BUILD_DIR)/libk.a

# The final binary files to produce.
BINS := libc.a

BINS := $(addprefix $(BUILD_DIR)/,$(BINS))

all: build-libs

.PHONY: clean
clean: clean-libs

.PHONY: build-libs
build-libs: build-dirs
	@$(MAKE) --no-print-directory libs

.PHONY: build-libk
build-libk: build-dirs
	@$(MAKE) --no-print-directory libk

.PHONY: libs
libs: $(BINS)

.PHONY: libk
libk: $(LIBK_BIN)

.PHONY: build-dirs
build-dirs: $(BUILD_DIR) $(LIBC_BUILD_DIRS)

$(BUILD_DIR)/libc.a: $(LIBC_OBJS)
	$(AR) rcs $@ $^

$(LIBK_BIN): $(LIBK_OBJS)
	$(AR) rcs $@ $^

$(BUILD_DIR):
	mkdir -p $@

$(LIBC_BUILD_DIRS):
	mkdir -p $@

$(BUILD_DIR)/%.o: %.c
	$(CC) -c $< -o $@ $(CPPFLAGS) $(CFLAGS)

$(BUILD_DIR)/%.k.o: %.c
	$(CC) -c $< -o $@ $(CPPFLAGS) $(CFLAGS) $(LIBK_FLAGS)

clean-libs:
	$(RM) $(LIBC_OBJS)
	$(RM) $(BINS)

clean-libk:
	$(RM) $(LIBK_OBJS)
	$(RM) $(LIBK_BIN)