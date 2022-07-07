# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.

.section .init
.global _init
.type _init, @function
_init:
	push %ebp
	movl %esp, %ebp

.section .fini
.global _fini
.type _fini, @function
_fini:
	push %ebp
	movl %esp, %ebp
