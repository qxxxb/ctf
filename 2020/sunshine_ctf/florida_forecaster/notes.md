Suspicious compares in `forecast`
With the right input, we can print out the address of `test_processing_unit`.
We can use this address to calculate the address of the flag code.

Found suspicious `y.init0` function (renamed to `sus_func`)
- It has an unconditional jump at the start to some random code
- After that are instructions that print the flag
- The instructions after the `exit` are used to handle the signal.
- After `I'm only going to warn you once`, it sets the alarm again but for some
  reason the signal handler is in the middle of the `.bss` section that causes a SEGFAULT

Only thing that's left: How do we hijack control flow?
We can overflow the buffer in the `test_processing_unit` function, but stack
canaries are enabled. Do we have to bypass the stack canaries?

Do we have to use `alarm` and `signal`?
