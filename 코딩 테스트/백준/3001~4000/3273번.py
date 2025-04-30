n = int(input())
nums = list(map(int, input().split()))
target = int(input())

nums = sorted(nums)

L = 0
R = n-1
count = 0

while L < R:
    answer = nums[L] + nums[R]
    
    if answer == target:
        count += 1
        L += 1
        R -= 1
    elif answer > target:
        R -= 1
    else:
        L += 1
        
print(count)