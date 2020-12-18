import pwn
import math

def make_v(v_1, N, a, c, mod):
    '''Use recurrence relation to create v'''
    v = [0] * (N + 1)
    v[1] = v_1
    for i in range(2, N + 1):
        v[i] = (a * v[i - 1] + c) % mod

    v = v[1:]
    return v

def sim(v, speeds):
    '''
    Count days using direct simulation.
    Implemented by stdnoerror.
    '''
    n_fast, fast, slow = speeds
    days = 0
    i = 0
    while len(v) > 0:
        days += 1
        v.sort(reverse=True)

        # Assign the fastest bots to the most busy rooms
        xs = v[:n_fast]
        xs = [x - fast for x in xs]

        # Assign the slowest bots to the least busy rooms
        ys = v[n_fast:]
        ys = [y - slow for y in ys]

        # Combine and remove completed rooms
        zs = xs + ys
        v = [z for z in zs if z >= 0]
        i += 1

    return days

def can_finish(v, days, speeds):
    n_fast, fast, slow = speeds

    def min_n_fast(x, days):
        # F: fast, S: slow
        # ans*F + (days - ans)*S = x
        # ans*F - ans*S + days*S = x
        # ans*(F-S) = x - days*S
        # ans = (x - days*S) / (F-S)
        ans = math.ceil((x - days * slow) / (fast - slow))
        return max(ans, 0)

    n_fast_needed = 0
    for x in v:
        # If there is a single day that cannot finish, return false
        if x > days * fast:
            return False
        n_fast_needed += min_n_fast(x, days)

    return (n_fast * days) >= n_fast_needed


def solve(v, speeds):
    n_fast, fast, slow = speeds

    m = max(v)
    lo = m // fast
    hi = m // slow

    while True:
        mid = (lo + hi) // 2
        if can_finish(v, mid, speeds):
            # Passed, try a lower time
            hi = mid
            if mid <= lo:
                return mid
        else:
            # Didn't pass, try a higher time
            lo = mid + 1

def get_speeds(N, K, P, Q):
    if P > Q:
        n_fast, fast, slow = K, P, Q
    else:
        n_fast, fast, slow = N - K, Q, P

    return (n_fast, fast, slow)

if __name__ == '__main__':
    io = pwn.remote('challs.xmas.htsp.ro', 6055)
    pwn.context.log_level = 'debug'

    for i in range(100):
        print('Attempt', i)
        io.recvregex(f'Test number: [0-9]*/100\n')
        s = io.recvuntilS('\n\n')
        s = s.replace(',', ';')
        s = s.replace('v[1]', 'v_1')
        exec(s)

        v = make_v(v_1, N, a, c, mod)
        speeds = get_speeds(N, K, P, Q)

        days = solve(v, speeds)
        io.sendline(str(days))

    io.interactive()

