	.file	"overflow.c"
	.text
	.section	.rodata
.LC0:
	.string	"Enter your name:"
.LC1:
	.string	"Welcome, %s\n"
.LC2:
	.string	"/bin/bash"
	.align 8
.LC3:
	.string	"Sorry %s, check value %x is incorrect.\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	stdout(%rip), %rax
	movl	$0, %ecx
	movl	$2, %edx
	movl	$0, %esi
	movq	%rax, %rdi
	call	setvbuf@PLT
	movl	$0, -36(%rbp)
	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	leaq	-32(%rbp), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	gets@PLT
	cmpl	$-889275714, -36(%rbp)
	jne	.L2
	leaq	-32(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC1(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	.LC2(%rip), %rdi
	call	system@PLT
	jmp	.L3
.L2:
	movl	-36(%rbp), %edx
	leaq	-32(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC3(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
.L3:
	movl	$0, %eax
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L5
	call	__stack_chk_fail@PLT
.L5:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
