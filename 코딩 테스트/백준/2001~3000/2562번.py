def find_first_position(nums, maxi):
    for x, num in enumerate(nums):
        if num == maxi:
            return x + 1
        
nums = []

for i in range(9):
    nums.append(int(input()))
    
maxi = max(nums)
print(maxi)
print(find_first_position(nums, maxi))
