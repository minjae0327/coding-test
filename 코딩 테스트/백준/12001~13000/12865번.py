# backjoon
import sys

input = sys.stdin.readline

n, k = map(int, input().split())
stuffs = [list(map(int, input().split())) for _ in range(n)]

dp = [[0 for _ in range(k + 1)] for _ in range(n + 1)]

for i in range(1, n + 1):
    weight = stuffs[i-1][0]
    value = stuffs[i-1][1]
    
    for j in range(k + 1):
        if j < weight:
            dp[i][j] = dp[i - 1][j]
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weight] + value)

print(dp[n][k])