n = int(input())

lines = [0] * n
dp = [1] * n

for i in range(n):
    lines[i] = list(map(int, input().split()))
lines = sorted(lines)
    
#LIS
for i in range(n):
    for j in range(i):
        if lines[i][1] > lines[j][1]:
            dp[i] = max(dp[j]+1, dp[i])
            
print(n-max(dp))