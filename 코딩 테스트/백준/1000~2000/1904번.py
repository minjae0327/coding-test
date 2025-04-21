MOD = 15746

def multiply(A, B):
    C = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
    return C

def power(matrix, n):
    result = [[1, 0], [0, 1]]
    base = matrix

    while n > 0:
        if n % 2 == 1:
            result = multiply(result, base)
        base = multiply(base, base)
        n //= 2
    return result

n = int(input())

if n <= 0:
    print(0)
elif n == 1:
    print(1)
else:
    base_matrix = [[1, 1], [1, 0]]
    final_matrix = power(base_matrix, n)

    print(final_matrix[0][0])