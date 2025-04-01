# backjoon
n = int(input())

dp = [0] * n
dp[0] = 1

for i in range(1, n):
    if i == 1:
        dp[i] = 2
    else:
        dp[i] = dp[i-1] + dp[i-2]
        
print(dp[n-1] % 10007)
