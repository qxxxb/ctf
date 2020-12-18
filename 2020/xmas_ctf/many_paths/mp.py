# Source: https://stackoverflow.com/a/26284607/6759699

from numpy.core.numeric import binary_repr, identity, asanyarray, dot


def matrix_power_mod(M, n, mod_val):
    # Implementation shadows numpy's matrix_power, but with modulo included
    M = asanyarray(M)
    if len(M.shape) != 2 or M.shape[0] != M.shape[1]:
        raise ValueError("input  must be a square array")

    from numpy.linalg import inv

    if n == 0:
        M = M.copy()
        M[:] = identity(M.shape[0])
        return M
    elif n < 0:
        M = inv(M)
        n *= -1

    result = M % mod_val
    if n <= 3:
        for _ in range(n - 1):
            result = dot(result, M) % mod_val
        return result

    # binary decompositon to reduce the number of matrix
    # multiplications for n > 3
    beta = binary_repr(n)
    Z, q, t = M, 0, len(beta)
    while beta[t - q - 1] == '0':
        Z = dot(Z, Z) % mod_val
        q += 1
    result = Z
    for k in range(q + 1, t):
        Z = dot(Z, Z) % mod_val
        if beta[t - k - 1] == '1':
            result = dot(result, Z) % mod_val
    return result % mod_val
