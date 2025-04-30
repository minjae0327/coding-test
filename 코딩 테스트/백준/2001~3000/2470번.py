n = int(input())
nums = list(map(int, input().split()))
target = float("inf")

nums = sorted(nums)

L = 0
R = n-1

result1 = 0
result2 = 0

while L < R:
    answer = nums[L] + nums[R]
    
    if target > abs(answer):
        target = abs(answer)
        result1 = L
        result2 = R
    
    if answer < 0:
        L += 1
    elif answer > 0:
        R -= 1
    else:
        break
        
print(nums[result1], nums[result2])