# Copyright 2022 Alexei Frolov
#
# Use of this source code is governed by an MIT-style license
# that can be found in the LICENSE file in the repository root.

# Entrypoint for x86 radix programs.
.global _start
.type _start, @function
_start:
	xorl %ebp, %ebp
	push %ebp
	push %ebp
	movl %esp, %ebp

	# Run global static initialization.
	call _init

	# Invoke the program's main function, storing its return value on the
	# stack.
	# TODO(frolv): Add arguments to main.
	push $0  # argv
	push $0  # argc
	call main
	addl $8, %esp
	push %eax

	# Run global cleanup.
	call _fini

	# Finish by invoking the exit() syscall (0 in eax) with the return value
	# of main as the sole argument (in ecx).
	# TODO(frolv): This is temporary. A proper exit function and syscall
	# layer should be implemented.
	popl %ecx
	xorl %eax, %eax
	int $222
