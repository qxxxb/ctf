# Biggest Lowest

**Category**: Programming \
**Points**: 37 \
**Author**: Gabies, Nutu

## Challenge

I see you're eager to prove yourself, why not try your luck with this problem?

Target: `nc challs.xmas.htsp.ro 6051`

## Solution

```
$ nc challs.xmas.htsp.ro 6051
So you think you have what it takes to be a good programmer?
Then solve this super hardcore task:
Given an array print the first k1 smallest elements of the array in increasing order and then the first k2 elements of the array in decreasing order.
You have 50 tests that you'll gave to answer in maximum 45 seconds, GO!
Here's an example of the format in which a response should be provided:
1, 2, 3; 10, 9, 8

Test number: 1/50
array = [10, 7, 6, 10, 7]
k1 = 4
k2 = 3
```

What data structure is good for keeping track of mins and maxes? HEAPS!!! \
How do you keep track of both the min and max values? Use TWO HEAPS!!!

Solution in `solve.py`

```
...
[DEBUG] Sent 0x49a bytes:
    b'1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 16, 16, 17, 18, 18, 18, 18, 18, 19, 19, 20, 20, 20, 21, 21, 22, 22, 22, 23, 23, 23, 23, 23, 24, 24, 25, 25, 25, 25, 26, 26, 27, 27, 28, 28, 28, 29, 29, 29, 29, 30, 30, 31, 32, 32, 32, 32, 32, 32, 33, 34, 34, 34, 34, 34, 34, 35, 36, 36, 36, 37, 37, 37, 37, 38, 38, 38, 38, 39, 39, 39, 39, 39, 40, 40, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 45, 45, 45, 46, 46, 46, 46, 47, 47, 47, 48, 48, 49, 49, 49, 49, 50, 50, 50, 50, 51, 51, 52, 52, 52, 53, 53, 54, 54, 54, 55, 55; 500, 500, 500, 500, 500, 500, 500, 499, 499, 499, 498, 498, 498, 497, 497, 497, 497, 497, 497, 497, 496, 496, 495, 495, 495, 495, 494, 494, 494, 493, 493, 492, 492, 492, 491, 491, 491, 490, 490, 490, 489, 489, 489, 488, 487, 487, 487, 486, 486, 485, 485, 485, 484, 484, 483, 482, 482, 482, 482, 482, 482, 482, 482, 481, 481, 481, 480, 480, 479, 479, 478, 478, 477, 477, 477, 477, 477, 476, 476, 475, 475, 475, 475, 474, 474, 473, 473, 473, 472, 472, 472, 472, 472, 472, 471, 471, 471, 470, 470, 470, 470, 470, 469, 468, 468\n'
[DEBUG] Received 0x9c bytes:
    b"Good, that's right!\n"
    b"Those are some was lightning quick reflexes you've got there!\n"
    b" Here's your flag: X-MAS{th15_i5_4_h34p_pr0bl3m_bu7_17'5_n0t_4_pwn_ch41l}\n"
[*] Switching to interactive mode
Those are some was lightning quick reflexes you've got there!
 Here's your flag: X-MAS{th15_i5_4_h34p_pr0bl3m_bu7_17'5_n0t_4_pwn_ch41l}
```
