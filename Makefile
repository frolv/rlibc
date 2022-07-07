# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.

TARGET ?= x86

ifeq ($(TARGET), x86)
	TOOLCHAIN_PREFIX := i686-radix
endif

CC := $(TOOLCHAIN_PREFIX)-gcc
AR := $(TOOLCHAIN_PREFIX)-ar

# Tools used to compile code for unit tests, which run on the host machine.
TEST_CC ?= gcc
TEST_LD ?= ld

RM := rm -f

BUILD_DIR := build
INCLUDE_DIR := include
TARGET_DIR := target/$(TARGET)
TARGET_INCLUDE_DIR := $(TARGET_DIR)/include

OPT_LEVEL ?= -O2

_FLAGS := -Wall -Wextra -Werror -Wimplicit-fallthrough -Wundef \
          -ffreestanding $(OPT_LEVEL)
CPPFLAGS := -I$(INCLUDE_DIR) -I$(TARGET_INCLUDE_DIR)
CFLAGS := $(_FLAGS) -std=c11 -Wstrict-prototypes

RADIX_FLAGS ?=
LIBK_FLAGS := -D__radix_kernel__ $(RADIX_FLAGS)

PREFIX ?=

# Source directories for libc.
LIBC_DIRS := ctype errno stdio string

LIBC_SRCS := $(foreach dir,$(LIBC_DIRS),$(wildcard $(dir)/*.c))
LIBC_OBJS := $(patsubst %.c,$(BUILD_DIR)/%.o,$(LIBC_SRCS))
LIBC_BUILD_DIRS := $(addprefix $(BUILD_DIR)/,$(LIBC_DIRS))

LIBK_OBJS := $(patsubst %.c,$(BUILD_DIR)/%.k.o,$(LIBC_SRCS))
LIBK_BIN := $(BUILD_DIR)/libk.a

TEST_OBJS := $(patsubst %.c,$(BUILD_DIR)/%.test.o,$(LIBC_SRCS))
TEST_BIN := $(BUILD_DIR)/test_rlibc.so
TEST_LDFLAGS := -shared -Bsymbolic -z nodefaultlib

# The final binary files to produce.
BINS := libc.a

STARTFILES := crti.o crtn.o crt0.o

BINS := $(addprefix $(BUILD_DIR)/,$(BINS))
STARTFILES := $(addprefix $(BUILD_DIR)/,$(STARTFILES))

all: build-libs

.PHONY: clean
clean: clean-libs clean-tests

.PHONY: build-libs
build-libs: build-dirs
	@$(MAKE) --no-print-directory libs

.PHONY: build-libk
build-libk: build-dirs
	@$(MAKE) --no-print-directory libk

.PHONY: test-lib
test-lib: build-dirs
	@$(MAKE) --no-print-directory $(TEST_BIN)

.PHONY: libs
libs: $(BINS) $(STARTFILES)

.PHONY: libk
libk: $(LIBK_BIN)

.PHONY: build-dirs
build-dirs: $(BUILD_DIR) $(LIBC_BUILD_DIRS)

.PHONY: install
install: build-libs
	mkdir -p $(PREFIX)/include
	mkdir -p $(PREFIX)/lib
	cp -RT $(INCLUDE_DIR) $(PREFIX)/include
	cp -RT $(TARGET_INCLUDE_DIR) $(PREFIX)/include
	cp $(BINS) $(PREFIX)/lib
	cp $(STARTFILES) $(PREFIX)/lib

$(BUILD_DIR)/libc.a: $(LIBC_OBJS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/crti.o: $(TARGET_DIR)/crti.S
	$(CC) -c $< -o $@ $(ASFLAGS)

$(BUILD_DIR)/crtn.o: $(TARGET_DIR)/crtn.S
	$(CC) -c $< -o $@ $(ASFLAGS)

$(BUILD_DIR)/crt0.o: $(TARGET_DIR)/crt0.S
	$(CC) -c $< -o $@ $(ASFLAGS)

$(LIBK_BIN): $(LIBK_OBJS)
	$(AR) rcs $@ $^

$(TEST_BIN): $(TEST_OBJS)
	$(TEST_LD) $(TEST_LDFLAGS) -o $@ $^

$(BUILD_DIR):
	mkdir -p $@

$(LIBC_BUILD_DIRS):
	mkdir -p $@

$(BUILD_DIR)/%.o: %.c
	$(CC) -c $< -o $@ $(CPPFLAGS) $(CFLAGS)

$(BUILD_DIR)/%.k.o: %.c
	$(CC) -c $< -o $@ $(CPPFLAGS) $(CFLAGS) $(LIBK_FLAGS)

$(BUILD_DIR)/%.test.o: %.c
	$(TEST_CC) -c $< -o $@ $(CPPFLAGS) $(CFLAGS) -fPIC

clean-libs:
	$(RM) $(LIBC_OBJS)
	$(RM) $(BINS)
	$(RM) $(STARTFILES)

clean-libk:
	$(RM) $(LIBK_OBJS)
	$(RM) $(LIBK_BIN)

clean-tests:
	$(RM) $(TEST_OBJS)
	$(RM) $(TEST_BIN)
