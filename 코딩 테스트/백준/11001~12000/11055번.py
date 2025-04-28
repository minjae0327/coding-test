import sys

input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().split()))
dp = [0] * n

for i in range(n):
    dp[i] = nums[i]  # 초기화 : 자기 자신만으로 수열을 만들었을 때 합

    for j in range(i):
        if nums[i] > nums[j]:
            dp[i] = max(dp[i], dp[j] + nums[i])

print(max(dp))
