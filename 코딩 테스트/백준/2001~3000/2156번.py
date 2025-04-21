n = int(input())

wines = [0] * n
for i in range(n):
    wines[i] = int(input())

dp = [[0]*3 for _ in range(n+1)]

dp[1][0] = 0
dp[1][1] = wines[0]   # drink glass 1, no previous
dp[1][2] = 0          # cannot have two in a row yet

for i in range(2, n+1):
    w = wines[i-1]
    
    dp[i][0] = max(dp[i-1])        
    dp[i][1] = dp[i-1][0] + w     
    dp[i][2] = dp[i-1][1] + w           

print( max(dp[n]) )