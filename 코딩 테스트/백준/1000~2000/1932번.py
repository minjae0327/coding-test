# backjoon
import sys

input = sys.stdin.readline

n = int(input())
pyramid = [list(map(int, input().split())) for _ in range(n)]

dp = [[0] * len(row) for row in pyramid]
dp[0] = pyramid[0]

for floor in range(1, n):
    for j in range(floor+1):
        if j==0:
            dp[floor][0] = pyramid[floor][0] + dp[floor-1][0]
        elif floor==j:
            dp[floor][j] = pyramid[floor][j] + dp[floor-1][j-1]
        else:
            num1 = pyramid[floor][j] + dp[floor-1][j]
            num2 = pyramid[floor][j] + dp[floor-1][j-1]
            dp[floor][j] = max(num1, num2)
            
    

print(max(dp[n-1]))