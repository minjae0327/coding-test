# backjoon
def set_test():
    dp[1] = 1
    dp[2] = 2
    dp[3] = 4
    
    for i in range(4, 11+1):
        dp[i] = dp[i-1]+dp[i-2]+dp[i-3]

T = int(input())
nums = []
dp = [0] * (12)
set_test()

for i in range(T):
    nums.append(int(input()))
    
for i in nums:
    result = dp[i]
    print(result)