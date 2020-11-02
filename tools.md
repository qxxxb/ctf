# Tools

## Binary

### `gdb`
- See [tools/gdb.md](tools/gdb.md)

### [pwntools]
Library for exploit development.

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

### [requests]
Library for using HTTP requests. Good for developing exploit scripts.

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
A repository with 3 tools for websites with `.git` repositories available.

[pwntools]: https://github.com/Gallopsled/pwntools
[Wireshark]: https://www.wireshark.org/
[ghidra]: https://ghidra-sre.org/
[fernflower]: https://github.com/fesh0r/fernflower
[nmap]: https://nmap.org/
[requests]: https://github.com/psf/requests
[nikto]: https://github.com/sullo/nikto
[GitTools]: https://github.com/internetwache/GitTools
[metasploit]: https://www.metasploit.com/
[sqlmap]: http://sqlmap.org/
[radare2]: https://www.radare.org/r/
