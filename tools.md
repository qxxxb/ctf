# Tools

## Binary

### `gdb`

#### Plugins
- [pwndbg]

#### Control flow

- `run`
  - Start debugged program

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

- `c`
  - Continue program being debugged

- `u` (`until`)
  - Continue running until a source line past the current line, in the current
    stack frame, is reached
  - Useful for stepping out of a loop

- `fin` (`finish`)
  - Execute until stack frame returns

- `starti`
  - Run and break at entry point

- `ni`, `si`
  - Step one instruction (with and without subroutine calls respectively)

#### Examination

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

#### Misc
- `refresh`
  - Refresh the window
  - Helpful when the TUI gets messed-up by program IO

### `objdump`
Display information from object files
- `objdump -d a.out`
  - Disassembles executable sections

## Forensics

### `file`
Determine file type
- Displays information about binary executables

### `binwalk`
Tool for searching binary images for embedded files and executable code
- Can also be used to extract embedded files
  - `binwalk data --dd='.*'`
  - Not sure why the `-e` (`--extract`) parameter doesn't seem to work

### [Wireshark]
Network protocol analyzer.
- Deep inspection of hundreds of protocols
- Live capture and offline analysis

## Reverse engineering

### [ghidra]
A software reverse engineering (SRE) suite of tools developed by NSA's Research
Directorate in support of the Cybersecurity mission

### [radare2]
- Tutorial: https://www.megabeets.net/a-journey-into-radare-2-part-1/
- https://radare.gitbooks.io/radare2book/content/first_steps/basic_debugger_session.html
- https://reverseengineering.stackexchange.com/a/11208

### [fernflower]
Fernflower is the first actually working analytical decompiler for Java and
probably for a high-level programming language in general

## Web

### [nmap]
Network exploration tool and security / port scanner
- It was designed to rapidly scan large networks, although it works fine
  against single hosts.
- Nmap uses raw IP packets in novel ways to determine:
  - What hosts are available on the network
  - What services (application name and version) those hosts are offering
  - What operating systems (and OS versions) they are running
  - What type of packet filters/firewalls are in use
  - and dozens of other characteristics.
- While Nmap is commonly used for security audits, many systems and network
  administrators find it useful for routine tasks such as network inventory,
  managing service upgrade schedules, and monitoring host or service uptime.
- Examples:
  - `nmap -v -A pwn.osucyber.club -Pn -p13370-13380`
    - `-v`: verbose
    - `-A`: Enable OS detection, version detection, script scanning, and
      traceroute
    - `-Pn`: Treat all hosts as online
    - `-p13370-13380`: Scan ports in range `13370` to `13380`

### [nikto]
Web server scanner which performs comprehensive tests against web servers for
multiple items:
- Over 6700 potentially dangerous files/programs
- Checks for outdated versions of over 1250 servers
- Version specific problems on over 270 servers
- Checks for server configuration items such as:
    - Multiple index files
    - HTTP server options
- Will attempt to identify installed web servers and software

### [metasploit]
Metasploit is a penetration testing platform that enables you to find, exploit,
and validate vulnerabilities.

### [sqlmap]
Automates the process of detecting and exploiting SQL injection flaws and
taking over of database servers.

### [GitTools]
A repository with 3 tools for pwning websites with `.git` repositories available

[Wireshark]: https://www.wireshark.org/
[ghidra]: https://ghidra-sre.org/
[fernflower]: https://github.com/fesh0r/fernflower
[nmap]: https://nmap.org/
[nikto]: https://github.com/sullo/nikto
[GitTools]: https://github.com/internetwache/GitTools
[metasploit]: https://www.metasploit.com/
[sqlmap]: http://sqlmap.org/
[radare2]: https://www.radare.org/r/
[pwndbg]: https://github.com/pwndbg/pwndbg
