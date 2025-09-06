# backjoon
n = 6
nums = [10, 20,10,30,20,50]
dp = [1] * n

for i in range(n):
    for j in range(i+1, n):
        if nums[j] > nums[i]:
            dp[j] = max(dp[j], dp[i] + 1)
            
print(max(dp))