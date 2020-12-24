*EAX  0x804a000 (_GLOBAL_OFFSET_TABLE_) —▸ 0x8049f10 (_DYNAMIC) ◂— 0x1

► 0x804851b <vuln+26>    call   gets@plt <gets@plt>
       arg[0]: 0xffffc5fe ◂— 0x35390000
       arg[1]: 0xffffc64c ◂— '1234567890123\n'
       arg[2]: 0x12
       arg[3]: 0x804850d (vuln+12) ◂— add    eax, 0x1af3

system addr: 0x08048390

ret addr offset: 62
