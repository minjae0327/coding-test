n = int(input())
a, b, c = map(int, input().split())
max_dp = [a, b, c]
min_dp = [a, b, c]

for _ in range(n-1):
    a, b, c = map(int, input().split())

    new_max_0 = max(max_dp[0], max_dp[1]) + a
    new_max_1 = max(max_dp[0], max_dp[1], max_dp[2]) + b
    new_max_2 = max(max_dp[1], max_dp[2]) + c

    new_min_0 = min(min_dp[0], min_dp[1]) + a
    new_min_1 = min(min_dp[0], min_dp[1], min_dp[2]) + b
    new_min_2 = min(min_dp[1], min_dp[2]) + c

    max_dp = [new_max_0, new_max_1, new_max_2]
    min_dp = [new_min_0, new_min_1, new_min_2]

print(max(max_dp), min(min_dp))