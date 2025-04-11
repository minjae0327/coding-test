# backjoon
n = int(input())
count = 0

dp = [0] * (n + 1)

for i in range(1, n + 1):
    dp[i] = i  # 최악의 경우 1^2을 i번 더함
    j = 1
    while j * j <= i:
        dp[i] = min(dp[i], dp[i - j*j] + 1)
        j += 1

print(dp[n])