n, m = 4, 3
table = [
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [3, 4, 5, 6],
    [4, 5, 6, 7]
]
coords = [
    [2, 2, 3, 4],
    [3, 4, 3, 4],
    [1, 1, 4, 4]
]

dp = [[0 for _ in range(n)] for _ in range(n)]

for i in range(n):
    for j in range(n):
        if j == 0:
            if i > 0:
                dp[i][j] = table[i][j] + dp[i-1][j-1]
            else:
                dp[i][j] = table[i][j] + dp[i-1][j]
        else:
            dp[i][j] = table[i][j] + dp[i][j-1] + dp[i-1][j] + dp[i-1][j-1]
            
print(dp)