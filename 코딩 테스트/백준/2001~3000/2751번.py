import sys

input = sys.stdin.readline

n = int(input())
nums = []

for i in range(n):
    nums.append(int(input()))
    
nums = sorted(nums)

for num in nums:
    print(num)