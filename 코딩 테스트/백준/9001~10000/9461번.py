# backjoon
import sys

input = sys.stdin.readline
t = int(input())
nums=[]
for i in range(t):
    nums.append(int(input().strip()))
    

dp = [0] * 101
dp[1] = 1
dp[2] = 1
dp[3] = 1
dp[4] = 2

for i in range(5, 100 + 1):
    dp[i] = dp[i-1] + dp[i-5]

for i in nums:
    print(dp[i])