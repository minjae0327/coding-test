import sys

input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().split()))
lis_dp = [1] * n
lds_dp = [1] * n

# LIS
for i in range(n):
    for j in range(i):
        if nums[i] > nums[j]:
            lis_dp[i] = max(lis_dp[i], lis_dp[j] + 1)

# LDS(뒤에서 감소)
for i in range(n-1, -1, -1):
    for j in range(n-1, i, -1):
        if nums[i] > nums[j]:
            lds_dp[i] = max(lds_dp[i], lds_dp[j] + 1)

print(max(lis_dp[i] + lds_dp[i] - 1 for i in range(n)))