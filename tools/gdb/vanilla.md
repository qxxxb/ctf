# Vanilla GDB commands

- `run`: Start debugged program

- `b`
  - Set breakpoint at specified location
  - Examples
    - `b *0x08048536`
      - Set breakpoint at `0x08048536`. The `*` tells gdb that it's an address
    - `b some_func`
      - Set breakpoint at `some_func`
    - `tb some_func`
      - Set a temporary breakpoint at `some_func` that is used only once

- `disable [breakpoints]`
  - Disable `breakpoints`, or all if none specified

- `enable [breakpoints]`
  - Enable `brekapoints`, or all if none specified

- `watch`
  - Set a watchpoint for an expression
  - A watchpoint stops execution of the program whenever the value of an
    expression changes

- `condition`
  - Specify a breakpoint to stop only if a condition is true

- `n`, `s`
  - Step program (with and without subroutine calls respectively)

- `c`: Continue program being debugged

- `u` (`until`)
  - Continue running until a source line past the current line, in the current
    stack frame, is reached
  - Useful for stepping out of a loop

- `fin` (`finish`): Execute until stack frame returns

- `starti`: Run and break at entry point

- `ni`, `si`
  - Step one instruction (with and without subroutine calls respectively)

## Examination

- `x`
  - Examine memory
  - Examples:
    - `x/12wx 0x800000`
      - Prints twelve 4-byte words in hexadecimal starting at `0x800000`
    - `x/6gx 0x080000`
      - Prints six 8-byte giant words in hexadecimal starting at `0x800000`
    - `x/12wx $rsp`
      - Prints twelve 4-byte words in hexadecimal starting at the address
        stored in `rsp`. This will print the contents of the stack starting
        from the top.

- `bt`
  - Print backtrace of all stack frames
  - Useful for stack smashing and finding source of crashes

- `frame [frame-selection]`
  - Select a frame
  - After selecting a frame, you can print variables at that frame
  - Useful for debugging crashes
  - Prints info on the current frame when run without arguments

- `i f` (`info frame`)
  - Print info on stack frame

- `i r` (`info register`)
  - Print info on registers
  - Examples:
    - `i r rdi`
      - Print info on `rdi`

- `layout asm`
  - Show assembly instructions

- `disassemble`
  - Disassemble a specified section of memory
  - Examples:
    - `disassemble main`
    - `disassemble some_func`

## Misc
- `refresh`
  - Refresh the window
  - Helpful when the TUI gets messed-up by program IO

- `objdump`
  - Display information from object files
  - `objdump -d a.out`
    - Disassembles executable sections
