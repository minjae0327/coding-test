# backjoon
import sys

input = sys.stdin.readline

n = int(input())
steps = []
for i in range(1, n+1):
    steps.append(int(input()))

dp = [[0, 0] for _ in range(n+1)]

dp[0] = [0, 0]
dp[1] = [steps[0], 0]

for i in range(2, n+1):
    dp[i][0] = max(dp[i-2][0], dp[i-2][1])  + steps[i-1]
    dp[i][1] = dp[i-1][0] + steps[i-1]

print(max(dp[-1]))