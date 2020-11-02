# `gdb`

## Setup
- [gdb/vanilla.md](gdb/vanilla.md)
- [pwndbg]
  - Usage examples:
    - https://tc.gts3.org/cs6265/2019/tut/tut02-warmup2.html
    - https://blog.xpnsec.com/pwndbg/
    - https://www.ins1gn1a.com/basics-of-gdb-and-pwndbg/

## Basics

- `start`: Start at entry point of program
- `main`: Jump to main
- `ctx`: Print context (registers, source, disassembly, backtrace, etc.)
  - `stack`: Print the stack
- `nearpc`: Show code near the PC (seems to be the same as `u`)
- `hexdump <addr> <nbytes>`: Dump `nbytes` starting at `addr`
- `cyclic <length>`: Create a cyclic string `length` long
  - Useful for calulating offsets in payloads
  - `cyclic -l <string>`: Find the offset where `<string>` is
- `search`: Find stuff
- `r2`: Launch [radare2]

[radare2]: https://www.radare.org/r/
[pwndbg]: https://github.com/pwndbg/pwndbg
